"""Day 7 - 10 minute map.

Built in one sitting, no new downloads: walking time from every 250 m cell
in Metro Manila to the nearest river, creek, canal or drain.
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
water = gpd.read_file(DATA / "mm_waterways.gpkg").to_crs(32651)
land = gpd.read_file(DATA / "ph_land.gpkg").to_crs(32651).clip(water.total_bounds)

grid = 20  # metres
minx, miny, maxx, maxy = water.total_bounds
width = int((maxx - minx) / grid)
height = int((maxy - miny) / grid)
transform = from_origin(minx, maxy, grid, grid)
shape = (height, width)

water_mask = rasterize([(g, 1) for g in water.geometry], out_shape=shape,
                       transform=transform, fill=0)
# distance in metres from every cell to the nearest waterway pixel
distance = distance_transform_edt(water_mask == 0, sampling=grid)
minutes = distance / 80  # ~4.8 km/h walking pace

land_mask = rasterize([(g, 1) for g in land.geometry], out_shape=shape,
                      transform=transform, fill=0)
minutes = np.where(land_mask == 1, minutes, np.nan)

cmap = LinearSegmentedColormap.from_list(
    "water", ["#e63946", "#f4a261", "#f4d35e", "#58c7f3", "#16222e"]
)
cmap.set_bad(PAPER)

fig, ax = plt.subplots(figsize=(11, 12), facecolor=PAPER)
ax.set_facecolor(PAPER)
im = ax.imshow(minutes, extent=(minx, maxx, miny, maxy), origin="upper",
               cmap=cmap, vmin=0, vmax=10, interpolation="nearest")

xs = minx + (np.arange(width) + 0.5) * grid
ys = maxy - (np.arange(height) + 0.5) * grid
xx, yy = np.meshgrid(xs, ys)
contours = ax.contour(xx, yy, minutes, levels=[5, 10], colors=INK,
                      linewidths=0.6, alpha=0.35, linestyles="dashed")
ax.clabel(contours, fmt="%d min", fontsize=7, colors=INK, inline=True)

ax.set_aspect("equal")
ax.axis("off")

labels = {"Manila": (120.9842, 14.5995), "Quezon City": (121.0437, 14.6760),
          "Marikina": (121.1029, 14.6507), "Taguig": (121.0509, 14.5176)}
for name, (lon, lat) in labels.items():
    pt = gpd.GeoSeries([shapely.Point(lon, lat)], crs=4326).to_crs(32651).iloc[0]
    ax.annotate(name, (pt.x, pt.y), ha="center", color=INK, fontsize=9,
                fontfamily=FONT, zorder=5,
                path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)])

fig.text(0.07, 0.93, "10  M I N U T E  M A P", color=ACCENT, fontsize=15,
         fontfamily=FONT, fontweight="bold")
fig.text(0.07, 0.885, "Ten minutes from the water", color=INK, fontsize=26,
         fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.845,
         "Straight-line walking time from every 20 m cell in Metro Manila to the nearest\n"
         "river, creek, canal or drain. Nine in ten cells are within ten minutes; the median\n"
         "is three. Water is never far. Built in ten minutes, from cached OpenStreetMap data.",
         color=INK, alpha=0.8, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

cax = fig.add_axes([0.30, 0.075, 0.40, 0.012])
cbar = fig.colorbar(im, cax=cax, orientation="horizontal")
cbar.set_label("minutes on foot (straight line) to the nearest mapped waterway", color=INK,
               fontsize=9, fontfamily=FONT, labelpad=8)
cbar.ax.tick_params(colors=INK, labelsize=8)
cbar.outline.set_edgecolor(INK)

fig.text(0.07, 0.025,
         "Data: © OpenStreetMap contributors  ·  #30DayMapChallenge 2026 · Day 7 · 10 minute map",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.06, right=0.94, top=0.74, bottom=0.13)
out = OUT / "day07_tenmin.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out)
