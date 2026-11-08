"""Day 3 - Polygons.

Mayon's 6 km Permanent Danger Zone against every building footprint
OpenStreetMap knows around the volcano. The 30 October 2026 eruption
forced 2,041 people out of these barangays.
"""
import json
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from shapely.geometry import Point, box

from osm import to_gdf
from style import ACCENT, DATA, FONT, INK, PAPER

OUT = Path(__file__).parent
BUILDINGS = DATA / "mayon_buildings.json"
PLACES = DATA / "mayon_places.gpkg"
SUMMIT = (123.6855, 13.2573)


buildings = to_gdf(json.loads(BUILDINGS.read_text())).to_crs(32651)
places = gpd.read_file(PLACES).to_crs(32651)
roads = places[places.geom_type == "LineString"]
towns = places[(places.geom_type == "Point") & (places.place.isin(["city", "town"]))]

summit = gpd.GeoSeries([Point(*SUMMIT)], crs=4326).to_crs(32651).iloc[0]
zone = gpd.GeoSeries([summit.buffer(6000)], crs=32651)
inside = buildings[buildings.within(zone.iloc[0])]

fig, ax = plt.subplots(figsize=(12, 13), facecolor=PAPER)
ax.set_facecolor(PAPER)

roads.plot(ax=ax, color="#22323f", linewidth=0.35, zorder=1)
buildings.plot(ax=ax, color="#465c6e", markersize=0.6, alpha=0.8, zorder=2)

zone.plot(ax=ax, color=ACCENT, alpha=0.10, zorder=3)
zone.boundary.plot(ax=ax, color=ACCENT, linewidth=1.1, alpha=0.9,
                   linestyle=(0, (5, 4)), zorder=4)
zone.boundary.plot(ax=ax, color=ACCENT, linewidth=4, alpha=0.08, zorder=3.5)

for _, t in towns.iterrows():
    ax.annotate(t["name"], (t.geometry.x, t.geometry.y), xytext=(0, 7),
                textcoords="offset points", ha="center",
                color=INK, fontsize=9, fontfamily=FONT,
                path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)], zorder=6)

ax.scatter([summit.x], [summit.y], marker="^", s=90, color=INK, zorder=6)
ax.annotate("Mayon · 2,462 m", (summit.x, summit.y), xytext=(0, 14),
            textcoords="offset points", ha="center", color=INK,
            fontsize=10, fontfamily=FONT, fontweight="bold",
            path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)], zorder=7)

ax.annotate("6 km Permanent Danger Zone", (summit.x, zone.iloc[0].bounds[3] - 1200),
            ha="center", color=ACCENT, fontsize=10, fontfamily=FONT, zorder=6,
            path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)])

ax.set_aspect("equal")
ax.axis("off")
minx, miny, maxx, maxy = gpd.GeoSeries(
    [box(123.52, 13.10, 123.86, 13.375)], crs=4326
).to_crs(32651).total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)

fig.text(0.07, 0.945, "P O L Y G O N S", color=ACCENT, fontsize=15, fontfamily=FONT,
         fontweight="bold")
fig.text(0.07, 0.905, "Inside the permanent danger zone", color=INK,
         fontsize=26, fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.865,
         f"{len(buildings):,} building footprints around Mayon; {len(inside):,} inside the 6 km zone.\n"
         "On 30 October 2026 a moderately explosive eruption sent an ash column 3,000 m high\n"
         "and forced 2,041 people to evacuate.",
         color=INK, alpha=0.8, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.035,
         "Data: © OpenStreetMap contributors  ·  Zone: 6 km buffer from Mayon summit  ·  "
         "#30DayMapChallenge 2026 · Day 3 · Polygons",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.06, right=0.94, top=0.835, bottom=0.06)
out = OUT / "day03_polygons.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out, "inside:", len(inside), "of", len(buildings))
