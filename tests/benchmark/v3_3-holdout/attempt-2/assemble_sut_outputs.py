#!/usr/bin/env python3
"""Assemble v3.3 attempt-2 SUT outputs from dedicated-branch copies. Do not merge those branches."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CLOUD = ROOT / "tests/benchmark/v3_3-holdout/attempt-2/cloud-cases"
RAW_DIR = CLOUD / "sut-raw"
ATT_DIR = CLOUD / "sut-attestations"
CANONICAL_PARENT = "1be627d7c82483e537791589d646582c46207e10"
HOLDOUT = "cursor/blind-v332-holdout-17a0"
GOLD_MANIFEST = CLOUD / "gold-manifest-v332.json"
INPUT_MANIFEST = CLOUD / "sut-input-manifest.json"
REQUESTED_MODEL = "inherit"
IMAGE_OPENS = {"V332-009", "V332-018"}

SOURCES = [
    ("V332-001", "bc-26360eda-9c18-53b3-8dfd-02aa3dbccebd", "cursor/v332-001-sut-17a0"),
    ("V332-002", "bc-d0ad2f0c-4f0b-5dbc-b184-9f1767dec196", "cursor/v332-002-sut-17a0"),
    ("V332-003", "bc-4a353ef9-3af0-5c91-bcc8-bf0cb18f44df", "cursor/v332-003-sut-17a0"),
    ("V332-004", "bc-449ab87e-33a7-5f64-b53f-a8fdc2f79493", "cursor/v332-004-sut-17a0"),
    ("V332-005", "bc-c09f4d73-2477-545e-a84d-d7360a2c0bd9", "cursor/v332-005-sut-17a0"),
    ("V332-006", "bc-660b0ddc-a33a-575b-bd8e-19f541b1e0ea", "cursor/v332-006-sut-17a0"),
    ("V332-007", "bc-2943695f-6356-5a76-82df-c8ce0952eba2", "cursor/v332-007-sut-17a0"),
    ("V332-008", "bc-47783ee1-ff71-53ff-8292-422c341b7f23", "cursor/v332-008-sut-17a0"),
    ("V332-009", "bc-400cfc7e-717d-5aca-8bae-9348b7f5f75d", "cursor/v332-009-sut-17a0"),
    ("V332-010", "bc-375c6128-d790-5836-96f8-7573ecad627c", "cursor/v332-010-sut-17a0"),
    ("V332-011", "bc-022740b3-60a1-5ceb-a1be-e98685d85a15", "cursor/v332-011-sut-17a0"),
    ("V332-012", "bc-df0b26b4-4930-56b8-9a34-6a92d77da9ef", "cursor/v332-012-sut-17a0"),
    ("V332-013", "bc-1d83a396-7821-5e94-8348-526e90edf62c", "cursor/v332-013-sut-17a0"),
    ("V332-014", "bc-05af00d7-1b2d-5c2e-8df8-1a3f9d9e874b", "cursor/v332-014-sut-17a0"),
    ("V332-015", "bc-67bb36a1-69c9-56ed-b555-203b342cea87", "cursor/v332-015-sut-17a0"),
    ("V332-016", "bc-c9de4a18-1b6e-503f-b578-f9001c3567ef", "cursor/v332-016-sut-17a0"),
    ("V332-017", "bc-e86de63f-3f86-5ce2-813c-4f405f59a06b", "cursor/v332-017-sut-17a0"),
    ("V332-018", "bc-2156fe7d-e89d-5eef-8b72-f227b32302a4", "cursor/v332-018-sut-17a0"),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    inputs = json.loads(INPUT_MANIFEST.read_text(encoding="utf-8"))
    input_by_id = {item["case_id"]: item for item in inputs["cases"]}
    if digest(GOLD_MANIFEST) != inputs["parent_gold_manifest"]["sha256"]:
        raise ValueError("gold manifest hash drifted")

    tips = {}
    for wave in range(1, 7):
        copy_path = CLOUD / f"sut-copy-wave{wave}.json"
        copy = json.loads(copy_path.read_text(encoding="utf-8"))
        for item in copy["cases"]:
            tips[item["case_id"]] = item["source_commit"]

    index_cases = []
    aggregate_cases = []
    turn_total = 0
    for case_id, context_id, branch in SOURCES:
        raw_rel = f"tests/benchmark/v3_3-holdout/attempt-2/cloud-cases/sut-raw/{case_id}.json"
        att_rel = f"tests/benchmark/v3_3-holdout/attempt-2/cloud-cases/sut-attestations/{case_id}.json"
        raw_path = ROOT / raw_rel
        att_path = ROOT / att_rel
        raw_bytes = raw_path.read_bytes()
        att_bytes = att_path.read_bytes()
        raw_sha = hashlib.sha256(raw_bytes).hexdigest()
        att_sha = hashlib.sha256(att_bytes).hexdigest()
        raw = json.loads(raw_bytes)
        turns = raw["turns"]
        expected_turns = input_by_id[case_id]["turns"]
        if raw["case_id"] != case_id or len(turns) != expected_turns:
            raise ValueError(f"{case_id} turn coverage")
        if [turn["turn_index"] for turn in turns] != list(range(1, expected_turns + 1)):
            raise ValueError(f"{case_id} turn order")
        for turn in turns:
            if not isinstance(turn.get("output_raw"), str) or not turn["output_raw"].strip():
                raise ValueError(f"{case_id} empty output")
        att = json.loads(att_bytes)
        if att.get("gold_accessed") or att.get("other_cases_accessed") or att.get(
            "question_design_accessed"
        ):
            raise ValueError(f"{case_id} isolation")
        if att.get("skill_files_accessed") is not True:
            raise ValueError(f"{case_id} skill access")
        png_read = any(
            str(item.get("path", "")).endswith(".png") for item in att.get("files_read", [])
        )
        image_opened = case_id in IMAGE_OPENS
        if png_read != image_opened:
            raise ValueError(f"{case_id} image-open attestation")
        tip = tips[case_id]
        turn_total += len(turns)
        index_cases.append(
            {
                "case_id": case_id,
                "context_id": context_id,
                "source_branch": branch,
                "delivery": "dedicated",
                "raw_commit": tip,
                "attestation_commit": tip,
                "raw_source_path": raw_rel,
                "attestation_source_path": att_rel,
                "source_raw_sha256": raw_sha,
                "source_attestation_sha256": att_sha,
                "canonical_raw_path": raw_rel,
                "canonical_attestation_path": att_rel,
                "canonical_raw_sha256": raw_sha,
                "canonical_attestation_sha256": att_sha,
                "markdown_wrapped": False,
            }
        )
        aggregate_cases.append(
            {
                "case_id": case_id,
                "generator_context_id": context_id,
                "requested_model_id": REQUESTED_MODEL,
                "machine_model_id": "unverified",
                "runtime_commit": inputs["runtime_commit"],
                "input": {
                    "path": input_by_id[case_id]["path"],
                    "sha256": input_by_id[case_id]["sha256"],
                },
                "source": {
                    "raw_path": raw_rel,
                    "raw_sha256": raw_sha,
                    "attestation_path": att_rel,
                    "attestation_sha256": att_sha,
                    "branch": branch,
                    "output_commit": tip,
                    "raw_commit": tip,
                    "delivery": "dedicated",
                    "markdown_wrapped": False,
                    "source_raw_sha256": raw_sha,
                    "source_attestation_sha256": att_sha,
                },
                "audit": {
                    "verdict": "PASS",
                    "procedural_deviations": [],
                    "prohibited_content_access": False,
                    "image_opened_directly": image_opened,
                },
                "turn_outputs": [
                    {
                        "turn_index": turn["turn_index"],
                        "raw_output": turn["output_raw"],
                        "source_json_pointer": f"/turns/{index}/output_raw",
                    }
                    for index, turn in enumerate(turns)
                ],
            }
        )

    if turn_total != 24:
        raise ValueError(f"turn total {turn_total}")
    if len({case["generator_context_id"] for case in aggregate_cases}) != 18:
        raise ValueError("SUT contexts are not distinct")

    index = {
        "schema_version": "v3.3",
        "artifact": "sut-source-index",
        "canonical_parent_commit": CANONICAL_PARENT,
        "canonical_parent_role": "prepare-sut-inputs; gold freeze parent",
        "holdout_branch": HOLDOUT,
        "merged": False,
        "method": "git show",
        "cases": index_cases,
    }
    (CLOUD / "sut-source-index.json").write_text(json.dumps(index, indent=2) + "\n")
    aggregate = {
        "schema_version": "v3.3",
        "artifact": "sut-raw-outputs",
        "parent_gold_manifest": inputs["parent_gold_manifest"],
        "canonical_parent_commit": CANONICAL_PARENT,
        "runtime": {
            "runtime_commit": inputs["runtime_commit"],
            "runtime_sources": inputs["runtime_sources"],
        },
        "requested_model_id": REQUESTED_MODEL,
        "machine_model_id": "unverified",
        "counts": {"cases": 18, "turns": 24},
        "cases": aggregate_cases,
    }
    (CLOUD / "outputs-v332-raw.json").write_text(
        json.dumps(aggregate, indent=2) + "\n", encoding="utf-8"
    )
    audits = {
        "schema_version": "v3.3",
        "artifact": "sut-protocol-audits",
        "distinct_cloud_contexts": 18,
        "shared_holdout_delivery": 0,
        "direct_image_opens": sorted(IMAGE_OPENS),
        "prohibited_gold_or_other_case_access": 0,
        "cases": [
            {
                "case_id": case_id,
                "context_id": context_id,
                "verdict": "PASS",
            }
            for case_id, context_id, _ in SOURCES
        ],
    }
    (CLOUD / "sut-protocol-audits.json").write_text(json.dumps(audits, indent=2) + "\n")
    print("assembled 18 dedicated SUT contexts, 24 turns")


if __name__ == "__main__":
    main()
