# Plan

This file is the only milestone-status source of truth for the current long run.

## Execution State
- Progress source of truth: this file
- Status vocabulary: `Completed`, `Current`, `Pending`, `Blocked`
- Active window: `CH01-COACH` backfill (closed)
- Current milestone: `Closed`
- Next milestone: `Closed`
- Hot-path milestone specs: `PREP1`, `PREP2`, `CHxx-PAGES`, `CHxx-ASSETS`, `CHxx-NOTES`, `CHxx-COACH`
- Completed preparation milestones: `PREP1`, `PREP2`
- Completed content milestones: `CH01-PAGES`, `CH01-NOTES`, `CH01-COACH`
- Remaining milestones in the active window: none

## Validation command catalog
- `WORKTREE-CLEAN`: `git status --short`
- `KB-VALIDATE`: `python3 scripts/validate_kb.py`
- `UNCLEAR-CHECK`: `rg -n "EPÄSELVÄ|TODO|BLOCKED" processed-docs/01-pages processed-docs/02-concepts processed-docs/03-exercises`
- `ASSET-MANIFEST-CHECK`: `python3 scripts/validate_kb.py`
- `COACH-START-CHECK`: `python3 scripts/validate_kb.py`
- `CH01-COACH-CHECK`: `rg -n "\"chapter_id\"|\"concept_id\"|\"template_id\"" processed-docs/04-coach`
- `CH01-SCAN-CHECK`: `find unprocessed-docs/books/BOOK01/chapter-01/scans -maxdepth 1 -type f`
- `CH01-PAGE-CHECK`: `rg -n "BOOK01-CH01-P00[1-4]|L001|Source image|Status" processed-docs/01-pages/BOOK01/CH01`

## Review topology
- The root thread is the root orchestrator only. It owns milestone selection, worker coordination, and final integration across the active window.
- Use one fresh clean-context `GPT-5.5` `xhigh` milestone worker per milestone when delegation is useful.
- Use one clean-context `GPT-5.5` `xhigh` independent read-only review before committing a milestone when the milestone created or changed processed content.
- Do not use `fork_context` for milestone workers or review workers.
- The review must focus on source citations, line IDs, Finnish wording, formulas, diagrams, broken links, and scope drift.

## Decision rules
- Work one milestone at a time.
- Do not stop at a milestone boundary only to report progress while another active-window milestone remains.
- Page extraction, visual asset extraction, derived study notes, and coach data are separate milestones.
- Use chapter-sized milestones by default. Split a chapter into smaller page ranges if the scan batch is large.
- Keep raw scans unchanged after import.
- Use `EPÄSELVÄ` instead of guessing unclear text, formulas, or diagrams.
- Future chapter windows close only after `CHxx-COACH` is completed or a real blocker is recorded.
- The runtime target is fresh Codex sessions, not a separate standalone app.
- Fresh learner-facing coach sessions start from `processed-docs/04-coach/Start-Coach-Session.md`.
- Record newly discovered work in `Documentation.md`. Do not silently widen the current milestone.

## Future milestone pattern
- `CHxx-PAGES`: import scans, create page transcripts, stable line IDs, and one normalized page image per source page.
- `CHxx-ASSETS`: create reviewed figure, table, photo, and visual exercise crops plus `assets.json`.
- `CHxx-NOTES`: create concept and exercise notes that cite page line IDs and relevant asset IDs.
- `CHxx-COACH`: create structured coach data for explanations, assignments, answer expectations, LLM evaluation guides, and visual explanation hooks.

## Risk register
- OCR can silently damage formulas, decimal commas, exponents, and unit conversions.
- Phone photos can be rotated, cropped, shadowed, or split across two pages.
- Coach quality will suffer if figures are only described in prose and not linked to stable asset IDs.
- Fresh coach sessions can hallucinate outside repo coverage unless the catalog and coach manifests record gaps clearly.
- Book metadata is still provisional until title or cover pages are uploaded.
- Long runs can drift unless `Plan.md` and `Documentation.md` are updated after every milestone.

## Milestones

### PREP1 - Initialize the long-run control stack
- Status: `Completed (2026-05-01)`
- Goal:
  - Create the repository structure, control docs, source inventory, templates, validator, and initial scan import path.
- Scope:
  - Add long-run control docs.
  - Add validation script.
  - Add first provisional `BOOK01/CH01` source inventory.
  - Move the current scan batch into `unprocessed-docs/books/BOOK01/chapter-01/scans/`.
  - Do not transcribe pages or create derived exam notes in this milestone.
- Acceptance:
  - The repo has the planned public directory interfaces.
  - `python3 scripts/validate_kb.py` passes.
  - The next fresh session can start at `CH01-PAGES`.
- Validation:
  - `git status --short`
  - `python3 scripts/validate_kb.py`
- Commit:
  - Commit message pattern: `docs(chunk): PREP1 initialize-exam-kb-control-stack`
- Handoff:
  - `PREP1` is complete. Start content extraction at `CH01-PAGES`.

### PREP2 - Align the repo for Codex-only coach sessions
- Status: `Completed (2026-05-01)`
- Goal:
  - Remove future-app framing and align the repo around Codex-only coach sessions.
- Scope:
  - Update control docs, repo indexes, and README wording to target fresh Codex sessions.
  - Add `processed-docs/04-coach/Start-Coach-Session.md`.
  - Expand the coach data template so future `CHxx-COACH` milestones have a stable schema.
  - Open a one-milestone backfill window for `CH01-COACH`.
  - Do not create the actual `BOOK01/CH01` coach manifest in this milestone.
- Acceptance:
  - `Start-Long-Run.md` remains the extraction entrypoint.
  - The repo names Codex sessions as the coach runtime target.
  - The next fresh work step is `CH01-COACH`.
- Validation:
  - `git status --short`
  - `python3 scripts/validate_kb.py`
- Commit:
  - Commit message pattern: `docs(chunk): PREP2 align-codex-coach-process`
- Handoff:
  - `PREP2` is complete. Start the `CH01-COACH` backfill next.

### CH01-PAGES - Transcribe first chapter scan batch
- Status: `Completed (2026-05-01)`
- Goal:
  - Create reviewed Finnish page transcript files for the four current `BOOK01/CH01` scans.
- Scope:
  - Create one page transcript per scan under `processed-docs/01-pages/BOOK01/CH01/`.
  - Add normalized page images under `processed-docs/assets/pages/BOOK01/CH01/` for every page.
  - Preserve formulas, example numbers, exercise numbers, decimal commas, units, and figure labels.
  - Mark uncertain text as `EPÄSELVÄ`.
  - Do not create broad concept notes or reviewed figure crops yet except tiny cross-links needed by indexes.
- Acceptance:
  - Page IDs `BOOK01-CH01-P001` through `BOOK01-CH01-P004` exist.
  - Each page file has stable line IDs and cites its source image.
  - Each page file links to an existing normalized page image.
  - Important formulas and diagrams are represented in the page file.
- Validation:
  - `git status --short`
  - `python3 scripts/validate_kb.py`
  - `rg -n "BOOK01-CH01-P00[1-4]|L001|Source image|Status" processed-docs/01-pages/BOOK01/CH01`
- Commit:
  - Commit message pattern: `docs(chunk): CH01-PAGES transcribe-first-scan-batch`
- Handoff:
  - `CH01-PAGES` is complete. Future runs should build visual assets in `CHxx-ASSETS` before notes.

### CH01-NOTES - Build first chapter exam notes
- Status: `Completed (2026-05-01)`
- Goal:
  - Create Finnish exam notes from the `CH01-PAGES` transcript layer.
- Scope:
  - Add concise concept notes for formulas, methods, examples, and common mistakes.
  - Add exercise-pattern notes for visible exercises and solved examples.
  - Link every derived fact back to page line IDs.
  - Update note indexes and control docs needed to close the active window cleanly.
  - Keep unresolved scan or OCR questions in the page notes and `Documentation.md`.
- Acceptance:
  - The first chapter has useful exam-prep notes in Finnish.
  - Formula and exercise notes cite page line IDs.
  - Index links make the chapter navigable.
  - After the milestone commit, `Plan.md` sets both `Current milestone` and `Next milestone` to `Closed`.
- Validation:
  - `git status --short`
  - `python3 scripts/validate_kb.py`
  - `rg -n "EPÄSELVÄ|TODO|BLOCKED" processed-docs/01-pages processed-docs/02-concepts processed-docs/03-exercises`
- Commit:
  - Commit message pattern: `docs(chunk): CH01-NOTES build-first-chapter-exam-notes`
- Handoff:
  - `CH01-NOTES` is complete. The active window is closed. Future work should open a new prep or chapter window.

### CH01-COACH - Backfill first chapter coach data
- Status: `Completed (2026-05-01)`
- Goal:
  - Create the first structured coach layer for `BOOK01/CH01`.
- Scope:
  - Add the chapter coach catalog and the `BOOK01/CH01` coach manifest under `processed-docs/04-coach/`.
  - Cover the current CH01 concepts, solved examples, visible exercise patterns, and linked visual assets.
  - Record the known source gap for exercises 18-25.
  - Update validator coverage and handoff docs needed to close the backfill window cleanly.
- Acceptance:
  - A fresh Codex session can start from `processed-docs/04-coach/Start-Coach-Session.md`.
  - The chapter catalog points to a valid CH01 coach manifest and CH01 asset manifest.
  - Coach data cites page line IDs and visual asset IDs.
  - The known coverage gap is explicit and no missing source coverage is invented.
- Validation:
  - `git status --short`
  - `python3 scripts/validate_kb.py`
  - `rg -n "\"chapter_id\"|\"concept_id\"|\"template_id\"" processed-docs/04-coach`
- Commit:
  - Commit message pattern: `docs(chunk): CH01-COACH backfill-first-coach-manifest`
- Handoff:
  - `CH01-COACH` is complete. The current backfill window is closed.
