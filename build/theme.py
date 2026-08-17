#!/usr/bin/env python3
"""
Passe de style : applique l'identité visuelle à toutes les pages.

Idempotent — on peut le relancer autant de fois qu'on veut.
Il injecte un bandeau de marque et un bloc CSS qui écrase les règles de base
(la cascade fait que ce qui est ajouté en dernier gagne), donc il fonctionne
aussi bien sur les outils écrits à la main que sur ceux sortis de la fabrique.
"""

import os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
MARK = "/* === KERFCALC THEME v3 === */"

THEME = MARK + """
@import url('');
:root{
  --bg:#faf8f5; --surface:#ffffff; --ink:#1b1a17; --muted:#6f6a61;
  --line:#e7e2d9; --accent:#a8622a; --accent-soft:#fbf1e7; --accent-ink:#8a4e1f;
  --shadow:0 1px 2px rgba(27,26,23,.05), 0 8px 24px -12px rgba(27,26,23,.14);
  --radius:14px;
}
@media (prefers-color-scheme:dark){
  :root{
    --bg:#14140f; --surface:#1c1c18; --ink:#f0ece4; --muted:#a09a8e;
    --line:#2e2e28; --accent:#e0a06a; --accent-soft:#2a2018; --accent-ink:#f0c79b;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px -12px rgba(0,0,0,.6);
  }
}
html{-webkit-text-size-adjust:100%}
body{
  background:var(--bg); color:var(--ink);
  font:16.5px/1.62 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Inter,Roboto,sans-serif;
  letter-spacing:-.005em;
}
.wrap{max-width:1020px;padding:0 22px 90px}

/* ---- bandeau de marque ---- */
.masthead{
  display:flex;align-items:center;justify-content:space-between;gap:16px;
  padding:18px 0 22px;margin-bottom:26px;border-bottom:1px solid var(--line);
}
.brand{display:inline-flex;align-items:center;gap:9px;text-decoration:none;color:var(--ink)}
.brand svg{display:block}
.brand b{font-size:1.06rem;font-weight:650;letter-spacing:-.02em}
.brand span{color:var(--muted);font-weight:400}
.masthead nav a{color:var(--muted);text-decoration:none;font-size:.88rem}
.masthead nav a:hover{color:var(--accent)}

h1{font-size:2.15rem;line-height:1.12;letter-spacing:-.035em;font-weight:680;margin:0 0 10px}
.sub{font-size:1.06rem;line-height:1.6;color:var(--muted);max-width:65ch;margin:0 0 30px}
h2{font-size:.74rem;font-weight:640;letter-spacing:.11em;text-transform:uppercase;color:var(--muted);margin:0 0 15px}
h3{font-size:.98rem;font-weight:620;letter-spacing:-.01em}

.card{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  padding:22px;margin-bottom:18px;box-shadow:var(--shadow);
}

/* ---- cartes de la page d'accueil ---- */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(272px,1fr));gap:14px}
.tool{
  padding:19px 19px 21px;border-radius:var(--radius);box-shadow:var(--shadow);
  transition:transform .16s ease, border-color .16s ease, box-shadow .16s ease;
}
.tool:hover{
  transform:translateY(-2px);border-color:var(--accent);
  box-shadow:0 2px 4px rgba(27,26,23,.06), 0 16px 32px -16px rgba(168,98,42,.4);
  background:var(--surface);
}
.tool strong{font-size:1.02rem;font-weight:620;letter-spacing:-.015em;margin-bottom:2px}
.tool span{font-size:.885rem;line-height:1.5}

/* ---- formulaires ---- */
.row{gap:16px 18px}
.f label{font-size:.79rem;font-weight:520;color:var(--muted);letter-spacing:.005em}
input,select{
  border-radius:9px;padding:9px 11px;font-size:.95rem;
  border:1px solid var(--line);background:var(--bg);color:var(--ink);
  transition:border-color .14s ease, box-shadow .14s ease;
}
input:hover,select:hover{border-color:var(--muted)}
input:focus,select:focus{
  outline:none;border-color:var(--accent);
  box-shadow:0 0 0 3px color-mix(in srgb, var(--accent) 18%, transparent);
}
input[type=checkbox]{width:17px;height:17px;accent-color:var(--accent)}

button{
  border-radius:9px;padding:9px 15px;font-size:.92rem;font-weight:520;
  border:1px solid var(--line);background:var(--surface);color:var(--ink);
  transition:border-color .14s ease, background .14s ease, transform .1s ease;
}
button:hover{border-color:var(--accent);background:var(--accent-soft)}
button:active{transform:translateY(1px)}
.primary{
  background:var(--accent);border-color:var(--accent);color:#fff;font-weight:580;
  padding:11px 22px;box-shadow:0 1px 2px rgba(0,0,0,.08);
}
.primary:hover{background:var(--accent-ink);border-color:var(--accent-ink);color:#fff}

/* ---- tuiles de résultat ---- */
.stats{gap:12px;margin-bottom:20px}
.stat{
  background:var(--accent-soft);border:1px solid var(--line);border-radius:12px;
  padding:13px 17px;min-width:118px;
}
.stat b{font-size:1.62rem;font-weight:640;letter-spacing:-.03em;line-height:1.15;
  font-variant-numeric:tabular-nums}
.stat span{font-size:.7rem;font-weight:560;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}

/* ---- tableaux ---- */
table{font-size:.91rem;border-collapse:collapse;width:100%}
th{font-size:.69rem;font-weight:620;letter-spacing:.09em;color:var(--muted);
  padding:9px 10px;border-bottom:1px solid var(--line)}
td{padding:8px 10px;border-bottom:1px solid var(--line);font-variant-numeric:tabular-nums}
tbody tr:hover{background:var(--accent-soft)}

/* ---- schémas ---- */
svg{border-radius:11px;border:1px solid var(--line);background:var(--surface)}
.part{fill:var(--accent-soft);stroke:var(--accent);stroke-width:1.4}
.plabel{fill:var(--ink);font-family:ui-monospace,SFMono-Regular,Menlo,monospace;
  letter-spacing:-.02em}

.warn{
  background:var(--accent-soft);border:1px solid var(--accent);color:var(--accent-ink);
  border-radius:11px;padding:13px 16px;font-size:.9rem;
}
@media (prefers-color-scheme:dark){.warn{color:var(--accent-ink)}}

.faq p{font-size:.925rem;line-height:1.62}
footer{font-size:.845rem;color:var(--muted);margin-top:44px;padding-top:20px;
  border-top:1px solid var(--line)}

@media (max-width:640px){
  h1{font-size:1.68rem}
  .wrap{padding:0 16px 70px}
  .card{padding:17px}
  .stat b{font-size:1.4rem}
}

/* ---- fond papier millimetre : c'est un site de tracage, ca se voit ---- */
body{
  background-color:var(--bg);
  background-image:
    linear-gradient(to right, color-mix(in srgb, var(--line) 55%, transparent) 1px, transparent 1px),
    linear-gradient(to bottom, color-mix(in srgb, var(--line) 55%, transparent) 1px, transparent 1px),
    radial-gradient(1200px 520px at 78% -8%, color-mix(in srgb, var(--accent) 9%, transparent), transparent 70%);
  background-size:28px 28px, 28px 28px, 100% 100%;
  background-attachment:fixed, fixed, fixed;
}

/* ---- bandeau collant ---- */
.masthead{
  position:sticky;top:0;z-index:50;margin-bottom:30px;
  padding:14px 0 13px;
  background:color-mix(in srgb, var(--bg) 84%, transparent);
  backdrop-filter:saturate(1.6) blur(12px);
  -webkit-backdrop-filter:saturate(1.6) blur(12px);
}
.masthead .brand b{font-size:1.08rem}
.brand svg{color:var(--accent)}
.mnav{display:flex;align-items:center;gap:20px}
.mnav a{color:var(--muted);text-decoration:none;font-size:.875rem;font-weight:500}
.mnav a:hover{color:var(--ink)}
.mnav .cta{
  color:#fff;background:var(--accent);border:1px solid var(--accent);
  padding:7px 15px;border-radius:9px;font-weight:560;
}
.mnav .cta:hover{background:var(--accent-ink);border-color:var(--accent-ink);color:#fff}
@media (max-width:700px){.mnav a:not(.cta){display:none}}

/* ---- profondeur sur les cartes ---- */
.card,.tool,.shot,.faqitem,.whyitem,.band{position:relative;overflow:hidden}
.tool::before,.shot::before{
  content:"";position:absolute;inset:0 0 auto 0;height:2px;
  background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent) 30%,transparent));
  opacity:0;transition:opacity .2s ease;
}
.tool:hover::before{opacity:1}
.tool{transition:transform .18s cubic-bezier(.2,.7,.3,1),box-shadow .18s ease,border-color .18s ease}
.tool:hover{transform:translateY(-3px);border-color:color-mix(in srgb,var(--accent) 55%,var(--line));
  box-shadow:0 2px 4px rgba(27,26,23,.05),0 18px 38px -18px color-mix(in srgb,var(--accent) 65%,transparent)}

/* ---- apparition au defilement ---- */
.reveal{opacity:0;transform:translateY(14px)}
.reveal.in{opacity:1;transform:none;transition:opacity .55s ease,transform .55s cubic-bezier(.2,.7,.3,1)}
@media (prefers-reduced-motion:reduce){
  .reveal,.reveal.in{opacity:1;transform:none;transition:none}
  .tool:hover{transform:none}
}

/* ---- trace anime du plan dans le heros ---- */
@keyframes drawin{from{opacity:0;transform:scale(.985)}to{opacity:1;transform:none}}
.herowrap .figsvg{animation:drawin .7s cubic-bezier(.2,.7,.3,1) both}

/* ---- pied de page ---- */
footer{margin-top:60px}
.footgrid{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:26px;margin-bottom:22px}
.footgrid h5{margin:0 0 9px;font-size:.72rem;font-weight:620;letter-spacing:.09em;
  text-transform:uppercase;color:var(--muted)}
.footgrid a{display:block;color:var(--muted);text-decoration:none;font-size:.88rem;padding:2px 0}
.footgrid a:hover{color:var(--accent)}
.footnote{font-size:.82rem;color:var(--muted);border-top:1px solid var(--line);padding-top:16px}
@media (max-width:700px){.footgrid{grid-template-columns:1fr 1fr}}

@media print{
  .masthead,.noprint{display:none!important}
  .card{box-shadow:none;border:1px solid #ddd}
  body{background:#fff}
}
"""

LOGO = ('<svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<rect x="2.5" y="2.5" width="19" height="19" rx="4" stroke="currentColor" '
        'stroke-width="1.7" opacity=".28"/>'
        '<path d="M7 17V7M7 12l5-5M7 12l5 5" stroke="currentColor" stroke-width="1.9" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M16 7v10" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" '
        'stroke-dasharray="1.5 3"/></svg>')


# Compte les outils reellement presents : le nombre etait ecrit en dur
# ("Browse all 15") et mentait des le 16e outil.
N_TOOLS = len([f for f in os.listdir(os.path.dirname(os.path.abspath(__file__)))
               if f.endswith('.html') and f != 'index.html'])


def masthead(is_index):
    left = (f'<a class="brand" href="./index.html">{LOGO}<b>Kerf<span>Calc</span></b></a>')
    if is_index:
        right = ('<nav class="mnav">'
                 '<a href="#tools">Tools</a>'
                 '<a href="#what">What you get</a>'
                 f'<a class="cta" href="#tools">Browse all {N_TOOLS} &rarr;</a></nav>')
    else:
        right = ('<nav class="mnav">'
                 '<a href="./index.html">All tools</a>'
                 '<a class="cta" href="./index.html">Back to KerfCalc &rarr;</a></nav>')
    return f'<header class="masthead noprint">{left}{right}</header>'


def apply_to(path):
    src = open(path).read()
    is_index = os.path.basename(path) == 'index.html'

    # 1. CSS — on remplace la version precedente si elle est deja la
    if MARK in src:
        src = re.sub(re.escape(MARK) + r".*?(?=</style>)", "", src, flags=re.S)
    src = src.replace('</style>', THEME + '\n</style>', 1)

    # 2. Bandeau — on retire l'ancien avant d'ajouter le nouveau
    src = re.sub(r'<header class="masthead[^"]*">.*?</header>', '', src, flags=re.S)
    src = re.sub(r'<nav id="site-nav".*?</nav>', '', src, flags=re.S)
    src = re.sub(r'(<div class="wrap">)', r'\1\n' + masthead(is_index), src, count=1)

    # 3. Apparition au defilement (leger, sans dependance)
    src = re.sub(r'<script id="reveal">.*?</script>', '', src, flags=re.S)
    reveal = ('<script id="reveal">(function(){var m=window.matchMedia&&'
              'window.matchMedia("(prefers-reduced-motion: reduce)").matches;'
              'var els=document.querySelectorAll(".card,.tool,.shot,.faqitem,.band,.catblock,.showcase");'
              'if(m||!("IntersectionObserver" in window)){return;}'
              'els.forEach(function(e){e.classList.add("reveal");});'
              'var io=new IntersectionObserver(function(es){es.forEach(function(en){'
              'if(en.isIntersecting){en.target.classList.add("in");io.unobserve(en.target);}});},'
              '{rootMargin:"0px 0px -40px 0px",threshold:.06});'
              'els.forEach(function(e){io.observe(e);});})();</script>')
    src = src.replace('</body>', reveal + '\n</body>', 1)

    open(path, 'w').write(src)
    return os.path.basename(path)


if __name__ == '__main__':
    done = [apply_to(p) for p in sorted(glob.glob(os.path.join(HERE, '*.html')))]
    print(f"Habillage appliqué à {len(done)} pages")
