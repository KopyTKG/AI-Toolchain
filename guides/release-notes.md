# Guide: patch notes and release notes

How to write the notes that go with a version tag of an app (mobile client, store listing). Taken from the ServiceDesk mobile client; the project's own `project.md` and `CLAUDE.md` win where they differ.

**Opt-in:** this applies only to repos with a "Releases" section in `project.md`, and only when the dev asks for it (`/task-commit --rc` for a patch/RC, `/task-commit --bump` for a release). A normal commit never bumps, writes notes or tags.

## Kinds of notes

There are two kinds. A **patch** is one release candidate: its notes tell the devkits (testers, developers) what changed in that RC. A **release** groups the patches since the last release into one text for the store.

| Kind | Tag | Written | File | Template |
|------|-----|---------|------|----------|
| **Patch notes** (= RC notes) | `X.Y.Z-rc.N` | For every RC; only the changes since the previous tag | `<version>-rc<N>.md` | `templates/release-notes-rc.md` |
| **Release notes** | `X.Y.Z-release` | When the version goes to the store; groups all patch notes since the last release | `<version>.md` | `templates/release-notes-release.md` |

Files live in the project's `docs/release-notes/` (set `release_notes_dir` in `project.md`). "Patch" and "RC" mean the same thing in this toolchain; the file and tag spelling stays `rc` (`2.6.2-rc6.md`). There is no separate patch-level version bump (`X.Y.P`) unless the project defines one in `project.md`.

## Order of work for a tag

1. **Write the notes.**
2. **Commit them** together with the version bump (`package.json` version, `rc` field, build number), so the tag, the bump and the notes are one thing.
3. **Tag and push.** A tag is never created without its notes in the commit it points at. Pushing a tag is outward-facing: only when the dev asks.

## What goes in

**Patch notes (RC)**
- Source: `git log <previous-tag>..HEAD`, plus the merged tickets. Previous tag = the previous RC, or the last release for `rc.1`.
- Only what changed in this RC, not the whole cycle. The devkits read it to know what to retest.
- One bullet per change a user or tester would notice. Not a commit list.
- Nothing visible changed: "Drobná vylepšení a opravy." / "Minor improvements and fixes."
- Changes only developers see (CI, logging, docs, build output names) go in the trailing "Developer-facing (not for the store)" section, never in the store blocks.
- Heading is `Novinky ve verzi X.Y.Z (RC N)` / `What's new in X.Y.Z (RC N)`.

**Release notes**
- Groups the patches: a TL;DR of **all** patch notes since the previous published release, not the RC-by-RC history. What the user gets compared with the last version they have.
- Merge duplicates (a bug mentioned in rc2 and fixed again in rc5 is one bullet). Drop anything a user cannot see (banner, log, build and CI work).
- No developer-facing section.
- A release that is just the last RC promoted (no code change) carries the grouped list of all its patches, as `2.5.15` did.

## Store text rules

- Two blocks, `cs-CZ` first (primary) and `en-US`, each in a fenced block with a count in the heading: `## cs-CZ (202 / 500 characters)`.
- Limit is 500 characters per language (Google Play). Count includes the title line and bullets.
- Format: title line, blank line, bullets with `• `. One sentence per bullet, user language, no ticket keys, no internals.
- Czech and English say the same thing; do not drop a bullet from one language only.
- Check and fix counts: `python3 <toolchain>/scripts/notes_check.py docs/release-notes/<file>.md [--fix]`. Exit code 1 means a wrong count or a block over the limit.

## Changelog

If the project keeps a `CHANGELOG.md` (Keep a Changelog), the developer-facing detail goes there per tag (Added / Changed / Fixed), with the why. Store notes are the short user version of it. Do not paste one into the other.

## Checklist before tagging

- [ ] Notes file named after the tag spelling used by the output folders (`2.6.2-rc6.md`, not `2.6.2-rc.6.md`)
- [ ] Heading `(build N)` matches `buildNumber` (RCs share the version's build number; it moves only for a release)
- [ ] `rc` field in `package.json` matches the RC tag; deleted for a final release
- [ ] `notes_check.py` passes
- [ ] cs-CZ and en-US carry the same bullets
- [ ] Notes, version bump and docs in one commit; tag points at it
- [ ] Docs describing changed behaviour are in the same commit

## Not decided by the toolchain

Which store lists, which languages besides cs-CZ/en-US, tag spelling, and where builds are uploaded come from the project. Put them in `project.md`.
