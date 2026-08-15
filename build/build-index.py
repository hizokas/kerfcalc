#!/usr/bin/env python3
"""
Assemble la page d'accueil, le plan du site et le maillage interne.

À relancer après chaque ajout d'outil : il suffit d'ajouter une entrée
dans TOOLS ci-dessous. Le script régénère index.html, sitemap.xml,
robots.txt et injecte le bandeau de navigation dans chaque outil.
"""

import os, re, datetime

# --- Le seul endroit à modifier quand on ajoute un outil ---------------------
SITE_NAME = "KerfCalc"
DOMAIN    = "https://getkerfcalc.com"

TOOLS = [
    ("cut-list-optimizer",       "Cut List Optimizer",
     "Lay out your parts on full sheets with the least waste. Kerf and grain aware, with scaled diagrams.",
     "Sheet goods"),
    ("linear-cut-optimizer",     "Linear Cut Optimizer",
     "Cut lists for bars, boards, pipe and trim. Minimises the number of stock lengths you buy.",
     "Sheet goods"),
    ("stair-stringer-calculator","Stair Stringer Calculator",
     "Riser and tread layout, stringer length, and the dropped-stringer correction most people forget.",
     "Framing"),
    ("rafter-calculator",        "Rafter & Roof Framing Calculator",
     "Common, hip and valley rafter lengths, plumb and seat cuts, with a fully dimensioned diagram.",
     "Framing"),
    ("deck-board-planner",       "Deck Board Layout Planner",
     "Board positions, staggered butt joints landing on joists, and a buy list by stock length.",
     "Framing"),
    ("tile-layout-planner",      "Tile Layout Planner",
     "Tile counts, edge cuts, and a start point that balances the cuts on both walls.",
     "Finishing"),
    ("box-joint-layout",         "Box Joint &amp; Dovetail Layout",
     "Even pin and tail spacing that actually divides, plus a 1:1 printable marking template.",
     "Joinery"),
    ("board-foot-calculator",    "Board Foot Calculator",
     "Board feet, waste allowance and cost across a whole list of boards, in quarters or millimetres.",
     "Sheet goods"),
    ("stud-wall-layout",          "Stud Wall Layout Calculator",
     "Stud positions with the first-stud correction so sheet edges land on framing, plus the material list.",
     "Framing"),
    ("roof-area-calculator",      "Roof Area &amp; Material Calculator",
     "True sloped area from footprint and pitch, with squares, bundles, ridge and hip lengths.",
     "Framing"),
    ("fence-post-planner",        "Fence Post Spacing Calculator",
     "Even post spacing with no stubby last bay, plus rails, pickets and concrete per hole.",
     "Framing"),
    ("concrete-volume-calculator","Concrete Volume Calculator",
     "Volume for slabs, footings, columns and post holes, plus how many bags that actually is.",
     "Finishing"),
    ("gravel-volume-calculator",  "Gravel &amp; Aggregate Calculator",
     "Volume and tonnage for aggregates, including the compaction allowance most calculators forget.",
     "Finishing"),
    ("paint-coverage-calculator", "Paint Coverage Calculator",
     "Litres or gallons per coat with openings subtracted, rounded up to real tin sizes.",
     "Finishing"),
    ("compound-miter-calculator", "Compound Miter Angle Calculator",
     "Saw miter and bevel settings for crown and sloped work, with the formulas shown.",
     "Joinery"),
]

HERE = os.path.dirname(os.path.abspath(__file__))
STYLE = open(os.path.join(HERE, "_shared.css")).read()


def existing():
    return [t for t in TOOLS if os.path.exists(os.path.join(HERE, t[0] + ".html"))]


def build_index():
    return existing()


def inject_nav(tools):
    """Ajoute un lien de retour et un bloc d'outils liés dans chaque page."""
    slugs = {t[0]: t for t in tools}
    for slug, title, desc, cat in tools:
        path = os.path.join(HERE, slug + ".html")
        src = open(path).read()
        # Nettoyage INCONDITIONNEL des blocs deja injectes.
        # Bug corrige : le nettoyage etait conditionne a la presence de #site-nav,
        # que la passe de style supprimait -> les blocs "related" s'empilaient a
        # chaque reconstruction (jusqu'a 8 copies sur une page).
        src = re.sub(r'<nav id="site-nav".*?</nav>', '', src, flags=re.S)
        src = re.sub(r'<aside id="related"[^>]*>.*?</aside>', '', src, flags=re.S)

        nav = f'<nav id="site-nav" class="noprint" style="margin-bottom:18px;font-size:.88rem">' \
              f'<a href="./index.html" style="color:var(--muted);text-decoration:none">← All {SITE_NAME} tools</a></nav>'

        siblings = [t for t in tools if t[3] == cat and t[0] != slug][:3]
        if len(siblings) < 3:
            siblings += [t for t in tools if t[3] != cat and t[0] != slug][:3 - len(siblings)]
        links = "".join(
            f'<li style="margin:4px 0"><a href="./{s}.html" style="color:var(--accent)">{ti}</a> '
            f'<span style="color:var(--muted)">— {de}</span></li>'
            for s, ti, de, _ in siblings)
        related = f'<aside id="related" class="card noprint"><h2>Related tools</h2>' \
                  f'<ul style="margin:0;padding-left:18px;font-size:.9rem">{links}</ul></aside>'

        src = re.sub(r'(<div class="wrap">)', r'\1\n' + nav, src, count=1)
        src = re.sub(r'(<footer>)', related + r'\n\1', src, count=1)
        open(path, "w").write(src)


def build_sitemap(tools):
    today = datetime.date.today().isoformat()
    urls = "".join(
        f"  <url><loc>{DOMAIN}/{s}.html</loc><lastmod>{today}</lastmod></url>\n"
        for s, _, _, _ in tools)
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{DOMAIN}/</loc><lastmod>{today}</lastmod><priority>1.0</priority></url>
{urls}</urlset>'''
    open(os.path.join(HERE, "sitemap.xml"), "w").write(xml)
    open(os.path.join(HERE, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")


if __name__ == "__main__":
    tools = build_index()
    inject_nav(tools)
    build_sitemap(tools)
    print(f"Site assemblé : {len(tools)} outil(s)")
    for s, t, _, c in tools:
        print(f"  [{c}] {t}  →  {s}.html")
