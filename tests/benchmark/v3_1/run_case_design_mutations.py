import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONTRACT = ROOT / "question_candidate_contract.py"
TESTS = ROOT / "test_question_candidate_contract.py"
RESULTS = ROOT / "MUTATION_RESULTS.json"

MUTATIONS = {
    "M1_PLACEHOLDER_ESCAPE_IGNORED": (
        'and not candidate["placeholder_safe"]',
        "and True",
    ),
    "M2_DOMINANT_RED_IGNORED": (
        'and not candidate["direct_red_defects"]',
        "and True",
    ),
    "M3_SUPPLIED_ANSWER_STILL_MISSING": (
        'mutated["answer_absent"] = False',
        'mutated["answer_absent"] = True',
    ),
    "M4_OVERPROVISIONING_DISABLED": (
        "MIN_CANDIDATES = 6",
        "MIN_CANDIDATES = 3",
    ),
}


def run_tests(path: Path) -> subprocess.CompletedProcess:
    environment = os.environ.copy()
    environment["V31_QUESTION_CONTRACT_PATH"] = str(path)
    return subprocess.run(
        [sys.executable, "-m", "unittest", str(TESTS)],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
    )


def main() -> None:
    if RESULTS.exists():
        raise FileExistsError("refusing to overwrite case-design mutation results")
    baseline = run_tests(CONTRACT)
    if baseline.returncode != 0:
        raise RuntimeError("baseline case-design tests failed\n" + baseline.stderr)
    source = CONTRACT.read_text(encoding="utf-8")
    outcomes = []
    with tempfile.TemporaryDirectory() as directory:
        directory = Path(directory)
        for mutation_id, (old, new) in MUTATIONS.items():
            if source.count(old) != 1:
                raise ValueError(f"{mutation_id}: target not unique")
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
                    "failure_excerpt": result.stderr[-1600:],
                }
            )
    if not all(item["killed"] for item in outcomes):
        raise RuntimeError("case-design mutant survived")
    document = {
        "schema_version": "v3.1",
        "baseline_passed": True,
        "mutants": outcomes,
        "killed": sum(item["killed"] for item in outcomes),
        "total": len(outcomes),
        "mutation_score": sum(item["killed"] for item in outcomes) / len(outcomes),
    }
    RESULTS.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"killed {document['killed']}/{document['total']} case-design mutants")


if __name__ == "__main__":
    main()
