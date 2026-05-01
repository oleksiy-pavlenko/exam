# Implement

Use this file as the execution runbook. `Prompt.md` is the binding run spec. `Plan.md` is the only milestone-status source of truth. `Documentation.md` is the audit log and durable run memory.

## Objective
- Process scanned math book chapters into a reliable Finnish exam knowledgebase.
- Produce app-ready visual assets and coach data for a later interactive exam coach.
- Keep the run resumable across Codex sessions.
- Continue until the active window is closed or a real stop rule fires.

## Non-Negotiable Rules
- Start from `Plan.md`.
- Continue work until the active window is closed or a real stop rule fires.
- Do not start a milestone while the worktree is dirty.
- Run `python3 scripts/validate_kb.py` before content work and after edits.
- One verified milestone equals one commit.
- Keep raw scans unchanged after import.
- Use Finnish for processed page, concept, and exercise content.
- Cite derived notes with page IDs and line IDs.
- Cite visual assets with page IDs and line IDs.
- Mark uncertainty with `EPÄSELVÄ`; do not guess.
- Do not use outside sources unless they are added to `unprocessed-docs/` and recorded in `source-inventory.md`.

## Mandatory Inputs
- `processed-docs/00-control/Prompt.md`
- `processed-docs/00-control/Plan.md`
- `processed-docs/00-control/Implement.md`
- `processed-docs/00-control/Review.md`
- `processed-docs/00-control/Documentation.md`
- `processed-docs/00-control/source-inventory.md`

## Agent Topology
- The root thread is the root orchestrator only. It owns milestone selection, final integration, and continuation across the active window.
- Use one fresh clean-context `GPT-5.5` `xhigh` milestone worker per milestone when delegation is useful.
- Review workers must be read-only clean-context `GPT-5.5` `xhigh` workers.
- Do not use `fork_context` for any milestone worker or review worker.
- Review workers must read repo state directly from files, not from chat memory.
- Give reviewers the milestone ID, touched files, acceptance target, and control-doc paths.

## Hard Stop Gate
- The root orchestrator must never send a final handoff while `Plan.md` still shows any active-window milestone as `Current`, `Pending`, or `Blocked`.
- Stop only if the active window is `Closed`, a real blocker is recorded, validation cannot be repaired, review cannot be satisfied, or the user redirects the work.
- If `Plan.md` says `Closed`, do not restart old milestones unless a later prep milestone reopens work.

## Root Orchestrator Loop
1. Read `Plan.md` and `Documentation.md`.
2. Run `git status --short`.
3. Run `python3 scripts/validate_kb.py`.
4. If `Plan.md` shows `Closed` for both `Current milestone` and `Next milestone`, stop and use `Documentation.md` as the later-work handoff.
5. If one active-window milestone is marked `Blocked`, stop and use `Documentation.md` as the blocker handoff.
6. Select the milestone marked `Current`.
7. Keep edits inside the milestone scope.
8. Run validation and milestone-specific checks.
9. Run self-review from `Review.md`.
10. Run independent review when processed content changed.
11. Fix blocking findings.
12. Update `Documentation.md` and `Plan.md`.
13. Commit once with the milestone message from `Plan.md`.
14. If the active window is still open after the commit, continue directly into the next milestone instead of stopping at the boundary.

## Milestone Worker Contract
1. Reread the mandatory inputs.
2. Inspect the relevant scans or page notes directly.
3. Create only the files needed for the assigned milestone.
4. Use stable source IDs and line IDs.
5. Keep page notes close to the source; keep study notes concise.
6. Update the asset manifests, note indexes, coach indexes, and control docs required by the milestone.
7. Run validation and milestone-specific checks.
8. Run self-review from `Review.md`.
9. Run one independent read-only clean-context `GPT-5.5` `xhigh` review when processed content changed.
10. Fix every `P0` and `P1` finding inside the same milestone.
11. Update `Documentation.md` and `Plan.md`. If the milestone closes the active window, set both `Current milestone` and `Next milestone` to `Closed`.
12. Commit once with the milestone message from `Plan.md`.
13. Report touched files, unresolved uncertainties, and validation results.

## Milestone Completion Checklist
- Scope stayed inside the current milestone.
- Required files and links exist.
- Source image, page ID, and line ID citations are present.
- Normalized page images, visual crops, and asset manifests are present when required by the milestone.
- Finnish wording is clear.
- Formulas, units, decimal commas, and exercise numbers were checked.
- `Documentation.md` records the result and handoff.
- `Plan.md` shows the next correct milestone state.
- If the active window ended, `Plan.md` shows `Closed` for both `Current milestone` and `Next milestone`.
- Validation passed.
- Exactly one commit was created.

## Validation Rules
- Always run `python3 scripts/validate_kb.py`.
- Run `git status --short` before starting and after commit.
- For page milestones, run the page-specific `rg` command from `Plan.md`.
- For asset milestones, confirm every page transcript has a normalized image and every listed figure has manifest-covered asset coverage or a clear no-crop reason.
- For coach milestones, confirm coach data references source line IDs and visual asset IDs where relevant.
- Before closing a notes milestone, run `rg -n "EPÄSELVÄ|TODO|BLOCKED" processed-docs/01-pages processed-docs/02-concepts processed-docs/03-exercises` and decide whether each hit is acceptable or blocking.
- Before closing the last milestone in the active window, confirm that `Plan.md` sets both `Current milestone` and `Next milestone` to `Closed`.

## Review Gate Rule
- Self-review is mandatory for every milestone.
- Independent review is mandatory when page transcripts, concept notes, exercise notes, or figure assets changed.
- Treat `P0` and `P1` findings as blocking.
- Fix blocking findings inside the same milestone.
- For the last active-window milestone, review also checks that `Plan.md` and `Documentation.md` close the window cleanly.
- Record non-blocking follow-up in `Documentation.md`.

## Resume Rule
- After an interruption, read `Plan.md`, `Documentation.md`, and `Implement.md`.
- Inspect `git status --short --branch` and `git log -1 --oneline`.
- If the tree is clean and `Plan.md` shows `Closed` for both `Current milestone` and `Next milestone`, treat the window as finished and do not restart it.
- If the tree is clean, continue from the milestone marked `Current` and keep going until the active window is closed or a stop rule fires.
- If the tree is dirty, treat the uncommitted changes as the current milestone and finish or repair that milestone.

## Stop Rule
- Stop only if the active window is closed, a real blocker is recorded, validation cannot be repaired, review cannot be satisfied, or the user redirects the work.
- Do not stop at a milestone boundary only to report progress while another active-window milestone remains.
- Leave `Documentation.md` useful for the next session.

## Commit Rule
- One verified milestone maps to one commit.
- Use this message pattern:
  - `docs(chunk): <milestone-id> <short-summary>`
