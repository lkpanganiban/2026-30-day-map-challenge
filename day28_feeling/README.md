# Day 28 — Senses: Feeling
**How the shaking felt**

**Output:** `day28_feeling/day28_feeling.png`
**Run:** `uv run python -m day28_feeling.map`

## The story

Seismographs record ground motion. People record fear. The USGS "Did You Feel
It?" programme collects both: anyone can report what they felt, where, and how
strong it was. For the M7.8 Sarangani earthquake of 8 June 2026, 597 responses
came from 144 places, as far as 2,850 km away.

This map turns those reports into a community decimal intensity (CDI) surface.
Near the epicentre the grid reaches 9.1 — violent shaking. Across Mindanao it
drops to 6, 5, 4. In Luzon it is mostly 2–4: felt, but as a sway rather than a
threat. The same earthquake, many feelings. That is the point of the day.

## Data

- **Event:** USGS event `us7000srb1`, M7.8, 8 June 2026, 25 km SW of Kablalan,
  Sarangani.
- **Product:** `dyfi`, specifically `dyfi_geo_10km.geojson` (10 km gridded
  intensity) and `dyfi_zip.geojson` (response counts by place).
- **Grid:** 188 polygons after cleaning unclosed rings in the source GeoJSON.
- **Responses:** 597 reports from 144 places; maximum reported distance
  2,850 km; maximum CDI 9.1.
- **Land:** Natural Earth 1:10m (`data/ph_land.gpkg`).
- **Licence:** USGS data, public domain.

## Process

1. Query the USGS event endpoint for `us7000srb1` and locate the `dyfi` product.
2. Download the gridded GeoJSON from the product's content URL (the event-page
   URL returns HTML, not GeoJSON).
3. The source polygons have unclosed rings, so GeoPandas refuses to read them.
   Parse the JSON manually, close each ring by repeating its first coordinate,
   and build Shapely polygons. 188 cells survive.
4. Load the ZIP-level reports to compute the headline totals and maximum
   distance.
5. Project the gridded cells to Web Mercator and plot them with a yellow-to-red
   ramp from CDI 1 to 10, at 80% opacity.
6. Draw the national land silhouette beneath, then mark the epicentre with a
   red star and a label.
7. Add a horizontal colour bar explaining CDI, and compose the title, the
   response totals and the "same quake, different feeling" line.
8. Save at 200 dpi.

## Numbers on the map

- 597 responses, 144 places.
- Maximum distance: 2,850 km.
- Maximum CDI: 9.1.
- 188 grid cells at 10 km resolution.

## Data links

External sources used for this map (the local caches live in `data/`):

- [USGS DYFI programme](https://earthquake.usgs.gov/data/dyfi/)
- [USGS event us7000srb1](https://earthquake.usgs.gov/earthquakes/eventpage/us7000srb1)
- [USGS FDSN Event API](https://earthquake.usgs.gov/fdsnws/event/1/)

## What this map does not say

- DYFI is self-reported and voluntary. Responses are biased toward people with
  internet access, smartphones and time; rural and low-connectivity areas are
  under-represented.
- CDI is not a physical measurement. It is a community-scaled intensity derived
  from reports, and it differs from instrumental shaking, PGA or MMI maps.
- A blank cell means no reports, not no shaking.
- The 10 km grid smooths local variation; two adjacent barangays can feel very
  different shaking.
- The maximum distance may include reports from people travelling or submitting
  from elsewhere; it is not a felt-radius boundary.
