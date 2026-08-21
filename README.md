# Reasoning as the Basis for Geo-Scientific Modeling in the Age of AI

Website for the workshop at Biosphere 2, May 15–19, 2027, honoring
Professor Hoshin V. Gupta.

Hosted by the Department of Hydrology & Atmospheric Sciences, University of Arizona.

**Live at <https://nkalauni.github.io/reasoning-workshop-2027/>** — published from
`main` via GitHub Pages. Pushing to `main` redeploys within a minute or two.
See [DEPLOY.md](DEPLOY.md).

## Running it

There is no build step and no dependencies. To preview:

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Checking how it looks

`tools/shots.py` screenshots every page at desktop and phone widths and reports
any failed requests or JS errors. Optional — it needs playwright, which the site
itself does not:

```sh
pip install playwright && playwright install chromium
python3 -m http.server 8765 &
python3 tools/shots.py
```

## Editing

Two ways, and they interact — read this bit.

**For a quick wording fix**, edit the `.html` file directly. It is plain HTML.

**For anything structural** — the navigation, the schedule, the speaker list, or
text that appears on more than one page — edit `tools/build.py` and run:

```sh
python3 tools/build.py
```

That regenerates all seven pages from one source, which is what keeps the
masthead and footer from drifting apart.

⚠️ **Running the build overwrites hand edits made in the `.html` files.** If you
edit HTML directly, mirror the change into `tools/build.py`, or the next person
to run the build will silently undo your work.

### Where things live

| What | Where |
|---|---|
| Schedule | `PROGRAM` list in `tools/build.py` |
| Speakers | `SESSIONS` list in `tools/build.py` |
| Navigation | `NAV` list in `tools/build.py` |
| Contact address | `EMAIL` in `tools/build.py` |
| Draft banner / `noindex` | `PRIVATE_DRAFT` in `tools/build.py` |
| Colours, type, layout | `assets/css/site.css` |
| Menu and scroll behaviour | `assets/js/site.js` |
| Photographs | `assets/img/` — see the README in that folder |
| Screenshot review | `tools/shots.py` (optional, needs playwright) |
| Verbatim-text check | `tools/check_verbatim.py` |
| Forbidden-copy check | `tools/check_forbidden.py` |

### Changing the speaker list

Edit the `SESSIONS` list in `tools/build.py` and rebuild. Each entry is
`(name, affiliation, role, topic, status)`. The `status` field no longer
changes what is rendered — everyone listed appears as a speaker — but it is
kept so the committee can track who has actually replied.

Named alternates and the "other possibilities" brainstorm list are deliberately
not on the site. Being publicly listed as somebody's fallback is worse than not
being listed at all.

## Quoted text

The Motivation and Workshop Focus paragraphs on the Home and Theme pages are
copied word for word from the workshop invitation. Keep them that way — don't
paraphrase, re-punctuate, or add sentences to them.

```sh
python3 tools/check_verbatim.py
```

diffs those paragraphs against the invitation document and exits non-zero if
they have drifted.

```sh
python3 tools/check_forbidden.py
```

fails if copy that must not be public has crept back in — anything about
funding or grants, and a few phrasings that were cut for being filler.
Registration timing is stated as unopened, never explained.

## Design notes for whoever picks this up

- **The palette carries meaning.** Cool glass-blue and midnight are the science;
  the terracotta (`--mesa`) is reserved *only* for sections about Hoshin
  himself. Please don't spend the warm colour elsewhere — it stops working
  as a signal the moment it becomes decoration.
- **The Program bars are drawn to scale.** A bar's length is the block's real
  duration in minutes, and the hatched segment is discussion time, taken from
  the `[35+10]` notation in the planning document. If you add a slot, put in
  honest minute counts or the whole device becomes a lie.
- Typefaces: Newsreader (display), IBM Plex Sans (body), IBM Plex Mono (times,
  labels, data). Loaded from Google Fonts.
- The hero photograph sits under a *directional* scrim — heavy on the left where
  the headline is, light on the right so the building stays visible. If you swap
  the hero image for one composed the other way round, flip the gradient angle
  in `.hero__frame` or the headline will lose contrast.
- The site works with JavaScript disabled and prints legibly — the Program page
  makes a decent handout on paper.

## Not in this repository, on purpose

The planning documents in the parent folder — the invitee spreadsheet in
particular — contain personal email addresses and internal notes. `.gitignore`
excludes `.docx` and `.xlsx` so they cannot be committed by accident. Keep it
that way.

## Known gaps

- Registration dates and fee are unset, pending funding decisions
- Abstract submission system not yet chosen, so nothing is linked
- Workshop logo and flyer (Hossein and Maria) not yet incorporated
