import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tests/benchmark/v3_2"))
import score_semantic_v3_2

CLOUD = ROOT / "tests/benchmark/v3_2-holdout/cloud-cases"


def main() -> None:
    gold = json.loads((CLOUD / "gold-v32.json").read_text())
    report = json.loads((CLOUD / "coverage-report-v32.json").read_text())
    facts = score_semantic_v3_2.coverage_facts(gold)
    score_semantic_v3_2.validate_coverage(facts)
    if report != {
        "schema_version": "v3.2",
        "status": "VALID_COVERAGE",
        "coverage": facts,
        "failed_gates": [],
        "sut_execution_authorized": True,
    }:
        raise ValueError("coverage report mismatch")
    if len(gold["cases"]) != 18 or facts["turns"] != 24:
        raise ValueError("gold coverage")
    print(
        "validated v3.2 gold coverage: "
        f"{facts['required_question_concepts']} question concepts across "
        f"{facts['required_question_cases']} cases"
    )


if __name__ == "__main__":
    main()
