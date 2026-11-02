# project.md – facts the toolchain needs about THIS repo

Copy this file to the project repo root (or next to its CLAUDE.md) and fill it in. `Task.md` refers to it.

```yaml
toolchain_dir: ai-toolchain     # folder of this toolchain inside the repo; skills use it to find Task.md and scripts
project: SLOUP                 # Jira project key
work_dir: source/work          # where the Jira XML and the notes live (stays untracked)
main_branch: master
branch_pattern: "{KEY}-{czech-slug}"
joined_branch_pattern: "{PROJECT}-{KEY1}_{KEY2}"
commit_language: Czech
commit_prefix: "{KEY}"         # Jira key from the branch name
fetch_before_branch: true      # fast-forward only
```

## Releases (OPTIONAL - delete this whole section if the repo does not bump versions or tag)
```yaml
release_notes_dir: docs/release-notes
tag_patterns: "X.Y.Z-rc.N (patch), X.Y.Z-release (release)"
store_languages: [cs-CZ, en-US]   # first one is primary
store_char_limit: 500
changelog: CHANGELOG.md           # or none
```

## Build / test / run
<!-- commands the toolchain may run to verify work, e.g. dotnet build, dotnet test, yarn build -->

## Where things are
<!-- route table file, menu structure, generated code that must not be hand-edited, DI composition root, ... -->

## Known baseline problems
<!-- errors that exist on the main branch (e.g. pre-existing tsc errors), so they are not blamed on a task -->

## Manual test conventions
<!-- browsers used in production, test accounts, how to reach a feature in the UI -->

## Do not
<!-- secrets in config, files that stay untracked, areas needing approval -->
