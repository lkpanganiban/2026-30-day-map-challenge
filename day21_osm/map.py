"""Day 21 - OpenStreetMap.

Every health facility mapped in the Philippines, and the ones within
50 km of the September 2025 Cebu earthquake.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from shapely.geometry import Point, box

from style import ACCENT, DATA, FONT, INK, PAPER

OUT = Path(__file__).parent
hospitals = gpd.read_file(DATA / "ph_hospitals.gpkg").to_crs(3857)
land = gpd.read_file(DATA / "ph_land.gpkg").to_crs(3857)

quakes = gpd.read_file(DATA / "ph_quakes.geojson")
quakes["depth"] = quakes.geometry.z
quakes = quakes.set_crs(4326, allow_override=True)
country = gpd.read_file(DATA / "ph_boundary.gpkg").to_crs(4326)
quakes = gpd.sjoin(quakes, country[["geometry"]], predicate="within")

box_mask = (quakes.geometry.y.between(10.7, 11.6)) & (quakes.geometry.x.between(123.6, 124.7))
cebu = quakes[box_mask].nlargest(1, "mag").iloc[0]
epi = gpd.GeoSeries([Point(cebu.geometry.x, cebu.geometry.y)], crs=4326).to_crs(32651).iloc[0]
ring = gpd.GeoSeries([epi.buffer(50000)], crs=32651)
near = hospitals.to_crs(32651)
inside = near[near.within(ring.iloc[0])]

fig, ax = plt.subplots(figsize=(11, 14), facecolor=PAPER)
ax.set_facecolor(PAPER)
land.plot(ax=ax, color="#16222e", edgecolor="#2b4155", linewidth=0.3, zorder=1)
ax.scatter(hospitals.geometry.x, hospitals.geometry.y, marker="+", s=14,
           color="#bcd3d9", linewidths=0.7, alpha=0.8, zorder=3)

ring.to_crs(3857).boundary.plot(ax=ax, color=ACCENT, linewidth=1, alpha=0.8,
                                linestyle=(0, (3, 3)), zorder=2)
epi_pt = gpd.GeoSeries([epi], crs=32651).to_crs(3857).iloc[0]
ax.scatter([epi_pt.x], [epi_pt.y], marker="*", s=260, color=ACCENT, zorder=5)
ax.annotate(f"M{cebu.mag} · 30 Sep 2025\n{len(inside)} hospitals within 50 km",
            (epi_pt.x, epi_pt.y), xytext=(-12, 16), textcoords="offset points",
            ha="right", color=INK, fontsize=9, fontfamily=FONT, linespacing=1.3,
            path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)], zorder=6)

ax.set_aspect("equal")
ax.axis("off")
minx, miny, maxx, maxy = gpd.GeoSeries([box(114, 4, 128, 22)], crs=4326).to_crs(3857).total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)

fig.text(0.07, 0.945, "O P E N S T R E E T M A P", color=ACCENT, fontsize=15,
         fontfamily=FONT, fontweight="bold")
fig.text(0.07, 0.905, "Every hospital the crowd knows", color=INK, fontsize=26,
         fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.865,
         f"{len(hospitals):,} health facilities mapped in OpenStreetMap across the Philippines.\n"
         f"{len(inside)} sit within 50 km of the September 2025 Cebu quake; when Typhoon Tino\n"
         "cut the roads this week, this layer is how responders find the ones still standing.",
         color=INK, alpha=0.82, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.035,
         "Data: © OpenStreetMap contributors (amenity=hospital)  ·  USGS  ·  "
         "#30DayMapChallenge 2026 · Day 21 · OpenStreetMap",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.05, right=0.95, top=0.825, bottom=0.06)
out = OUT / "day21_osm.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out, len(hospitals), "inside", len(inside))
