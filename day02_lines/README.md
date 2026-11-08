# Day 02 — Lines
**Nine storms entered the ring**

**Output:** `day02_lines/day02_lines.png`
**Run:** `uv run python -m day02_lines.map`

## The story

The 2026 western North Pacific season produced nine tropical cyclones that
entered the Philippine Area of Responsibility (PAR) in the IBTrACS archive used
here. Two of them carried the season: **Champi**, locally named **Rosal**, which
became the strongest cyclone of 2026 by maximum sustained wind, and **Bavi**,
locally **Inday**, which left 20 people dead in July after its passage and the
enhanced southwest monsoon.

The map is drawn during the week that **Kalmaegi — Tino** — made landfall in
southern Leyte and crossed Cebu and Negros. Tino is deliberately absent from the
tracks: the official best-track archive had not yet processed it when this map
was made. That absence became Day 18.

Lines are the right geometry for a track because a typhoon is a path through
time, not a dot. Colour along each line carries wind speed, so the reader can
see where a storm intensified, where it peaked, and where it weakened.

## Data

- **Tracks:** IBTrACS v04r01, `ibtracs.last3years.list.v04r01.csv`, NOAA/NCEI,
  cached as `data/ibtracs_last3years.csv`. Each row is a 6-hourly (or 3-hourly
  near landfall) position with `LAT`, `LON`, `USA_WIND`, `ISO_TIME`, `NAME`.
- **Filtering:** season 2026, named storms only, and only storms with at least
  one position inside a PAR test box (114.5–127°E, 4.5–22°N). Nine storms
  survive: Bavi, Champi, Maysak, Mekkhala, Nokaen, Noul, Peilou, Penha, Saudel.
- **Land:** Natural Earth 1:10m clipped to the western Pacific
  (`data/wp_land.gpkg`).
- **Philippine boundary:** OSM country relation (`data/ph_boundary.gpkg`),
  intersected with land to highlight the national territory.
- **PAR outline:** a simplified polygon with vertices at 115°E/5°N, 115°E/15°N,
  120°E/21°N, 120°E/25°N, 135°E/25°N, 135°E/5°N. It is schematic.

## Process

1. Load the cached IBTrACS CSV, skipping its second header row (units), and
   convert `LAT`, `LON` and `USA_WIND` to numbers.
2. Keep named 2026 storms, then test each storm for any point inside the PAR
   box. This is a rough entry test, not the official PAGASA polygon.
3. Sort each track by `ISO_TIME` so line segments connect in chronological
   order.
4. Project to EPSG:3857 and build segment lists. A `LineCollection` is used
   rather than a single `plot`, because each segment needs its own colour.
5. Colour by `USA_WIND` in knots: under 64 kt blue, 64–95 kt yellow, 96–136 kt
   orange, 137 kt and above red. A wider, very transparent duplicate of each
   segment adds the glow.
6. Draw land in two tones: the wider western Pacific faint, the Philippine
   territory brighter, so the country reads immediately without a legend.
7. Draw the schematic PAR boundary as a dashed line and label it once.
8. Place each storm name at its strongest point inside the frame, with a
   paper-coloured halo. Bavi and Champi carry their local names
   (`Bavi · Inday`, `Champi · Rosal`).
9. Add a legend of wind categories with counts and a source footer.

## Numbers on the map

- Nine named storms entered PAR in the archive.
- Champi peaked at 159 kt, the strongest of 2026.
- Bavi peaked at 154 kt and was linked to 20 deaths in July.
- The track colours also show that some storms peaked well east of the
  Philippines before recurving.

## Data links

External sources used for this map (the local caches live in `data/`):

- [IBTrACS product page](https://www.ncei.noaa.gov/products/international-best-track-archive)
- [IBTrACS CSV access](https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/)
- [PAGASA](https://www.pagasa.dost.gov.ph/)
- [Natural Earth](https://www.naturalearthdata.com/)
- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)

## What this map does not say

- IBTrACS is a best-track archive, not a real-time warning product. Its
  6-hourly sampling smooths out loops, eyewall replacements and short-lived
  intensification.
- The PAR outline is a simplified six-vertex polygon, not the legal PAGASA
  boundary.
- "Entered PAR" is tested against a bounding box, not the official polygon, so
  a storm skimming the edge may be included or excluded.
- Kalmaegi/Tino is missing because the archive lagged the event. Absence here
  means "not yet processed", not "did not happen".
- Wind speeds are agency estimates; different agencies can disagree by tens of
  knots for the same storm.
