#!/usr/bin/env python3
"""Mutation tests for the v3.2 manager-recipient construction contract."""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
CONTRACT = ROOT / "recipient_manager_contract.py"
TESTS = ROOT / "test_recipient_manager_contract.py"
RESULTS = ROOT / "RECIPIENT_MUTATION_RESULTS.json"

MUTATIONS = {
    "M1_ROUTING_MAY_BE_QUESTION_CANDIDATE": (
        'require(routing_id not in question_ids, "routing case cannot be a question candidate")',
        'require(True, "routing case cannot be a question candidate")',
    ),
    "M2_NON_MANAGER_QUESTION_CANDIDATES_ALLOWED": (
        'require(\n        non_managers == [routing_id],\n        "exactly one non-manager routing case",\n    )',
        'require(\n        True,\n        "exactly one non-manager routing case",\n    )',
    ),
    "M3_ROLE_WITHOUT_MANAGER_ALLOWED": (
        'if "manager" not in role_l:\n        return False',
        'if False:\n        return False',
    ),
}


def run_tests(path: Path) -> subprocess.CompletedProcess:
    environment = os.environ.copy()
    environment["V32_RECIPIENT_CONTRACT_PATH"] = str(path)
    return subprocess.run(
        [sys.executable, "-m", "unittest", str(TESTS)],
        cwd=REPO,
        env=environment,
        capture_output=True,
        text=True,
    )


def main() -> None:
    if RESULTS.exists():
        raise FileExistsError("refusing to overwrite recipient mutation results")
    baseline = run_tests(CONTRACT)
    if baseline.returncode != 0:
        raise RuntimeError(
            "baseline recipient-contract tests failed\n"
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
                raise ValueError(
                    f"{mutation_id}: target count {source.count(old)}"
                )
            mutant = directory / f"{mutation_id}.py"
            mutant.write_text(source.replace(old, new), encoding="utf-8")
            result = run_tests(mutant)
            if "ImportError" in result.stderr or "ModuleNotFoundError" in result.stderr:
                raise RuntimeError(f"{mutation_id}: invalid import failure")
            outcomes.append(
                {
                    "mutation_id": mutation_id,
                    "killed": result.returncode != 0,
                    "return_code": result.returncode,
                    "failure_excerpt": (result.stderr or result.stdout)[-1600:],
                }
            )
    if not all(item["killed"] for item in outcomes):
        survivors = [
            item["mutation_id"] for item in outcomes if not item["killed"]
        ]
        raise RuntimeError(
            "recipient-contract mutant survived: " + ", ".join(survivors)
        )
    document = {
        "schema_version": "v3.2-recipient",
        "baseline_passed": True,
        "mutants": outcomes,
        "killed": sum(item["killed"] for item in outcomes),
        "total": len(outcomes),
        "mutation_score": sum(item["killed"] for item in outcomes) / len(outcomes),
        "attempt1_cases_modified": False,
        "runtime_skill_changes": False,
    }
    RESULTS.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"killed {document['killed']}/{document['total']} recipient-contract mutants")


if __name__ == "__main__":
    main()
