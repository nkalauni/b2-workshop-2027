# Images

All images here are already sized and compressed for the web. The originals
live outside the repository — keep them somewhere safe, because these are
lossy and not worth re-editing.

| File | Used on | Source |
|---|---|---|
| `hero-biosphere2.jpg` | Home hero | Official B2 photo `201009_B2_exterior_0004` — golden-hour aerial of the whole complex |
| `biosphere2.jpg` | Venue | Official B2 photo `201009_B2_exterior_0002` — rainforest biome pyramid, cropped to 16:9 |
| `b2-interior.jpg` | Venue | Official B2 photo `201009_B2_0001` — inside the rainforest biome |
| `campus-aerial.jpg` | Venue | University of Arizona campus aerial |
| `hoshin.jpg` | Home, Theme, Organizers | Hoshin's headshot, resized to 900×1350 |
| `has-lockup.png` | Footer band, every page | Official HAS / College of Science lockup |
| `b2-logo.png` | Footer band, every page | Official Biosphere 2 / University of Arizona wordmark lockup, supplied as JPEG; white background knocked out to transparent |

## Replacing one

Keep the same filename and the pages pick it up with no code change. Match the
aspect ratio or the crop will shift:

- hero — wide, 2200px, roughly 1.87:1
- `biosphere2.jpg` — 16:9
- `b2-interior.jpg` — roughly 1.7:1
- `hoshin.jpg` — 2:3 portrait, face high in the frame (CSS crops to 4:5 biased
  toward the top)

If you change a photo's dimensions, update the `width` and `height` attributes
on its `<img>` tag in `tools/build.py` too. They are there to stop the page
jumping around as images load.

## Adding a new photograph

Resize before committing — nothing needs to exceed 2200px on its long edge:

```sh
sips -Z 2200 photo.jpg          # macOS, no extra software
```

Then check the total: the whole site should stay well under 2 MB of images, or
it gets slow on conference wifi.

## About the B2 logo

It arrived as a JPEG on a flat white background, which cannot sit on a coloured
surface as-is. The transparent PNG in this folder was made by ramping alpha
across the near-white pixels and then un-matting the partial ones from white,
so the edges carry no pale fringe. A plain "make white transparent" would have
left a visible halo.

If you ever get a vector version (SVG or EPS) from Biosphere 2, use that
instead — it will be sharper at every size and a fraction of the file size.

## Credit and licensing

The Biosphere 2 photographs are official University of Arizona / Biosphere 2
images. If B2 or UA Communications require a photographer credit for public
use, add it to the `figcaption` in `tools/build.py` — the captions are already
there, so it is a one-line change.

## Not currently used

`ua_block_rgb_3.png` (the standalone UA block A) is not on the site — the HAS
lockup already contains it, and showing both reads as logo clutter. Kept
outside the repo in case the flyer needs it.
