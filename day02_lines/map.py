"""Day 2 - Lines.

Every tropical cyclone that entered the Philippine Area of Responsibility
in 2026, drawn as a line and coloured by strength.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from shapely.geometry import Polygon, box

from style import ACCENT, DATA, FONT, INK, PAPER, WATER

OUT = Path(__file__).parent
TRACKS = DATA / "ibtracs_last3years.csv"
LAND = DATA / "wp_land.gpkg"
BOUNDARY = DATA / "ph_boundary.gpkg"

PAR = [(115, 5), (115, 15), (120, 21), (120, 25), (135, 25), (135, 5), (115, 5)]
WIND_BINS = [
    (0, "#3a6ea5", "tropical depression"),
    (34, WATER, "tropical storm"),
    (64, "#f4d35e", "typhoon"),
    (96, "#f4a261", "strong typhoon"),
    (137, ACCENT, "super typhoon"),
]


def wind_color(w):
    color = WIND_BINS[0][1]
    for threshold, c, _ in WIND_BINS:
        if w >= threshold:
            color = c
    return color


def load():
    df = pd.read_csv(TRACKS, skiprows=[1], low_memory=False)
    df["ISO_TIME"] = pd.to_datetime(df["ISO_TIME"], errors="coerce")
    df = df[(df.SEASON == 2026) & (df.NAME != "UNNAMED")].copy()
    for c in ["LAT", "LON", "USA_WIND"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["LAT", "LON"])
    in_par = df.groupby("NAME").apply(
        lambda g: ((g.LON.between(114.5, 127)) & (g.LAT.between(4.5, 22))).any(),
        include_groups=False,
    )
    df = df[df.NAME.isin(in_par[in_par].index)].sort_values(["NAME", "ISO_TIME"])
    land = gpd.read_file(LAND).to_crs(4326)
    country = gpd.read_file(BOUNDARY).to_crs(4326)
    ph_land = gpd.clip(land, country.union_all())
    return df, land.to_crs(3857), ph_land.to_crs(3857)


df, land, ph_land = load()

fig, ax = plt.subplots(figsize=(13, 12), facecolor=PAPER)
ax.set_facecolor(PAPER)

land.plot(ax=ax, color="#0d1620", edgecolor="#16222e", linewidth=0.2, zorder=1)
ph_land.plot(ax=ax, color="#22384b", edgecolor="#2b4155", linewidth=0.3, zorder=2)

par = gpd.GeoSeries([Polygon(PAR)], crs=4326).to_crs(3857)
par.boundary.plot(ax=ax, color="#9db4c0", linewidth=0.8, alpha=0.55,
                  linestyle=(0, (4, 4)), zorder=3)
ax.annotate("PAR", (par.total_bounds[0] + 60_000, par.total_bounds[1] + 120_000),
            color="#9db4c0", alpha=0.7, fontsize=9, fontfamily=FONT, rotation=90)

labels = {"BAVI": "Bavi · Inday", "CHAMPI": "Champi · Rosal"}
offsets = {
    "BAVI": (10, 4, "left"), "CHAMPI": (-6, 16, "right"),
    "MEKKHALA": (-8, 10, "right"), "NOUL": (-8, 8, "right"),
    "MAYSAK": (8, 8, "left"), "PEILOU": (-8, -14, "right"),
    "NOKAEN": (8, -12, "left"), "PENHA": (0, -14, "center"),
    "SAUDEL": (-8, 8, "right"),
}
for name, group in df.groupby("NAME"):
    pts = gpd.GeoSeries(gpd.points_from_xy(group.LON, group.LAT), crs=4326).to_crs(3857)
    xy = list(zip(pts.x, pts.y))
    if len(xy) < 2:
        continue
    segs = [[xy[i], xy[i + 1]] for i in range(len(xy) - 1)]
    colors = [wind_color(np) for np in group.USA_WIND.to_numpy()[:-1]]
    ax.add_collection(LineCollection(segs, colors=colors, linewidths=2.1,
                                    alpha=0.9, zorder=4, capstyle="round"))
    ax.add_collection(LineCollection(segs, colors=colors, linewidths=7,
                                    alpha=0.08, zorder=3.5, capstyle="round"))

    inside = group[(group.LON.between(105, 140)) & (group.LAT.between(0, 32))]
    if inside.empty:
        continue
    peak = inside.loc[inside.USA_WIND.idxmax()]
    anchor = gpd.GeoSeries([gpd.points_from_xy([peak.LON], [peak.LAT])[0]], crs=4326).to_crs(3857).iloc[0]
    text = labels.get(name, name.title())
    dx, dy, ha = offsets.get(name, (8, 8, "left"))
    ax.annotate(text, (anchor.x, anchor.y), xytext=(dx, dy), textcoords="offset points",
                ha=ha, color=INK, fontsize=8.5, fontfamily=FONT,
                path_effects=[pe.withStroke(linewidth=2.5, foreground=PAPER)],
                zorder=6)

handles = [Line2D([0], [0], color=c, lw=3, label=f"{t.title()} ({v}+ kt)")
           for v, c, t in WIND_BINS]
ax.legend(handles=handles, loc="lower left", frameon=False, fontsize=9,
          labelcolor=INK, title="Peak wind", title_fontsize=9,
          bbox_to_anchor=(0.02, 0.02))
leg = ax.get_legend()
leg.get_title().set_color(INK)
leg.get_title().set_fontfamily(FONT)
for t in leg.get_texts():
    t.set_fontfamily(FONT)

ax.set_aspect("equal")
ax.axis("off")
west, south, east, north = gpd.GeoSeries(
    [box(105, 0, 140, 32)], crs=4326
).to_crs(3857).total_bounds
ax.set_xlim(west, east)
ax.set_ylim(south, north)

fig.text(0.07, 0.945, "L I N E S", color=ACCENT, fontsize=15, fontfamily=FONT,
         fontweight="bold")
fig.text(0.07, 0.905, "Nine storms entered the ring", color=INK,
         fontsize=26, fontfamily=FONT, fontweight="bold", va="top")
fig.text(0.07, 0.862,
         "Every cyclone that entered the Philippine Area of Responsibility in 2026, coloured by strength.\n"
         "Champi (Rosal) was the year's strongest; Bavi (Inday) left 20 dead in July; this week's\n"
         "Kalmaegi (Tino) is too new for the official best-track record.",
         color=INK, alpha=0.8, fontsize=11, fontfamily=FONT, linespacing=1.5, va="top")

fig.text(0.07, 0.03,
         "Data: IBTrACS v04r01 (NOAA/NCEI) · Boundary: © OpenStreetMap contributors  ·  "
         "#30DayMapChallenge 2026 · Day 2 · Lines",
         color=INK, alpha=0.5, fontsize=9, fontfamily=FONT)

fig.subplots_adjust(left=0.05, right=0.95, top=0.805, bottom=0.055)
out = OUT / "day02_lines.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out, df.NAME.nunique(), "storms")
