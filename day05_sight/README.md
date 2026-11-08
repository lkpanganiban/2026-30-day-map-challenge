# Day 05 — Senses: Sight
**What Landsat saw two days later**

**Output:** `day05_sight/day05_sight.png`
**Run:** `uv run python -m day05_sight.map`

## The story

On 30 October 2026 Mayon erupted, sending an ash column roughly three kilometres
above the summit and forcing more than two thousand people to leave the slopes.
Two days later, on 1 November, Landsat 9 passed over Albay with only about a
quarter of the scene cloud-covered. The satellite saw the mountain and the ash
still streaming away from it.

This is "sight" in the most literal sense: what an instrument 705 km above the
ground could see. The image is a short-wave infrared composite rather than true
colour, because SWIR separates fresh ash, vegetation and cloud more clearly than
red-green-blue. The ash reads grey-brown, forest is green, cloud is blue.
Overlaid on the image is the same 6 km Permanent Danger Zone used in Day 3.

## Data

- **Scene:** Landsat 9 Collection 2 Level-2 surface reflectance,
  `LC09_L2SP_114051_20261101_02_T1`, 1 November 2026, about 26% cloud.
- **Bands:** `swir22` (B7), `swir16` (B6) and `red` (B4), read at native 30 m
  resolution from cloud-optimised GeoTIFFs.
- **Access:** Microsoft Planetary Computer STAC API, with SAS signing through
  the `planetary-computer` package.
- **Crop:** 123.55–123.82°E, 13.13–13.36°N, projected to UTM 51N for windowed
  reads.
- **Zone:** 6 km buffer around the summit (13.2573°N, 123.6855°E).
- **Licence:** Landsat data is NASA/USGS, public domain.

## Process

1. Search the Planetary Computer STAC for Landsat 9 scenes over Mayon between
   31 October and 3 November 2026, and choose the least cloudy result.
2. Sign the item's asset URLs, then read a window of each band. The window is
   computed by transforming the geographic crop into UTM 51N and using
   `rasterio.windows.from_bounds`; this avoids downloading whole 7,000-pixel
   scenes.
3. Stack SWIR2, SWIR1 and red into an RGB array and apply a percentile stretch
   (1st to 99th) with a gamma of 0.7. The stretch makes the ash plume visible
   without inventing contrast.
4. Cache the stacked array as `data/mayon_landsat.npy` so re-renders are
   instant.
5. Plot the image with a geographic extent inside a dark figure, then overlay
   the danger-zone circle in two passes: a wide dark underlay for contrast and a
   thin red dashed line on top.
6. Add a summit cross, a label chip, a north arrow and a 5 km scale bar.
7. Compose the title, a three-line explanation of the colour composite, and the
   source footer.

## Numbers on the map

- Scene date: 1 November 2026, two days after the eruption.
- Pixel size: 30 m.
- Zone diameter: 12 km (6 km radius).
- Scene cloud cover: about 26%.

## Data links

External sources used for this map (the local caches live in `data/`):

- [Planetary Computer: Landsat C2 L2](https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2)
- [USGS Landsat 9](https://www.usgs.gov/landsat-missions/landsat-9)
- [USGS EarthExplorer](https://earthexplorer.usgs.gov/)
- [PHIVOLCS](https://www.phivolcs.dost.gov.ph/)

## What this map does not say

- The grey-brown mass is interpreted as ash, but thin cloud and ash can look
  similar in a single SWIR composite. The map is a visual reading, not a
  classified plume mask.
- No atmospheric correction beyond the provider's Level-2 surface reflectance
  was applied, and no plume height or mass is derived.
- A single overpass is a snapshot. It cannot show how the plume evolved through
  the day.
- The 6 km circle is a schematic buffer, not the official PHIVOLCS hazard
  polygon.
