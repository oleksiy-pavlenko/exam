# Exam Knowledgebase

This folder is the AI-oriented math exam knowledgebase for Codex-driven coaching.

Start here:
- [Mode](00-control/Mode.md)
- [Documentation](00-control/Documentation.md)
- [Plan](00-control/Plan.md)
- [Prompt](00-control/Prompt.md)
- [Implement](00-control/Implement.md)
- [Review](00-control/Review.md)
- [Source inventory](00-control/source-inventory.md)
- [Start long run](00-control/Start-Long-Run.md)
- [Start coach session](04-coach/Start-Coach-Session.md)

Operating contract:
- `Mode.md` is the only current-mode source of truth for fresh sessions.
- If `Mode.md` says `tutor`, start from `04-coach/Start-Coach-Session.md`.
- If `Mode.md` says `extraction`, start from `00-control/Start-Long-Run.md`.
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
- [Coach data](04-coach/index.md)
- [Current visual assets](assets/pages/BOOK01/CH01/index.md)

Conventions:
- Raw scans are source evidence.
- Page transcripts use stable line IDs such as `L001`.
- Derived notes cite source page IDs and line IDs.
- Visual asset manifests cite source page IDs and line IDs.
- Processed math content is written in Finnish.
- `EPÄSELVÄ` marks text or formulas that need a later visual check.
- Fresh coach sessions should use structured coach data first and fall back to cited notes only when coach data is missing.
- Tutor mode may use own knowledge, web search, and generated images when repo coverage is missing or a clearer explanation is needed.
