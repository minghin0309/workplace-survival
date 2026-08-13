import hashlib
import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLOUD = ROOT / "tests/benchmark/v2-holdout/cloud-cases"
CANONICAL = CLOUD / "extraction-attestations"

SOURCES = {
    "extractor-1": {
        "path": "extractor-1-attestation.json",
        "context_id": "bc-7896a9d2-dc62-5494-8f72-df88bbf0f6a5",
        "model_family": "claude",
        "cloud_branch": "cursor/blind-v2-extractor-1-f6a5",
        "cloud_commit": "c19d189833d22cb95df3461487b72d19d79a101d",
    },
    "extractor-2": {
        "path": "extractor-2-attestation.json",
        "context_id": "bc-78dd5451-c6ec-52d5-b206-4ae4dcd21296",
        "model_family": "kimi",
        "cloud_branch": "cursor/blind-extractor-2-1296",
        "cloud_commit": "ffd6d7ec6d5cf80611945153e47d17a73843548c",
    },
    "evaluator": {
        "path": "evaluator-attestation-v2.json",
        "context_id": "bc-a9b8eb81-9224-509c-9ff8-641592ef875e",
        "model_family": "gpt",
        "cloud_branch": "cursor/blind-v2-adjudication-875e",
        "cloud_commit": "5510fa1c23426f94c36add975ad5dc77cc3f8402",
    },
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def source_limitations(source: dict) -> list[str]:
    values = source.get("limitations", [])
    if not isinstance(values, list):
        values = [str(values)]
    return values


def write_wrapper(role: str, config: dict) -> Path:
    source_path = CLOUD / config["path"]
    source = json.loads(source_path.read_text(encoding="utf-8"))
    output_path = CANONICAL / f"{role}.json"
    document = {
        "schema_version": "v2",
        "role": role,
        "context_id": config["context_id"],
        "model_id": "unverified",
        "model_family": config["model_family"],
        "cloud_branch": config["cloud_branch"],
        "cloud_commit": config["cloud_commit"],
        "files_read": source["files_read"],
        "limitations": source_limitations(source)
        + [
            "Machine model ID was unavailable from cloud run metadata; no ID was guessed.",
            "Transcript audit disposition is recorded in extraction-protocol-audits.json.",
        ],
        "source_attestation": {
            "path": relative(source_path),
            "sha256": digest(source_path),
        },
        "normalization": {
            "kind": "mechanical-provenance-wrapper",
            "extraction_decisions_changed": False,
        },
    }
    output_path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    return output_path


def main() -> None:
    CANONICAL.mkdir(parents=True, exist_ok=True)
    wrappers = {
        role: write_wrapper(role, config) for role, config in SOURCES.items()
    }
    raw_path = CLOUD / "evaluations-v2.json"
    canonical_path = CLOUD / "evaluations-v2-canonical.json"
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    canonical = deepcopy(raw)
    raw_cases = json.dumps(raw["cases"], sort_keys=True)
    canonical["evaluation_quality"]["extractors"] = [
        {
            "context_id": SOURCES[role]["context_id"],
            "model_id": "unverified",
            "model_family": SOURCES[role]["model_family"],
            "attestation_path": relative(wrappers[role]),
            "attestation_sha256": digest(wrappers[role]),
        }
        for role in ("extractor-1", "extractor-2")
    ]
    canonical["evaluation_quality"]["adjudicator"] = {
        "context_id": SOURCES["evaluator"]["context_id"],
        "model_id": "unverified",
        "model_family": "gpt",
    }
    if json.dumps(canonical["cases"], sort_keys=True) != raw_cases:
        raise RuntimeError("normalization changed evaluation decisions")
    canonical_path.write_text(
        json.dumps(canonical, indent=2) + "\n", encoding="utf-8"
    )
    print("normalized two extractor attestations and evaluator provenance")


if __name__ == "__main__":
    main()
