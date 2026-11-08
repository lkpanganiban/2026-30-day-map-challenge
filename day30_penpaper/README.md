# Day 30 — Pen & paper
**Mayon, a map to draw by hand**

**Output:** `day30_penpaper/day30_penpaper.pdf` (A4) and
`day30_penpaper/day30_penpaper.png`
**Run:** `uv run python -m day30_penpaper.map`

## The story

The final day asks you to close the laptop and draw. This folder contains the
part a script can do: a printable tracing sheet. It is deliberately sparse — a
coastline, the primary roads, the towns, the 6 km danger zone and a scale bar,
all in black line work on white A4.

The rest is yours. Trace the coast, ink the roads, mark the ash plume, add the
evacuation centres, write the names you know. Photograph the result. That is the
map this series cannot make for you.

## Data

- **Land:** Natural Earth 1:10m coastline (`data/ph_land.gpkg`), clipped to the
  Mayon area.
- **Roads:** OSM primary, secondary and tertiary highways around Mayon
  (`data/mayon_places.gpkg`), clipped to the land so ferry routes and lines
  across water disappear.
- **Towns:** OSM `place=city|town` nodes around the volcano.
- **Zone:** 6 km buffer around the summit (13.2573°N, 123.6855°E).
- **Page:** A4 portrait.
- **Licence:** OSM data © OpenStreetMap contributors, ODbL; Natural Earth public
  domain.

## Process

1. Load the cached Mayon land, road and place layers; project to UTM 51N.
2. Draw land as an outline only, roads as thin grey-black lines clipped to the
   land polygon, and the 6 km zone as a dashed circle.
3. Place town names in a small serif face at their OSM coordinates; mark the
   summit with a triangle and a two-line elevation label.
4. Add a 10 km scale bar in the lower-left.
5. Add a double rule border and a centred title (`MAYON — a map to draw by
   hand`) with three short instructions.
6. Save the figure as a vector PDF for printing and a PNG preview.
7. The PDF is the deliverable; the PNG exists so the day has a viewable image in
   the repo.

## Numbers on the map

- A4 portrait, 210 × 297 mm.
- 10 km scale bar.
- 6 km danger-zone radius.
- Mayon summit: 2,462 m.

## Data links

External sources used for this map (the local caches live in `data/`):

- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)
- [Overpass API](https://overpass-api.de/)
- [PHIVOLCS](https://www.phivolcs.dost.gov.ph/)

## What this map does not say

- This is a base sheet, not the finished day. The analogue map is the one you
  draw on it.
- The roads are a simplified primary network; smaller streets and footpaths are
  omitted to leave room for hand annotation.
- The zone circle is a schematic buffer, not the official hazard polygon.
- The coastline is Natural Earth 1:10m, so small coves and reclaimed land are
  generalised.
- The sheet has no legend, no north arrow beyond the page orientation, and no
  data attribution inside the drawing area; the footer carries the source.
