#!/usr/bin/env python3
"""Copies partials/*.html into every page. This is the only "build", and it is optional.

A page marks a shared block like this:

    <!-- @include header -->
    ...whatever is here gets replaced...
    <!-- @end header -->

Edit the file in partials/, then run:  python3 tools/sync.py

{{root}} inside a partial becomes the relative path back to the site root ("" or "../"),
or "/" on 404.html, which GitHub Pages can serve from any depth.
The nav link whose data-nav matches the page's <body data-page="..."> gets aria-current.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {"partials", "raw", "directions", "copy", "tools", ".claude", ".git"}
BLOCK = re.compile(r"(<!-- @include ([\w-]+) -->)(.*?)(<!-- @end \2 -->)", re.S)

partials = {p.stem: p.read_text(encoding="utf-8").strip("\n") for p in (ROOT / "partials").glob("*.html")}


def resolved(name, where, seen=()):
    """A partial's text, with any partials it includes already filled in."""
    if name not in partials:
        sys.exit("%s: no partial named %r" % (where, name))
    if name in seen:
        sys.exit("partial %r includes itself" % name)
    return BLOCK.sub(lambda m: "%s\n%s\n%s" % (m.group(1), resolved(m.group(2), where, seen + (name,)), m.group(4)),
                     partials[name])


def expand(text, root, page_key, where):
    text = BLOCK.sub(lambda m: "%s\n%s\n%s" % (m.group(1), resolved(m.group(2), where), m.group(4)), text)
    text = text.replace("{{root}}", root)
    text = re.sub(r' aria-current="page"', "", text)
    if page_key:
        text = text.replace('data-nav="%s"' % page_key, 'data-nav="%s" aria-current="page"' % page_key)
    return text


changed = 0
for page in sorted(ROOT.rglob("*.html")):
    rel = page.relative_to(ROOT)
    if SKIP & set(rel.parts) or rel.name.startswith("_"):
        continue
    src = page.read_text(encoding="utf-8")
    key = re.search(r'<body[^>]*data-page="([\w-]+)"', src)
    root = "/" if rel.name == "404.html" else "../" * (len(rel.parts) - 1)
    out = expand(src, root, key.group(1) if key else None, rel)
    if out != src:
        page.write_text(out, encoding="utf-8")
        changed += 1
        print("updated", rel)
print("%d page(s) updated" % changed)
