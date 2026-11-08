# Day 26 — Water
**Through the cloud, the water**

**Output:** `day26_water/day26_water.png`
**Run:** `uv run python -m day26_water.map`

## The story

In late August 2026, heavy monsoon rain and a tropical system produced floods and
landslides across Luzon. Optical satellites were useless: every Sentinel-2 scene
over Central Luzon in the following week was 100% cloud. Radar does not care
about cloud.

Sentinel-1 passed over the Pampanga basin on 5 September 2026, eight days after
the floods. The map shows its VV backscatter as a greyscale radar image. Water —
the Pampanga River, the Candaba wetlands, the fishponds — is dark because the
surface is smooth and reflects the radar away from the satellite. Cities,
fields and levee banks are brighter. It is a view of what the cloud was hiding.

## Data

- **Radar:** ESA Sentinel-1 RTC (radiometrically terrain corrected), VV
  polarisation, scene
  `S1D_IW_GRDH_1SDV_20260905T214558_20260905T214623_004448_0083EA_rtc`,
  5 September 2026.
- **Access:** Microsoft Planetary Computer STAC, chosen from two overlapping
  scenes by the fraction of valid pixels covering the basin (98.6% versus 5.8%).
- **Crop:** 120.45–121.00°E, 14.80–15.45°N, read at 20 m resolution into a
  2,400 × 2,858 array.
- **Towns:** Angeles, San Fernando, Candaba, Calumpit; Pampanga River label near
  120.75°E, 14.95°N.
- **Licence:** Copernicus Sentinel-1 data, free and open.

## Process

1. Search the Planetary Computer for Sentinel-1 RTC scenes over the Pampanga
   basin on 5 September 2026.
2. For each candidate, read a small preview window and compute the fraction of
   valid (non-zero) pixels. Choose the scene with the best coverage. The first
   attempt picked the other scene and produced a mostly black image.
3. Read the VV band for the full crop with `rasterio` windowed reads and
   `out_shape` to resample to 20 m.
4. Convert linear power to decibels (`10 × log10(VV)`), clip the floor, and set
   zero/nodata pixels to NaN.
5. Display with a grayscale ramp from −25 to −2 dB. Water is dark; built-up and
   vegetated surfaces are bright.
6. Add town labels and a river label with dark halos so they survive the busy
   image.
7. Add a vertical VV colour bar, the title, the "eight days after" context, and
   the source footer.

## Numbers on the map

- Scene date: 5 September 2026.
- Resolution: 20 m display grid.
- Coverage of the chosen scene: 98.6% of the crop.
- Backscatter range shown: −25 to −2 dB.

## Data links

External sources used for this map (the local caches live in `data/`):

- [Planetary Computer: Sentinel-1 RTC](https://planetarycomputer.microsoft.com/dataset/sentinel-1-rtc)
- [Copernicus Data Space](https://dataspace.copernicus.eu/)
- [Copernicus Sentinel-1 data guide](https://documentation.dataspace.copernicus.eu/Data/SentinelMissions/Sentinel1.html)

## What this map does not say

- The image is not a classified flood map. No threshold, change detection or
  ground truth was used; dark pixels are interpreted visually as water but can
  also be smooth surfaces, shadow, or low-return fields.
- Eight days after the flood, some water had already drained. The map shows
  what remained, not the peak extent.
- Radar backscatter depends on surface roughness, moisture and incidence angle,
  not only on water.
- The scene is one moment in time. It cannot show how the flood moved.
- No population, damage or road-closure data are overlaid.
