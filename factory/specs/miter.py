SPEC = {
"slug":"compound-miter-calculator",
"h1":"Compound Miter Angle Calculator",
"title_tag":"Compound Miter Calculator — Saw Miter and Bevel for Crown and Sloped Work",
"description":"Miter and bevel saw settings for crown moulding and any sloped compound joint, from the spring angle and the corner angle, with the trigonometry shown.",
"card_desc":"Saw miter and bevel settings for crown and sloped work, with the formulas shown.",
"category":"Joinery",
"intro":"Two numbers you cannot guess and cannot get right by trial and error on site. Give the spring angle of the moulding and the actual corner angle, and this gives you the miter and bevel to dial into the saw.",
"notes":[("Why 45 degrees does not work","Crown sits on the wall at a spring angle, so the cut face is not square to the saw table. The miter and bevel both shift, and for standard 38 degree crown on a square corner they land at 31.6 and 33.9, not 45 and 0."),
("Measure the corner, do not assume","Walls are rarely 90 degrees. A corner that is 2 degrees out leaves a visible gap at the top of the moulding. A digital angle finder pays for itself on the first room."),
("The formulas","miter = atan(sin(spring) x tan(corner/2)), bevel = asin(cos(spring) x cos(corner/2)). Both are shown in the results so you can check them."),
("What this does not do","It does not know which way up your moulding goes on the saw. Cut a test piece in scrap first, every time. Nobody gets the orientation right from memory.")],
"js":"""
var SPEC = {
  fields: [
    {id:'spring', label:'Spring angle (degrees)', value:38, group:'Moulding', min:1, max:89, hint:'38 or 45 are the usual crown profiles'},
    {id:'corner', label:'Corner angle (degrees)', value:90, group:'Corner', min:1, max:179, hint:'Measure it, do not assume 90'},
    {id:'type', label:'Corner type', type:'select', value:'inside', group:'Corner', options:[
      {value:'inside', label:'Inside corner'},
      {value:'outside', label:'Outside corner'}]}
  ],
  compute: function (i) {
    var errs=[];
    if(!(i.spring>0 && i.spring<90)) errs.push('Spring angle must be between 0 and 90 degrees.');
    if(!(i.corner>0 && i.corner<180)) errs.push('Corner angle must be between 0 and 180 degrees.');
    if(errs.length) return {ok:false, errors:errs};

    var d2r=Math.PI/180, r2d=180/Math.PI;
    var S=i.spring*d2r, C=i.corner*d2r;
    var miter=Math.atan(Math.sin(S)*Math.tan(C/2))*r2d;
    var bevel=Math.asin(Math.cos(S)*Math.cos(C/2))*r2d;
    var saw=90-miter;

    var warn=[];
    if (Math.abs(i.corner-90)>5) warn.push('That corner is '+WCfmt(Math.abs(i.corner-90),1)+' degrees off square — worth re-measuring before you cut anything expensive.');
    if (miter>50||bevel>50) warn.push('These settings are beyond the range of some mitre saws. Check the saw reaches them before cutting.');

    return {ok:true, miter:miter, bevel:bevel, saw:saw, warnings:warn,
      stats:[
        {value:WCfmt(miter,2)+String.fromCharCode(176), label:'Miter angle'},
        {value:WCfmt(bevel,2)+String.fromCharCode(176), label:'Bevel angle'},
        {value:WCfmt(i.spring,0)+String.fromCharCode(176), label:'Spring angle'},
        {value:WCfmt(i.corner,1)+String.fromCharCode(176), label:'Corner'}
      ],
      tables:[{title:'Saw settings', head:['Setting','Value','Where it comes from'], rows:[
        ['Miter', WCfmt(miter,2)+String.fromCharCode(176), 'atan(sin('+WCfmt(i.spring,0)+') x tan('+WCfmt(i.corner/2,1)+'))'],
        ['Bevel', WCfmt(bevel,2)+String.fromCharCode(176), 'asin(cos('+WCfmt(i.spring,0)+') x cos('+WCfmt(i.corner/2,1)+'))'],
        ['Miter, if your saw reads from 90', WCfmt(saw,2)+String.fromCharCode(176), '90 minus the miter'],
        ['Corner type', i.type==='inside'?'Inside':'Outside', i.type==='inside'?'Long point to the back':'Long point to the front'],
        ['Pieces per corner', '2', 'Both cut to the same settings, mirrored']
      ]}],
      note:'Cut a test pair in scrap and offer them up before touching the real moulding. The numbers are right; the orientation on the saw is what catches people out.'
    };
  },
  diagram: function (r,i){
    var W=560,H=240,s=SVG.open(W,H),cx=W/2,cy=150,L=150;
    var half=i.corner/2*Math.PI/180;
    var x1=cx-Math.sin(half)*L, y1=cy-Math.cos(half)*L;
    var x2=cx+Math.sin(half)*L, y2=cy-Math.cos(half)*L;
    s+=SVG.poly([[x1,y1],[cx,cy],[x2,y2]],'ghost');
    s+=SVG.line(cx,cy,x1,y1,' stroke-width="2.5"');
    s+=SVG.line(cx,cy,x2,y2,' stroke-width="2.5"');
    s+='<path d="M '+(cx-30*Math.sin(half))+' '+(cy-30*Math.cos(half))+' A 30 30 0 0 1 '+(cx+30*Math.sin(half))+' '+(cy-30*Math.cos(half))+'" fill="none" stroke="currentColor" stroke-width="1"/>';
    s+=SVG.text(cx,cy-42,WCfmt(i.corner,1)+String.fromCharCode(176),13);
    s+=SVG.text(cx,26,'Set the saw to these two numbers',12);
    s+=SVG.text(cx,H-38,'Miter '+WCfmt(r.miter,2)+String.fromCharCode(176)+'    Bevel '+WCfmt(r.bevel,2)+String.fromCharCode(176),15);
    s+=SVG.text(cx,H-16,'Spring angle '+WCfmt(i.spring,0)+String.fromCharCode(176)+' - '+(i.type==='inside'?'inside':'outside')+' corner',11);
    return s+SVG.close();
  }
};
"""}
