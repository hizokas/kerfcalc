#!/bin/sh
# Ordre de construction. theme.py DOIT etre lance en dernier :
# build-home.py regenere index.html a partir de zero et efface l'habillage.
# Bug reel : la page d'accueil est partie en production sans son theme.
set -e
cd "$(dirname "$0")"
(cd ../factory && python3 build.py)
python3 build-index.py
python3 build-home.py
python3 theme.py      # <-- toujours en dernier
echo "OK — construction terminee dans le bon ordre"
