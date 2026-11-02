---
name: task-commit
description: Commit the finished ticket work on its branch with a Czech message prefixed by the Jira key from the branch name, excluding the work folder, and mark the note COMMITED. Use for "/task-commit", "commit it", "commit the ticket". Flags --rc (a patch = next RC) and --bump (a release grouping the patches) also bump the version and write release notes; off by default.
---

# task-commit

## First

1. Find the toolchain folder; every `<toolchain>` below means it. Try in order and take the first that contains `Task.md`:
   - `toolchain_dir` in the repo's `project.md` (relative to the repo root, absolute, or `~/...`)
   - the env var `AI_TOOLCHAIN_DIR`
   - the folder this skill was loaded from, with symlinks resolved (`readlink -f`), two levels up (works for a global install)
   If none works, tell the dev and stop.
2. Read the repo's `project.md`. If it is missing, ask the dev whether to create it from `<toolchain>/templates/project.md`: prefill what the repo shows (main branch, build commands, work folder candidates), ask for the rest, write it only after the dev agrees, then continue. Never invent values.
3. Read `<toolchain>/Task.md`; its rules win over this skill.
4. `work_dir` in `project.md` is the home of the issue XML and notes. If it is missing or the folder does not exist, run `/task-init` first (`task-status`: just report it).

Follow `Task.md` ("Branching", "Done"). Never pushes.

## Steps
1. `git branch --show-current` and `git status --short`. The branch must not be the main branch.
2. Key: the Jira key from the branch name (`SLOUP-610-esc-...` -> `SLOUP-610`). Joined branch `SLOUP-608_610`: use the key of the item the changes belong to; if the changes mix items, make one commit per item.
3. Verify before committing, using the commands in `project.md` (build, type check, tests). Report failures as they are; do not commit over a failing build the dev did not accept. If a check is pre-existing and listed in "Known baseline problems", say so.
4. Stage only the task's files by explicit path. Never `git add -A`/`.`, never the work folder (`work_dir`), never secrets or `appsettings` changes the task did not need.
5. Message, in Czech, plain prose (no terse style, it is persisted text):
   - subject: `{KEY} {what changed, imperative or noun phrase}` per `commit_prefix` in `project.md`
   - body: why, and anything a reviewer must know. Follow the attribution lines the session gives, if any.
6. Commit, then show `git log --oneline -1`.
7. Set the note state: `python3 <toolchain>/scripts/state.py set {KEY} COMMITED {work_dir}`.
8. Report: commit hash, what was verified, what was not, and the manual tests still open for the dev (point to `## Manuální test`). Offer to push; do not push.

## Flags: `--rc` and `--bump` (opt-in release step)
Usage:
- `/task-commit` - plain commit.
- `/task-commit --rc` - a **patch**: the next release candidate of the current version. Patch and RC are the same thing here.
- `/task-commit --bump` - a **release**: groups the patches (RCs) since the last release.

Without a flag, this skill never changes `version`, `rc` or `buildNumber`, never writes release notes and never creates a tag, whatever the project is. Many repos do not release per commit; that is the default. Both flags need a "Releases" section in `project.md`; without it say so and stop. If both flags are given, stop and ask which one is meant.

**`--rc` (patch)**
1. Read the current `version` and `rc` (e.g. `2.6.2`, `rc.5`). Next RC is `rc.6`; if there is no `rc` field yet, `rc.1` of the version the dev names (ask if it is not obvious).
2. Set the `rc` field, leave `buildNumber` alone (RCs share the version's build number, as in the project rules).
3. Write the patch notes (`templates/release-notes-rc.md`) from `git log <previous-tag>..HEAD`: only what changed in this RC, for the devkits to retest. File `<version>-rc<N>.md`.

**`--bump` (release)**
1. Bump `version` (as the dev says) and `buildNumber` per the project rules; delete the `rc` field.
2. Write the release notes from `templates/release-notes-release.md` by grouping all patch notes (`<version>-rc*.md`) since the last release into one user-facing list: merge duplicates, drop what users cannot see.

**Both**
- Follow `<toolchain>/guides/release-notes.md`; run `notes_check.py` until it passes.
- Show the plan first (new version, `rc`, build number, notes file, which commit) and wait for OK before editing.
- Notes and bump go into the same commit as the task changes, or into their own commit if the dev prefers.
- Tag only when the dev explicitly asks for it as a separate step. The flags do not tag or push.

## Rules
- Do not amend or rewrite existing commits unless the dev asks.
- Do not push, do not open a PR.
