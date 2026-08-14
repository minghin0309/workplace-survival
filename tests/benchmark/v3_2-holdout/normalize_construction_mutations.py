import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CLOUD = ROOT / "tests/benchmark/v3_2-holdout/cloud-cases"


def main() -> None:
    design = json.loads(
        (CLOUD / "question-design.json").read_text(encoding="utf-8")
    )
    entries = design.get("entries") or design.get("candidates")
    if not entries:
        raise ValueError("question-design missing entries/candidates")
    document = {
        "schema_version": "v3.2",
        "artifact": "construction-mutations",
        "suite_id": design["suite_id"],
        "mutations": [
            {
                "case_id": entry["case_id"],
                "mutation_type": mutation["mutation_type"],
                "before_state": entry["base_state"],
                "after_state": mutation["resulting_state"],
            }
            for entry in entries
            for mutation in entry["mutations"]
        ],
    }
    path = CLOUD / "construction-mutations.json"
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"normalized {len(document['mutations'])} construction mutations")


if __name__ == "__main__":
    main()
