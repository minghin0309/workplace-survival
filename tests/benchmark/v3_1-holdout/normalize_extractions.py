#!/usr/bin/env python3
"""Normalize v3.1 extractor/evaluator attestations into canonical wrappers."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CLOUD = ROOT / "tests/benchmark/v3_1-holdout/cloud-cases"
CANONICAL = CLOUD / "extraction-attestations"

SOURCES = {
    "extractor-1": {
        "path": "extractor-1-attestation.json",
        "context_id": "bc-d8bcdf8c-3937-5830-847c-cb085ded528e",
        "model_family": "claude",
        "cloud_branch": "cursor/v31-extractor-claude-17a0",
        "cloud_commit": "553ee9846bb09a40f44e5a6ea205cea56d9dedee",
    },
    "extractor-2": {
        "path": "extractor-2-attestation.json",
        "context_id": "bc-407b6129-b25d-5064-9d64-5523806bbeb3",
        "model_family": "gemini",
        "cloud_branch": "cursor/v31-extractor-gemini-17a0",
        "cloud_commit": "ae5871023e7e3ddc0fd444fa9f66bd4196973767",
    },
    "evaluator": {
        "path": "evaluator-attestation-v31.json",
        "context_id": "bc-f001181e-4ec6-5746-aaad-b4bd3ba288e3",
        "model_family": "gpt",
        "cloud_branch": "cursor/v31-extractor-adjudicator-17a0",
        "cloud_commit": "94c1d4bde49cb9a3ff02a17da15b34372fe873eb",
    },
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def source_limitations(source: dict) -> list[str]:
    values = source.get("limitations", [])
    if isinstance(values, str):
        values = [values]
    if not isinstance(values, list):
        values = [str(values)]
    return [
        str(item)
        for item in values
        if str(item) and str(item).strip().lower() != "none"
    ]


def files_read(source: dict) -> list[dict]:
    values = source.get("files_read", [])
    normalized = []
    for item in values:
        if isinstance(item, str):
            path = ROOT / item
            normalized.append({"path": item, "sha256": digest(path)})
        else:
            normalized.append(item)
    return normalized


def write_wrapper(role: str, config: dict) -> Path:
    source_path = CLOUD / config["path"]
    source = json.loads(source_path.read_text(encoding="utf-8"))
    output_path = CANONICAL / f"{role}.json"
    document = {
        "schema_version": "v3.1",
        "role": role,
        "context_id": config["context_id"],
        "model_id": "unverified",
        "model_family": config["model_family"],
        "cloud_branch": config["cloud_branch"],
        "cloud_commit": config["cloud_commit"],
        "files_read": files_read(source),
        "limitations": source_limitations(source)
        + [
            "Machine model ID was unavailable from cloud run metadata; no ID was guessed.",
            "Transcript audit disposition is recorded in extraction-protocol-audits.json.",
        ],
        "source_attestation": {
            "path": relative(source_path),
            "sha256": digest(source_path),
        },
        "normalization": {
            "kind": "mechanical-provenance-wrapper",
            "extraction_decisions_changed": False,
        },
    }
    output_path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    return output_path


def main() -> None:
    CANONICAL.mkdir(parents=True, exist_ok=True)
    wrappers = {role: write_wrapper(role, config) for role, config in SOURCES.items()}
    raw_path = CLOUD / "evaluations-v31.json"
    canonical_path = CLOUD / "evaluations-v31-canonical.json"
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    canonical = deepcopy(raw)
    raw_cases = json.dumps(raw["cases"], sort_keys=True)
    canonical["evaluation_quality"]["extractors"] = [
        {
            "context_id": SOURCES[role]["context_id"],
            "model_id": "unverified",
            "model_family": SOURCES[role]["model_family"],
            "attestation_path": relative(wrappers[role]),
            "attestation_sha256": digest(wrappers[role]),
        }
        for role in ("extractor-1", "extractor-2")
    ]
    canonical["evaluation_quality"]["adjudicator"] = {
        "context_id": SOURCES["evaluator"]["context_id"],
        "model_id": "unverified",
        "model_family": "gpt",
    }
    if json.dumps(canonical["cases"], sort_keys=True) != raw_cases:
        raise RuntimeError("normalization changed evaluation decisions")
    canonical_path.write_text(json.dumps(canonical, indent=2) + "\n", encoding="utf-8")
    print("normalized two extractor attestations and evaluator provenance")


if __name__ == "__main__":
    main()
