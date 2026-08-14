#!/usr/bin/env python3
"""Normalize heterogeneous v3.1 SUT raw outputs into one canonical aggregate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CLOUD = ROOT / "tests/benchmark/v3_1-holdout/cloud-cases"
INPUT_MANIFEST = CLOUD / "sut-input-manifest.json"
AUDITS_PATH = CLOUD / "sut-protocol-audits.json"
INDEX_PATH = CLOUD / "sut-source-index.json"
OUTPUT_PATH = CLOUD / "outputs-v31-raw.json"
ATTESTATION_PATH = CLOUD / "generator-attestation-v31.json"
REQUESTED_MODEL_ID = "gpt-5.6-sol-high-fast"
HOLDOUT_BRANCH = "cursor/blind-v31-holdout-17a0"

CONTAINERS = ("turn_outputs", "turns", "responses", "outputs")
RAW_KEYS = (
    "raw_skill_output",
    "raw_output",
    "response_raw",
    "output_raw",
    "assistant_response",
    "response",
    "raw_response",
    "output",
)
TIMESTAMP_KEYS = (
    "executed_at_utc",
    "timestamp_utc",
    "generated_at_utc",
    "timestamp",
    "completed_at",
    "started_at",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def nested(document: dict, *path: str):
    value = document
    for key in path:
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def first_value(document: dict, paths: tuple[tuple[str, ...], ...]):
    for path in paths:
        value = nested(document, *path)
        if value not in (None, ""):
            return value
    return None


def unwrap_raw(raw: dict, case_id: str) -> dict:
    cases = raw.get("cases")
    if isinstance(cases, list) and len(cases) == 1 and isinstance(cases[0], dict):
        inner = cases[0]
        if inner.get("case_id") != case_id:
            raise ValueError(f"{case_id}: nested case_id")
        return inner
    return raw


def extract_turns(raw: dict, input_document: dict) -> list[dict]:
    case_id = input_document["case_id"]
    body = unwrap_raw(raw, case_id)
    extracted = []
    if isinstance(body.get("raw_skill_output"), str) and body["raw_skill_output"]:
        extracted.append(
            {
                "turn_index": 1,
                "executed_at_utc": first_value(
                    body,
                    (("generated_at_utc",), ("timestamp_utc",), ("timestamp",)),
                ),
                "raw_output": body["raw_skill_output"],
                "source_json_pointer": "/raw_skill_output",
            }
        )
    else:
        source_turns = None
        container_name = None
        for name in CONTAINERS:
            if isinstance(body.get(name), list):
                source_turns = body[name]
                container_name = name
                break
        if source_turns is not None:
            for position, turn in enumerate(source_turns, start=1):
                output_key = next(
                    (
                        key
                        for key in RAW_KEYS
                        if isinstance(turn.get(key), str) and turn[key]
                    ),
                    None,
                )
                if output_key is None:
                    raise ValueError(f"{case_id}: raw turn output missing")
                timestamp = next(
                    (turn[key] for key in TIMESTAMP_KEYS if turn.get(key) is not None),
                    None,
                )
                if timestamp is None:
                    timestamp = first_value(
                        body,
                        (
                            ("generated_at_utc",),
                            ("timestamp_utc",),
                            ("timestamp",),
                            ("timestamps", "completed_at"),
                        ),
                    )
                pointer_prefix = (
                    f"/cases/0/{container_name}"
                    if body is not raw
                    else f"/{container_name}"
                )
                extracted.append(
                    {
                        "turn_index": turn.get("turn_index", position),
                        "executed_at_utc": timestamp,
                        "raw_output": turn[output_key],
                        "source_json_pointer": f"{pointer_prefix}/{position - 1}/{output_key}",
                    }
                )
        else:
            output_key = next(
                (
                    key
                    for key in RAW_KEYS
                    if isinstance(body.get(key), str) and body[key]
                ),
                None,
            )
            if output_key is None:
                raise ValueError(f"{case_id}: top-level raw output missing")
            extracted.append(
                {
                    "turn_index": 1,
                    "executed_at_utc": first_value(
                        body,
                        (
                            ("generated_at_utc",),
                            ("timestamp_utc",),
                            ("timestamp",),
                        ),
                    ),
                    "raw_output": body[output_key],
                    "source_json_pointer": (
                        f"/cases/0/{output_key}" if body is not raw else f"/{output_key}"
                    ),
                }
            )

    expected_turns = input_document["turns"]
    if [turn["turn_index"] for turn in extracted] != [
        turn["turn_index"] for turn in expected_turns
    ]:
        raise ValueError(f"{case_id}: turn coverage")
    if any(not turn["raw_output"].strip() for turn in extracted):
        raise ValueError(f"{case_id}: empty Skill output")
    return extracted


def runtime_from_inputs(input_manifest: dict) -> dict:
    return {
        "runtime_commit": input_manifest["runtime_commit"],
        "runtime_sources": input_manifest["runtime_sources"],
    }


def main() -> None:
    input_manifest = json.loads(INPUT_MANIFEST.read_text(encoding="utf-8"))
    audits = json.loads(AUDITS_PATH.read_text(encoding="utf-8"))
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    input_entries = {item["case_id"]: item for item in input_manifest["cases"]}
    audit_entries = {item["case_id"]: item for item in audits["cases"]}
    index_entries = {item["case_id"]: item for item in index["cases"]}
    case_ids = [f"V31-{n:03d}" for n in range(1, 19)]
    if set(input_entries) != set(case_ids) or set(audit_entries) != set(case_ids):
        raise ValueError("input or audit case coverage")
    if list(index_entries) != case_ids:
        raise ValueError("source-index case order")

    runtime = runtime_from_inputs(input_manifest)
    cases = []
    source_reads = [INPUT_MANIFEST, AUDITS_PATH, INDEX_PATH, CLOUD / "sut-delivery-log.json"]
    for case_id in case_ids:
        source = index_entries[case_id]
        raw_path = ROOT / source["canonical_raw_path"]
        attestation_path = ROOT / source["canonical_attestation_path"]
        if digest(raw_path) != source["canonical_raw_sha256"]:
            raise ValueError(f"{case_id}: canonical raw changed")
        if digest(attestation_path) != source["canonical_attestation_sha256"]:
            raise ValueError(f"{case_id}: canonical attestation changed")
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
        attestation = json.loads(attestation_path.read_text(encoding="utf-8"))
        if attestation.get("case_id") != case_id:
            raise ValueError(f"{case_id}: attestation identity")
        input_entry = input_entries[case_id]
        input_path = ROOT / input_entry["path"]
        if digest(input_path) != input_entry["sha256"]:
            raise ValueError(f"{case_id}: input changed")
        input_document = json.loads(input_path.read_text(encoding="utf-8"))
        audit = audit_entries[case_id]
        if audit["prohibited_content_access"] is not False:
            raise ValueError(f"{case_id}: prohibited content access")
        if audit["context_id"] != source["context_id"]:
            raise ValueError(f"{case_id}: context mismatch")

        cases.append(
            {
                "case_id": case_id,
                "generator_context_id": audit["context_id"],
                "requested_model_id": REQUESTED_MODEL_ID,
                "machine_model_id": "unverified",
                "runtime_commit": runtime["runtime_commit"],
                "input": {
                    "path": input_entry["path"],
                    "sha256": input_entry["sha256"],
                },
                "source": {
                    "raw_path": source["canonical_raw_path"],
                    "raw_sha256": source["canonical_raw_sha256"],
                    "attestation_path": source["canonical_attestation_path"],
                    "attestation_sha256": source["canonical_attestation_sha256"],
                    "branch": source["source_branch"],
                    "output_commit": source["attestation_commit"],
                    "raw_commit": source["raw_commit"],
                    "delivery": source["delivery"],
                    "markdown_wrapped": source["markdown_wrapped"],
                    "source_raw_sha256": source["source_raw_sha256"],
                    "source_attestation_sha256": source["source_attestation_sha256"],
                },
                "audit": {
                    "verdict": audit["verdict"],
                    "procedural_deviations": audit["procedural_deviations"],
                    "prohibited_content_access": False,
                    "image_opened_directly": audit["image_opened_directly"],
                },
                "turn_outputs": extract_turns(raw, input_document),
            }
        )
        source_reads.extend((raw_path, attestation_path))

    aggregate = {
        "schema_version": "v3.1",
        "artifact": "sut-raw-outputs",
        "parent_gold_manifest": input_manifest["parent_gold_manifest"],
        "canonical_parent_commit": index["canonical_parent_commit"],
        "shared_delivery": index["shared_delivery"],
        "runtime": runtime,
        "requested_model_id": REQUESTED_MODEL_ID,
        "machine_model_id": "unverified",
        "counts": {
            "cases": len(cases),
            "turns": sum(len(case["turn_outputs"]) for case in cases),
        },
        "cases": cases,
    }
    OUTPUT_PATH.write_text(json.dumps(aggregate, indent=2) + "\n", encoding="utf-8")

    source_reads = list(dict.fromkeys(source_reads))
    generator_attestation = {
        "schema_version": "v3.1",
        "role": "generator",
        "context_id": "18-distinct-isolated-cloud-contexts",
        "source_context_ids": [case["generator_context_id"] for case in cases],
        "model_id": "unverified",
        "model_family": "gpt",
        "cloud_branch": HOLDOUT_BRANCH,
        "cloud_commit": index["canonical_parent_commit"],
        "files_read": [
            {"path": relative(path), "sha256": digest(path)} for path in source_reads
        ],
        "output": {"path": relative(OUTPUT_PATH), "sha256": digest(OUTPUT_PATH)},
        "source_attestation": {
            "path": relative(AUDITS_PATH),
            "sha256": digest(AUDITS_PATH),
        },
        "isolation": {
            "distinct_contexts": len({case["generator_context_id"] for case in cases}),
            "prohibited_content_access_cases": 0,
            "semantic_extraction_performed": False,
            "scoring_performed": False,
            "shared_delivery_merged": False,
        },
        "limitations": audits["limitations"]
        + [
            "Raw per-case schemas were heterogeneous; canonical aggregation preserves each raw Skill response string exactly and records its source JSON pointer.",
            "Markdown deliveries were wrapped without changing the Skill text. JSON deliveries were path-canonicalized without changing bytes.",
            "Shared-holdout commits remain on cursor/v31-sut-shared-delivery-17a0 and are not the freeze parent.",
        ],
    }
    ATTESTATION_PATH.write_text(
        json.dumps(generator_attestation, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"normalized {len(cases)} isolated SUT cases and {aggregate['counts']['turns']} turns"
    )


if __name__ == "__main__":
    main()
