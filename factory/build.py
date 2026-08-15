#!/usr/bin/env python3
"""
Fabrique d'outils — assemble un fichier HTML autonome à partir d'une spécification.

Chaque outil ne fournit que ce qui lui est propre : ses champs, sa formule,
son schéma et ses notes. Tout le reste (interface, unités, impression, style,
balises de référencement, maillage) vient d'ici.

Conséquence : ajouter un outil coûte ~80 lignes au lieu de ~600.
"""

import os, re, json, glob, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(HERE), "site")
STYLE = open(os.path.join(SITE, "_shared.css")).read()
FRAMEWORK = open(os.path.join(HERE, "framework.js")).read()

EXTRA_CSS = """
.plabel{font-size:11px;fill:var(--ink);font-family:ui-monospace,monospace}
.part{fill:var(--accent-soft);stroke:var(--accent);stroke-width:1.5}
.ghost{fill:none;stroke:var(--line);stroke-width:1}
.dim{stroke:var(--muted);stroke-width:.8}
svg{width:100%;height:auto;background:var(--surface);border:1px solid var(--line);border-radius:8px}
h3{font-size:.95rem}
.faq h3{margin:16px 0 4px}
.faq p{margin:0;color:var(--muted);font-size:.92rem}
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title_tag}</title>
<meta name="description" content="{description}">
<style>{style}{extra_css}</style>
</head>
<body>
<div class="wrap">

<h1>{h1}</h1>
<p class="sub">{intro}</p>

<div class="card noprint">
  <h2>Units</h2>
  <div class="row">
    <div class="f"><label for="unit">Working in</label>
      <select id="unit"><option value="mm">Millimetres</option><option value="in">Inches</option></select></div>
  </div>
</div>

<div id="form"></div>
<div id="out"></div>

<div class="card faq noprint">
  <h2>Notes</h2>
  {notes}
</div>

<footer>
  Runs entirely in your browser — nothing is uploaded, stored or tracked.
  {disclaimer}
</footer>
</div>

<script>
window.__SPEC__ = (function () {{
{spec_js}
return SPEC;
}})();
</script>
<script>
{framework}
</script>
</body>
</html>"""

DEFAULT_DISCLAIMER = ("These tools are planning aids, not engineering. Structural work needs "
                      "span tables, local building regulations and professional judgement. "
                      "Check every result against the real material before you cut.")


def build(spec_path):
    """Charge une spec Python, en extrait le JS et les métadonnées, écrit le HTML."""
    name = os.path.basename(spec_path)[:-3]
    mod_spec = importlib.util.spec_from_file_location(name, spec_path)
    mod = importlib.util.module_from_spec(mod_spec)
    mod_spec.loader.exec_module(mod)
    S = mod.SPEC

    notes_html = "\n  ".join(
        f"<h3>{q}</h3>\n  <p>{a}</p>" for q, a in S["notes"])

    # Substitution par remplacement et non par .format() : le JS des specs
    # est bourré d'accolades, qui feraient exploser un format().
    subs = {
        "{title_tag}": S["title_tag"],
        "{description}": S["description"],
        "{h1}": S["h1"],
        "{intro}": S["intro"],
        "{notes}": notes_html,
        "{style}": STYLE,
        "{extra_css}": EXTRA_CSS,
        "{spec_js}": S["js"],
        "{framework}": FRAMEWORK,
        "{disclaimer}": S.get("disclaimer", DEFAULT_DISCLAIMER),
    }
    html = TEMPLATE
    for k, v in subs.items():
        html = html.replace(k, v)

    out = os.path.join(SITE, S["slug"] + ".html")
    open(out, "w").write(html)
    return S["slug"], S["h1"], S["card_desc"], S["category"], len(html)


if __name__ == "__main__":
    built = []
    for path in sorted(glob.glob(os.path.join(HERE, "specs", "*.py"))):
        try:
            built.append(build(path))
        except Exception as e:
            print(f"  ÉCHEC {os.path.basename(path)} : {e}")
    print(f"{len(built)} outil(s) fabriqué(s)")
    for slug, title, _, cat, size in built:
        print(f"  [{cat}] {title} → {slug}.html ({size//1000} ko)")

    # Génère les entrées à coller dans build-index.py
    lines = [f'    ("{s}", "{t}",\n     "{d}",\n     "{c}"),' for s, t, d, c, _ in built]
    open(os.path.join(HERE, "index-entries.txt"), "w").write("\n".join(lines))
