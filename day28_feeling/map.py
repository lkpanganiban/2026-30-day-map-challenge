"""Day 28 - Senses: Feeling.

USGS "Did You Feel It?" intensity for the M7.8 Sarangani earthquake of
8 June 2026: 597 responses from 144 places, up to 2,850 km away.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from shapely.geometry import Point, box

from style import ACCENT, DATA, FONT, INK, PAPER

OUT = Path(__file__).parent
felt = gpd.read_file(DATA / "dyfi_geo.gpkg").to_crs(3857)
land = gpd.read_file(DATA / "ph_land.gpkg").to_crs(3857)

quakes = gpd.read_file(DATA / "ph_quakes.geojson")
epi = quakes.loc[quakes.mag.idxmax()]
epi_pt = gpd.GeoSeries([Point(epi.geometry.x, epi.geometry.y)], crs=4326).to_crs(3857).iloc[0]

fig, ax = plt.subplots(figsize=(11, 14), facecolor=PAPER)
ax.set_facecolor(PAPER)
land.plot(ax=ax, color="#16222e", edgecolor="#2b4155", linewidth=0.3, zorder=1)
felt.plot(ax=ax, column="cdi", cmap="YlOrRd", vmin=1, vmax=10, alpha=0.8,
          edgecolor="none", zorder=2)

ax.scatter([epi_pt.x], [epi_pt.y], marker="*", s=300, color=ACCENT,
           edgecolor=INK, linewidth=0.6, zorder=5)
ax.annotate("M7.8 · 8 June 2026", (epi_pt.x, epi_pt.y), xytext=(12, 14),
            textcoords="offset points", color=INK, fontsize=9, fontfamily=FONT,
            fontweight="bold", path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)],
            zorder=6)

ax.set_aspect("equal")
ax.axis("off")
minx, miny, maxx, maxy = gpd.GeoSeries([box(114, 4, 128, 22)], crs=4326).to_crs(3857).total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)

sm = plt.cm.ScalarMappable(cmap="YlOrRd", norm=plt.Normalize(1, 10))
cax = fig.add_axes([0.30, 0.075, 0.40, 0.012])
cbar = fig.colorbar(sm, cax=cax, orientation="horizontal")
cbar.set_label("community decimal intensity (CDI) — how strong it felt", color=INK,
               fontsize=9, fontfamily=FONT, labelpad=8)
cbar.ax.tick_params(colors=INK, labelsize=8)
cbar.outline.set_edgecolor(INK)

fig.text(0.07, 0.945, "S E N S E S :   F E E L I N G", color=ACCENT, fontsize=15,
         fontfamily=FONT, fontweight="bold")
fig.text(0.07, 0.905, "How the shaking felt", color=INK, fontsize=26,
         fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.865,
         "USGS \"Did You Feel It?\" reports for the M7.8 Sarangani earthquake: 597 responses\n"
         "from 144 places, as far as 2,850 km away. Intensity 9.1 near the epicentre; across\n"
         "Mindanao the same quake was a 4, a 6, or a story someone tells about a shelf.",
         color=INK, alpha=0.82, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.025,
         "Data: USGS DYFI, event us7000srb1  ·  #30DayMapChallenge 2026 · Day 28 · Senses: Feeling",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.05, right=0.95, top=0.825, bottom=0.13)
out = OUT / "day28_feeling.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out, len(felt))
