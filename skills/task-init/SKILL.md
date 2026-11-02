---
name: task-init
description: Initialise a repo for the task toolchain - mark the work folder, the "home" of its Jira XML files and ticket notes. Sets work_dir in project.md, creates the folder and makes sure git ignores it. Use for "/task-init [path]", "set up tasks in this repo", "set the work folder", or when another task skill finds work_dir missing.
---

# task-init

Usage: `/task-init [path]`
- `/task-init PATH` - initialise the repo for the task toolchain: make PATH the work folder.
- `/task-init --here` - make the current directory the work folder.
- `/task-init` (no path) - if `work_dir` is already set, show its health (read-only); if not, propose a default (`work/` at the repo root) and ask before using it.

## First

1. Find the toolchain folder; every `<toolchain>` below means it. Try in order and take the first that contains `Task.md`:
   - `toolchain_dir` in the repo's `project.md` (relative to the repo root, absolute, or `~/...`)
   - the env var `AI_TOOLCHAIN_DIR`
   - the folder this skill was loaded from, with symlinks resolved (`readlink -f`), two levels up (works for a global install)
   If none works, tell the dev and stop.
2. Read `<toolchain>/Task.md`; its rules win over this skill.
3. Repo root: `git rev-parse --show-toplevel`. Not in a git repo: say so and stop.

## Steps

1. **No argument.** Read `work_dir` from `project.md` (at the repo root). If set: report the path, whether it exists, whether git ignores it (`git check-ignore -q`), how many `*.xml` and notes (`*.md` with a `key:` frontmatter) it holds, and the state counts from `python3 <toolchain>/scripts/state.py list {work_dir}`, then stop. If unset: propose `work/` at the repo root (mention `--here` and an explicit path as alternatives) and continue only after the dev agrees.
2. **Resolve the path.** `PATH` (or the cwd for `--here`) becomes a path **relative to the repo root**. A path outside the repo is allowed only if the dev confirms it (then keep it absolute, and skip the ignore step).
3. **Check the folder.**
   - Missing: create it after telling the dev the full path.
   - Exists: list what it holds. If it contains files **tracked** by git (`git ls-files {dir}`), stop and tell the dev: a work folder must stay untracked. Do not `git rm` anything.
4. **Make git ignore it**, unless it is already ignored (`git check-ignore -q {dir}`). Ask the dev which:
   - `.git/info/exclude` (default; local, nothing to commit)
   - `.gitignore` (shared with the team; this makes a change in the working tree)
   Append `{dir}/` to the chosen file. Never edit both.
5. **Write `work_dir` in `project.md`.**
   - Exists: change only the `work_dir:` line; keep the rest and the comment.
   - Missing: ask whether to create it from `<toolchain>/templates/project.md` (same rules as the "First" step of the other task skills: prefill from the repo, ask for the rest, never invent). Write it only after the dev agrees.
6. **Loose files.** If Jira XML files (`*.xml` with an `<rss`) sit elsewhere in the repo, list them and offer to move them in. Move only what the dev names; never overwrite a file with the same name.
7. **Report in a few lines:** the work folder, the ignore rule used, what `project.md` now says, and the next step (`/task-intake KEY` for XML already inside).

## Rules
- One work folder per repo. If `work_dir` is already set to another path, show both and ask before changing it; do not move existing notes unasked.
- Nothing in the work folder is ever committed (Task.md rule 4).
- Do not touch tracked files, do not commit.
