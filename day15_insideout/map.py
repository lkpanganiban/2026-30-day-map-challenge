"""Day 15 - Inside out.

The map turned inside out: the seas are the subject, the islands the gaps.
The waters Tino crossed this week and Champi spun up in.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.collections import LineCollection
from shapely.geometry import box

from style import ACCENT, DATA, FONT, INK, PAPER

OUT = Path(__file__).parent
SEA = "#d8e6e3"
LAND = "#12202b"

land = gpd.read_file(DATA / "ph_land.gpkg").to_crs(3857)
country = gpd.read_file(DATA / "ph_boundary.gpkg").to_crs(3857)
tracks = pd.read_csv(DATA / "ibtracs_last3years.csv", skiprows=[1], low_memory=False)
tracks = tracks[(tracks.SEASON == 2026) & (tracks.NAME == "CHAMPI")].copy()
for c in ["LAT", "LON", "USA_WIND"]:
    tracks[c] = pd.to_numeric(tracks[c], errors="coerce")
tracks = tracks.dropna(subset=["LAT", "LON"])

fig, ax = plt.subplots(figsize=(11, 14), facecolor=SEA)
ax.set_facecolor(SEA)
land.plot(ax=ax, color=LAND, edgecolor="#2b4155", linewidth=0.4, zorder=2)
country.boundary.plot(ax=ax, color="#6f8a86", linewidth=0.6, alpha=0.6,
                      linestyle=(0, (4, 4)), zorder=3)

pts = gpd.GeoSeries(gpd.points_from_xy(tracks.LON, tracks.LAT), crs=4326).to_crs(3857)
xy = list(zip(pts.x, pts.y))
ax.add_collection(LineCollection([[xy[i], xy[i + 1]] for i in range(len(xy) - 1)],
                                colors=[ACCENT], linewidths=2.2, alpha=0.85, zorder=4))
near = ((tracks.LON - 125.3) ** 2 + (tracks.LAT - 20.6) ** 2).idxmin()
label_pt = gpd.GeoSeries([gpd.points_from_xy([tracks.loc[near, "LON"]], [tracks.loc[near, "LAT"]])[0]],
                         crs=4326).to_crs(3857).iloc[0]
ax.annotate("Champi · Rosal, 21 Oct", (label_pt.x, label_pt.y),
            xytext=(10, 8), textcoords="offset points", color=ACCENT, fontsize=9,
            fontfamily=FONT, fontweight="bold",
            path_effects=[pe.withStroke(linewidth=3, foreground=SEA)], zorder=6)

tino = gpd.GeoSeries([gpd.points_from_xy([123.65], [10.55])[0]], crs=4326).to_crs(3857).iloc[0]
gpd.GeoSeries([tino.buffer(120000)], crs=3857).boundary.plot(
    ax=ax, color=ACCENT, linewidth=1.1, alpha=0.8, linestyle=(0, (3, 4)), zorder=5)
ax.annotate("Tino · 4 Nov", (tino.x - 230000, tino.y + 30000),
            color=ACCENT, fontsize=9, fontfamily=FONT, fontweight="bold", ha="right",
            path_effects=[pe.withStroke(linewidth=3, foreground=SEA)], zorder=6)

seas = {
    "WEST PHILIPPINE SEA": (116.6, 15.6),
    "LUZON STRAIT": (121.3, 20.6),
    "PHILIPPINE SEA": (126.6, 15.0),
    "SIBUYAN SEA": (122.45, 12.35),
    "VISAYAN SEA": (123.55, 11.45),
    "SULU SEA": (120.2, 8.7),
    "CELEBES SEA": (123.6, 4.6),
    "BOHOL SEA": (124.3, 9.2),
}
for name, (lon, lat) in seas.items():
    pt = gpd.GeoSeries([gpd.points_from_xy([lon], [lat])[0]], crs=4326).to_crs(3857).iloc[0]
    ax.annotate(name, (pt.x, pt.y), ha="center", color="#3f5f5a", fontsize=10,
                fontfamily=FONT, fontweight="bold", alpha=0.9, zorder=5,
                path_effects=[pe.withStroke(linewidth=3, foreground=SEA)])

ax.set_aspect("equal")
ax.axis("off")
minx, miny, maxx, maxy = gpd.GeoSeries(
    [box(114, 4, 128, 22)], crs=4326
).to_crs(3857).total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)

fig.text(0.07, 0.945, "I N S I D E   O U T", color=ACCENT, fontsize=15,
         fontfamily=FONT, fontweight="bold")
fig.text(0.07, 0.905, "The sea between the islands", color=LAND, fontsize=26,
         fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.865,
         "Land and water swapped: the seas are the subject, the islands the gaps.\n"
         "Typhoon Tino crossed the Visayan Sea this week; Champi became the year's strongest\n"
         "storm over the Philippine Sea. The archipelago is mostly the space between.",
         color="#2f423f", alpha=0.9, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.035,
         "Data: © OpenStreetMap contributors · Natural Earth  ·  IBTrACS v04r01 (NOAA/NCEI)  ·  "
         "#30DayMapChallenge 2026 · Day 15 · Inside out",
         color="#3f5f5a", alpha=0.8, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.06, right=0.94, top=0.825, bottom=0.06)
out = OUT / "day15_insideout.png"
fig.savefig(out, dpi=200, facecolor=SEA)
print("wrote", out)
