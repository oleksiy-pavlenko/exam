# Review

Use this file as the review contract for every milestone.

## Purpose
- Keep long-running chapter extraction reliable.
- Catch bad citations, broken links, formula mistakes, unclear OCR, missing asset coverage, weak coach contracts, and milestone drift before commit.
- Make the last active-window milestone close the window cleanly.

## Review order
1. Finish the scoped milestone edits.
2. Run `python3 scripts/validate_kb.py`.
3. Run any milestone-specific checks from `Plan.md`.
4. Run the self-review checklist below.
5. Run independent read-only review when processed content changed.
6. Fix every `P0` and `P1` finding.
7. Rerun validation.
8. Update `Plan.md` and `Documentation.md`. If this was the last active-window milestone, set both `Current milestone` and `Next milestone` to `Closed`.
9. Commit once.

## Self-review checklist
- Scope stayed inside the current milestone.
- Source image paths resolve.
- Normalized page image paths and visual asset paths resolve.
- Page IDs and line IDs are stable.
- Derived notes cite page IDs and line IDs.
- Visual assets cite page IDs and line IDs.
- Finnish wording is simple and clear.
- Formulas, exponents, decimal commas, units, and exercise numbers match the scan.
- Diagrams and visual exercises have manifest-covered crops or a clear no-crop reason.
- Coach startup prompts, chapter catalogs, and coach data reference source lines and visual asset IDs where relevant.
- Unclear text is marked as `EPÄSELVÄ`.
- `Plan.md` and `Documentation.md` tell the next session what to do.
- If this was the last active-window milestone, `Plan.md` closes the window cleanly.

## Review worker contract
- Review workers are read-only clean-context `GPT-5.5` `xhigh` workers.
- Do not use `fork_context` for review workers.
- They must read repo files directly.
- They must not rely on chat history.
- They return findings first, ordered by severity.
- They focus on correctness, citations, broken links, milestone acceptance, source fidelity, and coach-session runtime clarity.
- For the last active-window milestone, they also check the close-window state in `Plan.md` and `Documentation.md`.
- They ignore style-only nits unless the wording harms learning or correctness.

## Severity rules
- `P0`: stop the run. Examples: fabricated source, wrong milestone state, validation cannot pass.
- `P1`: block the commit. Examples: missing line citations, broken source image link, missing required figure crop, incorrect formula, unmarked unclear OCR.
- `P2`: useful but non-blocking. Record it in `Documentation.md` if it is out of scope.

## Review prompt shape
- Name the milestone ID and title.
- List touched files.
- State the acceptance focus.
- Point to `Plan.md`, `Review.md`, and `Documentation.md`.
- For the last active-window milestone, ask for issues in the close-window state too.
- Ask for only real issues that matter for correctness, citations, links, scope, or milestone acceptance.
