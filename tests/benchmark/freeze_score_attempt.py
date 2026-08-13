import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLOUD = ROOT / "tests/benchmark/v2-holdout/cloud-cases"
MANIFEST = CLOUD / "score-attempt-manifest-v2.json"
PARENT = CLOUD / "evaluation-manifest-v2.json"
BRANCH = "cursor/blind-v2-holdout-17a0"


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
        raise ValueError(f"missing artifact commit: {path}")
    return value


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
        raise FileExistsError("refusing to overwrite score attempt manifest")
    report = json.loads((CLOUD / "score-report-v2.json").read_text(encoding="utf-8"))
    if report["status"] != "SCORER_ERROR" or report["formal_attempt_count"] != 1:
        raise ValueError("formal score failure record missing")
    document = {
        "version": "2",
        "immutable": True,
        "stage": "score-attempt",
        "parent_evaluation_manifest": {
            "path": str(PARENT.relative_to(ROOT)),
            "sha256": digest(PARENT),
        },
        "frozen_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "artifacts": [
            entry("score-report", CLOUD / "score-report-v2.json"),
            entry("triage", ROOT / "tests/benchmark/v2-holdout/SCORE_TRIAGE.md"),
            entry("scorer", ROOT / "tests/benchmark/score_semantic.py"),
            entry("validator", ROOT / "tests/benchmark/validate_score_attempt.py"),
            entry("freezer", ROOT / "tests/benchmark/freeze_score_attempt.py"),
        ],
    }
    MANIFEST.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print("froze failed formal score attempt")


if __name__ == "__main__":
    main()
