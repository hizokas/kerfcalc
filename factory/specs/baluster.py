SPEC = {
"slug":"baluster-spacing-calculator",
"h1":"Baluster &amp; Spindle Spacing Calculator",
"title_tag":"Baluster Spacing Calculator — Even Gaps That Divide Exactly",
"description":"Work out how many balusters fit a run and the exact even gap between them, so the last space is not a stubby offcut. Includes the centre-to-centre setting out.",
"card_desc":"How many spindles fit, with a gap that divides evenly and a centre-to-centre marking list.",
"category":"Framing",
"intro":"Set spindles at a round number and the last gap ends up wrong for the life of the balustrade. This works the other way round: it finds the smallest count whose gap stays under your limit, then divides the run exactly.",
"notes":[("Why you work backwards from the gap","The gap is what people see and what usually has a maximum. So you fix the maximum, find the smallest number of spindles that respects it, and let the actual gap land wherever it lands \u2014 evenly."),
("Gaps and safety limits","Balustrade gap limits vary by country and by where the balustrade is. Set the maximum yourself from whatever applies to your job \u2014 this tool does not know your local rules and does not pretend to."),
("Setting out on site","Mark centres, not gaps. Measuring gap to gap accumulates error and the last spindle ends up visibly off. Every centre in the table is measured from the same end."),
("What this does not do","It lays out a straight run between two posts. Curved runs, rake sections and transitions each need their own setting out.")],
"js":"""
var SPEC = {
  fields: [
    {id:'run', label:'Clear run between posts', value:2400, unit:'length', group:'Run', min:0},
    {id:'width', label:'Baluster width', value:32, unit:'length', group:'Run', min:0},
    {id:'maxGap', label:'Maximum gap allowed', value:99, unit:'length', group:'Run', min:1,
     hint:'Set this from the rules that apply to your job'},
    {id:'ends', label:'Gap at each end too', type:'check', value:true, group:'Run',
     hint:'Unticked: a baluster sits hard against each post'}
  ],
  compute: function (i) {
    var L = i.run, w = i.width, g = i.maxGap;
    if (!(L > 0)) return {ok:false, errors:['The run must be greater than zero.']};
    if (!(w > 0)) return {ok:false, errors:['Baluster width must be greater than zero.']};
    if (!(g > 0)) return {ok:false, errors:['The maximum gap must be greater than zero.']};
    if (w + g > L) return {ok:false, errors:['One baluster plus one gap is wider than the whole run.']};

    // Avec n balustres et un jeu a chaque bout : n+1 intervalles.
    // Sans jeu aux bouts : n-1 intervalles entre les balustres.
    var n, gaps, gap;
    for (n = 1; n < 10000; n++) {
      gaps = i.ends ? (n + 1) : (n - 1);
      if (gaps <= 0) continue;
      gap = (L - n*w) / gaps;
      if (gap <= g) break;
    }
    if (gap <= 0) return {ok:false, errors:['No arrangement fits \u2014 the balusters alone are wider than the run.']};

    var pitch = w + gap;
    var centres = [];
    for (var k = 0; k < n; k++) {
      var start = i.ends ? gap : 0;
      centres.push(start + k*pitch + w/2);
    }

    var warn = [];
    if (gap < w*0.4) warn.push('The gap ('+WCfmt(gap,1)+') is much narrower than the balusters. Visually heavy \u2014 worth checking against a sample.');

    return {ok:true, n:n, gap:gap, pitch:pitch, centres:centres, L:L, w:w,
      warnings: warn,
      stats:[
        {value: String(n), label:'Balusters'},
        {value: WCfmt(gap,2), label:'Actual gap'},
        {value: WCfmt(pitch,2), label:'Centre to centre'},
        {value: String(gaps), label:'Spaces'}
      ],
      tables:[
        {title:'Check', head:['Item','Value'], rows:[
          ['Clear run', WCfmt(L,1)],
          ['Balusters', String(n)+' at '+WCfmt(w,1)+' wide'],
          ['Spaces', String(gaps)],
          ['Actual gap', WCfmt(gap,3)+'  (limit '+WCfmt(g,1)+')'],
          ['Centre to centre', WCfmt(pitch,3)],
          ['Total check', WCfmt(n*w + gaps*gap,2)+' should equal '+WCfmt(L,2)]
        ]},
        {title:'Centres from the left post', head:['#','Centre'],
         rows: centres.map(function(c,k){ return [String(k+1), WCfmt(c,1)]; })}
      ],
      note:'Mark every centre from the same end. Measuring spindle to spindle lets small errors pile up, and the last gap always pays for it.'
    };
  },
  diagram: function (r, i) {
    var W=760,H=190,m=30,s=SVG.open(W,H);
    var sc=(W-2*m)/r.L, y=45, h=100, bw=Math.max(3, r.w*sc);
    s+=SVG.rect(m-10,y-12,10,h+24,'part');
    s+=SVG.rect(m+r.L*sc,y-12,10,h+24,'part');
    r.centres.forEach(function(c,k){
      s+=SVG.rect(m + c*sc - bw/2, y, bw, h, 'part');
    });
    s+=SVG.line(m,y+h+22,m+r.L*sc,y+h+22,' class="dim"');
    s+=SVG.text(W/2, y+h+40, r.n+' balusters  \u00b7  gap '+WCfmt(r.gap,1)+'  \u00b7  run '+WCfmt(r.L,0), 12);
    s+=SVG.text(W/2, 26, 'centre to centre '+WCfmt(r.pitch,1), 12);
    return s+SVG.close();
  }
};
"""}
