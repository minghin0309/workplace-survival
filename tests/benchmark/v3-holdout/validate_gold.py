import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tests/benchmark/v3"))

import score_semantic_v3


CLOUD = ROOT / "tests/benchmark/v3-holdout/cloud-cases"
RATINGS = {"Green", "Yellow", "Red", "Gray", None}
ROUTES = {
    "Normal mode",
    "Limited-background mode",
    "Message-template mode",
    "Intake",
    "Scope",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    gold = json.loads((CLOUD / "gold-v3.json").read_text(encoding="utf-8"))
    report = json.loads(
        (CLOUD / "coverage-report-v3.json").read_text(encoding="utf-8")
    )
    audits = json.loads(
        (CLOUD / "gold-protocol-audits.json").read_text(encoding="utf-8")
    )
    require(
        gold["schema_version"] == "v3"
        and gold["artifact"] == "adjudicated-gold"
        and len(gold["cases"]) == 18,
        "gold identity",
    )
    quality = gold["gold_quality"]
    require(
        quality["labeler_model_families"] == ["grok", "kimi", "gpt"]
        and quality["adjudicator_model_family"] == "claude"
        and quality["human_review_available"] is False
        and quality["adjudication_complete"] is True
        and quality["vote_distributions_preserved"] is True,
        "gold quality",
    )
    total_turns = 0
    for case in gold["cases"]:
        for expected_index, turn in enumerate(case["turn_labels"], start=1):
            total_turns += 1
            require(
                turn["turn_index"] == expected_index
                and turn["route"] in ROUTES
                and turn["responsibility"] in RATINGS
                and turn["tone"] in RATINGS
                and turn["overall"] in RATINGS,
                f"{case['case_id']}: labels",
            )
            for required_key, allowed_key in (
                ("required_question_concepts", "allowed_question_concepts"),
                ("required_revision_concepts", "allowed_revision_concepts"),
            ):
                required = turn[required_key]
                allowed = turn[allowed_key]
                require(
                    required == sorted(set(required))
                    and allowed == sorted(set(allowed))
                    and set(required) <= set(allowed),
                    f"{case['case_id']}: concepts",
                )
            require(
                turn["gold_quality"]["tier"]
                in {"heterogeneous_adjudicated", "gold_uncertain"},
                f"{case['case_id']}: tier",
            )
    require(total_turns == 24, "gold turn coverage")

    facts = score_semantic_v3.coverage_facts(gold)
    require(
        report["status"] == "INVALID_COVERAGE"
        and report["coverage"] == facts
        and set(report["failed_gates"])
        == {"required_question_concepts", "required_question_cases"}
        and report["sut_execution_authorized"] is False,
        "coverage gate disposition",
    )
    try:
        score_semantic_v3.validate_coverage(facts)
    except score_semantic_v3.CoverageError:
        pass
    else:
        raise ValueError("invalid holdout passed v3 coverage")
    require(
        all(item["prohibited_content_access"] is False for item in audits["contexts"])
        and len(audits["rejected_attempts"]) == 1
        and audits["rejected_attempts"][0]["artifacts_accepted"] is False,
        "gold protocol audit disposition",
    )
    for attestation in quality["attestations"]:
        path = ROOT / attestation["path"]
        require(
            path.is_file()
            and score_semantic_v3.digest(path) == attestation["sha256"],
            "gold attestation hash",
        )
    for forbidden in ("sut-inputs", "sut-raw", "outputs-v3.json", "score-report-v3.json"):
        require(not (CLOUD / forbidden).exists(), f"SUT started despite invalid coverage: {forbidden}")
    print("validated v3 INVALID_COVERAGE before SUT execution")


if __name__ == "__main__":
    main()
