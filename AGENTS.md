# Exam Knowledgebase Agent Guide

This repository stores an AI-friendly math exam knowledgebase built from scanned book pages.

This repo has two persisted modes: `tutor` and `extraction`.

Read these files before doing substantive work:
1. `processed-docs/00-control/Mode.md`
2. If the current mode is `extraction`, read:
   - `processed-docs/00-control/Documentation.md`
   - `processed-docs/00-control/Prompt.md`
   - `processed-docs/00-control/Plan.md`
   - `processed-docs/00-control/Implement.md`
   - `processed-docs/00-control/Review.md`
   - `processed-docs/00-control/source-inventory.md`
3. If the current mode is `tutor`, read:
   - `processed-docs/04-coach/Start-Coach-Session.md`
   - `processed-docs/04-coach/catalog.json` when it exists
   - relevant coach manifests, visual assets, concept notes, and exercise notes for the requested chapter or topic

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
- Codex coach data lives under `processed-docs/04-coach/`.
- Every processed chapter must have a reviewed visual asset manifest at `processed-docs/assets/pages/BOOKxx/CHxx/assets.json`.
- Fresh sessions must read `processed-docs/00-control/Mode.md` first.
- Fresh tutoring sessions should start from `processed-docs/04-coach/Start-Coach-Session.md` when the current mode is `tutor`.
- Fresh extraction sessions should start from `processed-docs/00-control/Start-Long-Run.md` when the current mode is `extraction`.
- Processed notes and transcripts must be in Finnish.
- Use stable source IDs and line IDs. Derived notes must cite source page IDs and line IDs.
- Visual assets must cite source page IDs and line IDs.
- Do not use chat memory as durable state. Persist decisions, blockers, and handoffs in `Documentation.md`.
- Keep raw scans unchanged once imported. Use generated assets for rotation, cropping, and cleanup.
- Mark unclear text as `EPÄSELVÄ` in page notes instead of guessing.
- Work one verified milestone at a time.
- Finish each verified milestone with validation, self-review, updated control docs, and one commit.
- Future chapter windows use four milestones by default: `CHxx-PAGES`, `CHxx-ASSETS`, `CHxx-NOTES`, and `CHxx-COACH`.

Before starting a milestone:
- Run `git status --short` and stop if the worktree is dirty.
- Run `python3 scripts/validate_kb.py` and repair structural failures before content work.
- Check `processed-docs/00-control/Plan.md` for the current milestone and next milestone.
- If subagents are used, every milestone worker and optional review worker must use clean-context `GPT-5.5` `xhigh`. Do not use `fork_context`.
- Review subagents are optional. Use one only when the user asks, validation or self-review is uncertain, or the milestone is high risk.

## Tutor mode
- Tutor mode is learner-facing and read-only by default.
- The user does not need to repeat a tutor prompt. Requests like “I want to prepare to exam using chapter 1-2” are enough to start coaching.
- When the user asks to visualize a chapter or topic, create a small disposable HTML app in `tmp/` by default, unless they ask for a static explanation or a durable artifact from the start.
- When possible, add simple dynamic behavior that helps the explanation, for example sliders, toggles, step buttons, or live labels.
- After a visualization is ready in `tmp/`, ask once whether it should be persisted in the repo.
- If the next reply is a clear yes in English or Finnish, move the full visualization bundle to `processed-docs/04-coach/visualizations/<chapter-id-or-general>/<YYYYMMDD>-<topic-slug>/` and create one git commit without asking more questions.
- Treat direct answers such as `yes`, `save it`, `persist it`, `ok save`, `kyllä`, `joo`, `tallenna`, `tallenna se`, and `persistoi` as confirmation when they answer that persistence question.
- If the next reply is a clear no such as `no` or `ei`, leave the visualization in `tmp/` and make no repo changes.
- Use repo material first, but do not treat extracted content as a hard limit.
- Own knowledge is allowed when it helps the explanation.
- Web search is allowed when it is useful.
- New images may be generated when they help the explanation.
- If the difference matters, make it clear what is repo-backed and what is general or web-backed guidance.
- If a requested chapter is missing or only partly extracted, use available repo material first and then continue with general guidance instead of stopping.
- When the user asks for exercises, keep them unsolved by default. Give the exercise first, then hints, checks, or step-by-step help. Give the full solution only when the user asks for it or clearly wants it.
- Cite source refs and asset IDs when they matter for explanations, feedback, or visual walkthroughs.
- A confirmed visualization save is explicit permission for that repo change and commit in tutor mode.
- Do not edit repo files in tutor mode unless the user explicitly asks to switch to extraction mode, asks for repo changes, or confirms saving the current visualization.

## Extraction mode
- Extraction mode is the only mode for repo content work, milestone work, validation, review, and commits that change extracted content or control docs.
- Use `processed-docs/00-control/Start-Long-Run.md` as the extraction entrypoint.
- Do not use outside sources as normative evidence unless the source file is added to `unprocessed-docs/` and recorded in `source-inventory.md`.

## Mode switching
- If the user request belongs to the other mode, ask before switching.
- A confirmed switch must update `processed-docs/00-control/Mode.md` and be persisted in a dedicated commit.
- If the worktree is dirty, do not switch persistently until the current work is finished, repaired, or redirected by the user.

Working style:
- Simplicity first.
- No single-use abstractions.
- No speculative edge-case handling.
- If 200 lines can be 50, rewrite it.
- Use simple English in control docs so non-native speakers can understand easily.
- Use Finnish for processed math content.
- Avoid multiple `return` statements inside one function.
