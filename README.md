# Exam Math Knowledgebase

This repo stores a long-running AI workflow for turning scanned math textbook pages into a Finnish exam knowledgebase.
The workflow now keeps visual assets and structured manifests for a future interactive coach app.

Start here:
- `AGENTS.md`
- `processed-docs/index.md`
- `processed-docs/00-control/Plan.md`
- `processed-docs/00-control/Documentation.md`

Validation:

```bash
python3 scripts/validate_kb.py
```

Current handoff:
- `processed-docs/00-control/Plan.md` is the live milestone-state gate.
- `processed-docs/00-control/Documentation.md` is the durable handoff and audit log.
- First scan batch is imported as provisional `BOOK01/CH01`.
- Current visual assets are indexed at `processed-docs/assets/pages/BOOK01/CH01/index.md`.
