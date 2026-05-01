# Exam Math Knowledgebase

This repo stores a long-running AI workflow for turning scanned math textbook pages into a Finnish exam knowledgebase for Codex-driven coaching.
The workflow keeps visual assets and structured coach data so fresh Codex sessions can explain, assign practice, verify answers, and show visual walkthroughs.

Start here:
- `AGENTS.md`
- `processed-docs/00-control/Mode.md`
- `processed-docs/index.md`
- `processed-docs/00-control/Plan.md`
- `processed-docs/00-control/Documentation.md`
- `processed-docs/00-control/Start-Long-Run.md` for extraction work
- `processed-docs/04-coach/Start-Coach-Session.md` for learner-facing coach sessions

Validation:

```bash
python3 scripts/validate_kb.py
```

Current handoff:
- `processed-docs/00-control/Mode.md` is the current-mode source of truth. The default committed mode is `tutor`.
- `processed-docs/00-control/Plan.md` is the live milestone-state gate.
- `processed-docs/00-control/Documentation.md` is the durable handoff and audit log.
- First scan batch is imported as provisional `BOOK01/CH01`.
- Current visual assets are indexed at `processed-docs/assets/pages/BOOK01/CH01/index.md`.
