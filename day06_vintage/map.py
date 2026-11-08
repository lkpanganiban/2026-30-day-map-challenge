"""Day 6 - Vintage.

Mayon and its towns, drawn in the dress of a 19th-century mapa.
The mountain that buried Cagsawa in 1814 is still the same mountain.
"""
import json
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from shapely.geometry import Point, box

from osm import to_gdf
from style import DATA

OUT = Path(__file__).parent
PAPER = "#e9dcbf"
INK = "#4a3826"
ACCENT = "#9b3a2a"
SERIF = "Baskerville"
SUMMIT = (123.6855, 13.2573)
CAGSAWA = (123.6947, 13.1647)


buildings = to_gdf(json.loads((DATA / "mayon_buildings.json").read_text())).to_crs(32651)
places = gpd.read_file(DATA / "mayon_places.gpkg").to_crs(32651)
roads = places[places.geom_type == "LineString"]
towns = places[(places.geom_type == "Point") & (places.place.isin(["city", "town"]))]
summit = gpd.GeoSeries([Point(*SUMMIT)], crs=4326).to_crs(32651).iloc[0]
cagsawa = gpd.GeoSeries([Point(*CAGSAWA)], crs=4326).to_crs(32651).iloc[0]
zone = gpd.GeoSeries([summit.buffer(6000)], crs=32651)

fig, ax = plt.subplots(figsize=(12, 14), facecolor=PAPER)
ax.set_facecolor(PAPER)

buildings.plot(ax=ax, color="#5c4a33", markersize=0.35, alpha=0.16, zorder=1)
roads.plot(ax=ax, color="#8f7a55", linewidth=0.6, alpha=0.9, zorder=2)

zone.boundary.plot(ax=ax, color=ACCENT, linewidth=0.9, alpha=0.75,
                   linestyle=(0, (6, 3)), zorder=3)
zone.boundary.plot(ax=ax, color=ACCENT, linewidth=3, alpha=0.06, zorder=2.5)

for _, t in towns.iterrows():
    ax.annotate(t["name"].upper(), (t.geometry.x, t.geometry.y), xytext=(0, 6),
                textcoords="offset points", ha="center", color=INK,
                fontsize=8.5, fontfamily=SERIF, zorder=6,
                path_effects=[pe.withStroke(linewidth=2.5, foreground=PAPER)])

ax.scatter([summit.x], [summit.y], marker="^", s=70, color=ACCENT, zorder=6)
ax.annotate("VOLCAN MAYON\n2,462 m", (summit.x, summit.y), xytext=(0, 11),
            textcoords="offset points", ha="center", color=INK, fontsize=9,
            fontfamily=SERIF, fontweight="bold", linespacing=1.3, zorder=7,
            path_effects=[pe.withStroke(linewidth=2.5, foreground=PAPER)])

ax.scatter([cagsawa.x], [cagsawa.y], marker="P", s=36, color=INK, zorder=6)
ax.annotate("Cagsawa\n(1814)", (cagsawa.x, cagsawa.y), xytext=(7, -4),
            textcoords="offset points", color=INK, fontsize=8,
            fontfamily=SERIF, style="italic", zorder=6,
            path_effects=[pe.withStroke(linewidth=2.5, foreground=PAPER)])

# compass rose, upper right
cx, cy = 123.80, 13.335
compass = gpd.GeoSeries([Point(cx, cy)], crs=4326).to_crs(32651).iloc[0]
cx, cy = compass.x, compass.y
ax.annotate("", (cx, cy + 2600), (cx, cy - 2600),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4), zorder=6)
ax.annotate("N", (cx, cy + 2900), ha="center", color=INK, fontsize=11,
            fontfamily=SERIF, fontweight="bold", zorder=6,
            path_effects=[pe.withStroke(linewidth=2.5, foreground=PAPER)])

ax.set_aspect("equal")
ax.axis("off")
minx, miny, maxx, maxy = gpd.GeoSeries(
    [box(123.54, 13.11, 123.84, 13.37)], crs=4326
).to_crs(32651).total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)

# double rule border
for pad, lw in [(0.018, 1.6), (0.026, 0.6)]:
    fig.add_artist(Rectangle((0.05 + pad / 2, 0.05 + pad / 2), 0.90 - pad, 0.90 - pad,
                             transform=fig.transFigure, fill=False, edgecolor=INK,
                             linewidth=lw, alpha=0.8))

fig.text(0.5, 0.925, "MAPA  DEL  VOLCAN  MAYON", color=INK, fontsize=24,
         fontfamily=SERIF, fontweight="bold", ha="center")
fig.text(0.5, 0.905, "y de sus contornos  ·  Albay, Islas Filipinas", color=INK,
         fontsize=12, fontfamily=SERIF, style="italic", ha="center")
fig.text(0.5, 0.885,
         "The cone that buried Cagsawa in 1814 is still the same cone.",
         color=ACCENT, fontsize=10, fontfamily=SERIF, ha="center")

fig.text(0.07, 0.035,
         "After the manner of a 19th-century mapa  ·  Data: © OpenStreetMap contributors  ·  "
         "#30DayMapChallenge 2026 · Day 6 · Vintage",
         color=INK, alpha=0.6, fontsize=8, fontfamily=SERIF)

fig.subplots_adjust(left=0.08, right=0.92, top=0.865, bottom=0.06)
out = OUT / "day06_vintage.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out)
