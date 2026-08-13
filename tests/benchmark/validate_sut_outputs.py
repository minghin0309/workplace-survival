import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests/benchmark"))

import normalize_sut_outputs as normalizer
import validate_benchmark


CLOUD = ROOT / "tests/benchmark/v2-holdout/cloud-cases"
AGGREGATE_PATH = CLOUD / "outputs-v2-raw.json"
ATTESTATION_PATH = CLOUD / "generator-attestation-v2.json"
INPUT_MANIFEST_PATH = CLOUD / "sut-input-manifest.json"
AUDITS_PATH = CLOUD / "sut-protocol-audits.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    aggregate = json.loads(AGGREGATE_PATH.read_text(encoding="utf-8"))
    attestation = json.loads(ATTESTATION_PATH.read_text(encoding="utf-8"))
    input_manifest = json.loads(INPUT_MANIFEST_PATH.read_text(encoding="utf-8"))
    audits = json.loads(AUDITS_PATH.read_text(encoding="utf-8"))
    input_entries = {item["case_id"]: item for item in input_manifest["cases"]}
    audit_entries = {item["case_id"]: item for item in audits["cases"]}

    require(
        set(aggregate)
        == {
            "schema_version",
            "artifact",
            "parent_gold_manifest",
            "runtime",
            "requested_model_id",
            "machine_model_id",
            "counts",
            "cases",
        },
        "aggregate schema",
    )
    require(
        aggregate["schema_version"] == "v2"
        and aggregate["artifact"] == "sut-raw-outputs"
        and aggregate["requested_model_id"] == normalizer.REQUESTED_MODEL_ID
        and aggregate["machine_model_id"] == "unverified",
        "aggregate identity",
    )
    parent = aggregate["parent_gold_manifest"]
    parent_path = ROOT / parent["path"]
    require(
        parent_path.is_file()
        and normalizer.digest(parent_path) == parent["sha256"]
        and parent == input_manifest["parent_gold_manifest"],
        "gold parent linkage",
    )
    validate_benchmark.validate_not_invalidated(parent_path)
    validate_benchmark.validate_manifest(
        json.loads(parent_path.read_text(encoding="utf-8"))
    )

    runtime = aggregate["runtime"]
    require(runtime == input_manifest["runtime"], "runtime manifest linkage")
    for source in runtime["runtime_sources"]:
        path = ROOT / source["path"]
        require(
            path.is_file() and normalizer.digest(path) == source["sha256"],
            f"runtime source changed: {path}",
        )

    cases = aggregate["cases"]
    require(
        aggregate["counts"] == {"cases": 18, "turns": 24}
        and [case["case_id"] for case in cases]
        == [f"V2-{index:03d}" for index in range(1, 19)],
        "aggregate coverage",
    )
    context_ids = set()
    source_paths = set()
    total_turns = 0
    for case in cases:
        case_id = case["case_id"]
        require(
            set(case)
            == {
                "case_id",
                "generator_context_id",
                "requested_model_id",
                "machine_model_id",
                "runtime_commit",
                "input",
                "source",
                "audit",
                "turn_outputs",
            },
            f"{case_id}: case schema",
        )
        require(
            case["generator_context_id"] not in context_ids
            and case["generator_context_id"] == audit_entries[case_id]["context_id"],
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
        input_path = ROOT / input_entry["path"]
        require(normalizer.digest(input_path) == input_entry["sha256"], f"{case_id}: input hash")

        source = case["source"]
        require(
            re.fullmatch(r"[0-9a-f]{40}", source["output_commit"]) is not None,
            f"{case_id}: output commit",
        )
        raw_path = ROOT / source["raw_path"]
        source_attestation_path = ROOT / source["attestation_path"]
        require(
            raw_path.is_file()
            and source_attestation_path.is_file()
            and normalizer.digest(raw_path) == source["raw_sha256"]
            and normalizer.digest(source_attestation_path)
            == source["attestation_sha256"],
            f"{case_id}: source hashes",
        )
        require(
            raw_path not in source_paths and source_attestation_path not in source_paths,
            f"{case_id}: duplicate source artifact",
        )
        source_paths.update((raw_path, source_attestation_path))

        audit = case["audit"]
        require(
            audit["prohibited_content_access"] is False
            and audit["verdict"] == audit_entries[case_id]["verdict"]
            and audit["procedural_deviations"]
            == audit_entries[case_id]["procedural_deviations"],
            f"{case_id}: audit linkage",
        )
        require(
            audit["image_opened_directly"]
            == (case_id in {"V2-017", "V2-018"}),
            f"{case_id}: image audit",
        )

        raw = json.loads(raw_path.read_text(encoding="utf-8"))
        input_document = json.loads(input_path.read_text(encoding="utf-8"))
        expected_turns = normalizer.extract_turns(raw, input_document)
        require(case["turn_outputs"] == expected_turns, f"{case_id}: raw output preservation")
        total_turns += len(expected_turns)
    require(len(context_ids) == 18 and total_turns == 24, "context or turn total")

    require(
        all(item["prohibited_content_access"] is False for item in audits["cases"]),
        "prohibited content audit failure",
    )
    require(
        set(attestation)
        == {
            "schema_version",
            "role",
            "context_id",
            "source_context_ids",
            "model_id",
            "model_family",
            "cloud_branch",
            "cloud_commit",
            "files_read",
            "output",
            "source_attestation",
            "isolation",
            "limitations",
        },
        "aggregate attestation schema",
    )
    require(
        attestation["schema_version"] == "v2"
        and attestation["role"] == "generator"
        and attestation["model_id"] == "unverified"
        and set(attestation["source_context_ids"]) == context_ids
        and attestation["isolation"]["distinct_contexts"] == 18
        and attestation["isolation"]["prohibited_content_access_cases"] == 0
        and attestation["isolation"]["semantic_extraction_performed"] is False
        and attestation["isolation"]["scoring_performed"] is False,
        "aggregate attestation identity",
    )
    for item in attestation["files_read"]:
        path = ROOT / item["path"]
        require(
            path.is_file()
            and normalizer.digest(path) == item["sha256"]
            and all(token not in item["path"] for token in ("gold", "oracle-notes", "score")),
            f"aggregate source read: {path}",
        )
    require(
        attestation["output"]
        == {
            "path": normalizer.relative(AGGREGATE_PATH),
            "sha256": normalizer.digest(AGGREGATE_PATH),
        }
        and attestation["source_attestation"]
        == {
            "path": normalizer.relative(AUDITS_PATH),
            "sha256": normalizer.digest(AUDITS_PATH),
        },
        "aggregate output or audit hash",
    )
    print("validated 18 isolated SUT contexts and 24 preserved raw outputs")


if __name__ == "__main__":
    main()
