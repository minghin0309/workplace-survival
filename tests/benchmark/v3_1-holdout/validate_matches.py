#!/usr/bin/env python3
"""Validate v3.1 semantic matches against frozen extractions, gold, and ontology."""

from __future__ import annotations

import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tests/benchmark"))

import score_semantic


CLOUD = ROOT / "tests/benchmark/v3_1-holdout/cloud-cases"
GOLD_LABELER_FAMILIES = {"grok", "kimi", "gpt"}
ALLOWLIST = {
    "tests/benchmark/v3_1-holdout/cloud-cases/extractions-manifest-v31.json": CLOUD
    / "extractions-manifest-v31.json",
    "tests/benchmark/v3_1-holdout/cloud-cases/evaluations-v31-canonical.json": CLOUD
    / "evaluations-v31-canonical.json",
    "tests/benchmark/v3_1-holdout/cloud-cases/outputs-v31-raw.json": CLOUD
    / "outputs-v31-raw.json",
    "tests/benchmark/v3_1-holdout/cloud-cases/gold-v31.json": CLOUD / "gold-v31.json",
    "tests/benchmark/SEMANTIC_ONTOLOGY.json": ROOT / "tests/benchmark/SEMANTIC_ONTOLOGY.json",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def unique(items: list[dict], key: str) -> dict:
    values = {item[key]: item for item in items}
    require(len(values) == len(items), f"duplicate {key}")
    return values


def main() -> None:
    snapshot_path = ALLOWLIST[
        "tests/benchmark/v3_1-holdout/cloud-cases/extractions-manifest-v31.json"
    ]
    evaluations_path = ALLOWLIST[
        "tests/benchmark/v3_1-holdout/cloud-cases/evaluations-v31-canonical.json"
    ]
    outputs_path = ALLOWLIST[
        "tests/benchmark/v3_1-holdout/cloud-cases/outputs-v31-raw.json"
    ]
    gold_path = ALLOWLIST["tests/benchmark/v3_1-holdout/cloud-cases/gold-v31.json"]
    ontology_path = ALLOWLIST["tests/benchmark/SEMANTIC_ONTOLOGY.json"]
    matches_path = CLOUD / "matches-v31-canonical.json"
    source_matches_path = CLOUD / "matches-v31.json"
    attestation_path = CLOUD / "matcher-attestation-v31-canonical.json"
    audits_path = CLOUD / "matcher-protocol-audits.json"

    matches = json.loads(matches_path.read_text(encoding="utf-8"))
    source_matches = json.loads(source_matches_path.read_text(encoding="utf-8"))
    normalized_source_cases = deepcopy(source_matches["cases"])
    for case in normalized_source_cases:
        for turn in case["turn_matches"]:
            for domain in ("question_matches", "revision_matches"):
                for decision in turn[domain]:
                    if "match" in decision:
                        decision["match_type"] = decision.pop("match")
    require(
        matches["cases"] == normalized_source_cases,
        "match normalization changed decisions",
    )
    require(
        matches["schema_version"] == "v3.1"
        and matches["artifact"] == "semantic-matches",
        "match identity",
    )
    require(
        matches["extraction_snapshot"]
        == {
            "path": "tests/benchmark/v3_1-holdout/cloud-cases/extractions-manifest-v31.json",
            "sha256": digest(snapshot_path),
        },
        "extraction snapshot linkage",
    )
    expected_hashes = {path: digest(file) for path, file in ALLOWLIST.items()}
    require(matches["source_hashes"] == expected_hashes, "matcher source hashes")
    matcher = matches["matcher"]
    require(
        matcher["gold_access"] is True
        and matcher["model_id"] == "unverified"
        and matcher["model_family"] not in GOLD_LABELER_FAMILIES
        and isinstance(matcher["context_id"], str)
        and matcher["context_id"] not in {"", "unverified"},
        "canonical matcher provenance",
    )

    evaluations = json.loads(evaluations_path.read_text(encoding="utf-8"))
    outputs = json.loads(outputs_path.read_text(encoding="utf-8"))
    gold = json.loads(gold_path.read_text(encoding="utf-8"))
    require(
        set(gold["gold_quality"]["labeler_model_families"]) == GOLD_LABELER_FAMILIES,
        "gold labeler families",
    )
    evaluation_cases = unique(evaluations["cases"], "case_id")
    output_cases = unique(outputs["cases"], "case_id")
    gold_cases = unique(gold["cases"], "case_id")
    match_cases = unique(matches["cases"], "case_id")
    require(
        set(evaluation_cases) == set(output_cases) == set(gold_cases) == set(match_cases),
        "match case coverage",
    )
    _, aliases = score_semantic.load_ontology(ontology_path)
    total_claims = unsupported = turns = 0
    for case_id in evaluation_cases:
        evaluation_turns = evaluation_cases[case_id]["turn_evaluations"]
        output_turns = output_cases[case_id]["turn_outputs"]
        gold_turns = gold_cases[case_id]["turn_labels"]
        match_turns = match_cases[case_id]["turn_matches"]
        require(
            len(evaluation_turns)
            == len(output_turns)
            == len(gold_turns)
            == len(match_turns),
            f"{case_id}: match turn coverage",
        )
        for evaluation, output, expected, match in zip(
            evaluation_turns, output_turns, gold_turns, match_turns
        ):
            turns += 1
            require(
                evaluation["turn_index"]
                == output["turn_index"]
                == expected["turn_index"]
                == match["turn_index"],
                f"{case_id}: match turn order",
            )
            question_claims = score_semantic.validate_claims(
                evaluation["question_claims"],
                output["raw_output"],
                f"{case_id}: question",
            )
            revision_claims = score_semantic.validate_claims(
                evaluation["revision_claims"],
                output["raw_output"],
                f"{case_id}: revision",
            )
            _, question_unsupported = score_semantic.validate_match_set(
                match["question_matches"],
                question_claims,
                "question",
                set(expected["allowed_question_concepts"]),
                aliases,
                f"{case_id}: question",
            )
            _, revision_unsupported = score_semantic.validate_match_set(
                match["revision_matches"],
                revision_claims,
                "revision",
                set(expected["allowed_revision_concepts"]),
                aliases,
                f"{case_id}: revision",
            )
            total_claims += len(question_claims) + len(revision_claims)
            unsupported += question_unsupported + revision_unsupported
    require(turns == 24 and total_claims == 59, "match turn or claim total")

    audits = json.loads(audits_path.read_text(encoding="utf-8"))
    accepted = [item for item in audits["attempts"] if item["artifacts_accepted"]]
    require(
        len(accepted) == 1
        and accepted[0]["context_id"] == matcher["context_id"]
        and accepted[0]["gold_access"] is True
        and accepted[0]["prohibited_content_access"] is False,
        "matcher audit disposition",
    )
    attestation = json.loads(attestation_path.read_text(encoding="utf-8"))
    require(
        attestation["context_id"] == matcher["context_id"]
        and attestation["model_id"] == "unverified"
        and attestation["gold_access"] is True
        and attestation["model_family"] == matcher["model_family"]
        and attestation["output"]
        == {
            "path": "tests/benchmark/v3_1-holdout/cloud-cases/matches-v31-canonical.json",
            "sha256": digest(matches_path),
        },
        "matcher attestation",
    )
    snapshot_path = CLOUD / "evaluation-manifest-v31.json"
    if snapshot_path.is_file():
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        require(
            snapshot["version"] == "3.1"
            and snapshot["immutable"] is True
            and snapshot["stage"] == "evaluations"
            and snapshot["parent_manifest"]["sha256"]
            == digest(CLOUD / "outputs-manifest-v31.json"),
            "evaluation snapshot identity",
        )
        print(
            f"validated semantic matches for {turns} turns and {total_claims} claims "
            f"({unsupported} unsupported) and evaluation snapshot"
        )
    else:
        print(
            f"validated semantic matches for {turns} turns and {total_claims} claims "
            f"({unsupported} unsupported) (pre-freeze)"
        )


if __name__ == "__main__":
    main()
