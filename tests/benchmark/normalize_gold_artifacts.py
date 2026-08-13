import hashlib
import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLOUD = ROOT / "tests/benchmark/v2-holdout/cloud-cases"
CANONICAL = CLOUD / "attestations"

ATTESTATIONS = {
    "labeler-1": {
        "source": "gold-labeler-1-attestation.json",
        "output": "labeler-1.json",
        "context_id": "bc-33b3fdac-74ca-5732-a9b3-4bd69c53d71f",
        "model_id": "claude-opus-5",
        "model_family": "claude",
        "cloud_branch": "cursor/v2-cloud-gold-labeler-1-d71f",
        "cloud_commit": "a06bbdfbd4e5237319f8580e20c0df5fa7ac4e3d",
    },
    "labeler-2": {
        "source": "gold-labeler-2-attestation.json",
        "output": "labeler-2.json",
        "context_id": "bc-1ce294c2-e4d2-5d25-b8fe-40cb5279c94a",
        "model_id": "cursor-grok-4.5",
        "model_family": "grok",
        "cloud_branch": "cursor/v2-gold-labeler-2-c94a",
        "cloud_commit": "bcdd71d8ecaaa52e8b43d1ca8aaa569c3223a312",
    },
    "labeler-3": {
        "source": "gold-labeler-3-attestation.json",
        "output": "labeler-3.json",
        "context_id": "bc-f40cbaca-7400-59c7-9772-52e73bf156bd",
        "model_id": "kimi-k3",
        "model_family": "kimi",
        "cloud_branch": "cursor/v2-gold-labeler-3-56bd",
        "cloud_commit": "c5fdaee38150e738bd4ca040c264fd5674ad0d8d",
    },
    "adjudicator": {
        "source": "adjudicator-attestation.json",
        "output": "adjudicator.json",
        "context_id": "bc-4ff6c2e1-5c63-5370-bb9d-11ea3c2786eb",
        "model_id": "gpt-5.5",
        "model_family": "gpt",
        "cloud_branch": "cursor/cloud-v2-gold-adjudicator-86eb",
        "cloud_commit": "5f47ba829827bf8db817464f9dc98fb569713683",
    },
    "designer": {
        "source": "designer-attestation.json",
        "output": "designer.json",
        "context_id": "bc-40936f78-40fe-5055-b664-fa5adf60294f",
        "model_id": "claude-opus-5",
        "model_family": "claude",
        "cloud_branch": "cursor/v2-cloud-cases-294f",
        "cloud_commit": "a638d2b87ef17c36e394319e3e46b361eb6eb061",
    },
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def source_files(role: str, source: dict) -> list:
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
    raise ValueError(f"{role}: source attestation does not identify files read")


def source_limitations(role: str, source: dict) -> list[str]:
    if isinstance(source.get("limitations"), list):
        return source["limitations"]
    if role == "labeler-3":
        return [
            "Filesystem isolation is self-attested; no independent access log was available.",
            "The original attestation did not record a machine-readable model or context identifier.",
        ]
    if role == "adjudicator":
        return [
            "No human reviewer was available.",
            "Filesystem isolation is self-attested; no independent access log was available.",
        ]
    raise ValueError(f"{role}: source attestation does not identify limitations")


def canonical_attestation(role: str, config: dict) -> tuple[Path, dict]:
    source_path = CLOUD / config["source"]
    source = json.loads(source_path.read_text(encoding="utf-8"))
    output_path = CANONICAL / config["output"]
    document = {
        "schema_version": "v2",
        "role": role,
        "context_id": config["context_id"],
        "model_id": config["model_id"],
        "model_family": config["model_family"],
        "cloud_branch": config["cloud_branch"],
        "cloud_commit": config["cloud_commit"],
        "files_read": source_files(role, source),
        "limitations": source_limitations(role, source),
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
    return output_path, document


def decision_snapshot(cases: list[dict]) -> str:
    snapshot = deepcopy(cases)
    turn_container = "turn_labels" if "turn_labels" in snapshot[0] else "turn_adjudications"
    for case in snapshot:
        for turn in case[turn_container]:
            decision = turn if turn_container == "turn_labels" else turn["adjudicated_turn"]
            decision["gold_quality"].pop("tier")
    return json.dumps(snapshot, sort_keys=True)


def normalize_quality_tiers(cases: list[dict]) -> None:
    turn_container = "turn_labels" if "turn_labels" in cases[0] else "turn_adjudications"
    for case in cases:
        for turn in case[turn_container]:
            decision = turn if turn_container == "turn_labels" else turn["adjudicated_turn"]
            if decision["gold_quality"]["tier"] == "gold":
                decision["gold_quality"]["tier"] = "heterogeneous_adjudicated"


def main() -> None:
    CANONICAL.mkdir(parents=True, exist_ok=True)
    for name in ("cases", "oracle-notes"):
        source_path = CLOUD / f"{name}-envelope.json"
        target_path = CLOUD / f"{name}.json"
        target_path.write_bytes(source_path.read_bytes())
    generated = {
        role: canonical_attestation(role, config)
        for role, config in ATTESTATIONS.items()
    }

    gold_path = CLOUD / "gold.json"
    gold = json.loads(gold_path.read_text(encoding="utf-8"))
    gold_decisions_before = decision_snapshot(gold["cases"])
    normalize_quality_tiers(gold["cases"])
    gold["gold_quality"]["labeler_model_families"] = [
        ATTESTATIONS[f"labeler-{index}"]["model_family"] for index in range(1, 4)
    ]
    gold["gold_quality"]["adjudicator_model_family"] = ATTESTATIONS["adjudicator"][
        "model_family"
    ]
    gold["gold_quality"]["attestations"] = [
        {
            "role": role,
            "path": relative(generated[role][0]),
            "sha256": digest(generated[role][0]),
        }
        for role in ("labeler-1", "labeler-2", "labeler-3", "adjudicator")
    ]
    if decision_snapshot(gold["cases"]) != gold_decisions_before:
        raise RuntimeError("normalization changed adjudicated gold decisions")
    gold_path.write_text(json.dumps(gold, indent=2) + "\n", encoding="utf-8")

    adjudication_path = CLOUD / "adjudication.json"
    adjudication = json.loads(adjudication_path.read_text(encoding="utf-8"))
    adjudicated_decisions_before = decision_snapshot(adjudication["cases"])
    normalize_quality_tiers(adjudication["cases"])
    adjudicator_path = generated["adjudicator"][0]
    adjudication["adjudicator_attestation"] = {
        "path": relative(adjudicator_path),
        "sha256": digest(adjudicator_path),
    }
    if decision_snapshot(adjudication["cases"]) != adjudicated_decisions_before:
        raise RuntimeError("normalization changed adjudication decisions")
    adjudication_path.write_text(
        json.dumps(adjudication, indent=2) + "\n", encoding="utf-8"
    )
    print(
        "normalized five attestations and quality-tier names; "
        "gold and adjudication decisions unchanged"
    )


if __name__ == "__main__":
    main()
