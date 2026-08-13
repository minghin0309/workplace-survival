import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
V3_DIR = ROOT / "tests/benchmark/v3"
sys.path.insert(0, str(V3_DIR))

import score_semantic_v3


BASE = ROOT / "tests/benchmark/v3-holdout"
CLOUD = BASE / "cloud-cases"
ATTESTATIONS = CLOUD / "attestations"
SOURCES = {
    "labeler-1": {
        "path": "gold-labeler-1-attestation.json",
        "context_id": "bc-2e9cf5a8-2026-520e-a714-1cda60c5696c",
        "model_family": "grok",
        "branch": "cursor/blind-v3-holdout-gold-labeler-1-696c",
        "commit": "afd564476f434cafb20a99799ff1b5dc877e512b",
    },
    "labeler-2": {
        "path": "gold-labeler-2-clean-attestation.json",
        "context_id": "bc-b0b46ffc-6a40-57cc-9e19-fe203c39480a",
        "model_family": "kimi",
        "branch": "cursor/gold-labeler-2-clean-v3-480a",
        "commit": "c266f11ef135156d03918852cc4d1a67d935caa9",
    },
    "labeler-3": {
        "path": "gold-labeler-3-attestation.json",
        "context_id": "bc-b7e9cb2b-4f3f-506e-a3e2-8a033b14708c",
        "model_family": "gpt",
        "branch": "cursor/gold-labeler-3-v3-holdout-708c",
        "commit": "0e5e6d8cd32370ee34d8a4e731564b565940c645",
    },
    "adjudicator": {
        "path": "adjudicator-v3-raw-attestation.json",
        "context_id": "bc-e03a992e-7ce2-50cf-a4ac-d1440189ee32",
        "model_family": "claude",
        "branch": "cursor/gold-v3-adjudication-ee32",
        "commit": "5add12b6d5c0e51365e000fed857490e879fa265",
    },
    "designer": {
        "path": "designer-attestation.json",
        "context_id": "bc-c754fd78-d593-5672-8209-b43b2396d463",
        "model_family": "claude",
        "branch": "cursor/v3-holdout-cloud-cases-d463",
        "commit": "b7507a2de1277be12e3a3badc221827f658bd3da",
    },
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def normalized_reads(source: dict) -> list[dict]:
    values = source.get("files_read") or source.get("exact_reads") or []
    reads = []
    for item in values:
        path = item.get("path") or item.get("opened_path")
        if path and item.get("sha256"):
            reads.append({"path": path, "sha256": item["sha256"]})
    return reads


def write_wrapper(role: str, config: dict) -> Path:
    source_path = CLOUD / config["path"]
    source = json.loads(source_path.read_text(encoding="utf-8"))
    limitations = source.get("limitations", [])
    if not isinstance(limitations, list):
        limitations = [str(limitations)]
    path = ATTESTATIONS / f"{role}.json"
    document = {
        "schema_version": "v3",
        "role": role,
        "context_id": config["context_id"],
        "model_id": "unverified",
        "model_family": config["model_family"],
        "cloud_branch": config["branch"],
        "cloud_commit": config["commit"],
        "files_read": normalized_reads(source),
        "limitations": limitations
        + [
            "Machine model identity was unavailable; no model ID was guessed.",
            "Transcript audit disposition is frozen in gold-protocol-audits.json.",
        ],
        "source_attestation": {
            "path": relative(source_path),
            "sha256": digest(source_path),
        },
    }
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    return path


def canonical_turn(turn: dict) -> dict:
    return {
        "turn_index": turn["turn_index"],
        "route": turn["route"],
        "responsibility": turn["responsibility"],
        "tone": turn["tone"],
        "overall": turn["overall"],
        "required_question_concepts": turn.get(
            "required_question_concepts", turn.get("required_question_topics", [])
        ),
        "allowed_question_concepts": turn.get(
            "allowed_question_concepts", turn.get("allowed_question_topics", [])
        ),
        "required_revision_concepts": turn.get(
            "required_revision_concepts", turn.get("required_revision_facts", [])
        ),
        "allowed_revision_concepts": turn.get(
            "allowed_revision_concepts", turn.get("allowed_revision_facts", [])
        ),
        "concept_definitions": turn["concept_definitions"],
        "critical_invariants": turn["critical_invariants"],
        "rationale": turn["rationale"],
        "gold_quality": turn["gold_quality"],
    }


def main() -> None:
    ATTESTATIONS.mkdir(parents=True, exist_ok=True)
    wrappers = {
        role: write_wrapper(role, config) for role, config in SOURCES.items()
    }
    raw_path = CLOUD / "gold-v3-raw.json"
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    gold = {
        "schema_version": "v3",
        "artifact": "adjudicated-gold",
        "case_set_id": "v3-holdout-cloud-cases",
        "gold_quality": {
            "labeler_model_families": ["grok", "kimi", "gpt"],
            "adjudicator_model_family": "claude",
            "human_review_available": False,
            "adjudication_complete": True,
            "vote_distributions_preserved": True,
            "attestations": [
                {
                    "role": role,
                    "path": relative(wrappers[role]),
                    "sha256": digest(wrappers[role]),
                }
                for role in ("labeler-1", "labeler-2", "labeler-3", "adjudicator")
            ],
        },
        "cases": [
            {
                "case_id": case["case_id"],
                "turn_labels": [canonical_turn(turn) for turn in case["turn_labels"]],
            }
            for case in raw["cases"]
        ],
    }
    gold_path = CLOUD / "gold-v3.json"
    gold_path.write_text(json.dumps(gold, indent=2) + "\n", encoding="utf-8")

    facts = score_semantic_v3.coverage_facts(gold)
    failures = []
    try:
        score_semantic_v3.validate_coverage(facts)
        status = "VALID_COVERAGE"
    except score_semantic_v3.CoverageError as error:
        status = "INVALID_COVERAGE"
        failures = str(error).removeprefix("coverage gates failed: ").split(", ")
    report = {
        "schema_version": "v3",
        "artifact": "pre-sut-coverage-report",
        "status": status,
        "gold": {"path": relative(gold_path), "sha256": digest(gold_path)},
        "coverage": facts,
        "minimums": {
            "required_question_concepts": 3,
            "required_question_cases": 3,
            "required_revision_concepts": 3,
            "required_revision_cases": 3,
            "accepted_turns": 1,
            "maximum_gold_uncertain_rate": 0.20,
        },
        "failed_gates": failures,
        "sut_execution_authorized": status == "VALID_COVERAGE",
        "limitations": [
            "Coverage is evaluated from adjudicated gold before any SUT execution.",
            "Coverage failure is a benchmark design outcome, not a Skill failure.",
        ],
    }
    (CLOUD / "coverage-report-v3.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(f"finalized v3 gold: {status}")


if __name__ == "__main__":
    main()
