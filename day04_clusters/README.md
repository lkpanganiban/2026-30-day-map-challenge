# Day 04 — Clusters
**Earthquakes travel in families**

**Output:** `day04_clusters/day04_clusters.png`
**Run:** `uv run python -m day04_clusters.map`

## The story

A big earthquake is rarely a single event. It opens a sequence: a mainshock,
then aftershocks that can continue for months along the same fault. Over two
years the Philippine catalogue contains several of these families, and they are
visually obvious once the points are grouped.

The map takes the same 133 M5+ events as Day 1 and links any two that lie within
50 km of each other. The result is 27 clusters, from isolated single events to
the 40-event Sarangani family that opened with the M7.8 on 8 June 2026. The
strongest five families are coloured and labelled; everything smaller is left
grey so the main sequences read first.

This is a deliberately naive clustering. It is spatial only — no time window, no
fault geometry, no magnitude dependence. That is the point: even the simplest
grouping recovers the sequences a reader remembers from the news.

## Data

- **Earthquakes:** the cached USGS FDSN catalogue from Day 1
  (`data/ph_quakes.geojson`), filtered to the OSM country polygon. 133 events.
- **Land:** Natural Earth 1:10m (`data/ph_land.gpkg`).
- **Boundary:** OSM country relation (`data/ph_boundary.gpkg`).
- **Licences:** USGS public domain; OSM ODbL; Natural Earth public domain.

## Process

1. Load the cached catalogue, read depth from the geometry's Z coordinate, and
   clip to the national boundary.
2. Implement single-linkage clustering with a tiny union-find structure. For
   every pair of events, compute the great-circle distance with the haversine
   formula; if it is under 50 km, union the two.
3. Assign each event the root of its union-find set as a cluster id. With 133
   points the O(n²) loop is trivial.
4. Sort clusters by size. The five largest (40, 20, 11, 7, 7) get fixed colours
   and human labels; all others are plotted as small grey dots.
5. Build a convex hull around each named family, buffer it slightly, and fill it
   at very low opacity to show the footprint of the sequence without hiding the
   points.
6. Plot points with magnitude-scaled area, plus a transparent larger copy for
   glow, exactly as in Day 1 so the series stays visually consistent.
7. Label each family at its centroid with its name, largest magnitude and count.
8. Project to Web Mercator, draw the national silhouette, and compose the title
   block and source line.

## Numbers on the map

- 133 events, 27 clusters.
- Sarangani: 40 events around the M7.8 of 8 June 2026.
- Moro Gulf: 20 events, largest M5.9.
- Cebu: 11 events around the M6.9 of 30 September 2025.
- Davao Oriental: 7 events around the M7.4 of October 2025.
- Surigao: 7 events, largest M6.0.
- Six events remain singletons.

## Data links

External sources used for this map (the local caches live in `data/`):

- [USGS FDSN Event API](https://earthquake.usgs.gov/fdsnws/event/1/)
- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)
- [Natural Earth](https://www.naturalearthdata.com/)

## What this map does not say

- The 50 km threshold is a choice. A larger radius merges neighbouring
  sequences into a single chain; a smaller one fragments real aftershock zones.
- There is no time constraint. Two unrelated events years apart but within
  50 km are grouped as one family.
- Clusters are not faults. They are clouds of epicentres, and epicentre
  uncertainty can move a point by tens of kilometres offshore.
- The M5 catalogue is incomplete for small aftershocks, so family sizes are
  minima, not true aftershock counts.
