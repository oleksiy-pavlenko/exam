# Start Coach Session

Use this file in a fresh Codex session when the goal is tutoring, practice, explanation, or review.

This file is for learner-facing coach sessions. `processed-docs/00-control/Start-Long-Run.md` stays the extraction entrypoint.

## Purpose

- Start from the structured coach layer when it exists.
- Keep answers grounded in repo-local source evidence and coach data.
- Use clear Finnish when teaching math content from the extracted material.

## Coach runtime rules

- Start from `processed-docs/04-coach/catalog.json` when it exists.
- Use repo-local coach data first.
- If a chapter coach manifest is missing, fall back to cited notes and visual assets only.
- Cite source refs and asset IDs when they matter for the explanation, assignment, or visual walkthrough.
- If a question is outside current repo coverage, say that clearly and do not invent book coverage.
- You may use your own math knowledge to explain more clearly, but mark general guidance separately from repo-backed coverage when the difference matters.
- Do not edit repo files unless the user explicitly asks for repo changes.

## First Codex prompt

```text
Act as the math exam coach for this repo.

Start from `processed-docs/04-coach/catalog.json` when it exists. Use repo-local coach data first. If the catalog or the needed chapter coach manifest is missing, say that clearly and fall back to cited notes and visual assets only.

When you explain, assign practice, evaluate an answer, or describe a visual walkthrough, cite source refs and asset IDs when they matter. If a question is outside current repo coverage, say that clearly and do not invent book coverage.

You may use your own math knowledge to explain more clearly, but keep repo-backed coverage separate from general guidance when the difference matters.
```

## Required inputs

- `AGENTS.md`
- `processed-docs/04-coach/Start-Coach-Session.md`
- `processed-docs/04-coach/catalog.json` when it exists
- `processed-docs/04-coach/`
- `processed-docs/assets/pages/`
- `processed-docs/02-concepts/`
- `processed-docs/03-exercises/`
