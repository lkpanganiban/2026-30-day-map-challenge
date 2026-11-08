# Day 17 — Light & dark
**The cone at first light**

**Output:** `day17_lightdark/day17_lightdark.png`
**Run:** `uv run python -m day17_lightdark.map`

## The story

Mayon is famous for the geometry of its cone: a near-perfect symmetric
stratovolcano with ravines radiating from the summit. Most maps describe it with
contours or hazard polygons. This map describes it with light.

A digital elevation model is lit from the north-west at a low sun angle. The
result is a hillshade: every ridge catches light, every ravine falls into
shadow. The volcano's shape becomes the map. The 6 km Permanent Danger Zone is
drawn over the slopes, and the villages at the foot of the cone sit exactly
where the ash and lahars would travel.

## Data

- **Elevation:** Copernicus DEM GLO-30, tile `Copernicus_DSM_COG_10_N13_00_E123_00_DEM`
  (30 m, EPSG:4326), accessed through the Microsoft Planetary Computer STAC API.
- **Crop:** 123.55–123.82°E, 13.13–13.36°N; the downloaded array is 829 × 973
  pixels after clipping.
- **Summit:** 13.2573°N, 123.6855°E.
- **Zone:** 6 km buffer computed in UTM 51N and converted back to geographic
  coordinates for plotting.
- **Licence:** Copernicus DEM is free and open under the Copernicus terms.

## Process

1. Search the Planetary Computer for the GLO-30 tile covering Mayon, sign the
   asset, and clip it to the crop box with `rioxarray`.
2. Cache the elevation array as `data/mayon_dem.npy`.
3. Create a `matplotlib.colors.LightSource` with azimuth 315° (north-west) and
   altitude 32°.
4. Call `LightSource.shade` on the elevation array with `vert_exag=2.5`,
   `dx=dy=30` metres, and a custom five-stop terrain colormap (deep navy, pine,
   olive, sand, cream). The blend mode is "soft", which preserves the colour
   ramp while adding shadows.
5. Display the shaded image with a geographic extent and an aspect ratio
   corrected for latitude (`1/cos(13.25°)`).
6. Overlay the 6 km zone as a red dashed circle, with a label chip below the
   summit.
7. Mark the summit with a cross and a label chip (`Mayon · 2,462 m`).
8. Compose the title, an explanation of the lighting, and the source footer.

## Numbers on the map

- 30 m elevation pixels.
- 829 × 973 pixels in the crop.
- Vertical exaggeration: 2.5×.
- Sun azimuth 315°, altitude 32°.
- Danger-zone radius: 6 km.

## Data links

External sources used for this map (the local caches live in `data/`):

- [Planetary Computer: Copernicus DEM GLO-30](https://planetarycomputer.microsoft.com/dataset/cop-dem-glo-30)
- [Copernicus Data Space](https://dataspace.copernicus.eu/)
- [PHIVOLCS](https://www.phivolcs.dost.gov.ph/)

## What this map does not say

- The hillshade is a visual product. It is not a slope, aspect or hazard map,
  and vertical exaggeration changes the apparent steepness.
- The lighting direction is arbitrary. A different sun angle would reveal
  different ravines and make the cone look different.
- The DEM is a surface model, not a bare-earth model; in forested areas the
  canopy is part of the elevation.
- The 6 km circle is a schematic buffer, not the official PHIVOLCS hazard
  polygon.
- The map does not show the 2026 ash deposit. For that, see Day 5.
