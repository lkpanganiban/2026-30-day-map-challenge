"""Day 5 - Senses: Sight.

Landsat 9 over Mayon on 1 November 2026, two days after the 30 October
eruption. Short-wave infrared composite: ash reads grey-brown, forest green,
clouds blue. The 6 km Permanent Danger Zone is overlaid.
"""
from pathlib import Path

import geopandas as gpd
import numpy as np
import planetary_computer as pc
import rasterio
from matplotlib import patheffects as pe
from matplotlib import pyplot as plt
from pyproj import Transformer
from pystac_client import Client
from rasterio.windows import from_bounds
from shapely.geometry import Point

from style import ACCENT, DATA, FONT, INK, PAPER

OUT = Path(__file__).parent
CACHE = DATA / "mayon_landsat.npy"
BOUNDS = (123.55, 13.13, 123.82, 13.36)
SUMMIT = (123.6855, 13.2573)


def fetch():
    if CACHE.exists():
        return np.load(CACHE)
    catalog = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
    items = list(catalog.search(
        collections=["landsat-c2-l2"],
        bbox=BOUNDS,
        datetime="2026-10-31/2026-11-03",
        query={"eo:cloud_cover": {"lt": 60}},
    ).items())
    item = pc.sign(min(items, key=lambda i: i.properties["eo:cloud_cover"]))
    print("scene:", item.id)

    t = Transformer.from_crs(4326, 32651, always_xy=True)
    x0, y0 = t.transform(BOUNDS[0], BOUNDS[1])
    x1, y1 = t.transform(BOUNDS[2], BOUNDS[3])
    bands = []
    for band in ("swir22", "swir16", "red"):
        with rasterio.open(item.assets[band].href) as src:
            window = from_bounds(x0, y0, x1, y1, src.transform).round()
            bands.append(src.read(1, window=window, boundless=True).astype(float))
    arr = np.dstack(bands)
    np.save(CACHE, arr)
    return arr


rgb = fetch()
lo, hi = np.nanpercentile(rgb, 1), np.nanpercentile(rgb, 99)
img = np.clip((rgb - lo) / (hi - lo), 0, 1) ** 0.7

t = Transformer.from_crs(4326, 32651, always_xy=True)
x0, y0 = t.transform(BOUNDS[0], BOUNDS[1])
x1, y1 = t.transform(BOUNDS[2], BOUNDS[3])
summit = Point(*t.transform(*SUMMIT))
zone = gpd.GeoSeries([summit.buffer(6000)], crs=32651)

fig = plt.figure(figsize=(12, 13), facecolor=PAPER)
ax = fig.add_axes([0.055, 0.075, 0.89, 0.70])
ax.imshow(img, extent=(x0, x1, y0, y1), origin="upper", zorder=1)
ax.set_facecolor(PAPER)

zone.boundary.plot(ax=ax, color="black", linewidth=3.2, alpha=0.55,
                   linestyle=(0, (5, 4)), zorder=3)
zone.boundary.plot(ax=ax, color=ACCENT, linewidth=1.1, alpha=0.95,
                   linestyle=(0, (5, 4)), zorder=3.1)
ax.annotate("6 km Permanent Danger Zone", (summit.x, summit.y - 7800), ha="center",
            color=INK, fontsize=9, fontfamily=FONT, zorder=4,
            bbox=dict(facecolor=PAPER, alpha=0.75, edgecolor="none", pad=3))

ax.scatter([summit.x], [summit.y], marker="+", s=130, color=INK, linewidths=1.6, zorder=5)
ax.annotate("Mayon", (summit.x, summit.y), xytext=(8, 10), textcoords="offset points",
            color=INK, fontsize=10, fontfamily=FONT, fontweight="bold", zorder=5,
            bbox=dict(facecolor=PAPER, alpha=0.75, edgecolor="none", pad=2))

# 5 km scale bar
sx, sy = x0 + 3000, y0 + 3000
ax.plot([sx, sx + 5000], [sy, sy], color=INK, linewidth=2.5, zorder=5)
ax.annotate("5 km", (sx + 2500, sy), xytext=(0, 6), textcoords="offset points",
            ha="center", color=INK, fontsize=9, fontfamily=FONT, zorder=5,
            path_effects=[pe.withStroke(linewidth=2, foreground="black")])

# north arrow
ax.annotate("N", (x1 - 3000, y1 - 2500), ha="center", color=INK, fontsize=11,
            fontfamily=FONT, fontweight="bold", zorder=5,
            path_effects=[pe.withStroke(linewidth=2, foreground="black")])
ax.annotate("", (x1 - 3000, y1 - 4000), (x1 - 3000, y1 - 7500),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.5), zorder=5)

ax.set_xlim(x0, x1)
ax.set_ylim(y0, y1)
ax.set_aspect("equal")
ax.axis("off")

fig.text(0.07, 0.955, "S I G H T", color=ACCENT, fontsize=15, fontfamily=FONT,
         fontweight="bold")
fig.text(0.07, 0.918, "What Landsat saw two days later", color=INK,
         fontsize=25, fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.878,
         "Landsat 9 over Mayon on 1 November 2026, two days after the 30 October eruption.\n"
         "Short-wave infrared composite: fresh ash reads grey-brown, forest green, clouds blue.\n"
         "Overlaid is the 6 km Permanent Danger Zone that emptied 2,041 people from their homes.",
         color=INK, alpha=0.82, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.035,
         "Imagery: NASA/USGS Landsat 9 (Collection 2), via Microsoft Planetary Computer  ·  "
         "#30DayMapChallenge 2026 · Day 5 · Sight",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

out = OUT / "day05_sight.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out)
