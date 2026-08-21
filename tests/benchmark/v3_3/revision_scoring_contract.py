"""v3.3 construction and gold-label contracts for H-003, G-001, and G-003."""

from __future__ import annotations


IMPLICIT_PRESERVE_RECIPIENT = "preserve-intended-recipient"
OCCLUDED_ROLES = {"data_a", "data_b", "none"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_required_revision_concepts(turn_label: dict) -> None:
    required = turn_label.get("required_revision_concepts") or []
    require(
        isinstance(required, list),
        "required_revision_concepts",
    )
    require(
        IMPLICIT_PRESERVE_RECIPIENT not in required,
        "preserve-intended-recipient cannot be required",
    )


def validate_gold_document(gold: dict) -> None:
    require(isinstance(gold, dict) and isinstance(gold.get("cases"), list), "gold schema")
    for case in gold["cases"]:
        require(isinstance(case.get("turn_labels"), list), "turn_labels")
        for turn in case["turn_labels"]:
            validate_required_revision_concepts(turn)


def is_established_omission(candidate: dict) -> bool:
    base = candidate.get("base_state") or {}
    return (
        candidate.get("writer_holds_answer") is True
        and base.get("question_necessary") is True
        and base.get("complete_safe_message_without_answer") is False
        and base.get("independent_red") is False
        and base.get("absent_from_sut_visible_fields") is True
        and candidate.get("data_b_contains_unconfirmed_token") is not True
    )


def validate_question_gold(candidate: dict, gold_turn: dict) -> None:
    if candidate.get("image_only"):
        role = candidate.get("occluded_role")
        require(role in OCCLUDED_ROLES, "image_only candidate missing occluded_role")
        if role == "data_b":
            require(
                gold_turn.get("route") == "Intake",
                "occluded Data B token requires Intake gold",
            )
            return
        if role == "data_a":
            return
    if is_established_omission(candidate):
        require(
            gold_turn.get("responsibility") == "Red",
            "established omission must be gold Red",
        )


def gold_turns_by_case(gold: dict) -> dict[str, list[dict]]:
    return {case["case_id"]: case["turn_labels"] for case in gold["cases"]}


def validate_question_design(gold: dict, question_design: dict) -> None:
    turns = gold_turns_by_case(gold)
    candidates = question_design.get("candidates") or []
    require(isinstance(candidates, list), "question-design candidates")
    for candidate in candidates:
        case_id = candidate["case_id"]
        require(case_id in turns, f"missing gold for {case_id}")
        validate_question_gold(candidate, turns[case_id][0])


def validate_envelope(gold: dict, question_design: dict | None = None) -> None:
    validate_gold_document(gold)
    if question_design is not None:
        validate_question_design(gold, question_design)
