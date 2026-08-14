#!/usr/bin/env python3
"""Normalize v3.1 matcher attestation into a canonical provenance wrapper."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CLOUD = ROOT / "tests/benchmark/v3_1-holdout/cloud-cases"
SOURCE_MATCHES = CLOUD / "matches-v31.json"
SOURCE_ATTESTATION = CLOUD / "matcher-attestation-v31.json"
CANONICAL_MATCHES = CLOUD / "matches-v31-canonical.json"
CANONICAL_ATTESTATION = CLOUD / "matcher-attestation-v31-canonical.json"
GOLD_LABELER_FAMILIES = {"grok", "kimi", "gpt"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def decision_tuple(decision: dict) -> tuple:
    match_type = decision.get("match_type", decision.get("match"))
    return (
        decision["claim_id"],
        decision["concept_id"],
        match_type,
        decision["confidence"],
        decision["rationale"],
    )


def main() -> None:
    source_matches = json.loads(SOURCE_MATCHES.read_text(encoding="utf-8"))
    source_attestation = json.loads(SOURCE_ATTESTATION.read_text(encoding="utf-8"))
    matches = deepcopy(source_matches)
    source_decisions = [
        decision_tuple(decision)
        for case in source_matches["cases"]
        for turn in case["turn_matches"]
        for domain in ("question_matches", "revision_matches")
        for decision in turn[domain]
    ]
    for case in matches["cases"]:
        for turn in case["turn_matches"]:
            for domain in ("question_matches", "revision_matches"):
                for decision in turn[domain]:
                    if "match" in decision:
                        decision["match_type"] = decision.pop("match")
    matcher = dict(source_matches["matcher"])
    matcher["model_id"] = "unverified"
    matcher["gold_access"] = True
    family = matcher["model_family"]
    if family in GOLD_LABELER_FAMILIES:
        raise RuntimeError(f"matcher family duplicates gold labeler: {family}")
    matches["matcher"] = matcher
    canonical_decisions = [
        decision_tuple(decision)
        for case in matches["cases"]
        for turn in case["turn_matches"]
        for domain in ("question_matches", "revision_matches")
        for decision in turn[domain]
    ]
    if canonical_decisions != source_decisions:
        raise RuntimeError("normalization changed semantic match decisions")
    CANONICAL_MATCHES.write_text(
        json.dumps(matches, indent=2) + "\n", encoding="utf-8"
    )

    files_read = source_attestation.get("files_read", [])
    limitations = source_attestation.get("limitations", [])
    if isinstance(limitations, str):
        limitations = [limitations]
    limitations = [
        str(item)
        for item in limitations
        if str(item) and str(item).strip().lower() != "none"
    ]
    attestation = {
        "schema_version": "v3.1",
        "role": "matcher",
        "context_id": matcher["context_id"],
        "model_id": "unverified",
        "model_family": family,
        "cloud_branch": source_attestation.get(
            "branch", source_attestation.get("cloud_branch", "")
        ),
        "cloud_commit": source_attestation.get(
            "output_commit", source_attestation.get("cloud_commit", "")
        ),
        "gold_access": True,
        "files_read": files_read,
        "output": {
            "path": relative(CANONICAL_MATCHES),
            "sha256": digest(CANONICAL_MATCHES),
        },
        "source_attestation": {
            "path": relative(SOURCE_ATTESTATION),
            "sha256": digest(SOURCE_ATTESTATION),
        },
        "limitations": limitations
        + [
            "Machine model ID was unavailable from cloud run metadata; no ID was guessed.",
            "Transcript audit disposition is recorded in matcher-protocol-audits.json.",
        ],
        "normalization": {
            "kind": "mechanical-provenance-wrapper",
            "match_decisions_changed": False,
        },
    }
    CANONICAL_ATTESTATION.write_text(
        json.dumps(attestation, indent=2) + "\n", encoding="utf-8"
    )
    print("normalized matcher provenance without changing match decisions")


if __name__ == "__main__":
    main()
