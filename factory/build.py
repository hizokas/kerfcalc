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
# Atelier : ../site ; depot : ../public. On ecrit la ou les pages vivent.
_root = os.path.dirname(HERE)
SITE = next(d for d in (os.path.join(_root, "public"), os.path.join(_root, "site"))
            if os.path.isdir(d))
_css = next(q for q in (os.path.join(_root, "build", "_shared.css"),
                        os.path.join(_root, "site", "_shared.css"))
            if os.path.exists(q))
STYLE = open(_css).read()
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

<div id="form">{form_html}</div>
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


def render_form_html(fields):
    """Écrit le formulaire en HTML statique.

    Pourquoi : les robots qui n'exécutent pas le JavaScript ne voyaient
    qu'une page sans champs. Google sait exécuter le JS, mais s'en passer
    est toujours plus sûr — et ça aligne les outils de la fabrique sur ceux
    écrits à la main. Le runtime détecte ce HTML et se contente de l'animer.
    """
    def esc(t):
        return (str(t).replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))

    groups = []
    for f in fields:
        g = f.get("group", "Inputs")
        if not groups or groups[-1][0] != g:
            groups.append((g, []))
        groups[-1][1].append(f)

    out = []
    for gname, gfields in groups:
        out.append('<div class="card noprint"><h2>%s</h2><div class="row">' % esc(gname))
        for f in gfields:
            fid = esc(f["id"])
            out.append('<div class="f"><label for="%s">%s%s</label>' % (
                fid, esc(f["label"]),
                ' <span class="u"></span>' if f.get("unit") == "length" else ""))
            t = f.get("type", "number")
            if t == "select":
                opts = "".join(
                    '<option value="%s"%s>%s</option>' % (
                        esc(o["value"]), " selected" if o["value"] == f.get("value") else "",
                        esc(o["label"]))
                    for o in f.get("options", []))
                out.append('<select id="%s">%s</select>' % (fid, opts))
            elif t == "check":
                out.append('<input type="checkbox" id="%s"%s>' % (
                    fid, " checked" if f.get("value") else ""))
            else:
                out.append('<input type="number" id="%s" value="%s" step="%s"%s>' % (
                    fid, esc(f.get("value", "")), esc(f.get("step", "any")),
                    ' min="%s"' % esc(f["min"]) if "min" in f else ""))
            if f.get("hint"):
                out.append('<span style="font-size:.74rem;color:var(--muted)">%s</span>'
                           % esc(f["hint"]))
            out.append("</div>")
        out.append("</div></div>")
    return "".join(out)


def extract_fields(js_source):
    """Fait évaluer la spec par node pour récupérer la définition des champs."""
    import json, subprocess, tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as fh:
        fh.write(js_source)
        path = fh.name
    try:
        res = subprocess.run(["node", os.path.join(HERE, "extract_fields.js"), path],
                             capture_output=True, text=True)
        if res.returncode:
            raise RuntimeError(res.stderr[:300])
        return json.loads(res.stdout)
    finally:
        os.unlink(path)


def build(spec_path):
    """Charge une spec Python, en extrait le JS et les métadonnées, écrit le HTML."""
    name = os.path.basename(spec_path)[:-3]
    mod_spec = importlib.util.spec_from_file_location(name, spec_path)
    mod = importlib.util.module_from_spec(mod_spec)
    mod_spec.loader.exec_module(mod)
    S = mod.SPEC

    form_html = render_form_html(extract_fields(S["js"]))

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
        "{form_html}": form_html,
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
