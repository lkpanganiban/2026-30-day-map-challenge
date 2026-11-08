"""Build the static gallery site.

Reads every day*/README.md, extracts the theme, title and first story
paragraph, renders the Markdown, and writes a single index.html with a
hash-routed gallery + detail view. No server, no build step at runtime.
"""
import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
OUT = ROOT / "index.html"

CSS = """
:root{
  --paper:#0b1622; --panel:#101f2c; --ink:#f4efe6; --muted:#9db0bd;
  --accent:#e63946; --line:#26394a; --water:#58c7f3; --max:1240px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:
    radial-gradient(1100px 520px at 72% -8%, #122a3c 0%, rgba(11,22,34,0) 60%),
    var(--paper);
  color:var(--ink);
  font-family:"Avenir Next","Helvetica Neue",Helvetica,Arial,sans-serif;
  line-height:1.65; -webkit-font-smoothing:antialiased;
}
a{color:inherit}
[hidden]{display:none!important}
.wrap{max-width:var(--max);margin:0 auto;padding:0 28px}
.kicker{
  color:var(--accent);font-size:.74rem;font-weight:700;letter-spacing:.34em;
  text-transform:uppercase;
}
header.site{padding:64px 0 26px}
header.site h1{
  font-size:clamp(2.4rem,5.6vw,4.6rem);line-height:1.02;letter-spacing:-.03em;
  margin:.28em 0 .35em;max-width:16ch;
}
header.site .dek{max-width:62ch;color:var(--muted);font-size:1.06rem}
.meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:26px}
.chip{
  border:1px solid var(--line);border-radius:999px;padding:5px 12px;
  font-size:.75rem;letter-spacing:.04em;color:var(--muted);
}
.chip b{color:var(--ink);font-weight:600}
.rule{height:1px;background:var(--line);margin:34px 0 0}
.section-head{
  display:flex;align-items:baseline;justify-content:space-between;gap:16px;
  margin:34px 0 18px;
}
.section-head h2{font-size:1.1rem;letter-spacing:.12em;text-transform:uppercase;margin:0}
.section-head span{color:var(--muted);font-size:.85rem}
.grid{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));
  gap:22px;padding-bottom:60px;
}
.card{
  display:flex;flex-direction:column;text-decoration:none;background:var(--panel);
  border:1px solid var(--line);border-radius:16px;overflow:hidden;
  transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease;
}
.card:hover,.card:focus-visible{
  transform:translateY(-4px);border-color:#3c5a73;
  box-shadow:0 18px 40px rgba(0,0,0,.32);outline:none;
}
.thumb{
  aspect-ratio:4/3;background:#0a1420;display:flex;align-items:center;
  justify-content:center;overflow:hidden;border-bottom:1px solid var(--line);
}
.thumb img{width:100%;height:100%;object-fit:contain;display:block}
.thumb--interactive{
  background:
    radial-gradient(500px 240px at 70% 20%, rgba(88,199,243,.18), transparent 65%),
    repeating-linear-gradient(135deg, rgba(255,255,255,.03) 0 1px, transparent 1px 12px),
    #0c1a27;
  color:var(--water);font-weight:700;letter-spacing:.28em;font-size:.82rem;
  text-transform:uppercase;flex-direction:column;gap:10px;
}
.thumb--interactive .dot{font-size:2rem;line-height:1;letter-spacing:0}
.card-body{padding:18px 18px 20px;display:flex;flex-direction:column;gap:8px;flex:1}
.eyebrow{
  display:flex;justify-content:space-between;gap:10px;color:var(--accent);
  font-size:.7rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;
}
.eyebrow span:last-child{color:var(--muted)}
.card h3{margin:0;font-size:1.22rem;line-height:1.25;letter-spacing:-.01em}
.card p{margin:0;color:var(--muted);font-size:.92rem;line-height:1.5}
.more{margin-top:auto;padding-top:10px;color:var(--ink);font-size:.84rem;font-weight:600}
.more::after{content:" →"}

/* detail */
.detail{padding:56px 0 80px;max-width:1000px;margin:0 auto}
.back{
  display:inline-block;color:var(--muted);text-decoration:none;font-size:.85rem;
  letter-spacing:.08em;margin-bottom:28px;
}
.back:hover{color:var(--ink)}
.detail-head h1{
  font-size:clamp(2rem,4.4vw,3.3rem);line-height:1.06;letter-spacing:-.025em;
  margin:.2em 0 .35em;
}
.detail-head .dek{color:var(--muted);font-size:1.02rem;max-width:70ch}
.hero{
  margin:34px 0 18px;border:1px solid var(--line);border-radius:16px;
  background:#08111b;overflow:hidden;
}
.hero img{display:block;max-width:100%;max-height:82vh;width:auto;height:auto;margin:0 auto}
.actions{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0 30px}
.btn{
  display:inline-block;text-decoration:none;border:1px solid var(--line);
  border-radius:999px;padding:9px 16px;font-size:.84rem;font-weight:600;
  color:var(--ink);background:#0e1c29;transition:border-color .15s,background .15s;
}
.btn:hover{border-color:#46647c;background:#122436}
.btn--accent{border-color:var(--accent);color:#fff}
.prose{max-width:78ch;font-size:1.02rem}
.prose h2{
  font-size:1.24rem;letter-spacing:.02em;margin:2.2em 0 .5em;
  padding-top:.7em;border-top:1px solid var(--line);
}
.prose h3{font-size:1.04rem;margin:1.6em 0 .4em}
.prose p{margin:.8em 0}
.prose ul,.prose ol{padding-left:1.3em;margin:.8em 0}
.prose li{margin:.28em 0}
.prose code{
  font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86em;
  background:#0d1c29;border:1px solid var(--line);border-radius:5px;
  padding:.1em .38em;white-space:nowrap;
}
.prose pre{background:#0d1c29;border:1px solid var(--line);border-radius:10px;
  padding:14px;overflow:auto}
.prose a{color:var(--water)}
.prose strong{color:#fff}
.detail-foot{
  display:flex;flex-wrap:wrap;justify-content:space-between;gap:14px;
  margin-top:44px;padding-top:20px;border-top:1px solid var(--line);
  font-size:.86rem;color:var(--muted);
}
.detail-foot a{color:var(--ink);text-decoration:none}
.detail-foot a:hover{color:var(--water)}
footer.site{padding:30px 0 56px;border-top:1px solid var(--line);color:var(--muted);font-size:.82rem}
footer.site a{color:var(--ink);text-decoration:none}
footer.site a:hover{color:var(--water)}
footer.site .src{display:flex;flex-wrap:wrap;gap:6px 18px;margin:10px 0 14px}
footer.site .src a{border-bottom:1px solid var(--line);padding-bottom:1px}
@media (max-width:640px){
  .wrap{padding:0 18px}
  header.site{padding-top:42px}
  .grid{grid-template-columns:1fr;gap:18px}
  .detail{padding-top:36px}
}
"""


def strip_md(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_`>#]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def short_description(text, limit=230):
    para = next((p.strip() for p in text.split("\n\n") if p.strip()), "")
    para = strip_md(para)
    if len(para) <= limit:
        return para
    cut = para[:limit]
    end = max(cut.rfind(". "), cut.rfind("; "))
    if end > 110:
        return cut[:end + 1]
    return cut.rsplit(" ", 1)[0] + "…"


def parse_day(folder):
    text = (folder / "README.md").read_text()
    lines = text.splitlines()
    h1 = lines[0].lstrip("# ").strip()
    title = next((l.strip().strip("*") for l in lines[1:] if l.strip()), h1)
    m = re.match(r"Day\s+(\d+)\s*[—-]+\s*(.+)", h1)
    number = int(m.group(1)) if m else 0
    theme = m.group(2).strip() if m else h1
    story = re.search(r"## The story\s*\n(.*?)\n## ", text, re.S)
    story_text = story.group(1).strip() if story else ""
    desc = short_description(story_text)
    images = sorted(folder.glob("day*.png"))
    image = images[0] if images else None
    interactive = folder.glob("day*.html")
    pdf = folder.glob("day*.pdf")
    interactive = next(interactive, None)
    pdf = next(pdf, None)
    return {
        "folder": folder.name, "number": number, "theme": theme, "title": title,
        "desc": desc, "image": image, "interactive": interactive, "pdf": pdf,
        "readme": folder / "README.md", "text": text,
    }


def detail_body(text):
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].startswith("**") and lines[0].endswith("**"):
        lines.pop(0)
    body = "\n".join(lines).lstrip()
    return re.sub(r"(\*\*Output:\*\*[^\n]*)\n(\*\*Run:\*\*)", r"\1\n\n\2", body)


days = sorted(
    (parse_day(p) for p in ROOT.glob("day*") if (p / "README.md").exists()),
    key=lambda d: d["number"],
)

cards = []
details = []
for i, d in enumerate(days):
    slug = d["folder"]
    num = f"{d['number']:02d}"
    if d["image"]:
        thumb = (f'<img src="{d["image"].relative_to(ROOT).as_posix()}" '
                 f'alt="{html.escape(d["title"])}" loading="lazy">')
    else:
        thumb = '<span class="dot">◉</span><span>Interactive</span>'
    thumb_class = "thumb" + ("" if d["image"] else " thumb--interactive")
    cards.append(f"""
<a class="card" href="#{slug}">
  <div class="{thumb_class}">{thumb}</div>
  <div class="card-body">
    <div class="eyebrow"><span>Day {num}</span><span>{html.escape(d["theme"])}</span></div>
    <h3>{html.escape(d["title"])}</h3>
    <p>{html.escape(d["desc"])}</p>
    <span class="more">{"Open interactive map" if d["interactive"] else "Open map"}</span>
  </div>
</a>""")

    hero = ""
    if d["image"]:
        hero = (f'<div class="hero"><img src="{d["image"].relative_to(ROOT).as_posix()}" '
                f'alt="{html.escape(d["title"])}"></div>')

    actions = []
    if d["image"]:
        actions.append(f'<a class="btn" href="{d["image"].relative_to(ROOT).as_posix()}" '
                       f'target="_blank" rel="noopener">Open full image</a>')
    if d["interactive"]:
        actions.append(f'<a class="btn btn--accent" '
                       f'href="{d["interactive"].relative_to(ROOT).as_posix()}" '
                       f'target="_blank" rel="noopener">Open interactive map</a>')
    if d["pdf"]:
        actions.append(f'<a class="btn btn--accent" '
                       f'href="{d["pdf"].relative_to(ROOT).as_posix()}" '
                       f'target="_blank" rel="noopener">Download printable PDF</a>')
    actions.append(f'<a class="btn" href="{slug}/README.md" target="_blank" '
                   f'rel="noopener">README.md</a>')
    actions.append(f'<a class="btn" href="{slug}/map.py" target="_blank" '
                   f'rel="noopener">Python source</a>')

    prev_day = days[i - 1] if i > 0 else None
    next_day = days[i + 1] if i < len(days) - 1 else None
    prev = (f'<a href="#{prev_day["folder"]}">← Day {prev_day["number"]:02d} · '
            f'{html.escape(prev_day["theme"])}</a>' if prev_day else "<span></span>")
    nxt = (f'<a href="#{next_day["folder"]}">Day {next_day["number"]:02d} · '
           f'{html.escape(next_day["theme"])} →</a>' if next_day else "<span></span>")

    body = markdown.markdown(
        detail_body(d["text"]),
        extensions=["extra", "sane_lists"],
    )
    body = re.sub(r'<a href="(https?://[^"]+)"',
                  r'<a href="\1" target="_blank" rel="noopener"', body)
    details.append(f"""
<section class="detail" id="{slug}" data-title="{html.escape(d["title"])}" hidden>
  <a class="back" href="#gallery">← All maps</a>
  <div class="detail-head">
    <div class="kicker">Day {num} · {html.escape(d["theme"])}</div>
    <h1>{html.escape(d["title"])}</h1>
    <p class="dek">{html.escape(d["desc"])}</p>
  </div>
  {hero}
  <div class="actions">{''.join(actions)}</div>
  <div class="prose">{body}</div>
  <div class="detail-foot">{prev}{nxt}</div>
</section>""")

JS = """
const gallery = document.getElementById('gallery');
const details = Array.from(document.querySelectorAll('.detail'));
const baseTitle = document.title;
function render(){
  const id = location.hash.replace('#','');
  if(!id || id === 'gallery'){
    gallery.hidden = false;
    details.forEach(d => d.hidden = true);
    document.title = baseTitle;
    window.scrollTo({top:0,behavior:'instant'});
    return;
  }
  const target = document.getElementById(id);
  if(!target || !target.classList.contains('detail')){
    location.hash = 'gallery';
    return;
  }
  gallery.hidden = true;
  details.forEach(d => d.hidden = d !== target);
  document.title = target.dataset.title + ' · 30 Day Map Challenge 2026';
  window.scrollTo({top:0,behavior:'instant'});
}
window.addEventListener('hashchange', render);
render();
"""

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>30 Day Map Challenge 2026 · The Philippines</title>
<meta name="description" content="Thirty Python maps of the Philippines: earthquakes, typhoons, volcanoes, floods and the open data behind them.">
<style>{CSS}</style>
</head>
<body>
<main class="wrap">

<div id="gallery">
  <header class="site">
    <div class="kicker">30 Day Map Challenge 2026</div>
    <h1>The Philippines in thirty maps</h1>
    <p class="dek">Earthquakes, typhoons, volcanoes, floods and the communities mapping
    them. Every map is built in Python from open data — OpenStreetMap, Landsat,
    Sentinel, USGS, IBTrACS and Copernicus.</p>
    <div class="meta">
      <span class="chip"><b>30</b> maps</span>
      <span class="chip"><b>Python</b> + open data</span>
      <span class="chip"><b>Nov 2026</b></span>
    </div>
    <div class="rule"></div>
  </header>

  <div class="section-head">
    <h2>The gallery</h2>
    <span>Click a map for the story, data and process</span>
  </div>
  <div class="grid">
    {''.join(cards)}
  </div>
</div>

{''.join(details)}

<footer class="site">
  <div class="kicker" style="margin-bottom:3px">Primary sources</div>
  <div class="src">
    <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>
    <a href="https://earthquake.usgs.gov/fdsnws/event/1/">USGS earthquakes</a>
    <a href="https://earthquake.usgs.gov/data/dyfi/">USGS DYFI</a>
    <a href="https://www.ncei.noaa.gov/products/international-best-track-archive">NOAA IBTrACS</a>
    <a href="https://www.usgs.gov/landsat-missions/landsat-9">NASA/USGS Landsat 9</a>
    <a href="https://dataspace.copernicus.eu/">ESA Copernicus</a>
    <a href="https://www.naturalearthdata.com/">Natural Earth</a>
    <a href="https://www.phivolcs.dost.gov.ph/">PHIVOLCS</a>
    <a href="https://www.pagasa.dost.gov.ph/">PAGASA</a>
  </div>
  Built for <a href="https://30daymapchallenge.com/2026">#30DayMapChallenge</a> ·
  <a href="README.md">Project README</a>. Every detail page lists the exact
  data links for that map.
</footer>

</main>
<script>{JS}</script>
</body>
</html>
"""

OUT.write_text(page)
(ROOT / ".nojekyll").write_text("")
print(f"wrote {OUT} ({OUT.stat().st_size/1024:.0f} KB, {len(days)} maps)")
