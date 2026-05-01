# Start Long Run

Use this prompt when starting a fresh Codex session for this repo.

## Verify the workspace first
- Run `git status --short`.
- Run `python3 scripts/validate_kb.py`.
- Read `processed-docs/00-control/Plan.md`.
- Read `processed-docs/00-control/Documentation.md`.
- If subagents are used, use clean-context `GPT-5.5` `xhigh` for every milestone worker and review worker. Do not use `fork_context`.

## First Codex prompt
CONTINUE THIS SESSION UNTIL THE CURRENT MILESTONE IN `processed-docs/00-control/Plan.md` IS COMPLETED. DO NOT RELY ON CHAT MEMORY. READ THE CONTROL DOCS, PROCESS ONLY THE CURRENT MILESTONE, RUN VALIDATION, UPDATE THE CONTROL DOCS, AND COMMIT ONCE WHEN THE MILESTONE IS VERIFIED.

## Required inputs
- `AGENTS.md`
- `processed-docs/00-control/Prompt.md`
- `processed-docs/00-control/Plan.md`
- `processed-docs/00-control/Implement.md`
- `processed-docs/00-control/Review.md`
- `processed-docs/00-control/Documentation.md`
- `processed-docs/00-control/source-inventory.md`
