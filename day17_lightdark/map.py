"""Day 17 - Light & dark.

Mayon at 30 m, lit from the north-west. The cone's own shadow is the map.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import planetary_computer as pc
import rioxarray
from matplotlib.colors import LightSource, LinearSegmentedColormap
from pystac_client import Client
from shapely.geometry import Point, box

from style import ACCENT, DATA, FONT, INK, PAPER

OUT = Path(__file__).parent
CACHE = DATA / "mayon_dem.npy"
BOUNDS = (123.55, 13.13, 123.82, 13.36)
SUMMIT = (123.6855, 13.2573)


def fetch():
    if CACHE.exists():
        return np.load(CACHE)
    catalog = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
    item = pc.sign(next(catalog.search(
        collections=["cop-dem-glo-30"], bbox=BOUNDS).items()))
    da = rioxarray.open_rasterio(item.assets["data"].href).rio.clip_box(*BOUNDS)
    elev = da.values[0].astype("float32")
    np.save(CACHE, elev)
    return elev


elev = fetch()
ls = LightSource(azdeg=315, altdeg=32)
cmap = LinearSegmentedColormap.from_list(
    "mayon", ["#0d1a24", "#1f3b35", "#5c7a55", "#b8a97e", "#efe6d0"])
rgb = ls.shade(elev, cmap=cmap, blend_mode="soft", vert_exag=2.5, dx=30, dy=30)

fig, ax = plt.subplots(figsize=(12, 13), facecolor=PAPER)
ax.set_facecolor(PAPER)
ax.imshow(rgb, extent=(BOUNDS[0], BOUNDS[2], BOUNDS[1], BOUNDS[3]),
          origin="upper", zorder=1)

summit = gpd.GeoSeries([Point(*SUMMIT)], crs=4326).to_crs(32651).iloc[0]
zone = gpd.GeoSeries([summit.buffer(6000)], crs=32651).to_crs(4326)
zone.boundary.plot(ax=ax, color=ACCENT, linewidth=1.1, alpha=0.9,
                   linestyle=(0, (5, 4)), zorder=3)
ax.annotate("6 km PDZ", (SUMMIT[0], SUMMIT[1] - 0.062), ha="center", color=INK,
            fontsize=9, fontfamily=FONT, zorder=4,
            bbox=dict(facecolor=PAPER, alpha=0.7, edgecolor="none", pad=3))
ax.scatter([SUMMIT[0]], [SUMMIT[1]], marker="+", s=110, color=INK, linewidths=1.5, zorder=5)
ax.annotate("Mayon · 2,462 m", (SUMMIT[0], SUMMIT[1]), xytext=(8, 10),
            textcoords="offset points", color=INK, fontsize=10, fontfamily=FONT,
            fontweight="bold", zorder=5,
            bbox=dict(facecolor=PAPER, alpha=0.7, edgecolor="none", pad=2))

ax.set_xlim(BOUNDS[0], BOUNDS[2])
ax.set_ylim(BOUNDS[1], BOUNDS[3])
ax.set_aspect(1 / np.cos(np.radians(13.25)))
ax.axis("off")

fig.text(0.07, 0.945, "L I G H T   &   D A R K", color=ACCENT, fontsize=15,
         fontfamily=FONT, fontweight="bold")
fig.text(0.07, 0.905, "The cone at first light", color=INK, fontsize=26,
         fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.865,
         "Mayon at 30 m, lit from the north-west, with the 6 km Permanent Danger Zone drawn over\n"
         "the slopes. The volcano's shape is the map: run your eye down the ravines and the\n"
         "villages sit exactly where the ash and lahars would go.",
         color=INK, alpha=0.82, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.035,
         "Elevation: Copernicus DEM GLO-30, via Microsoft Planetary Computer  ·  "
         "#30DayMapChallenge 2026 · Day 17 · Light & dark",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.06, right=0.94, top=0.825, bottom=0.06)
out = OUT / "day17_lightdark.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out, elev.shape)
