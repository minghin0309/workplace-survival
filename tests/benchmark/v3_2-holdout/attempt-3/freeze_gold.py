import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CLOUD = ROOT / "tests/benchmark/v3_2-holdout/attempt-3/cloud-cases"
MANIFEST = CLOUD / "gold-manifest-v323.json"
BRANCH = "cursor/blind-v323-holdout-17a0"


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
        raise FileExistsError("refusing to overwrite v3.2 attempt-3 gold manifest")
    paths = [
        ("cases", CLOUD / "cases.json"),
        ("oracle-notes", CLOUD / "oracle-notes.json"),
        ("question-design", CLOUD / "question-design.json"),
        ("construction-mutations", CLOUD / "construction-mutations.json"),
        *image_entries(),
        ("designer-attestation", CLOUD / "designer-attestation.json"),
        ("labeler-1", CLOUD / "gold-labeler-1.json"),
        ("labeler-2", CLOUD / "gold-labeler-2.json"),
        ("labeler-3", CLOUD / "gold-labeler-3.json"),
        ("labeler-1-attestation", CLOUD / "gold-labeler-1-attestation.json"),
        ("labeler-2-attestation", CLOUD / "gold-labeler-2-attestation.json"),
        ("labeler-3-attestation", CLOUD / "gold-labeler-3-attestation.json"),
        ("raw-gold", CLOUD / "gold-v323-raw.json"),
        ("raw-adjudication", CLOUD / "adjudication-v323-raw.json"),
        ("adjudicator-attestation", CLOUD / "adjudicator-v323-raw-attestation.json"),
        ("gold", CLOUD / "gold-v323.json"),
        ("coverage", CLOUD / "coverage-report-v323.json"),
        ("ontology", ROOT / "tests/benchmark/SEMANTIC_ONTOLOGY.json"),
        ("scorer", ROOT / "tests/benchmark/v3_2/score_semantic_v3_2.py"),
        ("methodology", ROOT / "tests/benchmark/v3_2/BENCHMARK_METHODOLOGY_V32.md"),
        ("recipient-contract", ROOT / "tests/benchmark/v3_2/recipient_manager_contract.py"),
        ("case-brief", ROOT / "tests/benchmark/v3_2/V32_ATTEMPT3_CASE_BRIEF.md"),
        ("plan", ROOT / "tests/benchmark/v3_2-holdout/attempt-3/V323_HOLDOUT_PLAN.md"),
        ("validator", ROOT / "tests/benchmark/v3_2-holdout/attempt-3/validate_holdout.py"),
        ("gold-validator", ROOT / "tests/benchmark/v3_2-holdout/attempt-3/validate_gold.py"),
        ("finalizer", ROOT / "tests/benchmark/v3_2-holdout/attempt-3/finalize_gold.py"),
        ("freezer", ROOT / "tests/benchmark/v3_2-holdout/attempt-3/freeze_gold.py"),
    ]
    coverage = json.loads((CLOUD / "coverage-report-v323.json").read_text())
    if coverage["status"] != "VALID_COVERAGE":
        raise ValueError("gold coverage is not valid")
    roles = {role for role, _ in paths}
    if not {"gold", "ontology", "scorer"} <= roles:
        raise ValueError("gold freeze missing required roles")
    document = {
        "version": "3.2",
        "immutable": True,
        "stage": "gold",
        "sut_execution_authorized": True,
        "frozen_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "artifacts": [entry(role, path) for role, path in paths],
    }
    MANIFEST.write_text(json.dumps(document, indent=2) + "\n")
    print(f"froze {len(paths)} v3.2 attempt-3 gold artifacts")


if __name__ == "__main__":
    main()
