import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


STAGE_ROLES = {
    "gold": {
        "cases",
        "oracle-notes",
        "gold",
        "adjudication",
        "ontology",
        "scorer",
        "validator",
        "runtime-manifest",
        "labeler-1",
        "labeler-2",
        "labeler-3",
        "labeler-1-attestation",
        "labeler-2-attestation",
        "labeler-3-attestation",
        "designer-attestation",
        "adjudicator-attestation",
    },
    "outputs": {"outputs", "generator-attestation"},
    "evaluations": {
        "evaluations",
        "matches",
        "evaluator-attestation",
        "matcher-attestation",
    },
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if len(sys.argv) < 5:
        raise SystemExit(
            "usage: freeze_cloud_artifacts.py <manifest.json> <stage> "
            "<GENESIS|parent-manifest.json> "
            "<role>::<path>::<cloud-branch>::<40-char-commit> [...]"
        )
    manifest_path = Path(sys.argv[1])
    stage = sys.argv[2]
    parent_value = sys.argv[3]
    if manifest_path.exists():
        raise FileExistsError("refusing to overwrite cloud artifact manifest")
    if stage not in STAGE_ROLES:
        raise ValueError(f"unknown stage: {stage}")

    if parent_value == "GENESIS":
        if stage != "gold":
            raise ValueError("only gold stage may use GENESIS")
        parent = {"path": None, "sha256": "0" * 64}
    else:
        parent_path = Path(parent_value)
        if not parent_path.is_file():
            raise FileNotFoundError(parent_path)
        parent = {"path": str(parent_path), "sha256": digest(parent_path)}

    artifacts = []
    roles = set()
    for value in sys.argv[4:]:
        role, path_text, branch, commit = value.split("::", 3)
        path = Path(path_text)
        if role in roles:
            raise ValueError(f"duplicate role: {role}")
        roles.add(role)
        if not path.is_file():
            raise FileNotFoundError(path)
        if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
            raise ValueError(f"invalid commit: {commit}")
        artifacts.append(
            {
                "role": role,
                "path": str(path),
                "sha256": digest(path),
                "cloud_branch": branch,
                "cloud_commit": commit,
            }
        )
    if not STAGE_ROLES[stage] <= roles:
        raise ValueError(f"missing required roles: {sorted(STAGE_ROLES[stage] - roles)}")
    if stage == "gold":
        cases_entry = next(item for item in artifacts if item["role"] == "cases")
        cases = json.loads(Path(cases_entry["path"]).read_text(encoding="utf-8"))
        expected_images = {
            f"image:{case['case_id']}:{turn['turn_index']}": turn["image_path"]
            for case in cases
            for turn in case["turns"]
            if turn.get("image_path") is not None
        }
        actual_images = {
            item["role"]: item["path"]
            for item in artifacts
            if item["role"].startswith("image:")
        }
        if actual_images != expected_images:
            raise ValueError("gold image artifact coverage mismatch")

    document = {
        "version": "2",
        "immutable": True,
        "stage": stage,
        "parent_manifest": parent,
        "frozen_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "artifacts": artifacts,
    }
    manifest_path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"froze {len(artifacts)} cloud artifacts at {stage} stage")


if __name__ == "__main__":
    main()
