# Day 12 — Power
**The grid, and the plant we never turned on**

**Output:** `day12_power/day12_power.png`
**Run:** `uv run python -m day12_power.map`

## The story

In the week this map was made, Typhoon Tino cut power across Cebu and Negros,
adding a electricity outage to an island region still recovering from earlier
disasters. A transmission map is therefore not an abstraction: it is the
infrastructure that has to carry the recovery.

The map draws every transmission line OpenStreetMap knows in the Philippines,
coloured by voltage, with substations as small points. In the middle of the
network sits the **Bataan Nuclear Power Plant** — completed in 1984, never
operated, and still the country's most famous piece of unused infrastructure.
The star is deliberately the only red object that is not a 500 kV line.

## Data

- **Transmission lines:** OSM `power=line` ways with full geometry across the
  Philippine bounding box, fetched from Overpass and cached as
  `data/ph_powerlines.gpkg`. 3,737 lines.
- **Substations:** OSM `power=substation` nodes and ways, cached in
  `data/ph_power.gpkg`.
- **Voltage:** the OSM `voltage` tag, in volts, converted to numeric. Counts by
  band: 500 kV 154, 230 kV 913, 138 kV 442, 115 kV 639, 69 kV 691; smaller and
  untagged lines are drawn in grey.
- **Bataan Nuclear Power Plant:** 14.6294°N, 120.4678°E.
- **Land:** Natural Earth 1:10m (`data/ph_land.gpkg`).
- **Licence:** OSM data © OpenStreetMap contributors, ODbL.

## Process

1. Fetch power lines with `out geom` (an earlier query using `out center`
   returned only midpoints, which is useless for a network map).
2. Fetch substations separately and filter to `power=substation`.
3. Convert the voltage tag to a number and draw five bands with fixed colours:
   red for 500 kV, orange for 230 kV, yellow for 138 kV, blue for 115 kV,
   slate for 69 kV. Lines below 69 kV or without voltage are drawn thin and
   grey.
4. Plot the national land silhouette, then the lines, then substations as small
   cream points.
5. Mark the Bataan plant with a red star and a two-line label: "completed 1984 ·
   never operated".
6. Build a legend with the voltage bands and their line counts, computed from
   the same filters used to draw them.
7. Set the extent to 114–127°E, 4.2–19.5°N, which keeps Luzon, the Visayas and
   most of Mindanao in frame without the empty ocean to the north.
8. Compose the title, the Tino context, the Bataan line, and the source footer.

## Numbers on the map

- 3,737 transmission lines.
- Voltage bands: 154 lines at 500 kV, 913 at 230 kV, 442 at 138 kV, 639 at
  115 kV, 691 at 69 kV.
- Bataan Nuclear Power Plant completed 1984, never operated.
- Tino cut power across Cebu and Negros in November 2026.

## Data links

External sources used for this map (the local caches live in `data/`):

- [OSM power networks wiki](https://wiki.openstreetmap.org/wiki/Power_networks)
- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)
- [IAEA PRIS: Philippines](https://pris.iaea.org/PRIS/CountryStatistics/CountryDetails.aspx?current=PH)
- [Department of Energy (PH)](https://doe.gov.ph/)

## What this map does not say

- OSM's power network is incomplete and uneven. Lines are mapped in some regions
  and missing in others; the map is a map of mapped infrastructure, not of the
  physical grid.
- Voltage tags can be missing, rounded or wrong. The legend counts depend on
  the tag, and 1% bands are used to group values.
- There is no outage, capacity, generation or demand data here. The Tino
  sentence is context from reporting, not a spatial overlay.
- The Bataan plant's status is summarised in one line; the political and
  technical history is far more complicated than "never operated" suggests.
- Lines are drawn as straight segments between OSM vertices; they are not
  electrical flow paths.
