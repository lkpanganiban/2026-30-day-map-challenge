# Day 07 — 10 minute map
**Ten minutes from the water**

**Output:** `day07_tenmin/day07_tenmin.png`
**Run:** `uv run python -m day07_tenmin.map`

## The story

Metro Manila is a city built on a delta, crossed by the Pasig River, dozens of
esteros and a dense network of drains. After the 2026 monsoon floods, the
question "how far is the water?" stopped being rhetorical. This map answers it
at walking scale: from every 20 m cell of land, how many minutes on foot to the
nearest mapped river, creek, canal or drain?

The answer is uncomfortable in the other direction from what one might expect:
**91% of the city is within ten minutes of a mapped waterway, and the median is
about three minutes.** Water is not a distant hazard in Metro Manila; it is the
substrate the city is built on. The map was also an experiment in the challenge's
time constraint — a genuine quick build from cached OSM data.

## Data

- **Waterways:** OSM `waterway=river|stream|canal|drain|ditch` inside the Metro
  Manila box (120.90–121.10°E, 14.55–14.78°N), cached as
  `data/mm_waterways.gpkg` (from Day 8's fetch).
- **Land mask:** Natural Earth 1:10m land (`data/ph_land.gpkg`) to exclude the
  bay and adjacent sea.
- **Walking speed:** 80 m per minute, approximately 4.8 km/h, an easy pace.
- **Licence:** OSM data © OpenStreetMap contributors, ODbL.

## Process

1. Load and project the waterways to UTM 51N.
2. Build a 20 m grid over the waterway bounding box. The grid has roughly
   1.35 million land cells.
3. Rasterise the waterway lines onto that grid with `rasterio.features.rasterize`.
   A cell is "water" if a line crosses it.
4. Compute the Euclidean distance from every non-water cell to the nearest water
   pixel with `scipy.ndimage.distance_transform_edt`, using the 20 m cell size
   as the sampling distance. This produces a smooth distance surface rather than
   250 m blocks.
5. Convert metres to walking minutes at 80 m/min.
6. Rasterise the land polygons onto the same grid and mask out the sea.
7. Draw the result with a five-stop colour ramp from red (0 minutes) through
   yellow and pale blue to dark navy (10+ minutes). Values above ten minutes are
   clipped into the darkest colour.
8. Overlay dashed contour lines at 5 and 10 minutes with inline labels.
9. Add city names (Manila, Quezon City, Marikina, Taguig) with dark halos, a
   horizontal colour bar, the headline statistic, and the source footer.

## Numbers on the map

- 20 m analysis grid, about 1.35 million land cells.
- 91% of land cells within 10 minutes of mapped water.
- Median walking time: about 3 minutes.
- 80 m/min assumed walking speed.

## Data links

External sources used for this map (the local caches live in `data/`):

- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)
- [Overpass API](https://overpass-api.de/)
- [Natural Earth](https://www.naturalearthdata.com/)
- [SciPy distance_transform_edt](https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.distance_transform_edt.html)

## What this map does not say

- Distances are straight-line, not routed along streets. A river behind a wall
  or across an expressway may be close but unreachable in the stated time.
- OSM's drain and canal coverage is uneven. Unmapped esteros make some areas
  look farther from water than they are; over-mapped drainage can do the
  opposite.
- The land mask is a 1:10m coastline, so small reclaimed areas and fishponds may
  be misclassified.
- This is not a flood-extent map. Proximity to water is not the same as flood
  risk; elevation, tide, drainage capacity and rainfall all matter.
- The first version of this map had a vertically flipped land mask, which
  produced a wrong "49% over ten minutes" statistic. The corrected version is
  the one shipped here.
