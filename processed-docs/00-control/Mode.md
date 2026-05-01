# Mode

This file is the only current-mode source of truth for fresh Codex sessions in this repo.

## Current mode
- Current mode: `extraction`

## Startup rules
- Every fresh session reads this file first.
- Fresh sessions use the last committed mode. Chat memory does not override this file.
- If the current mode is `tutor`, continue with `processed-docs/04-coach/Start-Coach-Session.md`.
- If the current mode is `extraction`, continue with `processed-docs/00-control/Start-Long-Run.md`.

## Switching rules
- If the user request belongs to the other mode, ask before switching.
- A confirmed switch updates this file and creates a dedicated commit such as `docs(mode): switch-to-tutor` or `docs(mode): switch-to-extraction`.
- If the worktree is dirty, do not switch persistently until the current work is finished, repaired, or redirected by the user.
- Ordinary mode switches do not reopen `Plan.md` milestones by themselves.
