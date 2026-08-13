import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "tests/benchmark/v3-holdout"
CLOUD = BASE / "cloud-cases"

RUNTIME_COMMIT = "9d48b048d083507c20f2714b21053d36b68d6366"
RUNTIME_PATHS = [
    ".cursor/skills/workplace-survival/SKILL.md",
    ".cursor/skills/workplace-survival/REFERENCE.md",
    ".cursor/skills/workplace-survival/FORMATS.md",
    ".cursor/skills/workplace-survival/EXAMPLES.md",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def item(path_text: str) -> dict:
    path = ROOT / path_text
    return {"path": path_text, "sha256": digest(path)}


def main() -> None:
    runtime = {
        "runtime_commit": RUNTIME_COMMIT,
        "runtime_sources": [item(path) for path in RUNTIME_PATHS],
    }
    (CLOUD / "runtime-manifest.json").write_text(
        json.dumps(runtime, indent=2) + "\n", encoding="utf-8"
    )
    holdout = {
        "schema_version": "v3",
        "artifact": "holdout-baseline",
        "methodology": item("tests/benchmark/v3/BENCHMARK_METHODOLOGY_V3.md"),
        "scorer": item("tests/benchmark/v3/score_semantic_v3.py"),
        "plan": item("tests/benchmark/v3-holdout/V3_HOLDOUT_PLAN.md"),
        "case_brief": item("tests/benchmark/v3-holdout/V3_CASE_BRIEF.md"),
        "cases": item("tests/benchmark/v3-holdout/cloud-cases/cases.json"),
        "oracle_notes": item(
            "tests/benchmark/v3-holdout/cloud-cases/oracle-notes.json"
        ),
        "images": [
            item("tests/benchmark/v3-holdout/cloud-cases/images/V3-017.png"),
            item("tests/benchmark/v3-holdout/cloud-cases/images/V3-018.png"),
        ],
        "designer_attestation": item(
            "tests/benchmark/v3-holdout/cloud-cases/designer-attestation.json"
        ),
        "runtime": runtime,
    }
    (CLOUD / "baseline-manifest.json").write_text(
        json.dumps(holdout, indent=2) + "\n", encoding="utf-8"
    )
    print("prepared v3 holdout baseline")


if __name__ == "__main__":
    main()
