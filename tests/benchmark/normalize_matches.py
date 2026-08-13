import hashlib
import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLOUD = ROOT / "tests/benchmark/v2-holdout/cloud-cases"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def main() -> None:
    source_matches_path = CLOUD / "matches-v2-clean.json"
    source_attestation_path = CLOUD / "matcher-attestation-v2-clean.json"
    matches_path = CLOUD / "matches-v2-canonical.json"
    attestation_path = CLOUD / "matcher-attestation-v2-canonical.json"
    source_matches = json.loads(source_matches_path.read_text(encoding="utf-8"))
    source_attestation = json.loads(
        source_attestation_path.read_text(encoding="utf-8")
    )

    matches = deepcopy(source_matches)
    source_decisions = [
        (
            decision["claim_id"],
            decision["concept_id"],
            decision.get("match_type", decision.get("match")),
            decision["confidence"],
            decision["rationale"],
        )
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
    matches["matcher"] = {
        "context_id": "bc-49280770-7415-5b2a-abb9-65f7bb13a6c0",
        "model_id": "unverified",
        "model_family": "gpt",
        "gold_access": True,
    }
    canonical_decisions = [
        (
            decision["claim_id"],
            decision["concept_id"],
            decision["match_type"],
            decision["confidence"],
            decision["rationale"],
        )
        for case in matches["cases"]
        for turn in case["turn_matches"]
        for domain in ("question_matches", "revision_matches")
        for decision in turn[domain]
    ]
    if canonical_decisions != source_decisions:
        raise RuntimeError("normalization changed semantic match decisions")
    matches_path.write_text(json.dumps(matches, indent=2) + "\n", encoding="utf-8")

    attestation = {
        "schema_version": "v2",
        "role": "matcher",
        "context_id": "bc-49280770-7415-5b2a-abb9-65f7bb13a6c0",
        "model_id": "unverified",
        "model_family": "gpt",
        "cloud_branch": "cursor/post-freeze-semantic-matcher-a6c0",
        "cloud_commit": "51a3c4df3628167586989cfd47780ed156d36dcf",
        "gold_access": True,
        "files_read": source_attestation["files_read"],
        "output": {
            "path": relative(matches_path),
            "sha256": digest(matches_path),
        },
        "source_attestation": {
            "path": relative(source_attestation_path),
            "sha256": digest(source_attestation_path),
        },
        "limitations": source_attestation["limitations"]
        + [
            "Machine model ID was unavailable from cloud run metadata; no ID was guessed.",
            "The isolated-branch checkout deviation is recorded in matcher-protocol-audits.json.",
        ],
        "normalization": {
            "kind": "mechanical-provenance-wrapper",
            "match_decisions_changed": False,
        },
    }
    attestation_path.write_text(
        json.dumps(attestation, indent=2) + "\n", encoding="utf-8"
    )
    print("normalized clean semantic matcher provenance")


if __name__ == "__main__":
    main()
