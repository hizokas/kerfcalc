SPEC = {
"slug":"firewood-cord-calculator",
"h1":"Firewood Cord Calculator",
"title_tag":"Firewood Calculator — Cords, Face Cords and Price per Cord From a Stack",
"description":"Measure a stack and get full cords, face cords, cubic metres and the real price per cord, so you can compare loads that are quoted in different units.",
"card_desc":"Cords, face cords and the real price per cord from any stack, so you can compare quotes.",
"category":"Finishing",
"intro":"Firewood gets sold by the cord, the face cord, the load, the cubic metre and the truckful, which makes comparing two prices nearly impossible. Measure the stack, get every unit at once, and see what you are really paying per cord.",
"notes":[("What a cord actually is","A full cord is 128 cubic feet of stacked wood \u2014 about 3.62 cubic metres. It is a volume of stack, not of solid wood: the air between the pieces counts."),
("Face cord is not a real unit","A face cord is one stack 8 feet long and 4 feet high, but only as deep as the pieces are long. Sold as 16 inch pieces that is a third of a cord; as 24 inch pieces it is half. Two sellers quoting face cords can be selling wildly different amounts."),
("Stack it properly before measuring","A loosely thrown pile measures far bigger than the same wood stacked. Measure the stack, not the heap, or you will pay for air."),
("What this does not do","It measures volume, not energy. A cord of oak holds roughly twice the heat of a cord of poplar, and seasoning matters as much as species. Volume alone never tells you what a load is worth.")],
"js":"""
var SPEC = {
  fields: [
    {id:'len', label:'Length of the stack', value:2400, unit:'length', group:'Stack', min:0},
    {id:'hgt', label:'Height of the stack', value:1200, unit:'length', group:'Stack', min:0},
    {id:'piece', label:'Length of the pieces', value:400, unit:'length', group:'Stack', min:0,
     hint:'This is the depth of the stack'},
    {id:'rows', label:'Number of rows deep', value:1, group:'Stack', min:1, step:1},
    {id:'price', label:'Price paid for this stack', value:0, group:'Price', min:0,
     hint:'Leave 0 to skip the price working'}
  ],
  compute: function (i) {
    var k = i.unit === 'in' ? 0.0254 : 0.001;
    var L = i.len*k, Hh = i.hgt*k, p = i.piece*k;
    var rows = Math.max(1, Math.round(i.rows));
    if (!(L > 0 && Hh > 0 && p > 0))
      return {ok:false, errors:['Stack length, height and piece length must all be greater than zero.']};

    var depth = p*rows;
    var m3 = L*Hh*depth;
    var CORD_M3 = 3.624556;          // 128 pieds cubes
    var cords = m3/CORD_M3;
    var ft3 = m3*35.3147;
    // Corde apparente : 8 pi x 4 pi de facade, profondeur = longueur des buches
    var faceArea = L*Hh;             // m2 de facade
    var FACE_M2 = 2.4384*1.2192;     // 8 pi x 4 pi
    var faceCords = faceArea/FACE_M2;
    var fractionOfCord = depth/1.2192;   // profondeur / 4 pieds

    var pricePerCord = i.price > 0 && cords > 0 ? i.price/cords : null;
    var pricePerM3   = i.price > 0 && m3 > 0 ? i.price/m3 : null;

    var warn = [];
    if (p > 0.65) warn.push('Pieces over 650 mm are longer than most stoves take \u2014 worth checking your firebox.');
    if (cords < 0.1) warn.push('This stack is under a tenth of a cord. Fine, but sellers rarely quote at this size.');

    var stats = [
      {value: WCfmt(cords,3), label:'Full cords'},
      {value: WCfmt(m3,2), label:'Cubic metres'},
      {value: WCfmt(faceCords,2), label:'Face cords'},
      {value: WCfmt(ft3,0), label:'Cubic feet'}
    ];
    if (pricePerCord !== null) stats.push({value:WCfmt(pricePerCord,0), label:'Price per cord'});

    return {ok:true, m3:m3, cords:cords, faceCords:faceCords, L:L, Hh:Hh, depth:depth,
      warnings: warn, stats: stats,
      tables:[{title:'Working', head:['Item','Value'], rows:[
        ['Stack face', WCfmt(L,2)+' m long \u00d7 '+WCfmt(Hh,2)+' m high'],
        ['Depth', WCfmt(depth,2)+' m ('+String(rows)+' row(s) of '+WCfmt(p,2)+' m pieces)'],
        ['Stacked volume', WCfmt(m3,3)+' m3 / '+WCfmt(ft3,1)+' ft3'],
        ['Full cords', WCfmt(cords,4)+'  (1 cord = 128 ft3 = 3.6246 m3)'],
        ['Face cords', WCfmt(faceCords,3)+'  (8 ft \u00d7 4 ft face)'],
        ['This depth as a fraction of a cord', WCfmt(fractionOfCord,3)],
        ['Price per cord', pricePerCord !== null ? WCfmt(pricePerCord,2) : '\u2014'],
        ['Price per m3', pricePerM3 !== null ? WCfmt(pricePerM3,2) : '\u2014']
      ]}],
      note:'A cord is a volume of stacked wood, air gaps included. Always compare sellers on full cords or cubic metres \u2014 face cords mean nothing without the piece length.'
    };
  },
  diagram: function (r, i) {
    var W=560,H=250,m=55,s=SVG.open(W,H);
    var sc=Math.min((W-2*m)/Math.max(r.L,0.1), (H-110)/Math.max(r.Hh,0.1));
    var bw=r.L*sc, bh=r.Hh*sc, x=m, y=H-70-bh, dep=Math.min(r.depth*sc, 34);
    s+=SVG.poly([[x,y],[x+dep,y-dep],[x+bw+dep,y-dep],[x+bw,y]],'part');
    s+=SVG.poly([[x+bw,y],[x+bw+dep,y-dep],[x+bw+dep,y+bh-dep],[x+bw,y+bh]],'part');
    s+=SVG.rect(x,y,bw,bh,'part');
    var cols=Math.max(1,Math.round(bw/22));
    for(var q=1;q<cols;q++) s+=SVG.line(x+bw*q/cols,y,x+bw*q/cols,y+bh,' class="dim"');
    s+=SVG.text(x+bw/2, y+bh/2+4, WCfmt(r.cords,2)+' cords', 15);
    s+=SVG.text(x+bw/2, H-40, WCfmt(r.L,2)+' m \u00d7 '+WCfmt(r.Hh,2)+' m \u00d7 '+WCfmt(r.depth,2)+' m deep', 12);
    s+=SVG.text(W/2, 26, WCfmt(r.m3,2)+' m3 stacked  \u00b7  '+WCfmt(r.faceCords,2)+' face cords', 12);
    return s+SVG.close();
  }
};
"""}
