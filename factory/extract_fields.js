// Extrait la définition des champs d'une spec, pour que build.py puisse
// écrire le formulaire en HTML statique au lieu de le laisser au JavaScript.
// Le JS de la spec est exécuté dans une fonction isolée, avec des doublures
// pour les aides du runtime qu'il ne doit pas réellement appeler ici.
const fs = require('fs');
const js = fs.readFileSync(process.argv[2], 'utf8');
const WCfmt = (v, d) => String(v);
const WCesc = s => s;
const SVG = new Proxy({}, { get: () => () => '' });
const fn = new Function('WCfmt', 'WCesc', 'SVG', js + '\nreturn SPEC;');
const spec = fn(WCfmt, WCesc, SVG);
process.stdout.write(JSON.stringify(spec.fields));
