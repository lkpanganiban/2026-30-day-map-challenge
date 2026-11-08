# Day 18 — NULL
**The storm that isn't here**

**Output:** `day18_null/day18_null.png`
**Run:** `uv run python -m day18_null.map`

## The story

The 2026 theme "NULL" has no description. This map takes the prompt literally:
what is missing from the data?

The grey lines are every named 2026 typhoon track in the IBTrACS archive used
for this series. The red circle in the Visayas is empty. That is where
**Kalmaegi — Tino** made landfall in southern Leyte on 4 November 2026 and cut
across Cebu and Negros, killing more than a hundred people and leaving over a
million households without power. Tino is not in the archive because the archive
was compiled before the event was processed.

The point is not that the storm is unknown. It is that a NULL in a dataset is
often a statement about the pipeline — latency, processing, revision — rather
than about the world. The damage is already real; the data is late.

## Data

- **Tracks:** IBTrACS v04r01 last-three-years CSV, cached as
  `data/ibtracs_last3years.csv`, filtered to named 2026 storms that entered the
  PAR test box. Nine tracks.
- **Archive timestamp:** the IBTrACS file used was last modified 7 November 2026.
- **Tino location:** landfall in southern Leyte and crossing of Cebu/Negros;
  the circle is centred on 123.65°E, 10.55°N with a 170 km radius.
- **Land:** Natural Earth 1:10m (`data/wp_land.gpkg`), with Philippine land
  highlighted.
- **Boundary:** OSM country relation (`data/ph_boundary.gpkg`).
- **Licences:** IBTrACS NOAA/NCEI; OSM ODbL; Natural Earth public domain.

## Process

1. Load the cached tracks and keep named 2026 storms with a point inside the
   PAR test box.
2. Project to Web Mercator and draw each track as a thin grey line at 55%
   opacity. Deliberately mute the archive so the absence is the bright object.
3. Draw the Philippine land silhouette more brightly than the surrounding
   western Pacific land.
4. Draw a dashed red circle around the Tino crossing area.
5. Place a large red `NULL` at the centre of the circle, with a two-line label
   naming Kalmaegi/Tino and the date.
6. Set the national extent, compose the title and a subtitle that explains the
    distinction between "no storm" and "not yet data".
7. Save at 200 dpi.

## Numbers on the map

- Nine archived 2026 tracks in grey.
- One missing storm: Kalmaegi/Tino, 4 November 2026.
- 170 km schematic circle.
- Archive compiled 7 November 2026.

## Data links

External sources used for this map (the local caches live in `data/`):

- [IBTrACS product page](https://www.ncei.noaa.gov/products/international-best-track-archive)
- [PAGASA](https://www.pagasa.dost.gov.ph/)
- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)

## What this map does not say

- The archive is not wrong; it is incomplete for the most recent event. A later
  IBTrACS release will contain Tino.
- The circle marks a known landfall area, not a reconstructed track. No
  positions are invented.
- "More than a hundred dead" and the outage figures came from reporting in the
  days after landfall and were still being revised; they are context, not
  values in the dataset.
- A NULL in a best-track file does not mean the storm was unobserved. Satellites,
  radars and warnings observed it in real time; only the curated archive lagged.
