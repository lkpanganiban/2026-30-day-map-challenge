# 30 Day Map Challenge 2026 — Philippines

Thirty Python maps for [#30DayMapChallenge](https://30daymapchallenge.com/2026),
built from OpenStreetMap, Landsat 9, Sentinel-1/2/5P, USGS, IBTrACS and
Copernicus DEM — each one a story from the Philippines' last two years.

Started late: Days 1–7 were catch-ups published after the fact; Day 7 was made
as a genuine ten-minute build from cached data. Days 8–30 are on schedule.
Day 30 is a printable template — the final map is meant to be drawn by hand.

## Run

```bash
uv sync
uv run python -m day08_utopia.map     # writes day08_utopia/day08_utopia.png
```

Every download is cached in `data/`, so re-renders are offline and fast.
First runs need network: Overpass, USGS, IBTrACS, Natural Earth, Planetary Computer.

Some days output HTML (`day13`, `day27`) or a printable PDF (`day30`).

Every day folder has its own `README.md` with the full story, data sources,
processing steps, numbers and limits of the map.

## Static site

`index.html` is a single-file, hash-routed gallery: a dashboard of all 30 maps
and a detail view containing each day's rendered README. Rebuild it with:

```bash
uv run python build_site.py
```

To host on GitHub Pages: push the repository, open **Settings → Pages**, choose
**Deploy from a branch**, and select the branch root (`/`). The included
`.nojekyll` file keeps Pages from running Jekyll over the map folders.

| Day | Theme | Map | Story |
|-----|-------|-----|-------|
| 1 | Points | 133 earthquakes, two years | Sarangani M7.8 (Jun 2026), Eastern Mindanao M7.4 (Oct 2025), Cebu M6.9 (Sep 2025) |
| 2 | Lines | Nine storms entered the ring | 2026 PAR tracks; Champi/Rosal strongest, Bavi/Inday 20 dead |
| 3 | Polygons | Inside the permanent danger zone | 1,363 buildings inside Mayon's 6 km PDZ; 2,041 evacuated 30 Oct 2026 |
| 4 | Clusters | Earthquakes travel in families | 50 km aftershock families of the 2025–26 sequences |
| 5 | Sight | What Landsat saw two days later | Landsat 9 SWIR composite of Mayon's ash plume, 1 Nov 2026 |
| 6 | Vintage | Mapa del Volcan Mayon | 19th-century styling; Cagsawa, buried 1814 |
| 7 | 10 minute map | Ten minutes from the water | 20 m walking-time raster to the nearest creek; 91% within 10 minutes |
| 8 | Utopia | A Metro Manila that does not flood | OSM waterways as the flood-control spine that could have been; Yolanda's 13th anniversary |
| 9 | Urban-rural | Where the city ends | Metro Manila land use; the farmland still holding the edge |
| 10 | Prompting only | The strongest storm of 2026 | Champi/Rosal at its closest pass to Batanes; made from one prompt |
| 11 | Senses: Sound | Where the city is quiet | Distance from major roads as a traffic-noise proxy |
| 12 | Power | The grid, and the plant we never turned on | 3,737 transmission lines; Bataan nuclear plant silent since 1984; Tino's outages |
| 13 | Interactions | Two years of shaking, wind and ash | Interactive Folium map of quakes, typhoons and Mayon |
| 14 | Borgesian map | The map is the territory | 24,811 building footprints in central Tacloban, 1:1 |
| 15 | Inside out | The sea between the islands | Land/water inverted; Tino's Visayan Sea crossing and Champi's Philippine Sea |
| 16 | Collaborative | The crowd maps the storm | 30 OSM changesets in Cebu–Negros since Tino, by mapper |
| 17 | Light & dark | The cone at first light | Copernicus DEM hillshade of Mayon, 30 m |
| 18 | NULL | The storm that isn't here | Kalmaegi (Tino) missing from the best-track archive |
| 19 | Senses: Smell | The volcano you can smell | TROPOMI SO2 enhancement from Taal, 29 Sep 2026 |
| 20 | Hexagons | The bestagons of shaking | H3 bins of M5+ quakes |
| 21 | OpenStreetMap | Every hospital the crowd knows | 2,029 mapped health facilities; 16 near the Cebu quake |
| 22 | Projections | The shape you choose | Mercator, Equal Earth, azimuthal from Manila |
| 23 | Senses: Taste | The taste of the city | 2,746 food shops; 385 wet markets as the last mile |
| 24 | Network | Two ways off the spine | Cebu's coastal routes north and south from Cebu City |
| 25 | Is this a map? | Wind writing | 29 typhoon tracks as ink on paper |
| 26 | Water | Through the cloud, the water | Sentinel-1 radar of the Pampanga basin after the August floods |
| 27 | New tool | A globe that turns | Plotly orthographic globe of tracks and quakes |
| 28 | Senses: Feeling | How the shaking felt | 597 DYFI responses for the M7.8; felt up to 2,850 km away |
| 29 | Raster | The cone, one pixel at a time | 30 m DEM with a 24 × 24 pixel summit zoom |
| 30 | Pen & paper | Mayon, a map to draw by hand | Printable A4 tracing sheet; the analogue map is yours |

## Data

- **OSM** © OpenStreetMap contributors, ODbL — [copyright](https://www.openstreetmap.org/copyright) ·
  [Overpass API](https://overpass-api.de/) ·
  [changeset API](https://wiki.openstreetmap.org/wiki/API_v0.6#Changesets_2)
- **Earthquakes** [USGS FDSN Event API](https://earthquake.usgs.gov/fdsnws/event/1/) ·
  [USGS DYFI](https://earthquake.usgs.gov/data/dyfi/)
- **Typhoons** [NOAA/NCEI IBTrACS v04r01](https://www.ncei.noaa.gov/products/international-best-track-archive)
- **Imagery** [NASA/USGS Landsat 9](https://www.usgs.gov/landsat-missions/landsat-9) ·
  [ESA Copernicus](https://dataspace.copernicus.eu/) via
  [Microsoft Planetary Computer](https://planetarycomputer.microsoft.com/)
- **Elevation** [Copernicus DEM GLO-30](https://planetarycomputer.microsoft.com/dataset/cop-dem-glo-30)
- **Boundaries/land** [Natural Earth 1:10m](https://www.naturalearthdata.com/)
- **Hazards context** [PHIVOLCS](https://www.phivolcs.dost.gov.ph/) ·
  [PAGASA](https://www.pagasa.dost.gov.ph/)

Every day folder's README ends with a **Data links** section listing the exact
external sources used for that map; the local cache paths under `data/` are
storage, not sources.
