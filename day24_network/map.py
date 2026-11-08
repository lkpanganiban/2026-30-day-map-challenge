"""Day 24 - Network.

Cebu's primary road network, and the two coastal routes out of Cebu City:
north to Daanbantayan, south to Santander.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from shapely.geometry import LineString, Point, box

from style import ACCENT, DATA, FONT, INK, PAPER, WATER

OUT = Path(__file__).parent
roads = gpd.read_file(DATA / "cebu_roads.gpkg").to_crs(32651)
land = gpd.read_file(DATA / "ph_land.gpkg").to_crs(32651)

G = nx.Graph()
for geom in roads.geometry:
    coords = list(geom.coords)
    for a, b in zip(coords[:-1], coords[1:]):
        na, nb = (round(a[0], 1), round(a[1], 1)), (round(b[0], 1), round(b[1], 1))
        G.add_edge(na, nb, weight=LineString([a, b]).length)


def nearest(lon, lat):
    pt = gpd.GeoSeries([Point(lon, lat)], crs=4326).to_crs(32651).iloc[0]
    return min(G.nodes, key=lambda n: (n[0] - pt.x) ** 2 + (n[1] - pt.y) ** 2)


cities = {"Cebu City": (123.893, 10.315), "Daanbantayan": (124.020, 11.200),
          "Santander": (123.420, 9.420)}
nodes = {k: nearest(*v) for k, v in cities.items()}

routes = {
    "North coast · to Daanbantayan": (nodes["Cebu City"], nodes["Daanbantayan"], ACCENT),
    "South coast · to Santander": (nodes["Cebu City"], nodes["Santander"], WATER),
}
paths = {}
for label, (a, b, color) in routes.items():
    try:
        path = nx.shortest_path(G, a, b, weight="weight")
        length = sum(G.edges[u, v]["weight"] for u, v in zip(path[:-1], path[1:]))
        paths[label] = (path, length, color)
    except nx.NetworkXNoPath:
        print("no path:", label)

fig, ax = plt.subplots(figsize=(10, 14), facecolor=PAPER)
ax.set_facecolor(PAPER)
land.plot(ax=ax, color="#16222e", edgecolor="#2b4155", linewidth=0.3, zorder=1)
roads.plot(ax=ax, color="#2a4055", linewidth=0.3, alpha=0.6, zorder=2)

for label, (path, length, color) in paths.items():
    xs = [n[0] for n in path]
    ys = [n[1] for n in path]
    ax.plot(xs, ys, color=color, linewidth=2.4, zorder=4, solid_capstyle="round")
    ax.plot(xs, ys, color=color, linewidth=8, alpha=0.08, zorder=3)
    print(label, round(length / 1000), "km")

for name, (lon, lat) in cities.items():
    pt = gpd.GeoSeries([Point(lon, lat)], crs=4326).to_crs(32651).iloc[0]
    ax.scatter([pt.x], [pt.y], s=45, color=INK, zorder=5)
    ax.annotate(name, (pt.x, pt.y), xytext=(8, 6), textcoords="offset points",
                color=INK, fontsize=10, fontfamily=FONT, fontweight="bold",
                path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)], zorder=6)

handles = [plt.Line2D([0], [0], color=c, lw=3,
                      label=f"{label.split(' · ')[0]} · {round(p[1] / 1000)} km")
           for label, p in paths.items()
           for c in [p[2]]]
ax.legend(handles=handles, loc="upper left", frameon=True, facecolor=PAPER,
          edgecolor="#2b4155", labelcolor=INK, fontsize=9, framealpha=0.9,
          title="Shortest route", title_fontsize=9)
leg = ax.get_legend()
leg.get_title().set_color(INK)
for t in leg.get_texts():
    t.set_fontfamily(FONT)
leg.get_title().set_fontfamily(FONT)

ax.set_aspect("equal")
ax.axis("off")
minx, miny, maxx, maxy = gpd.GeoSeries([box(123.3, 9.3, 124.3, 11.4)], crs=4326).to_crs(32651).total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)

fig.text(0.07, 0.945, "N E T W O R K", color=ACCENT, fontsize=15, fontfamily=FONT,
         fontweight="bold")
fig.text(0.07, 0.905, "Two ways off the spine", color=INK, fontsize=26,
         fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.865,
         "Cebu's primary road network, and the shortest routes from Cebu City to the island's\n"
         "northern and southern tips. There is no inland alternative: when Typhoon Tino closed\n"
         "the coast this week, the shortest path stopped being a choice.",
         color=INK, alpha=0.82, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.035,
         "Data: © OpenStreetMap contributors  ·  #30DayMapChallenge 2026 · Day 24 · Network",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.06, right=0.94, top=0.825, bottom=0.06)
out = OUT / "day24_network.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out, len(G), "nodes")
