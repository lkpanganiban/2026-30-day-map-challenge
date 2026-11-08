# Day 24 — Network
**Two ways off the spine**

**Output:** `day24_network/day24_network.png`
**Run:** `uv run python -m day24_network.map`

## The story

Cebu is a long, narrow island. Its population and its primary road network run
along the coast, with a mountainous spine in the middle. From Cebu City, there
are two obvious ways out: north along the coast toward Daanbantayan, and south
along the coast toward Santander. There is no equivalent inland alternative for
most of the island.

When Typhoon Tino crossed Cebu in November 2026, the coastal road was the
corridor that had to keep working. This map draws the primary network and
computes the shortest path from Cebu City to each tip. The routes are almost the
same length — 120 km north, 126 km south — and both hug the coast. The network
is efficient and exposed at the same time.

## Data

- **Roads:** OSM `highway=trunk|primary|secondary|tertiary` ways in the Cebu box
  (123.3–124.3°E, 9.3–11.4°N), fetched with `out geom` and cached as
  `data/cebu_roads.gpkg`. 9,919 line segments.
- **Graph:** built directly from the line vertices, with edges weighted by
  great-circle distance in UTM 51N. About 200,000 nodes.
- **Endpoints:** Cebu City (123.893°E, 10.315°N), Daanbantayan (124.020°E,
  11.200°N), Santander (123.420°E, 9.420°N).
- **Land:** Natural Earth 1:10m (`data/ph_land.gpkg`).
- **Licence:** OSM data © OpenStreetMap contributors, ODbL.

## Process

1. Load and project the Cebu road network to UTM 51N.
2. Build a NetworkX graph from every consecutive pair of vertices in every
   LineString. Nodes are rounded to 0.1 m so shared OSM junctions connect.
3. Snap the three cities to their nearest graph nodes.
4. Compute the shortest path with Dijkstra (`weight="weight"`) from Cebu City to
   each tip and sum the edge lengths.
5. Draw the full network as thin slate lines, then overlay the north route in
   red and the south route in blue, each with a transparent glow.
6. Mark the three cities with cream dots and labels.
7. Add a legend with the route lengths, placed in the empty sea at upper left.
8. Compose the title, the "no inland alternative" framing, and the source
   footer.

## Numbers on the map

- 9,919 road segments, about 200,000 graph nodes.
- Cebu City → Daanbantayan: 120 km.
- Cebu City → Santander: 126 km.

## Data links

External sources used for this map (the local caches live in `data/`):

- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)
- [Overpass API](https://overpass-api.de/)
- [NetworkX](https://networkx.org/)

## What this map does not say

- Only trunk, primary, secondary and tertiary roads are included. Barangay
  roads, trails and ferry links are not, so the "shortest" path is shortest
  within this network, not necessarily the real drive.
- The graph connects roads where OSM vertices share coordinates. Small mapping
  gaps can disconnect a route or push it onto a detour.
- The routes are shortest paths, not traffic-aware routes. They ignore
  one-ways, closures, landslides, checkpoints and ferry schedules.
- The map does not show Tino's damage or closures. The "when the coast closed"
  line is context; no closure data are overlaid.
- Distance is along the line geometry, not elevation-aware, so fuel and travel
  time are not represented.
