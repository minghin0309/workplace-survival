import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tests/benchmark/v3_1"))

import question_candidate_contract as contract


CLOUD = ROOT / "tests/benchmark/v3_1-holdout/cloud-cases"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def core(entry: dict) -> dict:
    return {key: entry[key] for key in contract.REQUIRED_KEYS}


def main() -> None:
    cases = json.loads((CLOUD / "cases.json").read_text(encoding="utf-8"))
    notes = json.loads((CLOUD / "oracle-notes.json").read_text(encoding="utf-8"))
    design = json.loads(
        (CLOUD / "question-design.json").read_text(encoding="utf-8")
    )
    mutations = json.loads(
        (CLOUD / "construction-mutations.json").read_text(encoding="utf-8")
    )
    expected_ids = [f"V31-{index:03d}" for index in range(1, 19)]
    require(
        cases["case_count"] == 18
        and cases["turn_count"] == 24
        and [case["case_id"] for case in cases["cases"]] == expected_ids,
        "case coverage",
    )
    require(
        [note["case_id"] for note in notes["case_notes"]] == expected_ids,
        "note coverage",
    )
    turn_total = 0
    for case in cases["cases"]:
        case_id = case["case_id"]
        expected_turns = 3 if case_id in {"V31-014", "V31-015", "V31-016"} else 1
        require(len(case["turns"]) == expected_turns, f"{case_id}: turns")
        turn_total += expected_turns
        for index, turn in enumerate(case["turns"], start=1):
            require(
                turn["turn_index"] == index
                and turn["turn_id"] == f"{case_id}-T{index}",
                f"{case_id}: turn order",
            )
            if case_id not in {"V31-008", "V31-018"}:
                require(
                    turn["image_path"] is None and turn["image_spec"] is None,
                    f"{case_id}: unexpected image",
                )
    require(turn_total == 24, "turn total")

    entries = [core(entry) for entry in design["entries"]]
    contract.validate_design(entries)
    require(
        [entry["case_id"] for entry in entries]
        == [f"V31-{index:03d}" for index in range(4, 10)],
        "question candidate IDs",
    )
    require(
        len(mutations["mutations"]) == 18,
        "construction mutation count",
    )
    by_case = {}
    for mutation in mutations["mutations"]:
        by_case.setdefault(mutation["case_id"], set()).add(
            mutation["mutation_type"]
        )
    require(
        all(
            by_case[case_id]
            == {"REMOVE_DEPENDENCY", "SUPPLY_ANSWER", "ADD_DOMINANT_RED"}
            for case_id in [f"V31-{index:03d}" for index in range(4, 10)]
        ),
        "construction mutation coverage",
    )
    for case in ("V31-008", "V31-018"):
        turn = next(item for item in cases["cases"] if item["case_id"] == case)[
            "turns"
        ][0]
        path = ROOT / turn["image_path"]
        if not path.is_file():
            path = CLOUD / turn["image_path"]
        require(
            path.is_file() and path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"),
            f"{case}: PNG",
        )
    print("validated v3.1 holdout construction: 18 cases, 24 turns, 6 candidates")


if __name__ == "__main__":
    main()
