# Day 15 — Inside out
**The sea between the islands**

**Output:** `day15_insideout/day15_insideout.png`
**Run:** `uv run python -m day15_insideout.map`

## The story

Conventional maps colour land and leave the sea as empty background. For an
archipelago, that is backwards. The Philippines is mostly water: the West
Philippine Sea, the Philippine Sea, the Sulu, Celebes, Bohol, Sibuyan and
Visayan seas are the connective tissue between 7,000+ islands, and they are
where typhoons travel.

This map turns the convention inside out. The seas are pale and named; the
islands are dark gaps. The subject is the water. Two recent paths are overlaid:
**Champi (Rosal)** crossing the Philippine Sea in October 2026, and a dashed
circle marking where **Tino (Kalmaegi)** crossed the Visayan Sea and the
Cebu–Negros islands in November 2026.

## Data

- **Land:** Natural Earth 1:10m (`data/ph_land.gpkg`).
- **National boundary:** OSM country relation (`data/ph_boundary.gpkg`), drawn
  dashed as the outer limit of territory.
- **Champi track:** IBTrACS v04r01, 2026, storm `CHAMPI`.
- **Tino location:** the landfall/crossing area around 123.65°E, 10.55°N, with a
  schematic 120 km radius circle. Tino itself is not in the archive used for the
  track data.
- **Sea labels:** eight manual positions (West Philippine Sea, Luzon Strait,
  Philippine Sea, Sibuyan Sea, Visayan Sea, Sulu Sea, Celebes Sea, Bohol Sea).
- **Licences:** Natural Earth public domain; OSM ODbL; IBTrACS NOAA.

## Process

1. Load land and boundary, project both to Web Mercator.
2. Set the figure background to a pale sea green and draw land in a dark navy
   with a thin slate edge.
3. Plot the national boundary as a dashed grey line.
4. Build the Champi track from `LAT`/`LON`, project it, and draw it as a red
   polyline. Find a track point near 125.3°E, 20.6°N for the label.
5. Draw a dashed red 120 km circle around the Tino crossing area and label it
   "Tino · 4 Nov".
6. Place the eight sea names at hand-chosen coordinates. Each label gets a
   sea-coloured halo so it remains readable over islands.
7. Use dark text for the title block (the background is light), and the series
   red for accents.
8. Set the extent to the national bounding box and save at 200 dpi.

## Numbers on the map

- Eight named seas.
- One typhoon track (Champi, October 2026).
- One 120 km schematic Tino crossing circle.
- The national boundary is drawn as a dashed outline.

## Data links

External sources used for this map (the local caches live in `data/`):

- [Natural Earth](https://www.naturalearthdata.com/)
- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)
- [IBTrACS product page](https://www.ncei.noaa.gov/products/international-best-track-archive)
- [PAGASA](https://www.pagasa.dost.gov.ph/)

## What this map does not say

- The inversion is a design choice, not a physical one. It changes what the eye
  reads first, not the underlying geography.
- The Tino circle is a location marker, not a track or a damage footprint. The
  best-track archive used for the line data did not yet contain Kalmaegi.
- The sea names are approximate label positions; maritime boundaries are not
  shown and are politically sensitive.
- The national boundary relation includes territorial waters and is simplified.
- Natural Earth 1:10m drops many small islands, which matters visually in an
  archipelago map.
