# Day 09 — Urban-rural
**Where the city ends**

**Output:** `day09_urbanrural/day09_urbanrural.png`
**Run:** `uv run python -m day09_urbanrural.map`

## The story

Metro Manila is usually drawn as a single urban blob. At the scale of land use,
however, it is a patchwork: vast residential polygons, a belt of industrial
land, commercial cores, and — at the edge — the farmland, forest and meadow that
the city has not yet swallowed. The 2026 monsoon floods pushed hardest against
that edge, where subdivisions meet floodplains and the drainage is least
engineered.

This map shows the land-use polygons that OpenStreetMap mappers have drawn
across Metro Manila and its immediate fringe. It is a map of categories, not of
people: each colour is a claim someone made about how the land is used.

## Data

- **Land use:** OSM `landuse=*` ways in the box 14.45–14.80°N,
  120.85–121.20°E, fetched with `out geom`. 7,063 polygons across seven classes:
  residential, commercial, industrial, farmland, forest, meadow and orchard.
- **Roads:** OSM motorway/trunk/primary/secondary ways in the same box, used as
  faint context.
- **Derived areas:** computed from the projected polygon geometry in UTM 51N and
  summed by class.
- **Licence:** OSM data © OpenStreetMap contributors, ODbL.

## Process

1. Fetch land-use polygons and major roads once; cache as GeoPackages.
2. Deduplicate tag columns that differ only in case (`FIXME` / `fixme`), which
   otherwise makes the GeoPackage writer fail.
3. Project to UTM 51N and compute each polygon's area in square kilometres.
4. Sum area by `landuse` class for the legend.
5. Draw roads first in a dark slate, then each land-use class with a fixed
   colour: sand for residential, red for commercial, purple for industrial,
   olive for farmland, dark green for forest, pale green for meadow, green for
   orchard.
6. Add a legend in the empty bay area at upper left, with the class name and its
   total area, and force the legend text to the series font/colour.
7. Crop the axes to the land-use bounding box so the map fills the frame.
8. Compose the title, the three headline counts and a short line connecting the
   green fringe to the 2026 floods.

## Numbers on the map (areas from OSM polygons)

- Residential: 113 km².
- Industrial: 22 km².
- Commercial: 13 km².
- Farmland: 10 km².
- Forest: 4 km².
- Meadow: 1 km².
- Orchard: 1 km².
- Seven classes, 7,063 polygons.

## Data links

External sources used for this map (the local caches live in `data/`):

- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)
- [Overpass API](https://overpass-api.de/)

## What this map does not say

- Land-use polygons are mapper interpretations, not cadastral records. Coverage
  is dense in some cities and sparse in others.
- The areas are planimetric polygon areas, not official statistics. They are
  useful for comparing classes on this map, not for quoting as municipal totals.
- The fringe box cuts through neighbouring provinces; some polygons belong to
  Rizal, Cavite, Laguna or Bulacan rather than Metro Manila proper.
- The map does not show population, building height or density. A large
  residential polygon can be a subdivision, a informal settlement or an
  industrial camp.
- The line about floods is context, not a spatial analysis: the map does not
  overlay flood extents.
