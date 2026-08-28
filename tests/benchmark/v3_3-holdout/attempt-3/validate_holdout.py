import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tests/benchmark/v3_1"))
sys.path.insert(0, str(ROOT / "tests/benchmark/v3_2"))
sys.path.insert(0, str(ROOT / "tests/benchmark/v3_3"))

import question_candidate_contract as qcontract
import recipient_manager_contract as rcontract
import revision_scoring_contract as v33contract


CLOUD = ROOT / "tests/benchmark/v3_3-holdout/attempt-3/cloud-cases"
QUESTION_IDS = [f"V333-{index:03d}" for index in range(4, 10)]
ROUTING_ID = "V333-017"
THREE_TURN_IDS = {"V333-014", "V333-015", "V333-016"}
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
    "greaveholt",
    "cold-cathode",
    "cold cathode",
    "nine-rib",
    "nine rib",
    "yarrowbridge",
    "orrin medwick",
    "lise cardenoy",
    "niall peveril",
    "tamsin quelch",
    "kerr adelune",
    "sablewick",
    "parquet room",
    "duskletter",
    "wintle chemist",
    "coppervine",
    "cc-3304",
    "cc-3311",
    "cc-3325",
    "cc-3332",
    "cc-3340",
    "cc-3348",
    "cc-3355",
    "cc-3362",
    "cc-3369",
    "cc-3376",
    "cc-3383",
    "cc-3390",
    "cc-3397",
    "cc-3404",
    "cc-3411",
    "cc-3418",
    "cc-3420",
    "cc-3425",
    "cc-3432",
    "pn-19",
    "ribbon burner",
    "mercury dos",
    "bombard-transformer",
    "bombard transformer",
    "wetherlees",
    "turret-clock",
    "turret clock",
    "quoyfen",
    "spire yard",
    "calder vossine",
    "neris holbeck",
    "colm yardrie",
    "merrin daske",
    "kellstrand",
    "barleywick",
    "gathering-pallet",
    "gathering pallet",
    "beat-rating",
    "beat rating",
    "keepership",
    "compensation rod",
    "chime-train",
    "chime train",
    "pendulum rating",
    "click-spring",
    "click spring",
    "kr-2281",
    "cs-6",
    "jc-4418",
    "jc-4520",
    "jc-4603",
    "jc-4711",
    "jc-4805",
    "jc-4912",
    "jc-5028",
    "jc-5116",
    "jc-5233",
    "jc-5340",
    "jc-5409",
    "jc-5517",
    "jc-5624",
    "jc-5731",
    "jc-5806",
    "jc-5914",
    "jc-6022",
    "jc-6110",
    "rowanleat",
    "braydon cut",
    "wren calloway",
    "edlyn marrow",
    "gareth pumice",
    "osa flint",
    "dorrin kedge",
    "pria osmund",
    "anwen trell",
    "quent isolde",
    "house oxbow",
    "mallowfrith",
    "montedor",
    "cork work",
    "cork-bark",
    "cork bark",
    "cork stopper",
    "stopper punching",
    "colmation",
    "agglomerat",
    "steam-expansion",
    "steam expansion",
    "house-mark",
    "lenticel",
    "cn-448",
    "cn-451",
    "cn-452",
    "bk-2218",
    "bk-2230",
    "bk-2231",
    "bk-2241",
    "bk-2244",
    "rc-8804",
    "rc-8807",
    "rc-8810",
    "rc-8811",
    "rc-8812",
    "rc-8813",
    "cork",
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
    expected_ids = [f"V333-{index:03d}" for index in range(1, 19)]
    require(
        cases["case_count"] == 18
        and cases["turn_count"] == 24
        and cases.get("suite_id") == "v333-holdout-cloud-attempt3"
        and cases.get("envelope_version") == "v3.3"
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
    require("V333-018" in image_cases, "V333-018 image")

    entries = [core(entry) for entry in design_entries]
    qcontract.validate_design(entries)
    require(
        [entry["case_id"] for entry in entries] == QUESTION_IDS,
        "question candidate IDs",
    )
    require(
        mutations.get("schema_version") == "v3.3",
        "construction mutation schema_version",
    )
    require(
        mutations.get("suite_id") == "v333-holdout-cloud-attempt3",
        "construction mutation suite_id",
    )
    require(
        any(
            entry.get("image_only_draft") or entry.get("image_only")
            for entry in design_entries
        ),
        "image-only question candidate",
    )
    for entry in design_entries:
        require(
            entry.get("writer_holds_answer") is True,
            f"{entry['case_id']}: writer_holds_answer",
        )
        require(
            entry.get("data_b_contains_unconfirmed_token") is not True,
            f"{entry['case_id']}: Data B unconfirmed token",
        )
        if entry.get("image_only") or entry.get("image_only_draft"):
            require(
                entry.get("occluded_role") in v33contract.OCCLUDED_ROLES,
                f"{entry['case_id']}: occluded_role",
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

    print("validated v3.3 attempt-3 construction: 18 cases, 24 turns, manager gate")


if __name__ == "__main__":
    main()
