# CLAUDE.md

This repo is a **template** that is pulled into other repos. It holds the task workflow, not any project's code.

- Keep everything here project-agnostic. Project facts (Jira key, folders, build commands, routes) belong in the consuming repo's `project.md` (see `templates/project.md`). Do not hardcode paths, ticket keys or product names here.
- `Task.md` is the workflow contract. Changing it changes the behaviour in every project that pulls it; keep it short and unambiguous.
- `scripts/` are stdlib-only Python 3 (no installs), runnable from any directory, and must never overwrite a note without `--force`.
- Templates use Czech section names because the tickets are Czech; the workflow text is English.
- Test script changes on real Jira XML, writing to a temp dir.
