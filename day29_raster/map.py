"""Day 29 - Raster.

Mayon's elevation surface at 30 m, and a 24 x 24 pixel zoom on the summit.
The hazard zone is 400 pixels across; the map's decisions are made at this size.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from shapely.geometry import Point

from style import ACCENT, DATA, FONT, INK, PAPER

OUT = Path(__file__).parent
BOUNDS = (123.55, 13.13, 123.82, 13.36)
SUMMIT = (123.6855, 13.2573)

elev = np.load(DATA / "mayon_dem.npy")
TERRAIN = LinearSegmentedColormap.from_list(
    "mayon", ["#0b1622", "#123a4a", "#2e6b5a", "#7fa06a", "#c9b98d", "#efe6d0"])
h, w = elev.shape

fig, ax = plt.subplots(figsize=(12, 13), facecolor=PAPER)
ax.set_facecolor(PAPER)
im = ax.imshow(elev, extent=(BOUNDS[0], BOUNDS[2], BOUNDS[1], BOUNDS[3]), origin="upper",
               cmap=TERRAIN, vmin=0, vmax=2600)

summit = gpd.GeoSeries([Point(*SUMMIT)], crs=4326).to_crs(32651).iloc[0]
zone = gpd.GeoSeries([summit.buffer(6000)], crs=32651).to_crs(4326)
zone.boundary.plot(ax=ax, color=ACCENT, linewidth=1.1, alpha=0.95,
                   linestyle=(0, (5, 4)), zorder=3)
ax.annotate("6 km PDZ · 400 pixels across", (SUMMIT[0], SUMMIT[1] - 0.062), ha="center",
            color=INK, fontsize=9, fontfamily=FONT, zorder=4,
            bbox=dict(facecolor=PAPER, alpha=0.75, edgecolor="none", pad=3))

ax.contour(np.linspace(BOUNDS[0], BOUNDS[2], w), np.linspace(BOUNDS[3], BOUNDS[1], h),
           elev, levels=range(250, 2500, 250), colors=INK, linewidths=0.3, alpha=0.22, zorder=2)
ax.set_xlim(BOUNDS[0], BOUNDS[2])
ax.set_ylim(BOUNDS[1], BOUNDS[3])
ax.set_aspect(1 / np.cos(np.radians(13.25)))
ax.axis("off")

# zoom inset: 24 x 24 pixels around the summit
row = int((BOUNDS[3] - SUMMIT[1]) / (BOUNDS[3] - BOUNDS[1]) * h)
col = int((SUMMIT[0] - BOUNDS[0]) / (BOUNDS[2] - BOUNDS[0]) * w)
r0, c0, n = row - 12, col - 12, 24
win = elev[r0:r0 + n, c0:c0 + n]
lon0 = BOUNDS[0] + c0 / w * (BOUNDS[2] - BOUNDS[0])
lon1 = BOUNDS[0] + (c0 + n) / w * (BOUNDS[2] - BOUNDS[0])
lat1 = BOUNDS[3] - r0 / h * (BOUNDS[3] - BOUNDS[1])
lat0 = BOUNDS[3] - (r0 + n) / h * (BOUNDS[3] - BOUNDS[1])

inset = ax.inset_axes([0.60, 0.10, 0.32, 0.32])
inset.set_facecolor(PAPER)
inset.imshow(win, extent=(lon0, lon1, lat0, lat1), origin="upper",
             cmap=TERRAIN, vmin=0, vmax=2600)
inset.set_xticks(np.linspace(lon0, lon1, n + 1), minor=False)
inset.set_yticks(np.linspace(lat0, lat1, n + 1), minor=False)
inset.grid(color=PAPER, linewidth=0.25, alpha=0.35)
inset.contour(np.linspace(lon0, lon1, n), np.linspace(lat1, lat0, n), win,
              levels=np.arange(1900, 2500, 100), colors=INK, linewidths=0.5, alpha=0.5)
inset.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
for spine in inset.spines.values():
    spine.set_edgecolor(INK)
    spine.set_linewidth(0.8)
inset.set_title("summit · 24 × 24 pixels · 720 m", color=INK, fontsize=8,
                fontfamily=FONT, pad=4)
inset.annotate("each square = 30 m", (0.5, -0.06), xycoords="axes fraction",
               ha="center", va="top", color=INK, fontsize=8, fontfamily=FONT)

cax = fig.add_axes([0.30, 0.075, 0.40, 0.012])
cbar = fig.colorbar(im, cax=cax, orientation="horizontal")
cbar.set_label("elevation (m) · Copernicus DEM GLO-30", color=INK, fontsize=9,
               fontfamily=FONT, labelpad=8)
cbar.ax.tick_params(colors=INK, labelsize=8)
cbar.outline.set_edgecolor(INK)

fig.text(0.07, 0.945, "R A S T E R", color=ACCENT, fontsize=15, fontfamily=FONT,
         fontweight="bold")
fig.text(0.07, 0.905, "The cone, one pixel at a time", color=INK, fontsize=26,
         fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.865,
         f"{h:,} × {w:,} elevation pixels, 30 m each. The whole 6 km danger zone is only 400\n"
         "pixels across. Zoom to the summit and every square is one measurement: the raster is\n"
         "where a hazard map decides what is steep, what is high, and what is safe.",
         color=INK, alpha=0.82, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.025,
         "Elevation: Copernicus DEM GLO-30, via Microsoft Planetary Computer  ·  "
         "#30DayMapChallenge 2026 · Day 29 · Raster",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.06, right=0.94, top=0.825, bottom=0.13)
out = OUT / "day29_raster.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out, elev.shape)
