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
| `scripts/install-global.sh` | Links the skills into `~/.claude/skills` (global install) |
| `scripts/state.py` | List, get or set the `state` of notes |
| `skills/task-*` | Claude Code skills for each step: `task-intake`, `task-start`, `task-commit`, `task-manual-test`, `task-status` |

## Install

Two ways. Either way each repo needs its own `project.md` (work folder, branch rules, build commands); the skills offer to create it from `templates/project.md` on first use.

### A. Global (one copy for all your repos)

```bash
git clone git@github.com:KopyTKG/AI-Toolchain.git ~/AI-Toolchain
~/AI-Toolchain/scripts/install-global.sh
```
- `install-global.sh` links every `skills/*` of the toolchain it sits in into `~/.claude/skills/`. Safe to re-run; it never replaces an entry that is not its own link unless `--force`. Options: `--dry-run`, `--uninstall`, `--target DIR`, or pass another toolchain folder as the last argument. Exit code 1 if a name conflict was skipped.
- Always-on rule: add `templates/CLAUDE.snippet.md` to `~/.claude/CLAUDE.md` with `<TOOLCHAIN_DIR>` set to `~/AI-Toolchain`. The snippet applies only in repos that have a `project.md`.
- The skills find the toolchain through `toolchain_dir` in `project.md`, else the env var `AI_TOOLCHAIN_DIR`, else their own symlink location, so nothing else is needed.
- Update: `git -C ~/AI-Toolchain pull`.
- A change reaches every repo at once; there is no per-repo pinning.

### B. Per project (subtree, shared with the team)

```bash
git subtree add --prefix=ai-toolchain git@github.com:KopyTKG/AI-Toolchain.git Live --squash
mkdir -p .claude/skills
for s in ai-toolchain/skills/*; do ln -s "../../$s" ".claude/skills/$(basename "$s")"; done
cp ai-toolchain/templates/project.md project.md     # set toolchain_dir: ai-toolchain
cat ai-toolchain/templates/CLAUDE.snippet.md >> CLAUDE.md   # set <TOOLCHAIN_DIR> to ai-toolchain
```
- Teammates get everything by cloning; each repo pins its own version.
- Update: `git subtree pull --prefix=ai-toolchain git@github.com:KopyTKG/AI-Toolchain.git Live --squash`.
- No symlinks (e.g. Windows): copy `skills/*` into `.claude/skills/` instead.

Skills load in a new session (or check with `/skills`). Copying only `skills/` is not enough: they read `Task.md`, the scripts and the guide from the toolchain folder.

## Using it on a ticket

1. In the repo: fill in `project.md` (`work_dir` stays untracked: `.gitignore` or `.git/info/exclude`).
2. Put the Jira XML into `work_dir`.
3. `/task-intake KEY` (parses the XML, estimates, plans, stops for your approval) → `/task-start KEY` → code → `/task-manual-test KEY` → `/task-commit` (`--rc` for a patch, `--bump` for a release, only if the repo opted in). `/task-status` shows the overview.
4. Without the skills: `python3 <toolchain>/scripts/xml2note.py work/PROJ-123.xml`.

## Flow

XML → note (`NEW`) → estimate (`OPEN`) → plan and overlaps (`PLANNED`) → **dev approves** → fresh main, branch → code (`CODED`) → commit (`COMMITED`) → push on request (`PUSHED`). UI/UX testing is handed to the dev as a manual task in the note.
