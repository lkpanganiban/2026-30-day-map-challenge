"""Day 19 - Senses: Smell.

Taal's sulphur dioxide on 29 September 2026, as TROPOMI saw it: an
enhancement drifting southeast over Quezon. 160 tonnes of SO2 that day.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.colors as mcolors
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from shapely.geometry import Point, box

from style import ACCENT, DATA, FONT, INK, PAPER

OUT = Path(__file__).parent
ds = xr.open_dataset(DATA / "s5p_so2_20260929.nc", engine="h5netcdf",
                     group="PRODUCT", decode_times=False)
lat = ds.latitude.values[0]
lon = ds.longitude.values[0]
so2 = ds.sulfurdioxide_total_vertical_column.values[0]
qa = ds.qa_value.values[0]

BBOX = (120.55, 12.15, 123.25, 15.10)
mask = ((qa > 0.5) & np.isfinite(so2) & (so2 > 1e-4)
        & (lat > BBOX[1]) & (lat < BBOX[3]) & (lon > BBOX[0]) & (lon < BBOX[2]))

land = gpd.read_file(DATA / "ph_land.gpkg").to_crs(4326).clip(
    gpd.GeoSeries([box(*BBOX)], crs=4326).iloc[0])

fig, ax = plt.subplots(figsize=(12, 13), facecolor=PAPER)
ax.set_facecolor(PAPER)
land.plot(ax=ax, color="#16222e", edgecolor="#2b4155", linewidth=0.3, zorder=1)

norm = mcolors.LogNorm(vmin=1e-4, vmax=1.6e-3)
sc = ax.scatter(lon[mask], lat[mask], c=so2[mask], s=9, marker="s",
                cmap="inferno", norm=norm, alpha=0.9, zorder=3, linewidths=0)

taal = (120.998, 14.002)
ax.scatter([taal[0]], [taal[1]], marker="^", s=150, color=ACCENT, zorder=5)
ax.annotate("Taal", (taal[0], taal[1]), xytext=(-9, 10), textcoords="offset points",
            ha="right", color=INK, fontsize=11, fontfamily=FONT, fontweight="bold",
            path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)], zorder=6)
ax.annotate("SO2 enhancement\ndrifting southeast", (122.45, 13.15), xytext=(0, 14),
            textcoords="offset points", ha="center", color=INK, fontsize=9,
            fontfamily=FONT, linespacing=1.3,
            path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)], zorder=6)

ax.set_aspect(1 / np.cos(np.radians(13.6)))
ax.set_xlim(BBOX[0], BBOX[2])
ax.set_ylim(BBOX[1], BBOX[3])
ax.axis("off")

cax = fig.add_axes([0.30, 0.075, 0.40, 0.012])
cbar = fig.colorbar(sc, cax=cax, orientation="horizontal", extend="both")
cbar.set_label("SO2 total vertical column (mol/m²)  ·  TROPOMI, 3.5 × 5.5 km pixels",
               color=INK, fontsize=9, fontfamily=FONT, labelpad=8)
cbar.ax.tick_params(colors=INK, labelsize=8)
cbar.outline.set_edgecolor(INK)

fig.text(0.07, 0.945, "S M E L L", color=ACCENT, fontsize=15, fontfamily=FONT,
         fontweight="bold")
fig.text(0.07, 0.905, "The volcano you can smell", color=INK, fontsize=26,
         fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.865,
         "Taal's sulphur dioxide on 29 September 2026, as TROPOMI saw it: an enhancement\n"
         "drifting southeast over Quezon. PHIVOLCS measured 160 tonnes of SO2 from the main\n"
         "crater that day, and a steam plume 2,700 m tall. This is what a smell looks like.",
         color=INK, alpha=0.82, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.025,
         "Data: ESA Sentinel-5P TROPOMI L2 SO2, via Microsoft Planetary Computer  ·  "
         "#30DayMapChallenge 2026 · Day 19 · Senses: Smell",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.06, right=0.94, top=0.80, bottom=0.13)
out = OUT / "day19_smell.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out, int(mask.sum()))
