# Day 01 — Points
**133 earthquakes, two years**

**Output:** `day01_points/day01_points.png`
**Run:** `uv run python -m day01_points.map`

## The story

The Philippines sits on the Pacific Ring of Fire, and the last two years made that
impossible to ignore. On 30 September 2025 a magnitude 6.9 earthquake shook the
Cebu–Bohol area. In October 2025 a magnitude 7.4 event struck off Eastern
Mindanao, followed hours later by a 6.7. Then, on 8 June 2026, a magnitude 7.8
earthquake ruptured offshore of Sarangani in southern Mindanao — the strongest
event in this window and the one that dominates the map.

This is the opening map of the series because points are the simplest honest
shape for an earthquake: an epicentre is a location, not an area. The map does
not try to show damage or intensity (that is Day 28's job). It shows how much of
the country's two years was spent inside these events, and how tightly the
Sarangani sequence clusters around its mainshock.

## Data

- **Earthquakes:** USGS FDSN Event API, `starttime=2024-11-01`,
  `minmagnitude=5`, bounding box 4–22°N, 114–128°E. The download is cached as
  `data/ph_quakes.geojson`.
- **Country boundary:** OpenStreetMap relation for the Philippines downloaded
  through Nominatim/OSMnx and cached as `data/ph_boundary.gpkg`. It is used as a
  filter, not as a land silhouette, because the relation includes territorial
  waters.
- **Land:** Natural Earth 1:10m land polygons, clipped to the Philippine
  bounding box and cached as `data/ph_land.gpkg`.
- **Licences:** USGS data is public domain; OSM data is © OpenStreetMap
  contributors under ODbL; Natural Earth is public domain.

## Process

1. **Fetch once, cache forever.** The script asks USGS for every event at or
   above magnitude 5 in the box and writes the raw GeoJSON. Re-runs read the
   cache, so the map is reproducible offline.
2. **Filter to national territory.** Events inside the OSM country polygon are
   kept with a spatial join. The raw query returns events in Malaysian and
   Indonesian waters; without this step the map would include shaking that is
   not Philippine territory. 133 events survive.
3. **Read depth.** GeoPandas exposes the third coordinate as `geometry.z`;
   this becomes the depth attribute used for colour.
4. **Project.** Everything is reprojected to EPSG:3857 (Web Mercator) so that
   distances and point sizes behave at national scale.
5. **Encode magnitude twice.** Marker area scales as `(mag − 4)³ × 4`, and a
   second, much larger, very transparent copy of each marker creates the glow.
   Area rather than diameter carries the value, which is the correct visual
   encoding for a quantity like energy/magnitude.
6. **Encode depth with colour.** Shallow events (under 70 km) are red; 70–300 km
   are orange; deeper events are blue. Shallow earthquakes are the ones that
   shake cities hardest, so the red should dominate the reader's attention.
7. **Label the three events a news reader would recognise.** The M7.8
   Sarangani, the M7.4 Eastern Mindanao and the M6.9 Cebu events get short
   labels with paper-coloured halos so they survive over dense clusters.
8. **Add a schematic national boundary.** The dashed line is the outer limit of
   the OSM country relation — a reminder that this is a maritime country and
   that many epicentres are offshore.
9. **Compose.** Dark paper background, cream type, a labelled dot legend
   (M5/M6/M7) and depth legend, title block top-left, sources bottom-left.

## Numbers on the map

- 133 events at M5 or above inside Philippine territory, November 2024 to
  November 2026.
- Largest: M7.8, 25 km SW of Kablalan, Sarangani, 8 June 2026.
- Other labelled events: M7.4 Eastern Mindanao (October 2025), M6.9 Cebu
  (30 September 2025).

## Data links

External sources used for this map (the local caches live in `data/`):

- [USGS FDSN Event API](https://earthquake.usgs.gov/fdsnws/event/1/)
- [USGS Earthquake Search](https://earthquake.usgs.gov/earthquakes/search/)
- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)
- [Nominatim geocoder](https://nominatim.org/)
- [Natural Earth](https://www.naturalearthdata.com/)

## What this map does not say

- USGS's M5 threshold is a catalogue choice, not a physical boundary. Thousands
  of smaller events are omitted, and completeness varies with distance from
  seismic stations.
- An epicentre is not damage. The map has no exposure, soil, building or
  intensity information.
- Depth comes from the catalogue's hypocentre solution and carries uncertainty,
  especially offshore.
- The country outline is a simplified maritime/territorial relation. It is not
  a legal boundary and should not be read as one.
