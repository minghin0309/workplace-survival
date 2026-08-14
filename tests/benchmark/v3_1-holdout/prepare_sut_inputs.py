import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CLOUD = ROOT / "tests/benchmark/v3_1-holdout/cloud-cases"
INPUTS = CLOUD / "sut-inputs"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    cases = json.loads((CLOUD / "cases.json").read_text())["cases"]
    INPUTS.mkdir(parents=True, exist_ok=True)
    entries = []
    for case in cases:
        turns = []
        for turn in case["turns"]:
            raw = turn["user_message"]
            if turn["draft_message"] is not None:
                raw += "\n\nDraft under review:\n" + turn["draft_message"]
            item = {"turn_index": turn["turn_index"], "input_raw": raw}
            if turn["image_path"]:
                item["image_path"] = str(
                    Path("tests/benchmark/v3_1-holdout/cloud-cases")
                    / turn["image_path"]
                )
            turns.append(item)
        document = {
            "schema_version": "v3.1",
            "case_id": case["case_id"],
            "recipient_context": case["recipient_context"],
            "data_a": case["data_a"],
            "turns": turns,
        }
        path = INPUTS / f"{case['case_id']}.json"
        path.write_text(json.dumps(document, indent=2) + "\n")
        entries.append(
            {
                "case_id": case["case_id"],
                "path": str(path.relative_to(ROOT)),
                "sha256": digest(path),
                "turns": len(turns),
            }
        )
    manifest = {
        "schema_version": "v3.1",
        "parent_gold_manifest": {
            "path": "tests/benchmark/v3_1-holdout/cloud-cases/gold-manifest-v31.json",
            "sha256": digest(CLOUD / "gold-manifest-v31.json"),
        },
        "runtime_commit": "9d48b048d083507c20f2714b21053d36b68d6366",
        "runtime_sources": [
            {
                "path": path,
                "sha256": digest(ROOT / path),
            }
            for path in (
                ".cursor/skills/workplace-survival/SKILL.md",
                ".cursor/skills/workplace-survival/REFERENCE.md",
                ".cursor/skills/workplace-survival/FORMATS.md",
                ".cursor/skills/workplace-survival/EXAMPLES.md",
            )
        ],
        "cases": entries,
    }
    (CLOUD / "sut-input-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )
    print("prepared 18 v3.1 SUT inputs")


if __name__ == "__main__":
    main()
