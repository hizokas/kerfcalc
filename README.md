# KerfCalc

Free workshop calculators that solve the layout and draw it to scale.
Live at **https://getkerfcalc.com**

Static site, no build step, no dependencies at runtime. Every tool is a single
self-contained HTML file that runs entirely in the browser: no accounts, no
storage, no tracking, no network calls.

## Layout

    public/     Ce qui est publié. Cloudflare sert ce dossier tel quel.
    build/      Scripts d'assemblage (maillage, page d'accueil, habillage)
    factory/    La fabrique : moteur partagé + une spec par outil

## Ajouter un outil

    cp factory/specs/paint.py factory/specs/mon-outil.py   # partir d'un modèle
    # définir : champs, compute(), diagram(), notes
    cd factory && python3 build.py                          # génère le HTML
    # ajouter l'entrée dans build/build-index.py (liste TOOLS)
    cd ../build && python3 build-index.py && python3 build-home.py && python3 theme.py
    git add -A && git commit -m "Add mon-outil" && git push

Le push déclenche le déploiement Cloudflare automatiquement.

## Règles à ne pas réapprendre

- Chercher un terme dans le **texte visible**, jamais dans le HTML brut :
  « bot » matche « cookiebot », « ia » matche « médiation ».
- Supprimer un bloc injecté **de façon inconditionnelle** avant de le
  réinjecter, avec un motif qui tolère les attributs. Sinon il s'empile.
- Dimensionner le texte d'un SVG d'après la **place disponible ET la longueur
  du libellé**, jamais d'après la taille de la pièce seule.
- **Vérifier chaque calcul avec node** et recalculer deux cas à la main avant
  de publier. Un mauvais chiffre détruit la crédibilité de tout le site.
- **Pas de génération de masse.** 25 à 40 outils réellement distincts, pas
  plus : la mise à jour anti-spam de juin 2026 vise les pages en rafale.

## Rendez-vous

- ~25 août 2026 : `site:getkerfcalc.com` doit renvoyer des pages
- mi-septembre : premières impressions dans la Search Console
- 10 octobre : décision (80 % indexé, 1 000 impressions, 100 clics)
