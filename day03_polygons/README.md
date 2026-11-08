# Day 03 — Polygons
**Inside the permanent danger zone**

**Output:** `day03_polygons/day03_polygons.png`
**Run:** `uv run python -m day03_polygons.map`

## The story

On 30 October 2026 Mayon Volcano produced a moderately explosive eruption that
sent an ash column roughly 3,000 metres above the summit and forced 2,041
people to evacuate from Tabaco City, Camalig and Ligao City. The 6 km Permanent
Danger Zone is the line the state draws around the crater; this map asks the
simplest possible question of it: **what is inside?**

Every building footprint that OpenStreetMap holds around Mayon is drawn as a
dot. The zone is a real polygon on top of them. The result is not a hazard
assessment — it is a reminder that a danger zone is a polygon, but evacuation
is a list of addresses. 1,363 mapped buildings sit inside the 6 km line.

## Data

- **Buildings:** OSM `building=*` ways around Mayon, fetched from the Overpass
  API with `out center` (one point per building) for the box
  13.08–13.40°N, 123.50–123.88°E. 140,694 building centres were returned and
  cached as `data/mayon_buildings.json`.
- **Roads and places:** a second Overpass query returns highways
  (primary/secondary/tertiary) and `place=city|town|village|hamlet` nodes,
  cached as `data/mayon_places.gpkg`.
- **Summit:** 13.2573°N, 123.6855°E, from the published Mayon coordinates.
- **Zone:** a geodesic 6,000 m buffer around the summit, computed in
  EPSG:32651 (UTM zone 51N).
- **Event facts:** 30 October 2026 eruption, 3,000 m ash column, 2,041 evacuees,
  from PHIVOLCS and the Albay provincial government reporting.
- **Licence:** OSM data © OpenStreetMap contributors, ODbL.

## Process

1. Fetch building centres and context once; cache both responses.
2. Convert the JSON elements to a GeoDataFrame with the project's small
   Overpass helper (`osm.py`).
3. Project everything to UTM 51N so buffer distances are metres, not degrees.
4. Buffer the summit by 6,000 m. This is a circle, not PHIVOLCS's official
   hazard polygon — an honest approximation made explicit in the footer.
5. Count buildings whose centre falls inside the buffer with a spatial
   predicate. **1,363 of 140,694** are inside.
6. Plot roads faintly, buildings as small slate dots, then the zone as a
   translucent red fill with a dashed edge and a soft outer glow.
7. Label the towns that matter in the news story (Tabaco, Malilipot, Bacacay,
   Santo Domingo, Ligao, Guinobatan, Camalig, Daraga, Legazpi) with paper
   halos so they remain legible over dense settlement.
8. Mark the summit with a triangle and add the zone label inside the circle.
9. Crop the axes inside the building extract so the rectangular data boundary
   never appears as a hard edge.
10. Compose the title, subtitle and source line on the series' dark paper.

## Numbers on the map

- 140,694 building footprints in the extract.
- 1,363 inside the 6 km zone.
- 2,041 people evacuated after the 30 October 2026 eruption.
- Ash column approximately 3,000 m.

## Data links

External sources used for this map (the local caches live in `data/`):

- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)
- [Overpass API](https://overpass-api.de/)
- [PHIVOLCS](https://www.phivolcs.dost.gov.ph/)
- [Smithsonian GVP: Mayon](https://volcano.si.edu/volcano.cfm?vn=273030)

## What this map does not say

- OSM building completeness is uneven. The count is a lower bound on what is
  mapped, not a census, and dense informal settlements may be under-mapped.
- A circular buffer is not the official PHIVOLCS hazard polygon. Real
  pyroclastic-flow, lahar and ashfall hazard zones are direction-dependent.
- Building centres are points; a large building straddling the line is counted
  by its centre.
- The map does not estimate how many people live in those buildings. Population
  would require a separate, much more uncertain dataset.
