#!/usr/bin/env python3
"""Check the store-text blocks of a release-notes file.

Usage: notes_check.py FILE.md [--limit 500] [--fix]

For every `## <locale> (N / LIMIT characters)` heading followed by a ``` block, counts the
characters of the block and reports a wrong N or a block over LIMIT. --fix rewrites the heading
counts. Stdlib only. Exit code 1 if anything is wrong.
"""
import argparse
import re
import sys
from pathlib import Path

HEAD = re.compile(r"^(## [A-Za-z]{2}-[A-Za-z]{2}) \((\d+) / (\d+) characters\)$")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file", type=Path)
    ap.add_argument("--limit", type=int, default=500)
    ap.add_argument("--fix", action="store_true")
    args = ap.parse_args()

    lines = args.file.read_text(encoding="utf-8").split("\n")
    bad = 0
    over = 0
    found = 0
    i = 0
    while i < len(lines):
        m = HEAD.match(lines[i])
        if not m:
            i += 1
            continue
        start = i
        j = i + 1
        while j < len(lines) and not lines[j].startswith("```"):
            j += 1
        k = j + 1
        block = []
        while k < len(lines) and not lines[k].startswith("```"):
            block.append(lines[k])
            k += 1
        text = "\n".join(block)
        n = len(text)
        found += 1
        status = "ok"
        if n > args.limit:
            status = f"OVER LIMIT {args.limit}"
            bad += 1
            over += 1
        elif n != int(m.group(2)):
            status = f"heading says {m.group(2)}"
            bad += 1
        print(f"{m.group(1)[3:]}: {n} / {args.limit}  {status}")
        if args.fix:
            lines[start] = f"{m.group(1)} ({n} / {args.limit} characters)"
        i = k + 1
    if not found:
        sys.exit("no '## xx-XX (N / LIMIT characters)' headings found")
    if args.fix:
        args.file.write_text("\n".join(lines), encoding="utf-8")
        sys.exit(1 if over else 0)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
