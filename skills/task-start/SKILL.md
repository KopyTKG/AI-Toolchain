---
name: task-start
description: After the dev approved the plan, update the main branch and create the ticket's branch (single or joined). Use for "/task-start KEY", "approved, go", "create the branch for KEY". Refuses to run without an approved plan or with a dirty working tree.
---

# task-start

## First

1. Find the toolchain folder; every `<toolchain>` below means it. Try in order and take the first that contains `Task.md`:
   - `toolchain_dir` in the repo's `project.md` (relative to the repo root, absolute, or `~/...`)
   - the env var `AI_TOOLCHAIN_DIR`
   - the folder this skill was loaded from, with symlinks resolved (`readlink -f`), two levels up (works for a global install)
   If none works, tell the dev and stop.
2. Read the repo's `project.md`. If it is missing, ask the dev whether to create it from `<toolchain>/templates/project.md`: prefill what the repo shows (main branch, build commands, work folder candidates), ask for the rest, write it only after the dev agrees, then continue. Never invent values.
3. Read `<toolchain>/Task.md`; its rules win over this skill.

Follow `Task.md` ("Interaction" step 4 and "Branching").

## Preconditions (stop and ask if any fails)
- The note exists and `state` is `PLANNED`: `python3 <toolchain>/scripts/state.py get {KEY} {work_dir}`.
- The dev has approved the plan in this conversation. Silence is not approval.
- `git status --short` shows no changes to tracked files. Untracked files, including the work folder, are fine and stay untouched.

## Steps
1. Use `main_branch` and the branch patterns from `project.md`.
2. Branch name:
   - single item: `{KEY}-{short-czech-slug}` (ascii slug, lowercase, hyphens)
   - items the dev approved as interacting: `{PROJECT}-{KEY1}_{KEY2}`
3. Update main, fast-forward only:
   `git fetch origin && git checkout {main_branch} && git pull --ff-only origin {main_branch}`
   If the fast-forward fails, report it and stop; do not merge or reset.
4. `git checkout -b {branch}`. If the branch already exists, ask before reusing it.
5. Say what changed on main (commit count) and the new branch name in two lines. State stays `PLANNED` until the implementation is done.
6. Start implementing the plan. Before the first edit, tell the dev in a short message what you are about to change.
7. When the implementation is finished and verified as far as `project.md` commands allow, set `CODED`: `python3 <toolchain>/scripts/state.py set {KEY} CODED {work_dir}`. Then suggest `/task-manual-test` and `/task-commit`; do not commit unasked.

## Rules
- Never `git push`, `reset --hard`, `clean` or `checkout .` here.
- Do not carry unrelated work over: the branch starts at main.
