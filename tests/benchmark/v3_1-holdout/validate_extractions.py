#!/usr/bin/env python3
"""Validate gold-blind v3.1 extractions and the extraction snapshot."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CLOUD = ROOT / "tests/benchmark/v3_1-holdout/cloud-cases"
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
    "extractor-visible",
    "normalizer",
    "validator",
    "freezer",
}
EXTRACTOR_CONTEXTS = {
    "bc-d8bcdf8c-3937-5830-847c-cb085ded528e",
    "bc-407b6129-b25d-5064-9d64-5523806bbeb3",
}
EXTRACTOR_RAW_CONTEXTS = {
    1: {"bc-d8bcdf8c-3937-5830-847c-cb085ded528e"},
    2: {"unverified", "bc-407b6129-b25d-5064-9d64-5523806bbeb3"},
}
EVALUATOR_CONTEXT = "bc-f001181e-4ec6-5746-aaad-b4bd3ba288e3"


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
    visible = json.loads((CLOUD / "extractor-visible.json").read_text(encoding="utf-8"))
    output_cases = by_case(visible, "turns")
    audits = json.loads(
        (CLOUD / "extraction-protocol-audits.json").read_text(encoding="utf-8")
    )
    require(
        len(audits["contexts"]) == 3
        and all(item["gold_access"] is False for item in audits["contexts"])
        and all(
            item["prohibited_content_access"] is False for item in audits["contexts"]
        ),
        "extraction audit failure",
    )

    extractor_families = set()
    for index, family in ((1, "claude"), (2, "gemini")):
        extraction_path = CLOUD / f"extractor-{index}-raw.json"
        extraction = json.loads(extraction_path.read_text(encoding="utf-8"))
        require(
            extraction["schema_version"] == "v3.1"
            and extraction["artifact"] == "gold-blind-extraction"
            and extraction["extractor"]["model_family"] == family
            and extraction["extractor"]["context_id"] in EXTRACTOR_RAW_CONTEXTS[index]
            and extraction["source_outputs"]
            == {
                "path": "tests/benchmark/v3_1-holdout/cloud-cases/extractor-visible.json",
                "sha256": digest(CLOUD / "extractor-visible.json"),
            },
            f"extractor {index} identity",
        )
        extractor_families.add(extraction["extractor"]["model_family"])
        cases = by_case(extraction, "turn_extractions")
        require(set(cases) == set(output_cases), f"extractor {index} cases")
        for case_id, turns in cases.items():
            source_turns = output_cases[case_id]
            require(len(turns) == len(source_turns), f"{case_id}: extractor turn coverage")
            for turn, source_turn in zip(turns, source_turns):
                require(
                    turn["turn_index"] == source_turn["turn_index"],
                    "extractor turn order",
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
                    f"{case_id}: extractor invariants",
                )
    require(extractor_families == {"claude", "gemini"}, "extractors not independent")

    evaluations_path = CLOUD / "evaluations-v31-canonical.json"
    evaluations = json.loads(evaluations_path.read_text(encoding="utf-8"))
    raw_evaluations = json.loads((CLOUD / "evaluations-v31.json").read_text(encoding="utf-8"))
    require(
        evaluations["cases"] == raw_evaluations["cases"],
        "canonicalization changed evaluations",
    )
    quality = evaluations["evaluation_quality"]
    require(
        len(quality["extractors"]) == 2
        and {item["context_id"] for item in quality["extractors"]}
        == EXTRACTOR_CONTEXTS
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
        quality["adjudicator"]["context_id"] == EVALUATOR_CONTEXT
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
                set(review["reviewed_by_context_ids"]) == EXTRACTOR_CONTEXTS
                and review["claim_completeness_reviewed"] is True
                and review["unresolved_claim_disagreements"] == 0,
                f"{case_id}: claim review",
            )
    require(total_turns == 24, "evaluation turn total")

    adjudication = json.loads(
        (CLOUD / "extraction-adjudication-v31.json").read_text(encoding="utf-8")
    )
    require(len(adjudication["cases"]) == 18, "extraction adjudication coverage")
    require(
        (CLOUD / "extraction-attestations/evaluator.json").is_file(),
        "canonical evaluator attestation missing",
    )
    snapshot_path = CLOUD / "extractions-manifest-v31.json"
    if snapshot_path.is_file():
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        require(
            snapshot["version"] == "3.1"
            and snapshot["immutable"] is True
            and snapshot["stage"] == "extraction-snapshot"
            and snapshot["parent_outputs_manifest"]["sha256"]
            == digest(CLOUD / "outputs-manifest-v31.json"),
            "extraction snapshot identity",
        )
        roles = set()
        for item in snapshot["artifacts"]:
            require(
                set(item)
                >= {"role", "path", "sha256", "cloud_branch", "cloud_commit"}
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
        require(roles == SNAPSHOT_ROLES, f"extraction snapshot roles: {roles}")
        print("validated two blind extractors, 24 adjudicated turns, and extraction snapshot")
    else:
        print("validated two blind extractors and 24 adjudicated turn evaluations (pre-freeze)")


if __name__ == "__main__":
    main()
