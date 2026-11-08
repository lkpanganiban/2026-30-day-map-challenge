# Day 10 — Prompting only
**The strongest storm of 2026**

**Output:** `day10_prompting/day10_prompting.png`
**Run:** `uv run python -m day10_prompting.map`

## The story

The challenge reserves Day 10 for maps produced from start to finish by
prompting an AI: "make AI work for its money." This whole series is built with
an AI coding agent, so the honest version of the day is not to pretend otherwise.
The map was specified in conversation, generated as a script, run, and fixed
from the rendered image — no hand-edited geometry, no manual styling pass in a
graphics editor.

The subject is **Super Typhoon Champi**, locally named **Rosal**, the strongest
tropical cyclone of 2026 by maximum sustained wind. On 21 October it passed
close enough to Batanes for PAGASA to raise Signal No. 2. The map shows the
track at its closest approach to the islands, coloured by wind speed, with the
peak intensity marked.

## Data

- **Track:** IBTrACS v04r01 last-three-years CSV, storm `CHAMPI`, fields `LAT`,
  `LON`, `USA_WIND`, `ISO_TIME`.
- **Land:** Natural Earth 1:10m western Pacific land (`data/wp_land.gpkg`).
- **Philippine territory:** OSM country relation clipped to land
  (`data/ph_boundary.gpkg`).
- **Event facts:** Batanes Signal No. 2 on 21 October 2026; Champi classified as
  the strongest cyclone of the year.
- **Licences:** IBTrACS NOAA/NCEI; OSM ODbL; Natural Earth public domain.

## Process

1. Load the cached IBTrACS file and keep only `CHAMPI`.
2. Convert coordinates and wind to numbers, drop missing positions, and sort by
   time.
3. Project the track to Web Mercator and split it into segments.
4. Colour each segment by wind: blue below 64 kt, yellow for typhoon strength,
   orange for strong typhoon, red for super typhoon (137 kt and above). A wide
   transparent duplicate creates the glow.
5. Draw the western Pacific land faintly and Philippine land more brightly, so
   Batanes is visible without a locator inset.
6. Find the closest track point to Batanes (121.97°E, 20.45°N) and annotate it
   with the date (22 October in UTC; 21 October local).
7. Find the peak-wind point and label the intensity (159 kt).
8. Set the map extent to 116–133°E, 14–24°N so both the closest approach and the
   peak remain inside the frame.
9. Compose the title, a three-line subtitle that states the prompting method
   plainly, and the source footer.

## Numbers on the map

- Peak intensity: 159 kt.
- Closest approach to Batanes: 22 October 2026 UTC (21 October local).
- Signal level over Batanes: No. 2.
- Track coloured in four wind bands.

## Data links

External sources used for this map (the local caches live in `data/`):

- [IBTrACS product page](https://www.ncei.noaa.gov/products/international-best-track-archive)
- [IBTrACS CSV access](https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/)
- [PAGASA](https://www.pagasa.dost.gov.ph/)
- [Natural Earth](https://www.naturalearthdata.com/)

## What this map does not say

- IBTrACS is a best-track archive compiled after the event; it is not the
  warning timeline PAGASA issued.
- The closest-approach label is computed from a 6-hourly track point, so the
  true closest pass could be slightly nearer between samples.
- "Strongest of 2026" is by maximum sustained wind in this archive; other
  metrics (central pressure, integrated kinetic energy) could rank storms
  differently.
- The land and boundary layers are simplified. Batanes is a small archipelago
  and is barely visible at this scale.
- The map demonstrates a prompting workflow, not a claim that prompting is a
  substitute for domain review. Every number was checked against the cached
  data.
