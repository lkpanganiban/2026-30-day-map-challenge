"""Shared bits: paths, colors, PH bounding boxes. Keep small; add as days need."""
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

# (west, south, east, north) - lon/lat
PH = (114.0, 4.0, 128.0, 22.0)
METRO_MANILA = (120.90, 14.55, 121.10, 14.78)

# cartographic palette used across the month
INK = "#f4efe6"
PAPER = "#0b1622"
ACCENT = "#e63946"
WATER = "#58c7f3"

FONT = "Avenir Next"  # macOS system font; falls back visibly if missing
