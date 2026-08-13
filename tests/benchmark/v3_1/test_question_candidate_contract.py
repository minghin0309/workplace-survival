import importlib.util
import os
import unittest
from pathlib import Path


DEFAULT_CONTRACT = Path(__file__).with_name("question_candidate_contract.py")
CONTRACT_PATH = Path(
    os.environ.get("V31_QUESTION_CONTRACT_PATH", DEFAULT_CONTRACT)
)
SPEC = importlib.util.spec_from_file_location(
    "question_candidate_contract_under_test", CONTRACT_PATH
)
contract = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(contract)


def candidate(index: int, concept: str) -> dict:
    return {
        "case_id": f"V31-{index:03d}",
        "missing_concept": concept,
        "dependency_present": True,
        "answer_absent": True,
        "placeholder_safe": False,
        "qualification_safe": False,
        "omission_safe": False,
        "direct_red_defects": [],
        "answer_fixture": f"synthetic-answer-{index}",
        "safe_completion_enabled_by_answer": True,
        "question_unnecessary_without_dependency": True,
    }


def valid_design() -> list[dict]:
    return [
        candidate(index, concept)
        for index, concept in enumerate(sorted(contract.CONCEPTS), start=4)
    ]


class CandidateTests(unittest.TestCase):
    def test_baseline_requires_question(self):
        self.assertTrue(
            contract.requires_question(
                candidate(4, "approval-authority")
            )
        )

    def test_placeholder_escape_rejects_candidate(self):
        value = candidate(4, "approval-authority")
        value["placeholder_safe"] = True
        self.assertFalse(contract.requires_question(value))

    def test_qualification_escape_rejects_candidate(self):
        value = candidate(4, "approval-authority")
        value["qualification_safe"] = True
        self.assertFalse(contract.requires_question(value))

    def test_omission_escape_rejects_candidate(self):
        value = candidate(4, "approval-authority")
        value["omission_safe"] = True
        self.assertFalse(contract.requires_question(value))

    def test_remove_dependency_removes_question(self):
        value = contract.apply_mutation(
            candidate(4, "approval-authority"), "REMOVE_DEPENDENCY"
        )
        self.assertFalse(contract.requires_question(value))

    def test_supply_answer_enables_completion_without_question(self):
        baseline = candidate(4, "approval-authority")
        value = contract.apply_mutation(baseline, "SUPPLY_ANSWER")
        self.assertFalse(contract.requires_question(value))
        self.assertTrue(baseline["safe_completion_enabled_by_answer"])

    def test_dominant_red_rejects_clean_candidate(self):
        value = contract.apply_mutation(
            candidate(4, "approval-authority"), "ADD_DOMINANT_RED"
        )
        self.assertFalse(contract.is_clean_candidate(value))

    def test_six_distinct_candidates_pass(self):
        contract.validate_design(valid_design())

    def test_fewer_than_six_candidates_fail(self):
        with self.assertRaises(ValueError):
            contract.validate_design(valid_design()[:5])

    def test_duplicate_concept_fails(self):
        values = valid_design()
        values[-1]["missing_concept"] = values[0]["missing_concept"]
        with self.assertRaises(ValueError):
            contract.validate_design(values)


if __name__ == "__main__":
    unittest.main()
