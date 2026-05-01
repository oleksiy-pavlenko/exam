# Documentation

This file is the audit log and durable run memory. `Plan.md` is the milestone controller.

## Current state snapshot
- Last updated: 2026-05-01
- Progress source of truth: `processed-docs/00-control/Plan.md`
- Active window: `CH01-PAGES` through `CH01-NOTES`
- Current milestone from Plan.md: `CH01-NOTES`
- Next milestone from Plan.md: `Closed`
- Validation command: `python3 scripts/validate_kb.py`
- Worktree check: `git status --short`
- Current provisional book ID: `BOOK01`
- Current provisional chapter ID: `CH01`

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

## Decisions
- Processed page transcripts, concept notes, and exercise notes are Finnish only.
- Control docs may use simple English for clear long-run coordination.
- The first book is `BOOK01` until title page, cover, or ISBN metadata is uploaded.
- The first chapter is `CH01` until better chapter metadata is confirmed.
- Raw scans stay unchanged after import. Rotated or cropped versions are generated assets.
- All subagents use clean-context `GPT-5.5` `xhigh`; `fork_context` is not used for milestone workers or review workers.
- Edge-only neighboring page content in a scan is not complete source coverage. Use only the fully transcribed page lines as evidence for derived notes.

## Blockers
- No current blocker.

## Backlog
- Add book title, publisher, ISBN, edition, and exact chapter name after metadata pages are uploaded.
- Decide whether later large chapters should use one milestone per chapter or one milestone per page range.

## Fresh-session handoff
- Start from `processed-docs/00-control/Plan.md`.
- Current milestone is `CH01-NOTES`.
- First run `git status --short` and `python3 scripts/validate_kb.py`.
- Then create concept and exercise notes from `BOOK01-CH01-P001` through `BOOK01-CH01-P004`.
- Cite page line IDs from `processed-docs/01-pages/BOOK01/CH01/`.
- Do not treat edge-only neighboring page content as complete source coverage.
