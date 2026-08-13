import hashlib
import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLOUD = ROOT / "tests/benchmark/v2-holdout/cloud-cases"
CANONICAL = CLOUD / "attestations-v2"

SOURCES = {
    "labeler-1": {
        "path": "gold-labeler-1-attestation.json",
        "context_id": "bc-33b3fdac-74ca-5732-a9b3-4bd69c53d71f",
        "model_family": "claude",
        "cloud_branch": "cursor/v2-cloud-gold-labeler-1-d71f",
        "cloud_commit": "24c91e5425fdd2b50b8dd728e329ef88a39474e4",
    },
    "labeler-2": {
        "path": "gold-labeler-2-rerun-attestation.json",
        "context_id": "bc-ad97cf43-3536-51e5-8449-36f664077d45",
        "model_family": "grok",
        "cloud_branch": "cursor/gold-labeler-2-rerun-7d45",
        "cloud_commit": "30bc76b0f569d57a373d91c25bbf4cf14ec176fb",
    },
    "labeler-3": {
        "path": "gold-labeler-3-attestation.json",
        "context_id": "bc-f40cbaca-7400-59c7-9772-52e73bf156bd",
        "model_family": "kimi",
        "cloud_branch": "cursor/v2-gold-labeler-3-56bd",
        "cloud_commit": "c5fdaee38150e738bd4ca040c264fd5674ad0d8d",
    },
    "adjudicator": {
        "path": "adjudicator-v2-raw-attestation.json",
        "context_id": "bc-71c5d4ca-0585-5745-99ec-50491605c172",
        "model_family": "gpt",
        "cloud_branch": "cursor/raw-v2-adjudication-c172",
        "cloud_commit": "5811293f638248d896dc3319ddcd5d0898aa0efb",
    },
    "designer": {
        "path": "designer-attestation.json",
        "context_id": "bc-40936f78-40fe-5055-b664-fa5adf60294f",
        "model_family": "claude",
        "cloud_branch": "cursor/v2-cloud-cases-294f",
        "cloud_commit": "a638d2b87ef17c36e394319e3e46b361eb6eb061",
    },
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def files_read(role: str, source: dict) -> list:
    if isinstance(source.get("files_read"), list):
        return source["files_read"]
    if role == "labeler-3":
        return [
            {"path": "tests/benchmark/v2-holdout/cloud-cases/cases.json"},
            {"path": "tests/benchmark/v2-holdout/cloud-cases/images/V2-017.png"},
            {"path": "tests/benchmark/v2-holdout/cloud-cases/images/V2-018.png"},
            {"path": "tests/blind/GOLD_RUBRIC.md"},
            {"path": "tests/benchmark/SEMANTIC_ONTOLOGY.json"},
        ]
    if role == "designer":
        return source["isolation"]["repository_files_read"]
    raise ValueError(f"{role}: files_read unavailable")


def limitations(role: str, source: dict) -> list[str]:
    values = list(source.get("limitations", []))
    if not values:
        values.append(
            "The source attestation did not use the canonical limitations schema."
        )
    values.append(
        "Machine model ID was unavailable from cloud run metadata; model_id is "
        "recorded as unverified and model_family is the protocol-assigned family."
    )
    if role in {"labeler-2", "adjudicator"}:
        values.append("A transcript-level allowlist audit passed before acceptance.")
    return values


def write_attestation(role: str, config: dict) -> Path:
    source_path = CLOUD / config["path"]
    source = json.loads(source_path.read_text(encoding="utf-8"))
    output_path = CANONICAL / f"{role}.json"
    document = {
        "schema_version": "v2",
        "role": role,
        "context_id": config["context_id"],
        "model_id": "unverified",
        "model_id_provenance": (
            "Cloud run metadata did not expose an exact machine model ID; no ID was guessed."
        ),
        "model_family": config["model_family"],
        "model_family_provenance": "protocol-assigned; not machine-metadata-verified",
        "cloud_branch": config["cloud_branch"],
        "cloud_commit": config["cloud_commit"],
        "files_read": files_read(role, source),
        "limitations": limitations(role, source),
        "source_attestation": {
            "path": relative(source_path),
            "sha256": digest(source_path),
        },
        "normalization": {
            "kind": "mechanical-schema-wrapper",
            "semantic_decisions_changed": False,
        },
    }
    output_path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    return output_path


def main() -> None:
    CANONICAL.mkdir(parents=True, exist_ok=True)
    attestations = {
        role: write_attestation(role, config)
        for role, config in SOURCES.items()
    }

    raw_gold_path = CLOUD / "gold-v2-raw.json"
    gold_path = CLOUD / "gold-v2.json"
    raw_gold = json.loads(raw_gold_path.read_text(encoding="utf-8"))
    gold = deepcopy(raw_gold)
    raw_decisions = json.dumps(raw_gold["cases"], sort_keys=True)
    gold["artifact"] = "gold-labels-readjudicated-canonical"
    gold["gold_quality"]["attestations"] = [
        {
            "role": role,
            "path": relative(attestations[role]),
            "sha256": digest(attestations[role]),
        }
        for role in ("labeler-1", "labeler-2", "labeler-3", "adjudicator")
    ]
    if json.dumps(gold["cases"], sort_keys=True) != raw_decisions:
        raise RuntimeError("normalization changed readjudicated gold decisions")
    gold_path.write_text(json.dumps(gold, indent=2) + "\n", encoding="utf-8")

    raw_adjudication_path = CLOUD / "adjudication-v2-raw.json"
    adjudication_path = CLOUD / "adjudication-v2.json"
    raw_adjudication = json.loads(raw_adjudication_path.read_text(encoding="utf-8"))
    adjudication = deepcopy(raw_adjudication)
    raw_adjudicated_cases = json.dumps(raw_adjudication["cases"], sort_keys=True)
    adjudication["artifact"] = "gold-adjudication"
    adjudication["gold_output_path"] = relative(gold_path)
    adjudicator_path = attestations["adjudicator"]
    adjudication["adjudicator_attestation"] = {
        "path": relative(adjudicator_path),
        "sha256": digest(adjudicator_path),
    }
    if json.dumps(adjudication["cases"], sort_keys=True) != raw_adjudicated_cases:
        raise RuntimeError("normalization changed raw adjudication decisions")
    adjudication_path.write_text(
        json.dumps(adjudication, indent=2) + "\n", encoding="utf-8"
    )
    print(
        "normalized corrected v2 gold and five attestations; "
        "adjudicated decisions unchanged"
    )


if __name__ == "__main__":
    main()
