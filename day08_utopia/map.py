"""Day 8 - Utopia.

Every waterway OSM knows in Metro Manila, drawn as the spine of the city
that could have been: 13 years after Yolanda, and one flood-control scandal later.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import osmnx as ox

from style import ACCENT, DATA, FONT, INK, METRO_MANILA, PAPER, WATER

OUT = Path(__file__).parent
WATERWAYS = DATA / "mm_waterways.gpkg"
KEEP = ["river", "stream", "canal", "drain", "ditch"]


def load():
    if not WATERWAYS.exists():
        gdf = ox.features_from_bbox(METRO_MANILA, {"waterway": True})
        gdf = gdf[gdf["waterway"].isin(KEEP)][["waterway", "name", "geometry"]]
        gdf.to_file(WATERWAYS, driver="GPKG")
    return gpd.read_file(WATERWAYS).to_crs(32651)


water = load()
width = {"river": 3.2, "stream": 1.1, "canal": 1.6, "drain": 0.7, "ditch": 0.6}

fig, ax = plt.subplots(figsize=(12, 13), facecolor=PAPER)
ax.set_facecolor(PAPER)

# glow underlay then bright line: the city's circulatory system
for t, w in width.items():
    lines = water[water["waterway"] == t]
    lines.plot(ax=ax, color=WATER, linewidth=w * 5, alpha=0.08, zorder=2)
    lines.plot(ax=ax, color=WATER, linewidth=w, alpha=0.95, zorder=3)

labels = {
    "Manila": (120.9842, 14.5995),
    "Quezon City": (121.0437, 14.6760),
    "Caloocan": (120.9670, 14.6500),
    "Pasig": (121.0851, 14.5764),
    "Marikina": (121.1029, 14.6507),
    "Taguig": (121.0509, 14.5176),
    "Pasay": (120.9945, 14.5378),
    "Makati": (121.0244, 14.5547),
}
for name, (lon, lat) in labels.items():
    pt = gpd.GeoSeries([gpd.points_from_xy([lon], [lat])[0]], crs=4326).to_crs(32651).iloc[0]
    ax.annotate(
        name,
        (pt.x, pt.y),
        color=INK,
        alpha=0.8,
        fontsize=10,
        fontfamily=FONT,
        ha="center",
        zorder=4,
        path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)],
    )

river_pts = {"Pasig River": (121.005, 14.572), "Marikina River": (121.095, 14.640)}
for name, (lon, lat) in river_pts.items():
    pt = gpd.GeoSeries([gpd.points_from_xy([lon], [lat])[0]], crs=4326).to_crs(32651).iloc[0]
    ax.annotate(name, (pt.x, pt.y), color=WATER, fontsize=9,
                fontfamily=FONT, style="italic", zorder=4)

minx, miny, maxx, maxy = water.total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)
ax.set_aspect("equal")
ax.axis("off")

fig.text(0.07, 0.945, "U T O P I A", color=ACCENT, fontsize=15, fontfamily=FONT,
         fontweight="bold")
fig.text(0.07, 0.895, "A Metro Manila that does not flood", color=INK,
         fontsize=26, fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.845,
         "Every river, creek, canal and drain OpenStreetMap knows in Metro Manila —\n"
         "drawn as the flood-control spine the city could have built.\n"
         "Thirteen years after Yolanda, on the week Typhoon Tino cut through Cebu and Negros.",
         color=INK, alpha=0.8, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.035,
         "Data: © OpenStreetMap contributors  ·  #30DayMapChallenge 2026 · Day 8 · Utopia",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.05, right=0.95, top=0.775, bottom=0.06)
out = OUT / "day08_utopia.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out)
