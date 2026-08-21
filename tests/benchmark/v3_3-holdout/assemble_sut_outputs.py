#!/usr/bin/env python3
"""Copy dedicated v3.3 attempt-1 SUT outputs via git show. Do not merge those branches."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CLOUD = ROOT / "tests/benchmark/v3_3-holdout/cloud-cases"
RAW_DIR = CLOUD / "sut-raw"
ATT_DIR = CLOUD / "sut-attestations"
CANONICAL_PARENT = "249806bf5093d698265b5113b73d549a81633a5a"
HOLDOUT = "cursor/blind-v33-holdout-17a0"
GOLD_MANIFEST = CLOUD / "gold-manifest-v33.json"
INPUT_MANIFEST = CLOUD / "sut-input-manifest.json"
REQUESTED_MODEL = "inherit"
IMAGE_OPENS = {"V33-008", "V33-018"}

SOURCES = [
    ("V33-001", "bc-7f8abf82-614c-55ea-bcfa-69dfbf78afc1", "cursor/v33-001-sut-17a0"),
    ("V33-002", "bc-05aed183-eab3-51ae-84ee-f0aac9f1f053", "cursor/v33-002-sut-17a0"),
    ("V33-003", "bc-1d281964-ccf4-542e-9e02-e8af775c299a", "cursor/v33-003-sut-17a0"),
    ("V33-004", "bc-1d375675-1943-528d-977a-7a6468c4040b", "cursor/v33-004-sut-17a0"),
    ("V33-005", "bc-94411713-75b4-54fa-8f9a-ba2be808e8b5", "cursor/v33-005-sut-17a0"),
    ("V33-006", "bc-1e556a03-877b-54ed-8b7e-0465bb64fc92", "cursor/v33-006-sut-17a0"),
    ("V33-007", "bc-91ce3dab-914d-5456-a5ab-7eb726a4fa5e", "cursor/v33-007-sut-17a0"),
    ("V33-008", "bc-672d2e1d-7861-5352-bc5d-7b56ba4141f3", "cursor/v33-008-sut-17a0"),
    ("V33-009", "bc-dc842e47-c25f-5277-9168-8819fc882064", "cursor/v33-009-sut-17a0"),
    ("V33-010", "bc-028d6530-587a-5450-9206-5bbfa0035d7b", "cursor/v33-010-sut-17a0"),
    ("V33-011", "bc-fa7e26b9-e683-5016-94af-02fb69725239", "cursor/v33-011-sut-17a0"),
    ("V33-012", "bc-70faf7e6-b3e2-5855-bb26-b2e4d2d5a36f", "cursor/v33-012-sut-17a0"),
    ("V33-013", "bc-23cdcc5d-6327-5b4b-a398-ff6e0eb99707", "cursor/v33-013-sut-17a0"),
    ("V33-014", "bc-1a10f2f2-1cfe-564a-a583-8450ef1d7d52", "cursor/v33-014-sut-17a0"),
    ("V33-015", "bc-5a99ccfd-3baa-5d24-a262-c6f4dbeb1b6b", "cursor/v33-015-sut-17a0"),
    ("V33-016", "bc-5d320c7a-45f9-5b3f-b8d7-485d8940576d", "cursor/v33-016-sut-17a0"),
    ("V33-017", "bc-1beb14a6-1969-5a83-a7c6-7316e6e7ce08", "cursor/v33-017-sut-17a0"),
    ("V33-018", "bc-a8355044-2e33-528d-8fd9-d7b072efc0a4", "cursor/v33-018-sut-17a0"),
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
        raw_rel = f"tests/benchmark/v3_3-holdout/cloud-cases/sut-raw/{case_id}.json"
        att_rel = f"tests/benchmark/v3_3-holdout/cloud-cases/sut-attestations/{case_id}.json"
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
        if att.get("gold_accessed") or att.get("other_cases_accessed") or att.get(
            "question_design_accessed"
        ):
            raise ValueError(f"{case_id} isolation")
        if att.get("skill_files_accessed") is not True:
            raise ValueError(f"{case_id} skill access")
        png_read = any(
            str(item.get("path", "")).endswith(".png") for item in att.get("files_read", [])
        )
        image_opened = case_id in IMAGE_OPENS
        if png_read != image_opened:
            raise ValueError(f"{case_id} image-open attestation")
        turn_total += len(turns)
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
                "requested_model_id": REQUESTED_MODEL,
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
        "schema_version": "v3.3",
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
        "schema_version": "v3.3",
        "artifact": "sut-raw-outputs",
        "parent_gold_manifest": inputs["parent_gold_manifest"],
        "canonical_parent_commit": CANONICAL_PARENT,
        "runtime": {
            "runtime_commit": inputs["runtime_commit"],
            "runtime_sources": inputs["runtime_sources"],
        },
        "requested_model_id": REQUESTED_MODEL,
        "machine_model_id": "unverified",
        "counts": {"cases": 18, "turns": 24},
        "cases": aggregate_cases,
    }
    (CLOUD / "outputs-v33-raw.json").write_text(
        json.dumps(aggregate, indent=2) + "\n", encoding="utf-8"
    )
    audits = {
        "schema_version": "v3.3",
        "artifact": "sut-protocol-audits",
        "distinct_cloud_contexts": 18,
        "shared_holdout_delivery": 0,
        "direct_image_opens": sorted(IMAGE_OPENS),
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
