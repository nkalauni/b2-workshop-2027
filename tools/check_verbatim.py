#!/usr/bin/env python3
"""
Check that the Motivation and Workshop Focus paragraphs on the built pages are
still word-for-word identical to the invitation document.

    python3 tools/check_verbatim.py

Exits non-zero on a mismatch.
"""
import difflib, html, os, re, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCX = os.path.join(ROOT, "..", "Hoshin Gupta retirement symposium",
                    "B2 Workshop Email Draft HVG 081826 TCA_BG.docx")

CHECKS = [("theme.html", "Motivation", "Motivation:"),
          ("theme.html", "Workshop focus", "Workshop Focus:"),
          ("index.html", "Motivation", "Motivation:")]


def norm(t):
    t = html.unescape(re.sub(r"<[^>]*>", " ", t))
    t = t.replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", t).strip().rstrip(".")


def source():
    if not os.path.exists(DOCX):
        print("source document not found; skipping check")
        sys.exit(0)
    raw = zipfile.ZipFile(DOCX).read("word/document.xml").decode("utf8")
    txt = html.unescape(re.sub(r"<[^>]*>", "", re.sub(r"<w:p[^>]*>", "\n", raw)))
    out = {}
    for line in txt.split("\n"):
        for key in ("Motivation:", "Workshop Focus:"):
            if line.strip().startswith(key) and key not in out:
                out[key] = line.strip()[len(key):].strip()
    return out


def rendered(page, eyebrow):
    h = open(os.path.join(ROOT, page), encoding="utf8").read()
    m = re.search(r'<p class="eyebrow">' + eyebrow + r"</p>(.*?)</section>", h, re.S)
    return norm(" ".join(re.findall(r"<p[^>]*>(.*?)</p>", m.group(1), re.S)))


src, bad = source(), 0
for page, eyebrow, key in CHECKS:
    got, want = rendered(page, eyebrow), norm(src[key])
    if got == want:
        print(f"  ok      {page:12} {eyebrow}")
    else:
        bad += 1
        print(f"  DIFFERS {page:12} {eyebrow}")
        for d in difflib.unified_diff(want.split(), got.split(), lineterm="", n=2):
            if d.startswith(("+", "-")) and not d.startswith(("+++", "---")):
                print("      ", d)
sys.exit(1 if bad else 0)
