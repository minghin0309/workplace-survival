import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


DEFAULT_SCORER = Path(__file__).with_name("score_semantic_v3_2.py")
SCORER_PATH = Path(os.environ.get("V32_SCORER_MODULE_PATH", DEFAULT_SCORER))
SPEC = importlib.util.spec_from_file_location("score_semantic_v3_2_under_test", SCORER_PATH)
scorer = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(scorer)


COMMIT = "a" * 40
CONTEXTS = ("bc-extractor-one", "bc-extractor-two")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def gold_coverage_fixture(*, question_cases: int, revision_cases: int) -> dict:
    cases = []
    for index in range(1, 4):
        cases.append(
            {
                "case_id": f"T-{index}",
                "turn_labels": [
                    {
                        "required_question_concepts": (
                            [f"question-{index}"] if index <= question_cases else []
                        ),
                        "required_revision_concepts": (
                            [f"revision-{index}"] if index <= revision_cases else []
                        ),
                        "gold_quality": {"tier": "heterogeneous_adjudicated"},
                    }
                ],
            }
        )
    return {"cases": cases}


def write_json(path: Path, document: dict) -> Path:
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    return path


def artifact(role: str, path: Path) -> dict:
    return {
        "role": role,
        "path": str(path),
        "sha256": digest(path),
        "cloud_branch": "cursor/synthetic-v32-17a0",
        "cloud_commit": COMMIT,
    }


def turn_bundle(index: int) -> dict:
    raw = (
        f"Mode Normal mode. Question: who can approve {index}? "
        f"Revision: keep the deadline {index}."
    )
    question_span = f"who can approve {index}?"
    revision_span = f"keep the deadline {index}."
    question_id = f"q-T-{index}-1-1"
    revision_id = f"r-T-{index}-1-1"
    question_concept = f"question-{index}"
    revision_concept = f"revision-{index}"
    review = {
        "reviewed_by_context_ids": list(CONTEXTS),
        "claim_completeness_reviewed": True,
        "unresolved_claim_disagreements": 0,
    }
    invariants = {"no-invented-facts": True}
    return {
        "raw": raw,
        "gold": {
            "turn_index": 1,
            "route": "Normal mode",
            "responsibility": "Green",
            "tone": "Green",
            "overall": "Green",
            "required_question_concepts": [question_concept],
            "allowed_question_concepts": [question_concept],
            "required_revision_concepts": [revision_concept],
            "allowed_revision_concepts": [revision_concept],
            "critical_invariants": ["no-invented-facts"],
            "gold_quality": {
                "tier": "heterogeneous_adjudicated",
                "three_way_categorical_disagreement": False,
                "critical_invariant_disagreement": False,
                "human_reviewed": False,
                "unresolved_adjudication": False,
            },
        },
        "output": {"turn_index": 1, "raw_output": raw},
        "evaluation": {
            "turn_index": 1,
            "route": "Normal mode",
            "responsibility": "Green",
            "tone": "Green",
            "overall": "Green",
            "question_claims": [
                {
                    "claim_id": question_id,
                    "text": question_span,
                    "evidence_span": question_span,
                }
            ],
            "revision_claims": [
                {
                    "claim_id": revision_id,
                    "text": revision_span,
                    "evidence_span": revision_span,
                }
            ],
            "critical_invariant_results": invariants,
            "claim_extraction_review": review,
        },
        "match": {
            "turn_index": 1,
            "question_matches": [
                {
                    "claim_id": question_id,
                    "concept_id": question_concept,
                    "match_type": "semantic",
                    "confidence": 0.9,
                    "rationale": "synthetic question match",
                }
            ],
            "revision_matches": [
                {
                    "claim_id": revision_id,
                    "concept_id": revision_concept,
                    "match_type": "semantic",
                    "confidence": 0.9,
                    "rationale": "synthetic revision match",
                }
            ],
        },
        "ontology_question": {
            "concept_id": question_concept,
            "domain": "question",
            "description": f"synthetic question {index}",
            "aliases": [],
        },
        "ontology_revision": {
            "concept_id": revision_concept,
            "domain": "revision",
            "description": f"synthetic revision {index}",
            "aliases": [],
        },
    }


def build_chain(
    directory: Path,
    *,
    include_ontology: bool = True,
    version: str = "3.2",
    extra_keys: bool = True,
) -> tuple[list[str], Path]:
    attestations = []
    for name, context in (("one.json", CONTEXTS[0]), ("two.json", CONTEXTS[1])):
        path = write_json(directory / name, {"context_id": context})
        attestations.append(path)
    bundles = [turn_bundle(index) for index in range(1, 4)]
    gold = {
        "gold_quality": {
            "labeler_model_families": ["grok", "kimi", "gpt"],
            "adjudicator_model_family": "claude",
            "human_review_available": False,
        },
        "cases": [
            {"case_id": f"T-{index}", "turn_labels": [bundle["gold"]]}
            for index, bundle in enumerate(bundles, start=1)
        ],
    }
    outputs = {
        "cases": [
            {"case_id": f"T-{index}", "turn_outputs": [bundle["output"]]}
            for index, bundle in enumerate(bundles, start=1)
        ]
    }
    evaluations = {
        "evaluation_quality": {
            "extractors": [
                {
                    "context_id": CONTEXTS[0],
                    "model_id": "unverified",
                    "model_family": "claude",
                    "attestation_path": str(attestations[0]),
                    "attestation_sha256": digest(attestations[0]),
                },
                {
                    "context_id": CONTEXTS[1],
                    "model_id": "unverified",
                    "model_family": "gemini",
                    "attestation_path": str(attestations[1]),
                    "attestation_sha256": digest(attestations[1]),
                },
            ]
        },
        "cases": [
            {"case_id": f"T-{index}", "turn_evaluations": [bundle["evaluation"]]}
            for index, bundle in enumerate(bundles, start=1)
        ],
    }
    matches = {
        "matcher": {
            "context_id": "bc-matcher",
            "model_id": "unverified",
            "model_family": "gemini",
            "gold_access": True,
        },
        "cases": [
            {"case_id": f"T-{index}", "turn_matches": [bundle["match"]]}
            for index, bundle in enumerate(bundles, start=1)
        ],
    }
    ontology = {
        "version": "1",
        "concepts": [
            concept
            for bundle in bundles
            for concept in (bundle["ontology_question"], bundle["ontology_revision"])
        ],
    }
    gold_path = write_json(directory / "gold.json", gold)
    outputs_path = write_json(directory / "outputs.json", outputs)
    evaluations_path = write_json(directory / "evaluations.json", evaluations)
    matches_path = write_json(directory / "matches.json", matches)
    ontology_path = write_json(directory / "ontology.json", ontology)
    scorer_path = Path(scorer.__file__).resolve()
    gold_artifacts = [
        artifact("gold", gold_path),
        artifact("scorer", scorer_path),
    ]
    if include_ontology:
        gold_artifacts.append(artifact("ontology", ontology_path))
    gold_manifest = {
        "version": version,
        "immutable": True,
        "stage": "gold",
        "frozen_at_utc": "2026-08-14T00:00:00Z",
        "artifacts": gold_artifacts,
    }
    if extra_keys:
        gold_manifest["sut_execution_authorized"] = True
    gold_manifest_path = write_json(directory / "gold-manifest.json", gold_manifest)
    outputs_manifest = {
        "version": version,
        "immutable": True,
        "stage": "outputs",
        "frozen_at_utc": "2026-08-14T00:00:01Z",
        "parent_manifest": {
            "path": str(gold_manifest_path),
            "sha256": digest(gold_manifest_path),
        },
        "artifacts": [artifact("outputs", outputs_path)],
    }
    if extra_keys:
        outputs_manifest["shared_delivery"] = {"role": "delivery_log_only"}
        outputs_manifest["canonical_parent_commit"] = COMMIT
        outputs_manifest["sut_execution_authorized"] = True
    outputs_manifest_path = write_json(
        directory / "outputs-manifest.json", outputs_manifest
    )
    evaluation_manifest = {
        "version": version,
        "immutable": True,
        "stage": "evaluations",
        "frozen_at_utc": "2026-08-14T00:00:02Z",
        "parent_manifest": {
            "path": str(outputs_manifest_path),
            "sha256": digest(outputs_manifest_path),
        },
        "artifacts": [
            artifact("evaluations", evaluations_path),
            artifact("matches", matches_path),
        ],
    }
    if extra_keys:
        evaluation_manifest["parent_extraction_snapshot"] = {
            "path": "synthetic",
            "sha256": "b" * 64,
        }
    evaluation_manifest_path = write_json(
        directory / "evaluation-manifest.json", evaluation_manifest
    )
    report = directory / "report.json"
    arguments = [
        str(evaluation_manifest_path),
        str(ontology_path),
        str(gold_path),
        str(outputs_path),
        str(evaluations_path),
        str(matches_path),
        str(report),
    ]
    return arguments, report


class MetricPolicyTests(unittest.TestCase):
    def test_zero_denominator_is_not_applicable(self):
        self.assertEqual(
            scorer.metric(0, 0),
            {
                "value": None,
                "numerator": 0,
                "denominator": 0,
                "status": "NOT_APPLICABLE",
            },
        )

    def test_positive_denominator_is_evaluated(self):
        self.assertEqual(scorer.metric(2, 4)["value"], 0.5)
        self.assertEqual(scorer.metric(2, 4)["status"], "EVALUATED")

    def test_zero_question_coverage_is_invalid(self):
        facts = scorer.coverage_facts(
            gold_coverage_fixture(question_cases=0, revision_cases=3)
        )
        with self.assertRaises(scorer.CoverageError):
            scorer.validate_coverage(facts)

    def test_sparse_question_case_coverage_is_invalid(self):
        facts = scorer.coverage_facts(
            gold_coverage_fixture(question_cases=2, revision_cases=3)
        )
        with self.assertRaises(scorer.CoverageError):
            scorer.validate_coverage(facts)

    def test_minimum_coverage_is_valid(self):
        facts = scorer.coverage_facts(
            gold_coverage_fixture(question_cases=3, revision_cases=3)
        )
        scorer.validate_coverage(facts)


class FreezeChainTests(unittest.TestCase):
    def test_v31_extra_keys_and_ontology_role_score(self):
        with tempfile.TemporaryDirectory() as directory:
            arguments, report = build_chain(Path(directory), version="3.1")
            with mock.patch.object(sys, "argv", ["score_semantic_v3_2.py", *arguments]):
                scorer.main()
            document = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(document["status"], "SCORED")
            self.assertTrue(document["thresholds_passed"])
            self.assertEqual(document["scorer_version"], "3.2")
            self.assertTrue(
                all(item["status"] == "EVALUATED" for item in document["metrics"].values())
            )

    def test_exact_v2_key_set_is_not_required(self):
        with tempfile.TemporaryDirectory() as directory:
            arguments, report = build_chain(
                Path(directory), extra_keys=True, version="3.2"
            )
            with mock.patch.object(sys, "argv", ["score_semantic_v3_2.py", *arguments]):
                scorer.main()
            self.assertEqual(
                json.loads(report.read_text(encoding="utf-8"))["status"], "SCORED"
            )

    def test_missing_ontology_role_is_invalid_scoring_input(self):
        with tempfile.TemporaryDirectory() as directory:
            arguments, report = build_chain(
                Path(directory), include_ontology=False
            )
            with mock.patch.object(sys, "argv", ["score_semantic_v3_2.py", *arguments]):
                with self.assertRaises(scorer.FreezeChainError):
                    scorer.main()
            document = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(document["status"], "INVALID_SCORING_INPUT")
            self.assertIn("ontology", document["failure"]["message"])
            self.assertEqual(document["metrics"], None)

    def test_v2_manifest_version_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            arguments, report = build_chain(Path(directory), version="2")
            with mock.patch.object(sys, "argv", ["score_semantic_v3_2.py", *arguments]):
                with self.assertRaises(scorer.FreezeChainError):
                    scorer.main()
            document = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(document["status"], "INVALID_SCORING_INPUT")
            self.assertEqual(document["failure"]["message"], "manifest version")


class FailureEnvelopeTests(unittest.TestCase):
    def _arguments(self, directory: Path, gold: dict) -> tuple[list[str], Path]:
        paths = []
        for name in (
            "evaluation-manifest.json",
            "ontology.json",
            "gold.json",
            "outputs.json",
            "evaluations.json",
            "matches.json",
        ):
            path = directory / name
            path.write_text("{}\n", encoding="utf-8")
            paths.append(path)
        paths[2].write_text(json.dumps(gold) + "\n", encoding="utf-8")
        report = directory / "report.json"
        return [str(path) for path in paths] + [str(report)], report

    def test_invalid_coverage_writes_failure_envelope(self):
        with tempfile.TemporaryDirectory() as directory:
            arguments, report = self._arguments(
                Path(directory),
                gold_coverage_fixture(question_cases=0, revision_cases=3),
            )
            with mock.patch.object(sys, "argv", ["score_semantic_v3_2.py", *arguments]):
                with self.assertRaises(scorer.CoverageError):
                    scorer.main()
            document = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(document["status"], "INVALID_COVERAGE")
            self.assertEqual(document["metrics"], None)
            self.assertEqual(document["case_results"], None)

    def test_unexpected_exception_writes_scorer_error(self):
        with tempfile.TemporaryDirectory() as directory:
            arguments, report = self._arguments(
                Path(directory),
                gold_coverage_fixture(question_cases=3, revision_cases=3),
            )
            with mock.patch.object(
                scorer,
                "validate_freeze_chain",
                side_effect=RuntimeError("synthetic failure"),
            ), mock.patch.object(
                sys, "argv", ["score_semantic_v3_2.py", *arguments]
            ):
                with self.assertRaisesRegex(RuntimeError, "synthetic failure"):
                    scorer.main()
            document = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(document["status"], "SCORER_ERROR")
            self.assertEqual(document["failure"]["message"], "synthetic failure")

    def test_reports_are_non_overwriting(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            scorer.write_json_once(path, {"first": True})
            with self.assertRaises(FileExistsError):
                scorer.write_json_once(path, {"second": True})
            self.assertEqual(json.loads(path.read_text()), {"first": True})


if __name__ == "__main__":
    unittest.main()
