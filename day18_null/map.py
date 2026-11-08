"""Day 18 - NULL.

Every 2026 typhoon track in the official best-track archive is here.
Kalmaegi (Tino), which hit Cebu on 4 November, is not — it is too new
to have been processed. NULL is not "no storm"; it is "not yet data".
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.collections import LineCollection
from shapely.geometry import Point, box

from style import ACCENT, DATA, FONT, INK, PAPER

OUT = Path(__file__).parent
tracks = pd.read_csv(DATA / "ibtracs_last3years.csv", skiprows=[1], low_memory=False)
tracks = tracks[(tracks.SEASON == 2026) & (tracks.NAME != "UNNAMED")].copy()
for c in ["LAT", "LON", "USA_WIND"]:
    tracks[c] = pd.to_numeric(tracks[c], errors="coerce")
tracks = tracks.dropna(subset=["LAT", "LON"])
in_par = tracks.groupby("NAME").apply(
    lambda g: ((g.LON.between(114.5, 127)) & (g.LAT.between(4.5, 22))).any(),
    include_groups=False)
tracks = tracks[tracks.NAME.isin(in_par[in_par].index)]

land = gpd.read_file(DATA / "wp_land.gpkg").to_crs(3857)
country = gpd.read_file(DATA / "ph_boundary.gpkg").to_crs(4326)
ph = gpd.clip(gpd.read_file(DATA / "wp_land.gpkg"), country.union_all()).to_crs(3857)

fig, ax = plt.subplots(figsize=(12, 12), facecolor=PAPER)
ax.set_facecolor(PAPER)
land.plot(ax=ax, color="#0d1620", edgecolor="#16222e", linewidth=0.2, zorder=1)
ph.plot(ax=ax, color="#1d3142", edgecolor="#2b4155", linewidth=0.3, zorder=2)

for name, g in tracks.groupby("NAME"):
    pts = gpd.GeoSeries(gpd.points_from_xy(g.LON, g.LAT), crs=4326).to_crs(3857)
    xy = list(zip(pts.x, pts.y))
    ax.add_collection(LineCollection([[xy[i], xy[i + 1]] for i in range(len(xy) - 1)],
                                    colors=["#4d6377"], linewidths=1.2, alpha=0.55, zorder=3))

tino = gpd.GeoSeries([Point(123.65, 10.55)], crs=4326).to_crs(3857).iloc[0]
gpd.GeoSeries([tino.buffer(170000)], crs=3857).boundary.plot(
    ax=ax, color=ACCENT, linewidth=1.3, alpha=0.9, linestyle=(0, (4, 5)), zorder=4)
ax.annotate("NULL", (tino.x, tino.y + 20000), ha="center", va="center",
            color=ACCENT, fontsize=30, fontfamily=FONT, fontweight="bold",
            path_effects=[pe.withStroke(linewidth=4, foreground=PAPER)], zorder=6)
ax.annotate("Kalmaegi · Tino\n4 November 2026", (tino.x, tino.y - 90000), ha="center",
            color=INK, fontsize=10, fontfamily=FONT, linespacing=1.4,
            path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)], zorder=6)

ax.set_aspect("equal")
ax.axis("off")
minx, miny, maxx, maxy = gpd.GeoSeries(
    [box(114, 4, 128, 22)], crs=4326
).to_crs(3857).total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)

fig.text(0.07, 0.945, "N U L L", color=ACCENT, fontsize=15, fontfamily=FONT,
         fontweight="bold")
fig.text(0.07, 0.905, "The storm that isn't here", color=INK, fontsize=26,
         fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.865,
         "Every 2026 track in the official best-track archive is drawn in grey. The one that hit\n"
         "Cebu this week is missing: Kalmaegi, named Tino here, is too new to have been processed.\n"
         "NULL is not 'no storm'. It is 'not yet data' — and the damage is already real.",
         color=INK, alpha=0.82, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.035,
         "Data: IBTrACS v04r01 (NOAA/NCEI), compiled 7 Nov 2026  ·  Boundary: © OpenStreetMap contributors  ·  "
         "#30DayMapChallenge 2026 · Day 18 · NULL",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.05, right=0.95, top=0.80, bottom=0.06)
out = OUT / "day18_null.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out)
