"""Day 20 - Hexagons.

The last two years of M5+ earthquakes binned into H3 hexagons.
The Sarangani sequence owns the southern cell; the east coast owns the rest.
"""
from pathlib import Path

import geopandas as gpd
import h3
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from shapely.geometry import Polygon, box

from style import ACCENT, DATA, FONT, INK, PAPER

OUT = Path(__file__).parent
RES = 4

q = gpd.read_file(DATA / "ph_quakes.geojson").set_crs(4326, allow_override=True)
country = gpd.read_file(DATA / "ph_boundary.gpkg").to_crs(4326)
q = gpd.sjoin(q, country[["geometry"]], predicate="within")
q["cell"] = [h3.latlng_to_cell(y, x, RES) for y, x in zip(q.geometry.y, q.geometry.x)]
counts = q.cell.value_counts()

land = gpd.read_file(DATA / "ph_land.gpkg").to_crs(3857)

fig, ax = plt.subplots(figsize=(11, 14), facecolor=PAPER)
ax.set_facecolor(PAPER)
land.plot(ax=ax, color="#16222e", edgecolor="#2b4155", linewidth=0.3, zorder=1)

cmap = LinearSegmentedColormap.from_list("hex", ["#1f3b3a", "#2a6f6a", "#f4d35e", ACCENT])
hexes = gpd.GeoDataFrame(
    {"cell": counts.index, "n": counts.values},
    geometry=[Polygon([(lon, lat) for lat, lon in h3.cell_to_boundary(c)])
              for c in counts.index],
    crs=4326,
).to_crs(3857)
hexes.plot(ax=ax, column="n", cmap=cmap, edgecolor=PAPER, linewidth=0.5,
           alpha=0.9, zorder=2, legend=False,
           vmin=1, vmax=max(counts.max(), 8))

pts = q.to_crs(3857)
ax.scatter(pts.geometry.x, pts.geometry.y, s=(pts.mag - 4) ** 2 * 1.5,
           color=INK, alpha=0.35, linewidths=0, zorder=3)

ax.set_aspect("equal")
ax.axis("off")
minx, miny, maxx, maxy = gpd.GeoSeries([box(114, 4, 128, 22)], crs=4326).to_crs(3857).total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)

sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(1, max(counts.max(), 8)))
cax = fig.add_axes([0.30, 0.075, 0.40, 0.012])
cbar = fig.colorbar(sm, cax=cax, orientation="horizontal")
cbar.set_label("earthquakes per hexagon (H3 resolution 4)", color=INK, fontsize=9,
               fontfamily=FONT, labelpad=8)
cbar.ax.tick_params(colors=INK, labelsize=8)
cbar.outline.set_edgecolor(INK)

fig.text(0.07, 0.945, "H E X A G O N S", color=ACCENT, fontsize=15, fontfamily=FONT,
         fontweight="bold")
fig.text(0.07, 0.905, "The bestagons of shaking", color=INK, fontsize=26,
         fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.865,
         f"{len(q)} M5+ earthquakes binned into H3 hexagons at resolution 4 (about 1,770 km² each).\n"
         f"The Sarangani sequence fills one southern cell with {counts.max()} events; the rest\n"
         "spread along the trenches, where the plates keep moving.",
         color=INK, alpha=0.82, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.035,
         "Data: USGS Earthquake Catalog · H3 · Boundary: © OpenStreetMap contributors  ·  "
         "#30DayMapChallenge 2026 · Day 20 · Hexagons",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.05, right=0.95, top=0.825, bottom=0.13)
out = OUT / "day20_hexagons.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out, counts.head(3).to_dict())
