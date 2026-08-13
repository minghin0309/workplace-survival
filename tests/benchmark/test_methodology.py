import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import score_semantic
import validate_benchmark


ROOT = Path(__file__).resolve().parent


class BenchmarkMethodologyTests(unittest.TestCase):
    def _attestations(self, directory: Path) -> list[dict]:
        import hashlib

        values = []
        roles = ["labeler-1", "labeler-2", "labeler-3", "adjudicator"]
        families = ["claude", "grok", "kimi", "gpt"]
        for index, (role, family) in enumerate(zip(roles, families)):
            path = directory / f"attestation-{index}.json"
            path.write_text(
                json.dumps(
                    {
                        "context_id": f"context-{index}",
                        "model_id": f"model-{index}",
                        "model_family": family,
                        "cloud_branch": f"cursor/branch-{index}",
                        "cloud_commit": f"{index + 1:x}" * 40,
                        "files_read": ["cases.json"],
                        "limitations": ["No filesystem access log."],
                    }
                )
                + "\n"
            )
            values.append(
                {
                    "role": role,
                    "path": str(path),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                }
            )
        return values

    def _valid_gold_manifest(self, directory: Path) -> dict:
        import hashlib

        image = directory / "B2-001.png"
        image.write_bytes(b"\x89PNG\r\n\x1a\nfixture")
        cases = directory / "cases.json"
        cases.write_text(
            json.dumps(
                [
                    {
                        "case_id": "B2-001",
                        "turns": [{"turn_index": 1, "image_path": str(image)}],
                    }
                ]
            )
            + "\n"
        )
        artifacts = []
        for role in sorted(validate_benchmark.STAGE_ROLES["gold"]):
            path = cases if role == "cases" else directory / f"{role}.json"
            if path != cases:
                if role.endswith("-attestation"):
                    path.write_text(
                        json.dumps(
                            {
                                "context_id": f"{role}-context",
                                "model_id": f"{role}-model",
                                "model_family": role,
                                "cloud_branch": "cursor/example",
                                "cloud_commit": "a" * 40,
                                "files_read": ["cases.json"],
                                "limitations": ["No filesystem access log."],
                            }
                        )
                        + "\n"
                    )
                else:
                    path.write_text(json.dumps({"role": role}) + "\n")
            artifacts.append(
                {
                    "role": role,
                    "path": str(path),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "cloud_branch": "cursor/example",
                    "cloud_commit": "a" * 40,
                }
            )
        artifacts.append(
            {
                "role": "image:B2-001:1",
                "path": str(image),
                "sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
                "cloud_branch": "cursor/example",
                "cloud_commit": "a" * 40,
            }
        )
        return {
            "version": "2",
            "immutable": True,
            "stage": "gold",
            "parent_manifest": {"path": None, "sha256": "0" * 64},
            "frozen_at_utc": "2026-08-13T00:00:00Z",
            "artifacts": artifacts,
        }

    def test_ontology_alias_matches_semantic_concept(self):
        _, aliases = score_semantic.load_ontology(ROOT / "SEMANTIC_ONTOLOGY.json")
        claims = {
            "q1": {
                "claim_id": "q1",
                "text": "due-date",
                "evidence_span": "due-date",
            }
        }
        matches = [
            {
                "claim_id": "q1",
                "concept_id": "confirmed-deadline",
                "match_type": "alias",
                "confidence": 1.0,
                "rationale": "Registered ontology alias.",
            }
        ]
        matched, unsupported = score_semantic.validate_match_set(
            matches,
            claims,
            "question",
            {"confirmed-deadline"},
            aliases,
            "test",
        )
        self.assertEqual(matched, {"confirmed-deadline"})
        self.assertEqual(unsupported, 0)

    def test_unsupported_claim_is_counted(self):
        _, aliases = score_semantic.load_ontology(ROOT / "SEMANTIC_ONTOLOGY.json")
        claims = {
            "r1": {
                "claim_id": "r1",
                "text": "invented-owner",
                "evidence_span": "Jamie owns it.",
            }
        }
        matched, unsupported = score_semantic.validate_match_set(
            [
                {
                    "claim_id": "r1",
                    "concept_id": None,
                    "match_type": "unsupported",
                    "confidence": 1.0,
                    "rationale": "No allowed concept supports this claim.",
                }
            ],
            claims,
            "revision",
            {"preserve-confirmed-owner"},
            aliases,
            "test",
        )
        self.assertEqual(matched, set())
        self.assertEqual(unsupported, 1)

    def test_weak_semantic_match_is_rejected(self):
        _, aliases = score_semantic.load_ontology(ROOT / "SEMANTIC_ONTOLOGY.json")
        with self.assertRaises(ValueError):
            score_semantic.validate_match_set(
                [
                    {
                        "claim_id": "q1",
                        "concept_id": "current-root-cause",
                        "match_type": "semantic",
                        "confidence": 0.5,
                        "rationale": "Weak guess.",
                    }
                ],
                {
                    "q1": {
                        "claim_id": "q1",
                        "text": "what happened",
                        "evidence_span": "What happened?",
                    }
                },
                "question",
                {"current-root-cause"},
                aliases,
                "test",
            )

    def test_omitted_claim_match_is_rejected(self):
        _, aliases = score_semantic.load_ontology(ROOT / "SEMANTIC_ONTOLOGY.json")
        claims = {
            "q1": {"claim_id": "q1", "text": "first", "evidence_span": "first"},
            "q2": {"claim_id": "q2", "text": "second", "evidence_span": "second"},
        }
        with self.assertRaises(ValueError):
            score_semantic.validate_match_set(
                [
                    {
                        "claim_id": "q1",
                        "concept_id": None,
                        "match_type": "unsupported",
                        "confidence": 1.0,
                        "rationale": "No match.",
                    }
                ],
                claims,
                "question",
                set(),
                aliases,
                "test",
            )

    def test_case_designer_notes_are_rejected(self):
        case = {
            "case_id": "B2-001",
            "category": "green_control",
            "recipient_context": "Direct manager",
            "data_a": "Alex owns the report.",
            "turns": [{"turn_index": 1, "input_raw": "Alex owns it.", "image_path": None}],
            "image_spec": None,
            "case_designer_notes": "Hidden fact",
        }
        note = {
            "case_id": "B2-001",
            "design_intent": "Green control",
            "difficulty_notes": "None",
        }
        with self.assertRaises(ValueError):
            validate_benchmark.validate_cases([case], [note])

    def test_changed_cloud_artifact_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            parent = directory / "parent.json"
            parent.write_text('{"parent": true}\n')
            path = directory / "artifact.json"
            path.write_text('{"value": 1}\n')
            import hashlib

            manifest = {
                "version": "2",
                "immutable": True,
                "stage": "outputs",
                "parent_manifest": {
                    "path": str(parent),
                    "sha256": hashlib.sha256(parent.read_bytes()).hexdigest(),
                },
                "artifacts": [
                    {
                        "role": "outputs",
                        "path": str(path),
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "cloud_branch": "cursor/example",
                        "cloud_commit": "a" * 40,
                    }
                ],
            }
            path.write_text('{"value": 2}\n')
            with self.assertRaises(ValueError):
                validate_benchmark.validate_manifest(manifest)

    def test_valid_parent_chained_cloud_manifests(self):
        import hashlib

        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            gold = self._valid_gold_manifest(directory)
            gold_path = directory / "gold-manifest.json"
            gold_path.write_text(json.dumps(gold) + "\n")
            outputs = directory / "outputs.json"
            outputs.write_text('{"outputs": []}\n')
            generator_attestation = directory / "generator-attestation.json"
            generator_attestation.write_text(
                json.dumps(
                    {
                        "context_id": "generator-context",
                        "model_id": "generator-model",
                        "model_family": "gpt",
                        "cloud_branch": "cursor/example",
                        "cloud_commit": "b" * 40,
                        "files_read": ["cases.json"],
                        "limitations": ["No filesystem access log."],
                    }
                )
                + "\n"
            )
            manifest = {
                "version": "2",
                "immutable": True,
                "stage": "outputs",
                "parent_manifest": {
                    "path": str(gold_path),
                    "sha256": hashlib.sha256(gold_path.read_bytes()).hexdigest(),
                },
                "frozen_at_utc": "2026-08-13T00:01:00Z",
                "artifacts": [
                    {
                        "role": "outputs",
                        "path": str(outputs),
                        "sha256": hashlib.sha256(outputs.read_bytes()).hexdigest(),
                        "cloud_branch": "cursor/example",
                        "cloud_commit": "b" * 40,
                    },
                    {
                        "role": "generator-attestation",
                        "path": str(generator_attestation),
                        "sha256": hashlib.sha256(
                            generator_attestation.read_bytes()
                        ).hexdigest(),
                        "cloud_branch": "cursor/example",
                        "cloud_commit": "b" * 40,
                    },
                ],
            }
            validate_benchmark.validate_manifest(manifest)

    def test_generator_oracle_note_access_is_rejected(self):
        import hashlib

        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            gold = self._valid_gold_manifest(directory)
            gold_path = directory / "gold-manifest.json"
            gold_path.write_text(json.dumps(gold) + "\n")
            outputs = directory / "outputs.json"
            outputs.write_text('{"outputs": []}\n')
            attestation = directory / "generator-attestation.json"
            attestation.write_text(
                json.dumps(
                    {
                        "context_id": "generator-context",
                        "model_id": "generator-model",
                        "model_family": "gpt",
                        "cloud_branch": "cursor/example",
                        "cloud_commit": "b" * 40,
                        "files_read": ["oracle-notes.json"],
                        "limitations": ["No filesystem access log."],
                    }
                )
                + "\n"
            )
            manifest = {
                "version": "2",
                "immutable": True,
                "stage": "outputs",
                "parent_manifest": {
                    "path": str(gold_path),
                    "sha256": hashlib.sha256(gold_path.read_bytes()).hexdigest(),
                },
                "frozen_at_utc": "2026-08-13T00:01:00Z",
                "artifacts": [
                    {
                        "role": "outputs",
                        "path": str(outputs),
                        "sha256": hashlib.sha256(outputs.read_bytes()).hexdigest(),
                        "cloud_branch": "cursor/example",
                        "cloud_commit": "b" * 40,
                    },
                    {
                        "role": "generator-attestation",
                        "path": str(attestation),
                        "sha256": hashlib.sha256(attestation.read_bytes()).hexdigest(),
                        "cloud_branch": "cursor/example",
                        "cloud_commit": "b" * 40,
                    },
                ],
            }
            with self.assertRaises(ValueError):
                validate_benchmark.validate_manifest(manifest)

    def test_missing_cloud_artifact_roles_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            parent = directory / "parent.json"
            parent.write_text('{"parent": true}\n')
            artifact = directory / "artifact.json"
            artifact.write_text('{"value": 1}\n')
            import hashlib

            manifest = {
                "version": "2",
                "immutable": True,
                "stage": "outputs",
                "parent_manifest": {
                    "path": str(parent),
                    "sha256": hashlib.sha256(parent.read_bytes()).hexdigest(),
                },
                "artifacts": [
                    {
                        "role": "wrong-role",
                        "path": str(artifact),
                        "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
                        "cloud_branch": "cursor/example",
                        "cloud_commit": "a" * 40,
                    }
                ],
            }
            with self.assertRaises(ValueError):
                validate_benchmark.validate_manifest(manifest)

    def test_invalid_attestation_content_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            attestations = self._attestations(directory)
            Path(attestations[0]["path"]).write_text('{"index": 0}\n')
            import hashlib

            attestations[0]["sha256"] = hashlib.sha256(
                Path(attestations[0]["path"]).read_bytes()
            ).hexdigest()
            gold = {
                "gold_quality": {
                    "labeler_model_families": ["claude", "grok", "kimi"],
                    "adjudicator_model_family": "gpt",
                    "human_review_available": False,
                    "adjudication_complete": True,
                    "vote_distributions_preserved": True,
                    "attestations": attestations,
                },
                "cases": [],
            }
            with self.assertRaises(ValueError):
                validate_benchmark.validate_gold(gold)

    def test_attestation_family_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            attestations = self._attestations(directory)
            path = Path(attestations[0]["path"])
            document = json.loads(path.read_text())
            document["model_family"] = "wrong-family"
            path.write_text(json.dumps(document) + "\n")
            import hashlib

            attestations[0]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            gold = {
                "gold_quality": {
                    "labeler_model_families": ["claude", "grok", "kimi"],
                    "adjudicator_model_family": "gpt",
                    "human_review_available": False,
                    "adjudication_complete": True,
                    "vote_distributions_preserved": True,
                    "attestations": attestations,
                },
                "cases": [],
            }
            with self.assertRaises(ValueError):
                validate_benchmark.validate_gold(gold)

    def test_missing_image_turn_artifact_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            manifest = self._valid_gold_manifest(directory)
            cases_entry = next(
                item for item in manifest["artifacts"] if item["role"] == "cases"
            )
            cases_path = Path(cases_entry["path"])
            second_image = directory / "B2-001-turn2.png"
            second_image.write_bytes(b"\x89PNG\r\n\x1a\nsecond")
            cases_path.write_text(
                json.dumps(
                    [
                        {
                            "case_id": "B2-001",
                            "turns": [
                                {"turn_index": 1, "image_path": str(directory / "B2-001.png")},
                                {"turn_index": 2, "image_path": str(second_image)},
                            ],
                        }
                    ]
                )
                + "\n"
            )
            import hashlib

            cases_entry["sha256"] = hashlib.sha256(cases_path.read_bytes()).hexdigest()
            with self.assertRaises(ValueError):
                validate_benchmark.validate_manifest(manifest)

    def test_excessive_gold_uncertainty_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            gold = {
                "gold_quality": {
                    "labeler_model_families": ["claude", "grok", "kimi"],
                    "adjudicator_model_family": "gpt",
                    "human_review_available": False,
                    "adjudication_complete": True,
                    "vote_distributions_preserved": True,
                    "attestations": self._attestations(Path(directory)),
                },
                "cases": [
                    {
                        "case_id": "B2-001",
                        "turn_labels": [
                            {
                                "gold_quality": {
                                    "tier": "gold_uncertain",
                                    "three_way_categorical_disagreement": True,
                                    "critical_invariant_disagreement": False,
                                    "human_reviewed": False,
                                    "unresolved_adjudication": True,
                                }
                            }
                        ],
                    }
                ],
            }
            with self.assertRaises(ValueError):
                validate_benchmark.validate_gold(gold)

    def test_invalid_human_review_tier_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            gold = {
                "gold_quality": {
                    "labeler_model_families": ["claude", "grok", "kimi"],
                    "adjudicator_model_family": "gpt",
                    "human_review_available": False,
                    "adjudication_complete": True,
                    "vote_distributions_preserved": True,
                    "attestations": self._attestations(Path(directory)),
                },
                "cases": [
                    {
                        "case_id": "B2-001",
                        "turn_labels": [
                            {
                                "gold_quality": {
                                    "tier": "human_reviewed",
                                    "three_way_categorical_disagreement": False,
                                    "critical_invariant_disagreement": False,
                                    "human_reviewed": False,
                                    "unresolved_adjudication": False,
                                }
                            }
                        ],
                    }
                ],
            }
            with self.assertRaises(ValueError):
                validate_benchmark.validate_gold(gold)

    def test_adjudication_requires_sha256_and_exact_gold_linkage(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory / "source.json"
            source.write_text('{"source": true}\n')
            attestation = directory / "adjudicator.json"
            attestation.write_text('{"attestation": true}\n')
            import hashlib

            source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            attestation_hash = hashlib.sha256(attestation.read_bytes()).hexdigest()
            turn = {
                "turn_index": 1,
                "route": "Normal mode",
                "ratings": {"responsibility": "Green", "tone": "Green"},
                "overall": "Green",
                "required_question_concepts": [],
                "allowed_question_concepts": [],
                "required_revision_concepts": ["no-revision"],
                "allowed_revision_concepts": ["no-revision"],
                "concept_definitions": {},
                "critical_invariants": ["no-invented-facts"],
                "rationale": "Supported.",
                "gold_quality": {
                    "tier": "heterogeneous_adjudicated",
                    "three_way_categorical_disagreement": False,
                    "critical_invariant_disagreement": False,
                    "human_reviewed": False,
                    "unresolved_adjudication": False,
                },
            }
            gold = {
                "case_set_id": "test-set",
                "cases": [{"case_id": "B2-001", "turn_labels": [turn]}],
            }
            adjudication = {
                "schema_version": "v2",
                "artifact": "gold-adjudication",
                "case_set_id": "test-set",
                "gold_output_path": "gold.json",
                "adjudicator_attestation": {
                    "path": str(attestation),
                    "sha256": attestation_hash,
                },
                "source_hashes": {str(source): source_hash},
                "adjudication_policy": ["Preserve votes."],
                "summary": {
                    "turns": 1,
                    "uncertain_turn_count": 0,
                    "uncertain_fraction": 0.0,
                },
                "cases": [
                    {
                        "case_id": "B2-001",
                        "turn_adjudications": [
                            {
                                "turn_index": 1,
                                "labeler_votes": {
                                    "gold-labeler-1": {},
                                    "gold-labeler-2": {},
                                    "gold-labeler-3": {},
                                },
                                "categorical_vote_distribution": {
                                    field: {"Green": 3}
                                    for field in ("route", "responsibility", "tone", "overall")
                                },
                                "adjudicated_turn": turn,
                            }
                        ],
                    }
                ],
            }
            validate_benchmark.validate_adjudication(adjudication, gold)
            adjudication["adjudicator_attestation"]["hash"] = adjudication[
                "adjudicator_attestation"
            ].pop("sha256")
            with self.assertRaisesRegex(ValueError, "adjudicator attestation schema"):
                validate_benchmark.validate_adjudication(adjudication, gold)


if __name__ == "__main__":
    unittest.main()
