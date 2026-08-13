import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / ".cursor/skills/workplace-survival"
EXPECTED_RUNTIME = {"SKILL.md", "REFERENCE.md", "FORMATS.md", "EXAMPLES.md"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    runtime_files = {path.name for path in RUNTIME.iterdir() if path.is_file()}
    require(runtime_files == EXPECTED_RUNTIME, f"runtime package mismatch: {runtime_files}")

    skill = (RUNTIME / "SKILL.md").read_text(encoding="utf-8")
    require(skill.startswith("---\nname: workplace-survival\n"), "invalid frontmatter start")
    frontmatter = skill.split("---", 2)[1]
    description = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
    require(description is not None and len(description.group(1)) < 1024, "invalid description")
    require("disable-model-invocation" not in frontmatter, "automatic invocation disabled")

    for path in RUNTIME.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        require("](" + "\\" not in text, f"Windows-style Markdown link: {path}")
        for target in re.findall(r"\[[^\]]+\]\(([^)#]+\.md)(?:#[^)]+)?\)", text):
            require((path.parent / target).resolve().is_file(), f"missing runtime link: {target}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    require(".cursor/skills/workplace-survival/" in readme, "project install path missing")
    require("~/.cursor/skills/workplace-survival/" in readme, "personal install path missing")
    require("~/.cursor/skills-cursor/" in readme, "managed-directory warning missing")

    manifest = (ROOT / "PUBLISH_MANIFEST.md").read_text(encoding="utf-8")
    publish_section = manifest.split("## Excluded local content", 1)[0]
    manifested = set(re.findall(r"^- `([^`]+)`", publish_section, re.M))
    for target in manifested:
        require((ROOT / target).exists(), f"manifest path missing: {target}")
    publishable = set(
        subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=ROOT,
            text=True,
        ).splitlines()
    )
    require(manifested == publishable, f"manifest mismatch: missing={sorted(publishable - manifested)}, extra={sorted(manifested - publishable)}")

    cases = (ROOT / "tests/TEST_CASES.md").read_text(encoding="utf-8")
    case_ids = [int(value) for value in re.findall(r"^### TC-(\d+)", cases, re.M)]
    require(case_ids == list(range(1, 115)), "functional case IDs are not contiguous")
    require(cases.count("```") % 2 == 0, "unbalanced Markdown code fences")
    require(len(list((ROOT / "tests/fixtures").glob("*.png"))) == 13, "fixture count mismatch")

    print("PACKAGE-01 PASS: runtime=4 files; links/frontmatter/install paths valid; manifest complete; TC-01–TC-114 contiguous; 13 PNG fixtures")


if __name__ == "__main__":
    main()
