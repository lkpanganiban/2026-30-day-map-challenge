# Day 11 — Senses: Sound
**Where the city is quiet**

**Output:** `day11_sound/day11_sound.png`
**Run:** `uv run python -m day11_sound.map`

## The story

Metro Manila is one of the loudest urban areas in Southeast Asia: jeepneys,
motorcycles, expressways, construction, generators and videoke. The challenge
asks how to map a soundscape. Without a calibrated noise model or a network of
sound sensors, the honest proxy is **distance from major roads**.

This map treats distance from the nearest motorway, trunk, primary or secondary
road as a rough traffic-noise proxy. The bright areas are quiet — far from the
fast roads — and the dark veins are the road network. What survives as quiet in
the city is revealing: watersheds, campuses, golf courses, large institutional
compounds and the gaps between expressways. The map labels La Mesa and the
Marikina Watershed because they are the two largest uninterrupted quiet areas in
the frame.

## Data

- **Roads:** OSM `highway=motorway|trunk|primary|secondary` in the Metro Manila
  box (120.85–121.10°E, 14.45–14.78°N), fetched with geometry and cached as
  `data/mm_roads.gpkg`.
- **Land mask:** Natural Earth 1:10m land (`data/ph_land.gpkg`), cropped to the
  road extent.
- **Derived metric:** Euclidean distance from each 25 m grid cell to the nearest
  major-road pixel, clipped at 900 m.
- **Licence:** OSM data © OpenStreetMap contributors, ODbL.

## Process

1. Load and project the major-road lines to UTM 51N.
2. Build a 25 m grid over the road bounding box.
3. Rasterise the roads onto the grid with `rasterio.features.rasterize`.
4. Compute distance to the nearest road pixel with
   `scipy.ndimage.distance_transform_edt`, sampling at 25 m.
5. Clip distances at 900 m. Anything beyond that is treated as equally quiet;
   otherwise the rural fringe would dominate the colour scale.
6. Rasterise land polygons onto the same grid so the sea is left blank.
7. Map distance to a five-stop ramp from dark blue-green (near a road) to warm
   cream (900 m away). Brighter means quieter.
8. Add city labels (Manila, Quezon City, Marikina) and two landscape labels
   (La Mesa, Marikina Watershed) with dark halos.
9. Add a horizontal colour bar labelled "metres from the nearest major road ·
   brighter = quieter", plus the title and source footer.

## Numbers on the map

- 25 m analysis grid.
- Distances clipped at 900 m.
- Four road classes included: motorway, trunk, primary, secondary.
- Two named quiet landscapes: La Mesa and the Marikina Watershed.

## Data links

External sources used for this map (the local caches live in `data/`):

- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)
- [Overpass API](https://overpass-api.de/)
- [WHO Environmental Noise Guidelines](https://www.who.int/europe/publications/i/item/9789289053563)

## What this map does not say

- Road distance is not noise. A quiet residential street can be louder than a
  distant expressway; topography, buildings, trees and time of day all change
  propagation.
- The map uses only major roads. Tertiary streets, jeepney routes, construction
  sites, airports and industrial sources are omitted, so some "quiet" areas may
  be noisy in reality.
- OSM road completeness varies. Sparse mapping on the eastern fringe can make
  rural areas look quieter than they are.
- The label positions are approximate landscape centroids, not measured
  quietest points.
- The colour scale is a visual index, not decibels. No calibration data were
  used.
