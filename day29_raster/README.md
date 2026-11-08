# Day 29 — Raster
**The cone, one pixel at a time**

**Output:** `day29_raster/day29_raster.png`
**Run:** `uv run python -m day29_raster.map`

## The story

Raster maps hide their own construction. A smooth hillshade or a flood mask looks
continuous, but underneath it is a grid of decisions: each cell has one elevation,
one class, one value. This day makes the grid visible.

The map shows Mayon's elevation surface at 30 m, with contour lines every 250 m.
A zoom inset takes a 24 × 24 pixel window around the summit and draws every cell
boundary. At that scale the perfect cone becomes a staircase. The 6 km danger
zone is only 400 pixels across. This is the resolution at which a hazard map
decides what is steep, what is high and what is safe.

## Data

- **Elevation:** Copernicus DEM GLO-30, tile `N13_00_E123_00`, cached as
  `data/mayon_dem.npy` from Day 17. 829 × 973 pixels at 30 m.
- **Crop:** 123.55–123.82°E, 13.13–13.36°N.
- **Summit:** 13.2573°N, 123.6855°E.
- **Zone:** 6 km buffer in UTM 51N.
- **Licence:** Copernicus DEM, free and open.

## Process

1. Load the cached elevation array (no new download).
2. Display it with a custom six-stop terrain colormap from deep navy at sea level
   through pine and olive to cream at the summit. No hillshade is used; the point
   is the raw raster.
3. Add contour lines at 250 m intervals in a faint dark ink so the cone's
   structure is readable without turning the map back into a hillshade.
4. Overlay the 6 km zone as a red dashed circle and label it "400 pixels across".
5. Compute the summit's row and column from the geographic bounds, then take a
   24 × 24 pixel window centred on it.
6. Draw the window as an inset with its own local colour stretch, a grid line at
   every pixel boundary, and contour lines every 100 m. The local stretch is
   necessary: on the global 0–2,600 m scale the summit window is almost uniform.
7. Add a title inside the inset: "summit · 24 × 24 pixels · 720 m" and a note
   that each square is 30 m.
8. Add a horizontal elevation colour bar and compose the title, the pixel-count
   explanation and the source footer.

## Numbers on the map

- 829 × 973 elevation pixels.
- 30 m pixel size.
- 6 km danger zone = about 400 pixels across.
- Inset: 24 × 24 pixels = 720 m across.
- Contours: 250 m on the main map, 100 m in the inset.

## Data links

External sources used for this map (the local caches live in `data/`):

- [Planetary Computer: Copernicus DEM GLO-30](https://planetarycomputer.microsoft.com/dataset/cop-dem-glo-30)
- [Copernicus Data Space](https://dataspace.copernicus.eu/)
- [PHIVOLCS](https://www.phivolcs.dost.gov.ph/)

## What this map does not say

- Elevation is not hazard. Steepness, ash thickness, lahar channels and
  evacuation routes are separate datasets.
- The DEM is a surface model with vertical error; 30 m cells smooth the summit
  and the ravines.
- The inset's local stretch exaggerates tiny differences, so its colours are not
  comparable to the main map's.
- The "400 pixels across" is a diameter estimate from the 6 km buffer, not a
  measured hazard boundary.
- Contours are interpolated from the same grid; they do not add information
  below 30 m resolution.
