#!/usr/bin/env python3
"""List or set the `state` property of ticket notes.

Usage:
  state.py list [DIR]            table of key, state, estimate, title for every note in DIR
  state.py get KEY [DIR]         print the state of one note
  state.py set KEY STATE [DIR]   set the state (validated), DIR defaults to the current directory

States, in order: NEW OPEN PLANNED CODED COMMITED PUSHED. Stdlib only.
"""
import re
import sys
from pathlib import Path

STATES = ["NEW", "OPEN", "PLANNED", "CODED", "COMMITED", "PUSHED"]
FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def notes(directory):
    for path in sorted(Path(directory).glob("*.md")):
        text = path.read_text(encoding="utf-8")
        m = FM_RE.match(text)
        if not m or not re.search(r"^key:", m.group(1), re.M):
            continue
        yield path, text, m.group(1)


def prop(front, name):
    m = re.search(rf"^{name}:[ \t]*(.*)$", front, re.M)
    return m.group(1).strip().strip('"') if m else ""


def find(key, directory):
    for path, text, front in notes(directory):
        if prop(front, "key") == key:
            return path, text, front
    sys.exit(f"{key}: no note with this key in {directory}")


def main(argv):
    if not argv or argv[0] not in ("list", "get", "set"):
        sys.exit(__doc__)
    cmd = argv[0]
    if cmd == "list":
        directory = argv[1] if len(argv) > 1 else "."
        rows = [(prop(f, "key"), prop(f, "state") or "-", prop(f, "estimate_md") or "-", prop(f, "title"))
                for _, _, f in notes(directory)]
        rows.sort(key=lambda r: (STATES.index(r[1]) if r[1] in STATES else -1, r[0]))
        for r in rows:
            print(f"{r[0]:<12} {r[1]:<9} {r[2]:<8} {r[3]}")
    elif cmd == "get":
        key = argv[1]
        print(prop(find(key, argv[2] if len(argv) > 2 else ".")[2], "state"))
    else:
        if len(argv) < 3:
            sys.exit(__doc__)
        key, state = argv[1], argv[2].upper()
        if state not in STATES:
            sys.exit(f"invalid state {state}; allowed: {', '.join(STATES)}")
        path, text, front = find(key, argv[3] if len(argv) > 3 else ".")
        old = prop(front, "state")
        if re.search(r"^state:", front, re.M):
            new_front = re.sub(r"^state:.*$", f"state: {state}", front, count=1, flags=re.M)
        else:
            new_front = re.sub(r"^(status:.*)$", rf"\1\nstate: {state}", front, count=1, flags=re.M)
        path.write_text(text.replace(front, new_front, 1), encoding="utf-8")
        print(f"{key}: {old or '-'} -> {state}")


if __name__ == "__main__":
    main(sys.argv[1:])
