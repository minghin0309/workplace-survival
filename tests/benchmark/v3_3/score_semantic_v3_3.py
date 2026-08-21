#!/usr/bin/env python3
"""Benchmark v3.3 scorer: v3.2 freeze-chain plus H-001/H-003 revision scoring."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


BENCHMARK_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BENCHMARK_DIR))

import score_semantic as v2_scorer


VERSION = "3.3"
ACCEPTED_MANIFEST_VERSIONS = {"3.1", "3.2", "3.3"}
NO_REVISION_CONCEPT = "no-revision"
IMPLICIT_PRESERVE_RECIPIENT = "preserve-intended-recipient"
MIN_REQUIRED_CONCEPTS = 3
MIN_REQUIRED_CASES = 3
REQUIRED_MANIFEST_KEYS = {
    "version",
    "immutable",
    "stage",
    "frozen_at_utc",
    "artifacts",
}
ARTIFACT_REQUIRED_KEYS = {
    "role",
    "path",
    "sha256",
    "cloud_branch",
    "cloud_commit",
}
PARENT_STAGES = {"evaluations": "outputs", "outputs": "gold"}
REQUIRED_ROLES = {
    "gold": {"gold", "ontology", "scorer"},
    "outputs": {"outputs"},
    "evaluations": {"evaluations", "matches"},
}
THRESHOLDS = {
    "route_accuracy": (">=", 0.95),
    "responsibility_accuracy": (">=", 0.90),
    "tone_accuracy": (">=", 0.90),
    "overall_accuracy": (">=", 0.90),
    "required_question_concept_recall": (">=", 0.90),
    "question_claim_support_precision": ("=", 1.0),
    "required_revision_concept_recall": (">=", 0.90),
    "revision_claim_support_precision": ("=", 1.0),
    "critical_invariant_violations": ("=", 0),
    "gold_uncertain_rate": ("<=", 0.20),
}


class CoverageError(ValueError):
    pass


class FreezeChainError(ValueError):
    pass


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_chain(condition: bool, message: str) -> None:
    if not condition:
        raise FreezeChainError(message)


def metric(numerator: int, denominator: int) -> dict:
    if denominator == 0:
        return {
            "value": None,
            "numerator": numerator,
            "denominator": denominator,
            "status": "NOT_APPLICABLE",
        }
    return {
        "value": numerator / denominator,
        "numerator": numerator,
        "denominator": denominator,
        "status": "EVALUATED",
    }


def scored_required_revisions(concepts: list[str] | set[str]) -> set[str]:
    return set(concepts) - {IMPLICIT_PRESERVE_RECIPIENT}


def credit_empty_no_revision(
    expected: dict, actual: dict, revision_claims: list, revision_matched: set[str]
) -> set[str]:
    credited = set(revision_matched)
    if (
        NO_REVISION_CONCEPT in expected["required_revision_concepts"]
        and not revision_claims
        and expected.get("responsibility") == "Green"
        and expected.get("tone") == "Green"
        and actual.get("responsibility") == "Green"
        and actual.get("tone") == "Green"
    ):
        credited.add(NO_REVISION_CONCEPT)
    return credited


def count_concept_coverage(gold: dict, field: str) -> tuple[int, int]:
    total = 0
    cases = 0
    for case in gold["cases"]:
        if field == "required_revision_concepts":
            case_total = sum(
                len(scored_required_revisions(turn[field]))
                for turn in case["turn_labels"]
            )
        else:
            case_total = sum(len(turn[field]) for turn in case["turn_labels"])
        total += case_total
        cases += int(case_total > 0)
    return total, cases


def coverage_facts(gold: dict) -> dict:
    question_total, question_cases = count_concept_coverage(
        gold, "required_question_concepts"
    )
    revision_total, revision_cases = count_concept_coverage(
        gold, "required_revision_concepts"
    )
    turns = [turn for case in gold["cases"] for turn in case["turn_labels"]]
    uncertain = sum(
        turn["gold_quality"]["tier"] == "gold_uncertain" for turn in turns
    )
    return {
        "turns": len(turns),
        "accepted_turns": len(turns) - uncertain,
        "gold_uncertain_turns": uncertain,
        "gold_uncertain_rate": None if not turns else uncertain / len(turns),
        "required_question_concepts": question_total,
        "required_question_cases": question_cases,
        "required_revision_concepts": revision_total,
        "required_revision_cases": revision_cases,
    }


def validate_coverage(facts: dict) -> None:
    failures = []
    for domain in ("question", "revision"):
        if facts[f"required_{domain}_concepts"] < MIN_REQUIRED_CONCEPTS:
            failures.append(f"required_{domain}_concepts")
        if facts[f"required_{domain}_cases"] < MIN_REQUIRED_CASES:
            failures.append(f"required_{domain}_cases")
    if facts["accepted_turns"] < 1:
        failures.append("accepted_turns")
    if facts["gold_uncertain_rate"] is None or facts["gold_uncertain_rate"] > 0.20:
        failures.append("gold_uncertain_rate")
    if failures:
        raise CoverageError("coverage gates failed: " + ", ".join(failures))


def threshold_pass(value: float | int, operator: str, target: float | int) -> bool:
    if operator == ">=":
        return value >= target
    if operator == "<=":
        return value <= target
    if operator == "=":
        return value == target
    raise ValueError(f"unknown threshold operator: {operator}")


def metric_records(report: dict) -> dict[str, dict]:
    totals = report["totals"]
    records = {
        "route_accuracy": metric(totals["route"], totals["accepted_turns"]),
        "responsibility_accuracy": metric(
            totals["rating_correct"]["responsibility"],
            totals["rated"]["responsibility"],
        ),
        "tone_accuracy": metric(
            totals["rating_correct"]["tone"], totals["rated"]["tone"]
        ),
        "overall_accuracy": metric(
            totals["rating_correct"]["overall"], totals["rated"]["overall"]
        ),
        "required_question_concept_recall": metric(
            totals["required_questions_hit"], totals["required_questions"]
        ),
        "question_claim_support_precision": metric(
            totals["question_claims"] - totals["unsupported_question_claims"],
            totals["question_claims"],
        ),
        "required_revision_concept_recall": metric(
            totals["required_revisions_hit"], totals["required_revisions"]
        ),
        "revision_claim_support_precision": metric(
            totals["revision_claims"] - totals["unsupported_revision_claims"],
            totals["revision_claims"],
        ),
        "critical_invariant_violations": {
            "value": totals["critical_violations"],
            "numerator": totals["critical_violations"],
            "denominator": totals["accepted_turns"],
            "status": "EVALUATED",
        },
        "gold_uncertain_rate": metric(
            totals["uncertain_turns"],
            totals["accepted_turns"] + totals["uncertain_turns"],
        ),
    }
    for name, record in records.items():
        operator, target = THRESHOLDS[name]
        record["threshold"] = {"operator": operator, "target": target}
        record["threshold_status"] = (
            "NOT_APPLICABLE"
            if record["status"] == "NOT_APPLICABLE"
            else (
                "PASS"
                if threshold_pass(record["value"], operator, target)
                else "FAIL"
            )
        )
    return records


def input_hashes(paths: list[Path]) -> list[dict]:
    return [
        {
            "path": str(path),
            "sha256": digest(path) if path.is_file() else None,
            "exists": path.is_file(),
        }
        for path in paths
    ]


def write_json_once(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"refusing to overwrite score report: {path}")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(document, handle, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def failure_envelope(
    *,
    status: str,
    executed_at: str,
    attempt_id: str,
    arguments: list[str],
    inputs: list[Path],
    stage: str,
    error: Exception,
    coverage: dict | None,
) -> dict:
    return {
        "schema_version": "v3.3",
        "scorer_version": VERSION,
        "status": status,
        "executed_at_utc": executed_at,
        "attempt_id": attempt_id,
        "rerun_performed": False,
        "arguments": arguments,
        "scorer_sha256": digest(Path(__file__)),
        "frozen_inputs": input_hashes(inputs),
        "failure": {
            "stage": stage,
            "type": type(error).__name__,
            "message": str(error),
        },
        "coverage": coverage,
        "metrics": None,
        "case_results": None,
        "limitations": [
            "This immutable envelope records a failed scorer invocation.",
            "No result from another benchmark version is repaired or replaced.",
        ],
    }


def validate_artifact(entry: dict) -> None:
    require_chain(
        ARTIFACT_REQUIRED_KEYS <= set(entry),
        "artifact schema",
    )
    require_chain(
        isinstance(entry["cloud_branch"], str)
        and isinstance(entry["cloud_commit"], str)
        and re.fullmatch(r"[0-9a-f]{40}", entry["cloud_commit"]) is not None,
        "cloud provenance missing",
    )
    path = Path(entry["path"])
    require_chain(path.is_file(), f"missing artifact: {path}")
    require_chain(
        re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]) is not None
        and digest(path) == entry["sha256"],
        f"artifact changed: {path}",
    )


def validate_manifest(manifest: dict, expected_stage: str, seen: set[Path] | None = None) -> None:
    if seen is None:
        seen = set()
    require_chain(isinstance(manifest, dict), "manifest schema")
    require_chain(REQUIRED_MANIFEST_KEYS <= set(manifest), "manifest schema")
    require_chain(
        manifest["version"] in ACCEPTED_MANIFEST_VERSIONS,
        "manifest version",
    )
    require_chain(manifest["immutable"] is True, "manifest must be immutable")
    require_chain(manifest["stage"] == expected_stage, "manifest stage")
    roles = set()
    for entry in manifest["artifacts"]:
        validate_artifact(entry)
        require_chain(entry["role"] not in roles, "duplicate artifact role")
        roles.add(entry["role"])
    require_chain(
        REQUIRED_ROLES[expected_stage] <= roles,
        "required artifact roles missing: "
        + ", ".join(sorted(REQUIRED_ROLES[expected_stage] - roles)),
    )
    if expected_stage == "gold":
        return
    require_chain("parent_manifest" in manifest, "parent manifest missing")
    parent = manifest["parent_manifest"]
    require_chain(
        isinstance(parent, dict) and {"path", "sha256"} <= set(parent),
        "parent manifest schema",
    )
    parent_path = Path(parent["path"])
    require_chain(
        parent_path.is_file() and parent_path not in seen,
        "parent manifest missing or cyclic",
    )
    seen.add(parent_path)
    require_chain(digest(parent_path) == parent["sha256"], "parent manifest changed")
    parent_document = json.loads(parent_path.read_text(encoding="utf-8"))
    validate_manifest(parent_document, PARENT_STAGES[expected_stage], seen)


def role_map(manifest: dict) -> dict[str, Path]:
    return {item["role"]: Path(item["path"]).resolve() for item in manifest["artifacts"]}


def load_parent(manifest: dict) -> dict:
    return json.loads(Path(manifest["parent_manifest"]["path"]).read_text(encoding="utf-8"))


def validate_freeze_chain(
    evaluation_manifest: dict,
    ontology_path: Path,
    gold_path: Path,
    outputs_path: Path,
    evaluations_path: Path,
    matches_path: Path,
    scorer_path: Path,
) -> None:
    validate_manifest(evaluation_manifest, "evaluations")
    outputs_manifest = load_parent(evaluation_manifest)
    gold_manifest = load_parent(outputs_manifest)
    evaluation_roles = role_map(evaluation_manifest)
    output_roles = role_map(outputs_manifest)
    gold_roles = role_map(gold_manifest)
    require_chain(
        evaluation_roles["evaluations"] == evaluations_path.resolve(),
        "unfrozen evaluations",
    )
    require_chain(
        evaluation_roles["matches"] == matches_path.resolve(),
        "unfrozen matches",
    )
    require_chain(output_roles["outputs"] == outputs_path.resolve(), "unfrozen outputs")
    require_chain(gold_roles["gold"] == gold_path.resolve(), "unfrozen gold")
    require_chain(
        gold_roles["ontology"] == ontology_path.resolve(),
        "unfrozen ontology",
    )
    require_chain(gold_roles["scorer"] == scorer_path.resolve(), "unfrozen scorer")


def empty_totals() -> dict:
    return {
        "accepted_turns": 0,
        "uncertain_turns": 0,
        "route": 0,
        "rated": {"responsibility": 0, "tone": 0, "overall": 0},
        "rating_correct": {"responsibility": 0, "tone": 0, "overall": 0},
        "required_questions": 0,
        "required_questions_hit": 0,
        "question_claims": 0,
        "unsupported_question_claims": 0,
        "required_revisions": 0,
        "required_revisions_hit": 0,
        "revision_claims": 0,
        "unsupported_revision_claims": 0,
        "critical_violations": 0,
    }


def score_turn(
    *,
    case_id: str,
    expected: dict,
    output: dict,
    actual: dict,
    turn_match: dict,
    aliases: dict,
    extractor_contexts: set,
    bucket: dict,
) -> list[str]:
    claim_review = actual["claim_extraction_review"]
    v2_scorer.require(
        set(claim_review)
        == {
            "reviewed_by_context_ids",
            "claim_completeness_reviewed",
            "unresolved_claim_disagreements",
        },
        f"{case_id}: claim extraction review schema",
    )
    v2_scorer.require(
        set(claim_review["reviewed_by_context_ids"]) == extractor_contexts,
        f"{case_id}: incomplete extractor coverage",
    )
    v2_scorer.require(
        claim_review["claim_completeness_reviewed"] is True
        and claim_review["unresolved_claim_disagreements"] == 0,
        f"{case_id}: unresolved claim extraction",
    )
    raw_output = output["raw_output"]
    question_claims = v2_scorer.validate_claims(
        actual["question_claims"], raw_output, f"{case_id}: question"
    )
    revision_claims = v2_scorer.validate_claims(
        actual["revision_claims"], raw_output, f"{case_id}: revision"
    )
    required_questions = set(expected["required_question_concepts"])
    required_revisions = scored_required_revisions(
        expected["required_revision_concepts"]
    )
    question_matched, question_unsupported = v2_scorer.validate_match_set(
        turn_match["question_matches"],
        question_claims,
        "question",
        set(expected["allowed_question_concepts"]),
        aliases,
        f"{case_id}: question",
    )
    revision_matched, revision_unsupported = v2_scorer.validate_match_set(
        turn_match["revision_matches"],
        revision_claims,
        "revision",
        set(expected["allowed_revision_concepts"]),
        aliases,
        f"{case_id}: revision",
    )
    revision_matched = credit_empty_no_revision(
        expected, actual, revision_claims, revision_matched
    )
    invariant_results = actual["critical_invariant_results"]
    applicable = set(expected["critical_invariants"])
    v2_scorer.require(applicable <= set(invariant_results), f"{case_id}: invariant coverage")
    violations = sum(not invariant_results[item] for item in applicable)
    mismatches = []
    route_match = actual["route"] == expected["route"]
    bucket["route"] += int(route_match)
    if not route_match:
        mismatches.append("route")
    for field in ("responsibility", "tone", "overall"):
        if expected[field] is not None:
            bucket["rated"][field] += 1
            same = actual[field] == expected[field]
            bucket["rating_correct"][field] += int(same)
            if not same:
                mismatches.append(field)
    bucket["required_questions"] += len(required_questions)
    bucket["required_questions_hit"] += len(required_questions & question_matched)
    bucket["question_claims"] += len(question_claims)
    bucket["unsupported_question_claims"] += question_unsupported
    bucket["required_revisions"] += len(required_revisions)
    bucket["required_revisions_hit"] += len(required_revisions & revision_matched)
    bucket["revision_claims"] += len(revision_claims)
    bucket["unsupported_revision_claims"] += revision_unsupported
    bucket["critical_violations"] += violations
    if not required_questions <= question_matched:
        mismatches.append("required-question-concepts")
    if question_unsupported:
        mismatches.append("unsupported-question-claims")
    if not required_revisions <= revision_matched:
        mismatches.append("required-revision-concepts")
    if revision_unsupported:
        mismatches.append("unsupported-revision-claims")
    if violations:
        mismatches.append("critical-invariant")
    return mismatches


def run_semantic_core(
    gold_doc: dict,
    outputs_doc: dict,
    evaluations_doc: dict,
    matches_doc: dict,
    aliases: dict,
) -> dict:
    outputs = v2_scorer.unique(outputs_doc["cases"], "case_id", "output case")
    evaluations = v2_scorer.unique(
        evaluations_doc["cases"], "case_id", "evaluation case"
    )
    matches = v2_scorer.unique(matches_doc["cases"], "case_id", "match case")
    gold = v2_scorer.unique(gold_doc["cases"], "case_id", "gold case")
    v2_scorer.require(
        set(gold) == set(outputs) == set(evaluations) == set(matches),
        "case coverage",
    )
    quality = gold_doc["gold_quality"]
    families = quality["labeler_model_families"]
    v2_scorer.require(len(set(families)) >= 3, "fewer than three gold model families")
    v2_scorer.require(
        quality["adjudicator_model_family"] not in set(families),
        "adjudicator not heterogeneous",
    )
    v2_scorer.require(
        isinstance(quality["human_review_available"], bool),
        "human review flag",
    )
    extractors = evaluations_doc["evaluation_quality"]["extractors"]
    v2_scorer.require(
        isinstance(extractors, list) and len(extractors) >= 2,
        "two extractors required",
    )
    extractor_contexts = set()
    extractor_families = set()
    for extractor in extractors:
        v2_scorer.require(
            set(extractor)
            == {
                "context_id",
                "model_id",
                "model_family",
                "attestation_path",
                "attestation_sha256",
            },
            "extractor schema",
        )
        extractor_contexts.add(extractor["context_id"])
        extractor_families.add(extractor["model_family"])
        attestation_path = Path(extractor["attestation_path"])
        v2_scorer.require(attestation_path.is_file(), "extractor attestation missing")
        v2_scorer.require(
            digest(attestation_path) == extractor["attestation_sha256"],
            "extractor attestation hash",
        )
    v2_scorer.require(
        len(extractor_contexts) == len(extractors),
        "extractor contexts not independent",
    )
    v2_scorer.require(
        len(extractor_families) >= 2,
        "claim extraction requires two model families",
    )
    matcher = matches_doc["matcher"]
    v2_scorer.require(matcher["gold_access"] is True, "semantic matcher must compare with gold")
    v2_scorer.require(
        matcher["model_family"] not in set(families),
        "matcher duplicates gold labeler family",
    )
    totals = empty_totals()
    case_results = []
    for case_id, expected_case in gold.items():
        output_turns = outputs[case_id]["turn_outputs"]
        evaluation_turns = evaluations[case_id]["turn_evaluations"]
        match_turns = matches[case_id]["turn_matches"]
        gold_turns = expected_case["turn_labels"]
        v2_scorer.require(
            len(output_turns)
            == len(evaluation_turns)
            == len(match_turns)
            == len(gold_turns),
            f"{case_id}: turn coverage",
        )
        case_mismatches = []
        case_uncertain_turns = 0
        for expected, output, actual, turn_match in zip(
            gold_turns, output_turns, evaluation_turns, match_turns
        ):
            v2_scorer.require(
                expected["turn_index"]
                == output["turn_index"]
                == actual["turn_index"]
                == turn_match["turn_index"],
                f"{case_id}: turn order",
            )
            quality_tier = expected["gold_quality"]["tier"]
            if quality_tier == "gold_uncertain":
                totals["uncertain_turns"] += 1
                case_uncertain_turns += 1
                score_turn(
                    case_id=case_id,
                    expected=expected,
                    output=output,
                    actual=actual,
                    turn_match=turn_match,
                    aliases=aliases,
                    extractor_contexts=extractor_contexts,
                    bucket=empty_totals(),
                )
                continue
            totals["accepted_turns"] += 1
            mismatches = score_turn(
                case_id=case_id,
                expected=expected,
                output=output,
                actual=actual,
                turn_match=turn_match,
                aliases=aliases,
                extractor_contexts=extractor_contexts,
                bucket=totals,
            )
            case_mismatches.extend(
                f"turn {expected['turn_index']}: {value}" for value in mismatches
            )
        case_results.append(
            {
                "case_id": case_id,
                "passed": not case_mismatches,
                "primary_scored": case_uncertain_turns < len(gold_turns),
                "gold_uncertain_turns": case_uncertain_turns,
                "mismatches": case_mismatches,
            }
        )
    return {
        "totals": totals,
        "case_results": case_results,
        "gold_quality": quality,
        "matcher": matcher,
    }


def main() -> None:
    if len(sys.argv) != 8:
        raise SystemExit(
            "usage: score_semantic_v3_3.py <evaluation-manifest.json> <ontology.json> "
            "<gold.json> <outputs.json> <evaluations.json> <matches.json> <report.json>"
        )
    arguments = sys.argv[1:]
    input_paths = [Path(value) for value in arguments[:-1]]
    report_path = Path(arguments[-1])
    if report_path.exists():
        raise FileExistsError(f"refusing to overwrite score report: {report_path}")

    executed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    attempt_id = hashlib.sha256(
        (executed_at + "\0" + "\0".join(arguments)).encode("utf-8")
    ).hexdigest()
    coverage = None
    try:
        (
            manifest_path,
            ontology_path,
            gold_path,
            outputs_path,
            evaluations_path,
            matches_path,
        ) = input_paths
        gold = json.loads(gold_path.read_text(encoding="utf-8"))
        coverage = coverage_facts(gold)
        validate_coverage(coverage)
        evaluation_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        validate_freeze_chain(
            evaluation_manifest,
            ontology_path,
            gold_path,
            outputs_path,
            evaluations_path,
            matches_path,
            Path(__file__),
        )
        _, aliases = v2_scorer.load_ontology(ontology_path)
        core = run_semantic_core(
            gold,
            json.loads(outputs_path.read_text(encoding="utf-8")),
            json.loads(evaluations_path.read_text(encoding="utf-8")),
            json.loads(matches_path.read_text(encoding="utf-8")),
            aliases,
        )
        records = metric_records(core)
        required_not_applicable = [
            name
            for name, record in records.items()
            if record["status"] == "NOT_APPLICABLE"
        ]
        status = (
            "INVALID_SCORING_INPUT" if required_not_applicable else "SCORED"
        )
        report = {
            "schema_version": "v3.3",
            "scorer_version": VERSION,
            "status": status,
            "executed_at_utc": executed_at,
            "attempt_id": attempt_id,
            "rerun_performed": False,
            "arguments": arguments,
            "scorer_sha256": digest(Path(__file__)),
            "frozen_inputs": input_hashes(input_paths),
            "coverage": coverage,
            "metrics": records,
            "thresholds_passed": (
                None
                if required_not_applicable
                else all(
                    record["threshold_status"] == "PASS"
                    for record in records.values()
                )
            ),
            "not_applicable_metrics": required_not_applicable,
            "case_results": core["case_results"],
            "totals": core["totals"],
            "gold_quality": core["gold_quality"],
            "matcher": core["matcher"],
            "limitations": [
                "v3.3 inherits v3.2 freeze-chain validation and does not call v2 main().",
                "Empty Green revision_claims credit required no-revision (H-001).",
                "preserve-intended-recipient is never a scored required revision (H-003).",
                "NOT_APPLICABLE metrics never count as threshold passes.",
                "Archived v2, v3.1, and v3.2 outcomes are not repaired or replaced.",
            ],
        }
        write_json_once(report_path, report)
    except CoverageError as error:
        write_json_once(
            report_path,
            failure_envelope(
                status="INVALID_COVERAGE",
                executed_at=executed_at,
                attempt_id=attempt_id,
                arguments=arguments,
                inputs=input_paths,
                stage="coverage",
                error=error,
                coverage=coverage,
            ),
        )
        raise
    except FreezeChainError as error:
        write_json_once(
            report_path,
            failure_envelope(
                status="INVALID_SCORING_INPUT",
                executed_at=executed_at,
                attempt_id=attempt_id,
                arguments=arguments,
                inputs=input_paths,
                stage="freeze-chain",
                error=error,
                coverage=coverage,
            ),
        )
        raise
    except Exception as error:
        if not report_path.exists():
            write_json_once(
                report_path,
                failure_envelope(
                    status="SCORER_ERROR",
                    executed_at=executed_at,
                    attempt_id=attempt_id,
                    arguments=arguments,
                    inputs=input_paths,
                    stage="scoring",
                    error=error,
                    coverage=coverage,
                ),
            )
        raise


if __name__ == "__main__":
    main()
