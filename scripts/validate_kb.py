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
    "processed-docs/00-control/Mode.md",
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
    "processed-docs/04-coach/catalog.json",
    "processed-docs/04-coach/BOOK01/CH01/coach.json",
    "processed-docs/assets/pages/BOOK01/CH01/index.md",
    "processed-docs/assets/pages/BOOK01/CH01/assets.json",
]

SECTION_REQUIREMENTS = {
    "processed-docs/00-control/Mode.md": [
        "Current mode",
        "Startup rules",
        "Switching rules",
    ],
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
        "processed-docs/00-control/Mode.md",
        "Tutor sessions are not milestone work.",
    ],
    "processed-docs/00-control/Implement.md": [
        "root orchestrator",
        "active-window milestone as `Current`, `Pending`, or `Blocked`",
    ],
    "processed-docs/04-coach/Start-Coach-Session.md": [
        "Start from `processed-docs/04-coach/catalog.json` when it exists.",
        "Use repo-local coach data first.",
        "The user does not need to repeat a tutor prompt.",
        "Web search is allowed when it is useful.",
        "Generated images are allowed when they help the explanation.",
        "do not solve the exercises immediately by default",
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
SOURCE_REF_FULL_RE = re.compile(r"(BOOK\d+-CH\d+-P\d{3}):L(\d{3})(?:-L(\d{3}))?$")
MODE_RE = re.compile(r"^- Current mode: `([^`]+)`", re.MULTILINE)
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
COACH_CATALOG_STATUSES = {
    "draft",
    "ready",
    "ready_with_gaps",
}
ALLOWED_MODES = {
    "tutor",
    "extraction",
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


def check_mode_state(errors: list[str]) -> None:
    path = ROOT / "processed-docs/00-control/Mode.md"
    if path.exists():
        text = read_text(path)
        modes = MODE_RE.findall(text)
        if len(modes) != 1:
            add_error(errors, "Mode.md: expected exactly one Current mode field")
        else:
            current_mode = modes[0]
            if current_mode not in ALLOWED_MODES:
                add_error(errors, f"Mode.md: invalid current mode `{current_mode}`")


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


def source_ref_parts(source_ref: str) -> tuple[str, tuple[int, int]] | None:
    match = SOURCE_REF_FULL_RE.fullmatch(source_ref)
    parts = None
    if match is not None:
        start = int(match.group(2))
        end = int(match.group(3) or match.group(2))
        if start <= end:
            parts = (match.group(1), (start, end))
    return parts


def check_string_list(
    errors: list[str],
    relative: str,
    label: str,
    values: object,
    allow_empty: bool,
) -> None:
    if not isinstance(values, list):
        add_error(errors, f"{relative}: {label} must be a list")
    else:
        if not values and not allow_empty:
            add_error(errors, f"{relative}: {label} must be a non-empty list")
        for value in values:
            if not isinstance(value, str) or not value.strip():
                add_error(errors, f"{relative}: {label} has an invalid string value")


def check_source_ref_list(errors: list[str], relative: str, label: str, source_refs: object) -> None:
    check_string_list(errors, relative, label, source_refs, allow_empty=False)
    if isinstance(source_refs, list):
        for source_ref in source_refs:
            if not isinstance(source_ref, str):
                continue
            parts = source_ref_parts(source_ref)
            if parts is None:
                add_error(errors, f"{relative}: {label} has invalid source ref {source_ref}")
            else:
                page_id, span = parts
                page_path = page_path_for_id(page_id)
                if not page_path.exists():
                    add_error(errors, f"{relative}: {label} points to missing page {page_id}")
                else:
                    page_text = read_text(page_path)
                    page_line_ids = set(LINE_ID_RE.findall(page_text))
                    endpoints = [f"`L{span[0]:03d}`", f"`L{span[1]:03d}`"]
                    for endpoint in endpoints:
                        if endpoint not in page_line_ids:
                            add_error(errors, f"{relative}: {label} missing source line {endpoint} in {page_id}")


def all_asset_ids(assets_by_page: dict[str, list[dict[str, object]]]) -> set[str]:
    asset_ids: set[str] = set()
    for assets in assets_by_page.values():
        for asset in assets:
            asset_id = asset.get("asset_id")
            if isinstance(asset_id, str):
                asset_ids.add(asset_id)
    return asset_ids


def check_visual_asset_id_list(
    errors: list[str],
    relative: str,
    label: str,
    visual_asset_ids: object,
    known_asset_ids: set[str],
) -> None:
    check_string_list(errors, relative, label, visual_asset_ids, allow_empty=False)
    if isinstance(visual_asset_ids, list):
        for asset_id in visual_asset_ids:
            if isinstance(asset_id, str) and asset_id not in known_asset_ids:
                add_error(errors, f"{relative}: {label} references unknown asset ID {asset_id}")


def manifest_paths() -> list[Path]:
    assets_root = ROOT / "processed-docs" / "assets" / "pages"
    return sorted(assets_root.rglob("assets.json")) if assets_root.exists() else []


def coach_manifest_paths() -> list[Path]:
    coach_root = ROOT / "processed-docs" / "04-coach"
    return sorted(coach_root.rglob("coach.json")) if coach_root.exists() else []


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


def load_coach_catalog(errors: list[str]) -> dict[str, dict[str, object]]:
    entries_by_chapter: dict[str, dict[str, object]] = {}
    path = ROOT / "processed-docs/04-coach/catalog.json"
    if path.exists():
        relative = path.relative_to(ROOT).as_posix()
        try:
            catalog = json.loads(read_text(path))
        except json.JSONDecodeError as exc:
            add_error(errors, f"{relative}: invalid JSON: {exc}")
        else:
            chapters = catalog.get("chapters")
            if catalog.get("manifest_version") != 1:
                add_error(errors, f"{relative}: manifest_version must be 1")
            if catalog.get("language") != "fi":
                add_error(errors, f"{relative}: language must be fi")
            if not isinstance(chapters, list) or not chapters:
                add_error(errors, f"{relative}: chapters must be a non-empty list")
            else:
                seen_chapters: set[str] = set()
                required_fields = {
                    "chapter_id",
                    "status",
                    "coach_manifest_path",
                    "asset_manifest_path",
                    "source_page_ids",
                    "concept_ids",
                    "known_gaps_fi",
                }
                for entry in chapters:
                    if not isinstance(entry, dict):
                        add_error(errors, f"{relative}: chapter entry must be an object")
                        continue
                    missing = sorted(required_fields - set(entry))
                    if missing:
                        add_error(errors, f"{relative}: chapter entry missing fields {missing}")
                        continue
                    chapter_id = entry["chapter_id"]
                    status = entry["status"]
                    coach_manifest_path = entry["coach_manifest_path"]
                    asset_manifest_path = entry["asset_manifest_path"]
                    source_page_ids = entry["source_page_ids"]
                    concept_ids = entry["concept_ids"]
                    known_gaps_fi = entry["known_gaps_fi"]
                    if not isinstance(chapter_id, str) or not chapter_id:
                        add_error(errors, f"{relative}: chapter entry has invalid chapter_id")
                        continue
                    if chapter_id in seen_chapters:
                        add_error(errors, f"{relative}: duplicate chapter_id {chapter_id}")
                    seen_chapters.add(chapter_id)
                    if not isinstance(status, str) or status not in COACH_CATALOG_STATUSES:
                        add_error(errors, f"{relative}: {chapter_id} has invalid status {status}")
                    if not isinstance(coach_manifest_path, str):
                        add_error(errors, f"{relative}: {chapter_id} coach_manifest_path must be a string")
                    else:
                        coach_path = (ROOT / coach_manifest_path).resolve()
                        if not coach_path.exists():
                            add_error(errors, f"{relative}: {chapter_id} missing coach manifest {coach_manifest_path}")
                    if not isinstance(asset_manifest_path, str):
                        add_error(errors, f"{relative}: {chapter_id} asset_manifest_path must be a string")
                    else:
                        asset_path = (ROOT / asset_manifest_path).resolve()
                        if not asset_path.exists():
                            add_error(errors, f"{relative}: {chapter_id} missing asset manifest {asset_manifest_path}")
                    check_string_list(errors, relative, f"{chapter_id} source_page_ids", source_page_ids, allow_empty=False)
                    if isinstance(source_page_ids, list):
                        for page_id in source_page_ids:
                            if isinstance(page_id, str) and not page_path_for_id(page_id).exists():
                                add_error(errors, f"{relative}: {chapter_id} references missing source page {page_id}")
                    check_string_list(errors, relative, f"{chapter_id} concept_ids", concept_ids, allow_empty=False)
                    check_string_list(errors, relative, f"{chapter_id} known_gaps_fi", known_gaps_fi, allow_empty=True)
                    entries_by_chapter.setdefault(chapter_id, entry)
    return entries_by_chapter


def load_coach_manifests(
    errors: list[str],
    assets_by_page: dict[str, list[dict[str, object]]],
    catalog_entries: dict[str, dict[str, object]],
) -> None:
    manifest_summaries: dict[str, dict[str, object]] = {}
    known_asset_ids = all_asset_ids(assets_by_page)
    required_top_fields = {
        "manifest_version",
        "book_id",
        "chapter_id",
        "language",
        "coverage_notes_fi",
        "concepts",
        "assignment_templates",
    }
    required_concept_fields = {
        "concept_id",
        "title_fi",
        "source_refs",
        "visual_asset_ids",
        "coach_goal_fi",
        "explanation_steps_fi",
        "common_mistakes_fi",
        "visual_demo_steps_fi",
        "related_assignment_ids",
    }
    required_assignment_fields = {
        "template_id",
        "title_fi",
        "concept_ids",
        "source_refs",
        "visual_asset_ids",
        "prompt_shape_fi",
        "answer_expectation_fi",
        "llm_evaluation_guide_fi",
        "hint_steps_fi",
        "variation_notes_fi",
    }
    for path in coach_manifest_paths():
        relative = path.relative_to(ROOT).as_posix()
        try:
            manifest = json.loads(read_text(path))
        except json.JSONDecodeError as exc:
            add_error(errors, f"{relative}: invalid JSON: {exc}")
            continue
        missing = sorted(required_top_fields - set(manifest))
        if missing:
            add_error(errors, f"{relative}: missing top-level fields {missing}")
            continue
        chapter_id = manifest["chapter_id"]
        concepts = manifest["concepts"]
        assignment_templates = manifest["assignment_templates"]
        if manifest.get("manifest_version") != 1:
            add_error(errors, f"{relative}: manifest_version must be 1")
        if manifest.get("language") != "fi":
            add_error(errors, f"{relative}: language must be fi")
        if not isinstance(chapter_id, str) or not chapter_id:
            add_error(errors, f"{relative}: chapter_id must be a non-empty string")
            continue
        if chapter_id in manifest_summaries:
            add_error(errors, f"{relative}: duplicate coach manifest for {chapter_id}")
            continue
        check_string_list(errors, relative, "coverage_notes_fi", manifest["coverage_notes_fi"], allow_empty=False)
        if not isinstance(concepts, list) or not concepts:
            add_error(errors, f"{relative}: concepts must be a non-empty list")
            continue
        if not isinstance(assignment_templates, list) or not assignment_templates:
            add_error(errors, f"{relative}: assignment_templates must be a non-empty list")
            continue
        concept_ids: set[str] = set()
        assignment_ids: set[str] = set()
        related_assignments_by_concept: dict[str, list[str]] = {}
        source_pages: set[str] = set()
        for concept in concepts:
            if not isinstance(concept, dict):
                add_error(errors, f"{relative}: concept entry must be an object")
                continue
            missing_concept_fields = sorted(required_concept_fields - set(concept))
            if missing_concept_fields:
                add_error(errors, f"{relative}: concept missing fields {missing_concept_fields}")
                continue
            concept_id = concept["concept_id"]
            title_fi = concept["title_fi"]
            coach_goal_fi = concept["coach_goal_fi"]
            source_refs = concept["source_refs"]
            visual_asset_ids = concept["visual_asset_ids"]
            if not isinstance(concept_id, str) or not concept_id:
                add_error(errors, f"{relative}: concept has invalid concept_id")
                continue
            if concept_id in concept_ids:
                add_error(errors, f"{relative}: duplicate concept_id {concept_id}")
            concept_ids.add(concept_id)
            if not isinstance(title_fi, str) or not title_fi.strip():
                add_error(errors, f"{relative}: {concept_id} title_fi must be a non-empty string")
            if not isinstance(coach_goal_fi, str) or not coach_goal_fi.strip():
                add_error(errors, f"{relative}: {concept_id} coach_goal_fi must be a non-empty string")
            check_source_ref_list(errors, relative, f"{concept_id} source_refs", source_refs)
            if isinstance(source_refs, list):
                for source_ref in source_refs:
                    if isinstance(source_ref, str):
                        parts = source_ref_parts(source_ref)
                        if parts is not None:
                            source_pages.add(parts[0])
            check_visual_asset_id_list(errors, relative, f"{concept_id} visual_asset_ids", visual_asset_ids, known_asset_ids)
            check_string_list(errors, relative, f"{concept_id} explanation_steps_fi", concept["explanation_steps_fi"], allow_empty=False)
            check_string_list(errors, relative, f"{concept_id} common_mistakes_fi", concept["common_mistakes_fi"], allow_empty=False)
            check_string_list(errors, relative, f"{concept_id} visual_demo_steps_fi", concept["visual_demo_steps_fi"], allow_empty=False)
            check_string_list(errors, relative, f"{concept_id} related_assignment_ids", concept["related_assignment_ids"], allow_empty=False)
            if isinstance(concept["related_assignment_ids"], list):
                related_assignments_by_concept[concept_id] = list(concept["related_assignment_ids"])
        for assignment in assignment_templates:
            if not isinstance(assignment, dict):
                add_error(errors, f"{relative}: assignment entry must be an object")
                continue
            missing_assignment_fields = sorted(required_assignment_fields - set(assignment))
            if missing_assignment_fields:
                add_error(errors, f"{relative}: assignment missing fields {missing_assignment_fields}")
                continue
            template_id = assignment["template_id"]
            title_fi = assignment["title_fi"]
            prompt_shape_fi = assignment["prompt_shape_fi"]
            answer_expectation_fi = assignment["answer_expectation_fi"]
            llm_evaluation_guide_fi = assignment["llm_evaluation_guide_fi"]
            source_refs = assignment["source_refs"]
            visual_asset_ids = assignment["visual_asset_ids"]
            if not isinstance(template_id, str) or not template_id:
                add_error(errors, f"{relative}: assignment has invalid template_id")
                continue
            if template_id in assignment_ids:
                add_error(errors, f"{relative}: duplicate template_id {template_id}")
            assignment_ids.add(template_id)
            if not isinstance(title_fi, str) or not title_fi.strip():
                add_error(errors, f"{relative}: {template_id} title_fi must be a non-empty string")
            if not isinstance(prompt_shape_fi, str) or not prompt_shape_fi.strip():
                add_error(errors, f"{relative}: {template_id} prompt_shape_fi must be a non-empty string")
            if not isinstance(answer_expectation_fi, str) or not answer_expectation_fi.strip():
                add_error(errors, f"{relative}: {template_id} answer_expectation_fi must be a non-empty string")
            if not isinstance(llm_evaluation_guide_fi, str) or not llm_evaluation_guide_fi.strip():
                add_error(errors, f"{relative}: {template_id} llm_evaluation_guide_fi must be a non-empty string")
            check_string_list(errors, relative, f"{template_id} concept_ids", assignment["concept_ids"], allow_empty=False)
            check_source_ref_list(errors, relative, f"{template_id} source_refs", source_refs)
            if isinstance(source_refs, list):
                for source_ref in source_refs:
                    if isinstance(source_ref, str):
                        parts = source_ref_parts(source_ref)
                        if parts is not None:
                            source_pages.add(parts[0])
            check_visual_asset_id_list(errors, relative, f"{template_id} visual_asset_ids", visual_asset_ids, known_asset_ids)
            check_string_list(errors, relative, f"{template_id} hint_steps_fi", assignment["hint_steps_fi"], allow_empty=False)
            check_string_list(errors, relative, f"{template_id} variation_notes_fi", assignment["variation_notes_fi"], allow_empty=False)
        for concept_id, related_assignment_ids in related_assignments_by_concept.items():
            for template_id in related_assignment_ids:
                if isinstance(template_id, str) and template_id not in assignment_ids:
                    add_error(errors, f"{relative}: {concept_id} references missing assignment template {template_id}")
        for assignment in assignment_templates:
            if isinstance(assignment, dict) and isinstance(assignment.get("concept_ids"), list):
                template_id = assignment.get("template_id")
                for concept_id in assignment["concept_ids"]:
                    if isinstance(concept_id, str) and concept_id not in concept_ids:
                        add_error(errors, f"{relative}: {template_id} references missing concept_id {concept_id}")
        manifest_summaries[chapter_id] = {
            "path": relative,
            "concept_ids": concept_ids,
            "source_pages": source_pages,
        }
    for chapter_id, entry in catalog_entries.items():
        summary = manifest_summaries.get(chapter_id)
        if summary is None:
            add_error(errors, f"processed-docs/04-coach/catalog.json: {chapter_id} has no matching coach manifest")
            continue
        coach_manifest_path = entry.get("coach_manifest_path")
        if coach_manifest_path != summary["path"]:
            add_error(errors, f"processed-docs/04-coach/catalog.json: {chapter_id} coach_manifest_path does not match loaded manifest")
        concept_ids = entry.get("concept_ids")
        if isinstance(concept_ids, list):
            catalog_concepts = set(concept_ids)
            if catalog_concepts != summary["concept_ids"]:
                add_error(errors, f"processed-docs/04-coach/catalog.json: {chapter_id} concept_ids do not match coach manifest")
        source_page_ids = entry.get("source_page_ids")
        if isinstance(source_page_ids, list):
            catalog_pages = set(source_page_ids)
            if not summary["source_pages"].issubset(catalog_pages):
                add_error(errors, f"processed-docs/04-coach/catalog.json: {chapter_id} source_page_ids do not cover all coach refs")
    for chapter_id in manifest_summaries:
        if chapter_id not in catalog_entries:
            add_error(errors, f"processed-docs/04-coach/{chapter_id}: coach manifest missing catalog entry")


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
    check_mode_state(errors)
    check_plan_state(errors)
    check_chapter_asset_manifests(errors)
    assets_by_page = load_asset_manifests(errors)
    check_page_figure_asset_coverage(errors, assets_by_page)
    check_derived_note_citations(errors, assets_by_page)
    catalog_entries = load_coach_catalog(errors)
    load_coach_manifests(errors, assets_by_page, catalog_entries)
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
