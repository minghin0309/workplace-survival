import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLOUD = ROOT / "tests/benchmark/v2-holdout/cloud-cases"
MANIFEST = CLOUD / "evaluation-manifest-v2.json"
PARENT = CLOUD / "outputs-manifest-v2.json"
FREEZER = ROOT / "tests/benchmark/freeze_cloud_artifacts.py"
BRANCH = "cursor/blind-v2-holdout-17a0"


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


def entry(role: str, path: Path) -> str:
    return f"{role}::{path.relative_to(ROOT)}::{BRANCH}::{latest_commit(path)}"


def main() -> None:
    arguments = [
        sys.executable,
        str(FREEZER),
        str(MANIFEST.relative_to(ROOT)),
        "evaluations",
        str(PARENT.relative_to(ROOT)),
        entry("evaluations", CLOUD / "evaluations-v2-canonical.json"),
        entry("matches", CLOUD / "matches-v2-canonical.json"),
        entry(
            "evaluator-attestation",
            CLOUD / "extraction-attestations/evaluator.json",
        ),
        entry(
            "matcher-attestation",
            CLOUD / "matcher-attestation-v2-canonical.json",
        ),
        entry("extraction-snapshot", CLOUD / "extractions-manifest-v2.json"),
        entry("extraction-adjudication", CLOUD / "extraction-adjudication-v2.json"),
        entry("extraction-audits", CLOUD / "extraction-protocol-audits.json"),
        entry("matcher-audits", CLOUD / "matcher-protocol-audits.json"),
        entry("matcher-source-evidence", CLOUD / "matcher-attestation-v2-clean.json"),
        entry("extraction-normalizer", ROOT / "tests/benchmark/normalize_extractions.py"),
        entry("match-normalizer", ROOT / "tests/benchmark/normalize_matches.py"),
        entry("extraction-validator", ROOT / "tests/benchmark/validate_extractions.py"),
        entry("match-validator", ROOT / "tests/benchmark/validate_matches.py"),
        entry("evaluation-freezer", ROOT / "tests/benchmark/freeze_evaluations.py"),
    ]
    subprocess.run(arguments, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
