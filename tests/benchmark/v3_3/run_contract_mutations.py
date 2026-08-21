#!/usr/bin/env python3
"""Mutation tests for the v3.3 revision and gold-label construction contract."""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
CONTRACT = ROOT / "revision_scoring_contract.py"
TESTS = ROOT / "test_revision_scoring_contract.py"
RESULTS = ROOT / "CONTRACT_MUTATION_RESULTS.json"

MUTATIONS = {
    "M1_PRESERVE_RECIPIENT_MAY_BE_REQUIRED": (
        'IMPLICIT_PRESERVE_RECIPIENT not in required,\n        "preserve-intended-recipient cannot be required",',
        'True,\n        "preserve-intended-recipient cannot be required",',
    ),
    "M2_ESTABLISHED_OMISSION_MAY_BE_GRAY": (
        'gold_turn.get("responsibility") == "Red",\n            "established omission must be gold Red",',
        'True,\n            "established omission must be gold Red",',
    ),
    "M3_OCCLUDED_ROLE_OPTIONAL": (
        'role in OCCLUDED_ROLES, "image_only candidate missing occluded_role"',
        'True, "image_only candidate missing occluded_role"',
    ),
}


def run_tests(path: Path) -> subprocess.CompletedProcess:
    environment = os.environ.copy()
    environment["V33_REVISION_CONTRACT_PATH"] = str(path)
    return subprocess.run(
        [sys.executable, "-m", "unittest", str(TESTS)],
        cwd=REPO,
        env=environment,
        capture_output=True,
        text=True,
    )


def main() -> None:
    if RESULTS.exists():
        raise FileExistsError("refusing to overwrite contract mutation results")
    baseline = run_tests(CONTRACT)
    if baseline.returncode != 0:
        raise RuntimeError(
            "baseline v3.3 revision contract tests failed\n"
            + baseline.stdout
            + "\n"
            + baseline.stderr
        )

    source = CONTRACT.read_text(encoding="utf-8")
    outcomes = []
    with tempfile.TemporaryDirectory() as directory:
        directory = Path(directory)
        for mutation_id, (old, new) in MUTATIONS.items():
            if source.count(old) != 1:
                raise ValueError(f"{mutation_id}: mutation target not unique")
            mutant_path = directory / f"{mutation_id}.py"
            mutant_path.write_text(source.replace(old, new), encoding="utf-8")
            result = run_tests(mutant_path)
            if "ImportError" in result.stderr or "ModuleNotFoundError" in result.stderr:
                raise RuntimeError(
                    f"{mutation_id}: invalid mutation harness import failure"
                )
            outcomes.append(
                {
                    "mutation_id": mutation_id,
                    "killed": result.returncode != 0,
                    "return_code": result.returncode,
                    "failure_excerpt": (result.stderr or result.stdout)[-2000:],
                }
            )
    if not all(item["killed"] for item in outcomes):
        raise RuntimeError("one or more v3.3 contract mutants survived")
    document = {
        "schema_version": "v3.3",
        "baseline_passed": True,
        "mutants": outcomes,
        "killed": sum(item["killed"] for item in outcomes),
        "total": len(outcomes),
        "mutation_score": sum(item["killed"] for item in outcomes) / len(outcomes),
    }
    RESULTS.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"killed {document['killed']}/{document['total']} v3.3 contract mutants")


if __name__ == "__main__":
    main()
