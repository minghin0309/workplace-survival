#!/usr/bin/env python3
"""Freeze the v3.3 attempt-1 evaluation/match snapshot. Scorer must not start before this exists."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CLOUD = ROOT / "tests/benchmark/v3_3-holdout/cloud-cases"
MANIFEST = CLOUD / "evaluation-manifest-v33.json"
PARENT = CLOUD / "outputs-manifest-v33.json"
EXTRACTION = CLOUD / "extractions-manifest-v33.json"
BRANCH = "cursor/blind-v33-holdout-17a0"


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
        raise FileExistsError("refusing to overwrite v3.3 attempt-1 evaluation snapshot")
    artifacts = [
        entry("evaluations", CLOUD / "evaluations-v33-canonical.json"),
        entry("matches", CLOUD / "matches-v33.json"),
        entry("evaluator-attestation", CLOUD / "evaluator-attestation-v33.json"),
        entry("matcher-attestation", CLOUD / "matcher-attestation-v33.json"),
        entry("extraction-snapshot", EXTRACTION),
        entry("extraction-adjudication", CLOUD / "extraction-adjudication-v33.json"),
        entry("extraction-audits", CLOUD / "extraction-protocol-audits.json"),
        entry("evaluation-freezer", ROOT / "tests/benchmark/v3_3-holdout/freeze_evaluations.py"),
    ]
    document = {
        "version": "3.3",
        "immutable": True,
        "stage": "evaluations",
        "parent_manifest": {
            "path": str(PARENT.relative_to(ROOT)),
            "sha256": digest(PARENT),
        },
        "parent_extraction_snapshot": {
            "path": str(EXTRACTION.relative_to(ROOT)),
            "sha256": digest(EXTRACTION),
        },
        "frozen_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "artifacts": artifacts,
    }
    MANIFEST.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"froze {len(artifacts)} evaluation artifacts")


if __name__ == "__main__":
    main()
