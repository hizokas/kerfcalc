SPEC = {
"slug":"sheet-metal-bend-calculator",
"h1":"Sheet Metal Bend Allowance Calculator",
"title_tag":"Bend Allowance Calculator — Flat Pattern Length, Setback and Bend Deduction",
"description":"Bend allowance, bend deduction, setback and the total flat blank length for any material thickness, bend radius, angle and K-factor.",
"card_desc":"Flat pattern length, bend allowance and deduction from thickness, radius, angle and K-factor.",
"category":"Sheet goods",
"intro":"Metal stretches on the outside of a bend and compresses on the inside, so the flat blank is never the sum of the finished legs. Enter your thickness, radius, angle and K-factor and get the blank length to cut.",
"notes":[("What the K-factor is","Somewhere inside the bend there is a layer that neither stretches nor compresses \u2014 the neutral axis. The K-factor says where it sits, as a fraction of the thickness from the inside face. Around 0.33 for tight bends and soft material, up to about 0.5 for large radii; the reliable figure is the one you measure on your own press."),
("Allowance, deduction, setback","Bend allowance is the length of material inside the bend itself. Bend deduction is how much shorter the blank is than the two outside legs added together. Setback is the distance from the bend line to the outside corner. Different shops work from different ones \u2014 all three are given."),
("Why your first part is always wrong","Published K-factors are starting points. Bend one test piece, measure the finished legs, and back-calculate your real K-factor. Then it is right forever on that machine and that material."),
("What this does not do","It does not predict springback, cracking on tight radii, or the minimum radius your material tolerates. Those depend on alloy, temper and grain direction.")],
"js":"""
var SPEC = {
  fields: [
    {id:'t', label:'Material thickness', value:2, unit:'length', group:'Material', min:0},
    {id:'r', label:'Inside bend radius', value:3, unit:'length', group:'Material', min:0},
    {id:'k', label:'K-factor', value:0.42, group:'Material', min:0.01,
     hint:'0.33 tight, 0.42 typical, up to 0.5'},
    {id:'angle', label:'Bend angle (degrees)', value:90, group:'Bend', min:0.1,
     hint:'The angle turned through, not the included angle'},
    {id:'legA', label:'Finished leg A', value:50, unit:'length', group:'Bend', min:0},
    {id:'legB', label:'Finished leg B', value:50, unit:'length', group:'Bend', min:0},
    {id:'bends', label:'Number of identical bends', value:1, group:'Bend', min:1, step:1}
  ],
  compute: function (i) {
    var t=i.t, R=i.r, K=i.k, A=i.angle;
    if (!(t>0)) return {ok:false, errors:['Thickness must be greater than zero.']};
    if (!(R>=0)) return {ok:false, errors:['Bend radius cannot be negative.']};
    if (!(A>0 && A<180)) return {ok:false, errors:['The bend angle must be between 0 and 180 degrees.']};
    if (!(K>0 && K<=0.5)) return {ok:false, errors:['The K-factor must be between 0 and 0.5.']};

    var rad = A*Math.PI/180;
    var BA = rad*(R + K*t);                       // developpe de la zone pliee
    var setback = (R + t)*Math.tan(rad/2);        // du trait de pliage au coin exterieur
    var OSSB = setback;
    var BD = 2*OSSB - BA;                         // deduction de pliage

    var n = Math.max(1, Math.round(i.bends));
    var flat = i.legA + i.legB - BD;              // longueur du flan pour un pli
    var flatN = (i.legA + i.legB) - n*BD;         // approximation pour n plis identiques

    var warn=[];
    if (R < t) warn.push('The inside radius is smaller than the material thickness. Many alloys crack there \u2014 check what yours tolerates.');
    if (flat <= 0) warn.push('The legs are too short for this bend \u2014 the deduction is bigger than the part.');

    return {ok:true, BA:BA, BD:BD, setback:setback, flat:flat, t:t, R:R, A:A, legA:i.legA, legB:i.legB,
      warnings: warn,
      stats:[
        {value: WCfmt(flat,2), label:'Flat blank length'},
        {value: WCfmt(BA,3), label:'Bend allowance'},
        {value: WCfmt(BD,3), label:'Bend deduction'},
        {value: WCfmt(setback,3), label:'Setback'}
      ],
      tables:[{title:'Working', head:['Item','Value','Formula'], rows:[
        ['Thickness', WCfmt(t,2), 'given'],
        ['Inside radius', WCfmt(R,2), 'given'],
        ['K-factor', WCfmt(K,3), 'given'],
        ['Bend angle', WCfmt(A,2)+String.fromCharCode(176), 'given'],
        ['Bend allowance', WCfmt(BA,4), 'angle(rad) \u00d7 (R + K \u00d7 t)'],
        ['Setback / OSSB', WCfmt(setback,4), '(R + t) \u00d7 tan(angle / 2)'],
        ['Bend deduction', WCfmt(BD,4), '2 \u00d7 setback \u2212 bend allowance'],
        ['Flat blank, one bend', WCfmt(flat,3), 'leg A + leg B \u2212 deduction'],
        ['Flat blank, '+n+' bends', WCfmt(flatN,3), 'legs \u2212 '+n+' \u00d7 deduction']
      ]}],
      note:'Bend one test piece and measure it. Adjust the K-factor until the calculated blank matches reality on your machine, then it is right for good.'
    };
  },
  diagram: function (r, i) {
    var W=560,H=280,s=SVG.open(W,H);
    var cx=200, cy=170, L=140;
    var a=r.A*Math.PI/180;
    var x2=cx+L*Math.cos(-a), y2=cy+L*Math.sin(-a);
    s+=SVG.line(cx,cy,cx+L,cy,' stroke-width="6"');
    s+=SVG.line(cx,cy,x2,y2,' stroke-width="6"');
    s+='<path d="M '+(cx+46)+' '+cy+' A 46 46 0 0 0 '+(cx+46*Math.cos(-a))+' '+(cy+46*Math.sin(-a))+'" fill="none" stroke="var(--muted)" stroke-width="1.2"/>';
    s+=SVG.text(cx+72,cy-14,WCfmt(r.A,1)+String.fromCharCode(176),13);
    s+=SVG.text(cx+L/2,cy+22,'leg '+WCfmt(r.legA,0),11);
    s+=SVG.text(W/2,30,'flat blank '+WCfmt(r.flat,2),14);
    s+=SVG.text(W/2,H-16,'t '+WCfmt(r.t,1)+'  \u00b7  R '+WCfmt(r.R,1)+'  \u00b7  allowance '+WCfmt(r.BA,2)+'  \u00b7  deduction '+WCfmt(r.BD,2),11);
    return s+SVG.close();
  }
};
"""}
