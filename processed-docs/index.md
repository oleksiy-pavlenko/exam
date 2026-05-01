# Exam Knowledgebase

This folder is the AI-oriented math exam knowledgebase.

Start here:
- [Documentation](00-control/Documentation.md)
- [Plan](00-control/Plan.md)
- [Prompt](00-control/Prompt.md)
- [Implement](00-control/Implement.md)
- [Review](00-control/Review.md)
- [Source inventory](00-control/source-inventory.md)

Operating contract:
- `Plan.md` is the only milestone-status source of truth.
- `Prompt.md` is the binding run spec after `Plan.md` names an active milestone.
- `Implement.md` is the long-run procedure.
- `Review.md` defines self-review and independent review gates.
- `Documentation.md` is the durable run memory.
- Validation command: `python3 scripts/validate_kb.py`
- Worktree gate: `git status --short` must be empty before a milestone starts and after its commit.
- One verified milestone means scoped content updates, citations checked, links checked, self-review complete, independent review complete with no open `P0` or `P1`, `Plan.md` and `Documentation.md` updated, and one commit.

Current content:
- [Page transcripts](01-pages/index.md)
- [Concept notes](02-concepts/index.md)
- [Exercise notes](03-exercises/index.md)

Conventions:
- Raw scans are source evidence.
- Page transcripts use stable line IDs such as `L001`.
- Derived notes cite source page IDs and line IDs.
- Processed math content is written in Finnish.
- `EPÄSELVÄ` marks text or formulas that need a later visual check.

