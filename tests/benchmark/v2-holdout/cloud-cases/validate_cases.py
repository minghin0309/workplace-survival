"""Structural validation for the cloud-designed v2 holdout case set.

Checks the case schema, the required category distribution, turn counts, the
rendered PNGs, and that oracle notes carry no factual rating inputs.
Exits non-zero on the first failure so it can be run in CI.
"""

import json
import pathlib
import re
import sys

from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]

CASE_KEYS = {"case_id", "category", "recipient_context", "data_a", "turns", "image_spec"}
TURN_KEYS_REQUIRED = {"turn_index", "input_raw"}
TURN_KEYS_OPTIONAL = {"image_path"}
NOTE_KEYS = {"case_id", "design_intent", "difficulty_notes"}

EXPECTED_DISTRIBUTION = {
    "green_control": 4,
    "responsibility": 3,
    "tone": 3,
    "multi_round": 3,
    "provenance_prompt": 2,
    "recipient_routing": 1,
    "image_ocr": 2,
}
MIN_TOTAL_TURNS = 21
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

failures = []


def check(condition, message):
    if not condition:
        failures.append(message)


def walk_strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from walk_strings(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_strings(value)


def main():
    cases_doc = json.loads((HERE / "cases.json").read_text())
    notes_doc = json.loads((HERE / "oracle-notes.json").read_text())
    cases = cases_doc["cases"]
    notes = notes_doc["notes"]

    check(len(cases) == 18, f"expected 18 cases, found {len(cases)}")

    expected_ids = [f"V2-{n:03d}" for n in range(1, 19)]
    check([c["case_id"] for c in cases] == expected_ids, "case ids are not V2-001..V2-018 in order")

    distribution = {}
    total_turns = 0

    for case in cases:
        cid = case["case_id"]
        check(set(case) == CASE_KEYS, f"{cid}: key set is {sorted(set(case))}, expected {sorted(CASE_KEYS)}")
        check("case_designer_notes" not in case, f"{cid}: case_designer_notes must not be present")
        check(case["category"] in EXPECTED_DISTRIBUTION, f"{cid}: unknown category {case['category']}")
        distribution[case["category"]] = distribution.get(case["category"], 0) + 1

        check(isinstance(case["recipient_context"], str) and case["recipient_context"].strip(),
              f"{cid}: recipient_context must be a non-empty string")

        data_a = case["data_a"]
        check(isinstance(data_a, dict) and data_a, f"{cid}: data_a must be a non-empty object")
        for required in ("organization", "sender", "manager", "situation_facts"):
            check(required in data_a, f"{cid}: data_a missing {required}")
        check(isinstance(data_a.get("situation_facts"), list) and len(data_a["situation_facts"]) >= 5,
              f"{cid}: data_a.situation_facts must list at least five facts")

        turns = case["turns"]
        check(isinstance(turns, list) and turns, f"{cid}: turns must be a non-empty list")
        total_turns += len(turns)
        for position, turn in enumerate(turns, start=1):
            check(turn.get("turn_index") == position, f"{cid}: turn {position} has turn_index {turn.get('turn_index')}")
            check(TURN_KEYS_REQUIRED <= set(turn) <= (TURN_KEYS_REQUIRED | TURN_KEYS_OPTIONAL),
                  f"{cid}: turn {position} key set is {sorted(set(turn))}")
            check(isinstance(turn["input_raw"], str) and turn["input_raw"].strip(),
                  f"{cid}: turn {position} input_raw must be a non-empty string")

        spec = case["image_spec"]
        if case["category"] == "image_ocr":
            check(isinstance(spec, dict), f"{cid}: image_ocr case must carry an image_spec object")
            paths = [t["image_path"] for t in turns if "image_path" in t]
            check(len(paths) == 1, f"{cid}: image_ocr case must have exactly one turn with an image_path")
            for rel in paths:
                png = REPO / rel
                check(png.is_file(), f"{cid}: missing image file {rel}")
                if png.is_file():
                    head = png.read_bytes()[:8]
                    check(head == PNG_MAGIC, f"{cid}: {rel} is not a PNG (bad magic bytes)")
                    with Image.open(png) as im:
                        im.verify()
                    with Image.open(png) as im:
                        check(im.format == "PNG", f"{cid}: {rel} format is {im.format}")
                        check(im.size == (spec["width"], spec["height"]),
                              f"{cid}: {rel} size {im.size} does not match image_spec")
                check(spec.get("path") == rel, f"{cid}: image_spec.path does not match the turn image_path")
            check(bool(spec.get("rendered_text_lines")), f"{cid}: image_spec must record rendered_text_lines")
            body = " ".join(spec["rendered_text_lines"]).lower()
            for turn in turns:
                overlap = turn["input_raw"].lower()
                check(body[:40] not in overlap, f"{cid}: draft text from the image is duplicated in input_raw")
        else:
            check(spec is None, f"{cid}: non image_ocr case must have image_spec null")
            check(all("image_path" not in t for t in turns), f"{cid}: non image_ocr case must not set image_path")

        if case["category"] == "multi_round":
            check(len(turns) >= 3, f"{cid}: multi_round case must have at least three turns")

    check(distribution == EXPECTED_DISTRIBUTION,
          f"category distribution {distribution} != required {EXPECTED_DISTRIBUTION}")
    check(total_turns >= MIN_TOTAL_TURNS, f"total turns {total_turns} is below the required {MIN_TOTAL_TURNS}")

    # Oracle notes: exact key set, full coverage, and no factual rating inputs.
    check(len(notes) == 18, f"expected 18 oracle notes, found {len(notes)}")
    check([n["case_id"] for n in notes] == expected_ids, "oracle note ids do not match the case ids in order")

    proper_nouns = set()
    for case in cases:
        haystack = " ".join(walk_strings({k: v for k, v in case.items() if k != "category"}))
        for token in re.findall(r"\b[A-Z][a-z]{3,}\b", haystack):
            proper_nouns.add(token)
    stopwords = {
        "This", "That", "These", "Those", "When", "With", "Direct", "Screenshot",
        "Following", "About", "Need", "Here", "Quick", "Draft", "Slack", "Email",
        "Purchase", "Sending", "Their", "There", "Escalating", "Just", "Anything",
        "Before", "From", "Over", "Each", "Only", "Even", "Both", "Also", "Some",
        "Should", "Sorry", "Sure", "Hope", "Nothing", "Comes", "Happy", "Left",
        "Reads", "Wanted", "Update", "Round", "Round", "None",
    }
    proper_nouns -= stopwords

    for note in notes:
        check(set(note) == NOTE_KEYS, f"{note['case_id']}: note key set is {sorted(set(note))}")
        text = f"{note['design_intent']} {note['difficulty_notes']}"
        check(not re.search(r"\d", text), f"{note['case_id']}: oracle note contains a digit (possible factual input)")
        leaked = sorted(n for n in proper_nouns if re.search(rf"\b{re.escape(n)}\b", text))
        check(not leaked, f"{note['case_id']}: oracle note leaks case entities {leaked}")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        print(f"\n{len(failures)} validation failure(s)")
        return 1

    print(f"OK 18 cases, {total_turns} turns, distribution {distribution}")
    print("OK oracle notes: exact key set, no digits, no case entities")
    print("OK images: both PNGs present, valid, and matching image_spec")
    return 0


if __name__ == "__main__":
    sys.exit(main())
