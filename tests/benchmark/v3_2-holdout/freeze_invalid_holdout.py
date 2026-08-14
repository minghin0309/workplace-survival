#!/usr/bin/env python3
"""Freeze the v3.2 attempt-1 invalid-coverage chain. Do not authorize SUT or invoke the scorer."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "tests/benchmark/v3_2-holdout"
CLOUD = BASE / "cloud-cases"
MANIFEST = CLOUD / "invalid-coverage-manifest-v32.json"
BRANCH = "cursor/blind-v32-holdout-17a0"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def latest_commit(path: Path) -> str:
    value = subprocess.run(
        ["git", "log", "-1", "--format=%H", "--", str(path.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if len(value) != 40:
        raise ValueError(f"missing commit: {path}")
    return value


def entry(role: str, path: Path) -> dict:
    return {
        "role": role,
        "path": str(path.relative_to(ROOT)),
        "sha256": digest(path),
        "cloud_branch": BRANCH,
        "cloud_commit": latest_commit(path),
    }


def image_entries() -> list[tuple[str, Path]]:
    cases = json.loads((CLOUD / "cases.json").read_text(encoding="utf-8"))
    seen = []
    for case in cases["cases"]:
        for turn in case["turns"]:
            relative = turn.get("image_path")
            if not relative:
                continue
            path = CLOUD / relative
            if not path.is_file():
                path = ROOT / relative
            seen.append((f"image:{case['case_id']}", path))
    return seen


def main() -> None:
    if MANIFEST.exists():
        raise FileExistsError("refusing to overwrite invalid coverage manifest")
    coverage = json.loads((CLOUD / "coverage-report-v32.json").read_text())
    if coverage["status"] != "INVALID_COVERAGE":
        raise ValueError("holdout is not invalid coverage")
    if coverage["sut_execution_authorized"]:
        raise ValueError("SUT must not be authorized")
    paths = [
        ("cases", CLOUD / "cases.json"),
        ("oracle-notes", CLOUD / "oracle-notes.json"),
        ("question-design", CLOUD / "question-design.json"),
        ("construction-mutations", CLOUD / "construction-mutations.json"),
        ("construction-copy", CLOUD / "construction-copy.json"),
        *image_entries(),
        ("designer-attestation", CLOUD / "designer-attestation.json"),
        ("labeler-1", CLOUD / "gold-labeler-1.json"),
        ("labeler-2", CLOUD / "gold-labeler-2.json"),
        ("labeler-3", CLOUD / "gold-labeler-3.json"),
        ("labeler-1-attestation", CLOUD / "gold-labeler-1-attestation.json"),
        ("labeler-2-attestation", CLOUD / "gold-labeler-2-attestation.json"),
        ("labeler-3-attestation", CLOUD / "gold-labeler-3-attestation.json"),
        ("raw-gold", CLOUD / "gold-v32-raw.json"),
        ("raw-adjudication", CLOUD / "adjudication-v32-raw.json"),
        ("adjudicator-attestation", CLOUD / "adjudicator-v32-raw-attestation.json"),
        ("gold", CLOUD / "gold-v32.json"),
        ("coverage", CLOUD / "coverage-report-v32.json"),
        ("protocol-audits", CLOUD / "gold-protocol-audits.json"),
        ("ontology", ROOT / "tests/benchmark/SEMANTIC_ONTOLOGY.json"),
        ("scorer", ROOT / "tests/benchmark/v3_2/score_semantic_v3_2.py"),
        ("methodology", ROOT / "tests/benchmark/v3_2/BENCHMARK_METHODOLOGY_V32.md"),
        ("case-brief", BASE / "V32_CASE_BRIEF.md"),
        ("plan", BASE / "V32_HOLDOUT_PLAN.md"),
        ("results", BASE / "V32_HOLDOUT_RESULTS.md"),
        ("validator", BASE / "validate_holdout.py"),
        ("finalizer", BASE / "finalize_gold.py"),
        ("freezer", BASE / "freeze_invalid_holdout.py"),
    ]
    document = {
        "version": "3.2",
        "immutable": True,
        "stage": "invalid-coverage",
        "sut_execution_authorized": False,
        "formal_scorer_invocations": 0,
        "frozen_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "artifacts": [entry(role, path) for role, path in paths],
    }
    MANIFEST.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"froze {len(paths)} invalid-coverage artifacts")


if __name__ == "__main__":
    main()
