#!/usr/bin/env python3
"""Validate canonical v3.1 SUT outputs, isolation, and non-merge of shared delivery."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tests/benchmark/v3_1-holdout"))

import extract_sut_artifacts as extractor
import normalize_sut_outputs as normalizer


CLOUD = ROOT / "tests/benchmark/v3_1-holdout/cloud-cases"
AGGREGATE_PATH = CLOUD / "outputs-v31-raw.json"
ATTESTATION_PATH = CLOUD / "generator-attestation-v31.json"
INPUT_MANIFEST_PATH = CLOUD / "sut-input-manifest.json"
AUDITS_PATH = CLOUD / "sut-protocol-audits.json"
INDEX_PATH = CLOUD / "sut-source-index.json"
DELIVERY_PATH = CLOUD / "sut-delivery-log.json"
MANIFEST_PATH = CLOUD / "outputs-manifest-v31.json"
IMAGE_CASES = {"V31-008", "V31-018"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_is_ancestor(ancestor: str, descendant: str) -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=ROOT,
    )
    return result.returncode == 0


def git_show(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def main() -> None:
    require(
        git_is_ancestor(extractor.CANONICAL_PARENT, "HEAD"),
        "canonical parent missing from HEAD",
    )
    require(
        not git_is_ancestor(extractor.DELIVERY_TIP, "HEAD")
        or subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
        == extractor.CANONICAL_PARENT,
        "shared delivery tip is an ancestor of HEAD; freeze parent would be contaminated",
    )
    require(
        subprocess.check_output(
            ["git", "rev-parse", extractor.DELIVERY_BRANCH], cwd=ROOT, text=True
        ).strip()
        == extractor.DELIVERY_TIP,
        "delivery-log ref moved",
    )

    aggregate = json.loads(AGGREGATE_PATH.read_text(encoding="utf-8"))
    attestation = json.loads(ATTESTATION_PATH.read_text(encoding="utf-8"))
    input_manifest = json.loads(INPUT_MANIFEST_PATH.read_text(encoding="utf-8"))
    audits = json.loads(AUDITS_PATH.read_text(encoding="utf-8"))
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    delivery = json.loads(DELIVERY_PATH.read_text(encoding="utf-8"))
    input_entries = {item["case_id"]: item for item in input_manifest["cases"]}
    audit_entries = {item["case_id"]: item for item in audits["cases"]}
    index_entries = {item["case_id"]: item for item in index["cases"]}

    require(
        aggregate["schema_version"] == "v3.1"
        and aggregate["artifact"] == "sut-raw-outputs"
        and aggregate["requested_model_id"] == normalizer.REQUESTED_MODEL_ID
        and aggregate["machine_model_id"] == "unverified"
        and aggregate["canonical_parent_commit"] == extractor.CANONICAL_PARENT
        and aggregate["shared_delivery"]["not_canonical_parent"] is True
        and aggregate["shared_delivery"]["tip"] == extractor.DELIVERY_TIP,
        "aggregate identity",
    )
    parent = aggregate["parent_gold_manifest"]
    parent_path = ROOT / parent["path"]
    require(
        parent_path.is_file()
        and digest(parent_path) == parent["sha256"]
        and parent == input_manifest["parent_gold_manifest"]
        and parent["sha256"]
        == "2aea483242418bdf73a56b0fdb921a718d4ea54c66611a8eae8d7bf7cf8e0377",
        "gold parent linkage",
    )
    runtime = aggregate["runtime"]
    require(
        runtime
        == {
            "runtime_commit": input_manifest["runtime_commit"],
            "runtime_sources": input_manifest["runtime_sources"],
        },
        "runtime manifest linkage",
    )
    for source in runtime["runtime_sources"]:
        path = ROOT / source["path"]
        require(
            path.is_file() and digest(path) == source["sha256"],
            f"runtime source changed: {path}",
        )

    require(
        delivery["not_canonical_parent"] is True
        and delivery["tip"] == extractor.DELIVERY_TIP
        and len(delivery["commits"]) == 7
        and delivery["cases_delivered_on_shared_holdout"]
        == ["V31-003", "V31-011", "V31-016", "V31-017", "V31-018"],
        "delivery log",
    )

    cases = aggregate["cases"]
    require(
        aggregate["counts"] == {"cases": 18, "turns": 24}
        and [case["case_id"] for case in cases]
        == [f"V31-{n:03d}" for n in range(1, 19)],
        "aggregate coverage",
    )
    context_ids = set()
    source_paths = set()
    total_turns = 0
    for case in cases:
        case_id = case["case_id"]
        require(
            case["generator_context_id"] not in context_ids
            and case["generator_context_id"] == audit_entries[case_id]["context_id"]
            and case["generator_context_id"] == index_entries[case_id]["context_id"],
            f"{case_id}: isolated context",
        )
        context_ids.add(case["generator_context_id"])
        require(
            case["requested_model_id"] == normalizer.REQUESTED_MODEL_ID
            and case["machine_model_id"] == "unverified"
            and case["runtime_commit"] == runtime["runtime_commit"],
            f"{case_id}: canonical runtime/model provenance",
        )
        input_entry = input_entries[case_id]
        require(
            case["input"]
            == {"path": input_entry["path"], "sha256": input_entry["sha256"]},
            f"{case_id}: input linkage",
        )
        source = case["source"]
        require(
            re.fullmatch(r"[0-9a-f]{40}", source["output_commit"]) is not None
            and source["output_commit"] == index_entries[case_id]["attestation_commit"],
            f"{case_id}: output commit",
        )
        raw_path = ROOT / source["raw_path"]
        attestation_path = ROOT / source["attestation_path"]
        require(
            digest(raw_path) == source["raw_sha256"]
            and digest(attestation_path) == source["attestation_sha256"],
            f"{case_id}: canonical hashes",
        )
        require(
            raw_path not in source_paths and attestation_path not in source_paths,
            f"{case_id}: duplicate source artifact",
        )
        source_paths.update((raw_path, attestation_path))

        original_raw = git_show(
            index_entries[case_id]["raw_commit"],
            index_entries[case_id]["raw_source_path"],
        )
        original_att = git_show(
            index_entries[case_id]["attestation_commit"],
            index_entries[case_id]["attestation_source_path"],
        )
        require(
            hashlib.sha256(original_raw).hexdigest()
            == index_entries[case_id]["source_raw_sha256"]
            and hashlib.sha256(original_att).hexdigest()
            == index_entries[case_id]["source_attestation_sha256"],
            f"{case_id}: source commit bytes drifted",
        )
        if index_entries[case_id]["markdown_wrapped"]:
            wrapped = json.loads(raw_path.read_text(encoding="utf-8"))
            require(
                wrapped["raw_skill_output"] == original_raw.decode("utf-8"),
                f"{case_id}: markdown wrap mutated Skill text",
            )
        else:
            require(raw_path.read_bytes() == original_raw, f"{case_id}: JSON bytes changed")
        require(
            attestation_path.read_bytes() == original_att,
            f"{case_id}: attestation bytes changed",
        )

        audit = case["audit"]
        require(
            audit["prohibited_content_access"] is False
            and audit["verdict"] == audit_entries[case_id]["verdict"]
            and audit["procedural_deviations"]
            == audit_entries[case_id]["procedural_deviations"]
            and audit["image_opened_directly"] == (case_id in IMAGE_CASES),
            f"{case_id}: audit linkage",
        )
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
        input_document = json.loads((ROOT / input_entry["path"]).read_text(encoding="utf-8"))
        expected_turns = normalizer.extract_turns(raw, input_document)
        require(case["turn_outputs"] == expected_turns, f"{case_id}: raw output preservation")
        total_turns += len(expected_turns)

    require(len(context_ids) == 18 and total_turns == 24, "context or turn total")
    require(
        all(item["prohibited_content_access"] is False for item in audits["cases"]),
        "prohibited content audit failure",
    )
    require(
        attestation["schema_version"] == "v3.1"
        and attestation["role"] == "generator"
        and attestation["model_id"] == "unverified"
        and set(attestation["source_context_ids"]) == context_ids
        and attestation["isolation"]["distinct_contexts"] == 18
        and attestation["isolation"]["prohibited_content_access_cases"] == 0
        and attestation["isolation"]["semantic_extraction_performed"] is False
        and attestation["isolation"]["scoring_performed"] is False
        and attestation["isolation"]["shared_delivery_merged"] is False
        and attestation["cloud_commit"] == extractor.CANONICAL_PARENT,
        "aggregate attestation identity",
    )
    for item in attestation["files_read"]:
        path = ROOT / item["path"]
        require(
            path.is_file()
            and digest(path) == item["sha256"]
            and all(
                token not in Path(item["path"]).name
                for token in ("gold-v31", "oracle-notes", "score-report")
            ),
            f"aggregate source read: {path}",
        )
    require(
        attestation["output"]
        == {
            "path": normalizer.relative(AGGREGATE_PATH),
            "sha256": digest(AGGREGATE_PATH),
        }
        and attestation["source_attestation"]
        == {
            "path": normalizer.relative(AUDITS_PATH),
            "sha256": digest(AUDITS_PATH),
        },
        "aggregate output or audit hash",
    )

    if MANIFEST_PATH.is_file():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        require(
            manifest["version"] == "3.1"
            and manifest["stage"] == "outputs"
            and manifest["immutable"] is True
            and manifest["parent_manifest"] == parent
            and manifest["canonical_parent_commit"] == extractor.CANONICAL_PARENT
            and manifest["shared_delivery"]["not_canonical_parent"] is True,
            "outputs manifest identity",
        )
        hashed = {item["role"]: item for item in manifest["artifacts"]}
        require(
            hashed["outputs"]["sha256"] == digest(AGGREGATE_PATH)
            and hashed["protocol-audits"]["sha256"] == digest(AUDITS_PATH),
            "outputs manifest hashes",
        )
        print("validated 18 isolated SUT contexts, 24 preserved raw outputs, and freeze manifest")
    else:
        print("validated 18 isolated SUT contexts and 24 preserved raw outputs (pre-freeze)")


if __name__ == "__main__":
    main()
