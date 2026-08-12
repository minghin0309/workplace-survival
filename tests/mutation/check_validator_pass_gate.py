import copy
import importlib.util
import json
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_validator_pass_gate.py <validate_evidence.py>")

    root = Path(__file__).resolve().parents[2]
    validator_path = Path(sys.argv[1]).resolve()
    spec = importlib.util.spec_from_file_location("mutant_validator", validator_path)
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)

    evidence_path = root / "tests/evidence/t13-10-validation.json"
    record = copy.deepcopy(json.loads(evidence_path.read_text(encoding="utf-8"))[1])
    record["assertions"][0]["passed"] = False

    try:
        validator.validate_record(
            record,
            root,
            "tests/evidence/t13-10-validation.json",
            set(),
        )
    except ValueError:
        print("PASS: validator rejected PASS evidence containing a failed assertion")
        return

    raise SystemExit("FAIL: validator accepted PASS evidence containing a failed assertion")


if __name__ == "__main__":
    main()
