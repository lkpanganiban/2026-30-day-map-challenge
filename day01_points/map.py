"""Day 1 - Points.

Every M5+ earthquake in Philippine waters since November 2024, as points.
Two years of shaking: Sarangani M7.8, Eastern Mindanao M7.4, Cebu M6.9.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import pandas as pd
import requests

from style import ACCENT, DATA, FONT, INK, PAPER, PH, WATER

OUT = Path(__file__).parent
QUAKES = DATA / "ph_quakes.geojson"
BOUNDARY = DATA / "ph_boundary.gpkg"
LAND = DATA / "ph_land.gpkg"
START = "2024-11-01"


def load():
    if not QUAKES.exists():
        r = requests.get(
            "https://earthquake.usgs.gov/fdsnws/event/1/query",
            params={
                "format": "geojson", "starttime": START, "minmagnitude": 5,
                "minlatitude": PH[1], "maxlatitude": PH[3],
                "minlongitude": PH[0], "maxlongitude": PH[2],
            },
            timeout=120,
        )
        r.raise_for_status()
        QUAKES.write_text(r.text)
    quakes = gpd.read_file(QUAKES)
    quakes["depth"] = quakes["geometry"].map(lambda g: g.z)
    quakes = quakes.set_crs(4326, allow_override=True)

    country = gpd.read_file(BOUNDARY).to_crs(4326)
    quakes = gpd.sjoin(quakes, country[["geometry"]], predicate="within")
    land = gpd.read_file(LAND).to_crs(4326)
    return quakes.to_crs(3857), land.to_crs(3857), country.to_crs(3857)


quakes, land, country = load()

fig, ax = plt.subplots(figsize=(11, 14), facecolor=PAPER)
ax.set_facecolor(PAPER)

land.plot(ax=ax, color="#16222e", edgecolor="#2b4155", linewidth=0.3, zorder=1)
country.boundary.plot(ax=ax, color=INK, linewidth=0.5, alpha=0.25,
                      linestyle=(0, (4, 4)), zorder=1.5)

shallow = quakes["depth"] < 70
intermediate = quakes["depth"].between(70, 300)
deep = quakes["depth"] > 300
sizes = (quakes["mag"] - 4) ** 3 * 4

for mask, color, z in [
    (deep, WATER, 2),
    (intermediate, "#f4a261", 3),
    (shallow, ACCENT, 4),
]:
    q = quakes[mask]
    ax.scatter(q.geometry.x, q.geometry.y, s=sizes[mask], color=color,
               alpha=0.85, linewidths=0, zorder=z)
    ax.scatter(q.geometry.x, q.geometry.y, s=sizes[mask] * 3.2, color=color,
               alpha=0.07, linewidths=0, zorder=z - 0.1)

big = quakes.nlargest(3, "mag")
label_offsets = {7.8: (14, -18), 7.4: (-12, 12), 6.9: (-14, 10)}
names = {"Kablalan": "Sarangani", "Santiago": "Eastern Mindanao", "Calape": "Cebu"}
for _, q in big.iterrows():
    short = names.get(q["place"].split(" of ")[-1].split(",")[0], q["place"])
    ax.annotate(
        f"M{q['mag']} {short}",
        (q.geometry.x, q.geometry.y),
        xytext=label_offsets.get(q["mag"], (10, 12)), textcoords="offset points",
        ha="left" if label_offsets.get(q["mag"], (10, 0))[0] > 0 else "right",
        color=INK, fontsize=9, fontfamily=FONT, fontweight="bold",
        path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)],
        zorder=6,
    )

legend_ax = ax.inset_axes([0.03, 0.06, 0.30, 0.13])
legend_ax.set_facecolor(PAPER)
legend_ax.patch.set_alpha(0.9)
legend_ax.set_xticks([])
legend_ax.set_yticks([])
for spine in legend_ax.spines.values():
    spine.set_visible(False)
for i, mag in enumerate([5, 6, 7]):
    legend_ax.scatter([0.05], [0.8 - i * 0.3], s=(mag - 4) ** 3 * 4,
                      color=INK, alpha=0.8, linewidths=0)
    legend_ax.text(0.16, 0.8 - i * 0.3, f"M{mag}", color=INK, fontsize=9,
                   fontfamily=FONT, va="center")
legend_ax.text(0.55, 0.8, "shallow", color=ACCENT, fontsize=9, fontfamily=FONT)
legend_ax.text(0.55, 0.5, "70–300 km", color="#f4a261", fontsize=9, fontfamily=FONT)
legend_ax.text(0.55, 0.2, "deep", color=WATER, fontsize=9, fontfamily=FONT)
legend_ax.set_xlim(0, 1)
legend_ax.set_ylim(0, 1)

ax.set_aspect("equal")
ax.axis("off")
minx, miny, maxx, maxy = country.total_bounds
ax.set_xlim(minx - 100_000, maxx + 100_000)
ax.set_ylim(miny - 100_000, maxy + 100_000)

fig.text(0.07, 0.95, "P O I N T S", color=ACCENT, fontsize=15, fontfamily=FONT,
         fontweight="bold")
fig.text(0.07, 0.915, f"{len(quakes)} earthquakes, two years", color=INK,
         fontsize=26, fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.875,
         "Every magnitude 5+ earthquake in Philippine territory since November 2024, "
         "sized by magnitude.\nThe M7.8 Sarangani quake of 8 June 2026, the M7.4 Eastern "
         "Mindanao quake of last October,\nand the M6.9 that shook Cebu on 30 September 2025 "
         "are all on this page.",
         color=INK, alpha=0.8, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.035,
         "Data: USGS Earthquake Catalog · Boundary: © OpenStreetMap contributors  ·  "
         "#30DayMapChallenge 2026 · Day 1 · Points",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.06, right=0.94, top=0.845, bottom=0.06)
out = OUT / "day01_points.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out, len(quakes), "quakes")
