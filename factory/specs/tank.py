SPEC = {
"slug":"tank-volume-calculator",
"h1":"Tank Volume &amp; Fill Level Calculator",
"title_tag":"Tank Volume Calculator — Capacity and Litres at Any Depth, Horizontal or Vertical",
"description":"Total capacity and the volume at any fill depth for vertical, horizontal and rectangular tanks, with a dipstick table you can print.",
"card_desc":"Capacity and litres at any depth, including horizontal cylinders, with a dipstick table.",
"category":"Finishing",
"intro":"A vertical tank half full holds half its capacity. A horizontal one does too \u2014 but at a third of the way up it holds barely a fifth, and that is where people get caught. This gives the volume at any depth, plus a dipstick table.",
"notes":[("Why horizontal tanks are counter-intuitive","The cross-section is a circle, so the area of the wetted part changes with the square of the depth near the bottom and top. Filling the first quarter of the height adds far less than filling the middle quarter."),
("The formula for a partly full cylinder","The wetted area is the circular segment: r squared times (theta minus sin theta) over two, where theta is twice the arccosine of (r minus depth) over r. Multiply by the length and you have the volume."),
("Making a dipstick","Print the table, mark the depths on a straight stick, and you have a gauge calibrated to your actual tank. Far more reliable than a float gauge and it never fails."),
("What this does not do","It assumes flat ends and a level tank. Dished or hemispherical ends add capacity, and a tank sitting even slightly out of level reads wrong at both extremes.")],
"js":"""
var SPEC = {
  fields: [
    {id:'shape', label:'Tank shape', type:'select', value:'vertical', group:'Tank', options:[
      {value:'vertical', label:'Vertical cylinder'},
      {value:'horizontal', label:'Horizontal cylinder'},
      {value:'rect', label:'Rectangular'}]},
    {id:'dia', label:'Diameter', value:1200, unit:'length', group:'Tank', min:0, hint:'Cylinders'},
    {id:'len', label:'Length or height', value:2000, unit:'length', group:'Tank', min:0},
    {id:'rectW', label:'Width', value:1000, unit:'length', group:'Tank', min:0, hint:'Rectangular only'},
    {id:'rectH', label:'Height', value:1000, unit:'length', group:'Tank', min:0, hint:'Rectangular only'},
    {id:'level', label:'Current fill depth', value:400, unit:'length', group:'Level', min:0},
    {id:'steps', label:'Dipstick rows', value:11, group:'Level', min:2, step:1}
  ],
  compute: function (i) {
    var k = i.unit === 'in' ? 0.0254 : 0.001;
    var d=i.dia*k, Ln=i.len*k, rw=i.rectW*k, rh=i.rectH*k, lvl=i.level*k;

    function volAt(h) {
      if (i.shape === 'vertical')   return Math.PI*d*d/4*Math.min(h, Ln);
      if (i.shape === 'rect')       return rw*Ln*Math.min(h, rh);
      var r=d/2, hh=Math.max(0, Math.min(h, d));
      if (hh<=0) return 0;
      if (hh>=d) return Math.PI*r*r*Ln;
      var theta=2*Math.acos((r-hh)/r);
      return 0.5*r*r*(theta - Math.sin(theta))*Ln;
    }

    var full, height;
    if (i.shape === 'vertical')      { if(!(d>0&&Ln>0)) return {ok:false,errors:['Diameter and height must be greater than zero.']};
                                       full=Math.PI*d*d/4*Ln; height=Ln; }
    else if (i.shape === 'horizontal'){ if(!(d>0&&Ln>0)) return {ok:false,errors:['Diameter and length must be greater than zero.']};
                                       full=Math.PI*d*d/4*Ln; height=d; }
    else                              { if(!(rw>0&&Ln>0&&rh>0)) return {ok:false,errors:['All three dimensions must be greater than zero.']};
                                       full=rw*Ln*rh; height=rh; }

    var cur = volAt(lvl);
    var pctFull = full>0 ? 100*cur/full : 0;
    var pctHeight = height>0 ? 100*Math.min(lvl,height)/height : 0;

    var n=Math.max(2, Math.round(i.steps));
    var rows=[];
    for (var q=0;q<n;q++){
      var h=height*q/(n-1);
      var v=volAt(h);
      rows.push([WCfmt(h*1000,0), WCfmt(v*1000,1), WCfmt(full>0?100*v/full:0,1)+'%']);
    }

    var warn=[];
    if (lvl > height) warn.push('The fill depth is greater than the tank \u2014 showing it as full.');
    if (i.shape==='horizontal') warn.push('At '+WCfmt(pctHeight,0)+'% of the height this tank is '+WCfmt(pctFull,0)+'% full by volume. Depth and volume are not proportional in a horizontal cylinder.');

    return {ok:true, full:full, cur:cur, pctFull:pctFull, height:height, d:d, Ln:Ln, shape:i.shape,
      warnings: warn,
      stats:[
        {value: WCfmt(full*1000,0), label:'Litres when full'},
        {value: WCfmt(cur*1000,1), label:'Litres now'},
        {value: WCfmt(pctFull,1)+'%', label:'Percent full'},
        {value: WCfmt(full,3), label:'m3 capacity'}
      ],
      tables:[
        {title:'Now', head:['Item','Value'], rows:[
          ['Shape', {vertical:'Vertical cylinder', horizontal:'Horizontal cylinder', rect:'Rectangular'}[i.shape] || i.shape],
          ['Capacity', WCfmt(full*1000,1)+' litres / '+WCfmt(full,4)+' m3 / '+WCfmt(full*219.969,1)+' imp gal'],
          ['Fill depth', WCfmt(lvl*1000,0)+' mm of '+WCfmt(height*1000,0)+' mm'],
          ['Depth as a percentage', WCfmt(pctHeight,1)+'%'],
          ['Volume as a percentage', WCfmt(pctFull,1)+'%'],
          ['Contents', WCfmt(cur*1000,1)+' litres'],
          ['Ullage (space left)', WCfmt((full-cur)*1000,1)+' litres']
        ]},
        {title:'Dipstick table', head:['Depth (mm)','Litres','Percent'], rows:rows}
      ],
      note:'Print the dipstick table and mark the depths on a straight stick \u2014 that gives you a gauge calibrated to this exact tank.'
    };
  },
  diagram: function (r, i) {
    var W=520,H=300,cx=W/2,cy=160,s=SVG.open(W,H);
    var frac=r.height>0?Math.min(1,(i.level*(i.unit==='in'?0.0254:0.001))/r.height):0;
    if (i.shape==='horizontal'){
      var rad=95;
      s+='<circle cx="'+cx+'" cy="'+cy+'" r="'+rad+'" class="ghost"/>';
      var hh=2*rad*frac, yTop=cy+rad-hh;
      s+='<clipPath id="cl"><rect x="'+(cx-rad)+'" y="'+yTop+'" width="'+(2*rad)+'" height="'+hh+'"/></clipPath>';
      s+='<circle cx="'+cx+'" cy="'+cy+'" r="'+rad+'" class="part" clip-path="url(#cl)"/>';
    } else {
      var bw=150,bh=170, x0=cx-bw/2, y0=cy-bh/2;
      s+=SVG.rect(x0,y0,bw,bh,'ghost');
      s+=SVG.rect(x0,y0+bh*(1-frac),bw,bh*frac,'part');
    }
    s+=SVG.text(cx,30, WCfmt(r.cur*1000,1)+' litres of '+WCfmt(r.full*1000,0), 14);
    s+=SVG.text(cx,H-14, WCfmt(r.pctFull,1)+'% full by volume', 12);
    return s+SVG.close();
  }
};
"""}
