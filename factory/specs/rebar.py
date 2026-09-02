SPEC = {
"slug":"rebar-spacing-calculator",
"h1":"Rebar Spacing &amp; Quantity Calculator",
"title_tag":"Rebar Calculator — Bar Count, Spacing and Total Length for a Slab",
"description":"How many bars each way, where they sit, total linear metres including laps, tie count and weight, for any slab size and spacing.",
"card_desc":"Bar count and positions each way, total length with laps, ties and weight for a slab.",
"category":"Finishing",
"intro":"Give the slab size, the spacing and the cover, and this returns how many bars run each way, exactly where they sit, the total linear metres once laps are added, and how many ties you will get through.",
"notes":[("How the count is worked out","The first and last bars sit one cover in from each edge, and the rest are spaced evenly between them. So the count is the clear span divided by the spacing, rounded down, plus one \u2014 the extra bar catches the one at the far edge."),
("Laps","Bars longer than the stock length have to overlap, and the lap is usually expressed as a number of bar diameters. Set it from your own specification \u2014 the default here is a common figure, not a rule."),
("Cover is not optional","Cover is what stops water reaching the steel. Too little and the slab spalls in a few winters; too much and the steel is not doing structural work where it should be. The right figure depends on exposure and comes from the design, not from a calculator."),
("What this does not do","It does not size reinforcement. Bar diameter, spacing and layer position are structural decisions that depend on loads and ground conditions \u2014 this tool lays out what you were told to place.")],
"js":"""
var SPEC = {
  fields: [
    {id:'len', label:'Slab length', value:6000, unit:'length', group:'Slab', min:0},
    {id:'wid', label:'Slab width', value:4000, unit:'length', group:'Slab', min:0},
    {id:'spacing', label:'Bar spacing (centres)', value:200, unit:'length', group:'Slab', min:1},
    {id:'cover', label:'Cover from each edge', value:50, unit:'length', group:'Slab', min:0},
    {id:'dia', label:'Bar diameter', value:12, unit:'length', group:'Bars', min:1},
    {id:'stock', label:'Bar stock length', value:6000, unit:'length', group:'Bars', min:1},
    {id:'lapDia', label:'Lap length (bar diameters)', value:40, group:'Bars', min:0,
     hint:'Set from your own specification'}
  ],
  compute: function (i) {
    var L = i.len, Wd = i.wid, sp = i.spacing, cov = i.cover, dia = i.dia;
    if (!(L > 0 && Wd > 0)) return {ok:false, errors:['Slab length and width must be greater than zero.']};
    if (!(sp > 0)) return {ok:false, errors:['Spacing must be greater than zero.']};
    if (2*cov >= Math.min(L, Wd)) return {ok:false, errors:['Cover on both sides leaves no slab left. Check the numbers.']};

    // Barres paralleles a la longueur : reparties sur la largeur
    var clearW = Wd - 2*cov, clearL = L - 2*cov;
    // L'espacement demande est un MAXIMUM : on arrondit le nombre d'intervalles
    // vers le HAUT, sinon l'espacement reel le depasse.
    // Bug corrige : floor() donnait 20 barres sur 3900 de libre, soit 205 mm
    // d'espacement reel pour 200 demandes.
    var nAlongLen = Math.ceil(clearW/sp) + 1;
    var nAlongWid = Math.ceil(clearL/sp) + 1;
    var actualSpW = nAlongLen > 1 ? clearW/(nAlongLen-1) : 0;
    var actualSpL = nAlongWid > 1 ? clearL/(nAlongWid-1) : 0;

    var barLenL = clearL, barLenW = clearW;
    var lap = Math.max(0, i.lapDia)*dia;
    function withLaps(barLen, stock) {
      if (stock <= 0 || barLen <= stock) return {pieces:1, total:barLen};
      var joints = Math.ceil(barLen/stock) - 1;
      return {pieces: joints+1, total: barLen + joints*lap};
    }
    var a = withLaps(barLenL, i.stock), b = withLaps(barLenW, i.stock);
    var totalLen = nAlongLen*a.total + nAlongWid*b.total;
    var intersections = nAlongLen*nAlongWid;

    // Les saisies sont dans l'unite choisie par l'utilisateur : on convertit
    // avant toute masse ou longueur en metres, sinon le mode pouces donne 0.
    var toMm = i.unit === 'in' ? 25.4 : 1;
    var diaMm = dia*toMm;
    var totalM = totalLen*toMm/1000;
    // Masse : 0.006165 kg par mm de diametre au carre et par metre (acier)
    var kgPerM = 0.006165*diaMm*diaMm;
    var weight = totalM*kgPerM;

    // Une barre se coupe d'un seul tenant : les chutes de deux barres
    // differentes ne s'additionnent pas. On compte donc combien de barres
    // sortent d'une longueur commerciale, direction par direction.
    function stockFor(n, one, total, stock) {
      if (stock <= 0) return n;
      if (one <= stock) {
        var per = Math.floor(stock/one);
        return per > 0 ? Math.ceil(n/per) : n;
      }
      return n*Math.ceil(total/stock);
    }
    var stockCount = stockFor(nAlongLen, barLenL, a.total, i.stock)
                   + stockFor(nAlongWid, barLenW, b.total, i.stock);

    var warn = [];
    if (lap > 0 && (barLenL > i.stock || barLenW > i.stock))
      warn.push('Bars are longer than the stock length, so laps of '+WCfmt(lap,0)+' have been added at each joint.');

    return {ok:true, nL:nAlongLen, nW:nAlongWid, totalLen:totalLen, weight:weight,
      L:L, Wd:Wd, cov:cov, spW:actualSpW, spL:actualSpL,
      warnings: warn,
      stats:[
        {value: String(nAlongLen + nAlongWid), label:'Bars in total'},
        {value: WCfmt(totalM,1), label:'Linear metres'},
        {value: WCfmt(weight,1), label:'Weight (kg)'},
        {value: String(intersections), label:'Ties needed'}
      ],
      tables:[{title:'Layout', head:['Direction','Bars','Actual spacing','Length each','With laps'], rows:[
        ['Along the length', String(nAlongLen), WCfmt(actualSpW,1), WCfmt(barLenL,0), WCfmt(a.total,0)],
        ['Across the width', String(nAlongWid), WCfmt(actualSpL,1), WCfmt(barLenW,0), WCfmt(b.total,0)]
      ]},
      {title:'Order list', head:['Item','Quantity'], rows:[
        ['Bar diameter', WCfmt(dia, i.unit === 'in' ? 2 : 0)],
        ['Total linear length', WCfmt(totalM,2)+' m'],
        ['Stock lengths of '+WCfmt(i.stock,0), String(stockCount)],
        ['Approximate weight', WCfmt(weight,1)+' kg'],
        ['Tie wire points', String(intersections)],
        ['Lap length used', WCfmt(lap,0)+'  ('+WCfmt(i.lapDia,0)+' \u00d7 diameter)']
      ]}],
      note:'Spacing is adjusted so the first and last bars sit exactly one cover in from the edges, and the rest divide the space evenly.'
    };
  },
  diagram: function (r, i) {
    var W=620,H=420,m=40,s=SVG.open(W,H);
    var sc=Math.min((W-2*m)/r.L, (H-2*m-30)/r.Wd);
    var x0=m, y0=m+16, sw=r.L*sc, sh=r.Wd*sc;
    s+=SVG.rect(x0,y0,sw,sh,'ghost');
    for(var k=0;k<r.nL;k++){
      var yy=y0+(r.cov + k*r.spW)*sc;
      s+=SVG.line(x0+r.cov*sc,yy,x0+sw-r.cov*sc,yy,' stroke="var(--accent)" stroke-width="1.6"');
    }
    for(var k=0;k<r.nW;k++){
      var xx=x0+(r.cov + k*r.spL)*sc;
      s+=SVG.line(xx,y0+r.cov*sc,xx,y0+sh-r.cov*sc,' stroke="var(--accent)" stroke-width="1.6" opacity=".72"');
    }
    s+=SVG.text(W/2, 20, r.nL+' + '+r.nW+' bars  \u00b7  '+WCfmt(r.totalLen/1000,1)+' m  \u00b7  '+WCfmt(r.weight,0)+' kg', 13);
    s+=SVG.text(W/2, H-10, WCfmt(r.L,0)+' \u00d7 '+WCfmt(r.Wd,0)+'  \u00b7  cover '+WCfmt(r.cov,0), 12);
    return s+SVG.close();
  }
};
"""}
