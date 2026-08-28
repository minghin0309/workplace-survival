import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tests/benchmark/v3_3"))
import revision_scoring_contract
import score_semantic_v3_3

CLOUD = ROOT / "tests/benchmark/v3_3-holdout/attempt-3/cloud-cases"


def main() -> None:
    gold = json.loads((CLOUD / "gold-v333.json").read_text())
    report = json.loads((CLOUD / "coverage-report-v333.json").read_text())
    question_design = json.loads((CLOUD / "question-design.json").read_text())
    facts = score_semantic_v3_3.coverage_facts(gold)
    score_semantic_v3_3.validate_coverage(facts)
    if report != {
        "schema_version": "v3.3",
        "status": "VALID_COVERAGE",
        "coverage": facts,
        "failed_gates": [],
        "sut_execution_authorized": True,
    }:
        raise ValueError("coverage report mismatch")
    if len(gold["cases"]) != 18 or facts["turns"] != 24:
        raise ValueError("gold coverage")
    revision_scoring_contract.validate_envelope(gold, question_design)
    print(
        "validated v3.3 attempt-3 gold coverage: "
        f"{facts['required_question_concepts']} question concepts across "
        f"{facts['required_question_cases']} cases"
    )


if __name__ == "__main__":
    main()
