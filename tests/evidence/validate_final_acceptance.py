import importlib.util
import json
import subprocess
import sys
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_validator(root: Path):
    path = root / "tests/evidence/validate_evidence.py"
    spec = importlib.util.spec_from_file_location("evidence_validator", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expand_cases(config: dict) -> list[str]:
    if "case_ids" in config:
        return config["case_ids"]
    return [
        f"{config['case_prefix']}{index:02d}"
        for index in range(config["first"], config["last"] + 1)
    ]


def main() -> None:
    require(
        len(sys.argv) == 3,
        "usage: validate_final_acceptance.py <plan.json> <evidence.json>",
    )
    root = Path(__file__).resolve().parents[2]
    plan_path = Path(sys.argv[1]).resolve()
    evidence_path = Path(sys.argv[2]).resolve()
    require(plan_path.is_relative_to(root), "plan must be inside repository")
    require(evidence_path.is_relative_to(root), "evidence must be inside repository")

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    records = json.loads(evidence_path.read_text(encoding="utf-8"))
    validator = load_validator(root)
    evidence_reference = evidence_path.relative_to(root).as_posix()
    seen: set[str] = set()
    for record in records:
        validator.validate_record(record, root, evidence_reference, seen)

    by_case = {record["case_id"]: record for record in records}
    require(len(by_case) == len(records), "duplicate case evidence")
    runtime_paths = {
        ".cursor/skills/workplace-survival/SKILL.md",
        ".cursor/skills/workplace-survival/REFERENCE.md",
        ".cursor/skills/workplace-survival/FORMATS.md",
        ".cursor/skills/workplace-survival/EXAMPLES.md",
    }
    require(
        len({record["runtime_commit"] for record in records}) == 1,
        "final acceptance records do not share one runtime commit",
    )
    for record in records:
        require(
            {item["path"] for item in record["runtime_sources"]} == runtime_paths,
            f"{record['case_id']}: incomplete runtime sources",
        )
        for runtime_path in runtime_paths:
            committed = subprocess.check_output(
                ["git", "show", f"{record['runtime_commit']}:{runtime_path}"],
                cwd=root,
            )
            require(
                committed == (root / runtime_path).read_bytes(),
                f"{record['case_id']}: runtime commit differs from packaged runtime",
            )

    expected: dict[str, str] = {}
    for suite, config in plan["suites"].items():
        for case_id in expand_cases(config):
            require(case_id not in expected, f"duplicate planned case: {case_id}")
            expected[case_id] = suite

    automated = set(plan["automated_checks"])
    expected_all = set(expected) | automated
    require(set(by_case) == expected_all, "final evidence does not exactly match plan")

    image_cases = plan["image_cases"]
    for case_id, suite in expected.items():
        record = by_case[case_id]
        require(record["suite"] == suite, f"{case_id}: suite mismatch")
        require(record["result"] == "PASS", f"{case_id}: not PASS")
        if case_id in image_cases:
            require(record["method"] == "image_attached", f"{case_id}: image method")
            require(
                {item["path"] for item in record["artifacts"]} == {image_cases[case_id]},
                f"{case_id}: wrong image artifact",
            )
            require(
                all(item["opened_with_image_reader"] for item in record["artifacts"]),
                f"{case_id}: image not opened",
            )
        elif suite in {"auto_trigger", "explicit_invocation"}:
            require(record["method"] == "routing_semantic", f"{case_id}: routing method")
            skill = subprocess.check_output(
                [
                    "git",
                    "show",
                    f"{record['runtime_commit']}:.cursor/skills/workplace-survival/SKILL.md",
                ],
                cwd=root,
                text=True,
            )
            frontmatter = skill.split("---", 2)[1]
            require("name: workplace-survival" in frontmatter, f"{case_id}: wrong skill slug")
            require(
                "disable-model-invocation" not in frontmatter,
                f"{case_id}: final configuration not enabled",
            )
        else:
            require(record["method"] == "manual_semantic", f"{case_id}: semantic method")

    for case_id in automated:
        record = by_case[case_id]
        require(record["result"] == "PASS", f"{case_id}: automated check failed")
        require(record["method"] == "automated", f"{case_id}: automated method")

    case_passes = len(expected)
    require(case_passes == plan["expected_case_passes"], "case-pass count mismatch")
    require(len(automated) == plan["expected_automated_passes"], "automated-pass count mismatch")

    repeat = plan["repeat_evidence"]
    repeat_plan_path = root / repeat["plan"]
    repeat_records_path = root / repeat["records"]
    repeat_plan = json.loads(repeat_plan_path.read_text(encoding="utf-8"))
    repeat_records = json.loads(repeat_records_path.read_text(encoding="utf-8"))
    repeat_reference = repeat_records_path.relative_to(root).as_posix()
    repeat_seen: set[str] = set()
    for record in repeat_records:
        validator.validate_record(record, root, repeat_reference, repeat_seen)
    validator.validate_repeat_plan(repeat_records, repeat_plan_path)
    require(len(repeat_plan["cases"]) == repeat["expected_cases"], "repeat case count")
    require(repeat_plan["required_repeats"] == repeat["expected_repeats"], "repeat count")
    require(
        len(repeat_records) == repeat["expected_cases"] * repeat["expected_repeats"],
        "repeat evidence count",
    )

    print(f"case acceptance: {case_passes}/{case_passes} passed")
    print(f"automated package checks: {len(automated)}/{len(automated)} passed")
    print(
        "repeat consistency: "
        f"{repeat['expected_cases']} cases × {repeat['expected_repeats']} runs; "
        f"{repeat['expected_material_variations']} material variations"
    )
    print(f"attached-image cases: {len(image_cases)}/{len(image_cases)} passed")


if __name__ == "__main__":
    main()
