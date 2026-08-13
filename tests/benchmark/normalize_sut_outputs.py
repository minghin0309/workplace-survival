import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLOUD = ROOT / "tests/benchmark/v2-holdout/cloud-cases"
INPUT_MANIFEST = CLOUD / "sut-input-manifest.json"
AUDITS_PATH = CLOUD / "sut-protocol-audits.json"
OUTPUT_PATH = CLOUD / "outputs-v2-raw.json"
ATTESTATION_PATH = CLOUD / "generator-attestation-v2.json"
SOURCE_SNAPSHOT_COMMIT = "8592fbb666df929bc38a59f735c6fb68bfb10f81"
REQUESTED_MODEL_ID = "gpt-5.6-sol-high-fast"

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


def locate(case_id: str, directory: str) -> Path:
    candidates = [
        CLOUD / directory / f"{case_id}.json",
        ROOT / directory / f"{case_id}.json",
    ]
    matches = [path for path in candidates if path.is_file()]
    if len(matches) != 1:
        raise ValueError(f"{case_id}: expected one {directory} source, got {matches}")
    return matches[0]


def extract_turns(raw: dict, input_document: dict) -> list[dict]:
    source_turns = None
    container_name = None
    for name in CONTAINERS:
        if isinstance(raw.get(name), list):
            source_turns = raw[name]
            container_name = name
            break

    extracted = []
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
                raise ValueError(f"{raw['case_id']}: raw turn output missing")
            timestamp = next(
                (turn[key] for key in TIMESTAMP_KEYS if turn.get(key) is not None),
                None,
            )
            if timestamp is None:
                timestamp = first_value(
                    raw,
                    (
                        ("generated_at_utc",),
                        ("timestamp_utc",),
                        ("timestamp",),
                        ("timestamps", "completed_at"),
                    ),
                )
            extracted.append(
                {
                    "turn_index": turn.get("turn_index", position),
                    "executed_at_utc": timestamp,
                    "raw_output": turn[output_key],
                    "source_json_pointer": f"/{container_name}/{position - 1}/{output_key}",
                }
            )
    else:
        output_key = next(
            (key for key in RAW_KEYS if isinstance(raw.get(key), str) and raw[key]),
            None,
        )
        if output_key is None:
            raise ValueError(f"{raw['case_id']}: top-level raw output missing")
        extracted.append(
            {
                "turn_index": 1,
                "executed_at_utc": first_value(
                    raw,
                    (
                        ("generated_at_utc",),
                        ("timestamp_utc",),
                        ("timestamp",),
                    ),
                ),
                "raw_output": raw[output_key],
                "source_json_pointer": f"/{output_key}",
            }
        )

    expected_turns = input_document["turns"]
    if [turn["turn_index"] for turn in extracted] != [
        turn["turn_index"] for turn in expected_turns
    ]:
        raise ValueError(f"{raw['case_id']}: turn coverage")
    return extracted


def source_branch(attestation: dict) -> str:
    value = first_value(
        attestation,
        (
            ("cloud_branch",),
            ("branch",),
            ("git", "working_branch"),
            ("git", "output_branch"),
            ("execution", "output_branch"),
            ("execution", "branch"),
            ("context", "branch"),
            ("context", "working_branch"),
            ("git", "branch"),
            ("base_branch",),
        ),
    )
    if not isinstance(value, str) or not value:
        raise ValueError("source branch missing")
    return value


def source_commit(attestation: dict) -> str:
    value = first_value(
        attestation,
        (
            ("cloud_commit",),
            ("output_commit",),
            ("git", "output_commit"),
            ("git", "raw_output_commit"),
            ("execution", "output_commit"),
            ("output", "commit"),
            ("context", "output_commit"),
        ),
    )
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{40}", value) is None:
        raise ValueError(f"source output commit missing: {value}")
    return value


def main() -> None:
    input_manifest = json.loads(INPUT_MANIFEST.read_text(encoding="utf-8"))
    input_entries = {item["case_id"]: item for item in input_manifest["cases"]}
    audits = json.loads(AUDITS_PATH.read_text(encoding="utf-8"))
    audit_entries = {item["case_id"]: item for item in audits["cases"]}
    case_ids = [f"V2-{index:03d}" for index in range(1, 19)]
    if set(input_entries) != set(case_ids) or set(audit_entries) != set(case_ids):
        raise ValueError("input or audit case coverage")

    cases = []
    source_reads = [INPUT_MANIFEST, AUDITS_PATH]
    for case_id in case_ids:
        raw_path = locate(case_id, "sut-raw")
        attestation_path = locate(case_id, "sut-attestations")
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
        attestation = json.loads(attestation_path.read_text(encoding="utf-8"))
        input_entry = input_entries[case_id]
        input_path = ROOT / input_entry["path"]
        if digest(input_path) != input_entry["sha256"]:
            raise ValueError(f"{case_id}: input changed")
        input_document = json.loads(input_path.read_text(encoding="utf-8"))
        if raw.get("case_id") != case_id or attestation.get("case_id") != case_id:
            raise ValueError(f"{case_id}: source identity")
        audit = audit_entries[case_id]
        if audit["prohibited_content_access"] is not False:
            raise ValueError(f"{case_id}: prohibited content access")

        cases.append(
            {
                "case_id": case_id,
                "generator_context_id": audit["context_id"],
                "requested_model_id": REQUESTED_MODEL_ID,
                "machine_model_id": "unverified",
                "runtime_commit": input_manifest["runtime"]["runtime_commit"],
                "input": {
                    "path": input_entry["path"],
                    "sha256": input_entry["sha256"],
                },
                "source": {
                    "raw_path": relative(raw_path),
                    "raw_sha256": digest(raw_path),
                    "attestation_path": relative(attestation_path),
                    "attestation_sha256": digest(attestation_path),
                    "branch": source_branch(attestation),
                    "output_commit": source_commit(attestation),
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
        "schema_version": "v2",
        "artifact": "sut-raw-outputs",
        "parent_gold_manifest": input_manifest["parent_gold_manifest"],
        "runtime": input_manifest["runtime"],
        "requested_model_id": REQUESTED_MODEL_ID,
        "machine_model_id": "unverified",
        "counts": {"cases": len(cases), "turns": sum(len(c["turn_outputs"]) for c in cases)},
        "cases": cases,
    }
    OUTPUT_PATH.write_text(json.dumps(aggregate, indent=2) + "\n", encoding="utf-8")

    source_reads = list(dict.fromkeys(source_reads))
    generator_attestation = {
        "schema_version": "v2",
        "role": "generator",
        "context_id": "18-distinct-isolated-cloud-contexts",
        "source_context_ids": [case["generator_context_id"] for case in cases],
        "model_id": "unverified",
        "model_family": "gpt",
        "cloud_branch": "cursor/blind-v2-holdout-17a0",
        "cloud_commit": SOURCE_SNAPSHOT_COMMIT,
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
        },
        "limitations": audits["limitations"]
        + [
            "Raw per-case schemas were heterogeneous; canonical aggregation preserves each raw Skill response string exactly and records its source JSON pointer.",
            "Procedural and metadata deviations are preserved per case and did not expose prohibited benchmark content.",
        ],
    }
    ATTESTATION_PATH.write_text(
        json.dumps(generator_attestation, indent=2) + "\n", encoding="utf-8"
    )
    print(f"normalized {len(cases)} isolated SUT cases and {aggregate['counts']['turns']} turns")


if __name__ == "__main__":
    main()
