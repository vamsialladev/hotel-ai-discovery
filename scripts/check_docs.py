"""Checks the discovery pack: required documents exist, the README links every one, no placeholders.

python scripts/check_docs.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_DOCS = [
    "docs/DISCOVERY.md",
    "docs/PROBLEM_SELECTION.md",
    "docs/SOW.md",
    "docs/PRICING.md",
    "docs/ARCHITECTURE_PROPOSAL.md",
    "docs/SECURITY_QUESTIONNAIRE.md",
    "docs/RISKS.md",
    "docs/INTERVIEW_WALKTHROUGH.md",
    "docs/VIDEO_SCRIPT.md",
    "docs/DECISIONS.md",
    "docs/ARCHITECTURE.md",
]

# Shapes that must never appear in a public document. Uppercase-only so ordinary words don't match.
PLACEHOLDER = re.compile(r"\bYOUR-[A-Z]+(?:-[A-Z]+)*\b|\bTODO\b|\bTBD\b|\bLorem\b|example\.com|\[YOU\]")
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")


def markdown_files(root: Path = ROOT) -> list[Path]:
    skip = {".git", ".venv", "node_modules", ".pytest_cache", ".ruff_cache"}
    return sorted(p for p in root.rglob("*.md") if not skip & set(p.relative_to(root).parts))


def placeholders(text: str) -> list[str]:
    return sorted(set(PLACEHOLDER.findall(text)))


def local_links(text: str) -> list[str]:
    return [link for link in LINK.findall(text) if not link.startswith(("http://", "https://", "mailto:"))]


def problems(root: Path = ROOT) -> list[str]:
    found: list[str] = []
    for doc in REQUIRED_DOCS:
        if not (root / doc).is_file():
            found.append(f"missing {doc}")
    readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").is_file() else ""
    for doc in REQUIRED_DOCS:
        if doc not in readme:
            found.append(f"README does not link {doc}")
    for path in markdown_files(root):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root).as_posix()
        if rel != "scripts/check_docs.py":
            for hit in placeholders(text):
                found.append(f"{rel}: placeholder {hit!r}")
        for link in local_links(text):
            if not (path.parent / link).resolve().exists():
                found.append(f"{rel}: broken link {link}")
    return found


def main() -> int:
    found = problems()
    for line in found:
        print(line)
    print(f"{len(found)} problem(s)" if found else "discovery pack OK")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
