#!/usr/bin/env python3
"""Copy dedicated v3.2 attempt-3 SUT outputs via git show. Do not merge those branches."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CLOUD = ROOT / "tests/benchmark/v3_2-holdout/attempt-3/cloud-cases"
RAW_DIR = CLOUD / "sut-raw"
ATT_DIR = CLOUD / "sut-attestations"
CANONICAL_PARENT = "4b09c2f7575b33cdc9f865200183cdd41eaa7117"
HOLDOUT = "cursor/blind-v323-holdout-17a0"
GOLD_MANIFEST = CLOUD / "gold-manifest-v323.json"
INPUT_MANIFEST = CLOUD / "sut-input-manifest.json"

SOURCES = [
    ("V323-001", "bc-bfd21a7d-69e4-5dab-8ec1-036e457abd3e", "cursor/v323-001-sut-17a0"),
    ("V323-002", "bc-e82004d2-041d-558d-816e-2a2118f9a765", "cursor/v323-002-sut-17a0"),
    ("V323-003", "bc-82aaa113-0da3-5367-8eca-1095eeb49dca", "cursor/v323-003-sut-17a0"),
    ("V323-004", "bc-54ecafa6-5a1c-54e3-960d-5bfd8a0c8b29", "cursor/v323-004-sut-17a0"),
    ("V323-005", "bc-855b4301-d51a-5ce8-b5ad-5f9972b18a20", "cursor/v323-005-sut-17a0"),
    ("V323-006", "bc-a1cdc3e0-8cd0-5386-9ac4-206d40723111", "cursor/v323-006-sut-17a0"),
    ("V323-007", "bc-bd9bfa34-cfb9-5999-beba-0d297b448fa9", "cursor/v323-007-sut-17a0"),
    ("V323-008", "bc-9b8edcb7-48bb-562b-aa48-1305b121fdf1", "cursor/v323-008-sut-17a0"),
    ("V323-009", "bc-9f8fc090-cda6-535f-882c-25b4c29932ff", "cursor/v323-009-sut-17a0"),
    ("V323-010", "bc-93c35904-652e-5dac-8359-3dcb5d6ef931", "cursor/v323-010-sut-17a0"),
    ("V323-011", "bc-a071b14e-f738-54ea-b74e-b855b70b0b67", "cursor/v323-011-sut-17a0"),
    ("V323-012", "bc-bdca1538-71ac-5a48-a3a9-3572a3662720", "cursor/v323-012-sut-17a0"),
    ("V323-013", "bc-30b27f84-82d8-588a-bfda-d49a21bb3142", "cursor/v323-013-sut-17a0"),
    ("V323-014", "bc-88be9191-959f-5243-86ab-dc007d3d74fa", "cursor/v323-014-sut-17a0"),
    ("V323-015", "bc-e0a15e2d-d628-515d-bdc1-13da6a8f72d2", "cursor/v323-015-sut-17a0"),
    ("V323-016", "bc-2f29443c-f524-553e-8516-2f6f2213cf67", "cursor/v323-016-sut-17a0"),
    ("V323-017", "bc-a94b4c99-e3f4-5058-bd7c-0df3e7cd8094", "cursor/v323-017-sut-17a0"),
    ("V323-018", "bc-9e4e0c27-2850-5d93-a2db-ba9f59e374d2", "cursor/v323-018-sut-17a0"),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_show(ref: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def rev_parse(ref: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", ref],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    ATT_DIR.mkdir(parents=True, exist_ok=True)
    inputs = json.loads(INPUT_MANIFEST.read_text(encoding="utf-8"))
    input_by_id = {item["case_id"]: item for item in inputs["cases"]}
    if digest(GOLD_MANIFEST) != inputs["parent_gold_manifest"]["sha256"]:
        raise ValueError("gold manifest hash drifted")

    index_cases = []
    aggregate_cases = []
    turn_total = 0
    for case_id, context_id, branch in SOURCES:
        subprocess.run(
            ["git", "fetch", "origin", branch],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
        tip = rev_parse(f"origin/{branch}")
        raw_rel = f"tests/benchmark/v3_2-holdout/attempt-3/cloud-cases/sut-raw/{case_id}.json"
        att_rel = f"tests/benchmark/v3_2-holdout/attempt-3/cloud-cases/sut-attestations/{case_id}.json"
        raw_bytes = git_show(f"origin/{branch}", raw_rel)
        att_bytes = git_show(f"origin/{branch}", att_rel)
        raw_sha = hashlib.sha256(raw_bytes).hexdigest()
        att_sha = hashlib.sha256(att_bytes).hexdigest()
        raw_path = RAW_DIR / f"{case_id}.json"
        att_path = ATT_DIR / f"{case_id}.json"
        raw_path.write_bytes(raw_bytes)
        att_path.write_bytes(att_bytes)
        raw = json.loads(raw_bytes)
        turns = raw["turns"]
        expected_turns = input_by_id[case_id]["turns"]
        if raw["case_id"] != case_id or len(turns) != expected_turns:
            raise ValueError(f"{case_id} turn coverage")
        if [turn["turn_index"] for turn in turns] != list(range(1, expected_turns + 1)):
            raise ValueError(f"{case_id} turn order")
        for turn in turns:
            if not isinstance(turn.get("output_raw"), str) or not turn["output_raw"].strip():
                raise ValueError(f"{case_id} empty output")
        att = json.loads(att_bytes)
        if att.get("gold_accessed") or att.get("other_cases_accessed") or att.get("question_design_accessed"):
            raise ValueError(f"{case_id} isolation")
        if att.get("skill_files_accessed") is not True:
            raise ValueError(f"{case_id} skill access")
        turn_total += len(turns)
        image_opened = case_id in {"V323-008", "V323-018"}
        index_cases.append(
            {
                "case_id": case_id,
                "context_id": context_id,
                "source_branch": branch,
                "delivery": "dedicated",
                "raw_commit": tip,
                "attestation_commit": tip,
                "raw_source_path": raw_rel,
                "attestation_source_path": att_rel,
                "source_raw_sha256": raw_sha,
                "source_attestation_sha256": att_sha,
                "canonical_raw_path": raw_rel,
                "canonical_attestation_path": att_rel,
                "canonical_raw_sha256": raw_sha,
                "canonical_attestation_sha256": att_sha,
                "markdown_wrapped": False,
            }
        )
        aggregate_cases.append(
            {
                "case_id": case_id,
                "generator_context_id": context_id,
                "requested_model_id": "gpt-5.6-sol-high-fast",
                "machine_model_id": "unverified",
                "runtime_commit": inputs["runtime_commit"],
                "input": {
                    "path": input_by_id[case_id]["path"],
                    "sha256": input_by_id[case_id]["sha256"],
                },
                "source": {
                    "raw_path": raw_rel,
                    "raw_sha256": raw_sha,
                    "attestation_path": att_rel,
                    "attestation_sha256": att_sha,
                    "branch": branch,
                    "output_commit": tip,
                    "raw_commit": tip,
                    "delivery": "dedicated",
                    "markdown_wrapped": False,
                    "source_raw_sha256": raw_sha,
                    "source_attestation_sha256": att_sha,
                },
                "audit": {
                    "verdict": "PASS",
                    "procedural_deviations": [],
                    "prohibited_content_access": False,
                    "image_opened_directly": image_opened,
                },
                "turn_outputs": [
                    {
                        "turn_index": turn["turn_index"],
                        "raw_output": turn["output_raw"],
                        "source_json_pointer": f"/turns/{index}/output_raw",
                    }
                    for index, turn in enumerate(turns)
                ],
            }
        )

    if turn_total != 24:
        raise ValueError(f"turn total {turn_total}")

    index = {
        "schema_version": "v3.2",
        "artifact": "sut-source-index",
        "canonical_parent_commit": CANONICAL_PARENT,
        "canonical_parent_role": "prepare-sut-inputs; gold freeze parent",
        "holdout_branch": HOLDOUT,
        "merged": False,
        "method": "git show",
        "cases": index_cases,
    }
    (CLOUD / "sut-source-index.json").write_text(json.dumps(index, indent=2) + "\n")
    aggregate = {
        "schema_version": "v3.2",
        "artifact": "sut-raw-outputs",
        "parent_gold_manifest": inputs["parent_gold_manifest"],
        "canonical_parent_commit": CANONICAL_PARENT,
        "runtime": {
            "runtime_commit": inputs["runtime_commit"],
            "runtime_sources": inputs["runtime_sources"],
        },
        "requested_model_id": "gpt-5.6-sol-high-fast",
        "machine_model_id": "unverified",
        "counts": {"cases": 18, "turns": 24},
        "cases": aggregate_cases,
    }
    (CLOUD / "outputs-v323-raw.json").write_text(
        json.dumps(aggregate, indent=2) + "\n", encoding="utf-8"
    )
    audits = {
        "schema_version": "v3.2",
        "artifact": "sut-protocol-audits",
        "distinct_cloud_contexts": 18,
        "shared_holdout_delivery": 0,
        "direct_image_opens": ["V323-008", "V323-018"],
        "prohibited_gold_or_other_case_access": 0,
        "cases": [
            {
                "case_id": case_id,
                "context_id": context_id,
                "verdict": "PASS",
            }
            for case_id, context_id, _ in SOURCES
        ],
    }
    (CLOUD / "sut-protocol-audits.json").write_text(json.dumps(audits, indent=2) + "\n")
    print("copied 18 dedicated SUT contexts, 24 turns")


if __name__ == "__main__":
    main()
