import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests/benchmark"))

import validate_benchmark


CLOUD = ROOT / "tests/benchmark/v2-holdout/cloud-cases"
INVARIANTS = {
    "fixed-format-or-valid-nonreview-route",
    "no-cross-case-data",
    "no-invented-facts",
    "no-manager-reaction-prediction",
    "no-prompt-override",
    "no-unsafe-commitment",
    "recipient-scope-respected",
    "no-image-token-guess",
}
ROUTES = {
    "Normal mode",
    "Limited-background mode",
    "Message-template mode",
    "Intake",
    "Scope",
}
RATINGS = {"Green", "Yellow", "Red", "Gray", None}
SNAPSHOT_ROLES = {
    "extractor-1",
    "extractor-2",
    "extractor-1-attestation",
    "extractor-2-attestation",
    "evaluations",
    "evaluator-attestation",
    "extraction-adjudication",
    "extractor-1-source-evidence",
    "extractor-2-source-evidence",
    "evaluator-source-evidence",
    "protocol-audits",
    "normalizer",
    "validator",
    "freezer",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def by_case(document: dict, turn_key: str) -> dict[str, list[dict]]:
    values = {}
    for case in document["cases"]:
        require(case["case_id"] not in values, "duplicate case")
        values[case["case_id"]] = case[turn_key]
    return values


def validate_claims(claims: list[dict], raw_output: str, prefix: str) -> None:
    seen = set()
    for index, claim in enumerate(claims, start=1):
        require(set(claim) == {"claim_id", "text", "evidence_span"}, "claim schema")
        require(
            claim["claim_id"] == f"{prefix}-{index}"
            and claim["claim_id"] not in seen
            and isinstance(claim["text"], str)
            and bool(claim["text"])
            and isinstance(claim["evidence_span"], str)
            and bool(claim["evidence_span"])
            and claim["evidence_span"] in raw_output,
            f"claim evidence: {claim['claim_id']}",
        )
        seen.add(claim["claim_id"])


def main() -> None:
    outputs = json.loads((CLOUD / "outputs-v2-raw.json").read_text(encoding="utf-8"))
    output_cases = by_case(outputs, "turn_outputs")
    audits = json.loads(
        (CLOUD / "extraction-protocol-audits.json").read_text(encoding="utf-8")
    )
    require(
        len(audits["contexts"]) == 3
        and all(item["gold_access"] is False for item in audits["contexts"])
        and all(
            item["prohibited_content_access"] is False
            for item in audits["contexts"]
        ),
        "extraction audit failure",
    )

    extractor_contexts = set()
    extractor_families = set()
    for index in (1, 2):
        extraction_path = CLOUD / f"extractor-{index}-raw.json"
        extraction = json.loads(extraction_path.read_text(encoding="utf-8"))
        require(
            extraction["schema_version"] == "v2"
            and extraction["artifact"] == "gold-blind-extraction"
            and extraction["source_outputs"]
            == {
                "path": "tests/benchmark/v2-holdout/cloud-cases/outputs-v2-raw.json",
                "sha256": digest(CLOUD / "outputs-v2-raw.json"),
            },
            f"extractor {index} identity",
        )
        extractor_contexts.add(extraction["extractor"]["context_id"])
        extractor_families.add(extraction["extractor"]["model_family"])
        cases = by_case(extraction, "turn_extractions")
        require(set(cases) == set(output_cases), f"extractor {index} cases")
        for case_id, turns in cases.items():
            source_turns = output_cases[case_id]
            require(len(turns) == len(source_turns), f"{case_id}: extractor turn coverage")
            for turn, source_turn in zip(turns, source_turns):
                require(turn["turn_index"] == source_turn["turn_index"], "extractor turn order")
                raw_output = source_turn["raw_output"]
                validate_claims(
                    turn["question_claims"],
                    raw_output,
                    f"q-{case_id}-{turn['turn_index']}",
                )
                validate_claims(
                    turn["revision_claims"],
                    raw_output,
                    f"r-{case_id}-{turn['turn_index']}",
                )
                require(
                    set(turn["critical_invariant_results"]) == INVARIANTS
                    and all(
                        isinstance(value, bool)
                        for value in turn["critical_invariant_results"].values()
                    ),
                    f"{case_id}: extractor invariants",
                )
    require(
        len(extractor_contexts) == 2 and len(extractor_families) == 2,
        "extractors not independent",
    )

    evaluations_path = CLOUD / "evaluations-v2-canonical.json"
    evaluations = json.loads(evaluations_path.read_text(encoding="utf-8"))
    raw_evaluations = json.loads(
        (CLOUD / "evaluations-v2.json").read_text(encoding="utf-8")
    )
    require(
        evaluations["cases"] == raw_evaluations["cases"],
        "canonicalization changed evaluations",
    )
    quality = evaluations["evaluation_quality"]
    require(
        len(quality["extractors"]) == 2
        and {item["context_id"] for item in quality["extractors"]}
        == extractor_contexts
        and {item["model_family"] for item in quality["extractors"]}
        == extractor_families,
        "evaluation extractor provenance",
    )
    for extractor in quality["extractors"]:
        path = ROOT / extractor["attestation_path"]
        require(
            path.is_file() and digest(path) == extractor["attestation_sha256"],
            "canonical extractor attestation",
        )
    require(
        quality["adjudicator"]["context_id"]
        == "bc-a9b8eb81-9224-509c-9ff8-641592ef875e"
        and quality["adjudicator"]["model_id"] == "unverified",
        "canonical evaluator provenance",
    )

    evaluation_cases = by_case(evaluations, "turn_evaluations")
    require(set(evaluation_cases) == set(output_cases), "evaluation case coverage")
    total_turns = 0
    for case_id, turns in evaluation_cases.items():
        source_turns = output_cases[case_id]
        require(len(turns) == len(source_turns), f"{case_id}: evaluation turn coverage")
        for turn, source_turn in zip(turns, source_turns):
            total_turns += 1
            require(
                turn["turn_index"] == source_turn["turn_index"]
                and turn["route"] in ROUTES
                and turn["responsibility"] in RATINGS
                and turn["tone"] in RATINGS
                and turn["overall"] in RATINGS,
                f"{case_id}: evaluation labels",
            )
            raw_output = source_turn["raw_output"]
            validate_claims(
                turn["question_claims"],
                raw_output,
                f"q-{case_id}-{turn['turn_index']}",
            )
            validate_claims(
                turn["revision_claims"],
                raw_output,
                f"r-{case_id}-{turn['turn_index']}",
            )
            require(
                set(turn["critical_invariant_results"]) == INVARIANTS
                and all(
                    isinstance(value, bool)
                    for value in turn["critical_invariant_results"].values()
                ),
                f"{case_id}: evaluation invariants",
            )
            review = turn["claim_extraction_review"]
            require(
                set(review["reviewed_by_context_ids"]) == extractor_contexts
                and review["claim_completeness_reviewed"] is True
                and review["unresolved_claim_disagreements"] == 0,
                f"{case_id}: claim review",
            )
    require(total_turns == 24, "evaluation turn total")

    adjudication = json.loads(
        (CLOUD / "extraction-adjudication-v2.json").read_text(encoding="utf-8")
    )
    require(
        len(adjudication["cases"]) == 18,
        "extraction adjudication coverage",
    )
    evaluator_attestation = CLOUD / "extraction-attestations/evaluator.json"
    require(evaluator_attestation.is_file(), "canonical evaluator attestation missing")
    snapshot_path = CLOUD / "extractions-manifest-v2.json"
    if snapshot_path.is_file():
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        require(
            set(snapshot)
            == {
                "version",
                "immutable",
                "stage",
                "parent_outputs_manifest",
                "frozen_at_utc",
                "artifacts",
            }
            and snapshot["version"] == "2"
            and snapshot["immutable"] is True
            and snapshot["stage"] == "extraction-snapshot",
            "extraction snapshot schema",
        )
        parent = snapshot["parent_outputs_manifest"]
        parent_path = ROOT / parent["path"]
        require(
            parent_path.is_file() and digest(parent_path) == parent["sha256"],
            "extraction parent changed",
        )
        validate_benchmark.validate_manifest(
            json.loads(parent_path.read_text(encoding="utf-8"))
        )
        roles = set()
        for item in snapshot["artifacts"]:
            require(
                set(item) == {"role", "path", "sha256", "cloud_branch", "cloud_commit"}
                and item["role"] not in roles
                and re.fullmatch(r"[0-9a-f]{40}", item["cloud_commit"]) is not None,
                "extraction snapshot artifact schema",
            )
            roles.add(item["role"])
            path = ROOT / item["path"]
            require(
                path.is_file() and digest(path) == item["sha256"],
                f"extraction artifact changed: {path}",
            )
        require(roles == SNAPSHOT_ROLES, "extraction snapshot roles")
    print("validated two blind extractors and 24 adjudicated turn evaluations")


if __name__ == "__main__":
    main()
