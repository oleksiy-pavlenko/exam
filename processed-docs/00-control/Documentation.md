# Documentation

This file is the audit log and durable run memory. `Plan.md` is the milestone controller.

## Current state snapshot
- Last updated: 2026-05-01
- Progress source of truth: `processed-docs/00-control/Plan.md`
- Active window: `CH02` second scan batch
- Current milestone from Plan.md: `Closed`
- Next milestone from Plan.md: `Closed`
- Validation command: `python3 scripts/validate_kb.py`
- Worktree check: `git status --short`
- Current mode source of truth: `processed-docs/00-control/Mode.md`
- Current committed mode: `extraction`
- Current provisional book ID: `BOOK01`
- Current provisional chapter ID: `CH02`
- Current CH01 visual asset manifest: `processed-docs/assets/pages/BOOK01/CH01/assets.json`
- Current CH02 raw scan path: `unprocessed-docs/books/BOOK01/chapter-02/scans/`
- Current coach data status: startup prompt, coach catalog with printed page ranges, and CH01/CH02 coach manifests with `page_reference_index` are built

## Control-doc roles
- `Prompt.md`: binding run spec after `Plan.md` names a milestone
- `Plan.md`: only milestone-status source of truth
- `Mode.md`: only current-mode source of truth
- `Implement.md`: execution runbook
- `Review.md`: review contract
- `Documentation.md`: audit log, decisions, blockers, and backlog
- `source-inventory.md`: source IDs and raw scan provenance

## Historical summary
- `PREP1` initialized the long-run control stack on 2026-05-01.
- The first scan batch was imported as provisional `BOOK01/CH01`.
- `CH01-PAGES` created reviewed page transcripts for the first four `BOOK01/CH01` scans.
- `CH01-NOTES` created Finnish concept and exercise notes for the current transcript layer and closed the active window.
- `PREP2` pivoted the repo from future-app wording to Codex-only coach sessions and opened a `CH01-COACH` backfill.
- `CH01-COACH` created the first coach catalog entry and the first usable chapter coach manifest for fresh Codex sessions.
- `PREP3` added persisted `tutor` and `extraction` modes with `Mode.md` as the startup source of truth.
- `PREP4` imported the second 30-image scan batch as provisional `BOOK01/CH02` and opened the `CH02` extraction window.
- `PREP5` backfilled canonical printed book pages into the page and coach layers so tutor references can cite real textbook pages.
- The next long run no longer requires a separate review subagent for every processed-content milestone. Self-review stays mandatory; independent review workers are optional.
- Future chapter windows still require visual asset and coach data milestones.

## Audit log

### 2026-05-01 - PREP1 completed: initialize the long-run exam knowledgebase
- Added the repository control stack, validation script, indexes, and note templates.
- Imported the first four scan images into `unprocessed-docs/books/BOOK01/chapter-01/scans/` with stable scan IDs.
- Stripped phone metadata from the tracked scan copies before commit so GPS EXIF data is not persisted.
- Recorded provisional source IDs in `source-inventory.md`.
- Left page transcription and study-note creation for later milestones.
- Next milestone: `CH01-PAGES`.

### 2026-05-01 - Process correction: pin subagent specifications
- Clarified the worker safety rule for milestone workers and review workers: clean-context `GPT-5.5` `xhigh`.
- Clarified that `fork_context` must not be used for milestone workers or review workers.
- Added validator checks so subagent model and context requirements do not drift silently.
- Later process correction made review workers optional, but kept the same safety rule for any review worker that is used.

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

### 2026-05-01 - Process correction: make extraction coach-ready
- Added reviewed CH01 visual crop assets and a coach-facing `assets.json` manifest.
- Added `CHxx-ASSETS` and `CHxx-COACH` as required future milestone types.
- Updated the control docs so future chapters produce normalized page images, figure crops, visual exercise assets, and coach data instead of Markdown-only notes.
- Added validator coverage for chapter asset manifests, normalized image links, figure asset coverage, and derived-note source citations.

### 2026-05-01 - Process correction: require derived-note visual links
- Added `## Visuaaliset aineistot` sections to current CH01 concept and exercise notes.
- Linked current derived notes to the CH01 visual asset IDs that match their cited source lines.
- Tightened `scripts/validate_kb.py` so a derived note fails validation when it cites source lines with manifest-covered visual assets but does not name the relevant asset IDs.

### 2026-05-01 - PREP2 completed: align the repo for Codex-only coach sessions
- Replaced future-app framing in the repo with Codex-only coach wording.
- Added `processed-docs/04-coach/Start-Coach-Session.md` for fresh learner-facing sessions.
- Expanded the coach data template so future `CHxx-COACH` milestones have a stable runtime contract.
- Kept `processed-docs/00-control/Start-Long-Run.md` as the extraction entrypoint.
- Opened a one-milestone `CH01-COACH` backfill window for the current first chapter.

### 2026-05-01 - CH01-COACH completed: backfill first chapter coach data
- Added `processed-docs/04-coach/catalog.json` as the first lookup file for fresh coach sessions.
- Added `processed-docs/04-coach/BOOK01/CH01/coach.json` with concept explanations, assignment templates, LLM evaluation guides, hints, and visual demo hooks.
- Linked the new coach layer to `BOOK01/CH01` page line IDs and visual asset IDs only.
- Recorded the known source gap for exercises 18-25 in both the catalog and the chapter coach manifest.
- Extended `scripts/validate_kb.py` so the coach catalog and coach manifests are checked structurally.
- Closed the one-milestone `CH01-COACH` backfill window in `Plan.md`.

### 2026-05-01 - PREP3 completed: add persisted tutor and extraction modes
- Added `processed-docs/00-control/Mode.md` as the only current-mode source of truth for fresh sessions.
- Set the committed default mode to `tutor`.
- Reworked `AGENTS.md` so startup, tutor defaults, and extraction rules depend on the committed mode.
- Updated the tutor startup contract so the user does not need to repeat a setup prompt and practice stays unsolved by default.
- Updated the extraction startup contract so tutor sessions are kept separate from milestone work.
- Extended `scripts/validate_kb.py` so mode state and tutor-mode contract phrases are checked structurally.
- Future ordinary mode switches should use dedicated `docs(mode): ...` commits instead of reopening `Plan.md` milestones.

### 2026-05-01 - Mode switch: extraction
- Switched `processed-docs/00-control/Mode.md` from `tutor` to `extraction` after the user requested extraction work.
- The image drop in `copy-from-here-and-delete/` was the source-prep input for the next import step.

### 2026-05-01 - PREP4 completed: import second scan batch and open CH02 window
- Imported 30 new JPEG scans into `unprocessed-docs/books/BOOK01/chapter-02/scans/` with stable scan IDs `BOOK01-CH02-S001` through `BOOK01-CH02-S030`.
- Stripped phone metadata from the tracked scan copies before commit so GPS EXIF data is not persisted.
- Recorded original filenames and source paths in `source-inventory.md`.
- Treated the batch as provisional `BOOK01/CH02` because the visible material continues after the current processed pages and includes later numbered geometry sections. Page transcription must confirm exact printed page numbers and section boundaries.
- Opened the standard `CH02-PAGES`, `CH02-ASSETS`, `CH02-NOTES`, and `CH02-COACH` milestone window in `Plan.md`.
- Next milestone: `CH02-PAGES`.

### 2026-05-01 - Process correction: make the next long run lighter
- Removed the mandatory independent review subagent gate from the extraction runbook.
- Kept self-review mandatory for every milestone.
- Made independent read-only review workers optional. Use one only when the user asks, validation or self-review is uncertain, or the milestone is high risk.
- Kept the worker safety rule: every milestone worker and optional review worker uses clean-context `GPT-5.5` `xhigh`, and `fork_context` is not used.

### 2026-05-01 - CH02-PAGES completed: transcribe second scan batch
- Created Finnish page transcript files for `BOOK01-CH02-P001` through `BOOK01-CH02-P030`.
- Added normalized readability assets for all 30 CH02 scans under `processed-docs/assets/pages/BOOK01/CH02/`.
- Updated `source-inventory.md` so the CH02 scan rows no longer show transcript work as pending.
- Recorded visible section boundaries across the batch: luku 2 monikulmiot, luku 3 ympyrä, luku 4 ympyrän kulmat, luku 5 kaaren pituus, luku 7 ympyrän pinta-ala, luku 8 sektorin pinta-ala, luku 9 ympyrälaskut, luku 11 Pythagoraan lause, luku 12 hypotenuusan ratkaiseminen, luku 13 kateetin ratkaiseminen, luku 14 suorakulmaisen kolmion piiri ja pinta-ala, luku 15 Pythagoraan harjoittelu ja myöhempi tasakylkisiin tai tasasivuisiin kolmioihin siirtyvä harjoitusjakso.
- Marked genuinely unclear printed page numbers or partial neighboring content as `EPÄSELVÄ` instead of guessing.
- Ran `python3 scripts/validate_kb.py`; it passed after page-note figure bullets were marked as temporary `no-crop` placeholders for the later asset milestone.
- Ran the CH02 page check from `Plan.md`; it passed.
- Ran self-review against `Review.md`; no `P0` or `P1` self-review findings remained.
- Requested one optional independent read-only spot-check because the milestone was high risk.
- The spot-check found one `P1` printed-page-number issue on `BOOK01-CH02-P014` and one `P2` wording issue on `BOOK01-CH02-P011`; both were fixed before the milestone close.
- Next milestone: `CH02-ASSETS`.

### 2026-05-01 - CH02-ASSETS completed: build second batch visual assets
- Added `processed-docs/assets/pages/BOOK01/CH02/assets.json` as the structured visual manifest for the current CH02 transcript layer.
- Added `processed-docs/assets/pages/BOOK01/CH02/index.md` and `processed-docs/01-pages/BOOK01/CH02/index.md`.
- Added one visual cluster crop per CH02 page under `processed-docs/assets/pages/BOOK01/CH02/crops/` so every page-level figure range has a stable non-page asset ID for later notes and coach data.
- Kept the crop pass intentionally broad: the current CH02 crops are page-level visual clusters, not tight per-task cutouts.
- Removed the temporary `no-crop` wording from the CH02 page notes after the manifest-covered crop assets existed.
- Updated `source-inventory.md` so the CH02 scan rows show transcript and visual asset work as completed.
- Ran `python3 scripts/validate_kb.py`; it passed.
- Ran self-review against `Review.md`; no `P0` or `P1` self-review findings remained.
- Next milestone: `CH02-NOTES`.

### 2026-05-01 - CH02-NOTES completed: build second batch exam notes
- Added five CH02 concept notes that follow the visible lesson units instead of the provisional source-batch boundary.
- Added CH02 solved-example and exercise-pattern notes under `processed-docs/03-exercises/`.
- Updated `processed-docs/02-concepts/index.md` and `processed-docs/03-exercises/index.md`.
- Every derived note cites CH02 page IDs and line IDs from the transcript layer.
- Every derived note names relevant CH02 visual asset IDs where the cited source lines overlap manifest-covered visual ranges.
- Ran `python3 scripts/validate_kb.py`; it passed.
- Ran the unclear-text check from `Plan.md`; the only hits were accepted page-layer `EPÄSELVÄ` markers for uncertain printed page numbers or one unseen late-section title, not note-layer TODOs.
- Requested one optional independent read-only spot-check because the notes compress many lesson units; it returned no material `P0`, `P1`, or `P2` findings in the sampled note files.
- Next milestone: `CH02-COACH`.

### 2026-05-01 - CH02-COACH completed: build second batch coach manifest
- Added `processed-docs/04-coach/BOOK01/CH02/coach.json` with five lesson-unit concepts and twelve assignment templates for the visible CH02 material.
- Added a `BOOK01-CH02` entry to `processed-docs/04-coach/catalog.json` with `ready_with_gaps` status.
- Updated `processed-docs/04-coach/index.md` so fresh sessions can discover the CH02 coach manifest directly.
- Kept the coach manifest structured by visible lesson units even though the provenance batch stays `BOOK01-CH02`.
- Recorded the known CH02 gaps: several uncertain printed page numbers, one partly unseen late-section title, and the current broad first-pass crop strategy.
- Ran `python3 scripts/validate_kb.py`; it passed.
- Ran the CH02 coach check from `Plan.md`; it passed.
- Ran self-review against `Review.md`; no `P0` or `P1` self-review findings remained.
- The active CH02 window is now closed in `Plan.md`.

### 2026-05-01 - Mode switch: tutor
- Switched `processed-docs/00-control/Mode.md` from `extraction` to `tutor` after the user requested learner-facing work.
- The extraction window in `Plan.md` stays closed.
- Fresh sessions should now continue with `processed-docs/04-coach/Start-Coach-Session.md`.

### 2026-05-01 - Mode switch: extraction
- Switched `processed-docs/00-control/Mode.md` back to `extraction` before repo maintenance work resumed.
- The closed CH02 extraction window stayed closed in `Plan.md`.
- Fresh extraction sessions should continue from `processed-docs/00-control/Start-Long-Run.md`.

### 2026-05-01 - PREP5 completed: backfill printed book pages for tutor references
- Added canonical `Book pages` and `Book page basis` metadata to all current `BOOK01` page transcripts while keeping `Printed pages visible` as the raw observation note.
- Corrected the first CH01 scan pair from the old wrong `170-173` transcript metadata to the confirmed printed range `176-179`.
- Recorded the confirmed printed coverage ranges `176-202`, `208-220`, and `224-248` in `source-inventory.md`.
- Extended the coach catalog with chapter-level `printed_page_ranges`.
- Extended both current coach manifests with a full `page_reference_index` that maps every `source_page_id` to learner-facing printed book pages and basis values.
- Updated the tutor startup contract so learner-facing book references prefer printed pages such as `kirjan s. 230-231` and keep internal `BOOK...` refs secondary.
- Extended `scripts/validate_kb.py` so the page layer, coach layer, and catalog must agree on printed page metadata.
- Ran `python3 scripts/validate_kb.py`; it passed.

## Decisions
- Processed page transcripts, concept notes, and exercise notes are Finnish only.
- Control docs may use simple English for clear long-run coordination.
- The first book is `BOOK01` until title page, cover, or ISBN metadata is uploaded.
- The first chapter is `CH01` until better chapter metadata is confirmed.
- `BOOK01-CH02` is the provisional ID for the second uploaded 30-image scan batch. It may contain more than one visible textbook section, so the page milestone must record section boundaries before derived notes are written.
- Raw scans stay unchanged after import. Rotated or cropped versions are generated assets.
- All milestone workers and optional review workers use clean-context `GPT-5.5` `xhigh`; `fork_context` is not used for them.
- Independent review subagents are optional, not mandatory. Self-review remains mandatory for every milestone.
- Edge-only neighboring page content in a scan is not complete source coverage. Use only the fully transcribed page lines as evidence for derived notes.
- Exercises 18-25 are not treated as covered by the current transcript layer.
- Future chapter windows use `CHxx-PAGES`, `CHxx-ASSETS`, `CHxx-NOTES`, and `CHxx-COACH`.
- The coach runtime is fresh Codex sessions, not a separate standalone app.
- `processed-docs/00-control/Mode.md` is the only current-mode source of truth for fresh sessions.
- The committed mode is `extraction`.
- Tutor mode uses repo material first, but it is not hard-limited by extracted coverage.
- Tutor mode may use own knowledge, web search, and generated images when they help.
- Tutor mode keeps exercises unsolved by default until the user asks for a full solution.
- The coach-facing layer is structured manifests. Do not make future coach sessions scrape free-form Markdown as their main data source.
- Fresh learner-facing sessions should start from `processed-docs/04-coach/Start-Coach-Session.md` and then read `processed-docs/04-coach/catalog.json`.
- Every reviewed visual asset must cite source page IDs and line IDs.
- Derived concept and exercise notes must name relevant visual asset IDs when their source line citations overlap manifest-covered visual assets.
- Canonical `Book pages` metadata is the tutor-facing source for original textbook page references.
- When one page number in an aukeama is unclear, scan order and the confirmed coverage ranges are authoritative for inferring the missing mate page.
- Keep `BOOK01-CH02` as the provisional source-batch ID for provenance, but split later durable notes and coach material by visible section boundaries instead of treating the whole 30-image batch as one teaching unit.
- The first CH02 asset pass uses one page-level visual cluster crop per page. Later notes or coach work may tighten individual crops when a page needs a more focused visual target.
- The durable CH02 study layer should follow visible lesson units, not the provisional `CH02` source-batch boundary.
- The CH02 coach manifest should preserve the provisional source-batch provenance while exposing visible lesson units as separate concepts and assignments.

## Blockers
- No current blocker.

## Backlog
- Add book title, publisher, ISBN, edition, and exact chapter name after metadata pages are uploaded.
- Decide whether later large chapters should use one milestone per chapter or one milestone per page range.
- Add missing source coverage for exercises 18-25 if later scans include those pages.
- Add later extracted chapters to `processed-docs/04-coach/catalog.json` as they reach `CHxx-COACH`.
- Replace inferred printed page numbers with directly visible confirmation later if clearer scans or metadata pages are added.
- If later scans fill the current gaps between `202-208` or `220-224`, extend the printed coverage ranges and page-reference indexes without renaming source IDs.
- Tighten individual CH02 crop boundaries later if a concept note or coach prompt needs a smaller figure than the current page-level cluster crop.

## Fresh-session handoff
- Read `processed-docs/00-control/Mode.md` first.
- If the current mode is `tutor`, start from `processed-docs/04-coach/Start-Coach-Session.md`.
- If the current mode is `extraction`, start from `processed-docs/00-control/Start-Long-Run.md`.
- Start extraction runs from `processed-docs/00-control/Plan.md` and `processed-docs/00-control/Start-Long-Run.md`.
- Start learner-facing coach sessions from `processed-docs/04-coach/Start-Coach-Session.md`.
- Current milestone is `Closed`.
- Next milestone is `Closed`.
- The committed mode is `extraction`.
- The `PREP4` source-prep work is complete.
- The `PREP5` printed-page backfill is complete.
- The active `CH02` window uses the four-step pattern: pages, assets, notes, coach data.
- The active `CH02` window is closed. Use `Plan.md` as the milestone proof and this file as the handoff.
- `CH02-PAGES`, `CH02-ASSETS`, `CH02-NOTES`, and `CH02-COACH` are complete. The current durable CH02 layer now includes page transcripts, asset manifest, note files, coach catalog entry, and coach manifest.
- `CH02` page line IDs and first-pass visual asset IDs now exist across the note and coach layers.
- Use canonical `Book pages` metadata from page transcripts and `page_reference_index` for learner-facing references to the original book.
- Cite page line IDs from `processed-docs/01-pages/BOOK01/CH01/` if later work extends the notes.
- Cite visual asset IDs from `processed-docs/assets/pages/BOOK01/CH01/assets.json` when later work needs images.
- Use `processed-docs/04-coach/catalog.json` to find ready coach chapters and known coverage gaps.
- Do not treat edge-only neighboring page content as complete source coverage.
