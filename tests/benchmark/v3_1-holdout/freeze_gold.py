import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CLOUD = ROOT / "tests/benchmark/v3_1-holdout/cloud-cases"
MANIFEST = CLOUD / "gold-manifest-v31.json"
BRANCH = "cursor/blind-v31-holdout-17a0"


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
        raise FileExistsError("refusing to overwrite v3.1 gold manifest")
    paths = [
        ("cases", CLOUD / "cases.json"),
        ("oracle-notes", CLOUD / "oracle-notes.json"),
        ("question-design", CLOUD / "question-design.json"),
        ("construction-mutations", CLOUD / "construction-mutations.json"),
        ("image:V31-008", CLOUD / "images/V31-008-block-order-docket.png"),
        ("image:V31-018", CLOUD / "images/V31-018-draft-note.png"),
        ("designer-attestation", CLOUD / "designer-attestation.json"),
        ("labeler-1", CLOUD / "gold-labeler-1.json"),
        ("labeler-2", CLOUD / "gold-labeler-2-clean.json"),
        ("labeler-3", CLOUD / "gold-labeler-3-clean.json"),
        ("labeler-1-attestation", CLOUD / "gold-labeler-1-attestation.json"),
        ("labeler-2-attestation", CLOUD / "gold-labeler-2-clean-attestation.json"),
        ("labeler-3-attestation", CLOUD / "gold-labeler-3-clean.attestation.json"),
        ("raw-gold", CLOUD / "gold-v31-raw.json"),
        ("raw-adjudication", CLOUD / "adjudication-v31-raw.json"),
        ("adjudicator-attestation", CLOUD / "adjudicator-v31-raw-attestation.json"),
        ("gold", CLOUD / "gold-v31.json"),
        ("coverage", CLOUD / "coverage-report-v31.json"),
        ("scorer", ROOT / "tests/benchmark/v3/score_semantic_v3.py"),
        ("methodology", ROOT / "tests/benchmark/v3/BENCHMARK_METHODOLOGY_V3.md"),
        ("case-brief", ROOT / "tests/benchmark/v3_1/V3_1_CASE_BRIEF.md"),
        ("plan", ROOT / "tests/benchmark/v3_1-holdout/V31_HOLDOUT_PLAN.md"),
        ("validator", ROOT / "tests/benchmark/v3_1-holdout/validate_holdout.py"),
        ("gold-validator", ROOT / "tests/benchmark/v3_1-holdout/validate_gold.py"),
        ("finalizer", ROOT / "tests/benchmark/v3_1-holdout/finalize_gold.py"),
        ("freezer", ROOT / "tests/benchmark/v3_1-holdout/freeze_gold.py"),
    ]
    coverage = json.loads((CLOUD / "coverage-report-v31.json").read_text())
    if coverage["status"] != "VALID_COVERAGE":
        raise ValueError("gold coverage is not valid")
    document = {
        "version": "3.1",
        "immutable": True,
        "stage": "gold",
        "sut_execution_authorized": True,
        "frozen_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "artifacts": [entry(role, path) for role, path in paths],
    }
    MANIFEST.write_text(json.dumps(document, indent=2) + "\n")
    print(f"froze {len(paths)} v3.1 gold artifacts")


if __name__ == "__main__":
    main()
