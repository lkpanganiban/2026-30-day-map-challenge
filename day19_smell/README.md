# Day 19 — Senses: Smell
**The volcano you can smell**

**Output:** `day19_smell/day19_smell.png`
**Run:** `uv run python -m day19_smell.map`

## The story

Taal Volcano, south of Manila, is one of the smallest active volcanoes in the
world and one of the easiest to smell: sulphur dioxide from its crater drifts
over Batangas and Cavite on ordinary days, and far more during unrest. On
29 September 2026 PHIVOLCS recorded a steam-laden plume 2,700 metres tall and
160 tonnes of SO₂ from the main crater.

Smell is chemistry in the air, so the map uses a chemical measurement. The
TROPOMI instrument on Sentinel-5P measures the total vertical column of sulphur
dioxide. On 29 September the daily pass caught an enhancement over the Taal area
and a larger patch drifting southeast over Quezon. This is what a smell looks
like as a raster of molecules per square metre.

## Data

- **Instrument:** ESA Sentinel-5P TROPOMI Level-2 SO₂, orbit
  `S5P_L2_SO2____20260929T055116_20260929T055616_46433`, downloaded as a
  120 MB NetCDF from the Microsoft Planetary Computer.
- **Variables:** `latitude`, `longitude`, `qa_value`,
  `sulfurdioxide_total_vertical_column` (mol/m²), read from the `PRODUCT` group
  with `xarray` + `h5netcdf`.
- **Quality filter:** `qa_value > 0.5`, finite values, and SO₂ above
  1 × 10⁻⁴ mol/m². 993 pixels survive inside the crop.
- **Crop:** 120.55–123.25°E, 12.15–15.10°N.
- **Event facts:** 160 tonnes of SO₂ and a 2,700 m plume on 29 September 2026,
  from PHIVOLCS.
- **Licence:** Copernicus Sentinel-5P data, free and open.

## Process

1. Search the Planetary Computer for Sentinel-5P SO₂ items over Taal on
   29 September 2026 and choose the orbit covering the area.
2. Download the NetCDF file and open the `PRODUCT` group. The root group is
   empty, which is why the first read attempt returned no variables.
3. Read latitude, longitude, quality flag and SO₂ column arrays (1 × 358 × 450
   pixels).
4. Build a mask from quality, finite values, a minimum column and the crop box.
5. Plot the selected pixels as 3.5 × 5.5 km squares coloured on a logarithmic
   scale from 10⁻⁴ to 1.6 × 10⁻³ mol/m². Log scaling is necessary because the
   plume is an order of magnitude above background.
6. Draw the Philippine land silhouette beneath the pixels so the plume's
   position relative to Taal, Batangas and Quezon is readable.
7. Mark Taal with a red triangle and label the enhancement southeast of the
   volcano.
8. Add a horizontal colour bar, explaining that each pixel is a TROPOMI
   footprint, and compose the title and source line.

## Numbers on the map

- 993 quality-filtered pixels.
- Pixel footprint: 3.5 × 5.5 km.
- Column range shown: 10⁻⁴ to 1.6 × 10⁻³ mol/m².
- 160 tonnes/day SO₂ and a 2,700 m plume on 29 September 2026.

## Data links

External sources used for this map (the local caches live in `data/`):

- [Planetary Computer: Sentinel-5P L2](https://planetarycomputer.microsoft.com/dataset/sentinel-5p-l2-netcdf)
- [TROPOMI](https://www.tropomi.eu/)
- [Copernicus Data Space](https://dataspace.copernicus.eu/)
- [PHIVOLCS](https://www.phivolcs.dost.gov.ph/)

## What this map does not say

- TROPOMI measures a column from the surface to the top of the atmosphere, not
  ground-level concentration. A high column does not mean a strong smell at
  street level.
- The enhancement is weak in absolute terms; most values are close to the
  detection limit. Some pixels may be noise, cloud artefacts or transport from
  other sources.
- The daily overpass is a snapshot around late morning local time. SO₂
  emissions vary hourly.
- The apparent southeast drift is a single-day pattern, not a climatology.
- The map shows an enhancement, not a health-risk zone. Odour thresholds,
  exposure and wind at ground level are not modelled.
