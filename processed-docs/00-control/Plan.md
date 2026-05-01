# Plan

This file is the only milestone-status source of truth for the current long run.

## Execution State
- Progress source of truth: this file
- Status vocabulary: `Completed`, `Current`, `Pending`, `Blocked`
- Active window: `CH02` second scan batch
- Current milestone: `Closed`
- Next milestone: `Closed`
- Hot-path milestone specs: `PREP1`, `PREP2`, `PREP3`, `PREP4`, `PREP5`, `CHxx-PAGES`, `CHxx-ASSETS`, `CHxx-NOTES`, `CHxx-COACH`
- Completed preparation milestones: `PREP1`, `PREP2`, `PREP3`, `PREP4`, `PREP5`
- Completed content milestones: `CH01-PAGES`, `CH01-NOTES`, `CH01-COACH`, `CH02-PAGES`, `CH02-ASSETS`, `CH02-NOTES`, `CH02-COACH`
- Remaining milestones in the active window: `Closed`

## Validation command catalog
- `WORKTREE-CLEAN`: `git status --short`
- `KB-VALIDATE`: `python3 scripts/validate_kb.py`
- `MODE-STATE-CHECK`: `python3 scripts/validate_kb.py`
- `UNCLEAR-CHECK`: `rg -n "EPÄSELVÄ|TODO|BLOCKED" processed-docs/01-pages processed-docs/02-concepts processed-docs/03-exercises`
- `ASSET-MANIFEST-CHECK`: `python3 scripts/validate_kb.py`
- `COACH-START-CHECK`: `python3 scripts/validate_kb.py`
- `CH01-COACH-CHECK`: `rg -n "\"chapter_id\"|\"concept_id\"|\"template_id\"" processed-docs/04-coach`
- `CH01-SCAN-CHECK`: `find unprocessed-docs/books/BOOK01/chapter-01/scans -maxdepth 1 -type f`
- `CH01-PAGE-CHECK`: `rg -n "BOOK01-CH01-P00[1-4]|L001|Source image|Status" processed-docs/01-pages/BOOK01/CH01`
- `CH02-SCAN-CHECK`: `find unprocessed-docs/books/BOOK01/chapter-02/scans -maxdepth 1 -type f`
- `CH02-PAGE-CHECK`: `rg -n "BOOK01-CH02-P0[0-3][0-9]|L001|Source image|Status" processed-docs/01-pages/BOOK01/CH02`

## Review topology
- The root thread is the root orchestrator only. It owns milestone selection, worker coordination, and final integration across the active window.
- Use one fresh clean-context `GPT-5.5` `xhigh` milestone worker per milestone when delegation is useful.
- Independent review workers are optional for the next long run. Use one only when the user asks, validation or self-review is uncertain, or the milestone is high risk.
- Optional review workers must be read-only clean-context `GPT-5.5` `xhigh`.
- Do not use `fork_context` for milestone workers or optional review workers.
- Self-review and any optional independent review must focus on source citations, line IDs, Finnish wording, formulas, diagrams, broken links, and scope drift.

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
- Ordinary mode switches update `processed-docs/00-control/Mode.md` and use dedicated mode commits. They do not reopen chapter milestones by themselves.
- Record newly discovered work in `Documentation.md`. Do not silently widen the current milestone.
- The current `CH02` window was opened from a 30-image imported scan batch. Page transcription must confirm exact printed page numbers and section boundaries before derived notes are written.
- Tutor-facing book references must prefer canonical printed `Book pages` metadata. Stable `BOOK...` page IDs stay as internal provenance or secondary trace links.

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

### PREP3 - Add persisted tutor and extraction modes
- Status: `Completed (2026-05-01)`
- Goal:
  - Add a committed mode system so fresh sessions know whether they should start in learner-facing tutor mode or milestone-driven extraction mode.
- Scope:
  - Add `processed-docs/00-control/Mode.md` as the only current-mode source of truth.
  - Update startup docs, `AGENTS.md`, and repo indexes to read the current mode first.
  - Make tutor mode use repo material first without treating extracted content as a hard limit.
  - Keep extraction mode as the only path for milestone work and repo content changes.
  - Extend validator coverage so the mode contract does not drift silently.
- Acceptance:
  - Fresh sessions can discover the committed mode from `Mode.md`.
  - Tutor mode has built-in startup behavior, hybrid coverage rules, and unsolved-by-default practice behavior.
  - Extraction mode remains the milestone workflow entrypoint.
  - `python3 scripts/validate_kb.py` passes with the new mode checks.
- Validation:
  - `git status --short`
  - `python3 scripts/validate_kb.py`
- Commit:
  - Commit message pattern: `docs(chunk): PREP3 add-persisted-session-modes`
- Handoff:
  - `PREP3` is complete. Future ordinary mode switches should use dedicated mode commits without reopening `Plan.md` milestones.

### PREP4 - Import second scan batch and open CH02 window
- Status: `Completed (2026-05-01)`
- Goal:
  - Import the new book image drop as a stable raw source batch and prepare the next extraction milestones.
- Scope:
  - Copy the 30 new JPEG scans into `unprocessed-docs/books/BOOK01/chapter-02/scans/`.
  - Strip phone metadata from the tracked scan copies before commit.
  - Record all source paths and original filenames in `source-inventory.md`.
  - Open the standard `CH02-PAGES`, `CH02-ASSETS`, `CH02-NOTES`, and `CH02-COACH` window.
  - Do not transcribe pages, create visual crops, write derived notes, or create coach data in this prep milestone.
- Acceptance:
  - All 30 tracked scan copies exist with stable scan IDs `BOOK01-CH02-S001` through `BOOK01-CH02-S030`.
  - `source-inventory.md` maps those scans to page IDs `BOOK01-CH02-P001` through `BOOK01-CH02-P030`.
  - `Plan.md` sets `CH02-PAGES` as the current milestone and `CH02-ASSETS` as the next milestone.
  - `python3 scripts/validate_kb.py` passes.
- Validation:
  - `git status --short`
  - `python3 scripts/validate_kb.py`
  - `find unprocessed-docs/books/BOOK01/chapter-02/scans -maxdepth 1 -type f`
- Commit:
  - Commit message pattern: `docs(chunk): PREP4 import-second-scan-batch`
- Handoff:
  - `PREP4` is complete. Start content extraction at `CH02-PAGES`.

### PREP5 - Backfill printed book pages for tutor references
- Status: `Completed (2026-05-01)`
- Goal:
  - Make real printed book pages first-class metadata and route learner-facing tutor references through them.
- Scope:
  - Add canonical `Book pages` and `Book page basis` metadata to the current CH01 and CH02 page transcripts.
  - Persist the confirmed printed coverage ranges `176-202`, `208-220`, and `224-248` in the durable control layer.
  - Extend the coach catalog and coach manifests with printed-page lookup data.
  - Update tutor startup guidance and validator coverage so printed-page references do not drift.
- Acceptance:
  - Every current `BOOK01` page transcript has canonical printed page metadata plus the raw visibility note.
  - `processed-docs/04-coach/catalog.json` has `printed_page_ranges` for ready chapters.
  - Each current coach manifest has a complete `page_reference_index` that matches the page transcript layer.
  - Tutor startup guidance prefers learner-facing references such as `kirjan s. 230-231`.
  - `python3 scripts/validate_kb.py` passes.
- Validation:
  - `git status --short`
  - `python3 scripts/validate_kb.py`
  - `rg -n "Book pages|Book page basis" processed-docs/01-pages/BOOK01/CH01 processed-docs/01-pages/BOOK01/CH02`
- Commit:
  - Commit message pattern: `docs(chunk): PREP5 backfill-printed-book-pages`
- Handoff:
  - `PREP5` is complete. Learner-facing tutor references should now prefer printed book pages over internal page IDs.

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

### CH02-PAGES - Transcribe second scan batch
- Status: `Completed (2026-05-01)`
- Goal:
  - Create reviewed Finnish page transcript files for the 30 imported `BOOK01/CH02` scans.
- Scope:
  - Create one page transcript per scan under `processed-docs/01-pages/BOOK01/CH02/`.
  - Add one normalized readability image per page under `processed-docs/assets/pages/BOOK01/CH02/`.
  - Preserve formulas, examples, exercise numbers, decimal commas, units, printed page numbers, and figure labels.
  - Confirm whether `BOOK01/CH02` should stay one provisional chapter or be split later by visible section boundaries.
  - Mark uncertain text as `EPÄSELVÄ`.
  - Do not create derived concept notes, exercise notes, figure crops, or coach manifests in this milestone.
- Acceptance:
  - Page IDs `BOOK01-CH02-P001` through `BOOK01-CH02-P030` exist.
  - Each page file has stable line IDs and cites its source image.
  - Each page file links to an existing normalized page image.
  - Important formulas and diagrams are represented in the page file.
- Validation:
  - `git status --short`
  - `python3 scripts/validate_kb.py`
  - `rg -n "BOOK01-CH02-P0[0-3][0-9]|L001|Source image|Status" processed-docs/01-pages/BOOK01/CH02`
- Commit:
  - Commit message pattern: `docs(chunk): CH02-PAGES transcribe-second-scan-batch`
- Handoff:
  - `CH02-PAGES` is complete. Continue directly to `CH02-ASSETS`.

### CH02-ASSETS - Build second batch visual assets
- Status: `Completed (2026-05-01)`
- Goal:
  - Create reviewed visual assets for the `BOOK01/CH02` transcript layer.
- Scope:
  - Create figure, table, photo, and visual exercise crops under `processed-docs/assets/pages/BOOK01/CH02/crops/`.
  - Create `processed-docs/assets/pages/BOOK01/CH02/assets.json`.
  - Link every visual asset to source page IDs and line IDs.
  - Record a clear no-crop reason in page notes only when a visible figure does not need a separate crop.
- Acceptance:
  - Every `BOOK01/CH02` page has a normalized image.
  - Important figures and visual exercises have manifest-covered assets or clear no-crop reasons.
  - `python3 scripts/validate_kb.py` passes.
- Validation:
  - `git status --short`
  - `python3 scripts/validate_kb.py`
- Commit:
  - Commit message pattern: `docs(chunk): CH02-ASSETS build-second-batch-visual-assets`
- Handoff:
  - `CH02-ASSETS` is complete. Continue directly to `CH02-NOTES`.

### CH02-NOTES - Build second batch exam notes
- Status: `Completed (2026-05-01)`
- Goal:
  - Create Finnish concept and exercise notes from the reviewed `BOOK01/CH02` page and asset layers.
- Scope:
  - Add concise concept notes for formulas, methods, examples, and common mistakes.
  - Add exercise-pattern notes for visible exercises and solved examples.
  - Cite source page IDs, line IDs, and relevant visual asset IDs.
  - Update note indexes.
- Acceptance:
  - Notes are useful for exam preparation and cite the transcript layer.
  - Notes name relevant visual asset IDs when source lines overlap manifest-covered assets.
  - Known scan gaps or unclear parts are recorded instead of guessed.
- Validation:
  - `git status --short`
  - `python3 scripts/validate_kb.py`
  - `rg -n "EPÄSELVÄ|TODO|BLOCKED" processed-docs/01-pages processed-docs/02-concepts processed-docs/03-exercises`
- Commit:
  - Commit message pattern: `docs(chunk): CH02-NOTES build-second-batch-exam-notes`
- Handoff:
  - `CH02-NOTES` is complete. Continue directly to `CH02-COACH`.

### CH02-COACH - Build second batch coach data
- Status: `Completed (2026-05-01)`
- Goal:
  - Create structured coach data for `BOOK01/CH02`.
- Scope:
  - Add or update the coach catalog entry for `BOOK01/CH02`.
  - Create `processed-docs/04-coach/BOOK01/CH02/coach.json`.
  - Cover the reviewed concepts, examples, exercise patterns, known gaps, and visual hooks.
  - Cite source line IDs and visual asset IDs where relevant.
- Acceptance:
  - A fresh Codex coach session can discover `BOOK01/CH02` from the catalog.
  - Coach data has explanation, assignment, answer expectation, LLM evaluation, hint, and visual hook coverage where the source supports it.
  - `Plan.md` closes the active window when this milestone is done.
- Validation:
  - `git status --short`
  - `python3 scripts/validate_kb.py`
  - `rg -n "\"chapter_id\"|\"concept_id\"|\"template_id\"" processed-docs/04-coach`
- Commit:
  - Commit message pattern: `docs(chunk): CH02-COACH build-second-batch-coach-manifest`
- Handoff:
  - `CH02-COACH` is complete. Set both `Current milestone` and `Next milestone` to `Closed`.
