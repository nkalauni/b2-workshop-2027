#!/usr/bin/env python3
"""
Page generator for the B2 Reasoning Workshop site.

Why this exists: the site is plain static HTML with no build step required to
*serve* it, but the masthead/footer appear on every page. Editing seven copies
by hand invites drift. Edit content here, run `python3 tools/build.py`, and the
plain .html files are rewritten.

Small copy fixes can also be made directly in the .html files -- just remember
to mirror them here, or the next build will overwrite them.

Stdlib only. No dependencies.
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TITLE = "Reasoning as the Basis for Geo-Scientific Modeling in the Age of AI"
SHORT = "Reasoning &amp; Geo-Scientific Modeling"
DATES = "May 15–19, 2027"
VENUE = "Biosphere 2, Arizona"
EMAIL = "has.reasoning@arizona.edu"

# Set to True to re-gate the site as a private draft (adds a banner and noindex).
PRIVATE_DRAFT = False

NAV = [
    ("theme.html", "Theme"),
    ("program.html", "Program"),
    ("speakers.html", "Speakers"),
    ("venue.html", "Venue &amp; Travel"),
    ("register.html", "Registration"),
    ("organizers.html", "Organizers"),
]

TRUSS = """<svg class="hero__truss" aria-hidden="true" focusable="false">
  <defs>
    <pattern id="truss" width="120" height="104" patternUnits="userSpaceOnUse">
      <path d="M0 104 L60 0 L120 104 Z M60 0 L60 104 M0 104 L120 104 M-60 0 L0 104 M120 104 L180 0"
            fill="none" stroke="#81D3EB" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#truss)"/>
</svg>"""

DRAFT_BAR = """  <p class="draft-flag">
    Private working draft &mdash; not for circulation. Speaker names below are <strong>invited, not yet confirmed</strong>.
    Comments to <a href="mailto:{email}">{email}</a>.
  </p>
""".format(email=EMAIL)


def head(page_title, description, page_css=""):
    full = page_title + " · " + "Reasoning Workshop 2027" if page_title else TITLE
    noindex = '\n<meta name="robots" content="noindex, nofollow">' if PRIVATE_DRAFT else ""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full}</title>
<meta name="description" content="{desc}">{noindex}
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..500&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">{extra}
<script>document.documentElement.className += " js";</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
""".format(full=full, title=TITLE, desc=description, extra=page_css, noindex=noindex)


def masthead(current):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        links.append('      <a href="{h}"{c}>{l}</a>'.format(h=href, c=cur, l=label))
    bar = DRAFT_BAR if PRIVATE_DRAFT else ""
    return bar + """  <header class="masthead">
    <div class="wrap masthead__inner">
      <a class="brand" href="index.html">
        <b>Reasoning &amp; Geo-Scientific Modeling</b>
        <span>Biosphere 2 &middot; {dates}</span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav">Menu</button>
      <nav class="nav" id="primary-nav" aria-label="Primary">
{links}
      </nav>
    </div>
  </header>
  <main id="main">
""".format(dates=DATES, links="\n".join(links))


FOOTER = """  </main>
  <section class="hosts">
    <div class="wrap hosts__inner">
      <div class="hosts__item">
        <p class="hosts__k">Hosted by</p>
        <img class="hosts__has" src="assets/img/has-lockup.png" width="1216" height="235"
             loading="lazy" decoding="async"
             alt="University of Arizona College of Science, Department of Hydrology and Atmospheric Sciences.">
      </div>
      <div class="hosts__item">
        <p class="hosts__k">Held at</p>
        <img class="hosts__b2" src="assets/img/b2-logo.png" width="273" height="168"
             loading="lazy" decoding="async" alt="Biosphere 2, The University of Arizona.">
      </div>
    </div>
  </section>
  <footer class="foot">
    <div class="wrap">
      <div class="foot__grid">
        <div>
          <h4>The workshop</h4>
          <p style="color:var(--on-dark);margin:0 0 .5rem">Reasoning as the Basis for Geo-Scientific Modeling in the Age of AI</p>
          <p style="margin:0">{dates}<br>Biosphere 2, Oracle, Arizona</p>
        </div>
        <div>
          <h4>Pages</h4>
          <ul>{nav}</ul>
        </div>
        <div>
          <h4>Contact</h4>
          <ul>
            <li><a href="mailto:{email}">{email}</a></li>
            <li>Department of Hydrology<br>&amp; Atmospheric Sciences</li>
            <li>University of Arizona</li>
          </ul>
        </div>
      </div>
      <div class="foot__base">
        <p>Hosted by the Department of Hydrology &amp; Atmospheric Sciences, University of Arizona.</p>
        <p>In honor of Professor Hoshin V. Gupta.</p>
      </div>
    </div>
  </footer>
  <script src="assets/js/site.js"></script>
</body>
</html>
"""


def footer():
    nav = "".join(
        '<li><a href="{h}">{l}</a></li>'.format(h=h, l=l) for h, l in NAV
    )
    return FOOTER.format(dates=DATES, nav=nav, email=EMAIL)


def page(filename, page_title, description, content, page_css=""):
    html = head(page_title, description, page_css) + masthead(filename) + content + footer()
    path = os.path.join(ROOT, filename)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return filename, len(html)


# ---------------------------------------------------------------------------
# Reusable pieces
# ---------------------------------------------------------------------------

def hero(eyebrow, title_html, sub, honoree=None, buttons=""):
    hon = ""
    if honoree:
        hon = '\n      <p class="hero__honoree">{h}</p>'.format(h=honoree)
    return """  <section class="hero hero--home">
    <div class="hero__media" aria-hidden="true"></div>
    <div class="hero__frame" aria-hidden="true"></div>
    <div class="wrap hero__inner">
      <p class="eyebrow">{eyebrow}</p>
      <h1>{title}</h1>
      <p class="hero__sub">{sub}</p>{hon}
      {buttons}
    </div>
  </section>
""".format(eyebrow=eyebrow, title=title_html, sub=sub, hon=hon, buttons=buttons)


def page_hero(eyebrow, title, sub):
    """Compact hero for interior pages."""
    return """  <section class="hero hero--plain">
    <div class="hero__frame" aria-hidden="true"></div>
    {truss}
    <div class="wrap hero__inner" style="padding-block:clamp(3rem,7vw,4.5rem) clamp(2.25rem,5vw,3rem)">
      <p class="eyebrow">{eyebrow}</p>
      <h1 style="font-size:clamp(2rem,4.2vw,3.2rem);max-width:20ch">{title}</h1>
      <p class="hero__sub" style="font-size:clamp(1rem,1.7vw,1.2rem)">{sub}</p>
    </div>
  </section>
""".format(truss=TRUSS, eyebrow=eyebrow, title=title, sub=sub)


# ---------------------------------------------------------------------------
# PROGRAM DATA
#
# Source: "B2 Workshop Schedule Planning HVG 040926.docx" reconciled against the
# schedule attached to the 18 Aug 2026 invitation emails (the newer of the two).
#
# Each entry: (kind, time, title, meta, minutes, qa_minutes)
#   kind: "session" | "talk" | "break" | "meal" | "logistics" | "hvg" | "plain"
#   minutes / qa_minutes drive the proportional duration bars. Set both to 0
#   for entries that should not draw a bar.
# ---------------------------------------------------------------------------

PROGRAM = [
    {
        "date": "Saturday, May 15",
        "name": "Tucson",
        "where": "University of Arizona &amp; Hoshin&rsquo;s home",
        "slots": [
            ("logistics", "08:00 – 17:00", "Arrival in Tucson, visits to the HAS department", "", 0, 0),
            ("hvg", "17:00 – 19:00", "Informal get-together with HAS faculty, staff and students",
             "At Hoshin&rsquo;s home", 120, 0),
            ("meal", "19:00 – 21:00", "Dinner on your own", "", 0, 0),
        ],
    },
    {
        "date": "Sunday, May 16",
        "name": "Transfer &amp; arrival",
        "where": "Biosphere 2",
        "slots": [
            ("logistics", "13:00 – 16:00", "Buses from the University of Arizona to Biosphere 2",
             "Departure times confirmed closer to the workshop", 180, 0),
            ("plain", "16:00 – 18:00", "Tour of Biosphere 2", "", 120, 0),
            ("meal", "18:00 – 20:00", "Dinner and socializing", "", 0, 0),
        ],
    },
    {
        "date": "Monday, May 17",
        "name": "Day one",
        "where": "Biosphere 2",
        "slots": [
            ("meal", "07:30 – 08:30", "Breakfast", "", 0, 0),
            ("plain", "08:30 – 09:00", "Welcome and goals", "", 30, 0),
            ("session", "09:00 – 12:00", "Models as Support for Understanding, Reasoning &amp; Discovery",
             "s-models", 0, 0),
            ("talk", "09:00 – 09:45", "Invited keynote", "s-models", 35, 10),
            ("break", "09:45 – 10:00", "Coffee break", "s-models", 15, 0),
            ("talk", "10:00 – 11:20", "Four invited talks", "s-models|4 × 15 min + 5 min discussion", 60, 20),
            ("talk", "11:20 – 12:00", "Moderated discussion", "s-models", 40, 0),
            ("meal", "12:00 – 13:00", "Lunch", "", 0, 0),
            ("plain", "13:00 – 14:00", "Poster session", "", 60, 0),
            ("session", "14:00 – 16:30", "The Learning Problem &mdash; Reflections on Four Decades of Systems Theory",
             "s-reflect", 0, 0),
            ("talk", "14:00 – 16:00", "Four invited talks", "s-reflect|4 × 25 min + 5 min discussion", 100, 20),
            ("break", "16:00 – 16:30", "Coffee break", "s-reflect", 30, 0),
            ("session", "16:30 – 17:30", "The Learning Problem &mdash; An Information-Theoretic Perspective on the Future",
             "s-hvg", 0, 0),
            ("hvg", "16:30 – 17:30", "Invited presentation by Hoshin V. Gupta", "s-hvg", 45, 5),
            ("plain", "17:30 – 18:30", "Poster session", "", 60, 0),
            ("meal", "18:30 – 20:00", "Dinner", "", 0, 0),
            ("hvg", "20:00 – 21:30", "Reflections and celebration of Hoshin&rsquo;s career",
             "s-hvg|An evening set aside to reminisce about Hoshin&rsquo;s career", 90, 0),
        ],
    },
    {
        "date": "Tuesday, May 18",
        "name": "Day two",
        "where": "Biosphere 2",
        "slots": [
            ("meal", "08:00 – 09:00", "Breakfast", "", 0, 0),
            ("session", "09:00 – 12:00", "Models as Support for Understanding, Reasoning &amp; Discovery",
             "s-models", 0, 0),
            ("talk", "09:00 – 09:45", "Invited keynote", "s-models", 35, 10),
            ("break", "09:45 – 10:00", "Coffee break", "s-models", 15, 0),
            ("talk", "10:00 – 11:20", "Four invited talks", "s-models|4 × 15 min + 5 min discussion", 60, 20),
            ("talk", "11:20 – 12:00", "Moderated discussion", "s-models", 40, 0),
            ("meal", "12:00 – 13:00", "Lunch", "", 0, 0),
            ("plain", "13:00 – 14:00", "Poster session", "", 60, 0),
            ("session", "14:00 – 17:30", "The Learning Problem &mdash; Looking to the Future", "s-future", 0, 0),
            ("talk", "14:00 – 14:45", "Invited keynote", "s-future", 35, 10),
            ("break", "14:45 – 15:00", "Coffee break", "s-future", 15, 0),
            ("talk", "15:00 – 16:20", "Four invited talks", "s-future|4 × 15 min + 5 min discussion", 60, 20),
            ("break", "16:20 – 16:30", "Coffee break", "s-future", 10, 0),
            ("talk", "16:30 – 17:30", "Moderated discussion", "s-future", 60, 0),
            ("plain", "17:30 – 18:30", "Poster session", "", 60, 0),
            ("meal", "18:30 – 20:00", "Dinner", "", 0, 0),
            ("plain", "20:00 – 21:00", "Extended discussion &mdash; future planning", "", 60, 0),
        ],
    },
    {
        "date": "Wednesday, May 19",
        "name": "Departure",
        "where": "Biosphere 2 &rarr; Tucson",
        "slots": [
            ("meal", "08:00 – 09:00", "Breakfast", "", 0, 0),
            ("logistics", "09:00 – 11:00", "Buses from Biosphere 2 to the University of Arizona", "", 120, 0),
        ],
    },
]


def render_bar(kind, sess, minutes, qa):
    if not minutes and not qa:
        return ""
    muted = " bar--muted" if kind in ("break", "logistics") else ""
    segs = ""
    if minutes:
        segs += '<span class="bar__seg" style="--m:{m}"></span>'.format(m=minutes)
    if qa:
        segs += '<span class="bar__qa" style="--q:{q}"></span>'.format(q=qa)
    total = minutes + qa
    if qa:
        label = "{t} min &middot; {m} presenting + {q} discussion".format(t=total, m=minutes, q=qa)
    else:
        label = "{t} min".format(t=total)
    return ('\n        <div class="bar{muted}" aria-hidden="true">{segs}'
            '<span class="bar__label">{label}</span></div>').format(
        muted=muted, segs=segs, label=label)


def render_program():
    out = []
    for day in PROGRAM:
        out.append('    <section class="day">')
        out.append('      <div class="day__head">')
        out.append('        <span class="day__date">{d}</span>'.format(d=day["date"]))
        out.append('        <h2 class="day__name">{n}</h2>'.format(n=day["name"]))
        out.append('        <span class="day__where">{w}</span>'.format(w=day["where"]))
        out.append('      </div>')

        for kind, time, title, meta, minutes, qa in day["slots"]:
            sess = ""
            note = ""
            if meta:
                parts = meta.split("|")
                if parts[0].startswith("s-"):
                    sess = parts[0]
                    note = parts[1] if len(parts) > 1 else ""
                else:
                    note = parts[0]

            classes = ["slot"]
            if kind == "session":
                classes.append("slot--session")
            elif kind in ("talk", "break", "hvg"):
                classes.append("slot--sub")
            if kind == "break":
                classes.append("slot--break")
            if kind == "meal":
                classes.append("slot--meal")
            if kind == "hvg":
                classes.append("slot--hvg")

            cls = " ".join(classes)
            if sess:
                cls += " " + sess

            meta_html = ""
            if note:
                meta_html = '\n        <p class="slot__meta">{n}</p>'.format(n=note)

            out.append('      <div class="{cls} reveal">'.format(cls=cls))
            out.append('        <div class="slot__time">{t}</div>'.format(t=time))
            out.append('        <div class="slot__body">')
            out.append('        <p class="slot__title">{t}</p>{m}{b}'.format(
                t=title, m=meta_html, b=render_bar(kind, sess, minutes, qa)))
            out.append('        </div>')
            out.append('      </div>')
        out.append('    </section>')
    return "\n".join(out)


# ---------------------------------------------------------------------------
# SPEAKERS
#
# Source: "Potential Oral Presentation Invitees.docx" + the invitation emails.
#
# To remove or replace a speaker, edit the tuple and rebuild. The status field
# ("invited" / "confirmed") no longer changes the rendering -- everyone is
# listed as speaking -- but it is kept so the committee can track state here.
#
# Deliberately NOT published: the named alternates ("if unavailable then X")
# and the "other possibilities" brainstorm list. Being publicly listed as
# somebody's fallback is worse than not being listed at all. Those names stay
# in the organizers' spreadsheet.
# ---------------------------------------------------------------------------

SESSIONS = [
    {
        "key": "s-models",
        "when": "Monday, May 17 &middot; Morning",
        "title": "Models as Support for Understanding, Reasoning &amp; Discovery",
        "blurb": "How models earn their place as instruments of understanding rather than "
                 "prediction machines &mdash; and what misspecification, diagnostics and "
                 "process reasoning demand of them.",
        "people": [
            ("Thorsten Wagener", "University of Potsdam, Germany", "Keynote", "Models and reasoning", "invited"),
            ("Jasper Vrugt", "University of California, Irvine", "Talk", "Dealing with misspecification", "invited"),
            ("Gab Abramowitz", "UNSW Sydney, Australia", "Talk", "Models and reasoning", "invited"),
            ("Uwe Ehret", "Karlsruhe Institute of Technology, Germany", "Talk",
             "Models and reasoning &middot; bridging process-based and machine learning", "invited"),
            ("Saman Razavi", "University of Saskatchewan, Canada", "Talk", "Models and reasoning", "invited"),
        ],
    },
    {
        "key": "s-reflect",
        "when": "Monday, May 17 &middot; Afternoon",
        "title": "The Learning Problem &mdash; Reflections on Four Decades of Systems Theory",
        "blurb": "A long view of what systems theory taught hydrology about learning from data, "
                 "from the people who did the work.",
        "people": [
            ("Soroosh Sorooshian", "University of California, Irvine", "Talk", "Reflections", "invited"),
            ("Qingyun Duan", "Hohai University, China", "Talk", "Reflections", "invited"),
            ("Harald Kling", "BOKU, Austria", "Talk", "Reflections", "invited"),
            ("Grey Nearing", "Google", "Talk", "Reflections", "invited"),
        ],
    },
    {
        "key": "s-hvg",
        "when": "Monday, May 17 &middot; Late afternoon",
        "title": "The Learning Problem &mdash; An Information-Theoretic Perspective on the Future",
        "blurb": "The honoree&rsquo;s own account of where the learning problem goes next.",
        "people": [
            ("Hoshin V. Gupta", "University of Arizona", "Invited presentation",
             "Information theory and the future of the learning problem", "honoree"),
        ],
    },
    {
        "key": "s-models",
        "when": "Tuesday, May 18 &middot; Morning",
        "title": "Models as Support for Understanding, Reasoning &amp; Discovery",
        "blurb": "The session continues, with a focus on bridging process-based modeling and "
                 "machine learning in practice.",
        "people": [
            ("Martyn Clark", "University of Calgary, Canada", "Keynote", "Models and reasoning", "invited"),
            ("Laura Condon", "University of Arizona", "Talk",
             "Models and reasoning &middot; bridging process-based and machine learning", "invited"),
            ("Bo Guo", "University of Arizona", "Talk",
             "Models and reasoning &middot; bridging process-based and machine learning", "invited"),
            ("Jonathan Frame", "University of Alabama", "Talk",
             "Bridging process-based and machine learning", "invited"),
            ("Andrew Bennett", "University of Arizona", "Talk",
             "Bridging process-based and machine learning", "invited"),
        ],
    },
    {
        "key": "s-future",
        "when": "Tuesday, May 18 &middot; Afternoon",
        "title": "The Learning Problem &mdash; Looking to the Future",
        "blurb": "Equation discovery, new architectures, causality and agentic methods &mdash; "
                 "what the next decade of geo-scientific model development might actually look like.",
        "people": [
            ("Karsten Schulz", "BOKU, Austria", "Keynote", "Equation generation", "invited"),
            ("Hernán Moreno", "University of Texas at El Paso", "Talk",
             "Kolmogorov–Arnold networks &middot; NEAT", "invited"),
            ("Yang Yang", "University of Massachusetts Boston", "Talk",
             "Latent representation &middot; contrastive learning", "invited"),
            ("Yang Hong", "University of Oklahoma", "Talk",
             "Agentic support for model development", "invited"),
            ("Praveen Kumar", "University of Illinois", "Talk",
             "Information theory &middot; causality &middot; agentic methods", "invited"),
        ],
    },
]

BADGE = {
    "invited": "",
    "confirmed": "",
    "honoree": '<span class="badge badge--invited">Honoree</span>',
}


def render_speakers():
    out = []
    for s in SESSIONS:
        out.append('    <section class="sess-block {k} reveal">'.format(k=s["key"]))
        out.append('      <div class="sess-block__head">')
        out.append('        <p class="sess-block__when">{w}</p>'.format(w=s["when"]))
        out.append('        <h2>{t}</h2>'.format(t=s["title"]))
        out.append('        <p style="color:var(--ink-soft);font-size:.95rem">{b}</p>'.format(b=s["blurb"]))
        out.append('      </div>')
        out.append('      <div class="people">')
        for name, affil, role, topic, status in s["people"]:
            out.append('        <article class="person">')
            out.append('          <p class="person__role">{r} {b}</p>'.format(r=role, b=BADGE.get(status, "")))
            out.append('          <h3 class="person__name">{n}</h3>'.format(n=name))
            out.append('          <p class="person__affil">{a}</p>'.format(a=affil))
            out.append('          <p class="person__topic">{t}</p>'.format(t=topic))
            out.append('        </article>')
        out.append('      </div>')
        out.append('    </section>')
    return "\n".join(out)


# ---------------------------------------------------------------------------
# PAGES
# ---------------------------------------------------------------------------

def build_index():
    h = hero(
        eyebrow="Hydrology &amp; Atmospheric Sciences",
        title_html="Reasoning as the Basis for Geo-Scientific Modeling <em>in the Age of AI</em>",
        sub="A two-day scientific workshop at Biosphere 2, examining how physics, domain "
            "understanding, information theory and systems theory can be integrated with "
            "modern AI to advance geoscientific modeling.",
        honoree="In honor of Professor Hoshin V. Gupta",
        buttons='<div class="btn-row">'
                '<a class="btn btn--ghost" href="theme.html">Read the theme</a>'
                '<a class="btn btn--ghost" href="program.html">See the program</a>'
                '</div>',
    )

    strip = """  <section class="strip">
    <div class="wrap">
      <div class="strip__grid">
        <div class="strip__cell">
          <p class="strip__k">Dates</p>
          <p class="strip__v">May 15 – 19, 2027<small>Science on Monday 17 and Tuesday 18</small></p>
        </div>
        <div class="strip__cell">
          <p class="strip__k">Venue</p>
          <p class="strip__v">Biosphere 2<small>Oracle, Arizona</small></p>
        </div>
        <div class="strip__cell">
          <p class="strip__k">Format</p>
          <p class="strip__v">Single track<small>Invited talks, moderated discussion, posters</small></p>
        </div>
        <div class="strip__cell">
          <p class="strip__k">Capacity</p>
          <p class="strip__v">About 100<small>Limited by the B2 conference facilities</small></p>
        </div>
      </div>
    </div>
  </section>
"""

    motivation = """  <section class="section">
    <div class="wrap wrap--narrow">
      <p class="eyebrow">Motivation</p>
      <p class="lede">While recent advances in artificial intelligence (AI) are transforming the
      Geosciences at an unprecedented rate, these developments are raising fundamental questions
      about the critical roles of reasoning, process understanding, counterfactual analysis and
      physical consistency in geo-scientific investigation and model development. Such concerns
      become even more pressing given the clear observational evidence that geo-scientific systems
      can no longer be treated as stationary.</p>
      <div class="btn-row"><a class="btn btn--light" href="theme.html">The full theme</a></div>
    </div>
  </section>
"""

    sessions = """  <section class="section">
    <div class="wrap">
      <p class="eyebrow">Three threads over two days</p>
      <div class="grid grid--3">
        <article class="card session-key s-models reveal">
          <p class="card__tag">Monday &amp; Tuesday mornings</p>
          <h3>Models as Support for Understanding, Reasoning &amp; Discovery</h3>
          <p>What it takes for a model to function as an instrument of understanding: diagnostics,
          misspecification, and the bridge between process-based and learned representations.</p>
        </article>
        <article class="card session-key s-reflect reveal" data-delay="90">
          <p class="card__tag">Monday afternoon</p>
          <h3>The Learning Problem &mdash; Reflections on Four Decades of Systems Theory</h3>
          <p>A long view of what systems theory taught hydrology about learning from data,
          from the people who did the work.</p>
        </article>
        <article class="card session-key s-future reveal" data-delay="180">
          <p class="card__tag">Tuesday afternoon</p>
          <h3>The Learning Problem &mdash; Looking to the Future</h3>
          <p>Equation discovery, new architectures, causality and agentic methods &mdash; where
          geo-scientific model development goes from here.</p>
        </article>
      </div>
      <div class="btn-row"><a class="btn btn--light" href="program.html">Full program &amp; timings</a></div>
    </div>
  </section>
"""

    honor = """  <section class="section honor">
    <div class="wrap">
      <div class="honor__layout">
        <div>
          <p class="eyebrow">The occasion</p>
          <h2>Celebrating the career of Hoshin V. Gupta</h2>
          <p class="lede">The workshop celebrates the scientific contributions of Professor Hoshin
          Gupta, whose work has insisted on the importance of reasoning, diagnostics and
          hypothesis testing in hydrologic science.</p>
          <p>Hoshin turns 70 on May 3, 2027, and formally retires in the spring of that year,
          though he plans to remain engaged and hold Emeritus status. Two moments in the
          schedule are set aside for the occasion.</p>
          <ul class="honor__events">
            <li>
              <time datetime="2027-05-15T17:00">Sat May 15, 17:00</time>
              <span>An informal get-together with HAS faculty, staff and students at Hoshin&rsquo;s home.</span>
            </li>
            <li>
              <time datetime="2027-05-17T16:30">Mon May 17, 16:30</time>
              <span>Hoshin&rsquo;s own presentation: <em>The Learning Problem &mdash; An
              Information-Theoretic Perspective on the Future</em>.</span>
            </li>
            <li>
              <time datetime="2027-05-17T20:00">Mon May 17, 20:00</time>
              <span>An evening at Biosphere 2 to reminisce about Hoshin&rsquo;s career.</span>
            </li>
          </ul>
        </div>
        <figure class="portrait">
          <img src="assets/img/hoshin.jpg" width="900" height="1350" loading="lazy" decoding="async"
               alt="Portrait of Hoshin V. Gupta.">
          <figcaption>Professor Hoshin V. Gupta, University of Arizona.</figcaption>
        </figure>
      </div>
    </div>
  </section>
"""

    dates = """  <section class="section">
    <div class="wrap">
      <p class="eyebrow">Key dates</p>
      <h2 style="max-width:16ch">What happens between now and May 2027</h2>
      <ul class="dates" style="margin-top:2.5rem">
        <li>
          <time datetime="2026-09-09">September 9, 2026</time>
          <div><strong>Invited speakers confirm participation.</strong>
          Replies to the invitation emails are due.</div>
        </li>
        <li>
          <time datetime="2026-11">Fall 2026</time>
          <div><strong>Confirmed speakers and detailed program announced.</strong></div>
        </li>
        <li>
          <time>Date to be announced</time>
          <div><strong>Registration opens.</strong><span class="tentative">Tentative</span>
          <br>Timing depends on pending funding decisions. Watch this page.</div>
        </li>
        <li>
          <time>Spring 2027</time>
          <div><strong>Poster abstracts due.</strong><span class="tentative">Tentative</span>
          <br>All general participants are asked to bring a poster.</div>
        </li>
        <li data-now>
          <time datetime="2027-05-15">May 15 – 19, 2027</time>
          <div><strong>The workshop.</strong> Tucson, then Biosphere 2.</div>
        </li>
      </ul>
    </div>
  </section>
"""

    cta = """  <section class="cta">
    <div class="wrap wrap--narrow">
      <p class="eyebrow">Taking part</p>
      <h2>Attendance is limited to about 100 people.</h2>
      <p>Capacity is set by the conference facilities at Biosphere 2 and includes both visitors
      and local participants. A registration fee will be charged to cover logistics, accommodation
      and meals on site. General participants are asked to bring a poster relating their work to
      the workshop theme.</p>
      <div class="btn-row">
        <a class="btn btn--ghost" href="register.html">Registration details</a>
        <a class="btn btn--ghost" href="venue.html">Venue &amp; travel</a>
      </div>
    </div>
  </section>
"""

    preload = ('\n<link rel="preload" as="image" href="assets/img/hero-biosphere2.jpg" '
               'fetchpriority="high">')
    return page("index.html", "", 
                "A two-day scientific workshop at Biosphere 2, May 2027, on reasoning as the basis "
                "for geo-scientific modeling in the age of AI, honoring Professor Hoshin V. Gupta.",
                h + strip + motivation + sessions + honor + dates + cta, preload)


def build_theme():
    h = page_hero(
        "The theme",
        "Reasoning as the Basis for Geo-Scientific Modeling in the Age of AI",
        "Why this workshop, and what we hope comes out of it.",
    )
    body = """  <section class="section">
    <div class="wrap wrap--narrow">
      <p class="eyebrow">Motivation</p>
      <p class="lede">While recent advances in artificial intelligence (AI) are transforming the
      Geosciences at an unprecedented rate, these developments are raising fundamental questions
      about the critical roles of reasoning, process understanding, counterfactual analysis and
      physical consistency in geo-scientific investigation and model development. Such concerns
      become even more pressing given the clear observational evidence that geo-scientific systems
      can no longer be treated as stationary.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap wrap--narrow">
      <p class="eyebrow">Workshop focus</p>
      <p class="lede">This workshop will examine how reasoning-based approaches, rooted in physics,
      domain understanding (including hydrology and atmospheric science), information theory, and
      systems theory can be suitably integrated with modern AI methods to advance geoscientific
      modeling. It therefore aims to initiate a dialog aimed at addressing these and related
      issues.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <p class="eyebrow">Sessions</p>
      <div class="grid grid--3">
        <article class="card session-key s-models reveal">
          <p class="card__tag">Monday &amp; Tuesday mornings</p>
          <h3>Models as Support for Understanding, Reasoning &amp; Discovery</h3>
          <p>Models as instruments of understanding rather than prediction machines: diagnostics,
          misspecification, and bridging process-based and learned representations.</p>
        </article>
        <article class="card session-key s-reflect reveal" data-delay="90">
          <p class="card__tag">Monday afternoon</p>
          <h3>The Learning Problem &mdash; Reflections on Four Decades of Systems Theory</h3>
          <p>What systems theory taught hydrology about learning from data, recounted by
          the people who built that record.</p>
        </article>
        <article class="card session-key s-future reveal" data-delay="180">
          <p class="card__tag">Tuesday afternoon</p>
          <h3>The Learning Problem &mdash; Looking to the Future</h3>
          <p>Equation discovery, new architectures, latent representation, causality and
          agentic methods for model development.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section honor">
    <div class="wrap">
      <div class="honor__layout">
        <div>
          <p class="eyebrow">Celebration</p>
          <h2>In honor of Professor Hoshin V. Gupta</h2>
          <p class="lede">The workshop celebrates the career and scientific contributions of
          Professor Hoshin Gupta, whose work has emphasized the importance of reasoning,
          diagnostics and hypothesis testing in hydrologic science.</p>
          <p>Hoshin will be 70 years of age on May 3, 2027, and will formally retire in the
          spring of 2027, although he plans to remain engaged and to maintain Emeritus status.
          The workshop&rsquo;s theme is drawn directly from the questions he has spent a career
          pressing on the field.</p>
          <ul class="honor__events">
            <li>
              <time datetime="2027-05-15T17:00">Sat May 15, 17:00</time>
              <span>Informal pre-workshop get-together at Hoshin&rsquo;s home, with HAS faculty,
              staff and students.</span>
            </li>
            <li>
              <time datetime="2027-05-17T16:30">Mon May 17, 16:30</time>
              <span>Hoshin&rsquo;s own presentation: <em>The Learning Problem &mdash; An
              Information-Theoretic Perspective on the Future</em>.</span>
            </li>
            <li>
              <time datetime="2027-05-17T20:00">Mon May 17, 20:00</time>
              <span>An evening at Biosphere 2 to reminisce about Hoshin&rsquo;s career.</span>
            </li>
          </ul>
        </div>
        <figure class="portrait">
          <img src="assets/img/hoshin.jpg" width="900" height="1350" loading="lazy" decoding="async"
               alt="Portrait of Hoshin V. Gupta.">
          <figcaption>Professor Hoshin V. Gupta, University of Arizona.</figcaption>
        </figure>
      </div>
    </div>
  </section>

  <section class="cta">
    <div class="wrap wrap--narrow">
      <p class="eyebrow">Next</p>
      <h2>The program is built around discussion, not just talks.</h2>
      <p>Two full days of invited presentations, four poster sessions and four moderated
      discussion periods.</p>
      <div class="btn-row">
        <a class="btn btn--ghost" href="program.html">See the program</a>
        <a class="btn btn--ghost" href="speakers.html">Invited speakers</a>
      </div>
    </div>
  </section>
"""
    return page("theme.html", "Theme",
                "Motivation, focus and sessions for the 2027 Biosphere 2 workshop on reasoning "
                "as the basis for geo-scientific modeling in the age of AI.",
                h + body)


def build_program():
    h = page_hero(
        "Program",
        "Five days, two of them science",
        "Arrival and a tour on the weekend, two full days of talks, posters and discussion "
        "at Biosphere 2, and departure Wednesday morning.",
    )
    legend = """  <section class="section section--tight">
    <div class="wrap">
      <div class="legend">
        <span class="legend__item"><span class="legend__swatch"></span> Presenting time</span>
        <span class="legend__item"><span class="legend__swatch legend__swatch--qa"></span> Discussion / Q&amp;A</span>
        <span class="legend__item">Bars are drawn to scale &mdash; length is real minutes.</span>
      </div>
      <div class="note" style="margin:-1rem 0 2.5rem">
        Program subject to change. Session titles and timings are settled; individual
        speakers are assigned to slots as the program is finalised.
      </div>
"""
    body = legend + render_program() + """
    </div>
  </section>

  <section class="cta">
    <div class="wrap wrap--narrow">
      <p class="eyebrow">Presenting</p>
      <h2>Four poster sessions, one hour each.</h2>
      <p>General participants are asked to bring a poster showing how their work relates to the
      workshop theme.</p>
      <div class="btn-row">
        <a class="btn btn--ghost" href="register.html">Posters &amp; registration</a>
      </div>
    </div>
  </section>
"""
    return page("program.html", "Program",
                "Full schedule for the 2027 Biosphere 2 workshop, May 15–19, with session "
                "timings drawn to scale.",
                h + body)


def build_speakers():
    h = page_hero(
        "Speakers",
        "Invited speakers",
        "Talks are organised into three threads across Monday and Tuesday.",
    )
    notice = """  <section class="section">
    <div class="wrap">
      <div class="note" style="margin-bottom:3rem">
        Speakers and session assignments are subject to change. This page is updated as the
        program is finalised.
      </div>
"""
    body = notice + render_speakers() + """
    </div>
  </section>

  <section class="cta">
    <div class="wrap wrap--narrow">
      <p class="eyebrow">Everyone else</p>
      <h2>Participants present posters.</h2>
      <p>Beyond the invited talks, the workshop runs on its poster sessions and discussion
      periods. If you are attending, plan to bring a poster on how your work relates to the theme.</p>
      <div class="btn-row"><a class="btn btn--ghost" href="register.html">How to take part</a></div>
    </div>
  </section>
"""
    return page("speakers.html", "Speakers",
                "Invited speakers for the 2027 Biosphere 2 workshop on reasoning as the basis "
                "for geo-scientific modeling in the age of AI.",
                h + body)


def build_venue():
    h = page_hero(
        "Venue &amp; travel",
        "Biosphere 2",
        "The workshop is held at the conference facilities of Biosphere 2, in Oracle, Arizona, "
        "about 30 miles north of Tucson.",
    )
    body = """  <section class="section">
    <div class="wrap">
      <div class="grid grid--2" style="gap:clamp(2rem,5vw,3.5rem);align-items:start">
        <div>
          <p class="eyebrow">The site</p>
          <p class="lede">Biosphere 2 is a University of Arizona research facility: a sealed
          glass-and-steel structure enclosing several biomes, built to study Earth systems as
          coupled wholes.</p>
          <p>Participants stay on site, and a guided tour of the facility is scheduled for
          Sunday afternoon before the science begins.</p>
        </div>
        <figure>
          <div class="figure-ph">
            <img src="assets/img/biosphere2.jpg" width="1600" height="900" loading="lazy" decoding="async"
                 alt="The stepped glass pyramid of the Biosphere 2 rainforest biome seen from below against a clear blue sky, its white space-frame truss visible through the glazing.">
          </div>
          <figcaption>The glass pyramid enclosing the rainforest biome.</figcaption>
        </figure>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <figure class="reveal">
        <div class="figure-ph" style="aspect-ratio:1500/885">
          <img src="assets/img/b2-interior.jpg" width="1500" height="885" loading="lazy" decoding="async"
               alt="Inside the Biosphere 2 rainforest biome: dense tropical vegetation under the glass roof, with three people on a walkway for scale.">
        </div>
        <figcaption>Inside the rainforest biome, one of five enclosed under glass.</figcaption>
      </figure>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <p class="eyebrow">Getting there</p>
      <h2 style="max-width:18ch">Buses run from campus in both directions</h2>
      <div class="grid grid--2" style="margin-top:2.5rem">
        <article class="card">
          <p class="card__tag">Sunday, May 16 &middot; 13:00 – 16:00</p>
          <h3>University of Arizona &rarr; Biosphere 2</h3>
          <p>Chartered buses carry participants from campus to B2 on Sunday afternoon.
          Exact pickup points and departure times will be confirmed closer to the workshop.</p>
        </article>
        <article class="card">
          <p class="card__tag">Wednesday, May 19 &middot; 09:00 – 11:00</p>
          <h3>Biosphere 2 &rarr; University of Arizona</h3>
          <p>Return buses run Wednesday morning after breakfast. Plan departing flights with
          the transfer time in mind.</p>
        </article>
      </div>
      <div class="note" style="margin-top:2rem">
        Travel to Tucson is arranged by participants. Tucson International Airport (TUS) is the
        nearest airport; Phoenix Sky Harbor (PHX) is roughly a two-hour drive and often has more
        international connections.
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <p class="eyebrow">Before the workshop</p>
      <div class="grid grid--2" style="gap:clamp(2rem,5vw,3.5rem);align-items:start">
        <figure style="order:2">
          <div class="figure-ph figure-ph--tall">
            <img src="assets/img/campus-aerial.jpg" width="1200" height="798" loading="lazy" decoding="async"
                 alt="Aerial view of the University of Arizona campus at golden hour, red-brick buildings among palms.">
          </div>
          <figcaption>The University of Arizona campus in Tucson.</figcaption>
        </figure>
        <div style="order:1">
          <h2 style="max-width:20ch">Saturday and Sunday in Tucson</h2>
          <p style="margin-top:1.5rem">Participants are welcome to arrive early. Saturday, May 15 is
          set aside for arrival, visits to the Department of Hydrology &amp; Atmospheric Sciences on
          the University of Arizona campus, and an informal evening get-together at Hoshin&rsquo;s home.
          Dinner that evening is on your own.</p>
          <p>Accommodation in Tucson for the nights before the transfer is arranged by
          participants.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="cta">
    <div class="wrap wrap--narrow">
      <p class="eyebrow">Staying on site</p>
      <h2>Accommodation and meals at Biosphere 2 are covered by the registration fee.</h2>
      <p>Participants stay on site for the three nights of the workshop, arriving Sunday afternoon
      and leaving after breakfast on Wednesday. The fee covers logistical expenses including
      lodging and meals at B2; the amount will be published when registration opens.</p>
      <div class="btn-row"><a class="btn btn--ghost" href="register.html">Registration</a></div>
    </div>
  </section>
"""
    return page("venue.html", "Venue &amp; travel",
                "Biosphere 2 venue information, bus transfers from the University of Arizona, "
                "and travel guidance for the May 2027 workshop.",
                h + body)


def build_register():
    h = page_hero(
        "Registration",
        "Taking part",
        "Attendance is limited to about 100 people. Registration opens once funding decisions "
        "are settled.",
    )
    body = """  <section class="section">
    <div class="wrap">
      <div class="grid grid--2" style="gap:clamp(2rem,5vw,3.5rem);align-items:start">
        <div>
          <p class="eyebrow">Status</p>
          <h2>Registration is not yet open.</h2>
          <p class="lede">The opening date depends on pending funding decisions, and will be
          announced here and by email to the workshop mailing list.</p>
          <p>If you received an invitation email, replying to it is what matters for now &mdash;
          it tells the organizers you intend to come, and it holds a place against a hard capacity
          limit. Formal registration comes later.</p>
          <div class="btn-row">
            <a class="btn" href="mailto:{email}?subject=B2%20Workshop%202027%20%E2%80%94%20mailing%20list">
              Ask to join the mailing list</a>
          </div>
        </div>
        <div>
          <ul class="dates" style="margin-top:0">
            <li>
              <time datetime="2026-09-09">September 9, 2026</time>
              <div><strong>Invited speakers reply</strong><br>
              <span style="color:var(--ink-soft);font-size:.9rem">Acceptance of speaking invitations due.</span></div>
            </li>
            <li>
              <time>Date to be announced</time>
              <div><strong>Registration opens</strong><span class="tentative">Tentative</span></div>
            </li>
            <li>
              <time>Spring 2027</time>
              <div><strong>Poster abstracts due</strong><span class="tentative">Tentative</span></div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <p class="eyebrow">What to expect</p>
      <div class="grid grid--3">
        <article class="card">
          <p class="card__tag">Capacity</p>
          <h3>About 100 participants</h3>
          <p>Set by the conference facilities at Biosphere 2, and counted across both visiting
          and local participants.</p>
        </article>
        <article class="card">
          <p class="card__tag">Fee</p>
          <h3>A registration fee will be charged</h3>
          <p>It covers logistical expenses including accommodation and meals at Biosphere 2.
          The amount will be published when registration opens.</p>
        </article>
        <article class="card">
          <p class="card__tag">Presenting</p>
          <h3>Bring a poster</h3>
          <p>General participants are asked to present a poster on how their work relates to the
          workshop theme. Abstract submission details follow.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap wrap--narrow">
      <p class="eyebrow">Posters</p>
      <h2>Every participant presents</h2>
      <p>Four hour-long poster sessions are scheduled across Monday and Tuesday, two on
      each day.</p>
      <p>An abstract submission system is being set up. Submission opens alongside registration,
      and the deadline will be announced with it.</p>
      <div class="note" style="margin-top:2rem">
        Sessions may be recorded and published. Registration will include a permission waiver
        covering recording and publication; you will be able to decline it.
      </div>
    </div>
  </section>

  <section class="cta">
    <div class="wrap wrap--narrow">
      <p class="eyebrow">Questions</p>
      <h2>Write to the organizing committee.</h2>
      <p>For questions about registration, travel, accessibility or anything else,
      contact <a href="mailto:{email}">{email}</a>.</p>
      <div class="btn-row"><a class="btn btn--ghost" href="organizers.html">Who is organizing this</a></div>
    </div>
  </section>
""".replace("{email}", EMAIL)
    return page("register.html", "Registration",
                "Registration, fees, capacity and poster presentation information for the "
                "May 2027 Biosphere 2 workshop.",
                h + body)


def build_organizers():
    h = page_hero(
        "Organizers",
        "Who is organizing this",
        "The workshop is convened by the Department of Hydrology &amp; Atmospheric Sciences at "
        "the University of Arizona.",
    )

    faculty = [
        ("Bo Guo", "University of Arizona"),
        ("Laura Condon", "University of Arizona"),
        ("Ali Behrangi", "University of Arizona"),
        ("Andrew Bennett", "University of Arizona"),
    ]
    students = [
        ("Maria Castro", "University of Arizona"),
        ("Mohammad Ali Farmani", "University of Arizona"),
        ("Nabin Kalauni", "University of Arizona"),
        ("Jawad Muhammad", "University of Arizona"),
        ("Hossein Yousefi Sohi", "University of Arizona"),
    ]

    def roster(people):
        cells = []
        for name, affil in people:
            cells.append(
                '        <div class="roster__cell"><h3>{n}</h3><p>{a}</p></div>'.format(n=name, a=affil))
        return '      <div class="roster">\n' + "\n".join(cells) + "\n      </div>"

    body = """  <section class="section">
    <div class="wrap">
      <p class="eyebrow">Organizing committee</p>
      <h2 style="max-width:20ch">Faculty organizing committee</h2>
      <p style="margin-bottom:2rem">Department of Hydrology &amp; Atmospheric Sciences,
      University of Arizona.</p>
""" + roster(faculty) + """
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <p class="eyebrow">Student team</p>
      <h2 style="max-width:22ch">Student organizing team</h2>
      <p style="margin-bottom:2rem">Graduate students in HAS handling the program, registration,
      abstracts, communications and this website.</p>
""" + roster(students) + """
    </div>
  </section>

  <section class="section honor">
    <div class="wrap">
      <div class="honor__layout">
        <div>
          <p class="eyebrow">Honoree</p>
          <h2>Hoshin V. Gupta</h2>
          <p class="lede">Professor of Hydrology and Atmospheric Sciences, University of Arizona.</p>
          <p>Hoshin&rsquo;s work has emphasized the importance of reasoning, diagnostics and
          hypothesis testing in hydrologic science. He turns 70 on May 3, 2027 and formally
          retires that spring, remaining engaged with Emeritus status.</p>
        </div>
        <figure class="portrait">
          <img src="assets/img/hoshin.jpg" width="900" height="1350" loading="lazy" decoding="async"
               alt="Portrait of Hoshin V. Gupta.">
          <figcaption>Professor Hoshin V. Gupta, University of Arizona.</figcaption>
        </figure>
      </div>
    </div>
  </section>

  <section class="cta">
    <div class="wrap wrap--narrow">
      <p class="eyebrow">Contact</p>
      <h2>One address reaches the whole committee.</h2>
      <p><a href="mailto:{email}">{email}</a></p>
      <p>Department of Hydrology &amp; Atmospheric Sciences<br>
      University of Arizona, Tucson, Arizona</p>
    </div>
  </section>
""".replace("{email}", EMAIL)

    return page("organizers.html", "Organizers",
                "Faculty and student organizing committee for the 2027 Biosphere 2 workshop "
                "honoring Professor Hoshin V. Gupta.",
                h + body)


def main():
    built = [
        build_index(),
        build_theme(),
        build_program(),
        build_speakers(),
        build_venue(),
        build_register(),
        build_organizers(),
    ]
    print("Built {n} pages into {root}".format(n=len(built), root=ROOT))
    for name, size in built:
        print("  {n:<20} {s:>7,} bytes".format(n=name, s=size))
    if PRIVATE_DRAFT:
        print("\n  NOTE: PRIVATE_DRAFT is True -- the draft banner and noindex tag are active.")
        print("        Set PRIVATE_DRAFT = False in tools/build.py before public launch.")


if __name__ == "__main__":
    main()
