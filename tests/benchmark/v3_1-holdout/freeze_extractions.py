#!/usr/bin/env python3
"""Freeze the v3.1 extraction snapshot. Matcher must not start before this exists."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CLOUD = ROOT / "tests/benchmark/v3_1-holdout/cloud-cases"
MANIFEST = CLOUD / "extractions-manifest-v31.json"
PARENT = CLOUD / "outputs-manifest-v31.json"
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
        raise FileExistsError("refusing to overwrite extraction snapshot")
    artifacts = [
        entry("extractor-1", CLOUD / "extractor-1-raw.json"),
        entry("extractor-2", CLOUD / "extractor-2-raw.json"),
        entry(
            "extractor-1-attestation",
            CLOUD / "extraction-attestations/extractor-1.json",
        ),
        entry(
            "extractor-2-attestation",
            CLOUD / "extraction-attestations/extractor-2.json",
        ),
        entry("evaluations", CLOUD / "evaluations-v31-canonical.json"),
        entry(
            "evaluator-attestation",
            CLOUD / "extraction-attestations/evaluator.json",
        ),
        entry("extraction-adjudication", CLOUD / "extraction-adjudication-v31.json"),
        entry("extractor-1-source-evidence", CLOUD / "extractor-1-attestation.json"),
        entry("extractor-2-source-evidence", CLOUD / "extractor-2-attestation.json"),
        entry("evaluator-source-evidence", CLOUD / "evaluator-attestation-v31.json"),
        entry("protocol-audits", CLOUD / "extraction-protocol-audits.json"),
        entry("extractor-visible", CLOUD / "extractor-visible.json"),
        entry("normalizer", ROOT / "tests/benchmark/v3_1-holdout/normalize_extractions.py"),
        entry("validator", ROOT / "tests/benchmark/v3_1-holdout/validate_extractions.py"),
        entry("freezer", ROOT / "tests/benchmark/v3_1-holdout/freeze_extractions.py"),
    ]
    document = {
        "version": "3.1",
        "immutable": True,
        "stage": "extraction-snapshot",
        "parent_outputs_manifest": {
            "path": str(PARENT.relative_to(ROOT)),
            "sha256": digest(PARENT),
        },
        "frozen_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "artifacts": artifacts,
    }
    MANIFEST.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"froze {len(artifacts)} extraction artifacts")


if __name__ == "__main__":
    main()
