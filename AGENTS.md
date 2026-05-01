# Exam Knowledgebase Agent Guide

This repository stores an AI-friendly math exam knowledgebase built from scanned book pages.

Read these files before doing substantive work:
1. `processed-docs/00-control/Documentation.md`
2. `processed-docs/00-control/Prompt.md`
3. `processed-docs/00-control/Plan.md`
4. `processed-docs/00-control/Implement.md`
5. `processed-docs/00-control/Review.md`
6. `processed-docs/00-control/source-inventory.md`

Control-doc roles:
- `Prompt.md` is the binding run spec.
- `Plan.md` is the only milestone-status controller.
- `Implement.md` is the execution runbook.
- `Review.md` is the review contract.
- `Documentation.md` is the audit log and durable run memory.
- `source-inventory.md` records raw source IDs, scan paths, and provenance.

Repository rules:
- Raw scans live under `unprocessed-docs/books/`.
- Processed page transcripts live under `processed-docs/01-pages/`.
- Derived exam notes live under `processed-docs/02-concepts/`.
- Exercise and solved-pattern notes live under `processed-docs/03-exercises/`.
- Page images, crops, and reviewed visual assets live under `processed-docs/assets/pages/`.
- Processed notes and transcripts must be in Finnish.
- Use stable source IDs and line IDs. Derived notes must cite source page IDs and line IDs.
- Do not use chat memory as durable state. Persist decisions, blockers, and handoffs in `Documentation.md`.
- Do not use outside sources as normative evidence unless the source file is added to `unprocessed-docs/` and recorded in `source-inventory.md`.
- Keep raw scans unchanged once imported. Use generated assets for rotation, cropping, and cleanup.
- Mark unclear text as `EPÄSELVÄ` in page notes instead of guessing.
- Work one verified milestone at a time.
- Finish each verified milestone with validation, review, updated control docs, and one commit.

Before starting a milestone:
- Run `git status --short` and stop if the worktree is dirty.
- Run `python3 scripts/validate_kb.py` and repair structural failures before content work.
- Check `processed-docs/00-control/Plan.md` for the current milestone and next milestone.

Working style:
- Simplicity first.
- No single-use abstractions.
- No speculative edge-case handling.
- If 200 lines can be 50, rewrite it.
- Use simple English in control docs so non-native speakers can understand easily.
- Use Finnish for processed math content.
- Avoid multiple `return` statements inside one function.

