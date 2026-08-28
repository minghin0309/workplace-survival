#!/usr/bin/env python3
"""Assemble v3.3 attempt-4 SUT outputs from dedicated-branch copies. Do not merge those branches."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CLOUD = ROOT / "tests/benchmark/v3_3-holdout/attempt-4/cloud-cases"
RAW_DIR = CLOUD / "sut-raw"
ATT_DIR = CLOUD / "sut-attestations"
CANONICAL_PARENT = "571e5492332978a25dcec847798bcc2c29bd6316"
HOLDOUT = "cursor/blind-v334-holdout-17a0"
GOLD_MANIFEST = CLOUD / "gold-manifest-v334.json"
INPUT_MANIFEST = CLOUD / "sut-input-manifest.json"
REQUESTED_MODEL = "inherit"
IMAGE_OPENS = {"V334-009", "V334-018"}

# Fill context_id after isolated SUT copy. Shared placeholder keeps
# distinct-context assembly failing until real bc- ids are written.
SOURCES = [
    ("V334-001", "bc-7f6f43e4-8244-50ab-8b09-4b62a5d7f071", "cursor/v334-001-sut-17a0"),
    ("V334-002", "bc-dfc036f2-16f3-5753-8c1b-f0f8417af256", "cursor/v334-002-sut-17a0"),
    ("V334-003", "bc-1ef0f2ca-99dc-58c9-a31b-7523f2902550", "cursor/v334-003-sut-17a0"),
    ("V334-004", "bc-d5c7067c-77ef-5f3e-948b-b09b67556333", "cursor/v334-004-sut-17a0"),
    ("V334-005", "bc-d89c8122-d38e-51d9-9068-02f54e95b8d3", "cursor/v334-005-sut-17a0"),
    ("V334-006", "bc-d0539f69-a312-50ab-a355-355775b56605", "cursor/v334-006-sut-17a0"),
    ("V334-007", "bc-03f09aa3-72b3-5a5d-8baf-40bb30e331fa", "cursor/v334-007-sut-17a0"),
    ("V334-008", "bc-e5c50344-1bb3-5285-9dd2-1ea9beb54c76", "cursor/v334-008-sut-17a0"),
    ("V334-009", "bc-8d964f87-d971-542d-8e75-aa5e1ee59f3e", "cursor/v334-009-sut-17a0"),
    ("V334-010", "bc-f89345bc-3535-5cef-8a82-80c45f32893d", "cursor/v334-010-sut-17a0"),
    ("V334-011", "bc-5d2cb333-bfff-57d1-981e-11795e19c3e0", "cursor/v334-011-sut-17a0"),
    ("V334-012", "bc-cfbaa733-e6dd-58e3-8424-beb4c819f7a0", "cursor/v334-012-sut-17a0"),
    ("V334-013", "bc-656a2acc-86ff-54e6-aad5-22e31306c107", "cursor/v334-013-sut-17a0"),
    ("V334-014", "bc-b59fe7a9-9533-5516-bb3a-00ec147cb7fe", "cursor/v334-014-sut-17a0"),
    ("V334-015", "bc-7fcce57a-c1ec-5580-8a98-7f2c5b2360cb", "cursor/v334-015-sut-17a0"),
    ("V334-016", "bc-a075588a-3999-5d54-b597-53d21e7dd19e", "cursor/v334-016-sut-17a0"),
    ("V334-017", "bc-ebdc959f-bc26-5099-9ac1-858ed14702f3", "cursor/v334-017-sut-17a0"),
    ("V334-018", "bc-c645680a-bfed-58f4-af7e-9a631213f751", "cursor/v334-018-sut-17a0"),
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
        raw_rel = f"tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/sut-raw/{case_id}.json"
        att_rel = f"tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/sut-attestations/{case_id}.json"
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
    (CLOUD / "outputs-v334-raw.json").write_text(
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
