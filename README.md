# AI-Toolchain

Template for handling Jira tickets with Claude Code: parse the XML export, estimate, plan, branch, code, commit, and keep track of progress in Obsidian notes. It is pulled into each repo that uses it (subtree, submodule or plain copy), so it contains no project-specific facts.

## Contents

| Path | Purpose |
|------|---------|
| `Task.md` | The workflow rules Claude must follow (read this first) |
| `templates/ticket-note.md` | Obsidian note skeleton for one ticket |
| `templates/project.md` | Fill-in sheet with the facts about the consuming repo |
| `templates/CLAUDE.snippet.md` | Lines to add to the consuming repo's `CLAUDE.md` |
| `scripts/xml2note.py` | Jira RSS XML to a note with `state: NEW` |
| `guides/release-notes.md` | Guide for patch notes (= RC, for the devkits) and release notes (group the patches; store "What's new" text) |
| `templates/release-notes-*.md` | Skeletons for patch (RC) notes and release notes |
| `scripts/notes_check.py` | Checks and fixes the character counts of store-text blocks |
| `scripts/state.py` | List, get or set the `state` of notes |
| `skills/task-*` | Claude Code skills for each step: `task-intake`, `task-start`, `task-commit`, `task-manual-test`, `task-status` |

## Using it in a project repo

1. Pull this repo into the project (e.g. `git subtree add --prefix=ai-toolchain <url> Live --squash`).
2. Copy `templates/project.md` to the project root and fill it in.
3. Add `templates/CLAUDE.snippet.md` to the project's `CLAUDE.md` (set `<TOOLCHAIN_DIR>`).
4. Make the skills available: copy or symlink `skills/*` into the project's `.claude/skills/`.
5. Put the Jira XML into the project's `work_dir` (kept untracked).
6. Convert (or run `/task-intake KEY`): `python3 ai-toolchain/scripts/xml2note.py work/PROJ-123.xml`
7. Work the ticket: `/task-intake` → approve → `/task-start` → code → `/task-manual-test` → `/task-commit`; `/task-status` shows the overview.

## Flow

XML → note (`NEW`) → estimate (`OPEN`) → plan and overlaps (`PLANNED`) → **dev approves** → fresh main, branch → code (`CODED`) → commit (`COMMITED`) → push on request (`PUSHED`). UI/UX testing is handed to the dev as a manual task in the note.
