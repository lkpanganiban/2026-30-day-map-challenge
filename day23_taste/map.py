"""Day 23 - Senses: Taste.

Where Metro Manila eats: 2,746 mapped food shops, with the wet markets
as the anchor of the everyday table.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from shapely.geometry import box

from style import ACCENT, DATA, FONT, INK, PAPER, WATER

OUT = Path(__file__).parent
food = gpd.read_file(DATA / "mm_food.gpkg").to_crs(3857)
land = gpd.read_file(DATA / "ph_land.gpkg").to_crs(3857)
roads = gpd.read_file(DATA / "mm_roads.gpkg").to_crs(3857)

markets = food[food.amenity == "marketplace"]
supermarkets = food[food.shop == "supermarket"]
fresh = food[food.shop.isin(["greengrocer", "butcher", "seafood"])]
bakeries = food[food.shop == "bakery"]

fig, ax = plt.subplots(figsize=(12, 12), facecolor=PAPER)
ax.set_facecolor(PAPER)
land.plot(ax=ax, color="#16222e", edgecolor="#2b4155", linewidth=0.3, zorder=1)
roads.plot(ax=ax, color="#22323f", linewidth=0.3, zorder=2)

ax.scatter(bakeries.geometry.x, bakeries.geometry.y, s=3, color="#c9b79c",
           alpha=0.75, linewidths=0, zorder=3)
ax.scatter(fresh.geometry.x, fresh.geometry.y, s=6, color="#8a9a5b",
           alpha=0.85, linewidths=0, zorder=4)
ax.scatter(supermarkets.geometry.x, supermarkets.geometry.y, s=8, color=WATER,
           alpha=0.9, linewidths=0, zorder=5)
ax.scatter(markets.geometry.x, markets.geometry.y, s=38, marker="*",
           color=ACCENT, edgecolor=PAPER, linewidth=0.5, zorder=6)

ax.set_aspect("equal")
ax.axis("off")
west, south, east, north = gpd.GeoSeries(
    [box(120.87, 14.45, 121.20, 14.79)], crs=4326
).to_crs(3857).total_bounds
ax.set_xlim(west, east)
ax.set_ylim(south, north)

handles = [
    plt.Line2D([0], [0], marker="*", linestyle="", markersize=11, color=ACCENT,
               label=f"wet markets · {len(markets)}"),
    plt.Line2D([0], [0], marker="o", linestyle="", markersize=5, color=WATER,
               label=f"supermarkets · {len(supermarkets)}"),
    plt.Line2D([0], [0], marker="o", linestyle="", markersize=5, color="#8a9a5b",
               label=f"butchers, greengrocers, fishmongers · {len(fresh)}"),
    plt.Line2D([0], [0], marker="o", linestyle="", markersize=4, color="#c9b79c",
               label=f"bakeries · {len(bakeries)}"),
]
ax.legend(handles=handles, loc="lower left", frameon=True, facecolor=PAPER,
          edgecolor="#2b4155", labelcolor=INK, fontsize=9, framealpha=0.9,
          title="Food retail", title_fontsize=9)
leg = ax.get_legend()
leg.get_title().set_color(INK)
for t in leg.get_texts():
    t.set_fontfamily(FONT)
leg.get_title().set_fontfamily(FONT)

fig.text(0.07, 0.945, "S E N S E S :   T A S T E", color=ACCENT, fontsize=15,
         fontfamily=FONT, fontweight="bold")
fig.text(0.07, 0.905, "The taste of the city", color=INK, fontsize=26,
         fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.865,
         f"{len(food):,} food shops mapped in Metro Manila: {len(bakeries):,} bakeries, "
         f"{len(markets)} wet markets,\nand the small butchers and greengrocers in between. "
         "When the floods close the roads,\nthe palengke is the last mile of the food supply chain.",
         color=INK, alpha=0.82, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.035,
         "Data: © OpenStreetMap contributors  ·  #30DayMapChallenge 2026 · Day 23 · Senses: Taste",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.06, right=0.94, top=0.825, bottom=0.06)
out = OUT / "day23_taste.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out, len(food), len(markets))
