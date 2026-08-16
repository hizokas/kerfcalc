SPEC = {
"slug":"arc-layout-calculator",
"h1":"Arc &amp; Curve Layout Calculator",
"title_tag":"Arc Calculator — Radius from Chord and Rise, With Marking Ordinates",
"description":"Work out the radius, arc length and trammel point of a curve from its width and height, and get the offsets to mark it out full size without a compass.",
"card_desc":"Radius, arc length and a table of offsets to mark any curve full size, no compass needed.",
"category":"Joinery",
"intro":"You know the opening is 1200 wide and you want the curve to rise 200 in the middle. This gives you the radius, where to put the trammel point, and \u2014 if the radius is too big for a compass \u2014 a table of offsets to plot the curve point by point.",
"notes":[("Where the formula comes from","With chord C and rise H, the radius is (C squared divided by 8H) plus H over 2. It falls out of the intersecting chords theorem, and it is exact, not an approximation."),
("When the radius is bigger than your shop","A 1200 opening rising 100 needs a radius of 1850 \u2014 fine. Rising 20 needs 9010, and no trammel reaches that. That is what the offsets table is for: measure along the chord, mark the offset up from it, and bend a batten through the points."),
("Marking with a batten","Drive a nail at each plotted point, spring a thin strip of straight-grained stock against them, and pencil along it. A batten naturally takes a fair curve, which is more forgiving to the eye than a slightly wrong true arc."),
("What this does not do","It handles circular arcs only. Ellipses, ogees and free curves are a different problem, and a batten sprung through three points is usually the better answer for those anyway.")],
"js":"""
var SPEC = {
  fields: [
    {id:'chord', label:'Width of the opening (chord)', value:1200, unit:'length', group:'Curve', min:0},
    {id:'rise', label:'Rise at the centre', value:200, unit:'length', group:'Curve', min:0},
    {id:'points', label:'Number of marking points', value:9, group:'Marking out', min:3, step:2,
     hint:'Odd numbers put one point at the centre'}
  ],
  compute: function (i) {
    var C = i.chord, Hh = i.rise;
    if (!(C > 0)) return {ok:false, errors:['The chord (width) must be greater than zero.']};
    if (!(Hh > 0)) return {ok:false, errors:['The rise must be greater than zero \u2014 with no rise there is no curve.']};
    if (Hh > C/2) return {ok:false, errors:['A rise larger than half the chord is more than a half circle. Check the numbers.']};

    var R = (C*C)/(8*Hh) + Hh/2;
    var halfAngle = Math.asin((C/2)/R);
    var theta = 2*halfAngle;
    var arc = R*theta;
    var centreBelow = R - Hh;        // profondeur du point de compas sous la corde

    var n = Math.max(3, Math.round(i.points));
    var rows = [];
    for (var k = 0; k < n; k++) {
      var x = -C/2 + C*k/(n-1);
      var y = Math.sqrt(Math.max(0, R*R - x*x)) - centreBelow;
      rows.push([WCfmt(C/2 + x,1), WCfmt(y,2)]);
    }

    var warn = [];
    if (R > 3000) warn.push('Radius is '+WCfmt(R,0)+' \u2014 too big for most trammels. Use the offsets table and a sprung batten.');

    return {ok:true, R:R, arc:arc, theta:theta*180/Math.PI, centreBelow:centreBelow, C:C, rise:Hh,
      warnings: warn,
      stats:[
        {value: WCfmt(R,1), label:'Radius'},
        {value: WCfmt(arc,1), label:'Arc length'},
        {value: WCfmt(theta*180/Math.PI,2)+String.fromCharCode(176), label:'Included angle'},
        {value: WCfmt(centreBelow,1), label:'Centre below chord'}
      ],
      tables:[
        {title:'Setting out', head:['Item','Value'], rows:[
          ['Chord (width)', WCfmt(C,1)],
          ['Rise at centre', WCfmt(Hh,1)],
          ['Radius', WCfmt(R,2)],
          ['Trammel point', WCfmt(centreBelow,2)+' below the chord, on the centreline'],
          ['Arc length', WCfmt(arc,2)],
          ['Included angle', WCfmt(theta*180/Math.PI,3)+String.fromCharCode(176)],
          ['Material length for the blank', WCfmt(C,1)+' x '+WCfmt(Hh,1)+' minimum']
        ]},
        {title:'Offsets from the chord', head:['Along the chord','Offset up'], rows: rows}
      ],
      note:'Measure along the chord from the left end, mark the offset square up from it. Spring a batten through the marks and pencil the curve.'
    };
  },
  diagram: function (r, i) {
    var W=640,H=300,m=50,s=SVG.open(W,H);
    var sc=(W-2*m)/r.C, base=H-70;
    var riseP=r.rise*sc, cW=r.C*sc, x0=m, x1=m+cW;
    var Rp=r.R*sc, cyP=base+ (r.centreBelow*sc);
    s+='<path d="M '+x0+' '+base+' A '+Rp+' '+Rp+' 0 0 1 '+x1+' '+base+'" fill="none" stroke="var(--accent)" stroke-width="2.5"/>';
    s+=SVG.line(x0,base,x1,base,' class="dim"');
    s+=SVG.line(W/2,base,W/2,base-riseP,' class="dim"');
    if (cyP < H+400) s+=SVG.line(W/2,base,W/2,Math.min(cyP,H-6),' class="dim" stroke-dasharray="5 5"');
    s+=SVG.text(W/2, base+22, 'chord '+WCfmt(r.C,0), 12);
    s+=SVG.text(W/2-8, base-riseP-10, 'rise '+WCfmt(r.rise,0), 12);
    s+=SVG.text(W/2, 26, 'radius '+WCfmt(r.R,1), 13);
    s+=SVG.text(W/2, H-14, 'arc '+WCfmt(r.arc,1)+'  \u00b7  trammel point '+WCfmt(r.centreBelow,0)+' below the chord', 12);
    return s+SVG.close();
  }
};
"""}
