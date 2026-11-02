---
name: task-status
description: Show where every ticket stands - state, estimate, branch, open manual tests and what is waiting on the dev. Use for "/task-status", "where are we", "what's waiting for me", "overview of tickets".
---

# task-status

## First

1. Find the toolchain folder; every `<toolchain>` below means it. Try in order and take the first that contains `Task.md`:
   - `toolchain_dir` in the repo's `project.md` (relative to the repo root, absolute, or `~/...`)
   - the env var `AI_TOOLCHAIN_DIR`
   - the folder this skill was loaded from, with symlinks resolved (`readlink -f`), two levels up (works for a global install)
   If none works, tell the dev and stop.
2. Read the repo's `project.md`. If it is missing, ask the dev whether to create it from `<toolchain>/templates/project.md`: prefill what the repo shows (main branch, build commands, work folder candidates), ask for the rest, write it only after the dev agrees, then continue. Never invent values.
3. Read `<toolchain>/Task.md`; its rules win over this skill.
4. `work_dir` in `project.md` is the home of the issue XML and notes. If it is missing or the folder does not exist, run `/task-init` first (`task-status`: just report it).

Read-only. Changes nothing. If `project.md` is missing, say so and stop; do not create it here (use another task skill for that).

## Steps
1. `python3 <toolchain>/scripts/state.py list {work_dir}` for key, state, estimate and title.
2. For notes in `CODED`, `COMMITED` or `PUSHED`, check git: does the branch exist (`git branch --list '{KEY}*'`), is it pushed (`git branch -r --list 'origin/{KEY}*'`), commits ahead of main (`git log --oneline {main_branch}..{branch}`). If git disagrees with `state`, report the mismatch; do not fix it unasked.
3. For each note, count unchecked acceptance criteria (`- [ ]`) and whether `## Manuální test` exists.
4. Reply with a short table and a "waiting on you" list:
   - `PLANNED`: plan awaits approval, plus its open questions
   - `COMMITED`: manual tests to run, then push on request
   - decisions marked open in a plan
5. Total the estimate (MD) of tickets not yet `PUSHED`.

## Releases
Only if `project.md` has a "Releases" section (the repo opted in), also report: the latest tag, commits since it, and whether `{release_notes_dir}` has a notes file for the current `version` / `rc` from `package.json`. Missing notes before a tag are a "waiting on you" item.

## Rules
- Do not call `state.py set`, `git fetch` or anything with side effects.
