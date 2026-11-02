# Task skill

## Rules

1. Before any code, explain to the dev what you will be doing.
2. Before coding, write a time estimate for human work in MD (man day; 8 h of work = 1 MD). Use a single range per item (e.g. 1.0–1.5 MD) that includes implementation, tests and manual verification, but not review. Break it down in a table by part.
3. Tasks come in RSS XML format (Jira export) in the work folder defined in the project's `project.md` (`work_dir`).
4. The work folder stays untracked in the project repo: never commit anything from it.
5. The task file is `Task.md` (this exact casing).

## Interaction

Steps run in this order. After step 3 stop and wait for the dev's approval before any code or branch is created.

1. Parse each XML to an Obsidian md file `{ITEM-KEY}.md` next to the XML (`scripts/xml2note.py`, layout in `templates/ticket-note.md`).
   - Language: same as the ticket (Czech).
   - Frontmatter: `key`, `title`, `type`, `status`, `priority`, `assignee`, `reporter`, `parent`, `related`, `created`, `estimate_md`, `url`, `tags`.
   - Linked issues are written as `[[ITEM-KEY]]` wikilinks.
   - Body: scope, acceptance criteria, estimate table, notes.
2. Calculate the estimate for a human (see Rule 2) and put it into the note.
3. Create a plan for each item as a `## Plan` section in its note (files to touch, steps, tests). With more than one item, add an overlap table: which files and features each item touches. Items interact if they touch the same file or the same feature; the dev has the final say.
4. After approval: `git fetch` and pull a fresh master (fast-forward only). If the working tree has tracked changes, stop and ask. Do this before creating each branch.

## State tracking

Each note has a `state` property in the frontmatter (separate from `status`, which is the Jira status). Allowed values, in order:

- `NEW` – note created from the XML, no estimate or plan yet.
- `OPEN` – parsed and estimated, plan not finished.
- `PLANNED` – plan and overlap table written, waiting for the dev's approval.
- `CODED` – implemented in the working tree, not committed.
- `COMMITED` – committed on its branch, not pushed.
- `PUSHED` – branch pushed to the remote.

Update `state` in the note as soon as the step is done, and mention the new state in the report.

## Branching

- Each item goes into a separate branch based on fresh master: `{ITEM-KEY}-{short-czech-slug}` (e.g. `SLOUP-610-esc-zavreni-okna-s-grafem`).
- If items interact with each other, make them into one joined branch marked `{project}-{item1}_{itemX}` (e.g. `SLOUP-991_992`).
- Commit message prefix is the Jira key from the branch name (see the project's `project.md`), in Czech. For a joined branch, use the key of the item the commit belongs to.

## Manual UI/UX testing

If an item needs UI/UX testing, do not claim it as verified. Hand it to the dev as a manual task:

- Give the route, the component (file path) and where to find it in the app (menu path and the click path to reach it).
- Give concrete steps and the expected result for each, plus the browser to use (Chrome/Edge for production).
- Prompt the dev to run it, and list it in the final report as "to be tested manually by the dev".
- Also add it to the item's note under `## Manuální test`.

## Releases

Release handling is **opt-in**. Not every repo versions, bumps or tags; a plain commit never changes a version, writes release notes or creates a tag.

- The repo opts in by having a "Releases" section in `project.md`.
- The step runs only on request: `/task-commit --rc` (a patch = the next release candidate) or `/task-commit --bump` (a release), or when the dev asks for a patch, an RC or a release in words.
- Then follow `guides/release-notes.md`. Two kinds of notes: a **patch** is one RC (`X.Y.Z-rc.N`; its notes say what changed in that RC, for the devkits) and a **release** (`X.Y.Z-release`) groups the patches since the last release. Templates: `templates/release-notes-rc.md`, `-release.md`.
- Order: write the notes, commit them together with the version bump, then tag. Never tag without notes in the tagged commit.
- Check the store text with `scripts/notes_check.py`; cs-CZ and en-US carry the same bullets.
- Tagging and pushing a tag are separate, explicit requests from the dev, after the guide's checklist passes.
- A release is not a ticket state: the tickets in it keep the normal `state` lifecycle.

## Done

- Done means: implemented, verified (build / type check / tests where they exist) and committed on its branch.
- Do not push and do not open a PR unless the dev asks.
- Report what was verified and what was not. Manual UI/UX checks are listed as open tasks for the dev (see above).
