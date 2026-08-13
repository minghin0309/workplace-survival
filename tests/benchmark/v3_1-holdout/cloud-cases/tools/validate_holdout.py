#!/usr/bin/env python3
"""Mechanical validator for the v3.1 cloud holdout (attempt 2).

Checks, in order:

1. envelope schema, case and turn counts, turn ordering, image wiring;
2. the distribution the brief specifies, by case id band;
3. the question-candidate contract and the six distinct primary concepts;
4. the three mutation state transitions for every candidate;
5. leakage: absent answers, answer fixtures, mutation text and construction
   vocabulary must not reach any SUT-visible field, the notes, or the pixels;
6. the aggregate novelty denylist, including single-token near-misses;
7. image determinism: two independent re-renders must reproduce the committed
   bytes and the sha256 recorded in the envelope.

The validator reads only the files this holdout owns. It never opens a prior
case set, a runtime, a scorer or a rubric.

Exit code 0 means every check passed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

CASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_images  # noqa: E402  (local construction tool)

CASES_PATH = CASE_DIR / "cases.json"
NOTES_PATH = CASE_DIR / "oracle-notes.json"
DESIGN_PATH = CASE_DIR / "question-design.json"
ATTESTATION_PATH = CASE_DIR / "designer-attestation.json"

EXPECTED_CASE_IDS = [f"V31-{n:03d}" for n in range(1, 19)]
THREE_TURN_CASES = {"V31-014", "V31-015", "V31-016"}
CANDIDATE_CASES = [f"V31-{n:03d}" for n in range(4, 10)]
EXPECTED_TURNS = 24

BRIEF_CONCEPTS = [
    "approval-authority",
    "confirmed-deadline",
    "intended-recipient",
    "traceable-source",
    "material-measurement",
    "required-decision-option",
]

CASE_KEYS = {"case_id", "recipient_context", "data_a", "turns"}
RECIPIENT_KEYS = {
    "recipient_name",
    "recipient_role",
    "relationship_to_user",
    "channel",
    "audience_scope",
    "additional_recipients",
}
DATA_A_KEYS = {
    "user_role",
    "organization",
    "site",
    "situation",
    "known_facts",
    "constraints",
}
TURN_KEYS = {
    "turn_index",
    "turn_id",
    "user_message",
    "draft_message",
    "image_path",
    "image_spec",
}
IMAGE_SPEC_KEYS = {
    "format",
    "width",
    "height",
    "color_mode",
    "background_hex",
    "font_family",
    "deterministic",
    "sha256",
}

DESIGN_ENTRY_KEYS = {
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

MUTATION_TRANSITIONS = {
    "REMOVE_DEPENDENCY": {
        "dependency_present": False,
        "answer_absent": True,
        "question_required": False,
        "clean_question_candidate": False,
        "direct_red_defects_empty": True,
    },
    "SUPPLY_ANSWER": {
        "dependency_present": True,
        "answer_absent": False,
        "question_required": False,
        "clean_question_candidate": False,
        "direct_red_defects_empty": True,
    },
    "ADD_DOMINANT_RED": {
        "dependency_present": True,
        "answer_absent": True,
        "question_required": True,
        "clean_question_candidate": False,
        "direct_red_defects_empty": False,
    },
}

DENYLIST_PHRASES = [
    "cargo-bike delivery",
    "cargo bike",
    "cargo-bike",
    "freight depot",
    "ceramics",
    "ceramic",
    "pottery",
    "kiln",
    "glaze",
    "glazing",
    "clay",
    "municipal water",
    "geothermal",
    "seed bank",
    "esports",
    "subtitling",
    "dubbing",
    "veterinary",
    "telehealth",
    "insurance claim",
    "offshore wind",
    "archive digitisation",
    "archive digitization",
    "mycelium",
    "heritage trust",
    "lighthouse",
    "drone",
    "bakery",
    "ornithology",
    "puppet",
    "marionette",
    "hydrographic",
    "funicular",
    "planetarium",
    "organ restoration",
    "solar carport",
    "timber kiln",
    "curling ice",
    "ground remediation",
    "sterile services",
    "dye works",
    "compounding pharmacy",
    "snow clearance",
    "seismograph",
    "mirror coating",
    "forensic accounting",
    "sauna",
    "orchard frost",
    "tunnel ventilation",
    "marine winch",
    "co-operative",
    "cooperative",
    "co-op",
]

# Single tokens refused as well, so that no denied domain is reached by rename.
DENYLIST_TOKENS = [
    "potter",
    "dye",
    "timber",
    "mirror",
    "winch",
    "organ",
    "orchard",
    "tunnel",
    "curling",
    "freight",
    "depot",
    "forensic",
    "sterile",
    "pharmacy",
    "remediation",
    "digitisation",
    "seed",
    "esport",
    "insurance",
]

# Construction vocabulary that must never appear in the SUT-visible envelope.
CASES_BANNED_TOKENS = [
    "missing_concept",
    "answer_fixture",
    "dependency_present",
    "answer_absent",
    "placeholder_safe",
    "qualification_safe",
    "omission_safe",
    "direct_red_defects",
    "question_design",
    "question-design",
    "oracle",
    "rubric",
    "scorer",
    "denylist",
    "construction_notes",
    "brief_band",
    "REMOVE_DEPENDENCY",
    "SUPPLY_ANSWER",
    "ADD_DOMINANT_RED",
    "mutation",
    "candidate",
    "green",
    "red",
    "ask",
    "gold",
    "verdict",
    "grade",
    "score",
    "label",
    "defect",
]

# Vocabulary of judgement that must not appear in the notes.
NOTES_BANNED_TOKENS = [
    "green",
    "red",
    "ask",
    "gold",
    "rubric",
    "scorer",
    "verdict",
    "grade",
    "score",
    "label",
    "candidate",
    "defect",
    "answer_fixture",
    "mutation",
]


class Report:
    def __init__(self) -> None:
        self.checks: list[dict[str, object]] = []

    def add(self, name: str, ok: bool, detail: str = "") -> None:
        self.checks.append({"check": name, "ok": bool(ok), "detail": detail})

    def require(self, name: str, ok: bool, detail: str = "") -> bool:
        self.add(name, ok, detail)
        return bool(ok)

    @property
    def failures(self) -> list[dict[str, object]]:
        return [c for c in self.checks if not c["ok"]]


def load(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def strings_of(node: object, path: str = "") -> list[tuple[str, str]]:
    """Every string in a JSON tree, with its dotted location."""
    found: list[tuple[str, str]] = []
    if isinstance(node, dict):
        for key, value in node.items():
            found.extend(strings_of(value, f"{path}.{key}" if path else str(key)))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found.extend(strings_of(value, f"{path}[{index}]"))
    elif isinstance(node, str):
        found.append((path, node))
    return found


def token_hits(tokens: list[str], strings: list[tuple[str, str]]) -> list[str]:
    hits = []
    for token in tokens:
        pattern = re.compile(rf"\b{re.escape(token)}\b", re.IGNORECASE)
        for location, text in strings:
            if pattern.search(text):
                hits.append(f"{token!r} at {location}")
    return hits


def phrase_hits(phrases: list[str], strings: list[tuple[str, str]]) -> list[str]:
    hits = []
    for phrase in phrases:
        needle = phrase.lower()
        for location, text in strings:
            if needle in text.lower():
                hits.append(f"{phrase!r} at {location}")
    return hits


def check_envelope(cases_doc: dict, report: Report) -> None:
    cases = cases_doc.get("cases", [])
    report.require("envelope: version is v3.1", cases_doc.get("envelope_version") == "v3.1")
    report.require("envelope: 18 cases present", len(cases) == 18, f"found {len(cases)}")
    report.require(
        "envelope: case ids are V31-001..V31-018 in order",
        [c.get("case_id") for c in cases] == EXPECTED_CASE_IDS,
    )
    report.require(
        "envelope: declared case_count matches", cases_doc.get("case_count") == len(cases)
    )

    total_turns = sum(len(c.get("turns", [])) for c in cases)
    report.require(
        "envelope: exactly 24 turns", total_turns == EXPECTED_TURNS, f"found {total_turns}"
    )
    report.require(
        "envelope: declared turn_count matches", cases_doc.get("turn_count") == total_turns
    )

    for case in cases:
        case_id = case.get("case_id", "?")
        report.require(f"{case_id}: case keys exact", set(case) == CASE_KEYS, str(set(case)))
        report.require(
            f"{case_id}: recipient_context keys exact",
            set(case.get("recipient_context", {})) == RECIPIENT_KEYS,
        )
        report.require(
            f"{case_id}: data_a keys exact", set(case.get("data_a", {})) == DATA_A_KEYS
        )
        data_a = case.get("data_a", {})
        report.require(
            f"{case_id}: data_a is structured with non-empty fact and constraint lists",
            isinstance(data_a.get("known_facts"), list)
            and len(data_a["known_facts"]) >= 4
            and isinstance(data_a.get("constraints"), list)
            and len(data_a["constraints"]) >= 2,
        )

        turns = case.get("turns", [])
        expected = 3 if case_id in THREE_TURN_CASES else 1
        report.require(
            f"{case_id}: turn count is {expected}", len(turns) == expected, f"found {len(turns)}"
        )
        for position, turn in enumerate(turns, start=1):
            report.require(f"{case_id}-T{position}: turn keys exact", set(turn) == TURN_KEYS)
            report.require(
                f"{case_id}-T{position}: turn_index ordered", turn.get("turn_index") == position
            )
            report.require(
                f"{case_id}-T{position}: turn_id matches case and position",
                turn.get("turn_id") == f"{case_id}-T{position}",
            )
            report.require(
                f"{case_id}-T{position}: user_message present",
                isinstance(turn.get("user_message"), str) and turn["user_message"].strip() != "",
            )
            image_path = turn.get("image_path")
            if image_path is None:
                report.require(
                    f"{case_id}-T{position}: non-image turn has null image_spec",
                    turn.get("image_spec") is None,
                )
            else:
                report.require(
                    f"{case_id}-T{position}: image turn carries no text draft",
                    turn.get("draft_message") is None,
                )
                spec = turn.get("image_spec")
                report.require(
                    f"{case_id}-T{position}: image_spec keys exact",
                    isinstance(spec, dict) and set(spec) == IMAGE_SPEC_KEYS,
                )
                report.require(
                    f"{case_id}-T{position}: image file exists",
                    (CASE_DIR / image_path).exists(),
                    image_path,
                )


def check_distribution(cases_doc: dict, design_doc: dict, report: Report) -> None:
    image_cases = sorted(
        {
            case["case_id"]
            for case in cases_doc["cases"]
            for turn in case["turns"]
            if turn.get("image_path")
        }
    )
    report.require(
        "distribution: three-turn cases are exactly V31-014..V31-016",
        {
            c["case_id"] for c in cases_doc["cases"] if len(c["turns"]) == 3
        } == THREE_TURN_CASES,
    )
    report.require(
        "distribution: question candidates are exactly V31-004..V31-009",
        [e["case_id"] for e in design_doc["entries"]] == CANDIDATE_CASES,
    )
    report.require(
        "distribution: V31-018 is an image case", "V31-018" in image_cases, str(image_cases)
    )
    candidate_image_cases = [
        e["case_id"] for e in design_doc["entries"] if e.get("image_only_draft") is True
    ]
    report.require(
        "distribution: at least one candidate uses an image-only draft",
        len(candidate_image_cases) >= 1,
        str(candidate_image_cases),
    )
    for case_id in candidate_image_cases:
        report.require(
            f"{case_id}: image-only candidate has an image turn and no text draft",
            case_id in image_cases,
        )
    report.require(
        "distribution: V31-018 is not used as a question candidate",
        "V31-018" not in CANDIDATE_CASES,
    )


def check_candidate_contract(design_doc: dict, report: Report) -> None:
    concepts = [e["missing_concept"] for e in design_doc["entries"]]
    report.require(
        "candidates: six entries", len(design_doc["entries"]) == 6, f"found {len(concepts)}"
    )
    report.require(
        "candidates: six distinct primary concepts", len(set(concepts)) == 6, str(concepts)
    )
    report.require(
        "candidates: concepts are the six the brief names",
        sorted(concepts) == sorted(BRIEF_CONCEPTS),
        str(sorted(concepts)),
    )

    for entry in design_doc["entries"]:
        case_id = entry["case_id"]
        report.require(
            f"{case_id}: every key the brief specifies is present",
            DESIGN_ENTRY_KEYS.issubset(set(entry)),
            str(sorted(DESIGN_ENTRY_KEYS - set(entry))),
        )
        report.require(f"{case_id}: dependency_present is true", entry["dependency_present"] is True)
        report.require(f"{case_id}: answer_absent is true", entry["answer_absent"] is True)
        report.require(f"{case_id}: placeholder_safe is false", entry["placeholder_safe"] is False)
        report.require(
            f"{case_id}: qualification_safe is false", entry["qualification_safe"] is False
        )
        report.require(f"{case_id}: omission_safe is false", entry["omission_safe"] is False)
        report.require(
            f"{case_id}: no independent direct Red defect", entry["direct_red_defects"] == []
        )
        report.require(
            f"{case_id}: answer fixture present",
            isinstance(entry["answer_fixture"], str) and entry["answer_fixture"].strip() != "",
        )
        report.require(
            f"{case_id}: safe completion enabled by the answer",
            entry["safe_completion_enabled_by_answer"] is True,
        )
        report.require(
            f"{case_id}: question unnecessary without the dependency",
            entry["question_unnecessary_without_dependency"] is True,
        )
        report.require(
            f"{case_id}: no competing unrelated unknown", entry.get("competing_unknowns") == []
        )
        base = entry.get("base_state", {})
        report.require(
            f"{case_id}: base state matches the contract",
            base
            == {
                "dependency_present": True,
                "answer_absent": True,
                "question_required": True,
                "direct_red_defects": [],
                "clean_question_candidate": True,
            },
            json.dumps(base, sort_keys=True),
        )


def check_mutations(design_doc: dict, report: Report) -> None:
    for entry in design_doc["entries"]:
        case_id = entry["case_id"]
        mutations = entry.get("mutations", [])
        types = [m.get("mutation_type") for m in mutations]
        report.require(f"{case_id}: three mutations", len(mutations) == 3, str(types))
        report.require(
            f"{case_id}: one mutation of each required type",
            sorted(types) == sorted(MUTATION_TRANSITIONS),
            str(sorted(types)),
        )
        for mutation in mutations:
            kind = mutation.get("mutation_type")
            expected = MUTATION_TRANSITIONS.get(kind)
            if expected is None:
                report.add(f"{case_id}: unknown mutation type", False, str(kind))
                continue
            state = mutation.get("resulting_state", {})
            label = f"{case_id}/{kind}"
            report.require(
                f"{label}: inserted_text present",
                isinstance(mutation.get("inserted_text"), str)
                and mutation["inserted_text"].strip() != "",
            )
            for key in ("dependency_present", "answer_absent", "question_required", "clean_question_candidate"):
                report.require(
                    f"{label}: {key} becomes {expected[key]}",
                    state.get(key) is expected[key],
                    f"found {state.get(key)!r}",
                )
            empty = state.get("direct_red_defects") == []
            report.require(
                f"{label}: direct_red_defects "
                + ("stays empty" if expected["direct_red_defects_empty"] else "is non-empty"),
                empty is expected["direct_red_defects_empty"],
                str(state.get("direct_red_defects")),
            )
            report.require(
                f"{label}: transition changes the base state",
                state
                != {
                    "dependency_present": True,
                    "answer_absent": True,
                    "question_required": True,
                    "direct_red_defects": [],
                    "clean_question_candidate": True,
                },
            )


def check_leakage(cases_doc: dict, notes_doc: dict, design_doc: dict, report: Report) -> None:
    case_strings = strings_of(cases_doc)
    note_strings = strings_of(notes_doc)
    image_strings: list[tuple[str, str]] = []
    for case_id in generate_images.IMAGES:
        for line in generate_images.visible_text(case_id):
            image_strings.append((f"pixels:{case_id}", line))

    visible = case_strings + image_strings

    for entry in design_doc["entries"]:
        case_id = entry["case_id"]
        tokens = entry.get("absent_answer_tokens", [])
        report.require(f"{case_id}: absent answer tokens listed", len(tokens) >= 1)
        hits = phrase_hits(tokens, visible)
        report.require(
            f"{case_id}: absent answer never reaches an SUT-visible field or the pixels",
            not hits,
            "; ".join(hits),
        )
        note_hits = phrase_hits(tokens, note_strings)
        report.require(
            f"{case_id}: absent answer never reaches the notes", not note_hits, "; ".join(note_hits)
        )
        fixture_hits = phrase_hits([entry["answer_fixture"]], visible + note_strings)
        report.require(
            f"{case_id}: answer fixture appears only in the construction file",
            not fixture_hits,
            "; ".join(fixture_hits),
        )
        for mutation in entry.get("mutations", []):
            inserted = mutation.get("inserted_text", "")
            hits = phrase_hits([inserted], visible + note_strings)
            report.require(
                f"{case_id}/{mutation.get('mutation_type')}: mutation text stays outside the envelope",
                not hits,
                "; ".join(hits),
            )
            for line in mutation.get("mutated_render_lines", []) or []:
                hits = phrase_hits([line.strip()], image_strings)
                report.require(
                    f"{case_id}/{mutation.get('mutation_type')}: mutated render line is not in the shipped pixels",
                    not hits,
                    "; ".join(hits),
                )

    hits = token_hits(CASES_BANNED_TOKENS, case_strings)
    report.require(
        "leakage: no construction or judgement vocabulary in cases.json", not hits, "; ".join(hits)
    )
    hits = token_hits(NOTES_BANNED_TOKENS, note_strings)
    report.require(
        "leakage: no judgement vocabulary in oracle-notes.json", not hits, "; ".join(hits)
    )
    design_keys = {"missing_concept", "answer_fixture", "mutations", "base_state", "resulting_state"}
    flat_cases = json.dumps(cases_doc)
    hits = [key for key in design_keys if key in flat_cases]
    report.require("leakage: no question-design keys in cases.json", not hits, str(hits))

    notes_case_ids = [n["case_id"] for n in notes_doc["case_notes"]]
    report.require(
        "notes: one note per case in order", notes_case_ids == EXPECTED_CASE_IDS, str(notes_case_ids)
    )
    for note in notes_doc["case_notes"]:
        case = next(c for c in cases_doc["cases"] if c["case_id"] == note["case_id"])
        report.require(
            f"{note['case_id']}: note turn count matches the envelope",
            note["turn_count"] == len(case["turns"]),
        )
        image_turns = sum(1 for t in case["turns"] if t.get("image_path"))
        report.require(
            f"{note['case_id']}: note image count matches the envelope",
            note["image_turns"] == image_turns,
        )


def check_denylist(docs: dict[str, object], report: Report) -> None:
    for name, doc in docs.items():
        strings = strings_of(doc)
        hits = phrase_hits(DENYLIST_PHRASES, strings)
        report.require(f"denylist: no prohibited domain phrase in {name}", not hits, "; ".join(hits))
        hits = token_hits(DENYLIST_TOKENS, strings)
        report.require(f"denylist: no near-miss token in {name}", not hits, "; ".join(hits))

    image_strings = [
        (f"pixels:{case_id}", line)
        for case_id in generate_images.IMAGES
        for line in generate_images.visible_text(case_id)
    ]
    hits = phrase_hits(DENYLIST_PHRASES, image_strings) + token_hits(DENYLIST_TOKENS, image_strings)
    report.require("denylist: no prohibited term rendered into the pixels", not hits, "; ".join(hits))


def check_images(cases_doc: dict, report: Report) -> dict[str, str]:
    committed: dict[str, str] = {}
    for case in cases_doc["cases"]:
        for turn in case["turns"]:
            if not turn.get("image_path"):
                continue
            path = CASE_DIR / turn["image_path"]
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            committed[case["case_id"]] = digest
            report.require(
                f"{case['case_id']}: envelope sha256 matches the committed file",
                digest == turn["image_spec"]["sha256"],
                digest,
            )
            spec = turn["image_spec"]
            gen = generate_images.IMAGES[case["case_id"]]
            report.require(
                f"{case['case_id']}: image_spec dimensions match the renderer",
                (spec["width"], spec["height"]) == (gen["width"], gen["height"]),
            )
            report.require(
                f"{case['case_id']}: image_spec background matches the renderer",
                spec["background_hex"].lower()
                == "#%02x%02x%02x" % tuple(gen["background"]),
                spec["background_hex"],
            )

    digests: list[dict[str, str]] = []
    for _ in range(2):
        temp = Path(tempfile.mkdtemp(prefix="v31-determinism-"))
        try:
            rendered = generate_images.render_all(temp)
            digests.append({k: v["sha256"] for k, v in rendered.items()})
        finally:
            shutil.rmtree(temp, ignore_errors=True)
    report.require(
        "images: two independent re-renders agree byte for byte",
        digests[0] == digests[1],
        json.dumps(digests, sort_keys=True),
    )
    report.require(
        "images: re-render reproduces the committed bytes",
        digests[0] == committed,
        json.dumps({"rendered": digests[0], "committed": committed}, sort_keys=True),
    )
    return committed


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path, help="write the full report to this path")
    args = parser.parse_args(argv)

    cases_doc = load(CASES_PATH)
    notes_doc = load(NOTES_PATH)
    design_doc = load(DESIGN_PATH)

    report = Report()
    check_envelope(cases_doc, report)
    check_distribution(cases_doc, design_doc, report)
    check_candidate_contract(design_doc, report)
    check_mutations(design_doc, report)
    check_leakage(cases_doc, notes_doc, design_doc, report)
    check_denylist(
        {
            "cases.json": cases_doc,
            "oracle-notes.json": notes_doc,
            "question-design.json": design_doc,
        },
        report,
    )
    digests = check_images(cases_doc, report)

    if ATTESTATION_PATH.exists():
        attestation = load(ATTESTATION_PATH)
        recorded = {
            item["case_id"]: item["sha256"]
            for item in attestation.get("images", {}).get("files", [])
        }
        report.require(
            "attestation: recorded image hashes match the committed files",
            recorded == digests,
            json.dumps({"attestation": recorded, "files": digests}, sort_keys=True),
        )

    summary = {
        "total_checks": len(report.checks),
        "failed": len(report.failures),
        "failures": report.failures,
        "image_sha256": digests,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.json:
        args.json.write_text(
            json.dumps({"summary": summary, "checks": report.checks}, indent=2, sort_keys=True),
            encoding="utf-8",
        )
    return 1 if report.failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
