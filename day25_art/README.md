# Day 25 — Is this a map?
**Wind writing**

**Output:** `day25_art/day25_art.png`
**Run:** `uv run python -m day25_art.map`

## The story

The prompt asks when something becomes a map and when it stops being one. This
piece removes every conventional map element: no coastline, no labels, no
legend, no scale, no north arrow, no axes. All that remains is the year's
weather, drawn as ink.

Each line is a named 2026 tropical cyclone track in the western North Pacific,
clipped to 100–180°E and 0–45°N. The result looks like handwriting, or roots, or
a weather chart without its annotations. It is still a map in the strict sense —
positions in a coordinate system — but it is also an abstract drawing. The title
and subtitle leave the question open on purpose.

## Data

- **Tracks:** IBTrACS v04r01 last-three-years CSV (`data/ibtracs_last3years.csv`),
  season 2026, named storms only.
- **Filtering:** positions between 100 and 180°E and 0 and 45°N; storms with
  fewer than two valid positions are dropped. 29 tracks survive.
- **Style:** cream paper, near-black ink, one thin line per track, no labels.
- **Licence:** IBTrACS NOAA/NCEI.

## Process

1. Load the cached IBTrACS file, keep 2026 named storms, and convert coordinates
   to numbers.
2. Drop missing positions and clip each track to the western Pacific window.
3. Sort each storm by `ISO_TIME` and draw a single `ax.plot` line at 0.45
   opacity with round caps. Overlaps create darker knots where storms crossed
   the same water.
4. Set the extent to 105–170°E, 2–42°N, with an aspect ratio of 1.2 (a gentle
   latitude correction) so the composition fills the page.
5. Remove axes, ticks, frames and legends.
6. Set a serif title (`WIND WRITING`) and an italic subtitle that states the
   count and asks the question.
7. Save at 200 dpi on cream paper.

## Numbers on the map

- 29 visible storm tracks.
- Window: 105–170°E, 2–42°N.
- No labels, no scale, no legend.

## Data links

External sources used for this map (the local caches live in `data/`):

- [IBTrACS product page](https://www.ncei.noaa.gov/products/international-best-track-archive)
- [NOAA NCEI](https://www.ncei.noaa.gov/)

## What this map does not say

- The count is 29, not the 86 named storms in the full basin, because tracks
  outside the window or with too few positions are excluded.
- Without labels, the reader cannot identify a storm. That is the point of the
  piece, but it also makes it useless as a reference map.
- The line positions are 6-hourly best-track points; the curves between them are
  straight interpolations, not the actual path.
- Overlapping tracks are not distinguishable; the ink density is a visual
  accident, not a count.
- "Is this a map?" is a provocation, not a definition. The piece satisfies a
  coordinate-space definition and fails almost every communicative one.
