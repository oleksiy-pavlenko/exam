# Prompt

Use this file as the binding run spec. `Plan.md` owns milestone status. `Implement.md` owns execution procedure. `Documentation.md` is the audit log and durable run memory.

## Mission
- Build a Finnish math exam knowledgebase from scanned textbook pages.
- Keep raw scans, page transcripts, derived concept notes, exercise patterns, visual assets, and structured coach data in stable repo paths.
- Prepare the material for Codex-driven coach sessions that can explain, assign practice, verify answers, and show dynamic visual explanations.
- Process the current first scan batch as `BOOK01` chapter `CH01`.
- Keep the repo ready for long-running chapter-by-chapter AI processing and fresh coach sessions.

## Non-goals
- Do not solve or summarize chapters that are not yet imported.
- Do not use external math websites, answer keys, or search results as normative evidence unless the file is added to `unprocessed-docs/`.
- Do not guess unclear OCR or formulas. Mark them as `EPÄSELVÄ`.
- Do not rewrite raw scans after import. Put rotated or cropped derivatives under `processed-docs/assets/pages/`.
- Do not design for a separate standalone app in this repo.

## Autonomous window
- Active window: `CH01-COACH` backfill (closed)
- Future chapter windows use `CHxx-PAGES`, `CHxx-ASSETS`, `CHxx-NOTES`, and `CHxx-COACH`.
- Current milestone is controlled only by `Plan.md`.
- Continue until every milestone in the active window is completed or a stop rule fires.
- If `Plan.md` shows `Closed`, do not restart this window unless a later prep milestone opens a new one.

## Hard constraints
- Confirm a clean worktree with `git status --short` before starting a milestone.
- Run `python3 scripts/validate_kb.py` before starting a milestone and after milestone edits.
- One verified milestone equals one commit.
- Do not stop at a milestone boundary only to report progress while another active-window milestone remains.
- Use Finnish for page transcripts, concept notes, and exercise notes.
- Cite every derived concept or method with a page ID and line ID.
- Cite every visual asset with a page ID and line ID.
- Keep source evidence inside the repo.

## Source and scope boundaries
- The first source is provisional `BOOK01` until the book title page, ISBN, or cover is uploaded.
- The first chapter is provisional `CH01` until chapter metadata is confirmed.
- Current raw scan paths are recorded in `source-inventory.md`.
- Later uploaded chapters must get their own chapter directory and four-milestone window.

## Run deliverables
- Page transcript files under `processed-docs/01-pages/BOOK01/CH01/`.
- Reviewed normalized page images, figure crops, and asset manifests under `processed-docs/assets/pages/BOOK01/CH01/`.
- Derived study notes under `processed-docs/02-concepts/`.
- Exercise and solved-pattern notes under `processed-docs/03-exercises/`.
- Coach startup prompts, chapter catalogs, and coach manifests under `processed-docs/04-coach/` when the `CHxx-COACH` milestone runs.
- Updated source inventory, indexes, plan state, and audit log.
- A passed validation command and one clean commit per milestone.

## Done when this run stops
- `Plan.md` shows `Closed` for both `Current milestone` and `Next milestone`, or `Documentation.md` records a real blocker that stops the active window.
- `Documentation.md` tells the next session what changed, what is next, what remains unclear, and whether the active window is closed.
- `python3 scripts/validate_kb.py` passes.
- `git status --short` is empty after the milestone commit.

## Writing rules
- Processed math content must be in Finnish.
- Use simple Finnish and short explanations.
- Preserve math symbols, decimal commas, exercise numbers, and page-visible labels.
- Prefer concise study notes over broad but vague summaries.
- Do not invent notation that is not useful for exam preparation.

## Citation rules
- Page transcript files must name their source image and page ID.
- Derived notes must cite page IDs and line IDs, for example `BOOK01-CH01-P002:L014-L018`.
- If a source line is unclear, cite it and mark the uncertainty.
- Do not cite chat messages as evidence.

## Diagram rules
- Treat diagrams and figures as first-class learning artifacts.
- Keep raw scans as evidence.
- Put every normalized page image, crop, or figure crop under `processed-docs/assets/pages/`.
- Every page transcript must link to an existing normalized page image.
- Every important figure needs a manifest-covered crop unless the page note gives a short no-crop reason.
- Every visual exercise needs a crop that can be used later for assignment and answer verification.

## Coach data rules
- Fresh Codex coach sessions should read structured manifests, not scrape free-form Markdown as their main data source.
- Chapter visual asset manifests live at `processed-docs/assets/pages/BOOKxx/CHxx/assets.json`.
- Each visual asset entry must include a stable asset ID, source page ID, source line IDs, image path, short Finnish description, related concepts or exercises, and intended uses.
- Coach data belongs in `processed-docs/04-coach/` and must cite source line IDs plus visual asset IDs where relevant.
- Fresh learner-facing sessions should start from `processed-docs/04-coach/Start-Coach-Session.md`.
