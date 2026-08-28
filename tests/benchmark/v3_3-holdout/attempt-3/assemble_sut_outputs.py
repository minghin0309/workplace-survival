#!/usr/bin/env python3
"""Assemble v3.3 attempt-3 SUT outputs from dedicated-branch copies. Do not merge those branches."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CLOUD = ROOT / "tests/benchmark/v3_3-holdout/attempt-3/cloud-cases"
RAW_DIR = CLOUD / "sut-raw"
ATT_DIR = CLOUD / "sut-attestations"
CANONICAL_PARENT = "98dbf74b2998b51387f6ea203b5ff878788c2a54"
HOLDOUT = "cursor/blind-v333-holdout-17a0"
GOLD_MANIFEST = CLOUD / "gold-manifest-v333.json"
INPUT_MANIFEST = CLOUD / "sut-input-manifest.json"
REQUESTED_MODEL = "inherit"
IMAGE_OPENS = {"V333-009", "V333-018"}

# Fill context_id after isolated SUT copy. Shared placeholder keeps
# distinct-context assembly failing until real bc- ids are written.
SOURCES = [
    ("V333-001", "bc-6b4f2c89-585a-5227-b608-e807123328e8", "cursor/v333-001-sut-17a0"),
    ("V333-002", "bc-8bd0aa6d-b7f7-5985-b054-2b6a77bc37b1", "cursor/v333-002-sut-17a0"),
    ("V333-003", "bc-efbfd8e8-bc83-539c-8857-2107d35b8bf8", "cursor/v333-003-sut-17a0"),
    ("V333-004", "bc-afef334f-f227-5002-830a-51cb5b6515b9", "cursor/v333-004-sut-17a0"),
    ("V333-005", "bc-fa8301cd-23c8-5b2b-bc2d-056244b3afb0", "cursor/v333-005-sut-17a0"),
    ("V333-006", "bc-200b68ff-b0e7-5bd4-a695-93ddd2183a76", "cursor/v333-006-sut-17a0"),
    ("V333-007", "bc-d204ab5d-e17c-51d5-95da-bfef6acd5864", "cursor/v333-007-sut-17a0"),
    ("V333-008", "bc-fb41388e-3e33-5efe-ad33-76d882448450", "cursor/v333-008-sut-17a0"),
    ("V333-009", "bc-bed461eb-f327-55b4-b48b-a7afdba50730", "cursor/v333-009-sut-17a0"),
    ("V333-010", "bc-47e162df-7f2a-5aea-b4c9-7259ca57360f", "cursor/v333-010-sut-17a0"),
    ("V333-011", "bc-2355f2bc-7bec-5404-b8ca-eb25797fa41c", "cursor/v333-011-sut-17a0"),
    ("V333-012", "bc-0d8ecd6f-0a17-54bb-b4b1-cf4660420452", "cursor/v333-012-sut-17a0"),
    ("V333-013", "bc-c0449c62-1ad4-5a4f-8779-1c9fcdca1ac4", "cursor/v333-013-sut-17a0"),
    ("V333-014", "bc-e5040126-4690-52ad-a26b-253dc5b92984", "cursor/v333-014-sut-17a0"),
    ("V333-015", "bc-23483466-ffd2-527b-afc4-3c475940599e", "cursor/v333-015-sut-17a0"),
    ("V333-016", "bc-5d1bdadd-fe81-53ff-8914-981fbdfe2681", "cursor/v333-016-sut-17a0"),
    ("V333-017", "bc-7d779d74-2a4c-51e7-8f2e-e357c699e899", "cursor/v333-017-sut-17a0"),
    ("V333-018", "bc-32ea4d6e-419d-51ef-b9d0-b6e7a6cb1750", "cursor/v333-018-sut-17a0"),
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
        raw_rel = f"tests/benchmark/v3_3-holdout/attempt-3/cloud-cases/sut-raw/{case_id}.json"
        att_rel = f"tests/benchmark/v3_3-holdout/attempt-3/cloud-cases/sut-attestations/{case_id}.json"
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
    (CLOUD / "outputs-v333-raw.json").write_text(
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
