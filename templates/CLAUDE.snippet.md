## Task toolchain

Applies only in repos that have a `project.md` (Jira tasks as RSS XML). The shared toolchain lives in `<TOOLCHAIN_DIR>/` (per-project: a folder in the repo; global: e.g. `~/AI-Toolchain`).
Before working on a ticket in such a repo, read `<TOOLCHAIN_DIR>/Task.md` and follow it exactly.
Skills `/task-init` (marks the folder that holds the issue XML and notes), `/task-intake`, `/task-start`, `/task-commit`, `/task-manual-test` and `/task-status` drive the steps; they locate the toolchain through `toolchain_dir` in `project.md`, the env var `AI_TOOLCHAIN_DIR`, or their own install location.
Project facts for the toolchain (work folder, branch and commit rules, build commands) are in `project.md`.
