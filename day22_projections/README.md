# Day 22 — Projections
**The shape you choose**

**Output:** `day22_projections/day22_projections.png`
**Run:** `uv run python -m day22_projections.map`

## The story

Every flat map of the Philippines is an argument about what to preserve.
Mercator keeps bearings and shapes useful for navigation, but inflates area as
you move away from the equator. Equal Earth keeps areas honest, at the cost of
bending shapes. An azimuthal equidistant projection centred on Manila keeps
distance from one point true in every direction, and distorts everything else.

This map puts the same archipelago in all three frames side by side. The
differences are subtle because the Philippines sits near the equator, where
Mercator's distortion is smallest. That is itself the point: projection choice
matters most where you are not looking. The azimuthal panel adds 500, 1,000 and
1,500 km rings, turning the projection into a distance map from the capital.

## Data

- **Land:** Natural Earth 1:10m, clipped to 114–128°E, 4–22°N
  (`data/ph_land.gpkg`).
- **Boundary:** OSM country relation (`data/ph_boundary.gpkg`), drawn dashed as
  the outer limit of territory.
- **Projections:**
  - Mercator, EPSG:3857.
  - Equal Earth, EPSG:8857.
  - Azimuthal equidistant, `+proj=aeqd +lat_0=14.6 +lon_0=121 +datum=WGS84 +units=m`.
- **Licences:** Natural Earth public domain; OSM ODbL.

## Process

1. Load land and boundary in EPSG:4326 and clip land to the Philippine box.
2. Create a 1 × 3 panel figure with a dark background.
3. For each projection, reproject the land and boundary with GeoPandas
   `to_crs`, plot land as a slate fill with a thin edge, and draw the national
   boundary dashed.
4. Set each panel's limits to the projected land bounds and force equal aspect
   so the shapes are comparable.
5. In the azimuthal panel, draw dashed circles at 500, 1,000 and 1,500 km from
   the projection origin (Manila at 14.6°N, 121°E). Because the projection is
   centred on that point, the circles are true distances.
6. Add each projection's name above its panel and a short note below it
   describing what it preserves and what it bends.
7. Compose the title, the three-line argument about preservation, and the source
   footer.

## Numbers on the map

- Three projections of the same national geometry.
- Three distance rings: 500, 1,000, 1,500 km.
- Projection centre: 14.6°N, 121°E (Manila).

## Data links

External sources used for this map (the local caches live in `data/`):

- [Natural Earth](https://www.naturalearthdata.com/)
- [EPSG:3857 Mercator](https://epsg.io/3857)
- [EPSG:8857 Equal Earth](https://epsg.io/8857)
- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)

## What this map does not say

- The panels look similar because the Philippines is near the equator. A global
  or high-latitude comparison would make the differences much larger.
- The azimuthal projection preserves distance only from its centre, not between
  arbitrary pairs of points.
- The "correct" projection depends on the question: navigation, area, distance,
  shape or a compromise.
- The national boundary is a simplified OSM relation, not a legal maritime
  boundary.
- Land is from Natural Earth 1:10m, which omits many small islands; the same
  omission appears in all three panels, so it does not affect the comparison but
  does affect the portrait of the country.
