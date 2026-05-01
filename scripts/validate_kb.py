#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "processed-docs/index.md",
    "processed-docs/00-control/Prompt.md",
    "processed-docs/00-control/Plan.md",
    "processed-docs/00-control/Implement.md",
    "processed-docs/00-control/Review.md",
    "processed-docs/00-control/Documentation.md",
    "processed-docs/00-control/Start-Long-Run.md",
    "processed-docs/00-control/source-inventory.md",
    "processed-docs/01-pages/index.md",
    "processed-docs/01-pages/BOOK01/CH01/index.md",
    "processed-docs/02-concepts/index.md",
    "processed-docs/03-exercises/index.md",
]

SECTION_REQUIREMENTS = {
    "processed-docs/00-control/Prompt.md": [
        "Mission",
        "Non-goals",
        "Autonomous window",
        "Hard constraints",
        "Source and scope boundaries",
        "Run deliverables",
        "Done when this run stops",
        "Writing rules",
        "Citation rules",
        "Diagram rules",
    ],
    "processed-docs/00-control/Plan.md": [
        "Execution State",
        "Validation command catalog",
        "Review topology",
        "Decision rules",
        "Risk register",
        "Milestones",
    ],
    "processed-docs/00-control/Implement.md": [
        "Objective",
        "Non-Negotiable Rules",
        "Mandatory Inputs",
        "Agent Topology",
        "Hard Stop Gate",
        "Root Orchestrator Loop",
        "Milestone Worker Contract",
        "Milestone Completion Checklist",
        "Validation Rules",
        "Review Gate Rule",
        "Resume Rule",
        "Stop Rule",
        "Commit Rule",
    ],
    "processed-docs/00-control/Review.md": [
        "Purpose",
        "Review order",
        "Self-review checklist",
        "Review worker contract",
        "Severity rules",
        "Review prompt shape",
    ],
    "processed-docs/00-control/Documentation.md": [
        "Current state snapshot",
        "Control-doc roles",
        "Historical summary",
        "Audit log",
        "Decisions",
        "Blockers",
        "Backlog",
        "Fresh-session handoff",
    ],
}

SUBAGENT_SPEC_FILES = [
    "AGENTS.md",
    "processed-docs/00-control/Plan.md",
    "processed-docs/00-control/Implement.md",
    "processed-docs/00-control/Review.md",
    "processed-docs/00-control/Start-Long-Run.md",
    "processed-docs/00-control/Documentation.md",
]

SUBAGENT_SPEC_TERMS = [
    "GPT-5.5",
    "xhigh",
    "clean-context",
    "fork_context",
]

PAGE_REQUIRED_SECTIONS = [
    "Source",
    "Lines",
    "Formulas",
    "Figures",
    "Exercises",
    "Unclear text",
    "Related notes",
]

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
PAGE_ID_RE = re.compile(r"`(BOOK\d+-CH\d+-P\d{3})`")
SOURCE_IMAGE_RE = re.compile(r"`(unprocessed-docs/books/[^`]+\.jpg)`")
LINE_ID_RE = re.compile(r"`L\d{3}`")


def read_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return text


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def check_required_files(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.exists():
            add_error(errors, f"missing required file: {relative}")


def check_required_sections(errors: list[str]) -> None:
    for relative, sections in SECTION_REQUIREMENTS.items():
        path = ROOT / relative
        if path.exists():
            text = read_text(path)
            found = set(SECTION_RE.findall(text))
            for section in sections:
                if section not in found:
                    add_error(errors, f"{relative}: missing section ## {section}")


def check_source_inventory(errors: list[str]) -> None:
    path = ROOT / "processed-docs/00-control/source-inventory.md"
    if path.exists():
        text = read_text(path)
        page_ids = PAGE_ID_RE.findall(text)
        source_paths = SOURCE_IMAGE_RE.findall(text)
        if not page_ids:
            add_error(errors, "source-inventory.md: no page IDs found")
        if not source_paths:
            add_error(errors, "source-inventory.md: no source image paths found")
        for source_path in source_paths:
            if not (ROOT / source_path).exists():
                add_error(errors, f"source-inventory.md: missing source image {source_path}")


def markdown_files(root: Path) -> list[Path]:
    paths = sorted(root.rglob("*.md")) if root.exists() else []
    return paths


def check_page_files(errors: list[str]) -> None:
    pages_root = ROOT / "processed-docs/01-pages"
    for path in markdown_files(pages_root):
        relative = path.relative_to(ROOT).as_posix()
        if relative.endswith("/index.md") or relative == "processed-docs/01-pages/index.md":
            continue
        text = read_text(path)
        found = set(SECTION_RE.findall(text))
        for section in PAGE_REQUIRED_SECTIONS:
            if section not in found:
                add_error(errors, f"{relative}: missing section ## {section}")
        if not PAGE_ID_RE.search(text):
            add_error(errors, f"{relative}: missing page ID")
        if not SOURCE_IMAGE_RE.search(text):
            add_error(errors, f"{relative}: missing source image path")
        if not LINE_ID_RE.search(text):
            add_error(errors, f"{relative}: missing line IDs")


def check_markdown_links(errors: list[str]) -> None:
    for path in markdown_files(ROOT / "processed-docs"):
        text = read_text(path)
        relative = path.relative_to(ROOT).as_posix()
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            clean_target = target.split("#", 1)[0]
            if not clean_target:
                continue
            resolved = (path.parent / clean_target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                add_error(errors, f"{relative}: link leaves repo: {target}")
                continue
            if not resolved.exists():
                add_error(errors, f"{relative}: broken link: {target}")


def check_plan_state(errors: list[str]) -> None:
    path = ROOT / "processed-docs/00-control/Plan.md"
    if path.exists():
        text = read_text(path)
        current = re.findall(r"- Current milestone: `([^`]+)`", text)
        next_items = re.findall(r"- Next milestone: `([^`]+)`", text)
        if len(current) != 1:
            add_error(errors, "Plan.md: expected exactly one Current milestone field")
        if len(next_items) != 1:
            add_error(errors, "Plan.md: expected exactly one Next milestone field")
        statuses = re.findall(r"^- Status: `([^`]+)`", text, re.MULTILINE)
        allowed_prefixes = ("Completed", "Current", "Pending", "Blocked")
        for status in statuses:
            if not status.startswith(allowed_prefixes):
                add_error(errors, f"Plan.md: invalid milestone status `{status}`")


def check_subagent_specs(errors: list[str]) -> None:
    for relative in SUBAGENT_SPEC_FILES:
        path = ROOT / relative
        if not path.exists():
            continue
        text = read_text(path)
        for term in SUBAGENT_SPEC_TERMS:
            if term not in text:
                add_error(errors, f"{relative}: missing subagent spec term `{term}`")


def check_git_ignored_noise(errors: list[str]) -> None:
    completed = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    for line in completed.stdout.splitlines():
        if line.endswith(".DS_Store"):
            add_error(errors, f"git status exposes ignored noise: {line}")


def main() -> int:
    errors: list[str] = []
    check_required_files(errors)
    check_required_sections(errors)
    check_source_inventory(errors)
    check_page_files(errors)
    check_markdown_links(errors)
    check_plan_state(errors)
    check_subagent_specs(errors)
    check_git_ignored_noise(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        exit_code = 1
    else:
        print("validate_kb: OK")
        exit_code = 0
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
