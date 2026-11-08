# Day 06 — Vintage
**Mapa del Volcan Mayon**

**Output:** `day06_vintage/day06_vintage.png`
**Run:** `uv run python -m day06_vintage.map`

## The story

In 1814 Mayon produced one of its most destructive eruptions. Pyroclastic flows
and lahars buried the town of Cagsawa; only the church bell tower survived, and
it still stands as the icon of Albay. The mountain that did that is the same
mountain that erupted again on 30 October 2026.

For "Vintage", the map dresses current OpenStreetMap detail in the visual
language of a nineteenth-century mapa: cream paper, sepia ink, a double rule
border, a serif cartouche, a compass rose and italic place names. The data is
modern; the grammar is old. The result is not a historical reconstruction but a
visual argument about continuity — the same cone, the same towns, the same
danger.

## Data

- **Buildings:** 140,694 OSM building centres around Mayon
  (`data/mayon_buildings.json`).
- **Roads and towns:** OSM highways and place nodes
  (`data/mayon_places.gpkg`).
- **Summit:** 13.2573°N, 123.6855°E.
- **Cagsawa:** 13.1647°N, 123.6947°E, marked as a cross.
- **Zone:** 6 km buffer around the summit, projected to UTM 51N.
- **Event context:** the 1814 eruption and the 30 October 2026 eruption.
- **Licence:** OSM data © OpenStreetMap contributors, ODbL.

## Process

1. Load the cached OSM building centres, roads and town nodes; project to UTM
   51N.
2. Choose a paper palette (`#e9dcbf` paper, `#4a3826` ink, `#9b3a2a` accent)
   and a serif family (Baskerville) for every label.
3. Draw buildings as very small, low-opacity ink specks. At this scale they read
   as settlement texture rather than individual structures, which is the
   intended vintage effect.
4. Draw primary, secondary and tertiary roads in a faded brown, then the 6 km
   zone as a dashed red circle with a faint wash.
5. Label the towns in upper case with paper-coloured halos so the names remain
   legible over the settlement texture.
6. Mark the summit as a triangle with a two-line label (`VOLCAN MAYON`,
   `2,462 m`), and Cagsawa as a cross labelled `Cagsawa (1814)`.
7. Add a compass rose and a double-rule border drawn in figure coordinates.
8. Set the title in a centred cartouche, with the Spanish-style subtitle
   `y de sus contornos · Albay, Islas Filipinas` and an English line about the
   1814 eruption.
9. Save at 200 dpi on the paper background.

## Numbers on the map

- 6 km danger-zone radius.
- Mayon summit elevation: 2,462 m.
- Cagsawa marker: 1814 eruption.
- 140,694 building footprints in the underlying data.

## Data links

External sources used for this map (the local caches live in `data/`):

- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)
- [Overpass API](https://overpass-api.de/)
- [Smithsonian GVP: Mayon](https://volcano.si.edu/volcano.cfm?vn=273030)
- [PHIVOLCS](https://www.phivolcs.dost.gov.ph/)

## What this map does not say

- This is not a historical map. It uses present-day OSM geometry restyled to
  look old; roads, buildings and town extents are 2026 data.
- The 6 km circle is a modern hazard buffer, not an 1814 flow boundary.
- The 1814 event is represented by a single marker and a line of text; no
  attempt is made to reconstruct the actual pyroclastic-flow footprint.
- Baskerville may fall back to another serif on machines that do not have it.
