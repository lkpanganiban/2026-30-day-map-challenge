"""Day 22 - Projections.

The same archipelago under Mercator, Equal Earth, and an azimuthal
equidistant view centred on Manila.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from shapely.geometry import box

from style import ACCENT, DATA, FONT, INK, PAPER

OUT = Path(__file__).parent
land = gpd.read_file(DATA / "ph_land.gpkg").to_crs(4326)
country = gpd.read_file(DATA / "ph_boundary.gpkg").to_crs(4326)
BBOX = gpd.GeoSeries([box(114, 4, 128, 22)], crs=4326).iloc[0]
land = gpd.clip(land, BBOX)

PROJECTIONS = [
    ("Mercator", "EPSG:3857", "shapes and bearings, at the cost of area"),
    ("Equal Earth", "EPSG:8857", "areas stay honest; shapes bend"),
    ("Azimuthal, from Manila", "+proj=aeqd +lat_0=14.6 +lon_0=121 +datum=WGS84 +units=m",
     "distance from one point, in every direction"),
]

fig, axes = plt.subplots(1, 3, figsize=(18, 10), facecolor=PAPER)
for ax, (name, crs, note) in zip(axes, PROJECTIONS):
    ax.set_facecolor(PAPER)
    l = land.to_crs(crs)
    c = country.to_crs(crs)
    l.plot(ax=ax, color="#22384b", edgecolor="#2b4155", linewidth=0.25, zorder=1)
    c.boundary.plot(ax=ax, color=INK, linewidth=0.5, alpha=0.35,
                    linestyle=(0, (3, 3)), zorder=2)
    if "aeqd" in crs:
        for km in (500, 1000, 1500):
            ax.add_patch(Circle((0, 0), km * 1000, fill=False, color=ACCENT,
                                linewidth=0.7, alpha=0.35, linestyle=(0, (2, 4)), zorder=2))
            ax.text(km * 0.71 * 1000, km * 0.71 * 1000, f" {km} km", color=ACCENT,
                    fontsize=7, fontfamily=FONT, alpha=0.7, ha="left", va="bottom",
                    clip_on=True)
    minx, miny, maxx, maxy = l.total_bounds
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(name, color=INK, fontsize=15, fontfamily=FONT, fontweight="bold", pad=14)
    ax.text(0.5, -0.075, note, transform=ax.transAxes, ha="center", va="top",
            color=INK, fontsize=9, fontfamily=FONT, alpha=0.65)

fig.text(0.05, 0.945, "P R O J E C T I O N S", color=ACCENT, fontsize=15,
         fontfamily=FONT, fontweight="bold")
fig.text(0.05, 0.905, "The shape you choose", color=INK, fontsize=26,
         fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.05, 0.865,
         "The same islands, three ways. Mercator keeps bearings but inflates area; Equal Earth\n"
         "keeps area but bends shape; the azimuthal view measures everything from Manila.\n"
         "An archipelago is always an argument about what a map should preserve.",
         color=INK, alpha=0.82, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.05, 0.025,
         "Boundary: © OpenStreetMap contributors · Land: Natural Earth  ·  "
         "#30DayMapChallenge 2026 · Day 22 · Projections",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.03, right=0.97, top=0.70, bottom=0.13, wspace=0.05)
out = OUT / "day22_projections.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out)
