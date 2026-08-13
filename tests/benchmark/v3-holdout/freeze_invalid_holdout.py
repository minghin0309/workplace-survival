import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "tests/benchmark/v3-holdout"
CLOUD = BASE / "cloud-cases"
MANIFEST = CLOUD / "invalid-coverage-manifest-v3.json"
BRANCH = "cursor/blind-v3-holdout-17a0"


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


def main() -> None:
    if MANIFEST.exists():
        raise FileExistsError("refusing to overwrite invalid coverage manifest")
    coverage = json.loads(
        (CLOUD / "coverage-report-v3.json").read_text(encoding="utf-8")
    )
    if coverage["status"] != "INVALID_COVERAGE":
        raise ValueError("holdout is not invalid coverage")
    paths = [
        ("baseline", CLOUD / "baseline-manifest.json"),
        ("cases", CLOUD / "cases.json"),
        ("oracle-notes", CLOUD / "oracle-notes.json"),
        ("image:V3-017", CLOUD / "images/V3-017.png"),
        ("image:V3-018", CLOUD / "images/V3-018.png"),
        ("designer-attestation", CLOUD / "designer-attestation.json"),
        ("labeler-1", CLOUD / "gold-labeler-1.json"),
        ("labeler-2", CLOUD / "gold-labeler-2-clean.json"),
        ("labeler-3", CLOUD / "gold-labeler-3.json"),
        ("labeler-1-source", CLOUD / "gold-labeler-1-attestation.json"),
        ("labeler-2-source", CLOUD / "gold-labeler-2-clean-attestation.json"),
        ("labeler-3-source", CLOUD / "gold-labeler-3-attestation.json"),
        ("raw-gold", CLOUD / "gold-v3-raw.json"),
        ("raw-adjudication", CLOUD / "adjudication-v3-raw.json"),
        ("raw-adjudicator-attestation", CLOUD / "adjudicator-v3-raw-attestation.json"),
        ("gold", CLOUD / "gold-v3.json"),
        ("coverage-report", CLOUD / "coverage-report-v3.json"),
        ("protocol-audits", CLOUD / "gold-protocol-audits.json"),
        ("runtime-manifest", CLOUD / "runtime-manifest.json"),
        ("methodology", ROOT / "tests/benchmark/v3/BENCHMARK_METHODOLOGY_V3.md"),
        ("scorer", ROOT / "tests/benchmark/v3/score_semantic_v3.py"),
        ("case-validator", BASE / "validate_holdout.py"),
        ("gold-validator", BASE / "validate_gold.py"),
        ("finalizer", BASE / "finalize_gold.py"),
        ("freezer", BASE / "freeze_invalid_holdout.py"),
    ]
    document = {
        "version": "3",
        "immutable": True,
        "stage": "invalid-coverage",
        "sut_execution_authorized": False,
        "frozen_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "artifacts": [entry(role, path) for role, path in paths],
    }
    MANIFEST.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"froze {len(paths)} invalid-coverage artifacts")


if __name__ == "__main__":
    main()
