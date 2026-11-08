# Day 20 — Hexagons
**The bestagons of shaking**

**Output:** `day20_hexagons/day20_hexagons.png`
**Run:** `uv run python -m day20_hexagons.map`

## The story

Every earthquake map in this series has used points. Hexagons offer a different
question: not "where exactly?" but "how much per area?" Binning the last two
years of M5+ earthquakes into H3 cells turns the catalogue into a surface. The
Sarangani sequence fills one southern cell with 18 events; the east coast and
the trenches carry the rest.

The hexagon is also a visual pun. H3 is a real spatial index used by data teams,
and the challenge's "bestagons" prompt invites the joke. Under the joke is a
serious point: binning changes the story. A single M7.8 at the edge of a cell
can dominate a hexagon that covers 1,770 km² of sea and islands.

## Data

- **Earthquakes:** the cached USGS M5+ catalogue from Day 1
  (`data/ph_quakes.geojson`), clipped to the OSM country polygon. 133 events.
- **Hexagons:** Uber's H3 discrete global grid, resolution 4, average cell area
  about 1,770 km². The Python `h3` package provides
  `latlng_to_cell` and `cell_to_boundary`.
- **Land:** Natural Earth 1:10m (`data/ph_land.gpkg`).
- **Boundary:** OSM country relation (`data/ph_boundary.gpkg`).
- **Licences:** USGS public domain; OSM ODbL; Natural Earth public domain.

## Process

1. Load and clip the earthquake catalogue.
2. Convert each epicentre to an H3 cell at resolution 4 and count events per
   cell.
3. Build a polygon for each cell from `h3.cell_to_boundary`, close the ring, and
   create a GeoDataFrame in EPSG:4326.
4. Project the hexagons to Web Mercator so they align with the basemap.
5. Draw the national land silhouette first, then the hexagons coloured by event
   count with a dark-teal-to-red ramp. Cells with one event are dark; the
   18-event Sarangani cell is bright red.
6. Add the earthquake points at low opacity on top, sized by magnitude, so the
   reader can see where inside each hexagon the events actually sit.
7. Add a horizontal colour bar for events per hexagon and a title block that
   explains the resolution and the largest cell.
8. Save at 200 dpi.

## Numbers on the map

- 133 M5+ earthquakes.
- H3 resolution 4; about 1,770 km² per cell.
- Largest cell: 18 events, in the Sarangani area.
- Next largest: 17 and 13 events.

## Data links

External sources used for this map (the local caches live in `data/`):

- [USGS FDSN Event API](https://earthquake.usgs.gov/fdsnws/event/1/)
- [H3 geospatial index](https://h3geo.org/)
- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)

## What this map does not say

- The hexagon resolution is a choice. At resolution 3 the sequences merge; at
  resolution 5 the map fragments into small counts.
- Counts are not rates. A cell with many events may be a long aftershock
  sequence, not a higher long-term hazard.
- H3 cells are equal-area on the globe but their shapes distort in Web Mercator;
  the visual areas are not exactly equal on screen.
- The M5 threshold and catalogue completeness affect counts, especially
  offshore.
- A hexagon crossing land and sea is coloured by events anywhere inside it; the
  colour does not mean the land part shook.
