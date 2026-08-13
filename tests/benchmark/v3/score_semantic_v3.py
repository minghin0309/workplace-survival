import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


BENCHMARK_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BENCHMARK_DIR))

import score_semantic as v2_scorer


VERSION = "3"
MIN_REQUIRED_CONCEPTS = 3
MIN_REQUIRED_CASES = 3
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


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def count_concept_coverage(gold: dict, field: str) -> tuple[int, int]:
    total = 0
    cases = 0
    for case in gold["cases"]:
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
    turns = [
        turn for case in gold["cases"] for turn in case["turn_labels"]
    ]
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
    if (
        facts["gold_uncertain_rate"] is None
        or facts["gold_uncertain_rate"] > 0.20
    ):
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
            else ("PASS" if threshold_pass(record["value"], operator, target) else "FAIL")
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
        "schema_version": "v3",
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


def run_v2_core(arguments: list[str], temporary_report: Path) -> dict:
    original_argv = sys.argv
    original_ratio = v2_scorer.ratio
    try:
        v2_scorer.ratio = lambda correct, total: (
            None if total == 0 else correct / total
        )
        sys.argv = [
            str(Path(v2_scorer.__file__)),
            *arguments[:-1],
            str(temporary_report),
        ]
        v2_scorer.main()
        return json.loads(temporary_report.read_text(encoding="utf-8"))
    finally:
        sys.argv = original_argv
        v2_scorer.ratio = original_ratio


def main() -> None:
    if len(sys.argv) != 8:
        raise SystemExit(
            "usage: score_semantic_v3.py <evaluation-manifest.json> <ontology.json> "
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
        gold = json.loads(input_paths[2].read_text(encoding="utf-8"))
        coverage = coverage_facts(gold)
        validate_coverage(coverage)
        with tempfile.TemporaryDirectory() as directory:
            temporary_report = Path(directory) / "v2-core-report.json"
            core = run_v2_core(arguments, temporary_report)
        records = metric_records(core)
        required_not_applicable = [
            name
            for name, record in records.items()
            if record["status"] == "NOT_APPLICABLE"
        ]
        status = (
            "INVALID_SCORING_INPUT"
            if required_not_applicable
            else "SCORED"
        )
        report = {
            "schema_version": "v3",
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
                "v3 wraps the frozen v2 semantic core without modifying v2 files.",
                "NOT_APPLICABLE metrics never count as threshold passes.",
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
