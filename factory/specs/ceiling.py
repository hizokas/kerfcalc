SPEC = {
"slug":"ceiling-grid-calculator",
"h1":"Suspended Ceiling Grid Calculator",
"title_tag":"Ceiling Grid Calculator — Tiles, Main Runners, Cross Tees and Balanced Borders",
"description":"Full tile count, border widths balanced on both sides, main runner and cross tee lengths, hanger positions and perimeter trim for a suspended ceiling.",
"card_desc":"Tiles, runners, cross tees and border widths balanced on both sides of the room.",
"category":"Finishing",
"intro":"Start a ceiling grid from one corner and you finish with a full tile on one wall and a 60 mm sliver on the other. This centres the grid so both borders match, then counts every component you have to order.",
"notes":[("Why borders are centred","A ceiling is seen whole, from below, with the eye running to the edges. Unequal borders read as a mistake from the doorway. Centring costs nothing and takes one extra calculation."),
("When to shift the grid off centre","If centring leaves borders narrower than about a third of a tile, drop one tile from the run and re-centre. Two 300 mm borders look intentional; two 40 mm ones look like a cutting error."),
("Hangers","Main runners are normally supported at regular intervals along their length and near each end. The spacing depends on the system and the load above \u2014 set it from your manufacturer, not from a calculator."),
("What this does not do","It lays out a rectangular ceiling. Bulkheads, columns, light fittings and air terminals all displace tiles and are counted separately.")],
"js":"""
var SPEC = {
  fields: [
    {id:'roomL', label:'Room length', value:6000, unit:'length', group:'Room', min:0},
    {id:'roomW', label:'Room width', value:4500, unit:'length', group:'Room', min:0},
    {id:'tileL', label:'Tile length', value:1200, unit:'length', group:'Grid', min:0},
    {id:'tileW', label:'Tile width', value:600, unit:'length', group:'Grid', min:0},
    {id:'runner', label:'Main runner spacing', value:1200, unit:'length', group:'Grid', min:0},
    {id:'hanger', label:'Hanger spacing along runners', value:1200, unit:'length', group:'Grid', min:0},
    {id:'minBorder', label:'Minimum acceptable border', value:200, unit:'length', group:'Grid', min:0}
  ],
  compute: function (i) {
    var L=i.roomL, Wd=i.roomW, tl=i.tileL, tw=i.tileW;
    if (!(L>0 && Wd>0)) return {ok:false, errors:['Room dimensions must be greater than zero.']};
    if (!(tl>0 && tw>0)) return {ok:false, errors:['Tile dimensions must be greater than zero.']};

    function centre(span, tile, minB) {
      var n = Math.floor(span/tile);
      var border = (span - n*tile)/2;
      var adjusted = false;
      if (border > 0.5 && border < minB && n >= 1) { n -= 1; border = (span - n*tile)/2; adjusted = true; }
      return {full:n, border:border, adjusted:adjusted};
    }
    var aL = centre(L, tl, i.minBorder);
    var aW = centre(Wd, tw, i.minBorder);

    var fullTiles = aL.full*aW.full;
    var borderTilesL = (aL.border>0.5 ? 2*aW.full : 0);
    var borderTilesW = (aW.border>0.5 ? 2*aL.full : 0);
    var corners = (aL.border>0.5 && aW.border>0.5) ? 4 : 0;
    var totalTiles = fullTiles + borderTilesL + borderTilesW + corners;

    var runnerRows = i.runner>0 ? Math.floor(Wd/i.runner)+1 : 0;
    var runnerLen = runnerRows*L;
    var crossTees = runnerRows>0 ? (runnerRows-1>=0 ? Math.max(0,(runnerRows))*Math.max(0,Math.floor(L/tw)) : 0) : 0;
    var hangers = (i.hanger>0 && runnerRows>0) ? runnerRows*(Math.floor(L/i.hanger)+1) : 0;
    var perimeter = 2*(L+Wd);

    var warn=[];
    if (aL.adjusted || aW.adjusted) warn.push('One row was dropped so the borders stay above '+WCfmt(i.minBorder,0)+'. Borders are now '+WCfmt(aL.border,0)+' and '+WCfmt(aW.border,0)+'.');

    // Les longueurs sont annoncees en metres : convertir la saisie.
    var toMm = i.unit === 'in' ? 25.4 : 1;

    return {ok:true, aL:aL, aW:aW, totalTiles:totalTiles, fullTiles:fullTiles, L:L, Wd:Wd, tl:tl, tw:tw,
      warnings: warn,
      stats:[
        {value: String(totalTiles), label:'Tiles in total'},
        {value: String(fullTiles), label:'Full tiles'},
        {value: WCfmt(aL.border,0)+' / '+WCfmt(aW.border,0), label:'Border widths'},
        {value: WCfmt(runnerLen*toMm/1000,1), label:'m of main runner'}
      ],
      tables:[{title:'Take-off', head:['Item','Quantity'], rows:[
        ['Room', WCfmt(L,0)+' \u00d7 '+WCfmt(Wd,0)],
        ['Tile size', WCfmt(tl,0)+' \u00d7 '+WCfmt(tw,0)],
        ['Full tiles', String(fullTiles)+'  ('+aL.full+' \u00d7 '+aW.full+')'],
        ['Border along the length', WCfmt(aL.border,1)+' each end'],
        ['Border along the width', WCfmt(aW.border,1)+' each side'],
        ['Cut border tiles', String(borderTilesL+borderTilesW+corners)],
        ['Tiles to order', String(totalTiles)],
        ['Main runners', String(runnerRows)+' rows, '+WCfmt(runnerLen*toMm/1000,2)+' m'],
        ['Cross tees', String(crossTees)],
        ['Hangers', String(hangers)],
        ['Perimeter trim', WCfmt(perimeter*toMm/1000,2)+' m']
      ]}],
      note:'Set out from the centre of the room in both directions so the border tiles match on opposite walls.'
    };
  },
  diagram: function (r, i) {
    var W=620,H=420,m=34,s=SVG.open(W,H);
    var sc=Math.min((W-2*m)/r.L,(H-2*m-24)/r.Wd);
    var x0=m,y0=m+16,rw=r.L*sc,rh=r.Wd*sc;
    s+=SVG.rect(x0,y0,rw,rh,'ghost');
    var bx=r.aL.border*sc, by=r.aW.border*sc, tw=r.tl*sc, th=r.tw*sc;
    for(var a=0;a<r.aL.full;a++) for(var b=0;b<r.aW.full;b++)
      s+=SVG.rect(x0+bx+a*tw+0.5, y0+by+b*th+0.5, tw-1, th-1, 'part');
    s+=SVG.text(W/2,20, r.totalTiles+' tiles  \u00b7  borders '+WCfmt(r.aL.border,0)+' and '+WCfmt(r.aW.border,0), 13);
    s+=SVG.text(W/2,H-8, WCfmt(r.L,0)+' \u00d7 '+WCfmt(r.Wd,0)+'  \u00b7  tile '+WCfmt(r.tl,0)+' \u00d7 '+WCfmt(r.tw,0), 12);
    return s+SVG.close();
  }
};
"""}
