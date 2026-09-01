#!/usr/bin/env python3
"""Génère la page d'accueil. Séparé de build-index.py pour rester lisible."""

import os, importlib.util

_here = os.path.dirname(os.path.abspath(__file__))
_pub = os.path.join(os.path.dirname(_here), "public")
# Deux dispositions possibles : l'atelier (script a cote des pages) et le
# depot (script dans build/, pages dans public/). On vise ce qui existe.
HERE = _pub if os.path.isdir(_pub) else _here
spec = importlib.util.spec_from_file_location("bi", os.path.join(_here, "build-index.py"))
bi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bi)

SITE_NAME, DOMAIN, STYLE = bi.SITE_NAME, bi.DOMAIN, bi.STYLE

ICONS = {
  "Sheet goods": '<svg viewBox="0 0 24 24" fill="none"><rect x="2" y="4" width="20" height="16" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M2 12h13M15 4v16" stroke="currentColor" stroke-width="1.6"/></svg>',
  "Framing": '<svg viewBox="0 0 24 24" fill="none"><path d="M3 20L12 5l9 15" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M6.5 14h11M12 5v15" stroke="currentColor" stroke-width="1.4" opacity=".55"/></svg>',
  "Finishing": '<svg viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="8" height="8" rx="1" stroke="currentColor" stroke-width="1.6"/><rect x="13" y="3" width="8" height="8" rx="1" stroke="currentColor" stroke-width="1.6" opacity=".45"/><rect x="3" y="13" width="8" height="8" rx="1" stroke="currentColor" stroke-width="1.6" opacity=".45"/><rect x="13" y="13" width="8" height="8" rx="1" stroke="currentColor" stroke-width="1.6"/></svg>',
  "Joinery": '<svg viewBox="0 0 24 24" fill="none"><path d="M4 8h4V4h4v4h4V4h4v16h-4v-4h-4v4H8v-4H4V8z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>',
}
BLURB = {
  "Sheet goods": "Plywood, MDF, bar stock and trim &mdash; every part out of the fewest sheets.",
  "Framing": "Stairs, roofs, walls and decks. The geometry, drawn and dimensioned.",
  "Finishing": "Tile, concrete, gravel and paint &mdash; quantities you can actually order.",
  "Joinery": "Layouts that divide evenly, with templates you print at full size.",
}

HERO_FIG = """<svg class="figsvg" viewBox="0 0 2440 1220" preserveAspectRatio="xMidYMid meet" aria-label="Example cutting layout">
  <rect x="0" y="0" width="2440" height="1220" rx="14" class="hsheet"/>
  <g class="hpart">
    <rect x="24" y="24" width="717" height="557" rx="6"/><rect x="765" y="24" width="717" height="557" rx="6"/>
    <rect x="1506" y="24" width="717" height="557" rx="6"/><rect x="24" y="605" width="797" height="557" rx="6"/>
    <rect x="845" y="605" width="797" height="557" rx="6"/><rect x="1666" y="605" width="593" height="557" rx="6"/>
    <rect x="2247" y="24" width="169" height="557" rx="6" class="hoff"/>
    <rect x="2283" y="605" width="133" height="557" rx="6" class="hoff"/>
  </g>
  <g class="hlab">
    <text x="382" y="330">720 &#215; 560</text><text x="1123" y="330">720 &#215; 560</text>
    <text x="1864" y="330">720 &#215; 560</text><text x="422" y="911">800 &#215; 560</text>
    <text x="1243" y="911">800 &#215; 560</text><text x="1962" y="911">596 &#215; 560</text>
  </g>
</svg>"""


def stair_fig():
    parts = []
    for i in range(9):
        x = 60 + i * 80
        y = 400 - i * 38
        parts.append('<rect x="%d" y="%d" width="80" height="16" rx="3" class="spart"/>' % (x, y - 16))
        parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="sline"/>' % (x, y, x, y - 38))
    return ('<svg class="figsvg" viewBox="0 0 840 470" preserveAspectRatio="xMidYMid meet" aria-label="Stair stringer elevation">'
            '<line x1="60" y1="415" x2="790" y2="415" class="sdim"/>'
            '<line x1="46" y1="415" x2="46" y2="55" class="sdim"/>'
            '<line x1="60" y1="400" x2="785" y2="58" class="sghost"/>'
            + "".join(parts) +
            '<text x="425" y="450" class="slab">total run 3500 &#183; 14 &#215; 250</text>'
            '<text x="168" y="392" class="slab">R 181.3</text>'
            '<text x="330" y="318" class="slab">35.8&#176;</text></svg>')


def joint_fig():
    p = []
    for i in range(7):
        x = 62 + i * 104
        p.append('<rect x="%d" y="66" width="72" height="140" rx="4" class="spart"/>' % x)
        p.append('<line x1="%d" y1="46" x2="%d" y2="226" class="sdim"/>' % (x, x))
        p.append('<line x1="%d" y1="46" x2="%d" y2="226" class="sdim"/>' % (x + 72, x + 72))
    return ('<svg class="figsvg" viewBox="0 0 840 300" preserveAspectRatio="xMidYMid meet" aria-label="Box joint template">'
            + "".join(p) +
            '<line x1="62" y1="250" x2="778" y2="250" class="sdim"/>'
            '<text x="420" y="282" class="slab">13 segments &#215; 11.54 = 150.00 exactly</text></svg>')


EXTRA_CSS = """
.hero{padding:8px 0 0}
.eyebrow{display:inline-flex;align-items:center;gap:7px;font-size:.75rem;font-weight:560;
  letter-spacing:.08em;text-transform:uppercase;color:var(--accent);
  background:var(--accent-soft);border:1px solid var(--line);
  padding:6px 13px;border-radius:999px;margin-bottom:18px}
.hero h1{font-size:clamp(2rem,4.4vw,3.05rem);line-height:1.06;letter-spacing:-.04em;
  font-weight:700;max-width:17ch;margin:0 0 16px}
.hero h1 .hl{color:var(--accent)}
.hero .sub{font-size:clamp(1.02rem,1.6vw,1.15rem);max-width:56ch;margin-bottom:24px}
.herowrap{display:grid;grid-template-columns:1.05fr .95fr;gap:38px;align-items:center;padding-bottom:30px}
.figsvg{width:100%;height:auto;border:1px solid var(--line);border-radius:14px;
  box-shadow:var(--shadow);background:var(--surface)}
.hsheet{fill:var(--surface);stroke:var(--line);stroke-width:3}
.hpart rect{fill:var(--accent-soft);stroke:var(--accent);stroke-width:3.5}
.hpart .hoff{fill:none;stroke:var(--line);stroke-width:3;stroke-dasharray:14 12}
.hlab text{fill:var(--muted);font-family:ui-monospace,Menlo,monospace;font-size:52px;
  text-anchor:middle;letter-spacing:-.02em}
.spart{fill:var(--accent-soft);stroke:var(--accent);stroke-width:2}
.sline{stroke:var(--accent);stroke-width:2}
.sdim{stroke:var(--muted);stroke-width:1;opacity:.45}
.sghost{stroke:var(--accent);stroke-width:1.6;stroke-dasharray:7 7;opacity:.65}
.slab{fill:var(--muted);font-family:ui-monospace,Menlo,monospace;font-size:19px;text-anchor:middle}
.figcap{font-size:.8rem;color:var(--muted);text-align:center;margin-top:10px}
.pills{display:flex;flex-wrap:wrap;gap:9px}
.pill{font-size:.83rem;color:var(--muted);background:var(--surface);
  border:1px solid var(--line);border-radius:999px;padding:6px 13px}
.band{display:grid;grid-template-columns:repeat(auto-fit,minmax(148px,1fr));
  background:var(--surface);border:1px solid var(--line);border-radius:16px;
  box-shadow:var(--shadow);overflow:hidden;margin:6px 0}
.bandit{padding:20px 22px;border-right:1px solid var(--line)}
.bandit:last-child{border-right:none}
.bandit b{display:block;font-size:1.72rem;font-weight:680;letter-spacing:-.035em;
  color:var(--accent);line-height:1.1;font-variant-numeric:tabular-nums}
.bandit span{font-size:.8rem;color:var(--muted)}
.section-title{font-size:1.5rem;font-weight:680;letter-spacing:-.03em;color:var(--ink);
  text-transform:none;margin:52px 0 6px}
.section-lead{color:var(--muted);font-size:.98rem;max-width:62ch;margin:0 0 22px}
.showcase{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:16px}
.shot{background:var(--surface);border:1px solid var(--line);border-radius:14px;
  padding:15px;box-shadow:var(--shadow)}
.shot .figsvg{border:none;box-shadow:none;border-radius:8px}
.shot h4{margin:12px 0 3px;font-size:.95rem;font-weight:620;letter-spacing:-.015em}
.shot p{margin:0;font-size:.86rem;color:var(--muted);line-height:1.5}
.catblock{margin:40px 0 0}
.cathead{display:flex;align-items:flex-start;gap:13px;margin-bottom:16px}
.caticon{flex:none;width:38px;height:38px;border-radius:11px;background:var(--accent-soft);
  border:1px solid var(--line);display:grid;place-items:center;color:var(--accent)}
.caticon svg{width:21px;height:21px}
.cattitle{font-size:1.12rem;font-weight:640;letter-spacing:-.02em;text-transform:none;
  color:var(--ink);margin:1px 0 3px}
.catblurb{font-size:.9rem;color:var(--muted);margin:0;max-width:60ch}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(272px,1fr));gap:14px}
.tool{display:flex;flex-direction:column;gap:5px;padding:19px;text-decoration:none;
  color:var(--ink);background:var(--surface);border:1px solid var(--line);
  border-radius:14px;box-shadow:var(--shadow)}
.tool .go{font-style:normal;font-size:.82rem;font-weight:560;color:var(--accent);
  margin-top:9px;opacity:0;transform:translateX(-4px);transition:all .18s ease}
.tool:hover .go{opacity:1;transform:translateX(0)}
.faqgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}
.faqitem{background:var(--surface);border:1px solid var(--line);border-radius:14px;
  padding:19px;box-shadow:var(--shadow)}
.faqitem b{display:block;font-size:.96rem;font-weight:620;margin-bottom:6px;letter-spacing:-.015em}
.faqitem p{margin:0;font-size:.89rem;color:var(--muted);line-height:1.58}
@media (max-width:860px){.herowrap{grid-template-columns:1fr;gap:26px}
  .bandit{border-right:none;border-bottom:1px solid var(--line)}}
"""


def build():
    tools = bi.existing()
    groups = {}
    for slug, title, desc, cat in tools:
        groups.setdefault(cat, []).append((slug, title, desc))

    cards = ""
    for cat in ["Sheet goods", "Framing", "Finishing", "Joinery"]:
        if cat not in groups:
            continue
        cards += ('\n<section class="catblock">\n  <div class="cathead">\n'
                  '    <span class="caticon">' + ICONS.get(cat, "") + '</span>\n'
                  '    <div><h2 class="cattitle">' + cat + '</h2>'
                  '<p class="catblurb">' + BLURB.get(cat, "") + '</p></div>\n'
                  '  </div>\n  <div class="grid">\n')
        for slug, title, desc in groups[cat]:
            cards += ('    <a class="tool" href="/' + slug + '">\n'
                      '      <strong>' + title + '</strong>\n'
                      '      <span>' + desc + '</span>\n'
                      '      <em class="go">Open tool &rarr;</em>\n    </a>\n')
        cards += "  </div>\n</section>\n"

    parts = []
    parts.append('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n')
    parts.append('<meta name="viewport" content="width=device-width,initial-scale=1">\n')
    parts.append('<title>' + SITE_NAME + ' &mdash; Free Workshop Calculators That Draw the Layout</title>\n')
    parts.append('<meta name="description" content="Free calculators for woodworking, framing and '
                 'finishing: cut list optimisation, stair stringers, rafters, deck boards, tile layout '
                 'and joinery templates. Scaled diagrams, printable cut lists, no sign-up.">\n')
    parts.append('<link rel="canonical" href="' + DOMAIN + '/">\n')
    parts.append('<style>' + STYLE + EXTRA_CSS + '</style>\n</head>\n<body>\n<div class="wrap">\n')

    parts.append('<div class="hero"><div class="herowrap"><div>'
                 '<span class="eyebrow">' + str(len(tools)) + ' free tools &middot; no sign-up</span>'
                 '<h1>Calculators that hand you the <span class="hl">layout</span>, not just a number.</h1>'
                 '<p class="sub">Every tool solves the arrangement, draws it to scale, and prints as a '
                 'working document you can take to the bench. Saw kerf is subtracted at every cut, grain '
                 'direction is respected, and joints land where they can actually be supported.</p>'
                 '<div class="pills"><span class="pill">Runs in your browser</span>'
                 '<span class="pill">Nothing uploaded</span><span class="pill">mm &amp; inches</span>'
                 '<span class="pill">Printable</span></div></div><div>'
                 + HERO_FIG +
                 '<p class="figcap">Real output: 22 parts nested on a 2440 &#215; 1220 sheet, kerf included.</p>'
                 '</div></div></div>\n')

    parts.append('<div class="band">'
                 '<div class="bandit"><b>' + str(len(tools)) + '</b><span>Tools, all free</span></div>'
                 '<div class="bandit"><b>0</b><span>Accounts to create</span></div>'
                 '<div class="bandit"><b>100%</b><span>Runs on your device</span></div>'
                 '<div class="bandit"><b>91.6%</b><span>Best nesting yield</span></div></div>\n')

    parts.append('<h2 class="section-title" id="what">What you actually get</h2>'
                 '<p class="section-lead">Not a number in a box. A dimensioned drawing you can print, '
                 'fold into your pocket and work from &mdash; plus the cut list that goes with it.</p>'
                 '<div class="showcase">'
                 '<div class="shot">' + stair_fig() + '<h4>Stair stringer elevation</h4>'
                 '<p>Every riser dimensioned, the angle, and the dropped-stringer correction applied.</p></div>'
                 '<div class="shot">' + joint_fig() + '<h4>Box joint template</h4>'
                 '<p>Pin width adjusted so the spacing divides exactly &mdash; printed at 1:1.</p></div>'
                 '<div class="shot">' + HERO_FIG + '<h4>Sheet nesting plan</h4>'
                 '<p>Parts placed, offcuts shown, kerf subtracted at every cut line.</p></div>'
                 '</div>\n')

    parts.append('<div id="tools"></div>' + cards)

    parts.append('<h2 class="section-title">Questions</h2><div class="faqgrid">'
                 '<div class="faqitem"><b>Is any of this really free?</b><p>Yes, and there is nothing to '
                 'sign up for. The tools run entirely in your browser, so there is no server cost per user '
                 'and no reason to put anything behind a login.</p></div>'
                 '<div class="faqitem"><b>Do you store what I type?</b><p>No. Nothing is uploaded, nothing '
                 'is saved, and there is no tracking. Close the tab and it is gone &mdash; which also means '
                 'write your numbers down if you need them again.</p></div>'
                 '<div class="faqitem"><b>Millimetres or inches?</b><p>Both, on every tool. The unit '
                 'selector converts the whole form, and the drawings and cut lists follow.</p></div>'
                 '<div class="faqitem"><b>Can I rely on this for structural work?</b><p>No. These are '
                 'planning aids. Span tables, building regulations and a qualified opinion are what '
                 'structural decisions need &mdash; the geometry here is a starting point, not a sign-off.</p>'
                 '</div></div>\n')

    foot_links = ""
    for cat in ["Sheet goods", "Framing", "Finishing", "Joinery"]:
        if cat not in groups:
            continue
        foot_links += '<div><h5>' + cat + '</h5>'
        for slug, title, _ in groups[cat][:4]:
            foot_links += '<a href="/' + slug + '">' + title + '</a>'
        foot_links += '</div>'

    parts.append('<footer><div class="footgrid">'
                 '<div><h5>KerfCalc</h5><p style="font-size:.88rem;color:var(--muted);'
                 'margin:0;line-height:1.55;max-width:34ch">Free workshop calculators that solve the '
                 'layout and draw it to scale. Built for people who actually cut the material.</p></div>'
                 + foot_links +
                 '</div><div class="footnote">Everything runs client-side &mdash; no accounts, no '
                 'uploads, no tracking. Planning aids only: check every layout against the real '
                 'material before you cut.</div></footer>\n</div>\n</body>\n</html>')

    open(os.path.join(HERE, "index.html"), "w").write("".join(parts))
    return len(tools)


if __name__ == "__main__":
    n = build()
    print("Page d'accueil générée avec " + str(n) + " outils")
