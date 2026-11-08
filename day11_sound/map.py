"""Day 11 - Senses: Sound.

Distance from the nearest major road in Metro Manila as a rough traffic-noise
proxy. The quiet pockets left are watersheds, campuses and golf courses.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import shapely
from matplotlib.colors import LinearSegmentedColormap
from rasterio.features import rasterize
from rasterio.transform import from_origin
from scipy.ndimage import distance_transform_edt

from style import ACCENT, DATA, FONT, INK, PAPER

OUT = Path(__file__).parent
roads = gpd.read_file(DATA / "mm_roads.gpkg").to_crs(32651)
land = gpd.read_file(DATA / "ph_land.gpkg").to_crs(32651).clip(roads.total_bounds)

grid = 25
minx, miny, maxx, maxy = roads.total_bounds
width, height = int((maxx - minx) / grid), int((maxy - miny) / grid)
transform = from_origin(minx, maxy, grid, grid)
shape = (height, width)

road_mask = rasterize([(g, 1) for g in roads.geometry], out_shape=shape,
                      transform=transform, fill=0)
distance = distance_transform_edt(road_mask == 0, sampling=grid)
distance = np.clip(distance, 0, 900)
land_mask = rasterize([(g, 1) for g in land.geometry], out_shape=shape,
                      transform=transform, fill=0)
distance = np.where(land_mask == 1, distance, np.nan)

cmap = LinearSegmentedColormap.from_list(
    "quiet", ["#16222e", "#1f3b35", "#4f7d6b", "#8fae9b", "#d9d4c5"]
)
cmap.set_bad(PAPER)

fig, ax = plt.subplots(figsize=(12, 12), facecolor=PAPER)
ax.set_facecolor(PAPER)
im = ax.imshow(distance, extent=(minx, maxx, miny, maxy), origin="upper",
               cmap=cmap, vmin=0, vmax=900, interpolation="nearest")

points = {"Manila": (120.9842, 14.5995), "Quezon City": (121.0437, 14.6760),
          "Marikina": (121.1029, 14.6507), "La Mesa": (121.072, 14.715),
          "Marikina\nWatershed": (121.185, 14.705)}
for name, (lon, lat) in points.items():
    pt = gpd.GeoSeries([shapely.Point(lon, lat)], crs=4326).to_crs(32651).iloc[0]
    ax.annotate(name, (pt.x, pt.y), ha="center", color=INK,
                fontsize=9 if "\n" in name else 10, fontfamily=FONT, zorder=5,
                linespacing=1.2,
                path_effects=[pe.withStroke(linewidth=3, foreground="black")])

ax.set_aspect("equal")
ax.axis("off")

cax = fig.add_axes([0.30, 0.075, 0.40, 0.012])
cbar = fig.colorbar(im, cax=cax, orientation="horizontal")
cbar.set_label("metres from the nearest major road  ·  brighter = quieter", color=INK,
               fontsize=9, fontfamily=FONT, labelpad=8)
cbar.ax.tick_params(colors=INK, labelsize=8)
cbar.outline.set_edgecolor(INK)

fig.text(0.07, 0.945, "S O U N D", color=ACCENT, fontsize=15, fontfamily=FONT,
         fontweight="bold")
fig.text(0.07, 0.905, "Where the city is quiet", color=INK, fontsize=26,
         fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.865,
         "Distance from the nearest motorway, trunk, primary or secondary road — a rough\n"
         "proxy for traffic noise. The quiet pockets left are watersheds, campuses and golf\n"
         "courses: islands of hush inside one of the loudest cities in Southeast Asia.",
         color=INK, alpha=0.8, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.025,
         "Data: © OpenStreetMap contributors  ·  #30DayMapChallenge 2026 · Day 11 · Senses: Sound",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.06, right=0.94, top=0.80, bottom=0.13)
out = OUT / "day11_sound.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out)
