#!/usr/bin/env python3
"""Validator for the v3.1 unseen holdout.

Construction tooling. Reads only the artifacts in this holdout directory and the
sole permitted repository input, the v3.1 case brief, whose hash it reports.

Checks: envelope schema and counts, turn ordering, image bytes and image
determinism, absence of construction metadata and of candidate answers from the
SUT-visible envelope, the question-candidate contract, and the mutation state
transitions.
"""

import hashlib
import json
import pathlib
import re
import struct
import sys

import render_images

HERE = pathlib.Path(__file__).resolve().parent
CASES_DIR = HERE.parent
REPO_ROOT = CASES_DIR.parents[3]
BRIEF = REPO_ROOT / "tests/benchmark/v3_1/V3_1_CASE_BRIEF.md"

EXPECTED_IDS = [f"V31-{n:03d}" for n in range(1, 19)]
MULTI_TURN_IDS = {"V31-014", "V31-015", "V31-016"}
CANDIDATE_IDS = [f"V31-{n:03d}" for n in range(4, 10)]
BRIEF_CONCEPTS = {
    "approval-authority",
    "confirmed-deadline",
    "intended-recipient",
    "traceable-source",
    "material-measurement",
    "required-decision-option",
}
MUTATION_STATES = ["REMOVE_DEPENDENCY", "SUPPLY_ANSWER", "ADD_DOMINANT_RED"]

CONSTRUCTION_VOCABULARY = [
    "missing_concept",
    "dependency_present",
    "answer_absent",
    "placeholder_safe",
    "qualification_safe",
    "omission_safe",
    "direct_red_defects",
    "answer_fixture",
    "safe_completion",
    "question_unnecessary",
    "remove_dependency",
    "supply_answer",
    "add_dominant_red",
    "question candidate",
    "question-candidate",
    "mutation",
    "predicate",
    "expected label",
    "green control",
    "responsibility boundary",
    "tone boundary",
    "recipient-scope",
    "prompt injection",
    "oracle",
    "rubric",
    "ontology",
    "scorer",
]

LABEL_VOCABULARY = [
    "green",
    "amber",
    "red",
    "verdict",
    "expected outcome",
    "expected label",
    "must ask",
    "should ask",
    "question required",
    "unsafe",
    "violation",
    "correct answer",
]

TURN_KEYS = {"turn_index", "turn_id", "user_message", "draft", "draft_source", "image_path", "image_spec"}
RECIPIENT_KEYS = {
    "recipient_name",
    "recipient_role",
    "relationship_to_sender",
    "channel",
    "audience_scope",
    "stated_requirements",
}
DATA_A_KEYS = {"sender", "situation", "known_facts", "constraints"}
QD_REQUIRED = {
    "dependency_present": True,
    "answer_absent": True,
    "placeholder_safe": False,
    "qualification_safe": False,
    "omission_safe": False,
    "safe_completion_enabled_by_answer": True,
    "question_unnecessary_without_dependency": True,
}

failures = []
checks = []


def check(condition, label, detail=""):
    checks.append(label)
    if not condition:
        failures.append(f"{label}: {detail}" if detail else label)
    return bool(condition)


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name):
    return json.loads((CASES_DIR / name).read_text(encoding="utf-8"))


def png_geometry(payload):
    width, height, depth, color_type = struct.unpack(">IIBB", payload[16:26])
    return width, height, depth, color_type


def validate_cases(cases_doc, cases_text):
    cases = cases_doc["cases"]
    ids = [case["case_id"] for case in cases]
    check(ids == EXPECTED_IDS, "cases: exactly 18 ids V31-001..V31-018 in order", str(ids))
    check(len(set(ids)) == 18, "cases: ids unique")

    turn_total = 0
    for case in cases:
        cid = case["case_id"]
        check(set(case) == {"case_id", "recipient_context", "data_a", "turns"}, f"{cid}: case keys exact", str(sorted(case)))
        rc = case["recipient_context"]
        check(set(rc) == RECIPIENT_KEYS, f"{cid}: recipient_context keys exact", str(sorted(rc)))
        check(isinstance(rc["stated_requirements"], list) and rc["stated_requirements"],
              f"{cid}: recipient_context has explicit requirements")
        data_a = case["data_a"]
        check(set(data_a) == DATA_A_KEYS, f"{cid}: data_a keys exact", str(sorted(data_a)))
        check(set(data_a["sender"]) == {"name", "role", "team"}, f"{cid}: data_a.sender structured")
        check(isinstance(data_a["known_facts"], list) and len(data_a["known_facts"]) >= 4,
              f"{cid}: data_a.known_facts populated")

        turns = case["turns"]
        expected_turns = 3 if cid in MULTI_TURN_IDS else 1
        check(len(turns) == expected_turns, f"{cid}: turn count is {expected_turns}", str(len(turns)))
        turn_total += len(turns)
        for position, turn in enumerate(turns, start=1):
            tid = turn.get("turn_id")
            check(set(turn) == TURN_KEYS, f"{tid}: turn keys exact", str(sorted(turn)))
            check(turn["turn_index"] == position, f"{tid}: turn_index ordered", str(turn["turn_index"]))
            check(tid == f"{cid}-T{position}", f"{cid} turn {position}: turn_id well formed", str(tid))
            check(isinstance(turn["user_message"], str) and turn["user_message"].strip(),
                  f"{tid}: user_message present")
            source = turn["draft_source"]
            check(source in {"text", "image", "carried_from_previous_turn"}, f"{tid}: draft_source known", str(source))
            if source == "text":
                check(isinstance(turn["draft"], str) and turn["draft"].strip(), f"{tid}: text draft present")
                check(turn["image_path"] is None and turn["image_spec"] is None,
                      f"{tid}: non-image turn carries image_path null")
            elif source == "image":
                check(turn["draft"] is None, f"{tid}: image-only turn has null draft")
                check(isinstance(turn["image_path"], str) and isinstance(turn["image_spec"], dict),
                      f"{tid}: image turn has image_path and image_spec")
            else:
                check(turn["draft"] is None, f"{tid}: correction turn has null draft")
                check(turn["image_path"] is None and turn["image_spec"] is None,
                      f"{tid}: correction turn carries image_path null")
                check(position > 1, f"{tid}: correction turn is not the first turn")

    check(turn_total == 24, "cases: exactly 24 turns", str(turn_total))
    check(cases_doc["case_count"] == 18 and cases_doc["turn_count"] == 24, "cases: header counts agree")
    check(cases_text.isascii(), "cases: ascii-only payload")

    lowered = cases_text.lower()
    for token in CONSTRUCTION_VOCABULARY:
        check(token not in lowered, f"cases: no construction vocabulary '{token}'")
    return cases


def validate_images(cases):
    on_disk = sorted(p.name for p in (CASES_DIR / "images").glob("*.png"))
    referenced = []
    for case in cases:
        for turn in case["turns"]:
            if turn["draft_source"] != "image":
                continue
            spec = turn["image_spec"]
            path = CASES_DIR / turn["image_path"]
            referenced.append(path.name)
            if not check(path.is_file(), f"{turn['turn_id']}: image file exists", str(path)):
                continue
            payload = path.read_bytes()
            check(payload[:8] == b"\x89PNG\r\n\x1a\n", f"{path.name}: png signature")
            check(payload[-8:-4] == b"IEND", f"{path.name}: png terminated by IEND")
            width, height, depth, color_type = png_geometry(payload)
            check((width, height) == (spec["width"], spec["height"]),
                  f"{path.name}: pixel dimensions match image_spec", f"{width}x{height}")
            check(depth == 8 and color_type == 0, f"{path.name}: 8-bit grayscale as declared")
            check(len(payload) == spec["byte_length"], f"{path.name}: byte_length matches image_spec",
                  str(len(payload)))
            check(hashlib.sha256(payload).hexdigest() == spec["sha256"],
                  f"{path.name}: sha256 matches image_spec")
            for chunk in (b"tEXt", b"zTXt", b"iTXt", b"tIME"):
                check(chunk not in payload, f"{path.name}: no {chunk.decode()} chunk")
    check(sorted(referenced) == on_disk, "images: every stored PNG is referenced by a case",
          f"referenced={sorted(referenced)} on_disk={on_disk}")

    for name, builder in render_images.BENCHMARK_IMAGES:
        rebuilt = builder().to_png()
        stored = (CASES_DIR / "images" / name).read_bytes()
        check(rebuilt == stored, f"{name}: deterministic re-render is byte-identical")
    for name, builder in render_images.MUTATION_IMAGES:
        rebuilt = builder().to_png()
        stored = (HERE / "mutation-renders" / name).read_bytes()
        check(rebuilt == stored, f"{name}: deterministic re-render is byte-identical")


def validate_question_design(design, cases_text, notes_text):
    entries = design["entries"]
    ids = [entry["case_id"] for entry in entries]
    check(ids == CANDIDATE_IDS, "question-design: six candidates V31-004..V31-009", str(ids))
    concepts = [entry["missing_concept"] for entry in entries]
    check(len(set(concepts)) == 6, "question-design: six distinct primary concepts", str(concepts))
    check(set(concepts) == BRIEF_CONCEPTS, "question-design: concepts are the six from the brief", str(concepts))

    lowered_cases = cases_text.lower()
    lowered_notes = notes_text.lower()
    for entry in entries:
        cid = entry["case_id"]
        for key, expected in QD_REQUIRED.items():
            check(entry[key] is expected, f"{cid}: {key} is {expected}", str(entry.get(key)))
        check(entry["direct_red_defects"] == [], f"{cid}: no independent direct Red defect",
              str(entry["direct_red_defects"]))
        check(isinstance(entry["answer_fixture"], str) and len(entry["answer_fixture"]) > 20,
              f"{cid}: answer_fixture present")
        for field in ("dependency_locus", "why_not_placeholder", "why_not_qualification",
                      "why_not_omission", "single_unknown_check"):
            check(bool(entry.get(field)), f"{cid}: {field} recorded")
        tokens = entry["answer_tokens_forbidden_in_cases"]
        check(bool(tokens), f"{cid}: answer tokens listed for leak checking")
        for token in tokens:
            check(token.lower() not in lowered_cases, f"{cid}: answer token absent from cases.json", token)
            check(token.lower() not in lowered_notes, f"{cid}: answer token absent from oracle-notes.json", token)

    image_only = [entry["case_id"] for entry in entries if entry.get("image_only_draft")]
    check(len(image_only) >= 1, "question-design: at least one candidate uses an image-only draft", str(image_only))
    for cid in image_only:
        entry = next(e for e in entries if e["case_id"] == cid)
        check(bool(entry.get("image_unreadable_value")), f"{cid}: unreadable value recorded")
        check(bool(entry.get("image_background_justification")), f"{cid}: visible background justification recorded")
    return entries


def validate_mutations(mutations_doc, design_entries):
    entries = mutations_doc["entries"]
    ids = [entry["case_id"] for entry in entries]
    check(ids == CANDIDATE_IDS, "mutations: one entry per candidate", str(ids))
    concepts_by_id = {entry["case_id"]: entry["missing_concept"] for entry in design_entries}

    for entry in entries:
        cid = entry["case_id"]
        check(entry["missing_concept"] == concepts_by_id[cid], f"{cid}: mutation concept matches question-design")
        base = entry["baseline_predicates"]
        check(base["dependency_present"] is True and base["answer_absent"] is True
              and base["direct_red_defects"] == [] and base["clean_question_candidate"] is True
              and base["question_required"] is True, f"{cid}: baseline predicate vector is a clean candidate", str(base))
        states = [mutation["mutation"] for mutation in entry["mutations"]]
        check(states == MUTATION_STATES, f"{cid}: three mutation states in order", str(states))
        for mutation in entry["mutations"]:
            name = mutation["mutation"]
            mid = mutation["mutation_id"]
            check(mid == f"{cid}-{name}", f"{cid}: mutation_id well formed", str(mid))
            check(bool(mutation["patches"]), f"{mid}: patch recorded")
            for patch in mutation["patches"]:
                check(patch["operation"] in {"replace_list", "replace_index", "append_list_item",
                                             "append_to_draft", "replace_image"},
                      f"{mid}: patch operation known", patch["operation"])
                check(bool(patch["field_path"]), f"{mid}: patch field_path recorded")
            result = mutation["resulting_predicates"]
            check(bool(mutation.get("evidence")), f"{mid}: transition evidence recorded")
            if name == "REMOVE_DEPENDENCY":
                check(result["dependency_present"] is False, f"{mid}: dependency_present flips to false")
                check(result["answer_absent"] is True, f"{mid}: answer stays absent")
                check(result["direct_red_defects"] == [], f"{mid}: no Red defect introduced")
                check(result["question_required"] is False, f"{mid}: question becomes unnecessary")
            elif name == "SUPPLY_ANSWER":
                check(result["answer_absent"] is False, f"{mid}: answer_absent flips to false")
                check(result["dependency_present"] is True, f"{mid}: dependency retained")
                check(result["direct_red_defects"] == [], f"{mid}: no Red defect introduced")
                check(result["question_required"] is False, f"{mid}: safe completion without the question")
            else:
                check(result["direct_red_defects"] != [], f"{mid}: direct Red defect introduced")
                check(result["dependency_present"] is True and result["answer_absent"] is True,
                      f"{mid}: dependency and absence unchanged")
                check(result["clean_question_candidate"] is False, f"{mid}: rejected as a clean candidate")

        red = next(m for m in entry["mutations"] if m["mutation"] == "ADD_DOMINANT_RED")
        for patch in red["patches"]:
            if patch["operation"] != "replace_image":
                continue
            path = CASES_DIR / patch["value"]
            if check(path.is_file(), f"{cid}: mutation render exists", str(path)):
                payload = path.read_bytes()
                check(hashlib.sha256(payload).hexdigest() == patch["image_sha256"],
                      f"{cid}: mutation render sha256 matches")
                check(len(payload) == patch["image_byte_length"], f"{cid}: mutation render byte_length matches")
                check(not str(path).startswith(str(CASES_DIR / "images")),
                      f"{cid}: mutation render is outside the benchmark image set")


def validate_notes(notes_doc, cases):
    entries = notes_doc["cases"]
    ids = [entry["case_id"] for entry in entries]
    check(ids == EXPECTED_IDS, "oracle-notes: one entry per case in order", str(ids))
    turn_counts = {case["case_id"]: len(case["turns"]) for case in cases}
    for entry in entries:
        cid = entry["case_id"]
        check(entry["turn_count"] == turn_counts[cid], f"{cid}: note turn_count matches envelope")
        check(entry["facts_added_by_note"] is False, f"{cid}: note adds no case facts")
        blob = json.dumps(entry).lower()
        for token in LABEL_VOCABULARY:
            check(not re.search(rf"\b{re.escape(token)}\b", blob),
                  f"{cid}: note free of label vocabulary '{token}'")


def validate_attestation(brief_sha):
    path = CASES_DIR / "designer-attestation.json"
    if not path.is_file():
        return
    doc = json.loads(path.read_text(encoding="utf-8"))
    sole = doc["sole_repository_input"]
    check(sole["path"] == "tests/benchmark/v3_1/V3_1_CASE_BRIEF.md",
          "attestation: records the brief as the sole repository input", sole["path"])
    check(sole["sha256"] == brief_sha, "attestation: brief sha256 matches the file on disk", sole["sha256"])
    check(bool(doc["branch"]), "attestation: branch recorded")
    check(bool(doc["output_commit"]["sha"]), "attestation: output commit recorded")
    check(bool(doc["limitations_and_unverified_claims"]), "attestation: limitations recorded")
    check(bool(doc["isolation"]), "attestation: isolation recorded")
    for entry in doc["output_hashes"]:
        target = CASES_DIR / entry["path"]
        if check(target.is_file(), f"attestation: {entry['path']} exists"):
            check(sha256_file(target) == entry["sha256"], f"attestation: {entry['path']} sha256 matches")
            check(target.stat().st_size == entry["byte_length"], f"attestation: {entry['path']} byte_length matches")


def manifest_files():
    for path in sorted(CASES_DIR.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            yield path


def main():
    cases_text = (CASES_DIR / "cases.json").read_text(encoding="utf-8")
    notes_text = (CASES_DIR / "oracle-notes.json").read_text(encoding="utf-8")
    cases_doc = json.loads(cases_text)
    notes_doc = json.loads(notes_text)
    design = load("question-design.json")
    mutations_doc = load("construction-mutations.json")

    cases = validate_cases(cases_doc, cases_text)
    validate_images(cases)
    design_entries = validate_question_design(design, cases_text, notes_text)
    validate_mutations(mutations_doc, design_entries)
    validate_notes(notes_doc, cases)
    brief_sha = sha256_file(BRIEF)
    validate_attestation(brief_sha)

    print("sole permitted repository input")
    print(f"  {BRIEF.relative_to(REPO_ROOT)} sha256={brief_sha}")
    print("artifact hashes")
    for path in manifest_files():
        print(f"  {path.relative_to(CASES_DIR)} {path.stat().st_size} bytes sha256={sha256_file(path)}")
    print(f"checks run: {len(checks)}")
    if failures:
        print(f"FAILURES: {len(failures)}")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("result: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
