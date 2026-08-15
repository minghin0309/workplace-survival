import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tests/benchmark/v3_1"))
sys.path.insert(0, str(ROOT / "tests/benchmark/v3_2"))

import question_candidate_contract as qcontract
import recipient_manager_contract as rcontract


CLOUD = ROOT / "tests/benchmark/v3_2-holdout/attempt-3/cloud-cases"
QUESTION_IDS = [f"V323-{index:03d}" for index in range(4, 10)]
ROUTING_ID = "V323-017"
THREE_TURN_IDS = {"V323-014", "V323-015", "V323-016"}
DENYLIST = [
    "cargo-bike",
    "cargo bike",
    "freight depot",
    "ceramics",
    "pottery",
    "kiln-production",
    "glaze",
    "municipal water",
    "geothermal",
    "seed bank",
    "esports",
    "subtitling",
    "dubbing",
    "veterinary telehealth",
    "insurance claim",
    "offshore wind",
    "archive digitisation",
    "archive digitization",
    "mycelium",
    "heritage trust",
    "lighthouse",
    "drone operation",
    "bakery",
    "ornithology",
    "marionette",
    "puppet theatre",
    "puppet theater",
    "hydrographic",
    "funicular",
    "planetarium",
    "organ restoration",
    "solar carport",
    "timber kiln",
    "curling ice",
    "ground remediation",
    "sterile service",
    "dye work",
    "compounding pharmac",
    "snow clearance",
    "seismograph",
    "mirror coating",
    "forensic accounting",
    "sauna manufactur",
    "orchard frost",
    "tunnel ventilation",
    "marine winch",
    "millinery",
    "milliner",
    "hatmaking",
    "hat-making",
    "hat block",
    "hat-block",
    "petersham",
    "sinamay",
    "straw plait",
    "harpworks",
    "pedal-harp",
    "pedal harp",
    "gut string",
    "gut-string",
    "pedal-rod",
    "pedal rod",
    "humidity cabinet",
    "quillsmere",
    "marit osgarde",
    "ferrowhite",
    "marchmont enclosure",
    "ashvale bridal",
    "menkes blockworks",
    "bellhouse yard",
    "ardhu lane",
    "thurlow & vane",
    "solberg straw",
    "cranthorpe",
    "ilex",
    "norrish",
    "coppice loft",
    "grellhaven",
    "vellum court",
    "braxton-yew",
    "padraig orliss",
    "vantsel",
    "corrindale",
    "halvern",
    "kelbrand",
    "tessaly",
    "ostrelle",
    "brandmoor",
    "halbrook",
    "fennmark",
    "vallonde",
    "rjukan",
    "marisco",
    "alderhoff",
    "tarnwick",
    "cavallini",
    "ashcombe",
    "halvard",
    "kestrel freight",
    "umber & kiln",
    "vireo valley",
    "lantern row",
    "basalt deep",
    "anvil ridge",
    "static meridian",
    "pawline",
    "grey halyard",
    "foxglove records",
    "chanterelle systems",
    "northbell mutual",
    "saltmark trust",
    "halcyon skyway",
    "ovenwright",
    "tern hollow",
    "brindle marionette",
    "fathom line",
    "aerostat",
    "hot-air balloon",
    "hot air balloon",
    "balloon",
    "gondola",
    "hangar",
    "envelope hall",
    "gore cutting",
    "load tape",
    "rip panel",
    "ripstop",
    "hangar-card",
    "hangar card",
    "mouth-tape",
    "mouth tape",
    "cubic-foot envelope",
    "thornwick",
    "spindlefen",
    "saira vennick",
    "bram cotrell",
    "ivo drellan",
    "mirelle oatswell",
    "pell oswaithe",
    "wardenmere",
    "pellwick",
    "brackfen",
    "rn-7602",
    "rn-7609",
    "rn-7741",
    "tw-441",
    "tw-508",
    "tw-512",
    "tw-519",
    "tw-530",
    "tw-547",
    "tw-561",
    "tw-574",
    "tw-588",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _mutation_name(mutation: dict) -> str:
    return mutation.get("mutation_type") or mutation["mutation"]


def core(entry: dict) -> dict:
    if qcontract.REQUIRED_KEYS <= set(entry):
        return {key: entry[key] for key in qcontract.REQUIRED_KEYS}
    base = entry.get("base_state") or {}
    mutations = {
        _mutation_name(item): item.get("resulting_state") or {}
        for item in entry.get("mutations") or []
    }
    independent_red = bool(base.get("independent_red"))
    placeholder = bool(base.get("qualification_or_placeholder_sufficient"))
    return {
        "case_id": entry["case_id"],
        "missing_concept": entry.get("missing_concept") or entry["primary_concept"],
        "dependency_present": True,
        "answer_absent": True,
        "placeholder_safe": placeholder,
        "qualification_safe": placeholder,
        "omission_safe": bool(base.get("complete_safe_message_without_answer")),
        "direct_red_defects": ["independent-red"] if independent_red else [],
        "answer_fixture": entry["answer_fixture"],
        "safe_completion_enabled_by_answer": bool(
            mutations.get("SUPPLY_ANSWER", {}).get(
                "complete_safe_message_possible", True
            )
        ),
        "question_unnecessary_without_dependency": not bool(
            mutations.get("REMOVE_DEPENDENCY", {}).get("question_necessary", False)
        ),
    }


def flatten(value) -> str:
    if isinstance(value, dict):
        return " ".join(flatten(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(flatten(item) for item in value)
    return str(value)


def main() -> None:
    cases = json.loads((CLOUD / "cases.json").read_text(encoding="utf-8"))
    notes = json.loads((CLOUD / "oracle-notes.json").read_text(encoding="utf-8"))
    design = json.loads(
        (CLOUD / "question-design.json").read_text(encoding="utf-8")
    )
    design_entries = design.get("entries") or design.get("candidates")
    require(bool(design_entries), "question-design entries")
    mutations = json.loads(
        (CLOUD / "construction-mutations.json").read_text(encoding="utf-8")
    )
    mutation_rows = mutations.get("mutations") or mutations.get("rows")
    require(isinstance(mutation_rows, list), "construction mutation rows")
    expected_ids = [f"V323-{index:03d}" for index in range(1, 19)]
    require(
        cases["case_count"] == 18
        and cases["turn_count"] == 24
        and cases.get("suite_id") == "v32-holdout-cloud-attempt3"
        and [case["case_id"] for case in cases["cases"]] == expected_ids,
        "case coverage",
    )
    note_rows = notes.get("case_notes") or notes.get("notes")
    require(bool(note_rows), "oracle notes")
    require(
        [note["case_id"] for note in note_rows] == expected_ids,
        "note coverage",
    )
    rcontract.validate_envelope(cases["cases"], QUESTION_IDS, ROUTING_ID)
    turn_total = 0
    image_cases = []
    for case in cases["cases"]:
        case_id = case["case_id"]
        expected_turns = 3 if case_id in THREE_TURN_IDS else 1
        require(len(case["turns"]) == expected_turns, f"{case_id}: turns")
        turn_total += expected_turns
        for index, turn in enumerate(case["turns"], start=1):
            require(
                turn["turn_index"] == index
                and turn["turn_id"] == f"{case_id}-T{index}",
                f"{case_id}: turn order",
            )
            if turn["image_path"] is None:
                require(turn["image_spec"] is None, f"{case_id}: unexpected spec")
            else:
                image_cases.append(case_id)
                require(
                    turn["draft_message"] is None,
                    f"{case_id}: image draft must be pixels-only",
                )
                path = ROOT / turn["image_path"]
                if not path.is_file():
                    path = CLOUD / turn["image_path"]
                require(
                    path.is_file()
                    and path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"),
                    f"{case_id}: PNG",
                )
    require(turn_total == 24, "turn total")
    require("V323-018" in image_cases, "V323-018 image")

    entries = [core(entry) for entry in design_entries]
    qcontract.validate_design(entries)
    require(
        [entry["case_id"] for entry in entries] == QUESTION_IDS,
        "question candidate IDs",
    )
    require(
        any(
            entry.get("image_only_draft") or entry.get("image_only")
            for entry in design_entries
        ),
        "image-only question candidate",
    )
    require(len(mutation_rows) == 18, "construction mutation count")
    by_case = {}
    for mutation in mutation_rows:
        by_case.setdefault(mutation["case_id"], set()).add(mutation["mutation_type"])
    require(
        all(
            by_case[case_id]
            == {"REMOVE_DEPENDENCY", "SUPPLY_ANSWER", "ADD_DOMINANT_RED"}
            for case_id in QUESTION_IDS
        ),
        "construction mutation coverage",
    )

    haystack = " ".join(
        [flatten(cases), flatten(notes), flatten(design)]
    ).lower()
    hits = [term for term in DENYLIST if term in haystack]
    require(not hits, "novelty denylist: " + ", ".join(hits))

    for entry in design_entries:
        tokens = list(entry.get("absent_answer_tokens") or [])
        if entry.get("absent_answer_token"):
            tokens.append(entry["absent_answer_token"])
        visible = flatten(
            next(
                case
                for case in cases["cases"]
                if case["case_id"] == entry["case_id"]
            )
        ).lower()
        leaked = [token for token in tokens if token and token.lower() in visible]
        require(not leaked, f"{entry['case_id']}: answer leak")
        require(
            entry["answer_fixture"] not in visible,
            f"{entry['case_id']}: fixture leak",
        )

    print("validated v3.2 attempt-3 construction: 18 cases, 24 turns, manager gate")


if __name__ == "__main__":
    main()
