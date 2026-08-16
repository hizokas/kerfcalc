SPEC = {
"slug":"ramp-slope-calculator",
"h1":"Ramp &amp; Slope Calculator",
"title_tag":"Slope Calculator — Convert Between Ratio, Percent, Degrees and Rise per Metre",
"description":"Convert any slope between ratio, percentage, degrees and fall per metre, and work out ramp length, rise or run when you know the other two.",
"card_desc":"Convert slopes between ratio, percent, degrees and fall, and size a ramp from any two knowns.",
"category":"Framing",
"intro":"Every trade writes slope differently \u2014 1:12 for ramps, 2% for drainage, 30 degrees for a roof, 20 mm per metre for a shower tray. Enter what you have, get all of them, plus the ramp length and landing count.",
"notes":[("The four ways of saying the same thing","A 1:12 ratio is 8.33 percent, is 4.76 degrees, is 83.3 mm of fall per metre. They describe the same slope. Ratio is common for ramps, percent for roads and drainage, degrees for roofs, mm per metre for plumbing."),
("Ratio is run over rise, not the reverse","1:12 means twelve along for one up. Writing it upside down turns a gentle ramp into an unusable one, and it happens more often than you would think."),
("Landings","Long ramps normally need level landings at intervals, and the maximum run between them varies by country and by use. Set the interval yourself from whatever applies to your job."),
("What this does not do","It converts geometry. Accessibility requirements, maximum gradients and landing rules are set by regulation where you are building, and this tool does not know them.")],
"js":"""
var SPEC = {
  fields: [
    {id:'mode', label:'What do you know', type:'select', value:'riseRun', group:'Slope', options:[
      {value:'riseRun', label:'Rise and run'},
      {value:'riseRatio', label:'Rise and ratio (1:X)'},
      {value:'risePct', label:'Rise and percentage'},
      {value:'riseDeg', label:'Rise and degrees'}]},
    {id:'rise', label:'Rise (height to climb)', value:450, unit:'length', group:'Slope', min:0},
    {id:'run', label:'Run available', value:5400, unit:'length', group:'Slope', min:0},
    {id:'ratio', label:'Ratio 1 : X', value:12, group:'Slope', min:0.1},
    {id:'pct', label:'Percentage', value:8.33, group:'Slope', min:0},
    {id:'deg', label:'Degrees', value:4.76, group:'Slope', min:0},
    {id:'landing', label:'Landing every (run)', value:9000, unit:'length', group:'Landings', min:0,
     hint:'0 to skip landings'}
  ],
  compute: function (i) {
    var rise=i.rise, run;
    if (!(rise>0)) return {ok:false, errors:['The rise must be greater than zero.']};

    if (i.mode==='riseRun')        { run=i.run; if(!(run>0)) return {ok:false,errors:['The run must be greater than zero.']}; }
    else if (i.mode==='riseRatio') { if(!(i.ratio>0)) return {ok:false,errors:['The ratio must be greater than zero.']}; run=rise*i.ratio; }
    else if (i.mode==='risePct')   { if(!(i.pct>0)) return {ok:false,errors:['The percentage must be greater than zero.']}; run=rise/(i.pct/100); }
    else                            { if(!(i.deg>0 && i.deg<90)) return {ok:false,errors:['Degrees must be between 0 and 90.']}; run=rise/Math.tan(i.deg*Math.PI/180); }

    var ratio = run/rise;
    var pct = 100*rise/run;
    var deg = Math.atan(rise/run)*180/Math.PI;
    var perM = 1000*rise/run;
    var slopeLen = Math.hypot(rise, run);

    var landings = (i.landing>0) ? Math.max(0, Math.ceil(run/i.landing)-1) : 0;

    var warn=[];
    if (ratio < 8) warn.push('This is steeper than 1:8. Steep for a ramp \u2014 check what your job actually allows.');
    if (deg > 45) warn.push('Over 45 degrees this is a stair or a ladder problem, not a ramp.');

    return {ok:true, rise:rise, run:run, ratio:ratio, pct:pct, deg:deg, slopeLen:slopeLen,
      warnings: warn,
      stats:[
        {value:'1 : '+WCfmt(ratio,2), label:'Ratio'},
        {value: WCfmt(pct,2)+'%', label:'Percentage'},
        {value: WCfmt(deg,2)+String.fromCharCode(176), label:'Degrees'},
        {value: WCfmt(slopeLen,1), label:'Length along the slope'}
      ],
      tables:[{title:'The same slope, four ways', head:['Expressed as','Value'], rows:[
        ['Ratio', '1 : '+WCfmt(ratio,3)],
        ['Percentage', WCfmt(pct,3)+' %'],
        ['Degrees', WCfmt(deg,3)+String.fromCharCode(176)],
        ['Fall per metre', WCfmt(perM,1)+' per 1000'],
        ['Rise', WCfmt(rise,1)],
        ['Run (horizontal)', WCfmt(run,1)],
        ['Length along the slope', WCfmt(slopeLen,2)],
        ['Level landings needed', i.landing>0 ? String(landings) : 'not calculated']
      ]}],
      note:'Run is horizontal, measured level. Length along the slope is the material you actually need \u2014 always longer than the run.'
    };
  },
  diagram: function (r, i) {
    var W=600,H=270,m=55,s=SVG.open(W,H);
    var sc=Math.min((W-2*m)/r.run,(H-100)/Math.max(r.rise,1));
    var base=H-60, x0=m, x1=m+r.run*sc, ytop=base-r.rise*sc;
    s+=SVG.poly([[x0,base],[x1,base],[x1,ytop]],'part');
    s+=SVG.line(x0,base,x1,base,' class="dim"');
    s+=SVG.line(x1,base,x1,ytop,' class="dim"');
    s+=SVG.text((x0+x1)/2,base+22,'run '+WCfmt(r.run,0),12);
    s+=SVG.text(x1+30,(base+ytop)/2,'rise',11);
    s+=SVG.text(x1+30,(base+ytop)/2+15,WCfmt(r.rise,0),11);
    s+=SVG.text((x0+x1)/2-10,(base+ytop)/2-14,'slope '+WCfmt(r.slopeLen,0),12);
    s+=SVG.text(x0+58,base-8,WCfmt(r.deg,1)+String.fromCharCode(176),12);
    s+=SVG.text(W/2,26,'1 : '+WCfmt(r.ratio,2)+'   \u00b7   '+WCfmt(r.pct,2)+'%   \u00b7   '+WCfmt(r.deg,2)+String.fromCharCode(176),13);
    return s+SVG.close();
  }
};
"""}
