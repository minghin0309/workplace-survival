import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tests/benchmark/v3_3"))
import score_semantic_v3_3

CLOUD = ROOT / "tests/benchmark/v3_3-holdout/attempt-2/cloud-cases"


def canonical_turn(turn: dict, definitions: dict) -> dict:
    uncertain = turn["gold_uncertain"]
    return {
        "turn_index": turn["turn_index"],
        "route": turn["route"],
        "responsibility": turn["responsibility"],
        "tone": turn["tone"],
        "overall": turn["overall"],
        "required_question_concepts": turn["required_question_concepts"],
        "allowed_question_concepts": turn["allowed_question_concepts"],
        "required_revision_concepts": turn["required_revision_concepts"],
        "allowed_revision_concepts": turn["allowed_revision_concepts"],
        "concept_definitions": definitions,
        "critical_invariants": turn["critical_invariants"],
        "rationale": turn["rationale"],
        "gold_quality": {
            "tier": "gold_uncertain" if uncertain else "heterogeneous_adjudicated",
            "three_way_categorical_disagreement": uncertain,
            "critical_invariant_disagreement": False,
            "human_reviewed": False,
            "unresolved_adjudication": uncertain,
        },
    }


def main() -> None:
    raw = json.loads((CLOUD / "gold-v332-raw.json").read_text(encoding="utf-8"))
    definitions = {
        concept_id: definition
        for domain in ("question", "revision")
        for concept_id, definition in raw["definitions"][domain].items()
    }
    quality = raw.get("gold_quality") or raw.get("quality") or {}
    gold = {
        "schema_version": "v3.3",
        "artifact": "adjudicated-gold",
        "case_set_id": "v332-holdout-cloud-attempt2",
        "gold_quality": {
            "labeler_model_families": quality.get("labeler_model_families")
            or quality.get("families"),
            "adjudicator_model_family": quality.get("adjudicator_model_family")
            or quality.get("adjudicator"),
            "human_review_available": False,
            "adjudication_complete": True,
            "vote_distributions_preserved": True,
            "attestations": [],
        },
        "cases": [
            {
                "case_id": case["case_id"],
                "turn_labels": [
                    canonical_turn(turn, definitions) for turn in case["turn_labels"]
                ],
            }
            for case in raw["cases"]
        ],
    }
    path = CLOUD / "gold-v332.json"
    path.write_text(json.dumps(gold, indent=2) + "\n", encoding="utf-8")
    facts = score_semantic_v3_3.coverage_facts(gold)
    status = "VALID_COVERAGE"
    failures = []
    try:
        score_semantic_v3_3.validate_coverage(facts)
    except score_semantic_v3_3.CoverageError as error:
        status = "INVALID_COVERAGE"
        failures = str(error).split(": ", 1)[-1].split(", ")
    report = {
        "schema_version": "v3.3",
        "status": status,
        "coverage": facts,
        "failed_gates": failures,
        "sut_execution_authorized": status == "VALID_COVERAGE",
    }
    (CLOUD / "coverage-report-v332.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(status, json.dumps(facts))


if __name__ == "__main__":
    main()
