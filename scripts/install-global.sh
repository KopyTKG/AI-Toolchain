#!/usr/bin/env bash
# Link the toolchain's skills into the global Claude Code skills folder.
#
# Usage: install-global.sh [--uninstall] [--dry-run] [--force] [--target DIR] [TOOLCHAIN_DIR]
#
#   TOOLCHAIN_DIR  folder holding skills/ and Task.md (default: the repo this script is in)
#   --target DIR   skills folder to link into (default: ~/.claude/skills)
#   --uninstall    remove the links that point into TOOLCHAIN_DIR
#   --dry-run      print what would happen, change nothing
#   --force        replace an existing entry of the same name that is not our link
#
# Links are absolute symlinks, so the skills resolve the toolchain through their own location
# (see "First" step in each SKILL.md). Re-running is safe. Exit code 1 if a name conflict was skipped.
set -euo pipefail

uninstall=0 dry=0 force=0
target="${HOME}/.claude/skills"
root=""

while [ $# -gt 0 ]; do
  case "$1" in
    --uninstall) uninstall=1 ;;
    --dry-run) dry=1 ;;
    --force) force=1 ;;
    --target) shift; target="${1:?--target needs a directory}" ;;
    -h|--help) sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) echo "unknown option: $1" >&2; exit 2 ;;
    *) root="$1" ;;
  esac
  shift
done

if [ -z "$root" ]; then
  root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
else
  root="$(cd "$root" && pwd -P)"
fi

[ -f "$root/Task.md" ] && [ -d "$root/skills" ] || {
  echo "$root is not a toolchain (needs Task.md and skills/)" >&2; exit 1; }

run() { if [ "$dry" -eq 1 ]; then echo "  would: $*"; else "$@"; fi; }

[ "$uninstall" -eq 1 ] || run mkdir -p "$target"

linked=0 skipped=0 removed=0 conflicts=0
for skill in "$root"/skills/*/; do
  [ -f "${skill}SKILL.md" ] || continue
  name="$(basename "$skill")"
  skill="${skill%/}"
  link="$target/$name"

  if [ "$uninstall" -eq 1 ]; then
    if [ -L "$link" ] && [ "$(readlink -f "$link")" = "$(readlink -f "$skill")" ]; then
      echo "remove  $link"; run rm "$link"; removed=$((removed + 1))
    elif [ -e "$link" ] || [ -L "$link" ]; then
      echo "keep    $link (not a link into $root)"; skipped=$((skipped + 1))
    fi
    continue
  fi

  if [ -L "$link" ] && [ "$(readlink -f "$link")" = "$(readlink -f "$skill")" ]; then
    echo "ok      $link"; skipped=$((skipped + 1)); continue
  fi
  if [ -e "$link" ] || [ -L "$link" ]; then
    if [ "$force" -eq 1 ]; then
      echo "replace $link"; run rm -rf "$link"
    else
      echo "SKIP    $link exists and is not our link (use --force to replace)" >&2
      skipped=$((skipped + 1)); conflicts=$((conflicts + 1)); continue
    fi
  else
    echo "link    $link"
  fi
  run ln -s "$skill" "$link"; linked=$((linked + 1))
done

if [ "$uninstall" -eq 1 ]; then
  echo "removed $removed, kept $skipped"
else
  echo "linked $linked, unchanged/skipped $skipped  (target: $target)"
  echo "Open a new Claude Code session or run /skills to load them."
fi
[ "$conflicts" -eq 0 ] || { echo "$conflicts skill(s) skipped because of a name conflict" >&2; exit 1; }
