"""Day 27 - New tool.

A Plotly orthographic globe: the 2026 PAR typhoon tracks and the M5+
earthquakes, on a globe that turns. First time plotly appears in this series.
"""
from pathlib import Path

import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go

from style import DATA

OUT = Path(__file__).parent

quakes = gpd.read_file(DATA / "ph_quakes.geojson")
quakes["depth"] = quakes.geometry.z
country = gpd.read_file(DATA / "ph_boundary.gpkg").to_crs(4326)
quakes = gpd.sjoin(quakes.set_crs(4326, allow_override=True), country[["geometry"]],
                   predicate="within")

tracks = pd.read_csv(DATA / "ibtracs_last3years.csv", skiprows=[1], low_memory=False)
tracks = tracks[(tracks.SEASON == 2026) & (tracks.NAME != "UNNAMED")].copy()
for c in ["LAT", "LON", "USA_WIND"]:
    tracks[c] = pd.to_numeric(tracks[c], errors="coerce")
tracks = tracks.dropna(subset=["LAT", "LON"])
in_par = tracks.groupby("NAME").apply(
    lambda g: ((g.LON.between(114.5, 127)) & (g.LAT.between(4.5, 22))).any(),
    include_groups=False)
tracks = tracks[tracks.NAME.isin(in_par[in_par].index)]

fig = go.Figure()
for name, g in tracks.groupby("NAME"):
    peak = g.USA_WIND.max()
    color = "#e63946" if peak >= 137 else "#f4a261" if peak >= 96 else "#f4d35e" if peak >= 64 else "#58c7f3"
    fig.add_trace(go.Scattergeo(
        lon=g.LON, lat=g.LAT, mode="lines", line=dict(color=color, width=2),
        name=f"{name} · {int(peak)} kt", hoverinfo="name", opacity=0.9,
    ))

fig.add_trace(go.Scattergeo(
    lon=quakes.geometry.x, lat=quakes.geometry.y, mode="markers",
    marker=dict(size=(quakes.mag - 4) * 2.2, color="#f4efe6", opacity=0.7),
    name="M5+ earthquakes",
    text=[f"M{q.mag} · {q.place}" for q in quakes.itertuples()],
    hovertemplate="%{text}<extra></extra>",
))

fig.update_geos(
    projection_type="orthographic", projection_rotation=dict(lon=122, lat=12),
    showland=True, landcolor="#1d3142", showocean=True, oceancolor="#0b1622",
    showcountries=True, countrycolor="#2b4155", showcoastlines=True,
    coastlinecolor="#2b4155", showlakes=False, bgcolor="#0b1622",
)
fig.update_layout(
    template="plotly_dark", paper_bgcolor="#0b1622", plot_bgcolor="#0b1622",
    title=dict(text="INTERACTIONS ON A GLOBE<br><sup>2026 PAR typhoons and M5+ earthquakes · drag to spin</sup>",
               font=dict(color="#f4efe6", size=22), x=0.05, y=0.95),
    legend=dict(bgcolor="rgba(11,22,34,0.8)", bordercolor="#2b4155", borderwidth=1,
                font=dict(color="#f4efe6", size=10)),
    margin=dict(l=0, r=0, t=90, b=0),
    height=1200,
)

out = OUT / "day27_newtool.html"
fig.write_html(out, include_plotlyjs="cdn")
html = out.read_text().replace(
    "</head>", "<style>html,body{margin:0;background:#0b1622}</style></head>"
)
out.write_text(html)
print("wrote", out, out.stat().st_size)
