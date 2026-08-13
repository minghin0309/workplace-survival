import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SCORER = ROOT / "score_semantic_v3.py"
TESTS = ROOT / "test_scorer_v3.py"
RESULTS = ROOT / "MUTATION_RESULTS.json"

MUTATIONS = {
    "M1_ZERO_DENOMINATOR_DIVIDES": (
        "if denominator == 0:",
        "if False and denominator == 0:",
    ),
    "M2_COVERAGE_MINIMUM_DISABLED": (
        "MIN_REQUIRED_CONCEPTS = 3\nMIN_REQUIRED_CASES = 3",
        "MIN_REQUIRED_CONCEPTS = 0\nMIN_REQUIRED_CASES = 0",
    ),
    "M3_EXCEPTION_ENVELOPE_DISABLED": (
        "if not report_path.exists():\n            write_json_once(",
        "if False and not report_path.exists():\n            write_json_once(",
    ),
}


def run_tests(module_path: Path) -> subprocess.CompletedProcess:
    environment = os.environ.copy()
    environment["V3_SCORER_MODULE_PATH"] = str(module_path)
    environment["PYTHONPATH"] = os.pathsep.join(
        filter(None, (str(ROOT.parent), environment.get("PYTHONPATH")))
    )
    return subprocess.run(
        [sys.executable, "-m", "unittest", str(TESTS)],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
    )


def main() -> None:
    if RESULTS.exists():
        raise FileExistsError("refusing to overwrite mutation results")
    baseline = run_tests(SCORER)
    if baseline.returncode != 0:
        raise RuntimeError("baseline v3 scorer tests failed\n" + baseline.stderr)

    source = SCORER.read_text(encoding="utf-8")
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
                raise RuntimeError(f"{mutation_id}: invalid mutation harness import failure")
            outcomes.append(
                {
                    "mutation_id": mutation_id,
                    "killed": result.returncode != 0,
                    "return_code": result.returncode,
                    "failure_excerpt": result.stderr[-2000:],
                }
            )
    if not all(item["killed"] for item in outcomes):
        raise RuntimeError("one or more v3 scorer mutants survived")
    document = {
        "schema_version": "v3",
        "baseline_passed": True,
        "mutants": outcomes,
        "killed": sum(item["killed"] for item in outcomes),
        "total": len(outcomes),
        "mutation_score": sum(item["killed"] for item in outcomes) / len(outcomes),
    }
    RESULTS.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"killed {document['killed']}/{document['total']} v3 scorer mutants")


if __name__ == "__main__":
    main()
