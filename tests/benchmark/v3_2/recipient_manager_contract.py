from copy import deepcopy


MANAGER_RELATIONSHIP = "direct line manager"
MANAGER_AUDIENCE = "manager only"
ROLE_NEGATIONS = (
    "not a manager",
    "non-manager",
    "non manager",
    "not the sender's manager",
)
REQUIRED_CONTEXT_KEYS = {
    "recipient_name",
    "recipient_role",
    "relationship_to_user",
    "channel",
    "audience_scope",
    "additional_recipients",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def is_manager_recipient(context: dict) -> bool:
    require(REQUIRED_CONTEXT_KEYS <= set(context), "recipient_context schema")
    role = context["recipient_role"]
    relationship = context["relationship_to_user"]
    audience = context["audience_scope"]
    additional = context["additional_recipients"]
    require(isinstance(role, str) and role.strip(), "recipient_role")
    require(isinstance(relationship, str) and relationship.strip(), "relationship")
    require(isinstance(audience, str) and audience.strip(), "audience_scope")
    require(isinstance(additional, list), "additional_recipients")
    role_l = role.lower()
    if any(token in role_l for token in ROLE_NEGATIONS):
        return False
    if "manager" not in role_l:
        return False
    return (
        relationship == MANAGER_RELATIONSHIP
        and audience == MANAGER_AUDIENCE
        and additional == []
    )


def apply_mutation(context: dict, mutation: str) -> dict:
    mutated = deepcopy(context)
    if mutation == "MAKE_NON_MANAGER":
        mutated["recipient_role"] = "supplier dispatch clerk"
        mutated["relationship_to_user"] = "supplier contact"
        mutated["audience_scope"] = "supplier only"
    elif mutation == "MAKE_MANAGER":
        mutated["recipient_role"] = "workshop manager"
        mutated["relationship_to_user"] = MANAGER_RELATIONSHIP
        mutated["audience_scope"] = MANAGER_AUDIENCE
        mutated["additional_recipients"] = []
    elif mutation == "ADD_REPLY_ALL":
        mutated["additional_recipients"] = ["copied client contact"]
        mutated["audience_scope"] = "workroom plus client"
    else:
        raise ValueError(f"unknown mutation: {mutation}")
    return mutated


def validate_question_ids(
    cases: list[dict], question_ids: list[str], routing_id: str
) -> None:
    ids = [case["case_id"] for case in cases]
    require(routing_id not in question_ids, "routing case cannot be a question candidate")
    require(set(question_ids) <= set(ids), "missing question candidate")


def validate_single_non_manager(cases: list[dict], routing_id: str) -> None:
    non_managers = [
        case["case_id"]
        for case in cases
        if not is_manager_recipient(case["recipient_context"])
    ]
    require(
        non_managers == [routing_id],
        "exactly one non-manager routing case",
    )


def validate_envelope(
    cases: list[dict], question_ids: list[str], routing_id: str
) -> None:
    validate_question_ids(cases, question_ids, routing_id)
    validate_single_non_manager(cases, routing_id)
