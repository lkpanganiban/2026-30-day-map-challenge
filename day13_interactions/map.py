"""Day 13 - Interactions.

An interactive map of the last two years: earthquakes, typhoon tracks and
Mayon's danger zone, each on its own layer.
"""
from pathlib import Path

import folium
import geopandas as gpd
import pandas as pd
from folium.plugins import MeasureControl

from style import DATA

OUT = Path(__file__).parent


def depth_color(d):
    return "#e63946" if d < 70 else "#f4a261" if d < 300 else "#58c7f3"


quakes = gpd.read_file(DATA / "ph_quakes.geojson")
quakes["depth"] = quakes.geometry.z
country = gpd.read_file(DATA / "ph_boundary.gpkg").to_crs(4326)
quakes = gpd.sjoin(quakes.set_crs(4326, allow_override=True), country[["geometry"]],
                   predicate="within")

m = folium.Map(
    location=[12.5, 122.0], zoom_start=5, tiles=None,
    control_scale=True, prefer_canvas=True,
)
folium.TileLayer(
    "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}",
    attr="Esri, HERE, Garmin, © OpenStreetMap contributors",
    name="Dark canvas", control=False,
).add_to(m)

eq = folium.FeatureGroup(name="Earthquakes M5+ (Nov 2024 – now)")
for _, q in quakes.iterrows():
    folium.CircleMarker(
        [q.geometry.y, q.geometry.x], radius=2 + (q.mag - 4) * 2.2,
        color=depth_color(q.depth), fill=True, fill_opacity=0.85, weight=0,
        popup=f"M{q.mag} · {q.place}<br>depth {q.depth:.0f} km",
    ).add_to(eq)
eq.add_to(m)

tracks = pd.read_csv(DATA / "ibtracs_last3years.csv", skiprows=[1], low_memory=False)
tracks = tracks[(tracks.SEASON == 2026) & (tracks.NAME != "UNNAMED")].copy()
for c in ["LAT", "LON", "USA_WIND"]:
    tracks[c] = pd.to_numeric(tracks[c], errors="coerce")
tracks = tracks.dropna(subset=["LAT", "LON"])
in_par = tracks.groupby("NAME").apply(
    lambda g: ((g.LON.between(114.5, 127)) & (g.LAT.between(4.5, 22))).any(),
    include_groups=False)
ty = folium.FeatureGroup(name="2026 typhoon tracks")
for name, g in tracks[tracks.NAME.isin(in_par[in_par].index)].groupby("NAME"):
    peak = g.USA_WIND.max()
    color = "#e63946" if peak >= 137 else "#f4a261" if peak >= 96 else "#f4d35e" if peak >= 64 else "#58c7f3"
    folium.PolyLine(g[["LAT", "LON"]].values.tolist(), color=color, weight=2.2,
                    opacity=0.9, tooltip=f"{name} · peak {int(peak)} kt").add_to(ty)
ty.add_to(m)

vol = folium.FeatureGroup(name="Mayon danger zone")
folium.Circle([13.2573, 123.6855], radius=6000, color="#e63946", weight=1.5,
              dash_array="6", fill=True, fill_opacity=0.12,
              popup="Mayon 6 km Permanent Danger Zone").add_to(vol)
folium.Marker([13.2573, 123.6855], tooltip="Mayon · 2,462 m",
              icon=folium.Icon(color="red", icon="triangle-exclamation", prefix="fa")).add_to(vol)
vol.add_to(m)

MeasureControl().add_to(m)
m.fit_bounds([[4.3, 114.0], [21.5, 127.0]])
folium.LayerControl(collapsed=True).add_to(m)

title = """
<div style="position: fixed; top: 14px; left: 54px; z-index: 9999;
     font-family: 'Avenir Next', Helvetica, sans-serif; color: #f4efe6;">
  <div style="color:#e63946;font-size:11px;letter-spacing:4px;font-weight:700;">INTERACTIONS</div>
  <div style="font-size:22px;font-weight:700;margin-top:2px;">Two years of shaking, wind and ash</div>
  <div style="font-size:11px;opacity:.8;margin-top:4px;">
    Click a point or line. Toggle layers in the panel.
  </div>
</div>
"""
m.get_root().html.add_child(folium.Element(title))

out = OUT / "day13_interactions.html"
m.save(out)
print("wrote", out, out.stat().st_size)
