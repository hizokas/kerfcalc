SPEC = {
"slug":"bolt-circle-calculator",
"h1":"Bolt Hole Circle Calculator",
"title_tag":"Bolt Circle Calculator — X and Y Coordinates for Any PCD and Hole Count",
"description":"X and Y coordinates for every hole on a bolt circle, chord distance between adjacent holes, and the PCD from a measured chord.",
"card_desc":"X and Y coordinates for every hole on a bolt circle, plus chord spacing and PCD from a measurement.",
"category":"Sheet goods",
"intro":"Marking a bolt circle by stepping a divider round it accumulates error and the last hole never lands right. This gives the exact X and Y of every hole from the centre, so you set out with a rule or a DRO instead.",
"notes":[("Coordinates beat stepping round","Stepping a divider means each hole inherits the error of the one before it. Coordinates are measured from a single origin, so no error accumulates and the last hole closes as well as the first."),
("The chord check","The chord is the straight-line distance between adjacent holes, equal to the PCD times the sine of 180 divided by the number of holes. Measure it on the finished part and you have an independent check on your setting out."),
("Finding an unknown PCD","On an existing flange, measure the chord between two adjacent holes and work backwards: PCD equals the chord divided by the sine of 180 over the hole count. That is more accurate than trying to measure across a circle where the centre is a hole."),
("What this does not do","It positions holes. It says nothing about hole size, edge distance, thread engagement or whether the pattern is strong enough for the load.")],
"js":"""
var SPEC = {
  fields: [
    {id:'mode', label:'What do you know', type:'select', value:'pcd', group:'Circle', options:[
      {value:'pcd', label:'The pitch circle diameter'},
      {value:'chord', label:'The chord between two holes'}]},
    {id:'pcd', label:'Pitch circle diameter', value:100, unit:'length', group:'Circle', min:0},
    {id:'chord', label:'Measured chord', value:38.27, unit:'length', group:'Circle', min:0},
    {id:'holes', label:'Number of holes', value:8, group:'Circle', min:2, step:1},
    {id:'start', label:'Angle of the first hole (degrees)', value:0, group:'Circle', min:0,
     hint:'0 puts the first hole at 3 o clock'}
  ],
  compute: function (i) {
    var n=Math.round(i.holes);
    if (!(n>=2)) return {ok:false, errors:['You need at least 2 holes.']};

    var pcd;
    if (i.mode==='chord') {
      if (!(i.chord>0)) return {ok:false, errors:['The chord must be greater than zero.']};
      pcd = i.chord/Math.sin(Math.PI/n);
    } else {
      if (!(i.pcd>0)) return {ok:false, errors:['The pitch circle diameter must be greater than zero.']};
      pcd = i.pcd;
    }
    var R = pcd/2;
    var step = 360/n;
    var chord = pcd*Math.sin(Math.PI/n);

    var rows=[];
    for (var k=0;k<n;k++){
      var a=(i.start + k*step)*Math.PI/180;
      rows.push([String(k+1), WCfmt((i.start+k*step)%360,3)+String.fromCharCode(176),
                 WCfmt(R*Math.cos(a),4), WCfmt(R*Math.sin(a),4)]);
    }

    return {ok:true, pcd:pcd, R:R, step:step, chord:chord, n:n, start:i.start,
      stats:[
        {value: WCfmt(pcd,3), label:'Pitch circle diameter'},
        {value: WCfmt(step,3)+String.fromCharCode(176), label:'Angle between holes'},
        {value: WCfmt(chord,3), label:'Chord between holes'},
        {value: String(n), label:'Holes'}
      ],
      tables:[
        {title:'Circle', head:['Item','Value','Formula'], rows:[
          ['Pitch circle diameter', WCfmt(pcd,4), i.mode==='chord' ? 'chord / sin(180 / '+n+')' : 'given'],
          ['Radius', WCfmt(R,4), 'PCD / 2'],
          ['Angle between holes', WCfmt(step,4)+String.fromCharCode(176), '360 / '+n],
          ['Chord between holes', WCfmt(chord,4), 'PCD \u00d7 sin(180 / '+n+')']
        ]},
        {title:'Hole coordinates from the centre', head:['Hole','Angle','X','Y'], rows:rows}
      ],
      note:'X and Y are measured from the centre of the circle, X to the right and Y upwards. Set every hole from that one origin.'
    };
  },
  diagram: function (r, i) {
    var W=460,H=460,cx=W/2,cy=H/2,rad=165,s=SVG.open(W,H);
    s+='<circle cx="'+cx+'" cy="'+cy+'" r="'+rad+'" class="ghost" stroke-dasharray="6 5"/>';
    s+=SVG.line(cx-rad-16,cy,cx+rad+16,cy,' class="dim"');
    s+=SVG.line(cx,cy-rad-16,cx,cy+rad+16,' class="dim"');
    for (var k=0;k<r.n;k++){
      var a=(r.start + k*r.step)*Math.PI/180;
      var x=cx+rad*Math.cos(a), y=cy-rad*Math.sin(a);
      s+='<circle cx="'+x+'" cy="'+y+'" r="13" class="part"/>';
      if (r.n<=16) s+=SVG.text(x,y+4,String(k+1),11);
    }
    s+=SVG.text(cx,26,'PCD '+WCfmt(r.pcd,2)+'  \u00b7  '+r.n+' holes',13);
    s+=SVG.text(cx,H-14,'chord '+WCfmt(r.chord,2)+'  \u00b7  '+WCfmt(r.step,2)+String.fromCharCode(176)+' apart',12);
    return s+SVG.close();
  }
};
"""}
