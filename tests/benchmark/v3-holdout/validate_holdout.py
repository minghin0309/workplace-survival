import hashlib
import json
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "tests/benchmark/v3-holdout"
CLOUD = BASE / "cloud-cases"
CASE_KEYS = {
    "case_id",
    "category",
    "recipient_context",
    "data_a",
    "turns",
    "image_spec",
}
TURN_KEYS = {"turn_index", "input_raw", "image_path"}
NOTE_KEYS = {"case_id", "design_intent", "difficulty_notes"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    require(data.startswith(b"\x89PNG\r\n\x1a\n"), f"invalid PNG: {path}")
    return struct.unpack(">II", data[16:24])


def main() -> None:
    cases_document = json.loads((CLOUD / "cases.json").read_text(encoding="utf-8"))
    notes_document = json.loads(
        (CLOUD / "oracle-notes.json").read_text(encoding="utf-8")
    )
    require(
        set(cases_document) == {"schema_version", "case_set_id", "cases"}
        and cases_document["schema_version"] == "v3"
        and cases_document["case_set_id"] == "v3-holdout-cloud-cases",
        "case envelope",
    )
    require(
        set(notes_document) == {"schema_version", "case_set_id", "notes"}
        and notes_document["schema_version"] == "v3"
        and notes_document["case_set_id"] == "v3-holdout-cloud-cases",
        "note envelope",
    )
    cases = cases_document["cases"]
    notes = notes_document["notes"]
    case_ids = [f"V3-{index:03d}" for index in range(1, 19)]
    require([case["case_id"] for case in cases] == case_ids, "case IDs")
    require([note["case_id"] for note in notes] == case_ids, "note IDs")
    expected_categories = (
        ["green_control"] * 3
        + ["material_information"] * 4
        + ["responsibility_boundary"] * 3
        + ["tone_boundary"] * 2
        + ["correction_state"] * 3
        + ["recipient_routing"]
        + ["image_only"] * 2
    )
    require(
        [case["category"] for case in cases] == expected_categories,
        "category distribution",
    )
    turn_total = 0
    for case, note in zip(cases, notes):
        case_id = case["case_id"]
        require(set(case) == CASE_KEYS, f"{case_id}: case schema")
        require(set(note) == NOTE_KEYS, f"{case_id}: note schema")
        require(
            isinstance(case["recipient_context"], str)
            and bool(case["recipient_context"])
            and isinstance(case["data_a"], dict)
            and bool(case["data_a"]),
            f"{case_id}: visible context",
        )
        expected_turns = 3 if case_id in {"V3-013", "V3-014", "V3-015"} else 1
        require(len(case["turns"]) == expected_turns, f"{case_id}: turn count")
        turn_total += expected_turns
        for index, turn in enumerate(case["turns"], start=1):
            require(
                set(turn) == TURN_KEYS
                and turn["turn_index"] == index
                and isinstance(turn["input_raw"], str)
                and bool(turn["input_raw"]),
                f"{case_id}: turn schema",
            )
            if case_id not in {"V3-017", "V3-018"}:
                require(turn["image_path"] is None, f"{case_id}: unexpected image")
        if case_id in {"V3-017", "V3-018"}:
            image_path = ROOT / case["turns"][0]["image_path"]
            require(image_path.is_file(), f"{case_id}: missing image")
            dimensions = png_dimensions(image_path)
            require(dimensions == (1080, 720), f"{case_id}: image dimensions")
            require(
                case["turns"][0]["input_raw"].lower().count("review") >= 1
                or "check" in case["turns"][0]["input_raw"].lower(),
                f"{case_id}: image review request",
            )
            require(case["image_spec"] is not None, f"{case_id}: image spec")
        else:
            require(case["image_spec"] is None, f"{case_id}: image spec leakage")
        require(
            all(
                isinstance(note[field], str) and bool(note[field])
                for field in NOTE_KEYS - {"case_id"}
            ),
            f"{case_id}: note content",
        )
    require(turn_total == 24, "turn total")

    baseline_path = CLOUD / "baseline-manifest.json"
    if baseline_path.is_file():
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
        for field in (
            "methodology",
            "scorer",
            "plan",
            "case_brief",
            "cases",
            "oracle_notes",
            "designer_attestation",
        ):
            path = ROOT / baseline[field]["path"]
            require(path.is_file() and digest(path) == baseline[field]["sha256"], field)
        for item in baseline["images"] + baseline["runtime"]["runtime_sources"]:
            path = ROOT / item["path"]
            require(path.is_file() and digest(path) == item["sha256"], str(path))
    print("validated fresh v3 holdout: 18 cases, 24 turns, 2 images")


if __name__ == "__main__":
    main()
