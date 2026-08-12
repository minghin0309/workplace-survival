import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


EXPECTED_CATEGORIES = {
    "green_control": 6,
    "responsibility": 5,
    "tone": 5,
    "multi_round": 4,
    "provenance_prompt": 3,
    "recipient_routing": 3,
    "image_ocr": 4,
}
ROUTES = {"Normal mode", "Limited-background mode", "Message-template mode", "Intake", "Scope"}
RATINGS = {"Green", "Yellow", "Red", "Gray", None}
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
RUNTIME_PATHS = [
    ".cursor/skills/workplace-survival/SKILL.md",
    ".cursor/skills/workplace-survival/REFERENCE.md",
    ".cursor/skills/workplace-survival/FORMATS.md",
    ".cursor/skills/workplace-survival/EXAMPLES.md",
]
FROZEN_RUNTIME_COMMIT = "f8c4d18c352c017715acfdb8c87f45393b474410"
CASE_KEYS = {"case_id", "category", "recipient_description", "turns", "image_spec", "case_designer_notes"}
TURN_KEYS = {"turn_index", "input_raw", "image_path"}
LABEL_FIELDS = {
    "route",
    "responsibility",
    "tone",
    "overall",
    "required_question_topics",
    "allowed_question_topics",
    "required_revision_facts",
    "allowed_revision_facts",
    "critical_invariants",
    "rationale",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def validate_sorted_strings(value, label: str, *, nonempty: bool = False) -> None:
    require(isinstance(value, list), f"{label}: list required")
    require(all(isinstance(item, str) and item for item in value), f"{label}: invalid item")
    require(value == sorted(set(value)), f"{label}: must be sorted and unique")
    if nonempty:
        require(value, f"{label}: must not be empty")


def safe_image_path(directory: Path, value: str, case_id: str) -> Path:
    require(not Path(value).is_absolute(), f"{case_id}: absolute image path")
    expected = f"images/{case_id}.png"
    require(value == expected, f"{case_id}: image path must be {expected}")
    resolved = (directory / value).resolve()
    require(resolved.is_relative_to(directory), f"{case_id}: image path escapes holdout")
    require(resolved.is_file(), f"{case_id}: missing image")
    with Image.open(resolved) as image:
        require(image.format == "PNG", f"{case_id}: image is not PNG")
        image.verify()
    return resolved


def validate_cases(cases: list[dict], directory: Path) -> list[Path]:
    expected_ids = [f"BH-{index:03d}" for index in range(1, 31)]
    require([item.get("case_id") for item in cases] == expected_ids, "case IDs/order")
    require(Counter(item.get("category") for item in cases) == EXPECTED_CATEGORIES, "category distribution")
    images = []
    for case in cases:
        case_id = case["case_id"]
        require(set(case) == CASE_KEYS, f"{case_id}: exact case schema")
        require(
            isinstance(case["recipient_description"], str) and case["recipient_description"],
            f"{case_id}: recipient",
        )
        require(
            isinstance(case["case_designer_notes"], str) and case["case_designer_notes"],
            f"{case_id}: designer notes",
        )
        turns = case["turns"]
        require(isinstance(turns, list) and turns, f"{case_id}: turns")
        require(
            [turn.get("turn_index") for turn in turns] == list(range(1, len(turns) + 1)),
            f"{case_id}: turn order",
        )
        for turn in turns:
            require(set(turn) == TURN_KEYS, f"{case_id}: exact turn schema")
            require(isinstance(turn["input_raw"], str) and turn["input_raw"], f"{case_id}: input")
            require(turn["image_path"] is None or isinstance(turn["image_path"], str), f"{case_id}: image")
        if case["category"] == "multi_round":
            require(len(turns) >= 2, f"{case_id}: multi-round turns")
        if case["category"] == "image_ocr":
            spec = case["image_spec"]
            require(
                isinstance(spec, dict)
                and set(spec)
                == {
                    "output_path",
                    "medium",
                    "canvas",
                    "scene_description",
                    "rendered_text",
                    "visual_conditions",
                    "legibility_notes",
                },
                f"{case_id}: image spec",
            )
            require(
                all(isinstance(value, str) and value for value in spec.values()),
                f"{case_id}: image spec value",
            )
            image = safe_image_path(directory, spec["output_path"], case_id)
            require(any(turn["image_path"] == spec["output_path"] for turn in turns), f"{case_id}: image turn")
            images.append(image)
        else:
            require(case["image_spec"] is None, f"{case_id}: unexpected image spec")
            require(all(turn["image_path"] is None for turn in turns), f"{case_id}: unexpected image turn")
    require(
        {path.name for path in directory.glob("images/*.png")}
        == {path.name for path in images},
        "image directory contains missing or extra fixtures",
    )
    return images


def validate_gold(gold: list[dict], cases: list[dict], label: str) -> None:
    require([item.get("case_id") for item in gold] == [item["case_id"] for item in cases], f"{label}: IDs")
    required_questions = required_facts = rated_turns = 0
    for case, item in zip(cases, gold):
        require(set(item) == {"case_id", "turn_labels"}, f"{case['case_id']}: {label} schema")
        turns = item["turn_labels"]
        require(isinstance(turns, list) and len(turns) == len(case["turns"]), f"{case['case_id']}: {label} turns")
        for expected_index, turn in enumerate(turns, start=1):
            require(
                set(turn) == LABEL_FIELDS | {"turn_index"},
                f"{case['case_id']}: {label} turn schema",
            )
            require(turn["turn_index"] == expected_index, f"{case['case_id']}: {label} turn index")
            route = turn["route"]
            require(route in ROUTES, f"{case['case_id']}: route")
            ratings = [turn[field] for field in ("responsibility", "tone", "overall")]
            require(all(value in RATINGS for value in ratings), f"{case['case_id']}: rating")
            if route in {"Intake", "Scope", "Message-template mode"}:
                require(ratings == [None, None, None], f"{case['case_id']}: non-review ratings")
            else:
                require(None not in ratings, f"{case['case_id']}: rated route")
                rated_turns += 1
                priority = {"Green": 0, "Yellow": 1, "Gray": 2, "Red": 3}
                require(
                    turn["overall"] == max((turn["responsibility"], turn["tone"]), key=priority.get),
                    f"{case['case_id']}: overall derivation",
                )
            for field in LABEL_FIELDS - {"route", "responsibility", "tone", "overall", "rationale"}:
                validate_sorted_strings(
                    turn[field],
                    f"{case['case_id']}: {label} {field}",
                    nonempty=field == "critical_invariants",
                )
            require(set(turn["critical_invariants"]) <= INVARIANTS, f"{case['case_id']}: invariant token")
            require(
                set(turn["required_question_topics"]) <= set(turn["allowed_question_topics"]),
                f"{case['case_id']}: required question not allowed",
            )
            if label == "final gold":
                require(
                    len(turn["required_question_topics"]) <= 3,
                    f"{case['case_id']}: more than three question topics",
                )
            require(
                set(turn["required_revision_facts"]) <= set(turn["allowed_revision_facts"]),
                f"{case['case_id']}: required fact not allowed",
            )
            require(isinstance(turn["rationale"], str) and turn["rationale"], f"{case['case_id']}: rationale")
            required_questions += len(turn["required_question_topics"])
            required_facts += len(turn["required_revision_facts"])
    if label == "final gold":
        require(required_questions >= 8, "insufficient required-question denominator")
        require(required_facts >= 12, "insufficient required-fact denominator")
        require(rated_turns >= 20, "insufficient rated-turn denominator")


def validate_model_metadata(value: object, label: str) -> str:
    require(isinstance(value, dict), f"{label}: model metadata")
    require(
        set(value) == {"context_id", "model_id", "model_family", "display_name"},
        f"{label}: model schema",
    )
    require(all(isinstance(item, str) and item for item in value.values()), f"{label}: model value")
    return value["model_family"]


def disagreement_map(label_docs: list[list[dict]]) -> dict[str, list[object]]:
    values = {}
    for case_index, labels in enumerate(zip(*label_docs)):
        case_id = labels[0]["case_id"]
        for turn_index, turns in enumerate(
            zip(*(item["turn_labels"] for item in labels)),
            start=1,
        ):
            for field in LABEL_FIELDS:
                candidates = [turn[field] for turn in turns]
                if not all(candidate == candidates[0] for candidate in candidates[1:]):
                    values[f"{case_id}:{turn_index}:{field}"] = candidates
    return values


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: freeze_holdout.py <holdout-dir> <manifest.json> <runtime-commit>")
    root = Path(__file__).resolve().parents[2]
    directory = Path(sys.argv[1]).resolve()
    manifest_path = Path(sys.argv[2]).resolve()
    runtime_commit = sys.argv[3]
    require(not manifest_path.exists(), "refusing to overwrite frozen holdout manifest")
    require(runtime_commit == FROZEN_RUNTIME_COMMIT, "runtime commit differs from preregistered baseline")

    files = {
        "cases": directory / "cases.json",
        "gold_labeler_1": directory / "gold-labeler-1.json",
        "gold_labeler_2": directory / "gold-labeler-2.json",
        "gold_labeler_3": directory / "gold-labeler-3.json",
        "gold_labeler_1_raw": directory / "gold-labeler-1-raw.json",
        "gold_labeler_2_raw": directory / "gold-labeler-2-raw.json",
        "gold_labeler_3_raw": directory / "gold-labeler-3-raw.json",
        "adjudication": directory / "adjudication.json",
        "gold": directory / "gold.json",
        "gold_raw": directory / "gold-raw.json",
    }
    require(all(path.is_file() for path in files.values()), "required holdout file missing")
    cases = json.loads(files["cases"].read_text(encoding="utf-8"))
    images = validate_cases(cases, directory)

    label_docs = []
    families = []
    for index in range(1, 4):
        document = json.loads(files[f"gold_labeler_{index}"].read_text(encoding="utf-8"))
        require(set(document) == {"labeler", "labels"}, f"labeler {index}: document schema")
        families.append(validate_model_metadata(document["labeler"], f"labeler {index}"))
        validate_gold(document["labels"], cases, f"labeler {index}")
        label_docs.append(document["labels"])
    require(len(set(families)) == 3, "gold labelers must use three model families")

    gold = json.loads(files["gold"].read_text(encoding="utf-8"))
    validate_gold(gold, cases, "final gold")
    adjudication = json.loads(files["adjudication"].read_text(encoding="utf-8"))
    require(
        set(adjudication) == {
            "adjudicator",
            "case_ids",
            "all_disagreements_reviewed",
            "disagreements",
        },
        "adjudication schema",
    )
    adjudicator_family = validate_model_metadata(adjudication["adjudicator"], "adjudicator")
    require(adjudicator_family not in set(families), "adjudicator model family must be distinct")
    require(adjudication["case_ids"] == [item["case_id"] for item in cases], "adjudication coverage")
    require(adjudication["all_disagreements_reviewed"] is True, "adjudication incomplete")

    disagreements = disagreement_map(label_docs)
    entries = adjudication["disagreements"]
    require(isinstance(entries, list), "adjudication disagreements")
    by_key = {item["key"]: item for item in entries}
    require(len(by_key) == len(entries), "duplicate adjudication key")
    require(set(by_key) == set(disagreements), "adjudication does not match all disagreements")

    final_by_id = {item["case_id"]: item for item in gold}
    for key, candidate_values in disagreements.items():
        entry = by_key[key]
        require(
            set(entry) == {"key", "candidate_values", "resolution", "rationale"},
            f"{key}: adjudication entry schema",
        )
        require(entry["candidate_values"] == candidate_values, f"{key}: candidate values")
        case_id, turn_text, field = key.split(":", 2)
        final_value = final_by_id[case_id]["turn_labels"][int(turn_text) - 1][field]
        require(entry["resolution"] == final_value, f"{key}: resolution/final mismatch")
        require(isinstance(entry["rationale"], str) and entry["rationale"], f"{key}: rationale")

    for case_index, labels in enumerate(zip(*label_docs)):
        case_id = labels[0]["case_id"]
        for turn_index, turns in enumerate(zip(*(item["turn_labels"] for item in labels)), start=1):
            for field in LABEL_FIELDS:
                key = f"{case_id}:{turn_index}:{field}"
                if key not in disagreements:
                    require(
                        final_by_id[case_id]["turn_labels"][turn_index - 1][field] == turns[0][field],
                        f"{key}: unanimous value changed in final gold",
                    )

    protected = {key: {"path": str(path), "sha256": digest(path)} for key, path in files.items()}
    for policy_path in (
        root / "tests/blind/BLIND_CASE_BRIEF.md",
        root / "tests/blind/GOLD_RUBRIC.md",
        root / "tests/blind/blind_common.py",
        root / "tests/blind/freeze_outputs.py",
        root / "tests/blind/normalize_outputs.py",
        root / "tests/blind/score_blind.py",
        root / "tests/blind/BLIND_PLAN.md",
    ):
        protected[policy_path.name] = {"path": str(policy_path), "sha256": digest(policy_path)}
    for image_path in images:
        protected[f"image:{image_path.name}"] = {"path": str(image_path), "sha256": digest(image_path)}

    runtime = []
    for runtime_path in RUNTIME_PATHS:
        blob = subprocess.check_output(["git", "show", f"{runtime_commit}:{runtime_path}"], cwd=root)
        runtime.append({"path": runtime_path, "sha256": digest_bytes(blob)})

    manifest = {
        "frozen_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "runtime_commit": runtime_commit,
        "runtime_sources": runtime,
        "protected_files": protected,
        "case_count": 30,
        "case_ids": [item["case_id"] for item in cases],
        "labeler_model_families": families,
        "adjudicator_model_family": adjudicator_family,
        "disagreement_count": len(disagreements),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"froze 30 cases and gold: manifest={digest(manifest_path)}")


if __name__ == "__main__":
    main()
