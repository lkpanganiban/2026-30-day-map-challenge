"""Day 25 - Is this a map?

Every named tropical cyclone track in the western North Pacific, 2026,
drawn as ink. No legend, no scale, no labels: just the year's weather hand.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from style import DATA

OUT = Path(__file__).parent
PAPER = "#efe9da"
INK = "#1f1c18"
ACCENT = "#9b3a2a"

df = pd.read_csv(DATA / "ibtracs_last3years.csv", skiprows=[1], low_memory=False)
df = df[(df.SEASON == 2026) & (df.NAME != "UNNAMED")].copy()
for c in ["LAT", "LON"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df = df.dropna(subset=["LAT", "LON"])

fig, ax = plt.subplots(figsize=(13, 9), facecolor=PAPER)
ax.set_facecolor(PAPER)
n = 0
for name, g in df.groupby("NAME"):
    g = g[(g.LON.between(100, 180)) & (g.LAT.between(0, 45))].sort_values("ISO_TIME")
    if len(g) < 2:
        continue
    ax.plot(g.LON, g.LAT, color=INK, linewidth=0.7, alpha=0.45, solid_capstyle="round")
    n += 1

ax.set_xlim(105, 170)
ax.set_ylim(2, 42)
ax.set_aspect(1.2)
ax.axis("off")

fig.text(0.07, 0.90, "WIND  WRITING", color=INK, fontsize=24,
         fontfamily="Baskerville", fontweight="bold")
fig.text(0.07, 0.86,
         f"{n} tropical cyclone tracks, western North Pacific, 2026.\n"
         "No legend, no scale, no labels. Is this a map?",
         color=INK, alpha=0.75, fontsize=11, fontfamily="Baskerville",
         style="italic", linespacing=1.5, va="top")

fig.text(0.07, 0.045,
         "Data: IBTrACS v04r01 (NOAA/NCEI)  ·  #30DayMapChallenge 2026 · Day 25 · Is this a map?",
         color=INK, alpha=0.5, fontsize=8, fontfamily="Baskerville")

fig.subplots_adjust(left=0.04, right=0.96, top=0.80, bottom=0.08)
out = OUT / "day25_art.png"
fig.savefig(out, dpi=200, facecolor=PAPER)
print("wrote", out, n, "tracks")
