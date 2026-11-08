"""Generate the README graphics: banner + 30-map mosaic.

Run: uv run python build_assets.py
"""
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

PAPER = (11, 22, 34)
PANEL = (8, 17, 27)
INK = (244, 239, 230)
MUTED = (157, 176, 189)
ACCENT = (230, 57, 70)
LINE = (38, 57, 74)

BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def day_meta(folder):
    first = (folder / "README.md").read_text().splitlines()[0]
    m = re.match(r"Day\s+(\d+)\s*[—-]+\s*(.+)", first.lstrip("# ").strip())
    return int(m.group(1)), m.group(2).strip()


def maps():
    out = []
    for folder in sorted(ROOT.glob("day*")):
        if not (folder / "README.md").exists():
            continue
        number, theme = day_meta(folder)
        images = sorted(folder.glob("day*.png"))
        if images:
            out.append((number, theme, images[0]))
    return out


def rounded(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, img.width - 1, img.height - 1],
                                           radius, fill=255)
    img = img.convert("RGBA")
    img.putalpha(mask)
    return img


def gradient(width, height):
    top, bottom = (11, 22, 34), (16, 38, 54)
    img = Image.new("RGB", (width, height))
    d = ImageDraw.Draw(img)
    for y in range(height):
        t = y / max(height - 1, 1)
        d.line([(0, y), (width, y)],
               fill=tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)))
    return img


def tracked(draw, xy, text, fnt, fill, tracking=0):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def make_banner():
    W, H = 1600, 560
    img = gradient(W, H)
    d = ImageDraw.Draw(img)

    d.rectangle([70, 92, 78, 118], fill=ACCENT)
    tracked(d, (96, 90), "30 DAY MAP CHALLENGE 2026", font(BOLD, 19), ACCENT, tracking=4)

    d.text((70, 140), "THE PHILIPPINES", font=font(BOLD, 82), fill=INK)
    d.text((70, 224), "IN THIRTY MAPS", font=font(BOLD, 82), fill=INK)

    d.text((72, 348), "Earthquakes, typhoons, volcanoes, floods —",
           font=font(REGULAR, 26), fill=MUTED)
    d.text((72, 386), "one Python map a day, built from open data.",
           font=font(REGULAR, 26), fill=MUTED)

    d.text((72, 482), "Python  ·  OpenStreetMap  ·  Landsat 9  ·  Sentinel-1/2/5P  ·  USGS",
           font=font(REGULAR, 18), fill=(120, 140, 156))

    picks = [p for n, _, p in maps() if n in (3, 8, 17, 26)]
    cell_w, cell_h, gap = 250, 182, 12
    start_x = W - 70 - (cell_w * 2 + gap)
    start_y = 92
    for i, path in enumerate(picks[:4]):
        im = Image.open(path).convert("RGB")
        im = ImageOps.contain(im, (cell_w, cell_h))
        tile = Image.new("RGB", (cell_w, cell_h), PANEL)
        tile.paste(im, ((cell_w - im.width) // 2, (cell_h - im.height) // 2))
        tile = rounded(tile, 11)
        frame = Image.new("RGBA", (cell_w + 2, cell_h + 2), (0, 0, 0, 0))
        ImageDraw.Draw(frame).rounded_rectangle(
            [0, 0, cell_w + 1, cell_h + 1], 12, outline=LINE, width=2)
        x = start_x + (i % 2) * (cell_w + gap)
        y = start_y + (i // 2) * (cell_h + gap)
        img.paste(tile, (x, y), tile)
        img.paste(frame, (x - 1, y - 1), frame)

    out = ASSETS / "banner.png"
    img.save(out, optimize=True)
    print("wrote", out, img.size)


def make_gallery():
    items = maps()
    cols, cell_w, cell_h = 6, 300, 320
    gap, margin = 10, 26
    rows = (len(items) + cols - 1) // cols
    W = margin * 2 + cols * cell_w + (cols - 1) * gap
    H = margin * 2 + rows * cell_h + (rows - 1) * gap
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    label_font = font(BOLD, 13)

    for i, (number, theme, path) in enumerate(items):
        x = margin + (i % cols) * (cell_w + gap)
        y = margin + (i // cols) * (cell_h + gap)
        cell = Image.new("RGB", (cell_w, cell_h), PANEL)
        im = Image.open(path).convert("RGB")
        im = ImageOps.contain(im, (cell_w - 8, cell_h - 38))
        cell.paste(im, ((cell_w - im.width) // 2, 4 + (cell_h - 38 - im.height) // 2))
        img.paste(cell, (x, y))
        d.rectangle([x, y, x + cell_w - 1, y + cell_h - 1], outline=(20, 35, 48))
        d.text((x + 10, y + cell_h - 24), f"{number:02d}  {theme.upper()}",
               font=label_font, fill=MUTED)

    out = ASSETS / "gallery.png"
    img.save(out, optimize=True)
    print("wrote", out, img.size)


make_banner()
make_gallery()
