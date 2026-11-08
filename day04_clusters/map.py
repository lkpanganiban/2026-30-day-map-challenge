"""Day 4 - Clusters.

133 M5+ earthquakes grouped when within 50 km of each other.
The aftershock families of the 2026 Sarangani and 2025 Eastern Mindanao quakes.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import box

from style import ACCENT, DATA, FONT, INK, PAPER, WATER

OUT = Path(__file__).parent
QUAKES = DATA / "ph_quakes.geojson"
BOUNDARY = DATA / "ph_boundary.gpkg"
LAND = DATA / "ph_land.gpkg"

# cluster -> (colour, short label)
FAMILIES = {
    "Sarangani": (ACCENT, "Sarangani · M7.8"),
    "Moro Gulf": ("#f4d35e", "Moro Gulf"),
    "Cebu": (WATER, "Cebu · M6.9"),
    "Davao Oriental": ("#f4a261", "Davao Oriental · M7.4"),
    "Surigao": ("#b388eb", "Surigao · M6.0"),
}


def haversine(a, b):
    r = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, (a[0], a[1], b[0], b[1]))
    h = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 2 * r * np.arcsin(np.sqrt(h))


def load():
    q = gpd.read_file(QUAKES)
    q["depth"] = q.geometry.z
    q = q.set_crs(4326, allow_override=True)
    country = gpd.read_file(BOUNDARY).to_crs(4326)
    q = gpd.sjoin(q, country[["geometry"]], predicate="within")
    pts = np.c_[q.geometry.y, q.geometry.x]

    parent = list(range(len(q)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(len(q)):
        for j in range(i + 1, len(q)):
            if haversine(pts[i], pts[j]) < 50:
                parent[find(i)] = find(j)
    q["cluster"] = [find(i) for i in range(len(q))]

    names = {
        "Balangonan": "Sarangani", "Bantogon": "Moro Gulf", "Anonang": "Cebu",
        "Santiago": "Davao Oriental", "Cortes": "Surigao",
    }
    label = {}
    for c, g in q.groupby("cluster"):
        if len(g) >= 5:
            place = g.place.mode().iloc[0].split(" of ")[-1].split(",")[0]
            label[c] = names.get(place, place)
    q["family"] = q.cluster.map(label)
    land = gpd.read_file(LAND).to_crs(3857)
    return q.to_crs(3857), land


quakes, land = load()
counts = quakes.family.value_counts()
sizes = (quakes.mag - 4) ** 3 * 4

fig, ax = plt.subplots(figsize=(11, 14), facecolor=PAPER)
ax.set_facecolor(PAPER)
land.plot(ax=ax, color="#16222e", edgecolor="#2b4155", linewidth=0.3, zorder=1)

small = quakes.family.isna()
ax.scatter(quakes[small].geometry.x, quakes[small].geometry.y, s=sizes[small],
           color="#41576a", alpha=0.7, linewidths=0, zorder=3)

for family, (color, text) in FAMILIES.items():
    g = quakes[quakes.family == family]
    hull = g.union_all().convex_hull.buffer(15000)
    gpd.GeoSeries([hull], crs=3857).plot(ax=ax, color=color, alpha=0.07, zorder=3.2)
    ax.scatter(g.geometry.x, g.geometry.y, s=sizes[quakes.family == family],
               color=color, alpha=0.85, linewidths=0, zorder=4)
    ax.scatter(g.geometry.x, g.geometry.y, s=sizes[quakes.family == family] * 3,
               color=color, alpha=0.06, linewidths=0, zorder=3.5)

offsets = {
    "Sarangani": (10, -18, "left"),
    "Moro Gulf": (-12, 12, "right"),
    "Cebu": (-12, 14, "right"),
    "Davao Oriental": (12, 10, "left"),
    "Surigao": (12, 12, "left"),
}
for family, (color, text) in FAMILIES.items():
    g = quakes[quakes.family == family]
    cx, cy = g.geometry.x.mean(), g.geometry.y.mean()
    dx, dy, ha = offsets[family]
    ax.annotate(f"{text} · {len(g)}", (cx, cy), xytext=(dx, dy),
                textcoords="offset points", ha=ha, color=color,
                fontsize=9, fontfamily=FONT, fontweight="bold",
                path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)],
                zorder=6)

ax.set_aspect("equal")
ax.axis("off")
minx, miny, maxx, maxy = gpd.GeoSeries([box(114, 4, 128, 22)], crs=4326).to_crs(3857).total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)

fig.text(0.07, 0.945, "C L U S T E R S", color=ACCENT, fontsize=15, fontfamily=FONT,
         fontweight="bold")
fig.text(0.07, 0.905, "Earthquakes travel in families", color=INK,
         fontsize=26, fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.862,
         "133 M5+ quakes in Philippine territory since November 2024, grouped when within 50 km of each other.\n"
         "Three in ten belong to the Sarangani sequence that opened with the M7.8 on 8 June 2026.\n"
         "The rest are smaller families, aftershocks looking for their mainshock.",
         color=INK, alpha=0.8, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.035,
         "Data: USGS Earthquake Catalog · Boundary: © OpenStreetMap contributors  ·  "
         "#30DayMapChallenge 2026 · Day 4 · Clusters",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.05, right=0.95, top=0.795, bottom=0.06)
out = OUT / "day04_clusters.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out, dict(counts))
