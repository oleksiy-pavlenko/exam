# Start Long Run Prompt

Use this file only in a fresh Codex session for this repo.

This file owns startup checks only. `Prompt.md` is the binding run spec. `Plan.md` is the only milestone-status source of truth. `Implement.md` is the execution runbook. `Review.md` is the review contract. `Documentation.md` is the audit log and durable handoff.

## Verify the workspace first

```bash
git status --short --branch
python3 scripts/validate_kb.py
```

Notes:
- The worktree must be clean before the run starts.
- `Plan.md` is the milestone-state gate. Older milestone text elsewhere does not override it.
- `Documentation.md` is the durable handoff and audit log.
- Milestone workers and review workers must use clean-context `GPT-5.5` `xhigh`.
- Do not use `fork_context` for milestone workers or review workers.
- If `Plan.md` shows `Closed` for both `Current milestone` and `Next milestone`, do not restart this window.
- Future chapter windows use `CHxx-PAGES`, `CHxx-ASSETS`, `CHxx-NOTES`, and `CHxx-COACH`.
- If preflight fails, repair the control stack before milestone work.
- `processed-docs/04-coach/Start-Coach-Session.md` is for learner-facing sessions. Do not use it as the extraction entrypoint.

## First Codex prompt

```text
CONTINUE THIS SESSION UNTIL EVERY MILESTONE IN THE ACTIVE WINDOW IS COMPLETED. DO NOT STOP AT THE END OF A MILESTONE ONLY TO REPORT PROGRESS.

First read `processed-docs/00-control/Plan.md` and `processed-docs/00-control/Documentation.md`.

Treat `processed-docs/00-control/Plan.md` as the milestone-state gate and only milestone-status source of truth. Treat `processed-docs/00-control/Documentation.md` as the audit log and durable handoff.

Act as the root orchestrator only. If `Plan.md` shows `Closed` for both `Current milestone` and `Next milestone`, do not restart the window. Review `Documentation.md` and stop until a later prep milestone reopens work. If one active-window milestone is `Blocked`, review `Documentation.md`, keep the blocker handoff, then read `AGENTS.md`, `processed-docs/00-control/Prompt.md`, `processed-docs/00-control/Implement.md`, `processed-docs/00-control/Review.md`, and `processed-docs/00-control/source-inventory.md` before you continue. If `Plan.md` names a milestone instead, read those same files and start there.

For each milestone, use one fresh clean-context `GPT-5.5` `xhigh` worker, require that worker to reread the mandatory docs, implement only the current milestone, run the exact milestone validation, run self-review, run one clean-context read-only `GPT-5.5` `xhigh` review worker before commit when processed content changed, do not use `fork_context`, fix blocking findings, update `Plan.md` and `Documentation.md`, commit exactly once, and continue until the active window is `Closed`.

Follow `Prompt.md` for source boundaries and `Implement.md` for stop rules.
For future chapter windows, do not skip the asset or coach milestones: fresh Codex coach sessions need structured visual manifests and coach data, not Markdown-only notes.
```

## Required inputs
- `AGENTS.md`
- `processed-docs/00-control/Prompt.md`
- `processed-docs/00-control/Plan.md`
- `processed-docs/00-control/Implement.md`
- `processed-docs/00-control/Review.md`
- `processed-docs/00-control/Documentation.md`
- `processed-docs/00-control/source-inventory.md`
