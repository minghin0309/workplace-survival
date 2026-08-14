#!/usr/bin/env python3
"""Freeze the v3.1 evaluation/match snapshot. Scorer must not start before this exists."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CLOUD = ROOT / "tests/benchmark/v3_1-holdout/cloud-cases"
MANIFEST = CLOUD / "evaluation-manifest-v31.json"
PARENT = CLOUD / "outputs-manifest-v31.json"
EXTRACTION = CLOUD / "extractions-manifest-v31.json"
BRANCH = "cursor/blind-v31-holdout-17a0"


def latest_commit(path: Path) -> str:
    value = subprocess.run(
        ["git", "log", "-1", "--format=%H", "--", str(path.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if len(value) != 40:
        raise ValueError(f"missing artifact commit: {path}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def entry(role: str, path: Path) -> dict:
    return {
        "role": role,
        "path": str(path.relative_to(ROOT)),
        "sha256": digest(path),
        "cloud_branch": BRANCH,
        "cloud_commit": latest_commit(path),
    }


def main() -> None:
    if MANIFEST.exists():
        raise FileExistsError("refusing to overwrite evaluation snapshot")
    artifacts = [
        entry("evaluations", CLOUD / "evaluations-v31-canonical.json"),
        entry("matches", CLOUD / "matches-v31-canonical.json"),
        entry(
            "evaluator-attestation",
            CLOUD / "extraction-attestations/evaluator.json",
        ),
        entry(
            "matcher-attestation",
            CLOUD / "matcher-attestation-v31-canonical.json",
        ),
        entry("extraction-snapshot", EXTRACTION),
        entry("extraction-adjudication", CLOUD / "extraction-adjudication-v31.json"),
        entry("extraction-audits", CLOUD / "extraction-protocol-audits.json"),
        entry("matcher-audits", CLOUD / "matcher-protocol-audits.json"),
        entry("matcher-source-evidence", CLOUD / "matcher-attestation-v31.json"),
        entry("match-normalizer", ROOT / "tests/benchmark/v3_1-holdout/normalize_matches.py"),
        entry("match-validator", ROOT / "tests/benchmark/v3_1-holdout/validate_matches.py"),
        entry("evaluation-freezer", ROOT / "tests/benchmark/v3_1-holdout/freeze_evaluations.py"),
    ]
    document = {
        "version": "3.1",
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
