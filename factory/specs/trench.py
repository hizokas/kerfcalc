SPEC = {
"slug":"trench-volume-calculator",
"h1":"Trench &amp; Excavation Volume Calculator",
"title_tag":"Trench Calculator — Excavation Volume, Spoil Bulking, Backfill and Lorry Loads",
"description":"Excavation volume for a trench, how much bigger the spoil gets once dug, backfill needed after the pipe and bedding, and how many loads to cart away.",
"card_desc":"Dig volume, spoil bulking, backfill after bedding, and how many loads to cart away.",
"category":"Finishing",
"intro":"The hole is one volume, the heap beside it is a bigger one, and what you cart away is bigger still. This gives all three, plus the bedding and backfill, so you order the right lorries and the right stone.",
"notes":[("Why spoil is bigger than the hole","Undisturbed ground is compacted. Dig it and it breaks into lumps with air between them. Clay bulks about 30 percent, sand and gravel around 15, rock 50 or more. Order skips on the bulked figure, never on the dig volume."),
("Battered sides","Anything deeper than about a metre normally needs the sides sloped back or supported. Sloping widens the top and adds volume fast \u2014 a 1 metre wide trench 2 metres deep at 45 degrees moves twice the material of a vertical one."),
("Backfill is less than you dug","Bedding stone and the pipe itself take up part of the trench, so you backfill less than you excavated \u2014 and the spoil you kept has to be compacted back in layers, which is why some of it never fits."),
("What this does not do","It does not tell you whether the sides need support. Trench collapse is the classic fatal accident on small sites, and depth alone does not decide it \u2014 ground conditions do.")],
"js":"""
var SPEC = {
  fields: [
    {id:'len', label:'Trench length', value:20000, unit:'length', group:'Trench', min:0},
    {id:'width', label:'Width at the bottom', value:600, unit:'length', group:'Trench', min:0},
    {id:'depth', label:'Depth', value:900, unit:'length', group:'Trench', min:0},
    {id:'batter', label:'Side slope (degrees from vertical)', value:0, group:'Trench', min:0,
     hint:'0 for vertical sides'},
    {id:'bulk', label:'Bulking factor (%)', value:25, group:'Spoil', min:0,
     hint:'Clay 30, sand 15, rock 50'},
    {id:'load', label:'Lorry or skip capacity (m3)', value:8, group:'Spoil', min:0.1},
    {id:'bedDepth', label:'Bedding depth', value:150, unit:'length', group:'Backfill', min:0},
    {id:'pipeDia', label:'Pipe diameter', value:110, unit:'length', group:'Backfill', min:0}
  ],
  compute: function (i) {
    var k = i.unit === 'in' ? 0.0254 : 0.001;
    var L=i.len*k, Wb=i.width*k, D=i.depth*k;
    if (!(L>0 && Wb>0 && D>0)) return {ok:false, errors:['Length, width and depth must all be greater than zero.']};
    if (!(i.batter>=0 && i.batter<80)) return {ok:false, errors:['The side slope must be between 0 and 80 degrees.']};

    var spread = D*Math.tan(i.batter*Math.PI/180);
    var Wt = Wb + 2*spread;                       // largeur en tete
    var dig = L*D*(Wb+Wt)/2;                      // section trapezoidale

    var bulked = dig*(1+Math.max(0,i.bulk)/100);
    var loads = Math.ceil(bulked/Math.max(0.1,i.load));

    var bed = L*Wb*(i.bedDepth*k);
    var pipeR = (i.pipeDia*k)/2;
    var pipeVol = L*Math.PI*pipeR*pipeR;
    var backfill = Math.max(0, dig - bed - pipeVol);

    var warn=[];
    if (D > 1.2 && i.batter === 0) warn.push('Over 1.2 m deep with vertical sides. Trench support or battering is normally required \u2014 this is the accident that kills people on small sites.');
    if (Wb < 0.45 && D > 1) warn.push('A trench under 450 mm wide is very hard to work in safely at this depth.');

    return {ok:true, dig:dig, bulked:bulked, loads:loads, backfill:backfill, bed:bed, pipeVol:pipeVol,
      L:L, Wb:Wb, Wt:Wt, D:D,
      warnings: warn,
      stats:[
        {value: WCfmt(dig,2), label:'m3 to dig'},
        {value: WCfmt(bulked,2), label:'m3 of spoil'},
        {value: String(loads), label:'Loads to cart'},
        {value: WCfmt(backfill,2), label:'m3 of backfill'}
      ],
      tables:[{title:'Working', head:['Item','Value'], rows:[
        ['Trench', WCfmt(L,2)+' m long, '+WCfmt(D,2)+' m deep'],
        ['Width at the bottom', WCfmt(Wb,3)+' m'],
        ['Width at the top', WCfmt(Wt,3)+' m'],
        ['Excavation volume', WCfmt(dig,3)+' m3'],
        ['Bulking at '+WCfmt(i.bulk,0)+'%', WCfmt(bulked,3)+' m3'],
        ['Loads of '+WCfmt(i.load,1)+' m3', String(loads)],
        ['Bedding stone', WCfmt(bed,3)+' m3'],
        ['Pipe displaces', WCfmt(pipeVol,4)+' m3'],
        ['Backfill required', WCfmt(backfill,3)+' m3'],
        ['Weight of spoil (approx)', WCfmt(bulked*1.6,1)+' tonnes at 1.6 t/m3']
      ]}],
      note:'Order removal on the bulked figure. The heap beside the trench is always bigger than the hole it came out of.'
    };
  },
  diagram: function (r, i) {
    var W=560,H=280,m=60,s=SVG.open(W,H);
    var sc=Math.min((W-2*m)/Math.max(r.Wt,0.1), (H-120)/Math.max(r.D,0.1));
    var cx=W/2, top=70, dh=r.D*sc, wt=r.Wt*sc, wb=r.Wb*sc;
    s+=SVG.line(m-20,top,W-m+20,top,' class="dim"');
    s+=SVG.poly([[cx-wt/2,top],[cx+wt/2,top],[cx+wb/2,top+dh],[cx-wb/2,top+dh]],'part');
    var bd=(i.bedDepth*(i.unit==='in'?0.0254:0.001))*sc;
    if (bd>1) s+=SVG.rect(cx-wb/2, top+dh-bd, wb, bd, 'ghost');
    s+=SVG.text(cx, top-10, 'top width '+WCfmt(r.Wt,2)+' m', 12);
    s+=SVG.text(cx, top+dh+22, 'bottom '+WCfmt(r.Wb,2)+' m', 12);
    s+=SVG.text(cx, 30, WCfmt(r.dig,2)+' m3 dug  \u00b7  '+WCfmt(r.bulked,2)+' m3 of spoil', 13);
    s+=SVG.text(cx, H-14, r.loads+' loads to cart away', 12);
    return s+SVG.close();
  }
};
"""}
