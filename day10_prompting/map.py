"""Day 10 - Prompting only.

Made end-to-end from a chat prompt: Super Typhoon Champi (Rosal) at its
closest approach to Batanes, 21 October 2026.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.collections import LineCollection
from shapely.geometry import box

from style import ACCENT, DATA, FONT, INK, PAPER, WATER

OUT = Path(__file__).parent
df = pd.read_csv(DATA / "ibtracs_last3years.csv", skiprows=[1], low_memory=False)
df = df[df.NAME == "CHAMPI"].copy()
for c in ["LAT", "LON", "USA_WIND"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df = df.dropna(subset=["LAT", "LON"])

land = gpd.read_file(DATA / "wp_land.gpkg").to_crs(3857)
country = gpd.read_file(DATA / "ph_boundary.gpkg").to_crs(4326)
ph = gpd.clip(gpd.read_file(DATA / "wp_land.gpkg"), country.union_all()).to_crs(3857)

pts = gpd.GeoSeries(gpd.points_from_xy(df.LON, df.LAT), crs=4326).to_crs(3857)
xy = list(zip(pts.x, pts.y))
segs = [[xy[i], xy[i + 1]] for i in range(len(xy) - 1)]
colors = []
for w in df.USA_WIND.to_numpy()[:-1]:
    colors.append(ACCENT if w >= 137 else "#f4a261" if w >= 96 else "#f4d35e" if w >= 64 else WATER)

fig, ax = plt.subplots(figsize=(11, 12), facecolor=PAPER)
ax.set_facecolor(PAPER)
land.plot(ax=ax, color="#0d1620", edgecolor="#16222e", linewidth=0.2, zorder=1)
ph.plot(ax=ax, color="#22384b", edgecolor="#2b4155", linewidth=0.3, zorder=2)
ax.add_collection(LineCollection(segs, colors=colors, linewidths=2.6, zorder=4))
ax.add_collection(LineCollection(segs, colors=colors, linewidths=9, alpha=0.08, zorder=3))

peak = df.loc[df.USA_WIND.idxmax()]
peak_pt = gpd.GeoSeries([gpd.points_from_xy([peak.LON], [peak.LAT])[0]], crs=4326).to_crs(3857).iloc[0]
batanes = gpd.GeoSeries([gpd.points_from_xy([121.97], [20.45])[0]], crs=4326).to_crs(3857).iloc[0]
nearest = df.loc[((df.LON - 121.97) ** 2 + (df.LAT - 20.45) ** 2).idxmin()]
near_pt = gpd.GeoSeries([gpd.points_from_xy([nearest.LON], [nearest.LAT])[0]], crs=4326).to_crs(3857).iloc[0]
ax.annotate(f"Closest approach\n{nearest.ISO_TIME[:10]}", (near_pt.x, near_pt.y),
            xytext=(-10, -18), textcoords="offset points", ha="right", color=INK,
            fontsize=9, fontfamily=FONT,
            path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)])
ax.annotate(f"Peak {int(peak.USA_WIND)} kt", (peak_pt.x, peak_pt.y),
            xytext=(8, 12), textcoords="offset points", ha="left", color=INK, fontsize=9,
            fontfamily=FONT, path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)])

ax.annotate("Batanes", (batanes.x, batanes.y), xytext=(8, 0), textcoords="offset points",
            color=INK, fontsize=10, fontfamily=FONT, fontweight="bold",
            path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)], zorder=6)

ax.set_aspect("equal")
ax.axis("off")
west, south, east, north = gpd.GeoSeries(
    [box(116, 14, 133, 24)], crs=4326
).to_crs(3857).total_bounds
ax.set_xlim(west, east)
ax.set_ylim(south, north)

fig.text(0.07, 0.945, "P R O M P T I N G  O N L Y", color=ACCENT, fontsize=15,
         fontfamily=FONT, fontweight="bold")
fig.text(0.07, 0.905, "The strongest storm of 2026", color=INK, fontsize=26,
         fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.865,
         "Super Typhoon Champi — Rosal in the Philippines — at its closest approach to Batanes\n"
         "on 21 October 2026, with Signal No. 2 raised. This map was produced end-to-end from\n"
         "a single prompt: no hand-edited geometry, no manual styling.",
         color=INK, alpha=0.8, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.035,
         "Data: IBTrACS v04r01 (NOAA/NCEI) · Boundary: © OpenStreetMap contributors  ·  "
         "#30DayMapChallenge 2026 · Day 10 · Prompting only",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.06, right=0.94, top=0.825, bottom=0.06)
out = OUT / "day10_prompting.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out)
