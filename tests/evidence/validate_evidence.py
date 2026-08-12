import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


METHODS = {
    "automated",
    "manual_semantic",
    "image_attached",
    "routing_semantic",
    "environment_limited",
}
ASSESSMENTS = {"automatic", "manual"}
RESULTS = {"PASS", "FAIL", "NOT_RUN"}
EXPECTED_SUITES = {
    "functional",
    "anti_hallucination",
    "interaction_quality",
    "auto_trigger",
    "explicit_invocation",
}
SUITE_RESULT_FILES = {
    "functional": "tests/TEST_RESULTS.md",
    "anti_hallucination": "tests/ANTI_HALLUCINATION_RESULTS.md",
    "interaction_quality": "tests/INTERACTION_QUALITY_RESULTS.md",
    "auto_trigger": "tests/AUTO_TRIGGER_RESULTS.md",
    "explicit_invocation": "tests/EXPLICIT_INVOCATION_RESULTS.md",
}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def resolve_repo_path(root: Path, value: str, label: str) -> Path:
    candidate = Path(value)
    require(not candidate.is_absolute(), f"{label}: absolute path is not allowed")
    resolved = (root / candidate).resolve()
    require(resolved.is_relative_to(root), f"{label}: path escapes repository")
    return resolved


def validate_timestamp(value: object, run_id: str) -> None:
    require(isinstance(value, str) and value.endswith("Z"), f"{run_id}: UTC timestamp required")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError(f"{run_id}: invalid ISO-8601 timestamp") from exc
    require(parsed.tzinfo == timezone.utc, f"{run_id}: timestamp must be UTC")


def validate_model(model: object, run_id: str) -> None:
    require(isinstance(model, dict), f"{run_id}: model object required")
    require(isinstance(model.get("id"), str) and model["id"], f"{run_id}: model id")
    require(
        isinstance(model.get("display_name"), str) and model["display_name"],
        f"{run_id}: model display_name",
    )
    exact = model.get("exact_backend_slug_available")
    require(isinstance(exact, bool), f"{run_id}: exact_backend_slug_available")
    reason = model.get("unavailable_reason")
    if exact:
        require(model["id"] not in {"inherit", "default", "unknown"}, f"{run_id}: exact model slug required")
        require(reason in (None, ""), f"{run_id}: exact model cannot have unavailable_reason")
    else:
        require(isinstance(reason, str) and reason, f"{run_id}: unavailable model reason required")


def validate_source(source: object, root: Path, run_id: str) -> None:
    require(isinstance(source, dict), f"{run_id}: input_source object required")
    reference = source.get("reference")
    require(isinstance(reference, str) and reference, f"{run_id}: input source reference")
    source_path = resolve_repo_path(root, reference.split("#", 1)[0], f"{run_id}: source")
    require(source_path.is_file(), f"{run_id}: missing input source {source_path}")
    require(
        source.get("file_sha256") == sha256_bytes(source_path.read_bytes()),
        f"{run_id}: source hash mismatch",
    )


def validate_turns(turns: object, run_id: str) -> None:
    require(isinstance(turns, list) and turns, f"{run_id}: turns required")
    for expected_index, turn in enumerate(turns, start=1):
        require(isinstance(turn, dict), f"{run_id}: invalid turn")
        require(turn.get("index") == expected_index, f"{run_id}: turn order mismatch")
        input_raw = turn.get("input_raw")
        raw_output = turn.get("raw_output")
        require(isinstance(input_raw, str) and input_raw, f"{run_id}: turn input required")
        require(isinstance(raw_output, str) and raw_output, f"{run_id}: turn output required")
        require(turn.get("input_sha256") == sha256_text(input_raw), f"{run_id}: input hash mismatch")
        require(
            turn.get("output_sha256") == sha256_text(raw_output),
            f"{run_id}: output hash mismatch",
        )


def validate_artifacts(artifacts: object, root: Path, method: str, run_id: str) -> None:
    require(isinstance(artifacts, list), f"{run_id}: artifacts must be a list")
    for artifact in artifacts:
        require(isinstance(artifact, dict), f"{run_id}: invalid artifact")
        path = artifact.get("path")
        require(isinstance(path, str) and path, f"{run_id}: artifact path")
        artifact_path = resolve_repo_path(root, path, f"{run_id}: artifact")
        require(artifact_path.is_file(), f"{run_id}: missing artifact {path}")
        require(
            artifact.get("sha256") == sha256_bytes(artifact_path.read_bytes()),
            f"{run_id}: artifact hash mismatch {path}",
        )
        require(isinstance(artifact.get("usage"), str) and artifact["usage"], f"{run_id}: usage")
        require(
            isinstance(artifact.get("opened_with_image_reader"), bool),
            f"{run_id}: image-open flag",
        )

    if method == "image_attached":
        require(artifacts, f"{run_id}: image_attached requires an artifact")
        require(
            all(item["opened_with_image_reader"] for item in artifacts),
            f"{run_id}: image artifact was not opened",
        )
        require(
            all(Path(item["path"]).suffix.lower() in IMAGE_SUFFIXES for item in artifacts),
            f"{run_id}: image_attached requires image artifacts",
        )


def validate_assertions(assertions: object, result: str, run_id: str) -> None:
    require(isinstance(assertions, list) and assertions, f"{run_id}: assertions required")
    seen: set[str] = set()
    for assertion in assertions:
        require(isinstance(assertion, dict), f"{run_id}: invalid assertion")
        assertion_id = assertion.get("id")
        require(isinstance(assertion_id, str) and assertion_id, f"{run_id}: assertion id")
        require(assertion_id not in seen, f"{run_id}: duplicate assertion id {assertion_id}")
        seen.add(assertion_id)
        require(isinstance(assertion.get("text"), str) and assertion["text"], f"{run_id}: assertion text")
        require(assertion.get("assessment") in ASSESSMENTS, f"{run_id}: assertion assessment")
        passed = assertion.get("passed")
        if result == "NOT_RUN":
            require(passed is None, f"{run_id}: NOT_RUN assertion must be null")
        else:
            require(isinstance(passed, bool), f"{run_id}: executed assertion must be boolean")

    if result == "PASS":
        require(all(item["passed"] for item in assertions), f"{run_id}: PASS has failed assertion")
    elif result == "FAIL":
        require(any(not item["passed"] for item in assertions), f"{run_id}: FAIL lacks failed assertion")


def validate_citations(
    citations: object,
    root: Path,
    evidence_reference: str,
    suite: str,
    run_id: str,
) -> None:
    require(isinstance(citations, list) and citations, f"{run_id}: result citations required")
    require(
        SUITE_RESULT_FILES[suite] in citations,
        f"{run_id}: missing suite result citation {SUITE_RESULT_FILES[suite]}",
    )
    for citation in citations:
        require(isinstance(citation, str) and citation, f"{run_id}: invalid result citation")
        result_path = resolve_repo_path(root, citation, f"{run_id}: citation")
        require(result_path.is_file(), f"{run_id}: missing result file {citation}")
        content = result_path.read_text(encoding="utf-8")
        require(f"`{run_id}`" in content, f"{run_id}: result file does not cite exact run_id")
        require(
            f"`{evidence_reference}`" in content,
            f"{run_id}: result file does not cite exact evidence file",
        )


def validate_record(
    record: dict,
    root: Path,
    evidence_reference: str,
    seen: set[str],
) -> None:
    run_id = record.get("run_id")
    require(isinstance(run_id, str) and run_id, "run_id is required")
    require(run_id not in seen, f"duplicate run_id: {run_id}")
    seen.add(run_id)

    require(record.get("schema_version") == "1", f"{run_id}: unsupported schema")
    require(record.get("suite") in EXPECTED_SUITES, f"{run_id}: unknown suite")
    require(isinstance(record.get("case_id"), str) and record["case_id"], f"{run_id}: case_id")
    validate_timestamp(record.get("executed_at_utc"), run_id)
    validate_model(record.get("model"), run_id)

    method = record.get("method")
    result = record.get("result")
    require(method in METHODS, f"{run_id}: invalid method")
    require(result in RESULTS, f"{run_id}: invalid result")
    if method == "environment_limited":
        require(result == "NOT_RUN", f"{run_id}: environment_limited must be NOT_RUN")
    else:
        require(result in {"PASS", "FAIL"}, f"{run_id}: executed method cannot be NOT_RUN")

    validate_source(record.get("input_source"), root, run_id)
    validate_turns(record.get("turns"), run_id)
    validate_artifacts(record.get("artifacts"), root, method, run_id)
    validate_assertions(record.get("assertions"), result, run_id)

    limitations = record.get("limitations")
    require(isinstance(limitations, list), f"{run_id}: limitations must be a list")
    if result == "NOT_RUN":
        require(limitations, f"{run_id}: NOT_RUN requires a limitation")

    validate_citations(
        record.get("result_citations"),
        root,
        evidence_reference,
        record["suite"],
        run_id,
    )


def main() -> None:
    require(len(sys.argv) == 2, "usage: validate_evidence.py <evidence.json>")
    evidence_path = Path(sys.argv[1]).resolve()
    root = Path(__file__).resolve().parents[2]
    require(evidence_path.is_relative_to(root), "evidence file must be inside repository")
    evidence_reference = evidence_path.relative_to(root).as_posix()
    records = json.loads(evidence_path.read_text(encoding="utf-8"))
    require(isinstance(records, list) and records, "evidence file must contain records")

    seen: set[str] = set()
    for record in records:
        require(isinstance(record, dict), "each evidence record must be an object")
        validate_record(record, root, evidence_reference, seen)

    suites = {record["suite"] for record in records}
    methods = {record["method"] for record in records}
    require(suites == EXPECTED_SUITES, f"suite coverage mismatch: {sorted(suites)}")
    require(methods == METHODS, f"method coverage mismatch: {sorted(methods)}")
    print(f"validated {len(records)} evidence records across {len(suites)} suites")


if __name__ == "__main__":
    main()
