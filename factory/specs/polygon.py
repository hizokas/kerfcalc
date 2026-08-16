SPEC = {
"slug":"polygon-miter-calculator",
"h1":"Polygon Miter Angle Calculator",
"title_tag":"Polygon Miter Calculator — Angles and Side Lengths for Any Number of Sides",
"description":"Miter angle, side length and material needed for hexagons, octagons and any polygon. Works from across-flats, across-corners or side length.",
"card_desc":"Miter angles and side lengths for hexagons, octagons and any polygon, from any known dimension.",
"category":"Joinery",
"intro":"Planters, tabletops, mirror frames, segmented turnings \u2014 anything with more than four sides. Give the number of sides and one dimension, and this gives you the miter angle, every side length, and how much stock to buy.",
"notes":[("Why the miter is 180 divided by the sides","The angles of a closed polygon have to add up. With N sides you have N joints, each made of two mitered ends, so each cut is 180/N degrees. An octagon is 22.5, a hexagon is 30, a square is 45."),
("Across flats or across corners?","Across flats is wall to opposite wall \u2014 what fits in a space. Across corners is point to opposite point \u2014 what the piece measures at its widest. They are different numbers and mixing them up is the classic error."),
("Why it never closes perfectly","Half a degree of error per cut, doubled per joint, multiplied by eight joints, is four degrees of gap. Cut one test set in scrap, dry-assemble the whole ring, and adjust before touching good stock."),
("What this does not do","It assumes flat, untilted sides. Staved or tapered work \u2014 buckets, splayed planters \u2014 needs compound angles, which is a different calculation.")],
"js":"""
var SPEC = {
  fields: [
    {id:'sides', label:'Number of sides', value:8, group:'Shape', min:3, step:1},
    {id:'known', label:'Dimension you know', type:'select', value:'flats', group:'Shape', options:[
      {value:'flats', label:'Across flats (wall to wall)'},
      {value:'corners', label:'Across corners (point to point)'},
      {value:'side', label:'Length of one side'}]},
    {id:'dim', label:'That dimension', value:600, unit:'length', group:'Shape', min:0},
    {id:'stock', label:'Stock length available', value:2400, unit:'length', group:'Materials', min:0},
    {id:'kerf', label:'Saw kerf', value:3, unit:'length', group:'Materials', min:0}
  ],
  compute: function (i) {
    var n = Math.round(i.sides);
    if (!(n >= 3)) return {ok:false, errors:['A polygon needs at least 3 sides.']};
    if (!(i.dim > 0)) return {ok:false, errors:['The dimension must be greater than zero.']};

    var pi = Math.PI, r2d = 180/pi;
    var miter = 180/n;                 // angle de coupe sur chaque about
    var interior = 180 - 360/n;        // angle interieur du polygone
    var R, side, apothem;

    if (i.known === 'side')      { side = i.dim;  R = side/(2*Math.sin(pi/n)); }
    else if (i.known === 'corners') { R = i.dim/2; side = 2*R*Math.sin(pi/n); }
    else                         { apothem = i.dim/2; R = apothem/Math.cos(pi/n); side = 2*R*Math.sin(pi/n); }
    apothem = R*Math.cos(pi/n);

    var perimeter = side*n;
    var area = 0.5*perimeter*apothem;
    var withKerf = perimeter + n*Math.max(0,i.kerf);
    var sticks = i.stock > 0 ? Math.ceil(withKerf/i.stock) : null;
    var perStick = i.stock > 0 ? Math.floor(i.stock/(side + Math.max(0,i.kerf))) : null;

    var warn = [];
    if (n > 24) warn.push('Above about 24 sides the miter drops under 4 degrees, which is very hard to cut accurately on a mitre saw.');

    return {ok:true, n:n, side:side, R:R, apothem:apothem, miter:miter, perimeter:perimeter,
      warnings: warn,
      stats:[
        {value: WCfmt(miter,2)+String.fromCharCode(176), label:'Miter each end'},
        {value: WCfmt(side,1), label:'Length of each side'},
        {value: String(n), label:'Pieces to cut'},
        {value: sticks !== null ? String(sticks) : '\u2014', label:'Stock lengths'}
      ],
      tables:[{title:'Full dimensions', head:['Item','Value'], rows:[
        ['Sides', String(n)],
        ['Miter angle, each end', WCfmt(miter,3)+String.fromCharCode(176)+'  (180 / '+n+')'],
        ['Angle at each joint', WCfmt(interior,3)+String.fromCharCode(176)],
        ['Length of one side', WCfmt(side,2)],
        ['Across flats', WCfmt(apothem*2,2)],
        ['Across corners', WCfmt(R*2,2)],
        ['Perimeter', WCfmt(perimeter,1)],
        ['Area', WCfmt(area/1e6,3)+' m2 (if working in mm)'],
        ['Material incl. kerf', WCfmt(withKerf,1)],
        ['Pieces per stock length', perStick !== null ? String(perStick) : '\u2014']
      ]}],
      note:'Side lengths are long-point to long-point on the outside face. Cut one test set in scrap and dry-fit the whole ring before cutting good material.'
    };
  },
  diagram: function (r, i) {
    var W=560,H=380,cx=W/2,cy=190,rad=140,s=SVG.open(W,H);
    var pts=[], n=r.n;
    for (var k=0;k<n;k++){
      var a = -Math.PI/2 + (2*Math.PI*k/n) + Math.PI/n;
      pts.push([cx+rad*Math.cos(a), cy+rad*Math.sin(a)]);
    }
    s += SVG.poly(pts,'part');
    for (var k=0;k<n;k++){
      var p1=pts[k], p2=pts[(k+1)%n];
      if (n<=12) s += SVG.text((p1[0]+p2[0])/2 + (p1[0]+p2[0])/2*0.02, (p1[1]+p2[1])/2, WCfmt(r.side,0), 12);
    }
    s += SVG.text(cx, cy-6, r.n+' sides', 15);
    s += SVG.text(cx, cy+16, 'miter '+WCfmt(r.miter,2)+String.fromCharCode(176), 14);
    s += SVG.text(cx, H-16, 'across flats '+WCfmt(r.apothem*2,0)+'  \u00b7  across corners '+WCfmt(r.R*2,0), 12);
    return s+SVG.close();
  }
};
"""}
