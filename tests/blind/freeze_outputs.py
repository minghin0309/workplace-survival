import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: freeze_outputs.py <freeze-manifest.json> <outputs.json> <outputs-manifest.json>")
    freeze_path = Path(sys.argv[1])
    outputs_path = Path(sys.argv[2])
    manifest_path = Path(sys.argv[3])
    if manifest_path.exists():
        raise FileExistsError("refusing to overwrite an existing output-freeze manifest")
    freeze_hash = digest(freeze_path)
    outputs = json.loads(outputs_path.read_text(encoding="utf-8"))
    if outputs.get("freeze_manifest_sha256") != freeze_hash:
        raise ValueError("outputs do not reference frozen holdout")
    manifest = {
        "frozen_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "holdout_manifest_sha256": freeze_hash,
        "outputs_path": str(outputs_path),
        "outputs_sha256": digest(outputs_path),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"froze raw outputs: {manifest['outputs_sha256']}")


if __name__ == "__main__":
    main()
