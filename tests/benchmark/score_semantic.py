import hashlib
import json
import sys
from pathlib import Path

import validate_benchmark


ROUTES = {"Normal mode", "Limited-background mode", "Message-template mode", "Intake", "Scope"}
RATINGS = {"Green", "Yellow", "Red", "Gray", None}
MATCH_TYPES = {"exact", "alias", "semantic", "unsupported"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def ratio(correct: int, total: int) -> float:
    require(total > 0, "metric denominator must be nonzero")
    return correct / total


def unique(items: list[dict], key: str, label: str) -> dict:
    values = {item[key]: item for item in items}
    require(len(values) == len(items), f"duplicate {label}")
    return values


def load_ontology(path: Path) -> tuple[dict[str, dict], dict[tuple[str, str], str]]:
    document = json.loads(path.read_text(encoding="utf-8"))
    require(document.get("version") == "1", "ontology version")
    concepts = unique(document["concepts"], "concept_id", "ontology concept")
    aliases = {}
    for concept_id, concept in concepts.items():
        require(concept["domain"] in {"question", "revision"}, f"{concept_id}: domain")
        tokens = [concept_id, *concept["aliases"]]
        for token in tokens:
            key = (concept["domain"], token)
            require(key not in aliases, f"duplicate ontology alias: {key}")
            aliases[key] = concept_id
    return concepts, aliases


def validate_claims(claims: list[dict], raw_output: str, label: str) -> dict[str, dict]:
    values = unique(claims, "claim_id", f"{label} claim")
    for claim in claims:
        require(
            set(claim) == {"claim_id", "text", "evidence_span"},
            f"{label}: claim schema",
        )
        require(claim["text"] and claim["evidence_span"], f"{label}: empty claim")
        require(claim["evidence_span"] in raw_output, f"{label}: evidence span absent")
    return values


def validate_match_set(
    matches: list[dict],
    claims: dict[str, dict],
    domain: str,
    allowed: set[str],
    aliases: dict[tuple[str, str], str],
    label: str,
) -> tuple[set[str], int]:
    decisions = unique(matches, "claim_id", f"{label} match")
    require(set(decisions) == set(claims), f"{label}: unmatched or extra claim")
    matched = set()
    unsupported = 0
    for claim_id, decision in decisions.items():
        require(
            set(decision)
            == {
                "claim_id",
                "concept_id",
                "match_type",
                "confidence",
                "rationale",
            },
            f"{label}: match schema",
        )
        match_type = decision["match_type"]
        require(match_type in MATCH_TYPES, f"{label}: match type")
        require(
            isinstance(decision["confidence"], (int, float))
            and 0 <= decision["confidence"] <= 1,
            f"{label}: confidence",
        )
        require(isinstance(decision["rationale"], str) and decision["rationale"], f"{label}: rationale")
        concept_id = decision["concept_id"]
        if match_type == "unsupported":
            require(concept_id is None, f"{label}: unsupported concept must be null")
            unsupported += 1
            continue
        require(isinstance(concept_id, str) and concept_id in allowed, f"{label}: concept not allowed")
        if match_type in {"exact", "alias"}:
            require(
                claims[claim_id]["text"] == claims[claim_id]["evidence_span"],
                f"{label}: deterministic match must use verbatim evidence",
            )
            token = claims[claim_id]["text"]
            require(
                aliases.get((domain, token)) == concept_id,
                f"{label}: invalid deterministic ontology match",
            )
        else:
            require(decision["confidence"] >= 0.8, f"{label}: weak semantic match")
        matched.add(concept_id)
    return matched, unsupported


def main() -> None:
    if len(sys.argv) != 8:
        raise SystemExit(
            "usage: score_semantic.py <evaluation-manifest.json> <ontology.json> "
            "<gold.json> <outputs.json> <evaluations.json> <matches.json> <report.json>"
        )
    (
        manifest_path,
        ontology_path,
        gold_path,
        outputs_path,
        evaluations_path,
        matches_path,
        report_path,
    ) = (
        Path(value) for value in sys.argv[1:]
    )
    require(not report_path.exists(), "refusing to overwrite score report")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    validate_benchmark.validate_manifest(manifest)
    require(manifest["stage"] == "evaluations", "scoring requires evaluation-stage manifest")
    outputs_manifest = validate_benchmark.find_stage_manifest(manifest, "outputs")
    gold_manifest = validate_benchmark.find_gold_manifest(manifest)
    evaluation_roles = {item["role"]: Path(item["path"]).resolve() for item in manifest["artifacts"]}
    output_roles = {
        item["role"]: Path(item["path"]).resolve()
        for item in outputs_manifest["artifacts"]
    }
    gold_roles = {
        item["role"]: Path(item["path"]).resolve() for item in gold_manifest["artifacts"]
    }
    require(evaluation_roles["evaluations"] == evaluations_path.resolve(), "unfrozen evaluations")
    require(evaluation_roles["matches"] == matches_path.resolve(), "unfrozen matches")
    require(output_roles["outputs"] == outputs_path.resolve(), "unfrozen outputs")
    require(gold_roles["gold"] == gold_path.resolve(), "unfrozen gold")
    require(gold_roles["ontology"] == ontology_path.resolve(), "unfrozen ontology")
    require(gold_roles["scorer"] == Path(__file__).resolve(), "unfrozen scorer")
    _, aliases = load_ontology(ontology_path)
    gold_doc = json.loads(gold_path.read_text(encoding="utf-8"))
    outputs = unique(json.loads(outputs_path.read_text(encoding="utf-8"))["cases"], "case_id", "output case")
    evaluations_doc = json.loads(evaluations_path.read_text(encoding="utf-8"))
    evaluations = unique(evaluations_doc["cases"], "case_id", "evaluation case")
    matches_doc = json.loads(matches_path.read_text(encoding="utf-8"))
    matches = unique(matches_doc["cases"], "case_id", "match case")
    gold = unique(gold_doc["cases"], "case_id", "gold case")
    require(set(gold) == set(outputs) == set(evaluations) == set(matches), "case coverage")

    quality = gold_doc["gold_quality"]
    families = quality["labeler_model_families"]
    require(len(set(families)) >= 3, "fewer than three gold model families")
    require(quality["adjudicator_model_family"] not in set(families), "adjudicator not heterogeneous")
    require(isinstance(quality["human_review_available"], bool), "human review flag")

    evaluation_quality = evaluations_doc["evaluation_quality"]
    extractors = evaluation_quality["extractors"]
    require(isinstance(extractors, list) and len(extractors) >= 2, "two extractors required")
    extractor_contexts = set()
    extractor_families = set()
    for extractor in extractors:
        require(
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
        require(attestation_path.is_file(), "extractor attestation missing")
        import hashlib

        require(
            hashlib.sha256(attestation_path.read_bytes()).hexdigest()
            == extractor["attestation_sha256"],
            "extractor attestation hash",
        )
    require(len(extractor_contexts) == len(extractors), "extractor contexts not independent")
    require(len(extractor_families) >= 2, "claim extraction requires two model families")

    matcher = matches_doc["matcher"]
    require(matcher["gold_access"] is True, "semantic matcher must compare with gold")
    require(matcher["model_family"] not in set(families), "matcher duplicates gold labeler family")

    totals = {
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
    uncertain_totals = {
        "turns": 0,
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
    case_results = []

    for case_id, expected_case in gold.items():
        output_turns = outputs[case_id]["turn_outputs"]
        evaluation_turns = evaluations[case_id]["turn_evaluations"]
        match_turns = matches[case_id]["turn_matches"]
        gold_turns = expected_case["turn_labels"]
        require(
            len(output_turns) == len(evaluation_turns) == len(match_turns) == len(gold_turns),
            f"{case_id}: turn coverage",
        )
        case_mismatches = []
        case_uncertain_turns = 0
        for expected, output, actual, turn_match in zip(
            gold_turns,
            output_turns,
            evaluation_turns,
            match_turns,
        ):
            require(
                expected["turn_index"]
                == output["turn_index"]
                == actual["turn_index"]
                == turn_match["turn_index"],
                f"{case_id}: turn order",
            )
            claim_review = actual["claim_extraction_review"]
            require(
                set(claim_review)
                == {
                    "reviewed_by_context_ids",
                    "claim_completeness_reviewed",
                    "unresolved_claim_disagreements",
                },
                f"{case_id}: claim extraction review schema",
            )
            require(
                set(claim_review["reviewed_by_context_ids"]) == extractor_contexts,
                f"{case_id}: incomplete extractor coverage",
            )
            require(
                claim_review["claim_completeness_reviewed"] is True
                and claim_review["unresolved_claim_disagreements"] == 0,
                f"{case_id}: unresolved claim extraction",
            )
            quality_tier = expected["gold_quality"]["tier"]
            three_way = expected["gold_quality"]["three_way_categorical_disagreement"]
            invariant_disagreement = expected["gold_quality"]["critical_invariant_disagreement"]
            human_reviewed = expected["gold_quality"]["human_reviewed"]
            unresolved = expected["gold_quality"]["unresolved_adjudication"]
            if quality_tier == "human_reviewed":
                require(human_reviewed is True and unresolved is False, f"{case_id}: human tier")
            if quality_tier == "heterogeneous_adjudicated":
                require(human_reviewed is False and unresolved is False, f"{case_id}: adjudicated tier")
            if unresolved:
                require(quality_tier == "gold_uncertain", f"{case_id}: unresolved gold")
            if (three_way or invariant_disagreement) and not human_reviewed:
                require(quality_tier == "gold_uncertain", f"{case_id}: uncertain gold not marked")
            if quality_tier == "gold_uncertain":
                totals["uncertain_turns"] += 1
                case_uncertain_turns += 1
                uncertain_totals["turns"] += 1
                uncertain_totals["route"] += int(actual["route"] == expected["route"])
                for field in ("responsibility", "tone", "overall"):
                    if expected[field] is not None:
                        uncertain_totals["rated"][field] += 1
                        uncertain_totals["rating_correct"][field] += int(
                            actual[field] == expected[field]
                        )
                raw_output = output["raw_output"]
                question_claims = validate_claims(
                    actual["question_claims"],
                    raw_output,
                    f"{case_id}: uncertain question",
                )
                revision_claims = validate_claims(
                    actual["revision_claims"],
                    raw_output,
                    f"{case_id}: uncertain revision",
                )
                required_questions = set(expected["required_question_concepts"])
                required_revisions = set(expected["required_revision_concepts"])
                question_matched, question_unsupported = validate_match_set(
                    turn_match["question_matches"],
                    question_claims,
                    "question",
                    set(expected["allowed_question_concepts"]),
                    aliases,
                    f"{case_id}: uncertain question",
                )
                revision_matched, revision_unsupported = validate_match_set(
                    turn_match["revision_matches"],
                    revision_claims,
                    "revision",
                    set(expected["allowed_revision_concepts"]),
                    aliases,
                    f"{case_id}: uncertain revision",
                )
                uncertain_totals["required_questions"] += len(required_questions)
                uncertain_totals["required_questions_hit"] += len(
                    required_questions & question_matched
                )
                uncertain_totals["question_claims"] += len(question_claims)
                uncertain_totals["unsupported_question_claims"] += question_unsupported
                uncertain_totals["required_revisions"] += len(required_revisions)
                uncertain_totals["required_revisions_hit"] += len(
                    required_revisions & revision_matched
                )
                uncertain_totals["revision_claims"] += len(revision_claims)
                uncertain_totals["unsupported_revision_claims"] += revision_unsupported
                applicable = set(expected["critical_invariants"])
                invariant_results = actual["critical_invariant_results"]
                require(applicable <= set(invariant_results), f"{case_id}: invariant coverage")
                uncertain_totals["critical_violations"] += sum(
                    not invariant_results[item] for item in applicable
                )
                continue

            totals["accepted_turns"] += 1
            mismatches = []
            route_match = actual["route"] == expected["route"]
            totals["route"] += int(route_match)
            if not route_match:
                mismatches.append("route")
            for field in ("responsibility", "tone", "overall"):
                if expected[field] is not None:
                    totals["rated"][field] += 1
                    same = actual[field] == expected[field]
                    totals["rating_correct"][field] += int(same)
                    if not same:
                        mismatches.append(field)

            raw_output = output["raw_output"]
            question_claims = validate_claims(
                actual["question_claims"],
                raw_output,
                f"{case_id}: question",
            )
            revision_claims = validate_claims(
                actual["revision_claims"],
                raw_output,
                f"{case_id}: revision",
            )
            required_questions = set(expected["required_question_concepts"])
            allowed_questions = set(expected["allowed_question_concepts"])
            required_revisions = set(expected["required_revision_concepts"])
            allowed_revisions = set(expected["allowed_revision_concepts"])
            question_matched, question_unsupported = validate_match_set(
                turn_match["question_matches"],
                question_claims,
                "question",
                allowed_questions,
                aliases,
                f"{case_id}: question",
            )
            revision_matched, revision_unsupported = validate_match_set(
                turn_match["revision_matches"],
                revision_claims,
                "revision",
                allowed_revisions,
                aliases,
                f"{case_id}: revision",
            )
            totals["required_questions"] += len(required_questions)
            totals["required_questions_hit"] += len(required_questions & question_matched)
            totals["question_claims"] += len(question_claims)
            totals["unsupported_question_claims"] += question_unsupported
            totals["required_revisions"] += len(required_revisions)
            totals["required_revisions_hit"] += len(required_revisions & revision_matched)
            totals["revision_claims"] += len(revision_claims)
            totals["unsupported_revision_claims"] += revision_unsupported
            if not required_questions <= question_matched:
                mismatches.append("required-question-concepts")
            if question_unsupported:
                mismatches.append("unsupported-question-claims")
            if not required_revisions <= revision_matched:
                mismatches.append("required-revision-concepts")
            if revision_unsupported:
                mismatches.append("unsupported-revision-claims")

            invariant_results = actual["critical_invariant_results"]
            applicable = set(expected["critical_invariants"])
            require(applicable <= set(invariant_results), f"{case_id}: invariant coverage")
            violations = sum(not invariant_results[item] for item in applicable)
            totals["critical_violations"] += violations
            if violations:
                mismatches.append("critical-invariant")
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

    total_turns = totals["accepted_turns"] + totals["uncertain_turns"]
    require(total_turns > 0, "no turns")
    uncertain_rate = totals["uncertain_turns"] / total_turns
    require(uncertain_rate <= 0.20, "gold uncertainty exceeds 20%")
    metrics = {
        "gold_uncertain_rate": uncertain_rate,
        "route_accuracy": ratio(totals["route"], totals["accepted_turns"]),
        "responsibility_accuracy": ratio(
            totals["rating_correct"]["responsibility"],
            totals["rated"]["responsibility"],
        ),
        "tone_accuracy": ratio(
            totals["rating_correct"]["tone"],
            totals["rated"]["tone"],
        ),
        "overall_accuracy": ratio(
            totals["rating_correct"]["overall"],
            totals["rated"]["overall"],
        ),
        "required_question_concept_recall": ratio(
            totals["required_questions_hit"],
            totals["required_questions"],
        ),
        "question_claim_support_precision": (
            1.0
            if totals["question_claims"] == 0
            else 1 - totals["unsupported_question_claims"] / totals["question_claims"]
        ),
        "required_revision_concept_recall": ratio(
            totals["required_revisions_hit"],
            totals["required_revisions"],
        ),
        "revision_claim_support_precision": (
            1.0
            if totals["revision_claims"] == 0
            else 1 - totals["unsupported_revision_claims"] / totals["revision_claims"]
        ),
        "critical_invariant_violations": totals["critical_violations"],
    }
    uncertain_metrics = {
        "turns": uncertain_totals["turns"],
        "route_accuracy": (
            None
            if uncertain_totals["turns"] == 0
            else uncertain_totals["route"] / uncertain_totals["turns"]
        ),
        "responsibility_accuracy": (
            None
            if uncertain_totals["rated"]["responsibility"] == 0
            else uncertain_totals["rating_correct"]["responsibility"]
            / uncertain_totals["rated"]["responsibility"]
        ),
        "tone_accuracy": (
            None
            if uncertain_totals["rated"]["tone"] == 0
            else uncertain_totals["rating_correct"]["tone"]
            / uncertain_totals["rated"]["tone"]
        ),
        "overall_accuracy": (
            None
            if uncertain_totals["rated"]["overall"] == 0
            else uncertain_totals["rating_correct"]["overall"]
            / uncertain_totals["rated"]["overall"]
        ),
        "required_question_concept_recall": (
            None
            if uncertain_totals["required_questions"] == 0
            else uncertain_totals["required_questions_hit"]
            / uncertain_totals["required_questions"]
        ),
        "question_claim_support_precision": (
            None
            if uncertain_totals["question_claims"] == 0
            else 1
            - uncertain_totals["unsupported_question_claims"]
            / uncertain_totals["question_claims"]
        ),
        "required_revision_concept_recall": (
            None
            if uncertain_totals["required_revisions"] == 0
            else uncertain_totals["required_revisions_hit"]
            / uncertain_totals["required_revisions"]
        ),
        "revision_claim_support_precision": (
            None
            if uncertain_totals["revision_claims"] == 0
            else 1
            - uncertain_totals["unsupported_revision_claims"]
            / uncertain_totals["revision_claims"]
        ),
        "critical_invariant_violations": uncertain_totals["critical_violations"],
    }
    report = {
        "artifact_manifest_sha256": hashlib.sha256(
            manifest_path.read_bytes()
        ).hexdigest(),
        "metrics": metrics,
        "gold_uncertain_metrics": uncertain_metrics,
        "totals": totals,
        "case_results": case_results,
        "gold_quality": quality,
        "matcher": matcher,
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
