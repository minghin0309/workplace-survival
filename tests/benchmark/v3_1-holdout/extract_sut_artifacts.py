#!/usr/bin/env python3
"""Extract each v3.1 SUT case from its own source commit. Do not merge the shared holdout."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CLOUD = ROOT / "tests/benchmark/v3_1-holdout/cloud-cases"
RAW_DIR = CLOUD / "sut-raw"
ATT_DIR = CLOUD / "sut-attestations"
CANONICAL_PARENT = "f609800eba5f3e8f20b541f7776c1a427ca8aed2"
DELIVERY_BRANCH = "cursor/v31-sut-shared-delivery-17a0"
DELIVERY_TIP = "a65e26961880130f237345c4ea74843b06399c22"
HOLDOUT_BRANCH = "cursor/blind-v31-holdout-17a0"

SOURCES = [
    {
        "case_id": "V31-001",
        "context_id": "bc-9d6cea32-519e-5bab-8ba0-e43bb1564a8e",
        "source_branch": "cursor/v31-001-sut-4a8e",
        "raw_commit": "a10702675fb745be18a2c83df563fffc67e910e0",
        "attestation_commit": "a10702675fb745be18a2c83df563fffc67e910e0",
        "raw_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-001.json",
        "attestation_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-attestations/V31-001.json",
        "delivery": "dedicated",
    },
    {
        "case_id": "V31-002",
        "context_id": "bc-15751b57-3800-5a37-86b6-8bbcc485a4c7",
        "source_branch": "cursor/v31-002-sut-a4c7",
        "raw_commit": "18bc987455a41466a7c3daf0bd412189f34696e1",
        "attestation_commit": "18bc987455a41466a7c3daf0bd412189f34696e1",
        "raw_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-002.json",
        "attestation_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-attestations/V31-002.json",
        "delivery": "dedicated",
    },
    {
        "case_id": "V31-003",
        "context_id": "bc-526c146f-1d81-5641-833e-a93c81fe687a",
        "source_branch": DELIVERY_BRANCH,
        "raw_commit": "07b22606abfb0636a8a4ef2946fbc4848343cf72",
        "attestation_commit": "367fcdc550789bbd2828511fa5007f88f0c5b1e7",
        "raw_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-003.json",
        "attestation_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-003.attestation.json",
        "delivery": "shared_holdout",
    },
    {
        "case_id": "V31-004",
        "context_id": "bc-5d7b8c7f-43db-5dee-844a-a8f4ce093a46",
        "source_branch": "cursor/v31-004-sut-3a46",
        "raw_commit": "50e5652dcf5f4738523d1b3a035b49d03f00c25f",
        "attestation_commit": "50e5652dcf5f4738523d1b3a035b49d03f00c25f",
        "raw_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-004.json",
        "attestation_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-attestations/V31-004.json",
        "delivery": "dedicated",
    },
    {
        "case_id": "V31-005",
        "context_id": "bc-ca0c5b2f-44ff-5eb0-9e5b-b4976b87fa0e",
        "source_branch": "cursor/v31-005-sut-fa0e",
        "raw_commit": "d2c6ff0f5caf12b9ec0db131d8f4ba935c363fdb",
        "attestation_commit": "d2c6ff0f5caf12b9ec0db131d8f4ba935c363fdb",
        "raw_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-005.md",
        "attestation_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-attestations/V31-005.json",
        "delivery": "dedicated",
    },
    {
        "case_id": "V31-006",
        "context_id": "bc-4ed20476-3c8a-5597-bb97-9e8c4fea371a",
        "source_branch": "cursor/v31-006-sut-371a",
        "raw_commit": "b909b51579d9affef2000912ff4b0fca12866edd",
        "attestation_commit": "b909b51579d9affef2000912ff4b0fca12866edd",
        "raw_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-outputs/V31-006.json",
        "attestation_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/attestations/V31-006.json",
        "delivery": "dedicated",
    },
    {
        "case_id": "V31-007",
        "context_id": "bc-05ddddf3-b881-5814-b849-89ca3f4ecfd5",
        "source_branch": "cursor/v31-007-sut-cfd5",
        "raw_commit": "0f98d9a486e76b39c0be8e308790ed82f6b16860",
        "attestation_commit": "0f98d9a486e76b39c0be8e308790ed82f6b16860",
        "raw_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-007.md",
        "attestation_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-attestations/V31-007.json",
        "delivery": "dedicated",
    },
    {
        "case_id": "V31-008",
        "context_id": "bc-0f429f5c-5c3d-5f19-b699-c4a238e8ef3f",
        "source_branch": "cursor/v31-008-sut-ef3f",
        "raw_commit": "f8077fcd5925f74fa35accd9fec4ba041cb80779",
        "attestation_commit": "f8077fcd5925f74fa35accd9fec4ba041cb80779",
        "raw_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-v31-raw.json",
        "attestation_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-v31-raw-attestation.json",
        "delivery": "dedicated",
    },
    {
        "case_id": "V31-009",
        "context_id": "bc-6ef7a0a5-961f-5ed3-bbe0-6249a5ebc521",
        "source_branch": "cursor/v31-009-sut-c521",
        "raw_commit": "fb64dc15f6875f03543e00843edf9505d35f3081",
        "attestation_commit": "fb64dc15f6875f03543e00843edf9505d35f3081",
        "raw_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-outputs/V31-009.md",
        "attestation_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/attestations/V31-009.json",
        "delivery": "dedicated",
    },
    {
        "case_id": "V31-010",
        "context_id": "bc-fa10bc11-9547-56c4-bf31-c1ab8ed376a3",
        "source_branch": "cursor/v31-010-sut-76a3",
        "raw_commit": "b4cbda822e6fd74fa13e4981f4c5fa731b4ec777",
        "attestation_commit": "b4cbda822e6fd74fa13e4981f4c5fa731b4ec777",
        "raw_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-010.md",
        "attestation_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-attestations/V31-010.json",
        "delivery": "dedicated",
    },
    {
        "case_id": "V31-011",
        "context_id": "bc-03abd61b-1348-5597-84ad-ea70a9d60f0b",
        "source_branch": DELIVERY_BRANCH,
        "raw_commit": "6f5062627285a1f48aae589292bfaa5140ae4cc0",
        "attestation_commit": "6f5062627285a1f48aae589292bfaa5140ae4cc0",
        "raw_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-011.json",
        "attestation_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-011.attestation.json",
        "delivery": "shared_holdout",
    },
    {
        "case_id": "V31-012",
        "context_id": "bc-970f87a6-addd-5c59-8bea-c0c52f45c696",
        "source_branch": "cursor/workplace-survival-v31-012-c696",
        "raw_commit": "95a112d9fff0dcc227fe3a0b2edce607871e4f95",
        "attestation_commit": "95a112d9fff0dcc227fe3a0b2edce607871e4f95",
        "raw_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-012.json",
        "attestation_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-012.attestation.json",
        "delivery": "dedicated_misnamed",
    },
    {
        "case_id": "V31-013",
        "context_id": "bc-dbd0f64b-7608-5483-a4b2-f8691737404b",
        "source_branch": "cursor/v31-013-sut-404b",
        "raw_commit": "9bf592c45cd718b57faeda5195856bbc79a6a8a1",
        "attestation_commit": "9bf592c45cd718b57faeda5195856bbc79a6a8a1",
        "raw_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-013.json",
        "attestation_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-013.attestation.json",
        "delivery": "dedicated",
    },
    {
        "case_id": "V31-014",
        "context_id": "bc-5311e780-52e2-5b0d-8e66-8b1534092eaa",
        "source_branch": "cursor/v31-014-sut-2eaa",
        "raw_commit": "6133944337b6454fba1cf11e3c1801da6c1532be",
        "attestation_commit": "6133944337b6454fba1cf11e3c1801da6c1532be",
        "raw_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-014.json",
        "attestation_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-attestations/V31-014.json",
        "delivery": "dedicated",
    },
    {
        "case_id": "V31-015",
        "context_id": "bc-e5e8f57e-0afb-52cc-92a1-6eeb0143fcf9",
        "source_branch": "cursor/v31-015-sut-fcf9",
        "raw_commit": "afeb1e61e15fb753aae42372ce232950abdb3b13",
        "attestation_commit": "afeb1e61e15fb753aae42372ce232950abdb3b13",
        "raw_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-015.json",
        "attestation_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-015.attestation.json",
        "delivery": "dedicated",
    },
    {
        "case_id": "V31-016",
        "context_id": "bc-d18b66e8-e111-5a78-ae71-f895f7e470ac",
        "source_branch": DELIVERY_BRANCH,
        "raw_commit": "99579d4760334b9752495bc1cbe93333c023938d",
        "attestation_commit": "a65e26961880130f237345c4ea74843b06399c22",
        "raw_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-016.json",
        "attestation_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-016.attestation.json",
        "delivery": "shared_holdout",
    },
    {
        "case_id": "V31-017",
        "context_id": "bc-dc3a2a74-64e8-50b6-a884-3f8d92c44b89",
        "source_branch": DELIVERY_BRANCH,
        "raw_commit": "b79e255b5ede61b957af35a36a8c1fe3b6e81b40",
        "attestation_commit": "b79e255b5ede61b957af35a36a8c1fe3b6e81b40",
        "raw_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-017.md",
        "attestation_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-attestations/V31-017.json",
        "delivery": "shared_holdout",
    },
    {
        "case_id": "V31-018",
        "context_id": "bc-703b80b4-bfdb-5ecb-a4b1-79656f279ccf",
        "source_branch": DELIVERY_BRANCH,
        "raw_commit": "04ef848aff0f8cc25893b1de7a846ae91cab8847",
        "attestation_commit": "04ef848aff0f8cc25893b1de7a846ae91cab8847",
        "raw_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-018.json",
        "attestation_source_path": "tests/benchmark/v3_1-holdout/cloud-cases/sut-raw/V31-018.attestation.json",
        "delivery": "shared_holdout",
    },
]


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_show(commit: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return result.stdout


def git_rev_parse(ref: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", ref], cwd=ROOT, text=True
    ).strip()


def git_is_ancestor(ancestor: str, descendant: str) -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=ROOT,
    )
    return result.returncode == 0


def wrap_markdown(case_id: str, text: str) -> bytes:
    document = {
        "schema_version": "v3.1",
        "artifact": "sut-raw-output",
        "case_id": case_id,
        "source_format": "markdown",
        "raw_skill_output": text,
    }
    return (json.dumps(document, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def main() -> None:
    head = git_rev_parse("HEAD")
    if git_is_ancestor(DELIVERY_TIP, "HEAD") and head != CANONICAL_PARENT:
        raise ValueError("refusing to extract on a history that merged the shared delivery tip")
    if not git_is_ancestor(CANONICAL_PARENT, "HEAD"):
        raise ValueError("canonical parent f609800 is not an ancestor of HEAD")
    if git_rev_parse(DELIVERY_BRANCH) != DELIVERY_TIP:
        raise ValueError("delivery-log ref moved")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    ATT_DIR.mkdir(parents=True, exist_ok=True)
    entries = []
    for source in SOURCES:
        case_id = source["case_id"]
        raw_bytes = git_show(source["raw_commit"], source["raw_source_path"])
        att_bytes = git_show(
            source["attestation_commit"], source["attestation_source_path"]
        )
        source_raw_sha = digest_bytes(raw_bytes)
        source_att_sha = digest_bytes(att_bytes)
        wrapped = False
        if source["raw_source_path"].endswith(".md"):
            text = raw_bytes.decode("utf-8")
            canonical_raw = wrap_markdown(case_id, text)
            wrapped = True
            parsed = json.loads(canonical_raw)
            if parsed["raw_skill_output"] != text:
                raise ValueError(f"{case_id}: markdown wrap mutated Skill text")
        else:
            canonical_raw = raw_bytes
            parsed = json.loads(canonical_raw)
            if isinstance(parsed, dict) and parsed.get("case_id") not in (None, case_id):
                raise ValueError(f"{case_id}: raw case_id mismatch")
            if (
                isinstance(parsed, dict)
                and "cases" in parsed
                and parsed["cases"][0]["case_id"] != case_id
            ):
                raise ValueError(f"{case_id}: nested case_id mismatch")
        attestation = json.loads(att_bytes)
        if attestation.get("case_id") != case_id:
            raise ValueError(f"{case_id}: attestation case_id mismatch")

        raw_path = RAW_DIR / f"{case_id}.json"
        att_path = ATT_DIR / f"{case_id}.json"
        raw_path.write_bytes(canonical_raw)
        att_path.write_bytes(att_bytes)
        entries.append(
            {
                "case_id": case_id,
                "context_id": source["context_id"],
                "source_branch": source["source_branch"],
                "delivery": source["delivery"],
                "raw_commit": source["raw_commit"],
                "attestation_commit": source["attestation_commit"],
                "raw_source_path": source["raw_source_path"],
                "attestation_source_path": source["attestation_source_path"],
                "source_raw_sha256": source_raw_sha,
                "source_attestation_sha256": source_att_sha,
                "canonical_raw_path": str(raw_path.relative_to(ROOT)),
                "canonical_attestation_path": str(att_path.relative_to(ROOT)),
                "canonical_raw_sha256": digest_bytes(canonical_raw),
                "canonical_attestation_sha256": digest_bytes(att_bytes),
                "markdown_wrapped": wrapped,
            }
        )

    index = {
        "schema_version": "v3.1",
        "artifact": "sut-source-index",
        "canonical_parent_commit": CANONICAL_PARENT,
        "canonical_parent_role": "prepare-sut-inputs; gold freeze parent",
        "holdout_branch": HOLDOUT_BRANCH,
        "shared_delivery": {
            "branch": DELIVERY_BRANCH,
            "tip": DELIVERY_TIP,
            "role": "delivery_log_only",
            "not_canonical_parent": True,
        },
        "cases": entries,
    }
    (CLOUD / "sut-source-index.json").write_text(
        json.dumps(index, indent=2) + "\n", encoding="utf-8"
    )

    log = subprocess.check_output(
        [
            "git",
            "log",
            "--format=%H %s",
            f"{CANONICAL_PARENT}..{DELIVERY_TIP}",
        ],
        cwd=ROOT,
        text=True,
    ).strip().splitlines()
    delivery = {
        "schema_version": "v3.1",
        "artifact": "sut-shared-delivery-log",
        "branch": DELIVERY_BRANCH,
        "tip": DELIVERY_TIP,
        "canonical_parent_commit": CANONICAL_PARENT,
        "not_canonical_parent": True,
        "commits": [
            {"sha256_commit": line.split(" ", 1)[0], "subject": line.split(" ", 1)[1]}
            for line in log
        ],
        "cases_delivered_on_shared_holdout": [
            "V31-003",
            "V31-011",
            "V31-016",
            "V31-017",
            "V31-018",
        ],
        "note": (
            "These seven commits raced onto cursor/blind-v31-holdout-17a0. "
            "Canonical SUT freeze extracts each case by git show from the listed "
            "source commits and does not merge this history."
        ),
    }
    (CLOUD / "sut-delivery-log.json").write_text(
        json.dumps(delivery, indent=2) + "\n", encoding="utf-8"
    )
    print(f"extracted {len(entries)} canonical SUT cases without merging shared delivery")


if __name__ == "__main__":
    main()
