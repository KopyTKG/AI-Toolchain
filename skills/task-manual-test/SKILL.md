---
name: task-manual-test
description: Write the "Manuální test" section of a ticket note - the UI/UX checks the dev must do by hand, with route, component, how to find it in the app, steps and expected result. Use for "/task-manual-test KEY", "what do I need to test", or when a change touches UI.
---

# task-manual-test

## First

1. Find the toolchain folder; every `<toolchain>` below means it. Try in order and take the first that contains `Task.md`:
   - `toolchain_dir` in the repo's `project.md` (relative to the repo root, absolute, or `~/...`)
   - the env var `AI_TOOLCHAIN_DIR`
   - the folder this skill was loaded from, with symlinks resolved (`readlink -f`), two levels up (works for a global install)
   If none works, tell the dev and stop.
2. Read the repo's `project.md`. If it is missing, ask the dev whether to create it from `<toolchain>/templates/project.md`: prefill what the repo shows (main branch, build commands, work folder candidates), ask for the rest, write it only after the dev agrees, then continue. Never invent values.
3. Read `<toolchain>/Task.md`; its rules win over this skill.

Follow `Task.md` ("Manual UI/UX testing"). UI behaviour is never claimed as verified; it is handed to the dev.

## Steps
1. Find what changed: `git diff {main_branch}...HEAD --stat` (or the plan, if nothing is coded yet). Keep only UI-visible changes.
2. For each affected screen, look it up; do not guess:
   - route: the route file from `project.md` (path and menu label)
   - component: the file that renders the change
   - how to reach it: menu path from the route labels, then the click path (which row, icon, button), citing the file and line that renders the trigger
3. Write `## Manuální test` in the note (language of the ticket):
   - a table: `#`, what, route, component, how to get there
   - per item: steps, expected result, and the browser from `project.md` (e.g. Chrome/Edge)
   - data needed (which record, account, state) and how to create it if it does not exist
   - a regression list: neighbouring screens that must behave as before
   - known browser limits that are not bugs
4. Mention what cannot be tested by hand without a decision (e.g. open questions in the plan).
5. Give the dev the list as a prompt in the reply: "To be tested manually by you:" followed by the numbered items. Do not mark them done.

## Rules
- If a route or menu label cannot be confirmed from the code, write "not verified" next to it.
- Do not change `state`; testing does not move the note between states.
