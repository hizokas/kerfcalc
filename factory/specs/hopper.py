SPEC = {
"slug":"splayed-side-angle-calculator",
"h1":"Splayed Side &amp; Hopper Angle Calculator",
"title_tag":"Hopper Angle Calculator — Miter and Bevel for Splayed Boxes and Tapered Legs",
"description":"Saw miter and blade bevel for boxes with sloping sides, planters, hoppers and splayed legs, at any splay angle and any number of sides.",
"card_desc":"Miter and bevel for boxes with sloping sides, planters, hoppers and splayed legs.",
"category":"Joinery",
"intro":"Tilt the sides of a box outwards and both saw settings change at once. A four-sided planter with 10 degrees of splay is not cut at 45 degrees \u2014 it needs 44.4 miter and 9.85 bevel, and guessing gets you gaps.",
"notes":[("Why both settings change","Once a side leans, the joint line is no longer square to the table, so the miter closes slightly and the blade has to tilt. The two effects are linked: more splay means less miter and more bevel."),
("The formulas","With S the splay from vertical and N the number of sides: miter equals atan(cos(S) times tan(180/N)), and bevel equals asin(sin(S) times cos(180/N)). Both are shown in the results so you can check them."),
("Measuring splay","Splay is measured from vertical, not from the table. A side leaning out by 10 degrees from plumb has a splay of 10. Getting this backwards gives you a box that tapers the wrong way."),
("What this does not do","It gives the two saw settings. It does not size the pieces \u2014 splayed sides are trapezoids whose top and bottom widths depend on the height, and that is a separate layout.")],
"js":"""
var SPEC = {
  fields: [
    {id:'sides', label:'Number of sides', value:4, group:'Box', min:3, step:1},
    {id:'splay', label:'Splay from vertical (degrees)', value:10, group:'Box', min:0,
     hint:'0 gives an ordinary square box'},
    {id:'height', label:'Height of the sides', value:200, unit:'length', group:'Sizes', min:0},
    {id:'bottomW', label:'Width at the bottom', value:300, unit:'length', group:'Sizes', min:0}
  ],
  compute: function (i) {
    var n=Math.round(i.sides), S=i.splay;
    if (!(n>=3)) return {ok:false, errors:['A box needs at least 3 sides.']};
    if (!(S>=0 && S<90)) return {ok:false, errors:['Splay must be between 0 and 90 degrees.']};

    var d2r=Math.PI/180, r2d=180/Math.PI;
    var half=(180/n)*d2r, Sr=S*d2r;
    var miter=Math.atan(Math.cos(Sr)*Math.tan(half))*r2d;
    var bevel=Math.asin(Math.sin(Sr)*Math.cos(half))*r2d;

    var lean = i.height*Math.tan(Sr);
    var topW = i.bottomW + 2*lean;
    var sideLen = i.height/Math.cos(Sr);

    var warn=[];
    if (S > 30) warn.push('Above 30 degrees of splay the bevel gets extreme and many saws cannot reach it. Check the machine before cutting.');

    return {ok:true, n:n, S:S, miter:miter, bevel:bevel, topW:topW, sideLen:sideLen, bottomW:i.bottomW,
      warnings: warn,
      stats:[
        {value: WCfmt(miter,3)+String.fromCharCode(176), label:'Miter angle'},
        {value: WCfmt(bevel,3)+String.fromCharCode(176), label:'Blade bevel'},
        {value: WCfmt(S,1)+String.fromCharCode(176), label:'Splay'},
        {value: String(n), label:'Sides'}
      ],
      tables:[{title:'Saw settings and sizes', head:['Item','Value','Where it comes from'], rows:[
        ['Miter', WCfmt(miter,4)+String.fromCharCode(176), 'atan(cos('+WCfmt(S,1)+') \u00d7 tan('+WCfmt(180/n,2)+'))'],
        ['Bevel', WCfmt(bevel,4)+String.fromCharCode(176), 'asin(sin('+WCfmt(S,1)+') \u00d7 cos('+WCfmt(180/n,2)+'))'],
        ['Miter if the box were upright', WCfmt(180/n,3)+String.fromCharCode(176), '180 / '+n],
        ['Width at the bottom', WCfmt(i.bottomW,1), 'given'],
        ['Width at the top', WCfmt(topW,2), 'bottom + 2 \u00d7 height \u00d7 tan(splay)'],
        ['Height', WCfmt(i.height,1), 'given'],
        ['Length along the sloping side', WCfmt(sideLen,2), 'height / cos(splay)'],
        ['Lean per side', WCfmt(lean,2), 'height \u00d7 tan(splay)']
      ]}],
      note:'Cut a test corner in scrap and offer up two pieces before touching good stock. The numbers are right; the orientation on the saw is what catches people out.'
    };
  },
  diagram: function (r, i) {
    var W=560,H=300,s=SVG.open(W,H);
    var sc=Math.min(320/Math.max(r.topW,1), 150/Math.max(i.height,1));
    var cx=W/2, base=H-80, hh=i.height*sc, bw=r.bottomW*sc, tw=r.topW*sc;
    s+=SVG.poly([[cx-bw/2,base],[cx+bw/2,base],[cx+tw/2,base-hh],[cx-tw/2,base-hh]],'part');
    s+=SVG.line(cx-tw/2,base-hh-16,cx-tw/2,base+16,' class="dim" stroke-dasharray="4 4"');
    s+=SVG.line(cx-bw/2,base,cx-bw/2,base-hh-16,' class="dim" stroke-dasharray="4 4"');
    s+=SVG.text(cx,base+24,'bottom '+WCfmt(r.bottomW,0),12);
    s+=SVG.text(cx,base-hh-14,'top '+WCfmt(r.topW,0),12);
    s+=SVG.text(cx,30,'miter '+WCfmt(r.miter,2)+String.fromCharCode(176)+'   bevel '+WCfmt(r.bevel,2)+String.fromCharCode(176),15);
    s+=SVG.text(cx,H-14,r.n+' sides at '+WCfmt(r.S,1)+String.fromCharCode(176)+' of splay',12);
    return s+SVG.close();
  }
};
"""}
