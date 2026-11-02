---
name: task-manual-test
description: Write the "Manuální test" section of a ticket note - the UI/UX checks the dev must do by hand, with route, component, how to find it in the app, steps and expected result. Use for "/task-manual-test KEY", "what do I need to test", or when a change touches UI.
---

# task-manual-test

## First

1. Read `project.md` of the repo. `toolchain_dir` there is the folder this toolchain lives in; every `<toolchain>` below means it. If `project.md` or `toolchain_dir` is missing, tell the dev and stop.
2. Read `<toolchain>/Task.md`; its rules win over this skill.

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
