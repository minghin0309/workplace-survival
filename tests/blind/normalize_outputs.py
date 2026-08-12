import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from blind_common import case_input_text, context_transcript_text, digest_text


RAW_CASE_KEYS = {"case_id", "turns"}
RAW_TURN_KEYS = {"turn_index", "executed_at_utc", "raw_output", "image_artifacts"}
IMAGE_KEYS = {"path", "sha256", "opened_with_image_reader"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def parse_time(value: str) -> datetime:
    require(isinstance(value, str) and value.endswith("Z"), "UTC timestamp required")
    return datetime.fromisoformat(value[:-1] + "+00:00")


def main() -> None:
    if len(sys.argv) != 7:
        raise SystemExit(
            "usage: normalize_outputs.py <freeze.json> <cases.json> <raw-dir> "
            "<contexts.json> <runtime-dir> <outputs.json>"
        )
    freeze_path, cases_path, raw_dir, contexts_path, runtime_dir, output_path = (
        Path(value).resolve() for value in sys.argv[1:]
    )
    require(not output_path.exists(), "refusing to overwrite normalized outputs")
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    protected = freeze["protected_files"]
    require(
        hashlib.sha256(cases_path.read_bytes()).hexdigest() == protected["cases"]["sha256"],
        "cases changed after holdout freeze",
    )
    contexts = json.loads(contexts_path.read_text(encoding="utf-8"))
    require(set(contexts) == {case["case_id"] for case in cases}, "context coverage")
    require(
        len(set(contexts.values())) == len(cases)
        and all(isinstance(value, str) and value for value in contexts.values()),
        "generator contexts not unique or valid",
    )
    frozen_at = parse_time(freeze["frozen_at_utc"])
    normalized_at = datetime.now(timezone.utc)

    normalized_cases = []
    for case in cases:
        case_id = case["case_id"]
        raw_path = raw_dir / f"{case_id}.json"
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
        require(set(raw) == RAW_CASE_KEYS and raw["case_id"] == case_id, f"{case_id}: raw schema")
        require(len(raw["turns"]) == len(case["turns"]), f"{case_id}: raw turn count")
        turns = []
        previous_at = None
        for expected_index, (case_turn, raw_turn) in enumerate(
            zip(case["turns"], raw["turns"]),
            start=1,
        ):
            require(set(raw_turn) == RAW_TURN_KEYS, f"{case_id}: raw turn schema")
            require(raw_turn["turn_index"] == expected_index, f"{case_id}: turn order")
            executed_at = parse_time(raw_turn["executed_at_utc"])
            require(executed_at >= frozen_at, f"{case_id}: output predates holdout freeze")
            require(executed_at <= normalized_at, f"{case_id}: output timestamp is in the future")
            require(previous_at is None or executed_at >= previous_at, f"{case_id}: turn chronology")
            previous_at = executed_at
            require(
                isinstance(raw_turn["raw_output"], str) and raw_turn["raw_output"],
                f"{case_id}: raw output",
            )
            artifacts = raw_turn["image_artifacts"]
            require(isinstance(artifacts, list), f"{case_id}: image artifacts")
            if case_turn["image_path"] is None:
                require(artifacts == [], f"{case_id}: unexpected image")
            else:
                require(len(artifacts) == 1 and set(artifacts[0]) == IMAGE_KEYS, f"{case_id}: image schema")
                artifact = artifacts[0]
                image_path = (cases_path.parent / artifact["path"]).resolve()
                require(artifact["path"] == case_turn["image_path"], f"{case_id}: image path")
                require(image_path.is_file(), f"{case_id}: image missing")
                require(
                    artifact["sha256"] == hashlib.sha256(image_path.read_bytes()).hexdigest(),
                    f"{case_id}: image hash",
                )
                require(
                    artifact["sha256"]
                    == protected[f"image:{Path(artifact['path']).name}"]["sha256"],
                    f"{case_id}: image changed after holdout freeze",
                )
                require(artifact["opened_with_image_reader"] is True, f"{case_id}: image not opened")

            turns.append(
                {
                    "turn_index": expected_index,
                    "executed_at_utc": raw_turn["executed_at_utc"],
                    "input_sha256": digest_text(case_turn["input_raw"]),
                    "case_input_sha256": digest_text(case_input_text(case, case_turn)),
                    "context_transcript_sha256": digest_text(
                        context_transcript_text(case, raw["turns"], expected_index)
                    ),
                    "raw_output": raw_turn["raw_output"],
                    "raw_output_sha256": digest_text(raw_turn["raw_output"]),
                    "image_artifacts": artifacts,
                }
            )
        normalized_cases.append(
            {
                "case_id": case_id,
                "generator_context_id": contexts[case_id],
                "turn_outputs": turns,
            }
        )

    runtime_entries = list(runtime_dir.iterdir())
    require(
        all(path.is_file() and not path.is_symlink() for path in runtime_entries),
        "runtime-only directory contains non-file or symlink",
    )
    runtime_files = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in runtime_entries
    }
    expected_runtime = {
        Path(item["path"]).name: item["sha256"] for item in freeze["runtime_sources"]
    }
    require(runtime_files == expected_runtime, "runtime-only directory mismatch")
    document = {
        "freeze_manifest_sha256": hashlib.sha256(freeze_path.read_bytes()).hexdigest(),
        "runtime_commit": freeze["runtime_commit"],
        "runtime_sources": freeze["runtime_sources"],
        "runtime_directory": str(runtime_dir),
        "generator_model": {
            "model_id": "inherit",
            "model_family": "gpt",
            "display_name": "GPT-5.6 Sol",
            "gold_access": False,
            "filesystem_access_audit_available": False,
            "limitation": "Separate prompt-restricted contexts; no filesystem access log was available.",
        },
        "cases": normalized_cases,
    }
    output_path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"normalized {len(normalized_cases)} cases")


if __name__ == "__main__":
    main()
