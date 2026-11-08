# Day 27 — New tool
**A globe that turns**

**Output:** `day27_newtool/day27_newtool.html` (interactive) and
`day27_newtool/day27_newtool.png` (static preview)
**Run:** `uv run python -m day27_newtool.map`

## The story

The challenge asks for a tool you have not used before. This series had already
used GeoPandas, OSMnx, Rasterio, Folium, H3 and Matplotlib; Plotly had not
appeared. A Plotly orthographic globe is a different way to see the same two
years: the reader can drag the planet, spin it, and watch the typhoon tracks
wrap around the curve of the Earth.

The globe carries the nine 2026 PAR tracks and the 133 M5+ Philippine
earthquakes. It is a deliberately small dataset on a deliberately large object.
The point is not analytical precision; it is the pleasure of spinning the
archipelago and seeing how a season of storms sits on a sphere.

## Data

- **Earthquakes:** cached USGS M5+ catalogue (`data/ph_quakes.geojson`), clipped
  to the national boundary. 133 events.
- **Typhoons:** cached IBTrACS 2026 tracks filtered to the PAR test box. Nine
  storms.
- **Globe:** Plotly `Scattergeo` with `projection_type="orthographic"`, centred
  on 122°E, 12°N.
- **Licences:** USGS public domain; IBTrACS NOAA; Plotly open source.

## Process

1. Load and clip the earthquake catalogue.
2. Load the typhoon tracks, filter to named 2026 storms entering the PAR box,
   and sort each track by time.
3. Create a Plotly figure. Each storm becomes a `Scattergeo` line trace,
   coloured by peak wind (blue, yellow, orange, red), with the storm name and
   intensity in the legend and hover label.
4. Add the earthquakes as a marker trace sized by magnitude, with magnitude and
   place in the hover text.
5. Configure the geo layer: orthographic projection centred on the Philippines,
   dark ocean, slate land, subtle coastlines and country borders, no lakes.
6. Apply a dark Plotly template and a fixed dark figure background so the HTML
   matches the rest of the series. The figure is 1,200 px tall, with a dark body
   injected after `write_html`, so the page has no white band below the globe.
7. Write a self-contained HTML file with Plotly loaded from a CDN.
8. For the gallery preview, capture the HTML with headless Chrome at
   1600 × 1200 (`--headless=new --virtual-time-budget=15000 --screenshot=…`)
   and save it next to the HTML as a PNG.

## Numbers on the map

- Nine typhoon tracks.
- 133 earthquakes.
- One interactive orthographic globe.

## Data links

External sources used for this map (the local caches live in `data/`):

- [IBTrACS product page](https://www.ncei.noaa.gov/products/international-best-track-archive)
- [USGS FDSN Event API](https://earthquake.usgs.gov/fdsnws/event/1/)
- [Plotly Python](https://plotly.com/python/)

## What this map does not say

- The globe is a display, not an analysis. There is no time animation, no
  filtering and no spatial query.
- Plotly loads from a CDN; the HTML needs network access to render.
- Orthographic projection makes distance and area judgments unreliable away
  from the centre.
- The typography and layout are constrained by Plotly's HTML renderer; it does
  not match the static maps pixel-for-pixel.
- The earthquake and typhoon layers are simplified versions of the static maps.
