import importlib.util
import json
import os
import unittest
from pathlib import Path


DEFAULT_CONTRACT = Path(__file__).with_name("revision_scoring_contract.py")
CONTRACT_PATH = Path(
    os.environ.get("V33_REVISION_CONTRACT_PATH", DEFAULT_CONTRACT)
)
SPEC = importlib.util.spec_from_file_location(
    "revision_scoring_contract_under_test", CONTRACT_PATH
)
contract = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(contract)

ATTEMPT3 = (
    Path(__file__).resolve().parents[1]
    / "v3_2-holdout"
    / "attempt-3"
    / "cloud-cases"
)


def gold_turn(*, responsibility="Red", route="Normal mode", required=None) -> dict:
    return {
        "turn_index": 1,
        "route": route,
        "responsibility": responsibility,
        "tone": "Green",
        "overall": responsibility,
        "required_question_concepts": ["confirmed-deadline"],
        "allowed_question_concepts": ["confirmed-deadline"],
        "required_revision_concepts": required or ["placeholder-unknown-value"],
        "allowed_revision_concepts": ["placeholder-unknown-value"],
    }


def gold_doc(turn: dict, case_id: str = "SYN-004") -> dict:
    return {"cases": [{"case_id": case_id, "turn_labels": [turn]}]}


def omission_candidate() -> dict:
    return {
        "case_id": "SYN-004",
        "image_only": False,
        "writer_holds_answer": True,
        "data_b_contains_unconfirmed_token": False,
        "base_state": {
            "question_necessary": True,
            "complete_safe_message_without_answer": False,
            "independent_red": False,
            "absent_from_sut_visible_fields": True,
        },
    }


class RevisionContractTests(unittest.TestCase):
    def test_required_preserve_intended_recipient_fails(self):
        turn = gold_turn(required=["preserve-intended-recipient"])
        with self.assertRaisesRegex(ValueError, "preserve-intended-recipient"):
            contract.validate_required_revision_concepts(turn)

    def test_allowed_preserve_intended_recipient_passes(self):
        turn = gold_turn(required=["placeholder-unknown-value"])
        turn["allowed_revision_concepts"] = [
            "placeholder-unknown-value",
            "preserve-intended-recipient",
        ]
        contract.validate_required_revision_concepts(turn)

    def test_established_omission_requires_gold_red(self):
        contract.validate_question_gold(omission_candidate(), gold_turn())
        with self.assertRaisesRegex(ValueError, "established omission"):
            contract.validate_question_gold(
                omission_candidate(), gold_turn(responsibility="Gray")
            )

    def test_unconfirmed_data_b_token_is_not_forced_red(self):
        candidate = omission_candidate()
        candidate["data_b_contains_unconfirmed_token"] = True
        contract.validate_question_gold(
            candidate, gold_turn(responsibility="Gray")
        )

    def test_image_only_requires_occluded_role(self):
        candidate = {
            "case_id": "SYN-008",
            "image_only": True,
            "writer_holds_answer": True,
            "base_state": omission_candidate()["base_state"],
        }
        with self.assertRaisesRegex(ValueError, "occluded_role"):
            contract.validate_question_gold(candidate, gold_turn())

    def test_occluded_data_b_token_requires_intake_gold(self):
        candidate = {
            "case_id": "SYN-008",
            "image_only": True,
            "occluded_role": "data_b",
            "writer_holds_answer": True,
            "base_state": omission_candidate()["base_state"],
        }
        with self.assertRaisesRegex(ValueError, "Intake"):
            contract.validate_question_gold(candidate, gold_turn())
        contract.validate_question_gold(
            candidate,
            {
                "turn_index": 1,
                "route": "Intake",
                "responsibility": None,
                "tone": None,
                "overall": None,
                "required_question_concepts": ["measured-cold-fill-pressure"],
                "allowed_question_concepts": ["measured-cold-fill-pressure"],
                "required_revision_concepts": [],
                "allowed_revision_concepts": [],
            },
        )

    def test_occluded_data_a_token_may_be_normal(self):
        candidate = {
            "case_id": "SYN-008",
            "image_only": True,
            "occluded_role": "data_a",
            "writer_holds_answer": True,
            "base_state": omission_candidate()["base_state"],
        }
        contract.validate_question_gold(
            candidate, gold_turn(responsibility="Gray")
        )

    def test_valid_envelope_passes(self):
        gold = gold_doc(gold_turn())
        design = {"candidates": [omission_candidate()]}
        contract.validate_envelope(gold, design)

    def test_attempt3_gold_fails_preserve_recipient_contract(self):
        gold = json.loads((ATTEMPT3 / "gold-v323.json").read_text(encoding="utf-8"))
        with self.assertRaisesRegex(ValueError, "preserve-intended-recipient"):
            contract.validate_gold_document(gold)

    def test_attempt3_question_design_fails_omission_or_occlusion_contract(self):
        gold = json.loads((ATTEMPT3 / "gold-v323.json").read_text(encoding="utf-8"))
        design = json.loads(
            (ATTEMPT3 / "question-design.json").read_text(encoding="utf-8")
        )
        with self.assertRaises(ValueError):
            contract.validate_question_design(gold, design)


if __name__ == "__main__":
    unittest.main()
