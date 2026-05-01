# Exam Math Knowledgebase

This repo stores a long-running AI workflow for turning scanned math textbook pages into a Finnish exam knowledgebase.

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
- First scan batch is imported as provisional `BOOK01/CH01`.
- Next milestone is `CH01-PAGES`.

