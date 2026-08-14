import importlib.util
import json
import os
import unittest
from copy import deepcopy
from pathlib import Path


DEFAULT_CONTRACT = Path(__file__).with_name("recipient_manager_contract.py")
CONTRACT_PATH = Path(
    os.environ.get("V32_RECIPIENT_CONTRACT_PATH", DEFAULT_CONTRACT)
)
SPEC = importlib.util.spec_from_file_location(
    "recipient_manager_contract_under_test", CONTRACT_PATH
)
contract = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(contract)

ATTEMPT1 = (
    Path(__file__).resolve().parents[1]
    / "v3_2-holdout"
    / "cloud-cases"
    / "cases.json"
)


def manager_context(name: str = "Ada Venn") -> dict:
    return {
        "recipient_name": name,
        "recipient_role": "workshop manager",
        "relationship_to_user": "direct line manager",
        "channel": "internal manager thread",
        "audience_scope": "manager only",
        "additional_recipients": [],
    }


def routing_context() -> dict:
    return {
        "recipient_name": "Lior Prest",
        "recipient_role": "client librarian",
        "relationship_to_user": "client-side contact",
        "channel": "external mail",
        "audience_scope": "librarian only",
        "additional_recipients": [],
    }


def envelope() -> list[dict]:
    cases = []
    for index in range(1, 19):
        case_id = f"SYN-{index:03d}"
        context = routing_context() if index == 17 else manager_context()
        cases.append(
            {
                "case_id": case_id,
                "recipient_context": deepcopy(context),
            }
        )
    return cases


QUESTION_IDS = [f"SYN-{index:03d}" for index in range(4, 10)]
ROUTING_ID = "SYN-017"


class RecipientContractTests(unittest.TestCase):
    def test_manager_context_is_manager(self):
        self.assertTrue(contract.is_manager_recipient(manager_context()))

    def test_routing_context_is_not_manager(self):
        self.assertFalse(contract.is_manager_recipient(routing_context()))

    def test_role_without_manager_token_fails(self):
        value = manager_context()
        value["recipient_role"] = "loft coordinator"
        self.assertFalse(contract.is_manager_recipient(value))

    def test_negated_manager_role_fails(self):
        value = manager_context()
        value["recipient_role"] = "colleague; not a manager"
        self.assertFalse(contract.is_manager_recipient(value))

    def test_reply_all_fails_manager_gate(self):
        value = contract.apply_mutation(manager_context(), "ADD_REPLY_ALL")
        self.assertFalse(contract.is_manager_recipient(value))

    def test_valid_envelope_passes(self):
        contract.validate_envelope(envelope(), QUESTION_IDS, ROUTING_ID)

    def test_question_candidate_non_manager_fails(self):
        cases = envelope()
        cases[3]["recipient_context"] = routing_context()
        with self.assertRaises(ValueError):
            contract.validate_envelope(cases, QUESTION_IDS, ROUTING_ID)

    def test_green_control_non_manager_fails(self):
        cases = envelope()
        cases[0]["recipient_context"] = routing_context()
        with self.assertRaises(ValueError):
            contract.validate_envelope(cases, QUESTION_IDS, ROUTING_ID)

    def test_image_case_non_manager_fails(self):
        cases = envelope()
        cases[17]["recipient_context"] = routing_context()
        with self.assertRaises(ValueError):
            contract.validate_envelope(cases, QUESTION_IDS, ROUTING_ID)

    def test_routing_case_as_manager_fails(self):
        cases = envelope()
        cases[16]["recipient_context"] = manager_context()
        with self.assertRaises(ValueError):
            contract.validate_envelope(cases, QUESTION_IDS, ROUTING_ID)

    def test_two_non_manager_cases_fail(self):
        cases = envelope()
        cases[10]["recipient_context"] = routing_context()
        with self.assertRaises(ValueError):
            contract.validate_envelope(cases, QUESTION_IDS, ROUTING_ID)

    def test_routing_case_cannot_be_question_candidate(self):
        with self.assertRaises(ValueError):
            contract.validate_question_ids(
                envelope(), QUESTION_IDS + [ROUTING_ID], ROUTING_ID
            )

    def test_make_non_manager_mutation_rejects_manager_gate(self):
        value = contract.apply_mutation(manager_context(), "MAKE_NON_MANAGER")
        self.assertFalse(contract.is_manager_recipient(value))

    def test_attempt1_frozen_envelope_fails(self):
        cases = json.loads(ATTEMPT1.read_text(encoding="utf-8"))["cases"]
        question_ids = [f"V32-{index:03d}" for index in range(4, 10)]
        with self.assertRaises(ValueError):
            contract.validate_envelope(cases, question_ids, "V32-017")


if __name__ == "__main__":
    unittest.main()
