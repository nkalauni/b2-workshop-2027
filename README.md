# Reasoning as the Basis for Geo-Scientific Modeling in the Age of AI

Website for the workshop at Biosphere 2, May 15–19, 2027, honoring
Professor Hoshin V. Gupta.

Hosted by the Department of Hydrology & Atmospheric Sciences, University of Arizona.

> **Status: private working draft.** Every speaker listed is *invited, not
> confirmed* — replies were due September 9, 2026. Do not make this repository
> or the site public until the organizing committee has signed off. See
> [DEPLOY.md](DEPLOY.md).

## Running it

There is no build step and no dependencies. To preview:

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

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

### Updating a speaker when they accept

In `SESSIONS`, change that person's status from `"invited"` to `"confirmed"`
and rebuild. The "Invited" badge disappears. When everyone in a session is
confirmed, delete the notice block in `build_speakers()`.

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
- No photographs yet — placeholders are showing
- Workshop logo and flyer (Hossein and Maria) not yet incorporated
