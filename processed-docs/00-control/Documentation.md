# Documentation

This file is the audit log and durable run memory. `Plan.md` is the milestone controller.

## Current state snapshot
- Last updated: 2026-05-01
- Progress source of truth: `processed-docs/00-control/Plan.md`
- Active window: `CH01-PAGES` through `CH01-NOTES` (closed)
- Current milestone from Plan.md: `Closed`
- Next milestone from Plan.md: `Closed`
- Validation command: `python3 scripts/validate_kb.py`
- Worktree check: `git status --short`
- Current provisional book ID: `BOOK01`
- Current provisional chapter ID: `CH01`
- Current CH01 visual asset manifest: `processed-docs/assets/pages/BOOK01/CH01/assets.json`
- Current coach data status: not built yet

## Control-doc roles
- `Prompt.md`: binding run spec after `Plan.md` names a milestone
- `Plan.md`: only milestone-status source of truth
- `Implement.md`: execution runbook
- `Review.md`: review contract
- `Documentation.md`: audit log, decisions, blockers, and backlog
- `source-inventory.md`: source IDs and raw scan provenance

## Historical summary
- `PREP1` initialized the long-run control stack on 2026-05-01.
- The first scan batch was imported as provisional `BOOK01/CH01`.
- `CH01-PAGES` created reviewed page transcripts for the first four `BOOK01/CH01` scans.
- `CH01-NOTES` created Finnish concept and exercise notes for the current transcript layer and closed the active window.
- The process now requires app-ready visual asset and coach data milestones for future chapter windows.

## Audit log

### 2026-05-01 - PREP1 completed: initialize the long-run exam knowledgebase
- Added the repository control stack, validation script, indexes, and note templates.
- Imported the first four scan images into `unprocessed-docs/books/BOOK01/chapter-01/scans/` with stable scan IDs.
- Stripped phone metadata from the tracked scan copies before commit so GPS EXIF data is not persisted.
- Recorded provisional source IDs in `source-inventory.md`.
- Left page transcription and study-note creation for later milestones.
- Next milestone: `CH01-PAGES`.

### 2026-05-01 - Process correction: pin subagent specifications
- Clarified that all milestone workers and review workers must use clean-context `GPT-5.5` `xhigh`.
- Clarified that `fork_context` must not be used for milestone workers or review workers.
- Added validator checks so subagent model and context requirements do not drift silently.

### 2026-05-01 - CH01-PAGES completed: transcribe first chapter scan batch
- Created Finnish page transcript files for `BOOK01-CH01-P001` through `BOOK01-CH01-P004`.
- Added normalized readability assets for all four scans under `processed-docs/assets/pages/BOOK01/CH01/`.
- Updated `processed-docs/01-pages/BOOK01/CH01/index.md` and `source-inventory.md`.
- Preserved visible formulas, examples, exercise numbers, units, decimal commas, and main figure labels.
- Recorded line IDs for later concept and exercise notes.
- Ran `python3 scripts/validate_kb.py`; it passed.
- Ran the milestone page check from `Plan.md`; it passed.
- Ran self-review and independent read-only review. No `P0` or `P1` findings remained.
- Independent review noted one `P2`: edge-only neighboring page content must not be treated as full source coverage in later notes. The page wording was clarified.
- Next milestone: `CH01-NOTES`.

### 2026-05-01 - Process correction: strengthen the CH01-NOTES startup contract
- Rewrote `Start-Long-Run.md` so a fresh session continues until every milestone in the active window is completed.
- Tightened `Prompt.md`, `Implement.md`, `Review.md`, and `Plan.md` so the active window closes only when `Plan.md` is updated to `Closed` or a real blocker is recorded.
- Replaced the stale milestone claim in `README.md` with stable pointers to `Plan.md` and `Documentation.md`.
- Extended `scripts/validate_kb.py` with startup-contract checks so the stronger prompt and hard-stop rules do not drift silently.
- The next fresh session should start at `CH01-NOTES`, complete that milestone, and close the current active window.

### 2026-05-01 - CH01-NOTES completed: build first chapter exam notes
- Created Finnish concept notes for `BOOK01/CH01` unit conversions, perimeter and area formulas, and equation-based side solving.
- Created Finnish exercise notes for solved examples 1-6 and visible exercise patterns 1-17 and 26-46.
- Updated `processed-docs/02-concepts/index.md` and `processed-docs/03-exercises/index.md`.
- Checked `BOOK01-CH01-P004:L039` against the normalized page image while aligning exercise patterns; it is task 44 and the line ID stays stable.
- Every derived note cites `BOOK01/CH01` page IDs and line IDs from the transcript layer.
- Recorded that exercises 18-25 are not covered by the current transcript layer because the current scans do not give full source coverage for them.
- Ran `python3 scripts/validate_kb.py`; it passed.
- Ran the unclear-text check from `Plan.md`; it returned no hits.
- Ran self-review against `Review.md`; no `P0` or `P1` self-review findings remained.
- Active window was closed in `Plan.md`.

### 2026-05-01 - Process correction: make extraction app-ready
- Added reviewed CH01 visual crop assets and an app-facing `assets.json` manifest.
- Added `CHxx-ASSETS` and `CHxx-COACH` as required future milestone types.
- Updated the control docs so future chapters produce normalized page images, figure crops, visual exercise assets, and coach data instead of Markdown-only notes.
- Added validator coverage for chapter asset manifests, normalized image links, figure asset coverage, and derived-note source citations.

### 2026-05-01 - Process correction: require derived-note visual links
- Added `## Visuaaliset aineistot` sections to current CH01 concept and exercise notes.
- Linked current derived notes to the CH01 visual asset IDs that match their cited source lines.
- Tightened `scripts/validate_kb.py` so a derived note fails validation when it cites source lines with manifest-covered visual assets but does not name the relevant asset IDs.

## Decisions
- Processed page transcripts, concept notes, and exercise notes are Finnish only.
- Control docs may use simple English for clear long-run coordination.
- The first book is `BOOK01` until title page, cover, or ISBN metadata is uploaded.
- The first chapter is `CH01` until better chapter metadata is confirmed.
- Raw scans stay unchanged after import. Rotated or cropped versions are generated assets.
- All subagents use clean-context `GPT-5.5` `xhigh`; `fork_context` is not used for milestone workers or review workers.
- Edge-only neighboring page content in a scan is not complete source coverage. Use only the fully transcribed page lines as evidence for derived notes.
- Exercises 18-25 are not treated as covered by the current transcript layer.
- Future chapter windows use `CHxx-PAGES`, `CHxx-ASSETS`, `CHxx-NOTES`, and `CHxx-COACH`.
- The app-facing layer is structured manifests. Do not make a future app scrape free-form Markdown as its main data source.
- Every reviewed visual asset must cite source page IDs and line IDs.
- Derived concept and exercise notes must name relevant visual asset IDs when their source line citations overlap manifest-covered visual assets.

## Blockers
- No current blocker.

## Backlog
- Add book title, publisher, ISBN, edition, and exact chapter name after metadata pages are uploaded.
- Decide whether later large chapters should use one milestone per chapter or one milestone per page range.
- Add missing source coverage for exercises 18-25 if later scans include those pages.
- Build a `BOOK01/CH01` coach manifest in a future `CH01-COACH` backfill if the first chapter is used by the app before more pages are imported.

## Fresh-session handoff
- Start from `processed-docs/00-control/Plan.md`.
- Current milestone is `Closed`.
- Next milestone is `Closed`.
- The active window `CH01-PAGES` through `CH01-NOTES` is closed.
- Future work should open a new prep or chapter milestone instead of restarting this window.
- Future chapter windows should use the four-step pattern: pages, assets, notes, coach data.
- Cite page line IDs from `processed-docs/01-pages/BOOK01/CH01/` if later work extends the notes.
- Cite visual asset IDs from `processed-docs/assets/pages/BOOK01/CH01/assets.json` when later work needs images.
- Do not treat edge-only neighboring page content as complete source coverage.
