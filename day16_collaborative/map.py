"""Day 16 - Collaborative map.

The OpenStreetMap community's edits in the Cebu–Negros box since Typhoon Tino
made landfall on 4 November 2026, coloured by mapper.
"""
import xml.etree.ElementTree as ET
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from shapely.geometry import Point, box

from style import ACCENT, DATA, FONT, INK, PAPER, WATER

OUT = Path(__file__).parent
BBOX = (123.3, 9.6, 124.6, 11.4)
COLORS = {"Totor": ACCENT, "junyeah": "#f4a261", "imiraldz": "#f4d35e",
          "DodaBettaMountain": "#b388eb", "RusumoFalls": WATER}

root = ET.parse(DATA / "cebu_changesets.xml").getroot()
rows = []
for c in root.findall("changeset"):
    rows.append({
        "user": c.get("user"),
        "time": c.get("created_at"),
        "post": c.get("created_at") >= "2026-11-04",
        "geometry": box(float(c.get("min_lon")), float(c.get("min_lat")),
                        float(c.get("max_lon")), float(c.get("max_lat"))),
    })
changes = gpd.GeoDataFrame(rows, crs=4326).to_crs(3857)
pre = changes[~changes.post]
changes = changes[changes.post]
land = gpd.read_file(DATA / "ph_land.gpkg").to_crs(3857).clip(
    gpd.GeoSeries([box(*BBOX)], crs=4326).to_crs(3857).iloc[0])
land = land[land.geometry.notna()]
roads = gpd.read_file(DATA / "cebu_roads.gpkg").to_crs(3857)

fig, ax = plt.subplots(figsize=(11, 13), facecolor=PAPER)
ax.set_facecolor(PAPER)
land.plot(ax=ax, color="#1d3142", edgecolor="#2b4155", linewidth=0.3, zorder=1)
roads.plot(ax=ax, color="#2a4055", linewidth=0.4, zorder=2)
pre.plot(ax=ax, facecolor="#4d6377", alpha=0.04, edgecolor="#4d6377",
         linewidth=0.4, zorder=2.5)

for user, g in changes.groupby("user"):
    color = COLORS.get(user, "#4d6377")
    g.plot(ax=ax, facecolor=color, alpha=0.12, edgecolor=color, linewidth=0.7, zorder=3)
    centers = g.geometry.centroid
    ax.scatter(centers.x, centers.y, s=14, color=color, zorder=4, linewidths=0)

tino = gpd.GeoSeries([Point(123.65, 10.55)], crs=4326).to_crs(3857).iloc[0]
gpd.GeoSeries([tino.buffer(120000)], crs=3857).boundary.plot(
    ax=ax, color=ACCENT, linewidth=1, alpha=0.55, linestyle=(0, (3, 4)), zorder=2)

cities = {"Cebu City": (123.89, 10.31), "Tagbilaran": (123.85, 9.65),
          "Dumaguete": (123.31, 9.31), "Toledo": (123.64, 10.38)}
for name, (lon, lat) in cities.items():
    pt = gpd.GeoSeries([Point(lon, lat)], crs=4326).to_crs(3857).iloc[0]
    ax.annotate(name, (pt.x, pt.y), ha="center", color=INK, fontsize=9,
                fontfamily=FONT, path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)])

counts = changes.user.value_counts()
handles = [plt.Line2D([0], [0], marker="o", linestyle="", markersize=6,
                      color=COLORS.get(u, "#4d6377"), label=f"{u} · {n}")
           for u, n in counts.head(5).items()]
ax.legend(handles=handles + [
              plt.Line2D([0], [0], marker="o", linestyle="", markersize=6,
                         color="#4d6377", label=f"others · {counts.iloc[5:].sum()}"),
              plt.Line2D([0], [0], marker="o", linestyle="", markersize=6,
                         color="#4d6377", alpha=0.35, label=f"before Tino · {len(pre)}")],
          loc="lower right", frameon=True, facecolor=PAPER, edgecolor="#2b4155",
          labelcolor=INK, fontsize=9, title="Mappers", title_fontsize=9,
          framealpha=0.9)
leg = ax.get_legend()
leg.get_title().set_color(INK)
for t in leg.get_texts():
    t.set_fontfamily(FONT)
leg.get_title().set_fontfamily(FONT)

ax.set_aspect("equal")
ax.axis("off")
minx, miny, maxx, maxy = gpd.GeoSeries([box(*BBOX)], crs=4326).to_crs(3857).total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)

fig.text(0.07, 0.945, "C O L L A B O R A T I V E   M A P", color=ACCENT, fontsize=15,
         fontfamily=FONT, fontweight="bold")
fig.text(0.07, 0.905, "The crowd maps the storm", color=INK, fontsize=26,
         fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.865,
         f"{len(changes)} OpenStreetMap changesets in the Cebu–Negros box since Typhoon Tino\n"
         f"made landfall on 4 November, by {counts.size} mappers. The map is being repaired\n"
         "the way the roads are: one small edit at a time, by whoever is nearby.",
         color=INK, alpha=0.8, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.035,
         "Data: OpenStreetMap changeset API, latest 100 changesets returned  ·  "
         "#30DayMapChallenge 2026 · Day 16 · Collaborative",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.06, right=0.94, top=0.785, bottom=0.06)
out = OUT / "day16_collaborative.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out, len(changes))
