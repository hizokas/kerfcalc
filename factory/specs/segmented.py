SPEC = {
"slug":"segmented-turning-calculator",
"h1":"Segmented Turning Ring Calculator",
"title_tag":"Segmented Turning Calculator — Segment Angle, Length and Board Feet per Ring",
"description":"Segment angle, blank length, board width and total strip length for each ring of a segmented bowl or vessel, at any diameter and segment count.",
"card_desc":"Segment angles, blank sizes and strip length for each ring of a segmented bowl.",
"category":"Joinery",
"intro":"Every ring in a segmented bowl needs its own segment length, and the miter has to be exact or the ring will not close. Give the diameter and the number of segments and this returns the cut angle, the blank size and how much strip to prepare.",
"notes":[("Why the angle must be exact","With 12 segments each joint has two 15 degree cuts, so 24 cuts have to sum to 360 degrees. A tenth of a degree of error becomes a 2.4 degree gap by the time the ring closes \u2014 visible, and it will not glue up tight."),
("Cut to the outside, size to the inside","The segment length given here is the long side, on the outside of the ring. The short side is what determines whether the ring closes on the inside \u2014 both are given so you can check your blanks before gluing."),
("Ring width and waste","A ring turns down considerably: you lose the corners of every segment when you round it. The blank width here is the flat width before turning, and 15 to 20 percent extra strip is normal."),
("What this does not do","It sizes one ring at a time. Stacking, orientation of the grain and the wall thickness of the finished vessel are design decisions, not calculations.")],
"js":"""
var SPEC = {
  fields: [
    {id:'segs', label:'Segments per ring', value:12, group:'Ring', min:3, step:1},
    {id:'outer', label:'Outside diameter', value:300, unit:'length', group:'Ring', min:0},
    {id:'wallW', label:'Ring width (radial)', value:40, unit:'length', group:'Ring', min:0},
    {id:'thick', label:'Ring thickness', value:25, unit:'length', group:'Ring', min:0},
    {id:'kerf', label:'Saw kerf', value:3, unit:'length', group:'Materials', min:0},
    {id:'extra', label:'Strip waste allowance (%)', value:20, group:'Materials', min:0}
  ],
  compute: function (i) {
    var n=Math.round(i.segs);
    if (!(n>=3)) return {ok:false, errors:['A ring needs at least 3 segments.']};
    if (!(i.outer>0)) return {ok:false, errors:['Outside diameter must be greater than zero.']};
    if (!(i.wallW>0)) return {ok:false, errors:['Ring width must be greater than zero.']};
    if (2*i.wallW >= i.outer) return {ok:false, errors:['The ring width leaves no hole \u2014 that is a solid disc.']};

    var pi=Math.PI;
    var miter = 180/n;                 // angle de coupe sur chaque about
    var Ro = i.outer/2, Ri = Ro - i.wallW;
    var outerLen = 2*Ro*Math.tan(pi/n);   // long point a long point
    var innerLen = 2*Ri*Math.tan(pi/n);
    var stripW = i.wallW;
    var perRing = n*(outerLen + Math.max(0,i.kerf));
    var withWaste = perRing*(1+Math.max(0,i.extra)/100);
    var volume = n*((outerLen+innerLen)/2)*i.wallW*i.thick;

    var warn=[];
    if (miter < 4) warn.push('At '+n+' segments the cut is only '+WCfmt(miter,2)+' degrees. Very hard to hold accurately \u2014 a sled and a stop block are essential.');
    if (innerLen <= 0) warn.push('The inner edge has no length \u2014 reduce the ring width.');

    return {ok:true, n:n, miter:miter, outerLen:outerLen, innerLen:innerLen, perRing:perRing,
      withWaste:withWaste, Ro:Ro, Ri:Ri, stripW:stripW,
      warnings: warn,
      stats:[
        {value: WCfmt(miter,3)+String.fromCharCode(176), label:'Miter each end'},
        {value: WCfmt(outerLen,2), label:'Outside length'},
        {value: String(n), label:'Segments'},
        {value: WCfmt(withWaste,0), label:'Strip to prepare'}
      ],
      tables:[{title:'Ring take-off', head:['Item','Value'], rows:[
        ['Segments', String(n)],
        ['Miter angle, each end', WCfmt(miter,4)+String.fromCharCode(176)+'  (180 / '+n+')'],
        ['Outside diameter', WCfmt(i.outer,1)],
        ['Inside diameter', WCfmt(2*Ri,1)],
        ['Segment length, outside', WCfmt(outerLen,3)],
        ['Segment length, inside', WCfmt(innerLen,3)],
        ['Strip width needed', WCfmt(stripW,1)],
        ['Strip thickness', WCfmt(i.thick,1)],
        ['Strip length incl. kerf', WCfmt(perRing,1)],
        ['With '+WCfmt(i.extra,0)+'% waste', WCfmt(withWaste,1)],
        ['Timber volume in the ring', WCfmt(volume/1e6,4)+' litres (if working in mm)']
      ]}],
      note:'Cut all segments from one setup without touching the fence. Dry-fit the whole ring with a band clamp before glue \u2014 any gap doubles when it closes.'
    };
  },
  diagram: function (r, i) {
    var W=520,H=400,cx=W/2,cy=205,s=SVG.open(W,H);
    var scale=150/Math.max(r.Ro,1), Ro=r.Ro*scale, Ri=r.Ri*scale;
    for (var k=0;k<r.n;k++){
      var a1=-Math.PI/2 + 2*Math.PI*k/r.n, a2=-Math.PI/2 + 2*Math.PI*(k+1)/r.n;
      var p=[[cx+Ro*Math.cos(a1),cy+Ro*Math.sin(a1)],[cx+Ro*Math.cos(a2),cy+Ro*Math.sin(a2)],
             [cx+Ri*Math.cos(a2),cy+Ri*Math.sin(a2)],[cx+Ri*Math.cos(a1),cy+Ri*Math.sin(a1)]];
      s+=SVG.poly(p,'part');
    }
    s+=SVG.text(cx,cy+4, r.n+' segments', 14);
    s+=SVG.text(cx,cy+24, WCfmt(r.miter,2)+String.fromCharCode(176)+' each end', 12);
    s+=SVG.text(cx,26, 'outside '+WCfmt(i.outer,0)+'  \u00b7  segment '+WCfmt(r.outerLen,1), 13);
    s+=SVG.text(cx,H-14, 'prepare '+WCfmt(r.withWaste,0)+' of strip, '+WCfmt(r.stripW,0)+' wide', 12);
    return s+SVG.close();
  }
};
"""}
