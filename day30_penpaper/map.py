"""Day 30 - Pen & paper.

A printable A4 tracing sheet for Mayon: coastline, roads, towns and the
6 km danger zone in black line work. The final map is drawn by hand.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from shapely.geometry import Point, box

from style import DATA

OUT = Path(__file__).parent
INK = "#111111"
SUMMIT = (123.6855, 13.2573)

land = gpd.read_file(DATA / "ph_land.gpkg").to_crs(32651)
places = gpd.read_file(DATA / "mayon_places.gpkg").to_crs(32651)
roads = places[places.geom_type == "LineString"]
towns = places[(places.geom_type == "Point") & (places.place.isin(["city", "town"]))]
summit = gpd.GeoSeries([Point(*SUMMIT)], crs=4326).to_crs(32651).iloc[0]
zone = gpd.GeoSeries([summit.buffer(6000)], crs=32651)

fig = plt.figure(figsize=(8.27, 11.69))  # A4 portrait
ax = fig.add_axes([0.08, 0.10, 0.84, 0.74])
ax.set_facecolor("white")

land.plot(ax=ax, color="none", edgecolor=INK, linewidth=0.7, zorder=1)
roads.clip(land.union_all()).plot(ax=ax, color=INK, linewidth=0.35, alpha=0.65, zorder=2)
zone.boundary.plot(ax=ax, color=INK, linewidth=0.9, linestyle=(0, (4, 3)), zorder=3)

for _, t in towns.iterrows():
    ax.annotate(t["name"].upper(), (t.geometry.x, t.geometry.y), xytext=(0, 4),
                textcoords="offset points", ha="center", color=INK,
                fontsize=6.5, fontfamily="Baskerville")

ax.scatter([summit.x], [summit.y], marker="^", s=45, color=INK, zorder=4)
ax.annotate("MAYON\n2,462 m", (summit.x, summit.y), xytext=(0, 8),
            textcoords="offset points", ha="center", color=INK, fontsize=7,
            fontfamily="Baskerville", fontweight="bold", linespacing=1.2)

minx, miny, maxx, maxy = gpd.GeoSeries(
    [box(123.54, 13.11, 123.84, 13.37)], crs=4326
).to_crs(32651).total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)
ax.set_aspect("equal")
ax.axis("off")

# 10 km scale bar
sx, sy = minx + 2000, miny + 2500
ax.plot([sx, sx + 10000], [sy, sy], color=INK, linewidth=2)
ax.text(sx + 5000, sy + 700, "10 km", ha="center", va="bottom", fontsize=6.5,
        fontfamily="Baskerville")

fig.add_artist(Rectangle((0.05, 0.05), 0.90, 0.90, transform=fig.transFigure,
                         fill=False, edgecolor=INK, linewidth=0.8))

fig.text(0.5, 0.935, "MAYON", ha="center", color=INK, fontsize=20,
         fontfamily="Baskerville", fontweight="bold")
fig.text(0.5, 0.912, "a map to draw by hand", ha="center", color=INK, fontsize=10,
         fontfamily="Baskerville", style="italic")
fig.text(0.5, 0.885,
         "Print this sheet. Trace the coast, roads and the dashed danger zone in ink.\n"
         "Add the ash plume, the evacuees, the names you know. Then photograph it.",
         ha="center", va="top", color=INK, fontsize=7.5, fontfamily="Baskerville",
         linespacing=1.5)

fig.text(0.5, 0.065,
         "Base data: © OpenStreetMap contributors  ·  #30DayMapChallenge 2026 · Day 30 · Pen & paper",
         ha="center", color=INK, fontsize=6, fontfamily="Baskerville")

pdf = OUT / "day30_penpaper.pdf"
png = OUT / "day30_penpaper.png"
fig.savefig(pdf, facecolor="white")
fig.savefig(png, dpi=150, facecolor="white")
print("wrote", pdf, png)
