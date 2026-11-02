#!/usr/bin/env python3
"""Convert a Jira RSS XML export into an Obsidian note (state: NEW).

Usage: xml2note.py ISSUE.xml [-o OUT_DIR] [--force]

Writes OUT_DIR/{KEY}.md (default: next to the XML). Stdlib only.
Estimate and plan are left empty; they are filled in later (see Task.md).
"""
import argparse
import re
import sys
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path

KEY_RE = re.compile(r"[A-Z][A-Z0-9]+-\d+")


class JiraHtml(HTMLParser):
    """Jira-rendered HTML (description field) -> Markdown, enough for tickets."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0  # depth inside elements we drop (lozenges, macro icons)
        self.macro_depth = 0
        self.list_stack = []
        self.table = None  # list of rows while inside <table>
        self.cell = None
        self.row = None
        self.header_row = False
        self.link_href = None

    def _w(self, text):
        if self.cell is not None:
            self.cell.append(text)
        else:
            self.out.append(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "") or ""
        if self.skip:
            if tag == "span":
                self.skip += 1
            return
        if tag == "span" and "jira-issue-macro" in cls.split() and a.get("data-jira-key"):
            self._w(f"[[{a['data-jira-key']}]]")
            self.skip = 1  # drop the inner link/icon/lozenge
            return
        if tag in ("h1", "h2", "h3", "h4"):
            self._w("\n\n" + "#" * int(tag[1]) + " ")
        elif tag == "p":
            self._w("\n\n")
        elif tag in ("ul", "ol"):
            self.list_stack.append(tag)
            self._w("\n")
        elif tag == "li":
            indent = "  " * (len(self.list_stack) - 1)
            mark = "1." if self.list_stack and self.list_stack[-1] == "ol" else "-"
            self._w(f"\n{indent}{mark} ")
        elif tag in ("b", "strong"):
            self._w("**")
        elif tag in ("i", "em"):
            self._w("*")
        elif tag in ("tt", "code"):
            self._w("`")
        elif tag == "br":
            self._w("\n")
        elif tag == "a":
            # <a name=...> are heading anchors; only real links become Markdown links
            self.link_href = a.get("href")
            if self.link_href:
                self._w("[")
        elif tag == "img":
            if a.get("src"):
                self._w(f"![{a.get('alt', '')}]({a['src']})")
        elif tag == "table":
            self.table = []
        elif tag == "tr":
            self.row = []
            self.header_row = False
        elif tag in ("th", "td"):
            self.cell = []
            if tag == "th":
                self.header_row = True

    def handle_endtag(self, tag):
        if self.skip:
            if tag == "span":
                self.skip -= 1
            return
        if tag in ("b", "strong"):
            self._w("**")
        elif tag in ("i", "em"):
            self._w("*")
        elif tag in ("tt", "code"):
            self._w("`")
        elif tag in ("ul", "ol"):
            if self.list_stack:
                self.list_stack.pop()
            self._w("\n")
        elif tag == "a":
            if self.link_href:
                self._w(f"]({self.link_href})")
            self.link_href = None
        elif tag in ("th", "td"):
            text = " ".join("".join(self.cell).split()).replace("|", "\\|")
            self.row.append(text)
            self.cell = None
        elif tag == "tr":
            self.table.append((self.header_row, self.row))
            self.row = None
        elif tag == "table":
            self._flush_table()

    def handle_data(self, data):
        if self.skip:
            return
        self._w(data if self.cell is not None else re.sub(r"\s*\n\s*", " ", data))

    def _flush_table(self):
        rows, self.table = self.table, None
        if not rows:
            return
        header = rows[0][1] if rows[0][0] else [""] * len(rows[0][1])
        body = rows[1:] if rows[0][0] else rows
        self.out.append("\n\n| " + " | ".join(header) + " |\n")
        self.out.append("|" + "|".join(["---"] * len(header)) + "|\n")
        for _, cells in body:
            self.out.append("| " + " | ".join(cells) + " |\n")

    def markdown(self):
        text = "".join(self.out)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip() + "\n"


def text_of(item, tag):
    el = item.find(tag)
    return (el.text or "").strip() if el is not None and el.text else ""


def linked_keys(item):
    keys = []
    for el in item.iter("issuekey"):
        if el.text and el.text.strip() not in keys:
            keys.append(el.text.strip())
    return keys


def yaml_str(value):
    if value == "" or re.search(r'[:#\[\]{}&*!|>\'"%@`]', value) or value != value.strip():
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return value


def convert(xml_path):
    root = ET.parse(xml_path).getroot()
    item = root.find("./channel/item")
    if item is None:
        sys.exit(f"{xml_path}: no <item> found")
    key = text_of(item, "key")
    summary = text_of(item, "summary")
    parent = text_of(item, "parent")
    created = text_of(item, "created")
    created_iso = parsedate_to_datetime(created).date().isoformat() if created else ""

    related = [k for k in linked_keys(item) if k != key and k != parent]
    # keys mentioned in the description (macros) are linked too, so the vault graph connects
    parser = JiraHtml()
    parser.feed(text_of(item, "description"))
    body = parser.markdown()
    for k in KEY_RE.findall(body):
        if k not in related and k not in (key, parent):
            related.append(k)

    fm = [
        "---",
        f"key: {key}",
        f"title: {yaml_str(summary)}",
        f"type: {yaml_str(text_of(item, 'type'))}",
        f"status: {yaml_str(text_of(item, 'status'))}",
        "state: NEW",
        f"priority: {text_of(item, 'priority')}",
        f"assignee: {yaml_str(text_of(item, 'assignee'))}",
        f"reporter: {yaml_str(text_of(item, 'reporter'))}",
        f'parent: "[[{parent}]]"' if parent else "parent:",
        "related: [" + ", ".join(f'"[[{k}]]"' for k in related) + "]",
        f"created: {created_iso}",
        "estimate_md:",
        f"url: {text_of(item, 'link')}",
        "tags: [jira]",
        "---",
    ]
    attachments = [
        f"- {a.get('name')} ({a.get('size')} B)" for a in item.iter("attachment")
    ]
    parts = ["\n".join(fm), f"# {key}: {summary}", body]
    if attachments:
        parts.append("## Přílohy\n\n" + "\n".join(attachments))
    parts += [
        "## Odhad práce (člověk)\n\n_(doplnit)_",
        "## Plan\n\n_(doplnit)_",
    ]
    return key, "\n\n".join(parts) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("xml", type=Path)
    ap.add_argument("-o", "--out-dir", type=Path)
    ap.add_argument("--force", action="store_true", help="overwrite an existing note")
    args = ap.parse_args()
    key, note = convert(args.xml)
    out = (args.out_dir or args.xml.parent) / f"{key}.md"
    if out.exists() and not args.force:
        sys.exit(f"{out} exists (use --force to overwrite; it may hold a plan and estimate)")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(note, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
