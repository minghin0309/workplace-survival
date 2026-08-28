#!/usr/bin/env python3
"""Build gold-blind extractor-visible outputs from the frozen attempt-4 SUT aggregate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CLOUD = ROOT / "tests/benchmark/v3_3-holdout/attempt-4/cloud-cases"
OUTPUTS = CLOUD / "outputs-v334-raw.json"
MANIFEST = CLOUD / "outputs-manifest-v334.json"
VISIBLE = CLOUD / "extractor-visible.json"
INPUT_MANIFEST = CLOUD / "sut-input-manifest.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if not MANIFEST.is_file():
        raise FileNotFoundError("SUT outputs must be frozen before extractor-visible")
    outputs = json.loads(OUTPUTS.read_text(encoding="utf-8"))
    inputs = json.loads(INPUT_MANIFEST.read_text(encoding="utf-8"))
    input_entries = {item["case_id"]: item for item in inputs["cases"]}
    if outputs["artifact"] != "sut-raw-outputs":
        raise ValueError("source is not frozen SUT outputs")
    cases = []
    for case in outputs["cases"]:
        case_id = case["case_id"]
        entry = input_entries[case_id]
        cases.append(
            {
                "case_id": case_id,
                "input": {"path": entry["path"], "sha256": entry["sha256"]},
                "turns": [
                    {
                        "turn_index": turn["turn_index"],
                        "raw_output": turn["raw_output"],
                    }
                    for turn in case["turn_outputs"]
                ],
            }
        )
    document = {
        "schema_version": "v3.3",
        "artifact": "extractor-visible",
        "parent_outputs_manifest": {
            "path": "tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/outputs-manifest-v334.json",
            "sha256": digest(MANIFEST),
        },
        "source_outputs": {
            "path": "tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/outputs-v334-raw.json",
            "sha256": digest(OUTPUTS),
        },
        "counts": outputs["counts"],
        "cases": cases,
    }
    VISIBLE.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"wrote extractor-visible.json sha256={digest(VISIBLE)}")


if __name__ == "__main__":
    main()
