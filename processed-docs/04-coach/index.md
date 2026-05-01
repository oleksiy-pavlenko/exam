# Coach Data

This folder stores structured coach data for fresh Codex sessions.

Start here:
- [Start coach session](Start-Coach-Session.md)
- [Coach catalog](catalog.json)
- [BOOK01 CH01 coach manifest](BOOK01/CH01/coach.json)
- [BOOK01 CH02 coach manifest](BOOK01/CH02/coach.json)

Rules:
- Coach manifests should be structured JSON, not free-form lesson prose.
- Chapter coach manifests must include a `page_reference_index` that maps each `source_page_id` to learner-facing printed book pages.
- Coach data should connect concepts, assignment templates, answer expectations, LLM evaluation guides, hint steps, and visual explanation asset IDs back to repo-local source lines and visual assets.
- The chapter catalog path is `processed-docs/04-coach/catalog.json` when coach coverage exists.

Current status:
- `BOOK01/CH01` coach manifest is built and listed in the coach catalog.
- `BOOK01/CH02` coach manifest is built and listed in the coach catalog.
- The current coach layer covers pages `BOOK01-CH01-P001` through `BOOK01-CH01-P004` and the current `BOOK01/CH02` batch.
- Known gap: exercises 18-25 are still outside current source coverage.
- Future chapter windows must include a `CHxx-COACH` milestone after notes and visual assets are reviewed.
