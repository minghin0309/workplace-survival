from copy import deepcopy


CONCEPTS = {
    "approval-authority",
    "confirmed-deadline",
    "intended-recipient",
    "traceable-source",
    "material-measurement",
    "required-decision-option",
}
REQUIRED_KEYS = {
    "case_id",
    "missing_concept",
    "dependency_present",
    "answer_absent",
    "placeholder_safe",
    "qualification_safe",
    "omission_safe",
    "direct_red_defects",
    "answer_fixture",
    "safe_completion_enabled_by_answer",
    "question_unnecessary_without_dependency",
}
MIN_CANDIDATES = 6


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_candidate(candidate: dict) -> None:
    require(set(candidate) == REQUIRED_KEYS, "candidate schema")
    require(candidate["missing_concept"] in CONCEPTS, "candidate concept")
    require(
        all(
            isinstance(candidate[field], bool)
            for field in (
                "dependency_present",
                "answer_absent",
                "placeholder_safe",
                "qualification_safe",
                "omission_safe",
                "safe_completion_enabled_by_answer",
                "question_unnecessary_without_dependency",
            )
        ),
        "candidate booleans",
    )
    require(
        isinstance(candidate["direct_red_defects"], list)
        and all(
            isinstance(value, str) and value
            for value in candidate["direct_red_defects"]
        ),
        "direct Red defects",
    )
    require(
        isinstance(candidate["answer_fixture"], str)
        and bool(candidate["answer_fixture"]),
        "answer fixture",
    )


def requires_question(candidate: dict) -> bool:
    validate_candidate(candidate)
    return (
        candidate["dependency_present"]
        and candidate["answer_absent"]
        and not candidate["placeholder_safe"]
        and not candidate["qualification_safe"]
        and not candidate["omission_safe"]
        and not candidate["direct_red_defects"]
    )


def is_clean_candidate(candidate: dict) -> bool:
    return (
        requires_question(candidate)
        and candidate["safe_completion_enabled_by_answer"]
        and candidate["question_unnecessary_without_dependency"]
    )


def apply_mutation(candidate: dict, mutation: str) -> dict:
    mutated = deepcopy(candidate)
    if mutation == "REMOVE_DEPENDENCY":
        mutated["dependency_present"] = False
    elif mutation == "SUPPLY_ANSWER":
        mutated["answer_absent"] = False
    elif mutation == "ADD_DOMINANT_RED":
        mutated["direct_red_defects"] = ["synthetic-independent-red-defect"]
    else:
        raise ValueError(f"unknown mutation: {mutation}")
    return mutated


def validate_mutations(candidate: dict) -> None:
    require(is_clean_candidate(candidate), "baseline question candidate")
    removed = apply_mutation(candidate, "REMOVE_DEPENDENCY")
    require(not requires_question(removed), "dependency removal must remove question")
    require(
        candidate["question_unnecessary_without_dependency"],
        "dependency-removal completion",
    )
    answered = apply_mutation(candidate, "SUPPLY_ANSWER")
    require(not requires_question(answered), "supplied answer must remove question")
    require(
        candidate["safe_completion_enabled_by_answer"],
        "answer must enable safe completion",
    )
    dominant = apply_mutation(candidate, "ADD_DOMINANT_RED")
    require(not is_clean_candidate(dominant), "dominant Red must reject candidate")


def validate_design(entries: list[dict]) -> None:
    require(len(entries) >= MIN_CANDIDATES, "insufficient candidate count")
    case_ids = [entry["case_id"] for entry in entries]
    concepts = [entry["missing_concept"] for entry in entries]
    require(len(case_ids) == len(set(case_ids)), "duplicate candidate case")
    require(len(concepts) == len(set(concepts)), "duplicate candidate concept")
    require(CONCEPTS <= set(concepts), "missing question concept")
    for entry in entries:
        validate_mutations(entry)
