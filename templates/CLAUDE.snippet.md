## Task toolchain

Jira tasks (RSS XML) are handled by the shared toolchain in `<TOOLCHAIN_DIR>/`.
Before working on any ticket, read `<TOOLCHAIN_DIR>/Task.md` and follow it exactly.
Skills `/task-intake`, `/task-start`, `/task-commit`, `/task-manual-test` and `/task-status` drive the steps; they locate the toolchain through `toolchain_dir` in `project.md`.
Project facts for the toolchain (work folder, branch and commit rules, build commands) are in `project.md`.
