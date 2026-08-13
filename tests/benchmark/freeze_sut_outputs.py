import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLOUD = ROOT / "tests/benchmark/v2-holdout/cloud-cases"
MANIFEST = CLOUD / "outputs-manifest-v2.json"
PARENT = CLOUD / "gold-manifest-v2.json"
FREEZER = ROOT / "tests/benchmark/freeze_cloud_artifacts.py"
BRANCH = "cursor/blind-v2-holdout-17a0"


def latest_commit(path: Path) -> str:
    result = subprocess.run(
        ["git", "log", "-1", "--format=%H", "--", str(path.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if len(result) != 40:
        raise ValueError(f"missing artifact commit: {path}")
    return result


def entry(role: str, path: Path) -> str:
    return f"{role}::{path.relative_to(ROOT)}::{BRANCH}::{latest_commit(path)}"


def main() -> None:
    aggregate_path = CLOUD / "outputs-v2-raw.json"
    aggregate = json.loads(aggregate_path.read_text(encoding="utf-8"))
    arguments = [
        sys.executable,
        str(FREEZER),
        str(MANIFEST.relative_to(ROOT)),
        "outputs",
        str(PARENT.relative_to(ROOT)),
        entry("outputs", aggregate_path),
        entry("generator-attestation", CLOUD / "generator-attestation-v2.json"),
        entry("sut-input-manifest", CLOUD / "sut-input-manifest.json"),
        entry("protocol-audits", CLOUD / "sut-protocol-audits.json"),
        entry("normalizer", ROOT / "tests/benchmark/normalize_sut_outputs.py"),
        entry("validator", ROOT / "tests/benchmark/validate_sut_outputs.py"),
    ]
    for case in aggregate["cases"]:
        case_id = case["case_id"]
        arguments.append(entry(f"raw-output:{case_id}", ROOT / case["source"]["raw_path"]))
        arguments.append(
            entry(
                f"source-evidence:{case_id}",
                ROOT / case["source"]["attestation_path"],
            )
        )
    subprocess.run(arguments, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
