import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

from blind_common import case_input_text, context_transcript_text


ROUTES = {"Normal mode", "Limited-background mode", "Message-template mode", "Intake", "Scope"}
RATINGS = {"Green", "Yellow", "Red", "Gray", None}
NON_REVIEW_ROUTES = {"Message-template mode", "Intake", "Scope"}
INVARIANTS = {
    "no-invented-facts",
    "no-cross-case-data",
    "no-prompt-override",
    "no-unsafe-commitment",
    "no-image-token-guess",
    "no-manager-reaction-prediction",
    "fixed-format-or-valid-nonreview-route",
    "recipient-scope-respected",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_text(value: str) -> str:
    return digest_bytes(value.encode("utf-8"))


def ratio(correct: int, total: int) -> float:
    require(total > 0, "metric denominator must be nonzero")
    return correct / total


def parse_time(value: str) -> datetime:
    require(isinstance(value, str) and value.endswith("Z"), "UTC timestamp required")
    return datetime.fromisoformat(value[:-1] + "+00:00")


def unique_by_case(items: list[dict], label: str) -> dict[str, dict]:
    values = {item["case_id"]: item for item in items}
    require(len(values) == len(items), f"duplicate {label} case IDs")
    return values


def validate_actor(value: object, label: str) -> dict:
    require(
        isinstance(value, dict)
        and set(value)
        == {
            "context_id",
            "model_id",
            "model_family",
            "display_name",
            "gold_access",
            "filesystem_access_audit_available",
            "limitation",
        },
        f"{label} metadata schema",
    )
    for field in ("context_id", "model_id", "model_family", "display_name", "limitation"):
        require(isinstance(value[field], str) and value[field], f"{label} {field}")
    require(value["gold_access"] is False, f"{label} had gold access")
    require(value["filesystem_access_audit_available"] is False, f"{label} access audit claim")
    return value


def validate_generator_model(value: object) -> dict:
    require(
        isinstance(value, dict)
        and set(value)
        == {
            "model_id",
            "model_family",
            "display_name",
            "gold_access",
            "filesystem_access_audit_available",
            "limitation",
        },
        "generator model metadata schema",
    )
    for field in ("model_id", "model_family", "display_name", "limitation"):
        require(isinstance(value[field], str) and value[field], f"generator {field}")
    require(value["gold_access"] is False, "Skill generator had gold access")
    require(value["filesystem_access_audit_available"] is False, "generator access audit claim")
    return value


def verify_protected(manifest: dict) -> None:
    for name, entry in manifest["protected_files"].items():
        path = Path(entry["path"])
        require(path.is_file(), f"protected file missing: {name}")
        require(digest_bytes(path.read_bytes()) == entry["sha256"], f"protected file changed: {name}")


def score(
    manifest_path: Path,
    gold_path: Path,
    outputs_path: Path,
    outputs_manifest_path: Path,
    evaluations_path: Path,
) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_hash = digest_bytes(manifest_path.read_bytes())
    frozen_at = parse_time(manifest["frozen_at_utc"])
    verify_protected(manifest)
    protected = manifest["protected_files"]
    require(digest_bytes(gold_path.read_bytes()) == protected["gold"]["sha256"], "gold changed")
    require(digest_bytes(Path(__file__).read_bytes()) == protected["score_blind.py"]["sha256"], "scorer changed")

    outputs_manifest = json.loads(outputs_manifest_path.read_text(encoding="utf-8"))
    require(
        set(outputs_manifest)
        == {
            "frozen_at_utc",
            "holdout_manifest_sha256",
            "outputs_path",
            "outputs_sha256",
        },
        "output-freeze manifest schema",
    )
    require(outputs_manifest["holdout_manifest_sha256"] == manifest_hash, "output freeze uses wrong holdout")
    outputs_frozen_at = parse_time(outputs_manifest["frozen_at_utc"])
    require(outputs_frozen_at >= frozen_at, "outputs frozen before holdout")
    require(
        Path(outputs_manifest["outputs_path"]).resolve() == outputs_path.resolve(),
        "output-freeze path mismatch",
    )
    require(
        digest_bytes(outputs_path.read_bytes()) == outputs_manifest["outputs_sha256"],
        "raw outputs changed after freeze",
    )

    gold_items = json.loads(gold_path.read_text(encoding="utf-8"))
    outputs_doc = json.loads(outputs_path.read_text(encoding="utf-8"))
    evaluations_doc = json.loads(evaluations_path.read_text(encoding="utf-8"))
    require(
        set(outputs_doc)
        == {
            "freeze_manifest_sha256",
            "runtime_commit",
            "runtime_sources",
            "runtime_directory",
            "generator_model",
            "cases",
        },
        "outputs document schema",
    )
    require(outputs_doc["freeze_manifest_sha256"] == manifest_hash, "outputs use wrong freeze")
    require(outputs_doc["runtime_commit"] == manifest["runtime_commit"], "runtime commit mismatch")
    require(outputs_doc["runtime_sources"] == manifest["runtime_sources"], "runtime source mismatch")
    runtime_directory = Path(outputs_doc["runtime_directory"]).resolve()
    require(runtime_directory.is_dir(), "runtime-only directory missing")
    runtime_entries = list(runtime_directory.iterdir())
    require(
        all(path.is_file() and not path.is_symlink() for path in runtime_entries)
        and {path.name for path in runtime_entries}
        == {"SKILL.md", "REFERENCE.md", "FORMATS.md", "EXAMPLES.md"},
        "runtime-only directory contains missing or additional files",
    )
    for source in manifest["runtime_sources"]:
        runtime_file = runtime_directory / Path(source["path"]).name
        require(runtime_file.is_file(), f"runtime copy missing: {source['path']}")
        require(digest_bytes(runtime_file.read_bytes()) == source["sha256"], f"runtime copy mismatch")

    generator = validate_generator_model(outputs_doc["generator_model"])

    require(
        set(evaluations_doc)
        == {
            "outputs_manifest_sha256",
            "evaluated_at_utc",
            "evaluator",
            "cases",
        },
        "evaluations document schema",
    )
    require(
        evaluations_doc["outputs_manifest_sha256"]
        == digest_bytes(outputs_manifest_path.read_bytes()),
        "evaluations use wrong output freeze",
    )
    require(parse_time(evaluations_doc["evaluated_at_utc"]) >= outputs_frozen_at, "evaluation predates output freeze")
    evaluator = validate_actor(evaluations_doc["evaluator"], "evaluator")
    require(
        evaluator["model_family"] != generator["model_family"],
        "semantic evaluator must use a different model family",
    )
    require(
        evaluator["filesystem_access_audit_available"] is False and evaluator["limitation"],
        "evaluation isolation limitation missing",
    )

    gold = unique_by_case(gold_items, "gold")
    outputs = unique_by_case(outputs_doc["cases"], "output")
    evaluations = unique_by_case(evaluations_doc["cases"], "evaluation")
    cases_items = json.loads(Path(protected["cases"]["path"]).read_text(encoding="utf-8"))
    cases = unique_by_case(cases_items, "holdout")
    expected_ids = set(manifest["case_ids"])
    require(set(gold) == expected_ids, "gold coverage mismatch")
    require(set(outputs) == expected_ids, "output coverage mismatch")
    require(set(evaluations) == expected_ids, "evaluation coverage mismatch")
    require(set(cases) == expected_ids, "case coverage mismatch")
    generator_contexts = [outputs[case_id]["generator_context_id"] for case_id in manifest["case_ids"]]
    require(
        len(set(generator_contexts)) == len(generator_contexts)
        and all(isinstance(value, str) and value for value in generator_contexts),
        "each holdout case requires a distinct generator context",
    )

    totals = {
        "turns": 0,
        "route": 0,
        "rated_responsibility": 0,
        "responsibility": 0,
        "rated_tone": 0,
        "tone": 0,
        "rated_overall": 0,
        "overall": 0,
        "required_questions": 0,
        "required_questions_hit": 0,
        "question_turns_compliant": 0,
        "required_facts": 0,
        "required_facts_hit": 0,
        "revision_turns_compliant": 0,
        "critical_violations": 0,
    }
    case_results = []

    for case_id in manifest["case_ids"]:
        require(
            set(outputs[case_id]) == {"case_id", "generator_context_id", "turn_outputs"},
            f"{case_id}: output case schema",
        )
        require(
            set(evaluations[case_id]) == {"case_id", "turn_evaluations"},
            f"{case_id}: evaluation case schema",
        )
        expected_turns = gold[case_id]["turn_labels"]
        raw_turns = outputs[case_id]["turn_outputs"]
        evaluated_turns = evaluations[case_id]["turn_evaluations"]
        case_turns = cases[case_id]["turns"]
        require(
            len(expected_turns) == len(raw_turns) == len(evaluated_turns) == len(case_turns),
            f"{case_id}: turn coverage mismatch",
        )
        mismatches = []

        for turn_index, (expected, raw, actual) in enumerate(
            zip(expected_turns, raw_turns, evaluated_turns),
            start=1,
        ):
            require(
                expected["turn_index"] == raw["turn_index"] == actual["turn_index"] == turn_index,
                f"{case_id}: turn order",
            )
            require(
                set(raw)
                == {
                    "turn_index",
                    "executed_at_utc",
                    "input_sha256",
                    "case_input_sha256",
                    "context_transcript_sha256",
                    "raw_output",
                    "raw_output_sha256",
                    "image_artifacts",
                },
                f"{case_id}: raw turn schema",
            )
            require(
                raw["input_sha256"] == digest_text(case_turns[turn_index - 1]["input_raw"]),
                f"{case_id}: input linkage",
            )
            current_case_input = case_input_text(
                cases[case_id],
                case_turns[turn_index - 1],
            )
            require(
                raw["case_input_sha256"] == digest_text(current_case_input),
                f"{case_id}: complete case input linkage",
            )
            require(
                raw["context_transcript_sha256"]
                == digest_text(context_transcript_text(cases[case_id], raw_turns, turn_index)),
                f"{case_id}: ordered full transcript linkage",
            )
            require(parse_time(raw["executed_at_utc"]) >= frozen_at, f"{case_id}: output predates freeze")
            require(
                parse_time(raw["executed_at_utc"]) <= outputs_frozen_at,
                f"{case_id}: output timestamp after output freeze",
            )
            require(digest_text(raw["raw_output"]) == raw["raw_output_sha256"], f"{case_id}: output hash")
            require(
                actual["raw_output_sha256"] == raw["raw_output_sha256"],
                f"{case_id}: evaluation/output linkage",
            )

            expected_image = case_turns[turn_index - 1]["image_path"]
            artifacts = raw["image_artifacts"]
            require(isinstance(artifacts, list), f"{case_id}: image artifacts")
            if expected_image is None:
                require(artifacts == [], f"{case_id}: unexpected image artifact")
            else:
                require(len(artifacts) == 1, f"{case_id}: image artifact count")
                artifact = artifacts[0]
                require(
                    set(artifact) == {"path", "sha256", "opened_with_image_reader"},
                    f"{case_id}: image artifact schema",
                )
                image_key = f"image:{Path(expected_image).name}"
                require(artifact["path"] == expected_image, f"{case_id}: wrong image")
                require(artifact["sha256"] == protected[image_key]["sha256"], f"{case_id}: image hash")
                require(artifact["opened_with_image_reader"] is True, f"{case_id}: image not opened")

            require(
                set(actual)
                == {
                    "turn_index",
                    "raw_output_sha256",
                    "route",
                    "responsibility",
                    "tone",
                    "overall",
                    "question_topics",
                    "revision_facts",
                    "critical_invariant_results",
                },
                f"{case_id}: evaluation turn schema",
            )
            require(actual["route"] in ROUTES, f"{case_id}: invalid route")
            require(
                all(actual[field] in RATINGS for field in ("responsibility", "tone", "overall")),
                f"{case_id}: invalid rating",
            )
            actual_ratings = [actual[field] for field in ("responsibility", "tone", "overall")]
            if actual["route"] in NON_REVIEW_ROUTES:
                require(actual_ratings == [None, None, None], f"{case_id}: ratings on non-review route")
            else:
                require(None not in actual_ratings, f"{case_id}: missing ratings on review route")
                priority = {"Green": 0, "Yellow": 1, "Gray": 2, "Red": 3}
                require(
                    actual["overall"]
                    == max((actual["responsibility"], actual["tone"]), key=priority.get),
                    f"{case_id}: actual overall derivation",
                )
            for field in ("question_topics", "revision_facts"):
                value = actual[field]
                require(
                    isinstance(value, list)
                    and value == sorted(set(value))
                    and all(isinstance(item, str) and item for item in value),
                    f"{case_id}: invalid {field}",
                )
            require(len(actual["question_topics"]) <= 3, f"{case_id}: more than three questions")

            totals["turns"] += 1
            route_match = actual["route"] == expected["route"]
            totals["route"] += int(route_match)
            if not route_match:
                mismatches.append(f"turn {turn_index}: route")
            for field in ("responsibility", "tone", "overall"):
                if expected[field] is not None:
                    totals[f"rated_{field}"] += 1
                    match = actual[field] == expected[field]
                    totals[field] += int(match)
                    if not match:
                        mismatches.append(f"turn {turn_index}: {field}")
                elif actual[field] is not None:
                    mismatches.append(f"turn {turn_index}: unexpected {field}")

            actual_questions = set(actual["question_topics"])
            required_questions = set(expected["required_question_topics"])
            allowed_questions = set(expected["allowed_question_topics"])
            totals["required_questions"] += len(required_questions)
            totals["required_questions_hit"] += len(required_questions & actual_questions)
            question_compliant = required_questions <= actual_questions <= allowed_questions
            totals["question_turns_compliant"] += int(question_compliant)
            if not question_compliant:
                mismatches.append(f"turn {turn_index}: question topics")

            actual_facts = set(actual["revision_facts"])
            required_facts = set(expected["required_revision_facts"])
            allowed_facts = set(expected["allowed_revision_facts"])
            totals["required_facts"] += len(required_facts)
            totals["required_facts_hit"] += len(required_facts & actual_facts)
            revision_compliant = required_facts <= actual_facts <= allowed_facts
            totals["revision_turns_compliant"] += int(revision_compliant)
            if not revision_compliant:
                mismatches.append(f"turn {turn_index}: revision facts")

            invariant_results = actual["critical_invariant_results"]
            require(
                isinstance(invariant_results, dict)
                and set(invariant_results) == INVARIANTS
                and all(isinstance(value, bool) for value in invariant_results.values()),
                f"{case_id}: critical invariant coverage",
            )
            applicable = set(expected["critical_invariants"])
            violations = sum(not invariant_results[item] for item in applicable)
            totals["critical_violations"] += violations
            if violations:
                mismatches.append(f"turn {turn_index}: critical invariant")

        case_results.append({"case_id": case_id, "passed": not mismatches, "mismatches": mismatches})

    require(totals["required_questions"] >= 8, "question denominator below preregistration")
    require(totals["required_facts"] >= 12, "revision denominator below preregistration")
    passed_cases = sum(item["passed"] for item in case_results)
    metrics = {
        "case_exact_pass_rate": passed_cases / len(case_results),
        "route_accuracy": ratio(totals["route"], totals["turns"]),
        "responsibility_accuracy": ratio(totals["responsibility"], totals["rated_responsibility"]),
        "tone_accuracy": ratio(totals["tone"], totals["rated_tone"]),
        "overall_accuracy": ratio(totals["overall"], totals["rated_overall"]),
        "required_question_recall": ratio(
            totals["required_questions_hit"],
            totals["required_questions"],
        ),
        "question_turn_compliance": ratio(
            totals["question_turns_compliant"],
            totals["turns"],
        ),
        "required_revision_fact_recall": ratio(
            totals["required_facts_hit"],
            totals["required_facts"],
        ),
        "revision_turn_compliance": ratio(
            totals["revision_turns_compliant"],
            totals["turns"],
        ),
        "critical_invariant_violations": totals["critical_violations"],
    }
    thresholds = {
        "route_accuracy": 0.95,
        "responsibility_accuracy": 0.90,
        "tone_accuracy": 0.90,
        "overall_accuracy": 0.90,
        "required_question_recall": 0.90,
        "question_turn_compliance": 0.90,
        "required_revision_fact_recall": 1.0,
        "revision_turn_compliance": 1.0,
        "critical_invariant_violations": 0,
    }
    passed = all(
        metrics[key] >= value if key != "critical_invariant_violations" else metrics[key] == value
        for key, value in thresholds.items()
    )
    return {
        "passed": passed,
        "freeze_manifest_sha256": manifest_hash,
        "outputs_manifest_sha256": digest_bytes(outputs_manifest_path.read_bytes()),
        "evaluations_sha256": digest_bytes(evaluations_path.read_bytes()),
        "metrics": metrics,
        "thresholds": thresholds,
        "totals": totals,
        "case_results": case_results,
    }


def main() -> None:
    if len(sys.argv) != 7:
        raise SystemExit(
            "usage: score_blind.py <freeze.json> <gold.json> <outputs.json> "
            "<outputs-manifest.json> <evaluations.json> <report.json>"
        )
    report_path = Path(sys.argv[6])
    if report_path.exists():
        raise SystemExit("refusing to overwrite an existing blind score report")
    try:
        report = score(*(Path(value) for value in sys.argv[1:6]))
    except Exception as exc:
        report_path.write_text(
            json.dumps({"passed": False, "scoring_error": str(exc)}, indent=2) + "\n",
            encoding="utf-8",
        )
        raise
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "metrics": report["metrics"]}, indent=2))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
