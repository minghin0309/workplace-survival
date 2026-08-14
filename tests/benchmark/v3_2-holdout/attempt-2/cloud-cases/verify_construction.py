#!/usr/bin/env python3
"""Construction-gate checks for the attempt-2 holdout. Hashes PNG bytes only; never opens them as images."""

from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FORBIDDEN_IN_SUT = [
    "AW_TAPE_SUB_AUTH",
    "AW_RIP_PANEL_DATE",
    "AW_GORE_BOOK_OWNER",
    "AW_RN7741_SOURCE",
    "AW_TW519_GORE_LENGTH",
    "AW_TW512_DECISION_CARD",
    "answer_fixture",
    "Joss Pellane",
    "COA-RN-7741",
    "42.6",
    "2 September 2026",
    "recut collar",
    "hold for the certificate holder",
    "PLACEHOLDER_SHA256",
]
MANAGER_FORBIDDEN = [
    "not a manager",
    "non-manager",
    "non manager",
    "not the sender's manager",
]


def png_chunk_types(data: bytes) -> list[str]:
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    types = []
    offset = 8
    while offset < len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        tag = data[offset + 4 : offset + 8].decode("ascii")
        types.append(tag)
        offset = offset + 12 + length
        if tag == "IEND":
            break
    return types


def main() -> None:
    cases_obj = json.loads((ROOT / "cases.json").read_text())
    oracle = json.loads((ROOT / "oracle-notes.json").read_text())
    qdesign = json.loads((ROOT / "question-design.json").read_text())
    errors: list[str] = []

    if cases_obj["case_count"] != 18:
        errors.append("case_count field mismatch")
    if cases_obj["turn_count"] != 24:
        errors.append("turn_count field mismatch")
    if len(cases_obj["cases"]) != 18:
        errors.append("cases array length")

    turns = 0
    three_turn = []
    for case in cases_obj["cases"]:
        cid = case["case_id"]
        n = len(case["turns"])
        turns += n
        if n == 3:
            three_turn.append(cid)
        rc = case["recipient_context"]
        if cid == "V322-017":
            if rc["relationship_to_user"] == "direct line manager":
                errors.append("V322-017 must not be a manager recipient")
            if rc["audience_scope"] == "manager only":
                errors.append("V322-017 audience_scope must not be manager only")
            if "manager" in rc["recipient_role"].lower():
                errors.append("V322-017 recipient_role contains manager")
        else:
            if rc["relationship_to_user"] != "direct line manager":
                errors.append(f"{cid} relationship")
            if rc["audience_scope"] != "manager only":
                errors.append(f"{cid} audience_scope")
            if rc["additional_recipients"] != []:
                errors.append(f"{cid} additional_recipients")
            role = rc["recipient_role"]
            if "manager" not in role.lower():
                errors.append(f"{cid} recipient_role missing manager")
            low = role.lower()
            for phrase in MANAGER_FORBIDDEN:
                if phrase in low:
                    errors.append(f"{cid} forbidden role phrase {phrase}")
        for i, turn in enumerate(case["turns"], start=1):
            if turn["turn_index"] != i:
                errors.append(f"{cid} turn_index {turn['turn_index']}")
            if (turn["image_path"] is None) != (turn["image_spec"] is None):
                errors.append(f"{cid} image fields mismatch")
            if turn["image_path"] is None and turn["draft_message"] is None:
                errors.append(f"{cid} empty draft")
            if turn["image_path"] is not None and turn["draft_message"] is not None:
                errors.append(f"{cid} both draft and image")
            if turn["image_spec"] is not None:
                spec = turn["image_spec"]
                path = ROOT / turn["image_path"]
                data = path.read_bytes()
                digest = hashlib.sha256(data).hexdigest()
                if digest != spec["sha256"]:
                    errors.append(f"{cid} sha256 mismatch")
                chunks = png_chunk_types(data)
                if "tIME" in chunks:
                    errors.append(f"{cid} tIME chunk")
                for needle in FORBIDDEN_IN_SUT:
                    if needle.encode("utf-8") in data:
                        errors.append(f"{cid} forbidden ascii in png bytes: {needle}")

    if turns != 24:
        errors.append(f"turn total {turns}")
    if three_turn != ["V322-014", "V322-015", "V322-016"]:
        errors.append(f"three-turn set {three_turn}")

    cases_text = (ROOT / "cases.json").read_text()
    oracle_text = (ROOT / "oracle-notes.json").read_text()
    for needle in FORBIDDEN_IN_SUT:
        if needle in cases_text:
            errors.append(f"cases.json contains {needle}")
        if needle in oracle_text:
            errors.append(f"oracle-notes.json contains {needle}")

    cand_ids = [c["case_id"] for c in qdesign["candidates"]]
    if cand_ids != [f"V322-00{i}" for i in range(4, 10)]:
        errors.append(f"candidate ids {cand_ids}")
    concepts = [c["primary_concept"] for c in qdesign["candidates"]]
    expected = [
        "approval-authority",
        "confirmed-deadline",
        "intended-recipient",
        "traceable-source",
        "material-measurement",
        "required-decision-option",
    ]
    if concepts != expected:
        errors.append(f"concepts {concepts}")
    for cand in qdesign["candidates"]:
        muts = [m["mutation"] for m in cand["mutations"]]
        if muts != ["REMOVE_DEPENDENCY", "SUPPLY_ANSWER", "ADD_DOMINANT_RED"]:
            errors.append(f"{cand['case_id']} mutations {muts}")
        if "base_state" not in cand:
            errors.append(f"{cand['case_id']} missing base_state")
        for m in cand["mutations"]:
            if "resulting_state" not in m:
                errors.append(f"{cand['case_id']} missing resulting_state")

    note_ids = [n["case_id"] for n in oracle["notes"]]
    if note_ids != [f"V322-{i:03d}" for i in range(1, 19)]:
        errors.append(f"oracle ids {note_ids}")

    if errors:
        raise SystemExit("\n".join(errors))
    print("construction gates ok")
    print("cases.json", hashlib.sha256(cases_text.encode()).hexdigest())
    print(
        "question-design.json",
        hashlib.sha256((ROOT / "question-design.json").read_bytes()).hexdigest(),
    )
    print(
        "oracle-notes.json",
        hashlib.sha256((ROOT / "oracle-notes.json").read_bytes()).hexdigest(),
    )


if __name__ == "__main__":
    main()
