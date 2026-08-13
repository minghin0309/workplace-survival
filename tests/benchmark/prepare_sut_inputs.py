import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLOUD = ROOT / "tests/benchmark/v2-holdout/cloud-cases"
INPUTS = CLOUD / "sut-inputs"
CASES_PATH = CLOUD / "cases.json"
GOLD_MANIFEST_PATH = CLOUD / "gold-manifest-v2.json"
RUNTIME_MANIFEST_PATH = CLOUD / "runtime-manifest.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def main() -> None:
    cases_document = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    cases = cases_document["cases"]
    gold_manifest = json.loads(GOLD_MANIFEST_PATH.read_text(encoding="utf-8"))
    frozen = {entry["role"]: entry for entry in gold_manifest["artifacts"]}
    if frozen["cases"]["sha256"] != digest(CASES_PATH):
        raise ValueError("SUT input source is not the frozen case artifact")

    runtime = json.loads(RUNTIME_MANIFEST_PATH.read_text(encoding="utf-8"))
    INPUTS.mkdir(parents=True, exist_ok=True)
    entries = []
    for case in cases:
        turns = []
        for turn in case["turns"]:
            prepared_turn = {
                "turn_index": turn["turn_index"],
                "input_raw": turn["input_raw"],
            }
            if turn.get("image_path") is not None:
                prepared_turn["image_path"] = turn["image_path"]
            turns.append(prepared_turn)
        document = {
            "schema_version": "v2",
            "case_id": case["case_id"],
            "recipient_context": case["recipient_context"],
            "data_a": case["data_a"],
            "turns": turns,
        }
        forbidden = {"category", "image_spec", "design_intent", "difficulty_notes"}
        if forbidden & set(document):
            raise ValueError(f"{case['case_id']}: hidden benchmark metadata leaked")
        output_path = INPUTS / f"{case['case_id']}.json"
        output_path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
        entries.append(
            {
                "case_id": case["case_id"],
                "path": relative(output_path),
                "sha256": digest(output_path),
                "turns": len(turns),
                "image_paths": [
                    turn["image_path"] for turn in turns if "image_path" in turn
                ],
            }
        )

    manifest = {
        "schema_version": "v2",
        "artifact": "sut-input-manifest",
        "source_cases": {
            "path": relative(CASES_PATH),
            "sha256": digest(CASES_PATH),
        },
        "parent_gold_manifest": {
            "path": relative(GOLD_MANIFEST_PATH),
            "sha256": digest(GOLD_MANIFEST_PATH),
        },
        "runtime": runtime,
        "cases": entries,
    }
    manifest_path = CLOUD / "sut-input-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"prepared {len(entries)} isolated SUT inputs")


if __name__ == "__main__":
    main()
