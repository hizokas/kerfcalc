/* ============================================================================
   Runtime partagé des outils Workshop Calc.
   Écrit UNE fois, embarqué dans chaque outil généré.
   Chaque outil ne fournit que : ses champs, sa formule, son schéma, ses notes.
   ========================================================================== */
(function () {
  'use strict';

  var SPEC = window.__SPEC__;
  var $ = function (s) { return document.querySelector(s); };

  /* ---- unités ------------------------------------------------------------ */
  var UNITS = {
    mm: { label: 'mm', toBase: 1, area: 'm²', vol: 'm³' },
    in: { label: 'in', toBase: 25.4, area: 'ft²', vol: 'ft³' }
  };
  function unit() { return $('#unit') ? $('#unit').value : 'mm'; }

  function num(v, fallback) {
    var n = parseFloat(v);
    return isFinite(n) ? n : (fallback === undefined ? NaN : fallback);
  }

  /* ---- formatage --------------------------------------------------------- */
  function fmt(v, dp) {
    if (v === null || v === undefined || !isFinite(v)) return '—';
    dp = dp === undefined ? 1 : dp;
    return (Math.round(v * Math.pow(10, dp)) / Math.pow(10, dp))
      .toLocaleString('en-US', { maximumFractionDigits: dp });
  }
  function esc(t) {
    var d = document.createElement('div');
    d.textContent = String(t === undefined || t === null ? '' : t);
    return d.innerHTML;
  }

  /* ---- construction du formulaire ---------------------------------------- */
  function buildForm() {
    var groups = {};
    SPEC.fields.forEach(function (f) {
      var g = f.group || 'Inputs';
      (groups[g] = groups[g] || []).push(f);
    });

    var html = '';
    Object.keys(groups).forEach(function (g) {
      html += '<div class="card noprint"><h2>' + esc(g) + '</h2><div class="row">';
      groups[g].forEach(function (f) {
        html += '<div class="f"><label for="' + f.id + '">' + esc(f.label) +
                (f.unit === 'length' ? ' <span class="u"></span>' : '') + '</label>';
        if (f.type === 'select') {
          html += '<select id="' + f.id + '">' + f.options.map(function (o) {
            return '<option value="' + esc(o.value) + '"' +
                   (o.value === f.value ? ' selected' : '') + '>' + esc(o.label) + '</option>';
          }).join('') + '</select>';
        } else if (f.type === 'check') {
          html += '<input type="checkbox" id="' + f.id + '"' + (f.value ? ' checked' : '') + '>';
        } else {
          html += '<input type="number" id="' + f.id + '" value="' + f.value +
                  '" step="' + (f.step || 'any') + '"' +
                  (f.min !== undefined ? ' min="' + f.min + '"' : '') + '>';
        }
        if (f.hint) html += '<span style="font-size:.74rem;color:var(--muted)">' + esc(f.hint) + '</span>';
        html += '</div>';
      });
      html += '</div></div>';
    });
    $('#form').innerHTML = html;
  }

  function readInputs() {
    var o = { unit: unit() };
    SPEC.fields.forEach(function (f) {
      var el = $('#' + f.id);
      if (!el) return;
      if (f.type === 'check') o[f.id] = el.checked;
      else if (f.type === 'select') o[f.id] = el.value;
      else o[f.id] = num(el.value, 0);
    });
    return o;
  }

  /* ---- rendu du résultat -------------------------------------------------- */
  function render() {
    var input = readInputs();
    var res;
    try { res = SPEC.compute(input); }
    catch (err) { res = { ok: false, errors: ['Something went wrong: ' + err.message] }; }

    var out = $('#out');
    if (!res || res.ok === false) {
      out.innerHTML = '<div class="card"><div class="warn"><strong>Cannot work this out:</strong><ul style="margin:6px 0 0;padding-left:18px">' +
        ((res && res.errors) || ['Check your inputs.']).map(function (e) { return '<li>' + esc(e) + '</li>'; }).join('') +
        '</ul></div></div>';
      return;
    }

    var html = '<div class="card">';

    if (res.warnings && res.warnings.length) {
      html += '<div class="warn"><ul style="margin:0;padding-left:18px">' +
        res.warnings.map(function (w) { return '<li>' + esc(w) + '</li>'; }).join('') + '</ul></div>';
    }

    if (res.stats && res.stats.length) {
      html += '<div class="stats">' + res.stats.map(function (s) {
        return '<div class="stat"><b>' + esc(s.value) + '</b><span>' + esc(s.label) + '</span></div>';
      }).join('') + '</div>';
    }

    html += '<button class="primary noprint" onclick="window.print()">Print this</button>';

    if (SPEC.diagram) {
      try {
        var svg = SPEC.diagram(res, input);
        if (svg) html += '<div style="margin-top:16px">' + svg + '</div>';
      } catch (e) { /* un schéma cassé ne doit pas emporter le résultat */ }
    }

    if (res.tables) {
      res.tables.forEach(function (t) {
        if (!t.rows || !t.rows.length) return;
        html += '<h3 style="font-size:.95rem;margin:20px 0 8px">' + esc(t.title) + '</h3>';
        html += '<table><thead><tr>' + t.head.map(function (h) { return '<th>' + esc(h) + '</th>'; }).join('') +
                '</tr></thead><tbody>' + t.rows.map(function (r) {
                  return '<tr>' + r.map(function (c) { return '<td>' + esc(c) + '</td>'; }).join('') + '</tr>';
                }).join('') + '</tbody></table>';
      });
    }

    if (res.note) {
      html += '<p style="color:var(--muted);font-size:.88rem;margin-top:14px">' + esc(res.note) + '</p>';
    }

    html += '</div>';
    out.innerHTML = html;
  }

  /* ---- aides au dessin ---------------------------------------------------- */
  window.SVG = {
    open: function (w, h, extra) {
      return '<svg viewBox="0 0 ' + w + ' ' + h + '" preserveAspectRatio="xMidYMid meet"' +
             (extra || '') + '>';
    },
    close: function () { return '</svg>'; },
    rect: function (x, y, w, h, cls, extra) {
      return '<rect x="' + x + '" y="' + y + '" width="' + Math.max(0, w) + '" height="' + Math.max(0, h) +
             '" class="' + (cls || 'part') + '"' + (extra || '') + '/>';
    },
    line: function (x1, y1, x2, y2, extra) {
      return '<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 +
             '" stroke="currentColor" stroke-width="1"' + (extra || '') + '/>';
    },
    text: function (x, y, t, size, anchor) {
      return '<text x="' + x + '" y="' + y + '" text-anchor="' + (anchor || 'middle') +
             '" class="plabel" style="font-size:' + (size || 12) + 'px">' + esc(t) + '</text>';
    },
    poly: function (pts, cls) {
      return '<polygon points="' + pts.map(function (p) { return p[0] + ',' + p[1]; }).join(' ') +
             '" class="' + (cls || 'part') + '"/>';
    }
  };

  window.WCfmt = fmt;
  window.WCesc = esc;

  /* ---- démarrage ---------------------------------------------------------- */
  function syncUnitLabels() {
    var u = UNITS[unit()].label;
    [].forEach.call(document.querySelectorAll('.u'), function (e) { e.textContent = '(' + u + ')'; });
  }

  function boot() {
    buildForm();
    syncUnitLabels();
    document.addEventListener('input', function (e) {
      if (e.target.id === 'unit') {
        if (SPEC.onUnitChange) SPEC.onUnitChange(unit(), $);
        syncUnitLabels();
      }
      render();
    });
    document.addEventListener('change', render);
    render();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
