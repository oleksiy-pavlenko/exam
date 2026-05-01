#!/usr/bin/env python3
from __future__ import annotations

import json
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
    "processed-docs/04-coach/index.md",
    "processed-docs/04-coach/Start-Coach-Session.md",
    "processed-docs/assets/pages/BOOK01/CH01/index.md",
    "processed-docs/assets/pages/BOOK01/CH01/assets.json",
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
        "Coach data rules",
    ],
    "processed-docs/00-control/Plan.md": [
        "Execution State",
        "Validation command catalog",
        "Review topology",
        "Decision rules",
        "Future milestone pattern",
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
    "processed-docs/04-coach/Start-Coach-Session.md": [
        "Purpose",
        "Coach runtime rules",
        "First Codex prompt",
        "Required inputs",
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

REQUIRED_CONTRACT_PHRASES = {
    "processed-docs/00-control/Start-Long-Run.md": [
        "EVERY MILESTONE IN THE ACTIVE WINDOW IS COMPLETED",
        "DO NOT STOP AT THE END OF A MILESTONE ONLY TO REPORT PROGRESS",
        "root orchestrator",
    ],
    "processed-docs/00-control/Implement.md": [
        "root orchestrator",
        "active-window milestone as `Current`, `Pending`, or `Blocked`",
    ],
    "processed-docs/04-coach/Start-Coach-Session.md": [
        "Start from `processed-docs/04-coach/catalog.json` when it exists.",
        "Use repo-local coach data first.",
        "If a question is outside current repo coverage, say that clearly and do not invent book coverage.",
    ],
}

README_FORBIDDEN_PATTERNS = [
    re.compile(r"Next milestone is `[^`]+`"),
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
READABILITY_ASSET_RE = re.compile(r"Readability asset:\s+(?:!?\[[^\]]*\]\(([^)]+)\)|`([^`]+)`)")
SOURCE_LINE_REF_DETAIL_RE = re.compile(r"(BOOK\d+-CH\d+-P\d{3}):L(\d{3})(?:-L(\d{3}))?")
ASSET_ID_RE = re.compile(r"BOOK\d+-CH\d+-P\d{3}-(?:PAGE|F\d{3})")
ASSET_LINE_REF_RE = re.compile(r"^L\d{3}(?:-L\d{3})?$")
ALLOWED_ASSET_TYPES = {
    "page_normalized",
    "figure_crop",
    "exercise_crop",
    "table_crop",
    "photo_crop",
}
ALLOWED_ASSET_USES = {
    "source_review",
    "explanation",
    "assignment",
    "verification",
    "visual_animation",
}


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
        readability_match = READABILITY_ASSET_RE.search(text)
        if not readability_match:
            add_error(errors, f"{relative}: missing readability asset")
        else:
            target = readability_match.group(1) or readability_match.group(2)
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                add_error(errors, f"{relative}: readability asset leaves repo: {target}")
            else:
                if not resolved.exists():
                    add_error(errors, f"{relative}: missing readability asset file: {target}")


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


def page_path_for_id(page_id: str) -> Path:
    match = re.fullmatch(r"(BOOK\d+)-CH(\d+)-P\d{3}", page_id)
    if not match:
        return ROOT / "missing"
    book_id = match.group(1)
    chapter_id = f"CH{match.group(2)}"
    return ROOT / "processed-docs" / "01-pages" / book_id / chapter_id / f"{page_id}.md"


def section_body(text: str, section: str) -> str:
    matches = list(SECTION_RE.finditer(text))
    body = ""
    for index, match in enumerate(matches):
        if match.group(1) == section:
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            body = text[start:end].strip()
    return body


def line_span(line_ref: str) -> tuple[int, int] | None:
    if not ASSET_LINE_REF_RE.fullmatch(line_ref):
        return None
    numbers = [int(item) for item in re.findall(r"L(\d{3})", line_ref)]
    if len(numbers) == 1:
        span = (numbers[0], numbers[0])
    else:
        span = (numbers[0], numbers[1])
    if span[0] > span[1]:
        span = None
    return span


def spans_overlap(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return left[0] <= right[1] and right[0] <= left[1]


def asset_line_spans(asset: dict[str, object]) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    for line_ref in asset.get("source_line_ids", []):
        if isinstance(line_ref, str):
            span = line_span(line_ref)
            if span is not None:
                spans.append(span)
    return spans


def source_line_refs(text: str) -> list[tuple[str, tuple[int, int]]]:
    refs: list[tuple[str, tuple[int, int]]] = []
    for match in SOURCE_LINE_REF_DETAIL_RE.finditer(text):
        page_id = match.group(1)
        start = int(match.group(2))
        end = int(match.group(3) or match.group(2))
        if start <= end:
            refs.append((page_id, (start, end)))
    return refs


def manifest_paths() -> list[Path]:
    assets_root = ROOT / "processed-docs" / "assets" / "pages"
    return sorted(assets_root.rglob("assets.json")) if assets_root.exists() else []


def load_asset_manifests(errors: list[str]) -> dict[str, list[dict[str, object]]]:
    assets_by_page: dict[str, list[dict[str, object]]] = {}
    seen_asset_ids: set[str] = set()
    required_fields = {
        "asset_id",
        "asset_type",
        "path",
        "source_page_id",
        "source_line_ids",
        "description_fi",
        "related_concepts",
        "related_exercises",
        "uses",
    }
    for path in manifest_paths():
        relative = path.relative_to(ROOT).as_posix()
        try:
            manifest = json.loads(read_text(path))
        except json.JSONDecodeError as exc:
            add_error(errors, f"{relative}: invalid JSON: {exc}")
            continue
        assets = manifest.get("assets")
        if not isinstance(assets, list) or not assets:
            add_error(errors, f"{relative}: assets must be a non-empty list")
            continue
        for asset in assets:
            if not isinstance(asset, dict):
                add_error(errors, f"{relative}: asset entry must be an object")
                continue
            missing = sorted(required_fields - set(asset))
            if missing:
                add_error(errors, f"{relative}: asset missing fields {missing}")
                continue
            asset_id = asset["asset_id"]
            asset_type = asset["asset_type"]
            asset_path = asset["path"]
            source_page_id = asset["source_page_id"]
            source_line_ids = asset["source_line_ids"]
            uses = asset["uses"]
            if not isinstance(asset_id, str) or not asset_id:
                add_error(errors, f"{relative}: asset has invalid asset_id")
                continue
            if asset_id in seen_asset_ids:
                add_error(errors, f"{relative}: duplicate asset_id {asset_id}")
            seen_asset_ids.add(asset_id)
            if asset_type not in ALLOWED_ASSET_TYPES:
                add_error(errors, f"{relative}: {asset_id} has invalid asset_type {asset_type}")
            if not isinstance(asset_path, str):
                add_error(errors, f"{relative}: {asset_id} path must be a string")
            else:
                resolved = (ROOT / asset_path).resolve()
                try:
                    resolved.relative_to(ROOT)
                except ValueError:
                    add_error(errors, f"{relative}: {asset_id} path leaves repo: {asset_path}")
                else:
                    if not resolved.exists():
                        add_error(errors, f"{relative}: {asset_id} missing asset file {asset_path}")
            if not isinstance(source_page_id, str):
                add_error(errors, f"{relative}: {asset_id} source_page_id must be a string")
                continue
            page_path = page_path_for_id(source_page_id)
            if not page_path.exists():
                add_error(errors, f"{relative}: {asset_id} missing source page {source_page_id}")
                continue
            page_text = read_text(page_path)
            page_line_ids = set(LINE_ID_RE.findall(page_text))
            if not isinstance(source_line_ids, list) or not source_line_ids:
                add_error(errors, f"{relative}: {asset_id} source_line_ids must be a non-empty list")
                continue
            for line_ref in source_line_ids:
                if not isinstance(line_ref, str):
                    add_error(errors, f"{relative}: {asset_id} has non-string source line")
                    continue
                span = line_span(line_ref)
                if span is None:
                    add_error(errors, f"{relative}: {asset_id} invalid line ref {line_ref}")
                    continue
                endpoints = [f"`L{span[0]:03d}`", f"`L{span[1]:03d}`"]
                for endpoint in endpoints:
                    if endpoint not in page_line_ids:
                        add_error(errors, f"{relative}: {asset_id} missing source line {endpoint} in {source_page_id}")
            if not isinstance(uses, list) or not uses:
                add_error(errors, f"{relative}: {asset_id} uses must be a non-empty list")
            else:
                for use in uses:
                    if use not in ALLOWED_ASSET_USES:
                        add_error(errors, f"{relative}: {asset_id} has invalid use {use}")
            assets_by_page.setdefault(source_page_id, []).append(asset)
    return assets_by_page


def check_chapter_asset_manifests(errors: list[str]) -> None:
    pages_root = ROOT / "processed-docs" / "01-pages"
    for chapter_index in sorted(pages_root.glob("BOOK*/CH*/index.md")):
        relative = chapter_index.relative_to(ROOT).as_posix()
        parts = chapter_index.relative_to(pages_root).parts
        if len(parts) < 3:
            continue
        book_id, chapter_id = parts[0], parts[1]
        manifest = ROOT / "processed-docs" / "assets" / "pages" / book_id / chapter_id / "assets.json"
        if not manifest.exists():
            add_error(errors, f"{relative}: missing chapter asset manifest {manifest.relative_to(ROOT).as_posix()}")


def check_page_figure_asset_coverage(errors: list[str], assets_by_page: dict[str, list[dict[str, object]]]) -> None:
    pages_root = ROOT / "processed-docs" / "01-pages"
    for path in markdown_files(pages_root):
        relative = path.relative_to(ROOT).as_posix()
        if relative.endswith("/index.md") or relative == "processed-docs/01-pages/index.md":
            continue
        text = read_text(path)
        page_match = PAGE_ID_RE.search(text)
        if not page_match:
            continue
        page_id = page_match.group(1)
        figure_body = section_body(text, "Figures")
        if not figure_body or "None yet." in figure_body:
            continue
        figure_assets = [
            asset for asset in assets_by_page.get(page_id, [])
            if asset.get("asset_type") != "page_normalized"
        ]
        asset_spans: list[tuple[int, int]] = []
        for asset in figure_assets:
            for line_ref in asset.get("source_line_ids", []):
                if isinstance(line_ref, str):
                    span = line_span(line_ref)
                    if span is not None:
                        asset_spans.append(span)
        for line in figure_body.splitlines():
            stripped = line.strip()
            if not stripped.startswith("-"):
                continue
            if "no-crop" in stripped.lower() or "ei erillistä assettia" in stripped.lower():
                continue
            numbers = [int(number) for number in re.findall(r"L(\d{3})", stripped)]
            if not numbers:
                add_error(errors, f"{relative}: figure bullet has no line IDs: {stripped}")
                continue
            figure_span = (min(numbers), max(numbers))
            if not any(spans_overlap(figure_span, asset_span) for asset_span in asset_spans):
                add_error(errors, f"{relative}: figure lines L{figure_span[0]:03d}-L{figure_span[1]:03d} have no manifest-covered crop")


def check_derived_note_citations(errors: list[str], assets_by_page: dict[str, list[dict[str, object]]]) -> None:
    all_asset_ids: set[str] = set()
    visual_assets_by_page: dict[str, list[dict[str, object]]] = {}
    for page_id, assets in assets_by_page.items():
        for asset in assets:
            asset_id = asset.get("asset_id")
            if isinstance(asset_id, str):
                all_asset_ids.add(asset_id)
            if asset.get("asset_type") != "page_normalized":
                visual_assets_by_page.setdefault(page_id, []).append(asset)

    for root in [ROOT / "processed-docs" / "02-concepts", ROOT / "processed-docs" / "03-exercises"]:
        for path in markdown_files(root):
            relative = path.relative_to(ROOT).as_posix()
            if path.name == "index.md":
                continue
            text = read_text(path)
            refs = source_line_refs(text)
            if not refs:
                add_error(errors, f"{relative}: missing source page line citations")
                continue
            mentioned_asset_ids = set(ASSET_ID_RE.findall(text))
            for asset_id in sorted(mentioned_asset_ids - all_asset_ids):
                add_error(errors, f"{relative}: unknown visual asset ID {asset_id}")
            required_asset_ids: set[str] = set()
            for page_id, source_span in refs:
                for asset in visual_assets_by_page.get(page_id, []):
                    asset_id = asset.get("asset_id")
                    if not isinstance(asset_id, str):
                        continue
                    if any(spans_overlap(source_span, asset_span) for asset_span in asset_line_spans(asset)):
                        required_asset_ids.add(asset_id)
            if required_asset_ids:
                visual_body = section_body(text, "Visuaaliset aineistot")
                visual_asset_ids = set(ASSET_ID_RE.findall(visual_body))
                if not visual_body:
                    add_error(errors, f"{relative}: missing section ## Visuaaliset aineistot")
                    continue
                missing = sorted(required_asset_ids - visual_asset_ids)
                if missing:
                    add_error(errors, f"{relative}: missing relevant visual asset IDs {missing}")


def check_subagent_specs(errors: list[str]) -> None:
    for relative in SUBAGENT_SPEC_FILES:
        path = ROOT / relative
        if not path.exists():
            continue
        text = read_text(path)
        for term in SUBAGENT_SPEC_TERMS:
            if term not in text:
                add_error(errors, f"{relative}: missing subagent spec term `{term}`")


def check_required_contract_phrases(errors: list[str]) -> None:
    for relative, phrases in REQUIRED_CONTRACT_PHRASES.items():
        path = ROOT / relative
        if not path.exists():
            continue
        text = read_text(path)
        for phrase in phrases:
            if phrase not in text:
                add_error(errors, f"{relative}: missing contract phrase `{phrase}`")


def check_readme_handoff(errors: list[str]) -> None:
    path = ROOT / "README.md"
    if path.exists():
        text = read_text(path)
        for pattern in README_FORBIDDEN_PATTERNS:
            if pattern.search(text):
                add_error(errors, "README.md: should not claim a specific next milestone")


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
    check_chapter_asset_manifests(errors)
    assets_by_page = load_asset_manifests(errors)
    check_page_figure_asset_coverage(errors, assets_by_page)
    check_derived_note_citations(errors, assets_by_page)
    check_subagent_specs(errors)
    check_required_contract_phrases(errors)
    check_readme_handoff(errors)
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
