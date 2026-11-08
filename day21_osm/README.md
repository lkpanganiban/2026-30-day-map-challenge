# Day 21 — OpenStreetMap
**Every hospital the crowd knows**

**Output:** `day21_osm/day21_osm.png`
**Run:** `uv run python -m day21_osm.map`

## The story

On 30 September 2025 a magnitude 6.9 earthquake struck the sea between Cebu and
Bohol. Hospitals in Cebu City, Danao, Lapu-Lapu and the surrounding towns were
within the shaking radius. Less than a year later, Typhoon Tino cut roads across
the same islands. In both cases, the first operational question is the same:
**which health facilities are near, and are they still reachable?**

OpenStreetMap is the map responders and volunteers can edit in real time. This
day is a celebration of that layer: every `amenity=hospital` mapped in the
country, with the ones near the Cebu earthquake highlighted. It is not a health
system inventory. It is a map of what the crowd has recorded.

## Data

- **Health facilities:** OSM `amenity=hospital` nodes and ways across the
  Philippine bounding box, fetched with `out center` and cached as
  `data/ph_hospitals.gpkg`. 2,029 facilities.
- **Earthquakes:** the cached USGS catalogue (`data/ph_quakes.geojson`). The
  Cebu event is selected as the largest magnitude in the box 10.7–11.6°N,
  123.6–124.7°E: M6.9, 30 September 2025.
- **Buffer:** 50 km around that epicentre, computed in UTM 51N.
- **Land:** Natural Earth 1:10m (`data/ph_land.gpkg`).
- **Licence:** OSM data © OpenStreetMap contributors, ODbL.

## Process

1. Fetch hospitals once, keeping only the centre point of each way so the map
   can be drawn as a point layer.
2. Load the earthquake catalogue, clip to the national boundary, and select the
   Cebu event.
3. Project the epicentre to UTM 51N and build a 50 km buffer.
4. Count hospital points inside the buffer. **16 hospitals** fall within 50 km.
5. Draw the national land silhouette, hospitals as small cream crosses, and the
   quake buffer as a dashed red circle.
6. Mark the epicentre with a red star and a two-line label: magnitude/date and
   the hospital count.
7. Compose the title, the OSM-day framing, and a source footer that credits
   contributors and USGS.

## Numbers on the map

- 2,029 mapped health facilities.
- 16 inside 50 km of the M6.9 Cebu earthquake.
- Epicentre: M6.9, 30 September 2025.

## Data links

External sources used for this map (the local caches live in `data/`):

- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)
- [Overpass API](https://overpass-api.de/)
- [USGS FDSN Event API](https://earthquake.usgs.gov/fdsnws/event/1/)

## What this map does not say

- OSM hospital coverage is uneven. Dense cities are well mapped; remote
  municipalities, birthing homes, clinics and barangay health stations are
  often missing. The 2,029 is a lower bound.
- A hospital point does not mean the facility was open, staffed or undamaged
  after the earthquake or the typhoon.
- The 50 km radius is a simple distance, not travel time. Roads, ferries and
  bridges matter.
- `amenity=hospital` includes both large hospitals and small facilities; the
  tag is not a capacity measure.
- The map does not show evacuation centres, clinics, pharmacies or field
  hospitals.
