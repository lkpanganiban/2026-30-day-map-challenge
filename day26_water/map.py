"""Day 26 - Water.

Sentinel-1 radar over the Pampanga basin, five days after the late-August
2026 floods. Water is dark; the Candaba wetlands and fishponds hold it longest.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import planetary_computer as pc
import rasterio
from pystac_client import Client
from shapely.geometry import Point
from pyproj import Transformer
from rasterio.windows import from_bounds

from style import ACCENT, DATA, FONT, INK, PAPER

OUT = Path(__file__).parent
BBOX = (120.45, 14.80, 121.00, 15.45)


def sample():
    if (DATA / "pampanga_sar.npy").exists():
        return np.load(DATA / "pampanga_sar.npy")
    catalog = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
    items = [i for i in catalog.search(
        collections=["sentinel-1-rtc"], bbox=BBOX, datetime="2026-09-05").items()]
    t = Transformer.from_crs(4326, 32651, always_xy=True)
    x0, y0 = t.transform(BBOX[0], BBOX[1])
    x1, y1 = t.transform(BBOX[2], BBOX[3])

    def coverage(item):
        with rasterio.open(item.assets["vv"].href) as src:
            win = from_bounds(x0, y0, x1, y1, src.transform).round()
            a = src.read(1, window=win, out_shape=(200, 240))
        return (a > 0).mean()

    signed = [pc.sign(i) for i in items]
    item = max(signed, key=coverage)
    with rasterio.open(item.assets["vv"].href) as src:
        win = from_bounds(x0, y0, x1, y1, src.transform).round()
        vv = src.read(1, window=win,
                      out_shape=(2400, int(2400 * (y1 - y0) / (x1 - x0)))).astype("float32")
    db = 10 * np.log10(np.clip(vv, 1e-5, None))
    db[vv == 0] = np.nan
    np.save(DATA / "pampanga_sar.npy", db)
    return db


db = sample()
t = Transformer.from_crs(4326, 32651, always_xy=True)
x0, y0 = t.transform(BBOX[0], BBOX[1])
x1, y1 = t.transform(BBOX[2], BBOX[3])

fig, ax = plt.subplots(figsize=(12, 12), facecolor=PAPER)
ax.set_facecolor(PAPER)
cmap = plt.get_cmap("gray").copy()
cmap.set_bad(PAPER)
ax.imshow(db, extent=(x0, x1, y0, y1), origin="upper", cmap=cmap,
          vmin=-25, vmax=-2, interpolation="nearest")

towns = {"Angeles": (120.59, 15.15), "San Fernando": (120.69, 15.03),
         "Candaba": (120.89, 15.09), "Calumpit": (120.77, 14.92)}
for name, (lon, lat) in towns.items():
    px, py = t.transform(lon, lat)
    ax.annotate(name, (px, py), xytext=(6, 6), textcoords="offset points",
                color=INK, fontsize=9, fontfamily=FONT,
                path_effects=[pe.withStroke(linewidth=3, foreground="black")], zorder=5)

river = gpd.GeoSeries([Point(120.75, 14.95)],
                      crs=4326).to_crs(32651).iloc[0]
ax.annotate("Pampanga River", (river.x, river.y), xytext=(8, -14),
            textcoords="offset points", color="#58c7f3", fontsize=9,
            fontfamily=FONT, path_effects=[pe.withStroke(linewidth=3, foreground="black")],
            zorder=5)

ax.set_aspect("equal")
ax.set_xlim(x0, x1)
ax.set_ylim(y0, y1)
ax.axis("off")

cbar = fig.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(-25, -2), cmap="gray"),
                    ax=ax, fraction=0.03, pad=0.01, shrink=0.5)
cbar.set_label("VV backscatter (dB)", color=INK, fontsize=9, fontfamily=FONT)
cbar.ax.tick_params(colors=INK, labelsize=8)
cbar.outline.set_edgecolor(INK)

fig.text(0.07, 0.945, "W A T E R", color=ACCENT, fontsize=15, fontfamily=FONT,
         fontweight="bold")
fig.text(0.07, 0.905, "Through the cloud, the water", color=INK, fontsize=26,
         fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.865,
         "Sentinel-1 radar over the Pampanga basin on 5 September 2026, eight days after the\n"
         "late-August floods. Water is dark: the Candaba wetlands and the fishponds keep it\n"
         "longest. Radar sees through the monsoon cloud that hides the same ground from optics.",
         color=INK, alpha=0.82, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.035,
         "Data: ESA Sentinel-1 RTC, via Microsoft Planetary Computer  ·  "
         "#30DayMapChallenge 2026 · Day 26 · Water",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.06, right=0.90, top=0.79, bottom=0.06)
out = OUT / "day26_water.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out, db.shape)
