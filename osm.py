"""Minimal Overpass fetch -> GeoDataFrame. OSMnx's default calls get rate-limited;
one POST with a real User-Agent is enough for the small extracts we need."""
import json
from pathlib import Path

import geopandas as gpd
import requests
from shapely.geometry import LineString, Point, Polygon

URL = "https://overpass-api.de/api/interpreter"
HEADERS = {"User-Agent": "30daymapchallenge-ph/1.0 (local cartography script)"}


def query(q, cache):
    cache = Path(cache)
    if not cache.exists():
        r = requests.post(URL, data={"data": q}, headers=HEADERS, timeout=300)
        r.raise_for_status()
        cache.write_bytes(r.content)
    return json.loads(cache.read_text())


def to_gdf(data):
    rows = []
    for e in data["elements"]:
        tags = e.get("tags", {})
        if e["type"] == "node":
            geom = Point(e["lon"], e["lat"])
        elif e.get("center"):
            geom = Point(e["center"]["lon"], e["center"]["lat"])
        elif e.get("geometry"):
            coords = [(p["lon"], p["lat"]) for p in e["geometry"]]
            closed = len(coords) > 3 and coords[0] == coords[-1]
            area = any(k in tags for k in ("building", "landuse", "natural", "leisure"))
            geom = Polygon(coords) if closed and area else LineString(coords)
        else:
            continue
        rows.append({**tags, "osm_id": e["id"], "osm_type": e["type"], "geometry": geom})
    return gpd.GeoDataFrame(rows, crs=4326)


def save(gdf, path):
    """to_file, dropping case-insensitive duplicate tag columns (FIXME/fixme)."""
    seen, keep = set(), []
    for c in gdf.columns:
        if c != "geometry" and c.lower() in seen:
            continue
        seen.add(c.lower())
        keep.append(c)
    gdf[keep].to_file(path, driver="GPKG")
