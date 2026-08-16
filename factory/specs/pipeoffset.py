SPEC = {
"slug":"pipe-offset-calculator",
"h1":"Pipe Offset Calculator",
"title_tag":"Pipe Offset Calculator — Travel, Run and Rolling Offsets for Any Fitting Angle",
"description":"Travel and run for pipe offsets at 45, 30, 22.5 or any angle, including rolling offsets, with fitting take-off subtracted to give the real cut length.",
"card_desc":"Travel, run and cut length for simple and rolling offsets, with fitting take-off subtracted.",
"category":"Framing",
"intro":"Two fittings, one obstruction, and a piece of pipe that has to land exactly. Give the offset and the fitting angle and this returns the travel, the run, and the length to actually cut once the take-off of both fittings is removed.",
"notes":[("Travel, run and offset","Offset is how far the line shifts sideways. Travel is the length of the sloping pipe, centre to centre. Run is how far along the original direction you consume doing it. Travel equals offset divided by the sine of the angle \u2014 for 45 degrees that is offset times 1.414."),
("Why the take-off matters","Travel is centre to centre of the fittings. The pipe you cut is shorter by the take-off of each fitting \u2014 the distance from the fitting centre to the end of the socket. Forget it and every offset comes out long by an inch or more."),
("Rolling offsets","When the obstruction moves the line both sideways and up, the true offset is the diagonal of those two: the square root of the sum of their squares. The roll angle tells you how far round the vertical the whole offset is rotated."),
("What this does not do","It is pure geometry. It does not size pipe, check fall on drainage, or know which fittings your system allows.")],
"js":"""
var SPEC = {
  fields: [
    {id:'kind', label:'Type of offset', type:'select', value:'simple', group:'Offset', options:[
      {value:'simple', label:'Simple offset (one plane)'},
      {value:'rolling', label:'Rolling offset (two planes)'}]},
    {id:'offset', label:'Offset', value:300, unit:'length', group:'Offset', min:0,
     hint:'Simple offset: the sideways shift'},
    {id:'vert', label:'Vertical shift', value:300, unit:'length', group:'Offset', min:0, hint:'Rolling only'},
    {id:'horiz', label:'Horizontal shift', value:200, unit:'length', group:'Offset', min:0, hint:'Rolling only'},
    {id:'angle', label:'Fitting angle (degrees)', type:'select', value:'45', group:'Fittings', options:[
      {value:'45', label:'45\u00b0'}, {value:'30', label:'30\u00b0'},
      {value:'22.5', label:'22.5\u00b0'}, {value:'60', label:'60\u00b0'},
      {value:'11.25', label:'11.25\u00b0'}]},
    {id:'takeoff', label:'Take-off per fitting', value:25, unit:'length', group:'Fittings', min:0,
     hint:'Centre of fitting to end of socket'}
  ],
  compute: function (i) {
    var A = parseFloat(i.angle);
    if (!(A > 0 && A < 90)) return {ok:false, errors:['The fitting angle must be between 0 and 90 degrees.']};

    var offset, roll = null;
    if (i.kind === 'rolling') {
      if (!(i.vert > 0 || i.horiz > 0))
        return {ok:false, errors:['A rolling offset needs a vertical or horizontal shift greater than zero.']};
      offset = Math.sqrt(i.vert*i.vert + i.horiz*i.horiz);
      roll = Math.atan2(i.horiz, i.vert) * 180/Math.PI;
    } else {
      if (!(i.offset > 0)) return {ok:false, errors:['The offset must be greater than zero.']};
      offset = i.offset;
    }

    var rad = A*Math.PI/180;
    var travel = offset/Math.sin(rad);
    var run = offset/Math.tan(rad);
    var cut = travel - 2*Math.max(0, i.takeoff);

    var warn = [];
    if (cut <= 0) warn.push('The take-off of the two fittings is longer than the travel \u2014 at this offset the fittings meet. Use a shallower angle.');

    return {ok:true, offset:offset, travel:travel, run:run, cut:cut, roll:roll, A:A,
      warnings: warn,
      stats:[
        {value: WCfmt(travel,1), label:'Travel (centre to centre)'},
        {value: WCfmt(cut,1), label:'Cut length'},
        {value: WCfmt(run,1), label:'Run consumed'},
        {value: WCfmt(offset,1), label:'True offset'}
      ],
      tables:[{title:'Working', head:['Item','Value','Where it comes from'], rows:[
        ['Fitting angle', WCfmt(A,2)+String.fromCharCode(176), 'chosen'],
        ['True offset', WCfmt(offset,2), i.kind==='rolling' ? 'sqrt('+WCfmt(i.vert,0)+'\u00b2 + '+WCfmt(i.horiz,0)+'\u00b2)' : 'given'],
        ['Roll angle', roll !== null ? WCfmt(roll,2)+String.fromCharCode(176) : '\u2014', roll !== null ? 'atan(horizontal / vertical)' : 'simple offset'],
        ['Travel', WCfmt(travel,2), 'offset / sin('+WCfmt(A,1)+')'],
        ['Run', WCfmt(run,2), 'offset / tan('+WCfmt(A,1)+')'],
        ['Take-off, both fittings', WCfmt(2*i.takeoff,2), '2 \u00d7 '+WCfmt(i.takeoff,1)],
        ['Length to cut', WCfmt(cut,2), 'travel \u2212 both take-offs']
      ]}],
      note:'Travel is centre to centre of the two fittings. Cut length is what you saw, after removing the take-off at each end. Check the take-off against your actual fittings \u2014 it varies by material and manufacturer.'
    };
  },
  diagram: function (r, i) {
    var W=620,H=280,m=60,s=SVG.open(W,H);
    var sc = Math.min((W-2*m)/(r.run*2 + 40), (H-120)/Math.max(r.offset,1));
    if (!isFinite(sc) || sc<=0) sc = 0.3;
    var y1 = 90, y2 = y1 + r.offset*sc, xa = m, xb = m + 90, xc = xb + r.run*sc, xd = xc + 90;
    s += SVG.line(xa,y1,xb,y1,' stroke-width="4"');
    s += SVG.line(xb,y1,xc,y2,' stroke-width="4"');
    s += SVG.line(xc,y2,xd,y2,' stroke-width="4"');
    s += SVG.line(xb,y1,xb,y2,' class="dim" stroke-dasharray="4 4"');
    s += SVG.line(xb,y2,xc,y2,' class="dim" stroke-dasharray="4 4"');
    s += SVG.text((xb+xc)/2, (y1+y2)/2 - 12, 'travel '+WCfmt(r.travel,0), 13);
    s += SVG.text(xb-32, (y1+y2)/2, 'offset', 11);
    s += SVG.text((xb+xc)/2, y2+20, 'run '+WCfmt(r.run,0), 11);
    s += SVG.text(W/2, 30, WCfmt(r.A,1)+String.fromCharCode(176)+' offset  \u00b7  cut '+WCfmt(r.cut,1), 14);
    s += SVG.text(W/2, H-16, r.roll !== null ? 'rolling \u00b7 roll angle '+WCfmt(r.roll,1)+String.fromCharCode(176) : 'simple offset, one plane', 12);
    return s+SVG.close();
  }
};
"""}
