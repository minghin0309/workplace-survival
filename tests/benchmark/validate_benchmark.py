import hashlib
import json
import re
import sys
from pathlib import Path


CASE_KEYS = {
    "case_id",
    "category",
    "recipient_context",
    "data_a",
    "turns",
    "image_spec",
}
TURN_REQUIRED_KEYS = {"turn_index", "input_raw"}
TURN_OPTIONAL_KEYS = {"image_path"}
NOTE_KEYS = {"case_id", "design_intent", "difficulty_notes"}
QUALITY_TIERS = {"human_reviewed", "heterogeneous_adjudicated", "gold_uncertain"}
STAGE_ROLES = {
    "gold": {
        "cases",
        "oracle-notes",
        "gold",
        "adjudication",
        "ontology",
        "scorer",
        "validator",
        "runtime-manifest",
        "labeler-1",
        "labeler-2",
        "labeler-3",
        "labeler-1-attestation",
        "labeler-2-attestation",
        "labeler-3-attestation",
        "designer-attestation",
        "adjudicator-attestation",
    },
    "outputs": {"outputs", "generator-attestation"},
    "evaluations": {
        "evaluations",
        "matches",
        "evaluator-attestation",
        "matcher-attestation",
    },
}
PREVIOUS_STAGE = {"outputs": "gold", "evaluations": "outputs"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unwrap_document(document: object, collection_key: str) -> list[dict]:
    if isinstance(document, list):
        return document
    require(
        isinstance(document, dict)
        and set(document) == {"schema_version", "case_set_id", collection_key}
        and document["schema_version"] == "v2"
        and isinstance(document[collection_key], list),
        f"{collection_key} envelope schema",
    )
    return document[collection_key]


def validate_cases(cases: list[dict], notes: list[dict]) -> None:
    case_ids = [item["case_id"] for item in cases]
    require(len(case_ids) == len(set(case_ids)), "duplicate case IDs")
    require([item["case_id"] for item in notes] == case_ids, "oracle-note coverage")
    for case, note in zip(cases, notes):
        require(set(case) == CASE_KEYS, f"{case['case_id']}: case schema")
        require("case_designer_notes" not in case, f"{case['case_id']}: leaked designer notes")
        require(isinstance(case["recipient_context"], str), f"{case['case_id']}: recipient context")
        require(
            isinstance(case["data_a"], (str, dict)) and bool(case["data_a"]),
            f"{case['case_id']}: Data A",
        )
        require(isinstance(case["turns"], list) and case["turns"], f"{case['case_id']}: turns")
        for index, turn in enumerate(case["turns"], start=1):
            require(
                TURN_REQUIRED_KEYS <= set(turn)
                and set(turn) <= TURN_REQUIRED_KEYS | TURN_OPTIONAL_KEYS,
                f"{case['case_id']}: turn schema",
            )
            require(turn["turn_index"] == index, f"{case['case_id']}: turn order")
            require(isinstance(turn["input_raw"], str) and turn["input_raw"], f"{case['case_id']}: input")
        require(set(note) == NOTE_KEYS, f"{case['case_id']}: oracle-note schema")
        require(
            all(isinstance(note[field], str) and note[field] for field in NOTE_KEYS - {"case_id"}),
            f"{case['case_id']}: oracle-note value",
        )


def validate_gold(gold: dict) -> None:
    quality = gold["gold_quality"]
    require(
        set(quality)
        == {
            "labeler_model_families",
            "adjudicator_model_family",
            "human_review_available",
            "adjudication_complete",
            "vote_distributions_preserved",
            "attestations",
        },
        "gold quality schema",
    )
    families = quality["labeler_model_families"]
    require(len(set(families)) >= 3, "gold requires three model families")
    require(quality["adjudicator_model_family"] not in set(families), "adjudicator not independent")
    require(isinstance(quality["human_review_available"], bool), "human-review flag")
    require(quality["adjudication_complete"] is True, "adjudication incomplete")
    require(quality["vote_distributions_preserved"] is True, "vote distributions missing")
    attestations = quality["attestations"]
    require(isinstance(attestations, list) and len(attestations) >= 4, "gold attestations missing")
    seen_attestations = set()
    roles = set()
    attestation_documents = {}
    for item in attestations:
        require(set(item) == {"role", "path", "sha256"}, "attestation schema")
        require(item["role"] not in roles, "duplicate attestation role")
        roles.add(item["role"])
        path = Path(item["path"])
        require(path.is_file() and path not in seen_attestations, "attestation path")
        seen_attestations.add(path)
        require(
            re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) is not None
            and digest(path) == item["sha256"],
            "attestation hash",
        )
        document = json.loads(path.read_text(encoding="utf-8"))
        attestation_documents[item["role"]] = document
        require(
            all(
                key in document
                for key in (
                    "context_id",
                    "model_id",
                    "model_family",
                    "cloud_branch",
                    "cloud_commit",
                    "files_read",
                    "limitations",
                )
            ),
            "attestation content",
        )
        require(
            re.fullmatch(r"[0-9a-f]{40}", document["cloud_commit"]) is not None
            and isinstance(document["files_read"], list)
            and isinstance(document["limitations"], list),
            "attestation provenance",
        )
        source = document.get("source_attestation")
        if source is not None:
            require(set(source) == {"path", "sha256"}, "source attestation schema")
            source_path = Path(source["path"])
            require(
                source_path.is_file()
                and re.fullmatch(r"[0-9a-f]{64}", source["sha256"]) is not None
                and digest(source_path) == source["sha256"],
                "source attestation hash",
            )
        require(
            all("oracle-notes" not in str(value) for value in document["files_read"]),
            "gold labeler accessed oracle notes",
        )
    require(
        {"labeler-1", "labeler-2", "labeler-3", "adjudicator"} <= roles,
        "required gold attestation roles missing",
    )
    for index, family in enumerate(families, start=1):
        require(
            attestation_documents[f"labeler-{index}"]["model_family"] == family,
            "labeler attestation family mismatch",
        )
    require(
        attestation_documents["adjudicator"]["model_family"]
        == quality["adjudicator_model_family"],
        "adjudicator attestation family mismatch",
    )
    uncertain = total = 0
    for case in gold["cases"]:
        for turn in case["turn_labels"]:
            total += 1
            turn_quality = turn["gold_quality"]
            tier = turn_quality["tier"]
            require(tier in QUALITY_TIERS, f"{case['case_id']}: quality tier")
            require(
                isinstance(turn_quality["unresolved_adjudication"], bool),
                f"{case['case_id']}: unresolved adjudication flag",
            )
            if tier == "human_reviewed":
                require(turn_quality["human_reviewed"] is True, f"{case['case_id']}: human tier")
                require(
                    turn_quality["unresolved_adjudication"] is False,
                    f"{case['case_id']}: unresolved human review",
                )
            if tier == "heterogeneous_adjudicated":
                require(turn_quality["human_reviewed"] is False, f"{case['case_id']}: heterogeneous tier")
                require(
                    turn_quality["unresolved_adjudication"] is False,
                    f"{case['case_id']}: unresolved adjudication",
                )
            if turn_quality["unresolved_adjudication"]:
                require(tier == "gold_uncertain", f"{case['case_id']}: unresolved tier")
            if (
                turn_quality["three_way_categorical_disagreement"]
                or turn_quality["critical_invariant_disagreement"]
            ) and not turn_quality["human_reviewed"]:
                require(tier == "gold_uncertain", f"{case['case_id']}: uncertain gold")
            uncertain += int(tier == "gold_uncertain")
    require(total > 0 and uncertain / total <= 0.20, "gold uncertainty exceeds 20%")


def validate_adjudication(adjudication: dict, gold: dict) -> None:
    require(
        set(adjudication)
        == {
            "schema_version",
            "artifact",
            "case_set_id",
            "gold_output_path",
            "adjudicator_attestation",
            "source_hashes",
            "adjudication_policy",
            "summary",
            "cases",
        },
        "adjudication schema",
    )
    require(
        adjudication["schema_version"] == "v2"
        and adjudication["artifact"] == "gold-adjudication"
        and adjudication["case_set_id"] == gold["case_set_id"],
        "adjudication identity",
    )
    attestation = adjudication["adjudicator_attestation"]
    require(set(attestation) == {"path", "sha256"}, "adjudicator attestation schema")
    attestation_path = Path(attestation["path"])
    require(
        attestation_path.is_file()
        and digest(attestation_path) == attestation["sha256"],
        "adjudicator attestation hash",
    )
    source_hashes = adjudication["source_hashes"]
    require(isinstance(source_hashes, dict) and source_hashes, "adjudication sources")
    for path_text, expected_hash in source_hashes.items():
        path = Path(path_text)
        require(
            path.is_file()
            and re.fullmatch(r"[0-9a-f]{64}", expected_hash) is not None
            and digest(path) == expected_hash,
            f"adjudication source changed: {path}",
        )

    gold_cases = {case["case_id"]: case["turn_labels"] for case in gold["cases"]}
    adjudicated_cases = adjudication["cases"]
    require(
        [case["case_id"] for case in adjudicated_cases] == list(gold_cases),
        "adjudication case coverage",
    )
    turn_count = uncertain_count = 0
    for case in adjudicated_cases:
        case_id = case["case_id"]
        turn_adjudications = case["turn_adjudications"]
        expected_turns = gold_cases[case_id]
        require(len(turn_adjudications) == len(expected_turns), f"{case_id}: adjudication turn coverage")
        for expected_index, (turn, expected_gold) in enumerate(
            zip(turn_adjudications, expected_turns), start=1
        ):
            require(turn["turn_index"] == expected_index, f"{case_id}: adjudication turn order")
            require(
                set(turn["labeler_votes"]) == {"gold-labeler-1", "gold-labeler-2", "gold-labeler-3"},
                f"{case_id}: labeler vote coverage",
            )
            for field in ("route", "responsibility", "tone", "overall"):
                distribution = turn["categorical_vote_distribution"][field]
                require(
                    sum(distribution.values()) == 3,
                    f"{case_id}: {field} vote distribution",
                )
            require(
                turn["adjudicated_turn"] == expected_gold,
                f"{case_id}: adjudicated gold linkage",
            )
            turn_count += 1
            uncertain_count += int(expected_gold["gold_quality"]["tier"] == "gold_uncertain")
    summary = adjudication["summary"]
    require(
        summary["turns"] == turn_count
        and summary["uncertain_turn_count"] == uncertain_count
        and summary["uncertain_fraction"] == uncertain_count / turn_count,
        "adjudication summary",
    )


def validate_manifest(manifest: dict, seen: set[Path] | None = None) -> None:
    if seen is None:
        seen = set()
    require(
        isinstance(manifest, dict)
        and set(manifest)
        == {
            "version",
            "immutable",
            "stage",
            "parent_manifest",
            "frozen_at_utc",
            "artifacts",
        },
        "manifest schema",
    )
    require(manifest["version"] == "2", "manifest version")
    require(manifest["immutable"] is True, "manifest must be immutable")
    stage = manifest["stage"]
    require(stage in STAGE_ROLES, "manifest stage")
    parent = manifest["parent_manifest"]
    require(set(parent) == {"path", "sha256"}, "parent manifest schema")
    if parent["path"] is None:
        require(stage == "gold" and parent["sha256"] == "0" * 64, "invalid genesis parent")
    else:
        parent_path = Path(parent["path"])
        require(parent_path.is_file() and parent_path not in seen, "parent manifest missing or cyclic")
        seen.add(parent_path)
        require(digest(parent_path) == parent["sha256"], "parent manifest changed")
        parent_document = json.loads(parent_path.read_text(encoding="utf-8"))
        validate_manifest(parent_document, seen)
        require(
            parent_document["stage"] == PREVIOUS_STAGE[stage],
            "invalid manifest stage order",
        )
    roles = set()
    for entry in manifest["artifacts"]:
        require(
            set(entry) == {"role", "path", "sha256", "cloud_branch", "cloud_commit"},
            "artifact schema",
        )
        require(entry["role"] not in roles, "duplicate artifact role")
        roles.add(entry["role"])
        path = Path(entry["path"])
        require(path.is_file(), f"missing artifact: {path}")
        require(digest(path) == entry["sha256"], f"artifact changed: {path}")
        require(
            isinstance(entry["cloud_branch"], str)
            and isinstance(entry["cloud_commit"], str)
            and re.fullmatch(r"[0-9a-f]{40}", entry["cloud_commit"]) is not None,
            f"cloud provenance missing: {path}",
        )
        if entry["role"].endswith("-attestation"):
            document = json.loads(path.read_text(encoding="utf-8"))
            require(
                all(
                    key in document
                    for key in (
                        "context_id",
                        "model_id",
                        "model_family",
                        "cloud_branch",
                        "cloud_commit",
                        "files_read",
                        "limitations",
                    )
                ),
                f"{entry['role']}: attestation content",
            )
            require(
                document["cloud_branch"] == entry["cloud_branch"]
                and document["cloud_commit"] == entry["cloud_commit"],
                f"{entry['role']}: attestation provenance mismatch",
            )
            if entry["role"] in {"generator-attestation", "evaluator-attestation"}:
                require(
                    all(
                        all(
                            token not in str(value)
                            for token in ("gold", "oracle-notes", "score")
                        )
                        for value in document["files_read"]
                    ),
                    f"{entry['role']}: prohibited file access",
                )
    require(STAGE_ROLES[stage] <= roles, "required artifact roles missing")
    if stage == "gold":
        cases_entry = next(item for item in manifest["artifacts"] if item["role"] == "cases")
        cases_document = json.loads(Path(cases_entry["path"]).read_text(encoding="utf-8"))
        cases = unwrap_document(cases_document, "cases")
        expected_images = {
            f"image:{case['case_id']}:{turn['turn_index']}": turn["image_path"]
            for case in cases
            for turn in case["turns"]
            if turn.get("image_path") is not None
        }
        actual_images = {
            item["role"]: item["path"]
            for item in manifest["artifacts"]
            if item["role"].startswith("image:")
        }
        require(actual_images == expected_images, "gold image artifact coverage mismatch")


def find_gold_manifest(manifest: dict) -> dict:
    current = manifest
    while current["stage"] != "gold":
        current = json.loads(
            Path(current["parent_manifest"]["path"]).read_text(encoding="utf-8")
        )
    return current


def main() -> None:
    if len(sys.argv) != 5:
        raise SystemExit(
            "usage: validate_benchmark.py <cases.json> <oracle-notes.json> "
            "<gold.json> <artifact-manifest.json>"
        )
    cases_document = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    notes_document = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    cases = unwrap_document(cases_document, "cases")
    notes = unwrap_document(notes_document, "notes")
    gold = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
    manifest = json.loads(Path(sys.argv[4]).read_text(encoding="utf-8"))
    validate_cases(cases, notes)
    validate_gold(gold)
    validate_manifest(manifest)
    gold_manifest = find_gold_manifest(manifest)
    by_role = {item["role"]: item for item in gold_manifest["artifacts"]}
    adjudication_path = Path(by_role["adjudication"]["path"])
    adjudication = json.loads(adjudication_path.read_text(encoding="utf-8"))
    validate_adjudication(adjudication, gold)
    expected_paths = {
        "cases": Path(sys.argv[1]).resolve(),
        "oracle-notes": Path(sys.argv[2]).resolve(),
        "gold": Path(sys.argv[3]).resolve(),
    }
    for role, path in expected_paths.items():
        require(
            Path(by_role[role]["path"]).resolve() == path
            and by_role[role]["sha256"] == digest(path),
            f"validated {role} is not the frozen artifact",
        )
    print(f"validated benchmark v2: {len(cases)} cases")


if __name__ == "__main__":
    main()
