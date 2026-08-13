import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


DEFAULT_SCORER = Path(__file__).with_name("score_semantic_v3.py")
SCORER_PATH = Path(os.environ.get("V3_SCORER_MODULE_PATH", DEFAULT_SCORER))
SPEC = importlib.util.spec_from_file_location("score_semantic_v3_under_test", SCORER_PATH)
scorer = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(scorer)


def gold_fixture(*, question_cases: int, revision_cases: int) -> dict:
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
            gold_fixture(question_cases=0, revision_cases=3)
        )
        with self.assertRaises(scorer.CoverageError):
            scorer.validate_coverage(facts)

    def test_sparse_question_case_coverage_is_invalid(self):
        facts = scorer.coverage_facts(
            gold_fixture(question_cases=2, revision_cases=3)
        )
        with self.assertRaises(scorer.CoverageError):
            scorer.validate_coverage(facts)

    def test_minimum_coverage_is_valid(self):
        facts = scorer.coverage_facts(
            gold_fixture(question_cases=3, revision_cases=3)
        )
        scorer.validate_coverage(facts)


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
                gold_fixture(question_cases=0, revision_cases=3),
            )
            with mock.patch.object(sys, "argv", ["score_semantic_v3.py", *arguments]):
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
                gold_fixture(question_cases=3, revision_cases=3),
            )
            with mock.patch.object(
                scorer, "run_v2_core", side_effect=RuntimeError("synthetic failure")
            ), mock.patch.object(
                sys, "argv", ["score_semantic_v3.py", *arguments]
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

    def _successful_core(self) -> dict:
        return {
            "totals": {
                "accepted_turns": 3,
                "uncertain_turns": 0,
                "route": 3,
                "rated": {"responsibility": 3, "tone": 3, "overall": 3},
                "rating_correct": {
                    "responsibility": 3,
                    "tone": 3,
                    "overall": 3,
                },
                "required_questions": 3,
                "required_questions_hit": 3,
                "question_claims": 3,
                "unsupported_question_claims": 0,
                "required_revisions": 3,
                "required_revisions_hit": 3,
                "revision_claims": 3,
                "unsupported_revision_claims": 0,
                "critical_violations": 0,
            },
            "case_results": [{"case_id": "T-1", "passed": True}],
            "gold_quality": {"synthetic": True},
            "matcher": {"synthetic": True},
        }

    def test_success_writes_evaluated_thresholds(self):
        with tempfile.TemporaryDirectory() as directory:
            arguments, report = self._arguments(
                Path(directory),
                gold_fixture(question_cases=3, revision_cases=3),
            )
            with mock.patch.object(
                scorer, "run_v2_core", return_value=self._successful_core()
            ), mock.patch.object(
                sys, "argv", ["score_semantic_v3.py", *arguments]
            ):
                scorer.main()
            document = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(document["status"], "SCORED")
            self.assertTrue(document["thresholds_passed"])
            self.assertEqual(document["not_applicable_metrics"], [])
            self.assertTrue(
                all(
                    value["status"] == "EVALUATED"
                    for value in document["metrics"].values()
                )
            )

    def test_required_zero_output_claim_metric_invalidates_scoring_input(self):
        with tempfile.TemporaryDirectory() as directory:
            arguments, report = self._arguments(
                Path(directory),
                gold_fixture(question_cases=3, revision_cases=3),
            )
            core = self._successful_core()
            core["totals"]["question_claims"] = 0
            with mock.patch.object(
                scorer, "run_v2_core", return_value=core
            ), mock.patch.object(
                sys, "argv", ["score_semantic_v3.py", *arguments]
            ):
                scorer.main()
            document = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(document["status"], "INVALID_SCORING_INPUT")
            self.assertIsNone(document["thresholds_passed"])
            self.assertIn(
                "question_claim_support_precision",
                document["not_applicable_metrics"],
            )


if __name__ == "__main__":
    unittest.main()
