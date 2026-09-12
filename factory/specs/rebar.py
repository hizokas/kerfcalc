SPEC = {
"slug":"rebar-spacing-calculator",
"h1":"Rebar Spacing &amp; Quantity Calculator",
"title_tag":"Rebar Calculator — Bar Count, Spacing and Total Length for a Slab",
"description":"How many bars each way, where they sit, total linear metres including laps, tie count and weight, for any slab size and spacing.",
"card_desc":"Bar count and positions each way, total length with laps, ties and weight for a slab.",
"category":"Finishing",
"intro":"Give the slab size, the spacing and the cover, and this returns how many bars run each way, exactly where they sit, the total linear metres once laps are added, and how many ties you will get through.",
"notes":[("How the count is worked out","The requested spacing is a maximum, measured centre to centre. Subtract twice the edge-to-centre distance from the perpendicular slab dimension. Divide that span by the maximum spacing, round UP to get the number of intervals, then add one bar. Actual spacing is the span divided by the number of intervals."),
("Worked example: 6 m by 4 m slab","With bar centrelines 50 mm from each edge and maximum spacing of 200 mm, the spans are 5,900 mm and 3,900 mm. The 3,900 mm span needs ceil(3900 / 200) + 1 = 21 bars along the length, at 195 mm centres. The other direction needs 31 bars at 196.7 mm centres. That is 52 bars, 244.8 m of steel before any laps, and 651 crossings for a single two-way grid."),
("What the edge distance means","The input is the distance from the slab edge to the BAR CENTRELINE, not clear concrete cover to the steel surface. If your drawing specifies clear cover, add half the bar diameter to obtain this centreline distance. Confirm the layout and cover with your designer."),
("Laps","Bars longer than the stock length have to overlap, and the lap is usually expressed as a number of bar diameters. Set it from your own specification \u2014 the default here is a common figure, not a rule."),
("Buying stock and counting ties","Stock quantities are conservative: each direction is cut separately and offcuts are not shared between directions or spliced runs. For a spliced run, each extra stock piece adds stock length minus one lap to the covered distance. The tie figure is one tie per crossing for one grid; it is not a tying specification and does not include extra layers or chairs."),
("What this does not do","It does not size reinforcement. Bar diameter, spacing and layer position are structural decisions that depend on loads and ground conditions \u2014 this tool lays out what you were told to place.")],
"js":"""
var SPEC = {
  fields: [
    {id:'len', label:'Slab length', value:6000, unit:'length', group:'Slab', min:0},
    {id:'wid', label:'Slab width', value:4000, unit:'length', group:'Slab', min:0},
    {id:'spacing', label:'Bar spacing (centres)', value:200, unit:'length', group:'Slab', min:1},
    {id:'cover', label:'Edge to bar centreline', value:50, unit:'length', group:'Slab', min:0,
     hint:'Clear concrete cover + half the bar diameter'},
    {id:'dia', label:'Bar diameter', value:12, unit:'length', group:'Bars', min:1},
    {id:'stock', label:'Bar stock length', value:6000, unit:'length', group:'Bars', min:1},
    {id:'lapDia', label:'Lap length (bar diameters)', value:40, group:'Bars', min:0,
     hint:'Set from your own specification'}
  ],
  compute: function (i) {
    var L = i.len, Wd = i.wid, sp = i.spacing, cov = i.cover, dia = i.dia;
    if (![L,Wd,sp,cov,dia,i.stock,i.lapDia].every(Number.isFinite))
      return {ok:false, errors:['Enter a finite number in every field.']};
    if (!(L > 0 && Wd > 0)) return {ok:false, errors:['Slab length and width must be greater than zero.']};
    if (!(sp > 0)) return {ok:false, errors:['Spacing must be greater than zero.']};
    if (cov < 0 || dia <= 0 || i.stock <= 0 || i.lapDia < 0)
      return {ok:false, errors:['Edge distance and lap multiplier cannot be negative. Diameter and stock length must be greater than zero.']};
    if (cov < dia/2) return {ok:false, errors:['The bar centreline must be at least half a bar diameter inside the slab.']};
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
    if (Math.max(barLenL,barLenW) > i.stock && lap >= i.stock)
      return {ok:false, errors:['Lap length must be shorter than stock length when bars need to be joined.']};
    function withLaps(barLen, stock) {
      if (barLen <= stock) return {pieces:1, total:barLen};
      var joints = Math.ceil((barLen-stock)/(stock-lap));
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

    return {ok:true, nL:nAlongLen, nW:nAlongWid, totalLen:totalLen, totalM:totalM, weight:weight,
      piecesL:a.pieces, piecesW:b.pieces, stockCount:stockCount,
      L:L, Wd:Wd, cov:cov, spW:actualSpW, spL:actualSpL,
      warnings: warn,
      stats:[
        {value: String(nAlongLen + nAlongWid), label:'Bars in total'},
        {value: WCfmt(totalM,1), label:'Linear metres'},
        {value: WCfmt(weight,1), label:'Weight (kg)'},
        {value: String(intersections), label:'Grid crossings'}
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
        ['Crossings (one grid)', String(intersections)],
        ['Lap length used', WCfmt(lap,0)+'  ('+WCfmt(i.lapDia,0)+' \u00d7 diameter)']
      ]}],
      note:'One two-way grid. Spacing never exceeds the requested maximum. Edge distances are to bar centrelines; stock counts do not reuse offcuts between directions.'
    };
  },
  diagram: function (r, i) {
    var W=620,H=420,m=40,s=SVG.open(W,H);
    var sc=Math.min((W-2*m)/r.L, (H-2*m-30)/r.Wd);
    var x0=m, y0=m+16, sw=r.L*sc, sh=r.Wd*sc;
    s+=SVG.rect(x0,y0,sw,sh,'ghost');
    var strideL=Math.max(1,Math.ceil(r.nL/150)),strideW=Math.max(1,Math.ceil(r.nW/150));
    for(var k=0;k<r.nL;k+=strideL){
      var yy=y0+(r.cov + k*r.spW)*sc;
      s+=SVG.line(x0+r.cov*sc,yy,x0+sw-r.cov*sc,yy,' stroke="var(--accent)" stroke-width="1.6"');
    }
    for(var k=0;k<r.nW;k+=strideW){
      var xx=x0+(r.cov + k*r.spL)*sc;
      s+=SVG.line(xx,y0+r.cov*sc,xx,y0+sh-r.cov*sc,' stroke="var(--accent)" stroke-width="1.6" opacity=".72"');
    }
    s+=SVG.text(W/2, 20, r.nL+' + '+r.nW+' bars  \u00b7  '+WCfmt(r.totalM,1)+' m  \u00b7  '+WCfmt(r.weight,0)+' kg', 13);
    s+=SVG.text(W/2, H-10, WCfmt(r.L,0)+' \u00d7 '+WCfmt(r.Wd,0)+'  \u00b7  edge to centre '+WCfmt(r.cov,0)+(strideL>1||strideW>1?' (grid simplified)':''), 12);
    return s+SVG.close();
  }
};
"""}
