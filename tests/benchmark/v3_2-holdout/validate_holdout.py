import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tests/benchmark/v3_1"))

import question_candidate_contract as contract


CLOUD = ROOT / "tests/benchmark/v3_2-holdout/cloud-cases"
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
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def core(entry: dict) -> dict:
    return {key: entry[key] for key in contract.REQUIRED_KEYS}


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
    expected_ids = [f"V32-{index:03d}" for index in range(1, 19)]
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
    image_cases = []
    for case in cases["cases"]:
        case_id = case["case_id"]
        expected_turns = 3 if case_id in {"V32-014", "V32-015", "V32-016"} else 1
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
    require("V32-018" in image_cases, "V32-018 image")

    entries = [core(entry) for entry in design_entries]
    contract.validate_design(entries)
    require(
        [entry["case_id"] for entry in entries]
        == [f"V32-{index:03d}" for index in range(4, 10)],
        "question candidate IDs",
    )
    require(
        any(entry.get("image_only_draft") for entry in design_entries),
        "image-only question candidate",
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
            for case_id in [f"V32-{index:03d}" for index in range(4, 10)]
        ),
        "construction mutation coverage",
    )

    haystack = " ".join(
        [
            flatten(cases),
            flatten(notes),
            flatten(design),
        ]
    ).lower()
    hits = [term for term in DENYLIST if term in haystack]
    require(not hits, "novelty denylist: " + ", ".join(hits))

    for entry in design_entries:
        tokens = entry.get("absent_answer_tokens") or []
        visible = flatten(
            next(
                case
                for case in cases["cases"]
                if case["case_id"] == entry["case_id"]
            )
        ).lower()
        leaked = [
            token
            for token in tokens
            if token and token.lower() in visible
        ]
        require(not leaked, f"{entry['case_id']}: answer leak")
        require(
            entry["answer_fixture"] not in visible,
            f"{entry['case_id']}: fixture leak",
        )

    print("validated v3.2 holdout construction: 18 cases, 24 turns, 6 candidates")


if __name__ == "__main__":
    main()
