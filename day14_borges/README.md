# Day 14 — Borgesian map
**The map is the territory**

**Output:** `day14_borges/day14_borges.png`
**Run:** `uv run python -m day14_borges.map`

## The story

Borges' one-paragraph story *On Exactitude in Science* describes a map so
detailed that it covers the territory exactly. This day asks for a map that
approaches that joke. The answer is central Tacloban, drawn at building level:
**24,811 building footprints**, every one of them, in fine ink line work.

Tacloban is also the ground zero of Super Typhoon Yolanda (Haiyan), which
flattened the city in November 2013. Thirteen years later, on the anniversary
week when this series was made, the map shows the city rebuilt building by
building. The line work is not a memorial; it is evidence of the rebuild, and of
the volunteers who mapped it.

## Data

- **Buildings:** OSM `building=*` ways with full geometry in central Tacloban,
  bounding box 11.21–11.28°N, 124.97–125.04°E. 24,811 polygons after filtering.
- **Roads:** OSM primary, secondary, tertiary and residential highways in the
  same box, used as fine context lines. 1,028 ways.
- **Fetching:** Overpass API with `out geom`, cached as
  `data/tacloban_detail.gpkg`.
- **Licence:** OSM data © OpenStreetMap contributors, ODbL.

## Process

1. Fetch building polygons and roads once; cache the combined GeoPackage.
2. Split the layer into polygons and lines by geometry type.
3. Project to UTM 51N.
4. Draw roads first as thin brown lines, then buildings as **outlines only** —
   no fill — so overlapping footprints and courtyards remain visible.
5. Crop the view to the dense urban core (124.975–125.032°E, 11.218–11.268°N),
   which removes the sparse northern fragments and fills the frame with city.
6. Add a 1 km scale bar and a small "1 km" label in Baskerville.
7. Set the title in a serif face on cream paper, with the line "The map is the
   territory" and a short note about Yolanda and the rebuild.
8. Save at 200 dpi.

## Numbers on the map

- 24,811 building footprints.
- 1,028 road segments.
- Scale: 1 km bar; the "1:1" in the subtitle is conceptual, not literal.
- View covers roughly 5.5 × 5.5 km of central Tacloban.

## Data links

External sources used for this map (the local caches live in `data/`):

- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)
- [Overpass API](https://overpass-api.de/)
- [PAGASA](https://www.pagasa.dost.gov.ph/)

## What this map does not say

- OSM does not contain every building. The map is a census of mapped
  footprints, not of structures on the ground.
- Building outlines can be outdated, simplified or traced from old imagery.
  Some may have been destroyed or replaced since mapping.
- The "1:1" claim is a literary reference. The image is a projection at a
  printable scale, not a physically exact copy of the territory.
- The map has no attributes: no height, use, occupancy or construction date.
- The ink density is a visual effect; it is not a measure of damage or recovery.
