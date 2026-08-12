import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "tests/mutation/evidence"
EXPECTED = {f"M{index:02d}" for index in range(1, 10)}
RUNTIME_PATH = ".cursor/skills/workplace-survival"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    actual = {path.name for path in EVIDENCE.iterdir() if path.is_dir()}
    require(actual == EXPECTED, f"mutant evidence mismatch: {actual}")

    killed = 0
    survived = 0
    equivalent = 0
    for mutant_id in sorted(EXPECTED):
        directory = EVIDENCE / mutant_id
        metadata = json.loads((directory / "metadata.json").read_text(encoding="utf-8"))
        oracle = json.loads((directory / "oracle.json").read_text(encoding="utf-8"))
        isolation = json.loads((directory / "isolation.json").read_text(encoding="utf-8"))
        require(metadata["mutant_id"] == mutant_id, f"{mutant_id}: metadata ID")
        require(metadata["classification"] in {"KILLED", "SURVIVED", "EQUIVALENT"}, f"{mutant_id}: class")
        require(str(oracle["classification"]).upper() == metadata["classification"], f"{mutant_id}: oracle")
        require(oracle["mutant_id"] == mutant_id, f"{mutant_id}: normalized oracle ID")
        require((directory / "mutant.diff").stat().st_size > 0, f"{mutant_id}: empty diff")
        output_name = "sut-output.txt" if mutant_id == "M09" else "sut-output.json"
        require((directory / output_name).stat().st_size > 0, f"{mutant_id}: missing output")
        require((directory / "oracle-raw.json").stat().st_size > 0, f"{mutant_id}: raw oracle")

        if metadata["classification"] == "KILLED":
            failures = oracle.get("failed_assertions")
            require(isinstance(failures, list) and failures, f"{mutant_id}: no killing assertion")
            for failure in failures:
                require(
                    all(
                        isinstance(failure.get(field), str) and failure[field]
                        for field in ("case_id", "assertion", "evidence")
                    ),
                    f"{mutant_id}: incomplete killing assertion",
                )

        if mutant_id != "M09":
            require(isolation["sut_context_id"] == metadata["sut_context_id"], f"{mutant_id}: SUT context")
            require(
                isolation["oracle_context_id"] == metadata["oracle_context_id"],
                f"{mutant_id}: oracle context",
            )
            require(
                isolation["sut_context_id"] != isolation["oracle_context_id"],
                f"{mutant_id}: SUT and oracle context reused",
            )
            require(
                "Expected assertions" in isolation["sut_forbidden_inputs"]
                and "Forbidden assertions" in isolation["sut_forbidden_inputs"],
                f"{mutant_id}: SUT oracle access not forbidden",
            )
            require(
                "mutated runtime files" in isolation["oracle_forbidden_inputs"],
                f"{mutant_id}: oracle mutation access not forbidden",
            )
            require(
                isolation["filesystem_access_audit_available"] is False
                and isolation["limitation"],
                f"{mutant_id}: isolation limitation missing",
            )

        if metadata["classification"] == "KILLED":
            killed += 1
        elif metadata["classification"] == "SURVIVED":
            survived += 1
        else:
            equivalent += 1

    require(killed + survived + equivalent == len(EXPECTED), "classification count")
    require(survived == 0, "surviving mutants require regression tests")
    require(killed == 9, "expected all nine selected mutants to be killed")

    m09_validator = EVIDENCE / "M09/mutated-validator.py"
    m09_gate = subprocess.run(
        [
            "python3",
            str(ROOT / "tests/mutation/check_validator_pass_gate.py"),
            str(m09_validator),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    require(m09_gate.returncode != 0, "M09 deterministic mutant was not killed")
    require(
        "accepted PASS evidence containing a failed assertion" in m09_gate.stdout + m09_gate.stderr,
        "M09 killing output mismatch",
    )

    runtime_diff = subprocess.check_output(
        ["git", "diff", "8ca59a8..HEAD", "--", RUNTIME_PATH],
        cwd=ROOT,
    )
    require(not runtime_diff, "baseline runtime changed during mutation testing")

    score = killed / (killed + survived)
    print(
        f"mutation result: killed={killed}; survived={survived}; "
        f"equivalent={equivalent}; score={score:.0%}; baseline runtime unchanged"
    )


if __name__ == "__main__":
    main()
