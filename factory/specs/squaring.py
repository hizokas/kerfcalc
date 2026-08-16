SPEC = {
"slug":"squaring-diagonal-calculator",
"h1":"Squaring &amp; Diagonal Calculator",
"title_tag":"Squaring Calculator — Diagonal Check, 3-4-5 Method and Out-of-Square",
"description":"Check whether a frame, slab or opening is square by comparing diagonals, see how far out it is, and get 3-4-5 triangle numbers scaled to your job.",
"card_desc":"Diagonal check, how far out of square you are, and 3-4-5 numbers scaled to your job.",
"category":"Framing",
"intro":"Two diagonals that differ by 8 mm on a 3 metre frame means the corner is off by about a degree \u2014 enough to see. Enter your sides, get the diagonal it should measure, and if you have measured both, exactly how far out you are and which way.",
"notes":[("Why diagonals prove square","A rectangle is the only quadrilateral with equal sides and equal diagonals. Sides alone do not prove it: a parallelogram can have four correct sides and still lean. Equal diagonals are the proof."),
("How to correct it","Push the corner at the end of the longer diagonal towards the shorter one. Half the difference is roughly how far the corner moves \u2014 so an 8 mm difference means nudging about 4 mm."),
("The 3-4-5 method","Any triangle with sides in the ratio 3:4:5 has a right angle. It works at any scale, and bigger is more accurate \u2014 measuring 300:400:500 is far more forgiving than 30:40:50."),
("What this does not do","It checks a rectangle in one plane. Winding \u2014 a frame twisted out of flat \u2014 is a separate problem and needs winding sticks, not a tape.")],
"js":"""
var SPEC = {
  fields: [
    {id:'a', label:'Side A', value:3000, unit:'length', group:'Frame', min:0},
    {id:'b', label:'Side B', value:2000, unit:'length', group:'Frame', min:0},
    {id:'d1', label:'Measured diagonal 1', value:0, unit:'length', group:'Check', min:0,
     hint:'Leave 0 if you have not measured yet'},
    {id:'d2', label:'Measured diagonal 2', value:0, unit:'length', group:'Check', min:0},
    {id:'mult', label:'3-4-5 scale', value:100, group:'3-4-5', min:1,
     hint:'100 gives 300 : 400 : 500'}
  ],
  compute: function (i) {
    var a=i.a, b=i.b;
    if (!(a>0 && b>0)) return {ok:false, errors:['Both sides must be greater than zero.']};

    var target = Math.sqrt(a*a + b*b);
    var rows = [
      ['Side A', WCfmt(a,1)],
      ['Side B', WCfmt(b,1)],
      ['Diagonal when square', WCfmt(target,2)],
      ['3-4-5 triangle', WCfmt(3*i.mult,0)+' : '+WCfmt(4*i.mult,0)+' : '+WCfmt(5*i.mult,0)]
    ];

    var diff=null, err=null, angle=null, warn=[];
    if (i.d1>0 && i.d2>0) {
      diff = Math.abs(i.d1-i.d2);
      err = diff/2;
      // Ecart angulaire approche : la difference de diagonales sur un rectangle
      var mean=(i.d1+i.d2)/2;
      angle = Math.asin(Math.min(1, diff/(2*Math.max(a,b))))*180/Math.PI;
      rows.push(['Diagonal 1 measured', WCfmt(i.d1,1)]);
      rows.push(['Diagonal 2 measured', WCfmt(i.d2,1)]);
      rows.push(['Difference', WCfmt(diff,2)]);
      rows.push(['Move the corner about', WCfmt(err,2)]);
      rows.push(['Out of square by roughly', WCfmt(angle,3)+String.fromCharCode(176)]);
      if (diff < 1) warn.push('Under 1 of difference \u2014 that is square for any practical purpose.');
      else warn.push('Push the corner at the end of the LONGER diagonal ('+(i.d1>i.d2?'diagonal 1':'diagonal 2')+') towards the shorter one, about '+WCfmt(err,1)+'.');
    }

    var stats = [
      {value: WCfmt(target,1), label:'Diagonal when square'},
      {value: WCfmt(3*i.mult,0)+':'+WCfmt(4*i.mult,0)+':'+WCfmt(5*i.mult,0), label:'3-4-5 numbers'}
    ];
    if (diff !== null) {
      stats.push({value: WCfmt(diff,1), label:'Difference measured'});
      stats.push({value: WCfmt(angle,2)+String.fromCharCode(176), label:'Out of square'});
    }

    return {ok:true, a:a, b:b, target:target, diff:diff, warnings:warn, stats:stats,
      tables:[{title:'Working', head:['Item','Value'], rows:rows}],
      note:'Measure both diagonals from the same reference points, corner to corner. If they match, it is square.'
    };
  },
  diagram: function (r, i) {
    var W=560,H=330,m=60,s=SVG.open(W,H);
    var sc=Math.min((W-2*m)/r.a,(H-110)/r.b);
    var x=m,y=60,bw=r.a*sc,bh=r.b*sc;
    s+=SVG.rect(x,y,bw,bh,'part');
    s+=SVG.line(x,y,x+bw,y+bh,' class="dim" stroke-dasharray="6 5"');
    s+=SVG.line(x+bw,y,x,y+bh,' class="dim" stroke-dasharray="6 5"');
    s+=SVG.text(x+bw/2,y-12,'A '+WCfmt(r.a,0),12);
    s+=SVG.text(x-26,y+bh/2,'B',12);
    s+=SVG.text(x+bw/2,y+bh/2-6,'diagonal',11);
    s+=SVG.text(x+bw/2,y+bh/2+14,WCfmt(r.target,1),13);
    s+=SVG.text(W/2,H-16, r.diff!==null ? 'measured difference '+WCfmt(r.diff,1) : 'both diagonals must match', 12);
    return s+SVG.close();
  }
};
"""}
