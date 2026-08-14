#!/usr/bin/env python3
"""Copy dedicated v3.2 attempt-2 SUT outputs via git show. Do not merge those branches."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CLOUD = ROOT / "tests/benchmark/v3_2-holdout/attempt-2/cloud-cases"
RAW_DIR = CLOUD / "sut-raw"
ATT_DIR = CLOUD / "sut-attestations"
CANONICAL_PARENT = "1dee74484c7913b5b1b74153c3ece33334c3b684"
HOLDOUT = "cursor/blind-v322-holdout-17a0"
GOLD_MANIFEST = CLOUD / "gold-manifest-v322.json"
INPUT_MANIFEST = CLOUD / "sut-input-manifest.json"

SOURCES = [
    ("V322-001", "bc-8ed91aeb-2ade-5c39-802c-ad1268f2da45", "cursor/v322-001-sut-17a0", "32062525a2013b0189fed9a555e2ed6403ec77a62efc744ae5c68ce5cc9acf64", "b23b6d0edfa176a0494f2d58d8bdb90e98a968d1f9c5dddcb58280fdecb2b413"),
    ("V322-002", "bc-ef16d173-7826-5db7-8450-c23c549a142b", "cursor/v322-002-sut-17a0", "5083b7bd5f237b960f97485c67438eaf32cbccb3790df6a3af922c14d0afc9ed", "2e2f9c621ad9c74cf1469badbba7cc177bfd455acc7c8534150265fee6c0c832"),
    ("V322-003", "bc-bdc1c371-f667-5d47-abad-78e389c4351a", "cursor/v322-003-sut-17a0", "5fab9503d8c55584024179e1d2015660cfbc33ac1ea8e5254e7945ed4db79bac", "a33f23ae5a9a7e98f083f55e50ad9c5d7d86f082bf6a1b01af8fd9068b2cda97"),
    ("V322-004", "bc-fefcbe5c-533e-5757-b682-b0d5874a071e", "cursor/v322-004-sut-17a0", "f3eb7585d911165c7554c9c1d3b10a07a60bcd7eed35963f922165c9dbad1e94", "27cb19a1aa65b5b8ceea95887d30f714283fdd401f53f1639d6e0799a42b4023"),
    ("V322-005", "bc-6df4b8e3-cac8-5b80-828c-4ee0b1462049", "cursor/v322-005-sut-17a0-2049", "5e8a04bbfa44bc3d57b402482c643a327baba63c3e4c48ad916e21f68fbe1a24", "a5d391498de0b7fc411386dc3844b94c744ba5eadc45b4097156dac5459953b1"),
    ("V322-006", "bc-3b2616d1-a42b-5ffe-bdfb-c4661f6630af", "cursor/v322-006-sut-17a0", "553c99d8ba0f105045fb13e4183496ba61fc47e450d814e95e6712fea5ae4d21", "d334d804bcb79fde48bc6d60af7b1d8343d8eea561ffeaba2bd7845cdcdb7075"),
    ("V322-007", "bc-d6ff2936-3264-55e1-88f1-d67c6097c40d", "cursor/v322-007-sut-17a0", "85aac329dac3d167abf9fc83bad01f5b6cccaffc0bc16b43094f7c8086b86c10", "a0ee8f8ceeff33e2ad85541d004857c11d35c67b0ad9e7ede641b32a3527ecec"),
    ("V322-008", "bc-3d06dd2a-dbf6-5df1-b9f7-53bce4748887", "cursor/v322-008-sut-17a0", "55ed36b4cf82d1c06063e9f344f9353b3ad26fc510b20641a46fff1f084ad916", "bb7da19100a2f58f2c1ae91c07fe83ef0b7fe29e321678add0dcf768f28e9bce"),
    ("V322-009", "bc-b27cb5ec-ba62-59c3-a920-fb5f210f5f4f", "cursor/v322-009-sut-17a0", "0103500d3b799addfaefaf3a2b44e1787bce9ba6803b6b5ecb97e1d640807368", "e5878bf1a1f1e72da5cdffb020ebf84cfed99db4edf1a140db3b71e7c0555235"),
    ("V322-010", "bc-d60fcaac-6fc7-59d8-b845-36ab81841a3b", "cursor/v322-010-sut-17a0", "7e094a3f7b7a6d25838095d025e0ab889029b9ba519ed5e2928eaa035329a975", "4e44e8d3c5b4816d7b394c3d759c9f4d040aedafc6f2e37aa3503c29dbeb9ed0"),
    ("V322-011", "bc-70c8286f-f859-54b7-a9c3-64fece64ff5c", "cursor/v322-011-sut-17a0", "3f719f43c837ef5447c319c97d8e2ca6645fdd54d074fb12957bf9f56da9b4b8", "d3ae47886a730f22c30ffdec574dca26e23cf3b6e3666473d0f033772d6d529a"),
    ("V322-012", "bc-4d0d28cf-3dae-554a-aaaf-ff5789e83a0d", "cursor/v322-012-sut-17a0", "aa62dc19ba1486f1cb51a19f287f58eca2e269f8d8fb4699b45af8e11e3c03e4", "1ce84a3b2be805aa85fc475a6857ddd8dd5731690a84ad8ff98fed377abb8f36"),
    ("V322-013", "bc-629e3b2c-be66-51d6-aade-cf3b846128ef", "cursor/v322-013-sut-17a0", "b5741d9cc038fa6c0b504f49d60b06a0063677646bb1d4cbe27a52e7210a8605", "1df8cb701949c4f3cd95a1f086a84801cc61bc0a62da6f6914645ab1d28e4729"),
    ("V322-014", "bc-13f762de-0258-51b1-9f34-c546359d8956", "cursor/v322-014-sut-17a0", "4e98c8398930471c1d373b902b1bfa997781931ca19c6ea50b3e071565e5def6", "40aa8c603f1fa1ddbcec9a3c34241a077813fafadaa04debe5329d2ce4c6138e"),
    ("V322-015", "bc-1a647b2d-3458-52be-94c0-de2f59a60a9e", "cursor/v322-015-sut-17a0", "6459f76ee6a4ded113634113c54a279f18980ace8d1624b8e28dbe64c7be7375", "69fddcb5bc740bbab86f901ccbb27f4dd395dcdb34762028704cd86e8a5ef276"),
    ("V322-016", "bc-3b6dc286-bef4-5fa2-bb4a-d862a32338c6", "cursor/v322-016-sut-17a0", "65c7e522535269d255cc1c5257d2a56ca720d9e3239d891b3315dc7dc225e0e7", "0ca910f3a8f9fcc6dfa85c8293b4afaea761589cd97b018e8f36d10fb9722bed"),
    ("V322-017", "bc-b575ed05-5008-5236-a109-117892b02795", "cursor/v322-017-sut-17a0", "274c71c1270132161458ddd6746df8e1292e720c5056f81b1ad44b5b0fc18d93", "1dad8df404fbe6b0ada0c7d738a81f124fd20e899d8a5f7df7dd0ef6fd0dc559"),
    ("V322-018", "bc-373991e1-e0fd-54b9-8fb6-e5dff74cc1c9", "cursor/v322-018-sut-17a0", "404fff60b04dd2e3797ff5f8312236daa2cfae75b67699b9a848fbc45afe0ace", "ec99013d859b2d853a76e3438496e2cdec009f99095fee8dd0e514fe1e262527"),
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
    for case_id, context_id, branch, raw_sha, att_sha in SOURCES:
        subprocess.run(["git", "fetch", "origin", branch], cwd=ROOT, check=True, capture_output=True)
        tip = rev_parse(f"origin/{branch}")
        raw_rel = f"tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/sut-raw/{case_id}.json"
        att_rel = f"tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/sut-attestations/{case_id}.json"
        raw_bytes = git_show(f"origin/{branch}", raw_rel)
        att_bytes = git_show(f"origin/{branch}", att_rel)
        if hashlib.sha256(raw_bytes).hexdigest() != raw_sha:
            raise ValueError(f"{case_id} raw hash")
        if hashlib.sha256(att_bytes).hexdigest() != att_sha:
            raise ValueError(f"{case_id} attestation hash")
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
        turn_total += len(turns)
        image_opened = case_id in {"V322-008", "V322-018"}
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
    (CLOUD / "outputs-v322-raw.json").write_text(
        json.dumps(aggregate, indent=2) + "\n", encoding="utf-8"
    )
    audits = {
        "schema_version": "v3.2",
        "artifact": "sut-protocol-audits",
        "distinct_cloud_contexts": 18,
        "shared_holdout_delivery": 0,
        "direct_image_opens": ["V322-008", "V322-018"],
        "prohibited_gold_or_other_case_access": 0,
        "cases": [
            {
                "case_id": case_id,
                "context_id": context_id,
                "verdict": "PASS",
            }
            for case_id, context_id, *_ in SOURCES
        ],
    }
    (CLOUD / "sut-protocol-audits.json").write_text(json.dumps(audits, indent=2) + "\n")
    print("copied 18 dedicated SUT contexts, 24 turns")


if __name__ == "__main__":
    main()
