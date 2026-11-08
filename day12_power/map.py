"""Day 12 - Power.

Every transmission line mapped in OpenStreetMap, coloured by voltage —
and the Bataan Nuclear Power Plant, finished in 1984, never switched on.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
from shapely.geometry import box

from style import ACCENT, DATA, FONT, INK, PAPER, WATER

OUT = Path(__file__).parent
lines = gpd.read_file(DATA / "ph_powerlines.gpkg").to_crs(3857)
subs = gpd.read_file(DATA / "ph_power.gpkg")
subs = subs[subs.power == "substation"].to_crs(3857)
land = gpd.read_file(DATA / "ph_land.gpkg").to_crs(3857)

lines["kv"] = pd.to_numeric(lines.voltage, errors="coerce")
BANDS = [(500000, ACCENT, "500 kV"), (230000, "#f4a261", "230 kV"),
         (138000, "#f4d35e", "138 kV"), (115000, WATER, "115 kV"),
         (69000, "#7f9bb3", "69 kV")]

fig, ax = plt.subplots(figsize=(11, 14), facecolor=PAPER)
ax.set_facecolor(PAPER)
land.plot(ax=ax, color="#16222e", edgecolor="#2b4155", linewidth=0.3, zorder=1)

for kv, color, _ in BANDS:
    lo = kv if kv < 230000 else kv * 0.99
    hi = kv * 1.01
    lines[(lines.kv >= lo) & (lines.kv <= hi)].plot(
        ax=ax, color=color, linewidth=0.8, alpha=0.9, zorder=3)
lines[lines.kv < 69000].plot(ax=ax, color="#4d6377", linewidth=0.5, zorder=2)

subs.plot(ax=ax, color=INK, markersize=2.2, alpha=0.7, zorder=4)

bnpp = gpd.GeoSeries([gpd.points_from_xy([120.4678], [14.6294])[0]], crs=4326).to_crs(3857).iloc[0]
ax.scatter([bnpp.x], [bnpp.y], marker="*", s=280, color=ACCENT, zorder=6)
ax.annotate("Bataan Nuclear Power Plant\ncompleted 1984 · never operated",
            (bnpp.x, bnpp.y), xytext=(-14, 18), textcoords="offset points",
            ha="right", color=INK, fontsize=9, fontfamily=FONT, linespacing=1.3,
            path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)], zorder=6)

handles = [Line2D([0], [0], color=c, lw=2, label=f"{name}  ({len(lines[(lines.kv >= (kv if kv < 230000 else kv*0.99)) & (lines.kv <= kv*1.01)])})")
           for kv, c, name in BANDS]
ax.legend(handles=handles, loc="lower left", frameon=True, facecolor=PAPER,
          edgecolor="#2b4155", labelcolor=INK, fontsize=9, title="Transmission voltage",
          title_fontsize=9, framealpha=0.9)
leg = ax.get_legend()
leg.get_title().set_color(INK)
leg.get_title().set_fontfamily(FONT)
for t in leg.get_texts():
    t.set_fontfamily(FONT)

ax.set_aspect("equal")
ax.axis("off")
minx, miny, maxx, maxy = gpd.GeoSeries(
    [box(114, 4.2, 127, 19.5)], crs=4326
).to_crs(3857).total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)

fig.text(0.07, 0.945, "P O W E R", color=ACCENT, fontsize=15, fontfamily=FONT,
         fontweight="bold")
fig.text(0.07, 0.905, "The grid, and the plant we never turned on", color=INK,
         fontsize=24, fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.867,
         f"{len(lines):,} transmission lines mapped in OpenStreetMap, coloured by voltage.\n"
         "This week Typhoon Tino cut power across Cebu and Negros — the grid that has to\n"
         "carry the recovery. Bataan's nuclear plant has sat silent since 1984.",
         color=INK, alpha=0.8, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.035,
         "Data: © OpenStreetMap contributors  ·  #30DayMapChallenge 2026 · Day 12 · Power",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.06, right=0.94, top=0.825, bottom=0.06)
out = OUT / "day12_power.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out)
