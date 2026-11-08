"""Day 14 - Borgesian map.

Every building footprint OSM holds in central Tacloban, drawn as line work.
A map at the scale of the territory: 24,811 buildings, one by one.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import box

from style import DATA

OUT = Path(__file__).parent
PAPER = "#ece3cf"
INK = "#2f2a24"
ACCENT = "#9b3a2a"

detail = gpd.read_file(DATA / "tacloban_detail.gpkg").to_crs(32651)
buildings = detail[detail.geom_type == "Polygon"]
roads = detail[detail.geom_type == "LineString"]

fig, ax = plt.subplots(figsize=(13, 13), facecolor=PAPER)
ax.set_facecolor(PAPER)

roads.plot(ax=ax, color="#8d7d63", linewidth=0.45, zorder=1)
buildings.plot(ax=ax, facecolor="none", edgecolor=INK, linewidth=0.18, zorder=2)

minx, miny, maxx, maxy = gpd.GeoSeries(
    [box(124.975, 11.218, 125.032, 11.268)], crs=4326
).to_crs(32651).total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)
ax.set_aspect("equal")
ax.axis("off")

sx, sy = minx + 900, miny + 900
ax.plot([sx, sx + 1000], [sy, sy], color=INK, linewidth=2)
ax.annotate("1 km", (sx + 500, sy), xytext=(0, 6), textcoords="offset points",
            ha="center", color=INK, fontsize=8, fontfamily="Baskerville")

fig.text(0.07, 0.945, "B O R G E S I A N   M A P", color=ACCENT, fontsize=14,
         fontfamily="Baskerville", fontweight="bold")
fig.text(0.07, 0.905, "The map is the territory", color=INK, fontsize=27,
         fontfamily="Baskerville", fontweight="bold", va="top")
fig.text(0.07, 0.860,
         f"{len(buildings):,} building footprints in central Tacloban, every one drawn.\n"
         "In November 2013 Yolanda flattened this ground; the streets were rebuilt building\n"
         "by building, and mapped the same way. Scale: 1:1.",
         color=INK, alpha=0.85, fontsize=11, fontfamily="Baskerville",
         style="italic", linespacing=1.5, va="top")

fig.text(0.07, 0.035,
         "Data: © OpenStreetMap contributors  ·  #30DayMapChallenge 2026 · Day 14 · Borgesian map",
         color=INK, alpha=0.6, fontsize=9, fontfamily="Baskerville")

fig.subplots_adjust(left=0.06, right=0.94, top=0.82, bottom=0.06)
out = OUT / "day14_borges.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out, len(buildings))
