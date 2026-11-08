# Day 13 — Interactions
**Two years of shaking, wind and ash**

**Output:** `day13_interactions/day13_interactions.html` (interactive) and
`day13_interactions/day13_interactions.png` (static preview)
**Run:** `uv run python -m day13_interactions.map`

## The story

The static maps in this series each isolate one hazard. This day asks for
interaction: let the reader move between earthquakes, typhoon tracks and the
Mayon danger zone on one canvas. The result is a Folium map centred on the
Philippines with three toggleable layers, popups, a scale bar and a measuring
tool.

The narrative is the same as the rest of the series: the last two years in the
Philippines were a compound emergency. Earthquakes, typhoons and volcanic
eruptions did not wait for each other. An interactive map makes that
co-occurrence easier to explore than a stack of separate posters.

## Data

- **Earthquakes:** the cached USGS M5+ catalogue from Day 1
  (`data/ph_quakes.geojson`), clipped to the national boundary. 133 events.
- **Typhoons:** the cached IBTrACS 2026 tracks, filtered to storms that entered
  the PAR test box. Nine storms.
- **Mayon:** a 6 km circle around 13.2573°N, 123.6855°E.
- **Basemap:** Esri World Dark Gray Canvas tiles (free tier), with attribution.
- **Libraries:** Folium for the map, `folium.plugins.MeasureControl` for
  distance measurement.
- **Licences:** USGS public domain; IBTrACS NOAA; OSM ODbL; Esri basemap terms.

## Process

1. Load the cached earthquake catalogue, read depth from the geometry Z, and
   spatial-join to the OSM country polygon.
2. Create a Folium map centred at 12.5°N, 122°E, zoom 5, with no default tile
   layer. Add Esri's dark canvas as a named but uncontrolled layer
   (`name="Dark canvas"`, `control=False`), so the layer control does not show a
   raw tile URL. (CartoDB's dark tiles now require an API key, so the basemap was
   switched.)
3. Add a `FeatureGroup` for earthquakes. Each event becomes a circle marker:
   radius scales with magnitude, colour by depth (red under 70 km, orange
   70–300 km, blue deeper), popup with magnitude, place and depth.
4. Add a second `FeatureGroup` for typhoons. For each storm, build a polyline
   from its `LAT`/`LON` sequence and colour it by peak wind (blue, yellow,
   orange, red). The tooltip carries the storm name and peak intensity.
5. Add a third group for Mayon: a dashed red 6 km circle with fill and a marker
   with a warning icon.
6. Add a collapsed layer control (cleaner default view), a scale bar and a
   measuring tool.
7. Fit the initial view to the Philippine bounding box (4.3–21.5°N,
   114–127°E) so the map opens on the archipelago instead of the whole of
   Southeast Asia.
8. Inject a fixed-position HTML title block in the page's top-left, using the
   series palette and letter-spaced theme label.
9. Save as a self-contained HTML file. Tiles load from the network when opened.
10. For the gallery preview, capture the HTML with headless Chrome at
    1600 × 1200 (`--headless=new --virtual-time-budget=15000 --screenshot=…`)
    and save it next to the HTML as a PNG.

## Numbers on the map

- 133 M5+ earthquakes.
- 9 named 2026 typhoon tracks.
- One 6 km volcanic danger zone.
- Three toggleable layers.

## Data links

External sources used for this map (the local caches live in `data/`):

- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)
- [USGS FDSN Event API](https://earthquake.usgs.gov/fdsnws/event/1/)
- [IBTrACS product page](https://www.ncei.noaa.gov/products/international-best-track-archive)
- [Esri Dark Gray Canvas](https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer)
- [Folium](https://python-visualization.github.io/folium/)

## What this map does not say

- The HTML depends on external tile and JavaScript CDNs. Offline, the layers
  remain but the basemap disappears.
- Earthquake and typhoon layers are simplified versions of the static maps;
  there is no time slider, so events from different months sit on top of each
  other.
- The Mayon circle is a schematic buffer, not the official hazard polygon.
- Popups show catalogue values, not impact or damage.
- Folium renders vector layers client-side; with many points on a low-end
  device, panning and zooming can be slow.
