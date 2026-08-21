#!/usr/bin/env python3
"""
Fail if copy that must never appear on the public site has crept back in.

    python3 tools/check_forbidden.py

Exits non-zero on a hit. Run before pushing.
"""
import glob, html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Substring, and why it is banned.
FORBIDDEN = [
    ("funding",        "internal financial matters are not public"),
    ("ORP ",           "internal grant programme"),
    ("grant applica",  "internal financial matters are not public"),
    ("Watch this page", "filler"),
    ("much of the point", "editorial flourish"),
    ("not a side activity", "editorial flourish"),
    ("worth protecting", "editorial flourish"),
    ("El D",           "El Dia is a separate March event, unconnected to this workshop"),
]

bad = 0
for path in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
    text = html.unescape(re.sub(r"<[^>]+>", " ", open(path, encoding="utf8").read()))
    for needle, why in FORBIDDEN:
        if needle.lower() in text.lower():
            # "model development" contains "el d"; require a word boundary there
            if needle == "El D" and not re.search(r"\bEl D", text):
                continue
            bad += 1
            print(f"  {os.path.basename(path):16} contains {needle!r} — {why}")
if not bad:
    print("  no forbidden copy found")
sys.exit(1 if bad else 0)
