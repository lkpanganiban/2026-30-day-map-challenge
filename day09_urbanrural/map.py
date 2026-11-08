"""Day 9 - Urban-rural.

Land use across Metro Manila and its fringe: the residential city, the
industrial belt, and the farmland and forest still holding the edge.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from style import ACCENT, DATA, FONT, INK, PAPER

OUT = Path(__file__).parent
land = gpd.read_file(DATA / "mm_landuse.gpkg").to_crs(32651)
roads = gpd.read_file(DATA / "mm_roads.gpkg").to_crs(32651)

COLORS = {
    "residential": "#c9b79c",
    "commercial": ACCENT,
    "industrial": "#9b5de5",
    "farmland": "#8a9a5b",
    "forest": "#2d6a4f",
    "meadow": "#b5c99a",
    "orchard": "#6a994e",
}
areas = (land.assign(km2=land.area / 1e6).groupby("landuse").km2.sum()
         .sort_values(ascending=False))

fig, ax = plt.subplots(figsize=(12, 12), facecolor=PAPER)
ax.set_facecolor(PAPER)
roads.plot(ax=ax, color="#22323f", linewidth=0.3, zorder=1)
for use, color in COLORS.items():
    land[land.landuse == use].plot(ax=ax, color=color, linewidth=0, alpha=0.85, zorder=2)

ax.set_aspect("equal")
ax.axis("off")
minx, miny, maxx, maxy = land.total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)

handles = [Line2D([0], [0], marker="s", linestyle="", markersize=9, color=c,
                  label=f"{u}  ·  {areas.get(u, 0):,.0f} km²")
           for u, c in COLORS.items()]
ax.legend(handles=handles, loc="upper left", frameon=True, facecolor=PAPER,
          edgecolor="#2b4155", labelcolor=INK, fontsize=9, framealpha=0.9,
          title="Land use", title_fontsize=9)

leg = ax.get_legend()
leg.get_title().set_color(INK)
leg.get_title().set_fontfamily(FONT)
for t in leg.get_texts():
    t.set_fontfamily(FONT)

fig.text(0.07, 0.945, "U R B A N  –  R U R A L", color=ACCENT, fontsize=15,
         fontfamily=FONT, fontweight="bold")
fig.text(0.07, 0.905, "Where the city ends", color=INK, fontsize=26,
         fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.865,
         "Land use across Metro Manila and its fringe. 4,016 residential patches, 1,524 industrial,\n"
         "894 commercial — and only 264 of farmland still holding the edge. The city's last green\n"
         "fringe is also where the 2026 monsoon floods pushed hardest against the suburbs.",
         color=INK, alpha=0.8, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.035,
         "Data: © OpenStreetMap contributors  ·  #30DayMapChallenge 2026 · Day 9 · Urban–rural",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.06, right=0.94, top=0.79, bottom=0.06)
out = OUT / "day09_urbanrural.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out)
