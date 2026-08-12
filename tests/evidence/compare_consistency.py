import json
import sys
from collections import defaultdict
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    require(
        len(sys.argv) == 3,
        "usage: compare_consistency.py <plan.json> <evidence.json>",
    )
    plan = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    records = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))

    repeats = plan["required_repeats"]
    planned = {item["case_id"]: item for item in plan["cases"]}
    require(len(planned) == len(plan["cases"]), "duplicate case in plan")

    grouped: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        case_id = record["case_id"]
        require(case_id in planned, f"unplanned case: {case_id}")
        require(record["result"] == "PASS", f"{case_id}: non-PASS repeat")
        require(
            record["consistency"]["group"] == planned[case_id]["group"],
            f"{case_id}: group mismatch",
        )
        grouped[case_id].append(record)

    require(set(grouped) == set(planned), "evidence does not cover complete plan")

    print("| Case | Group | Repeats | Route | Responsibility | Tone | Overall | Questions | Revision facts |")
    print("|---|---|---:|---|---|---|---|---:|---|")
    for case_id, expected in planned.items():
        case_records = grouped[case_id]
        require(len(case_records) == repeats, f"{case_id}: expected {repeats} repeats")
        indices = sorted(item["consistency"]["repeat_index"] for item in case_records)
        require(indices == list(range(1, repeats + 1)), f"{case_id}: repeat indices")
        require(
            len({item["consistency"]["evaluator_context_id"] for item in case_records})
            == repeats,
            f"{case_id}: evaluator contexts are not independent",
        )
        for record in case_records:
            require(
                record["observations"] == expected["observations"],
                f"{case_id}: observation differs from planned boundary",
            )

        baseline = expected["observations"]
        facts = "; ".join(baseline["revision_facts"]) or "None"
        print(
            f"| {case_id} | {expected['group']} | {repeats} | {baseline['route']} | "
            f"{baseline['responsibility']} | {baseline['tone']} | {baseline['overall']} | "
            f"{baseline['question_count']} | {facts} |"
        )

    print(f"consistency result: {len(planned)} cases × {repeats} repeats; 0 material variations")


if __name__ == "__main__":
    main()
