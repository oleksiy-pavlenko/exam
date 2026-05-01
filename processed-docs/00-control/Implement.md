# Implement

Use this file as the execution runbook. `Prompt.md` is the binding run spec. `Plan.md` is the only milestone-status source of truth. `Documentation.md` is the audit log and durable run memory.

## Objective
- Process scanned math book chapters into a reliable Finnish exam knowledgebase.
- Keep the run resumable across Codex sessions.
- Complete one verified milestone at a time.

## Non-Negotiable Rules
- Start from `Plan.md`.
- Do not start a milestone while the worktree is dirty.
- Run `python3 scripts/validate_kb.py` before content work and after edits.
- One verified milestone equals one commit.
- Keep raw scans unchanged after import.
- Use Finnish for processed page, concept, and exercise content.
- Cite derived notes with page IDs and line IDs.
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
- The root thread owns milestone selection and final integration.
- For long extraction work, use one fresh clean-context `GPT-5.5` `xhigh` worker per milestone or page range when the work can run independently.
- Review workers must be read-only clean-context `GPT-5.5` `xhigh` workers.
- Do not use `fork_context` for any milestone worker or review worker.
- Review workers must read repo state directly from files, not from chat memory.
- Give reviewers the milestone ID, touched files, acceptance target, and control-doc paths.

## Hard Stop Gate
- Do not send a final handoff while `Plan.md` shows a milestone in progress and the current turn can finish it.
- Stop only for a real blocker, validation failure that cannot be repaired, or a user redirect.
- If `Plan.md` says `Closed`, do not restart old milestones unless a later prep milestone reopens work.

## Root Orchestrator Loop
1. Read `Plan.md` and `Documentation.md`.
2. Run `git status --short`.
3. Run `python3 scripts/validate_kb.py`.
4. Select the milestone marked `Current`.
5. Keep edits inside the milestone scope.
6. Run validation and milestone-specific checks.
7. Run self-review from `Review.md`.
8. Run independent review when processed content changed.
9. Fix blocking findings.
10. Update `Documentation.md` and `Plan.md`.
11. Commit once with the milestone message from `Plan.md`.

## Milestone Worker Contract
1. Reread the mandatory inputs.
2. Inspect the relevant scans or page notes directly.
3. Create only the files needed for the assigned milestone.
4. Use stable source IDs and line IDs.
5. Keep page notes close to the source; keep study notes concise.
6. Run validation.
7. Report touched files, unresolved uncertainties, and validation results.

## Milestone Completion Checklist
- Scope stayed inside the current milestone.
- Required files and links exist.
- Source image, page ID, and line ID citations are present.
- Finnish wording is clear.
- Formulas, units, decimal commas, and exercise numbers were checked.
- `Documentation.md` records the result and handoff.
- `Plan.md` shows the next correct milestone state.
- Validation passed.
- Exactly one commit was created.

## Validation Rules
- Always run `python3 scripts/validate_kb.py`.
- Run `git status --short` before starting and after commit.
- For page milestones, run the page-specific `rg` command from `Plan.md`.
- Before closing a notes milestone, run `rg -n "EPÄSELVÄ|TODO|BLOCKED" processed-docs/01-pages processed-docs/02-concepts processed-docs/03-exercises` and decide whether each hit is acceptable or blocking.

## Review Gate Rule
- Self-review is mandatory for every milestone.
- Independent review is mandatory when page transcripts, concept notes, exercise notes, or figure assets changed.
- Treat `P0` and `P1` findings as blocking.
- Fix blocking findings inside the same milestone.
- Record non-blocking follow-up in `Documentation.md`.

## Resume Rule
- After an interruption, read `Plan.md`, `Documentation.md`, and `Implement.md`.
- Inspect `git status --short --branch` and `git log -1 --oneline`.
- If the tree is clean, continue from the milestone marked `Current`.
- If the tree is dirty, treat the uncommitted changes as the current milestone and finish or repair that milestone.

## Stop Rule
- Stop only if the current milestone is complete, a real blocker is recorded, validation cannot be repaired, review cannot be satisfied, or the user redirects the work.
- Leave `Documentation.md` useful for the next session.

## Commit Rule
- One verified milestone maps to one commit.
- Use this message pattern:
  - `docs(chunk): <milestone-id> <short-summary>`
