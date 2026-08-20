# Images

Drop files in here with these exact names and the pages pick them up
automatically. Until then, each slot shows a labelled placeholder — nothing
breaks, so there is no rush.

| File | Used on | Wanted |
|---|---|---|
| `hero-biosphere2.jpg` | Home page hero background | Landscape, **2400×1400 or wider**. The glass pyramids work best. It sits behind a dark blue overlay at 50% opacity, so a bright, high-contrast shot survives it. Avoid anything with text or a busy centre — the headline sits over the left half. |
| `hoshin.jpg` | Home, Theme, Organizers | Portrait, **4:5 ratio**, at least 800×1000. Cropped with `object-fit: cover`, so leave a little headroom. |
| `biosphere2.jpg` | Venue & Travel | Landscape **16:9**, at least 1600×900. A different shot from the hero. |

## Also useful, not yet wired in

- University of Arizona, HAS department, and Biosphere 2 logos (SVG preferred,
  otherwise transparent PNG at 2× the display size)
- The workshop logo and flyer, once Hossein and Maria have them
- A HAS department or campus photograph for the Venue page

## Before committing a photograph

- Confirm you have the right to publish it. B2 and UA Communications both have
  media libraries with clear licensing; a photo pulled off a search engine does not.
- Resize first. Nothing here needs to exceed 2400px on its long edge, and
  large files make the page slow on conference wifi.
  `sips -Z 2400 photo.jpg` works on macOS with no extra software.
- Add a credit line if the source requires one — put it in the `figcaption`.
