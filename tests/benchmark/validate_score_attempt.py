import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLOUD = ROOT / "tests/benchmark/v2-holdout/cloud-cases"
REPORT_PATH = CLOUD / "score-report-v2.json"
TRIAGE_PATH = ROOT / "tests/benchmark/v2-holdout/SCORE_TRIAGE.md"
MANIFEST_PATH = CLOUD / "score-attempt-manifest-v2.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    require(
        report["status"] == "SCORER_ERROR"
        and report["formal_attempt_count"] == 1
        and report["rerun_performed"] is False
        and report["exit_code"] == 1
        and report["error"]
        == {
            "type": "ValueError",
            "message": "metric denominator must be nonzero",
            "location": "tests/benchmark/score_semantic.py:451",
            "metric_being_constructed": "required_question_concept_recall",
        },
        "formal score failure identity",
    )
    frozen_paths = {
        "evaluation_manifest_sha256": CLOUD / "evaluation-manifest-v2.json",
        "ontology_sha256": ROOT / "tests/benchmark/SEMANTIC_ONTOLOGY.json",
        "gold_sha256": CLOUD / "gold-v2.json",
        "outputs_sha256": CLOUD / "outputs-v2-raw.json",
        "evaluations_sha256": CLOUD / "evaluations-v2-canonical.json",
        "matches_sha256": CLOUD / "matches-v2-canonical.json",
        "scorer_sha256": ROOT / "tests/benchmark/score_semantic.py",
    }
    for key, path in frozen_paths.items():
        require(path.is_file() and digest(path) == report["frozen_inputs"][key], key)
    require(
        report["denominator_facts"]
        == {
            "turns": 24,
            "required_question_concepts": 0,
            "required_revision_concepts": 72,
            "gold_uncertain_turns": 1,
            "gold_uncertain_rate": 1 / 24,
        },
        "denominator facts",
    )
    require(
        report["metrics"] is None
        and report["case_results"] is None
        and report["unscored_case_ids"]
        == [f"V2-{index:03d}" for index in range(1, 19)],
        "unscored case preservation",
    )
    threshold_status = {item["metric"]: item["status"] for item in report["thresholds"]}
    require(
        threshold_status["required_question_concept_recall"]
        == "UNDEFINED_ZERO_DENOMINATOR"
        and threshold_status["gold_uncertain_rate"] == "PRE_SCORE_GATE_PASS"
        and all(
            status == "NOT_EVALUATED"
            for metric, status in threshold_status.items()
            if metric
            not in {"required_question_concept_recall", "gold_uncertain_rate"}
        ),
        "threshold disposition",
    )
    triage = TRIAGE_PATH.read_text(encoding="utf-8")
    for label in (
        "Confirmed harness defects",
        "Confirmed Skill defects",
        "Gold ambiguity or coverage",
        "Ontology or matcher findings",
        "Failed and unscored cases",
    ):
        require(label in triage, f"triage section missing: {label}")

    if MANIFEST_PATH.is_file():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        require(
            set(manifest)
            == {
                "version",
                "immutable",
                "stage",
                "parent_evaluation_manifest",
                "frozen_at_utc",
                "artifacts",
            }
            and manifest["version"] == "2"
            and manifest["immutable"] is True
            and manifest["stage"] == "score-attempt",
            "score attempt manifest schema",
        )
        parent = manifest["parent_evaluation_manifest"]
        parent_path = ROOT / parent["path"]
        require(parent_path.is_file() and digest(parent_path) == parent["sha256"], "score parent")
        roles = set()
        for item in manifest["artifacts"]:
            require(
                set(item) == {"role", "path", "sha256", "cloud_branch", "cloud_commit"}
                and item["role"] not in roles
                and re.fullmatch(r"[0-9a-f]{40}", item["cloud_commit"]) is not None,
                "score artifact schema",
            )
            roles.add(item["role"])
            path = ROOT / item["path"]
            require(path.is_file() and digest(path) == item["sha256"], f"score artifact: {path}")
        require(
            roles == {"score-report", "triage", "scorer", "validator", "freezer"},
            "score artifact roles",
        )
    print("validated single formal scorer error and preserved triage")


if __name__ == "__main__":
    main()
