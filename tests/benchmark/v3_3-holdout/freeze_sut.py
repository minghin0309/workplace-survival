#!/usr/bin/env python3
"""Freeze v3.3 attempt-1 SUT outputs against the gold manifest. Dedicated branches are not merged."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CLOUD = ROOT / "tests/benchmark/v3_3-holdout/cloud-cases"
MANIFEST = CLOUD / "outputs-manifest-v33.json"
PARENT = CLOUD / "gold-manifest-v33.json"
BRANCH = "cursor/blind-v33-holdout-17a0"
CANONICAL_PARENT = "249806bf5093d698265b5113b73d549a81633a5a"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def commit(path: Path) -> str:
    value = subprocess.run(
        ["git", "log", "-1", "--format=%H", "--", str(path.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if len(value) != 40:
        raise ValueError(path)
    return value


def entry(role: str, path: Path) -> dict:
    return {
        "role": role,
        "path": str(path.relative_to(ROOT)),
        "sha256": digest(path),
        "cloud_branch": BRANCH,
        "cloud_commit": commit(path),
    }


def main() -> None:
    if MANIFEST.exists():
        raise FileExistsError("refusing to overwrite v3.3 attempt-1 SUT output manifest")
    aggregate = json.loads((CLOUD / "outputs-v33-raw.json").read_text(encoding="utf-8"))
    parent_hash = digest(PARENT)
    if aggregate["parent_gold_manifest"] != {
        "path": str(PARENT.relative_to(ROOT)),
        "sha256": parent_hash,
    }:
        raise ValueError("aggregate parent is not the frozen gold manifest")
    if aggregate["canonical_parent_commit"] != CANONICAL_PARENT:
        raise ValueError("aggregate canonical parent drifted")
    if aggregate["counts"] != {"cases": 18, "turns": 24}:
        raise ValueError("aggregate coverage")
    contexts = {case["generator_context_id"] for case in aggregate["cases"]}
    if len(contexts) != 18:
        raise ValueError("SUT contexts are not distinct")
    paths = [
        ("outputs", CLOUD / "outputs-v33-raw.json"),
        ("sut-input-manifest", CLOUD / "sut-input-manifest.json"),
        ("protocol-audits", CLOUD / "sut-protocol-audits.json"),
        ("source-index", CLOUD / "sut-source-index.json"),
        ("assembler", ROOT / "tests/benchmark/v3_3-holdout/assemble_sut_outputs.py"),
        ("freezer", ROOT / "tests/benchmark/v3_3-holdout/freeze_sut.py"),
    ]
    for case in aggregate["cases"]:
        paths.append((f"raw-output:{case['case_id']}", ROOT / case["source"]["raw_path"]))
        paths.append(
            (
                f"source-evidence:{case['case_id']}",
                ROOT / case["source"]["attestation_path"],
            )
        )
    document = {
        "version": "3.3",
        "immutable": True,
        "stage": "outputs",
        "sut_execution_authorized": True,
        "frozen_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "canonical_parent_commit": CANONICAL_PARENT,
        "parent_manifest": {
            "path": str(PARENT.relative_to(ROOT)),
            "sha256": parent_hash,
        },
        "artifacts": [entry(role, path) for role, path in paths],
    }
    MANIFEST.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"froze {len(paths)} v3.3 attempt-1 SUT output artifacts")


if __name__ == "__main__":
    main()
