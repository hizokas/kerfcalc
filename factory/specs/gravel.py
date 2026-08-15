SPEC = {
"slug":"gravel-volume-calculator",
"h1":"Gravel & Aggregate Calculator",
"title_tag":"Gravel Calculator — Volume, Tonnage and Compaction for Any Area",
"description":"Volume and tonnage for gravel, hardcore, sand and topsoil, including the compaction allowance that loose-volume calculators leave out.",
"card_desc":"Volume and tonnage for aggregates, including the compaction allowance most calculators forget.",
"category":"Finishing",
"intro":"Aggregate is quoted by the tonne, spread by the cubic metre, and it shrinks when you compact it. All three are handled here, so the number you order is the number that finishes the job.",
"notes":[("Why compaction matters","Loose gravel loses 15-25% of its volume under a plate compactor. Order the compacted depth and you finish 20 mm short across the whole area, which on a driveway is a lot of missing material."),
("Volume to tonnes","Multiply cubic metres by the bulk density. Roughly 1.5 t/m3 for gravel and hardcore, 1.6 for sharp sand, 1.4 for topsoil, 2.4 for solid stone. Merchants publish their own figures and they do vary."),
("Depths that actually work","Decorative gravel 40-50 mm, pedestrian paths 50 mm over a base, driveways 150-200 mm of sub-base plus a wearing course. Too thin and it rutts, too thick and it never locks up."),
("What this does not do","It does not design a build-up or tell you whether you need a membrane and a sub-base. On anything a car drives over, you usually do.")],
"js":"""
var SPEC = {
  fields: [
    {id:'shape', label:'Area shape', type:'select', value:'rect', group:'Area', options:[
      {value:'rect', label:'Rectangle'},
      {value:'circle', label:'Circle'}]},
    {id:'a', label:'Length', value:8000, unit:'length', group:'Area', min:0},
    {id:'b', label:'Width', value:3000, unit:'length', group:'Area', min:0},
    {id:'dia', label:'Diameter', value:4000, unit:'length', group:'Area', min:0, hint:'Circles only'},
    {id:'depth', label:'Finished depth', value:50, unit:'length', group:'Area', min:0},
    {id:'compact', label:'Compaction allowance (%)', value:20, group:'Ordering', min:0, hint:'0 for loose decorative gravel'},
    {id:'density', label:'Bulk density (t/m3)', value:1.5, group:'Ordering', min:0.1, hint:'1.5 gravel, 1.6 sand, 1.4 topsoil'},
    {id:'bagT', label:'Bulk bag size (tonnes)', value:0.85, group:'Ordering', min:0.05}
  ],
  compute: function (i) {
    var k=i.unit==='in'?0.0254:0.001;
    var area, label;
    if (i.shape==='circle'){ var d=i.dia*k; if(!(d>0)) return {ok:false,errors:['Diameter must be greater than zero.']};
      area=Math.PI*Math.pow(d/2,2); label='Circle diameter '+WCfmt(d,2)+' m'; }
    else { var A=i.a*k,B=i.b*k; if(!(A>0&&B>0)) return {ok:false,errors:['Length and width must both be greater than zero.']};
      area=A*B; label='Rectangle '+WCfmt(A,2)+' x '+WCfmt(B,2)+' m'; }
    var dep=i.depth*k;
    if(!(dep>0)) return {ok:false, errors:['Depth must be greater than zero.']};
    if(!(i.density>0)) return {ok:false, errors:['Bulk density must be greater than zero.']};

    var finished=area*dep;
    var loose=finished*(1+Math.max(0,i.compact)/100);
    var tonnes=loose*i.density;
    var bags=Math.ceil(tonnes/Math.max(0.05,i.bagT));

    var warn=[];
    if (dep<0.04) warn.push('Under 40 mm, loose gravel scatters and will not lock up.');
    if (dep>0.3) warn.push('Over 300 mm should normally be laid and compacted in layers rather than in one go.');

    return {ok:true, area:area, finished:finished, loose:loose, tonnes:tonnes, bags:bags, label:label, warnings:warn,
      stats:[
        {value:WCfmt(tonnes,2), label:'Tonnes to order'},
        {value:WCfmt(loose,2), label:'m3 loose'},
        {value:String(bags), label:'Bulk bags'},
        {value:WCfmt(area,1), label:'m2 of area'}
      ],
      tables:[{title:'Breakdown', head:['Item','Value'], rows:[
        ['Area', label+' = '+WCfmt(area,2)+' m2'],
        ['Finished depth', WCfmt(dep*1000,0)+' mm'],
        ['Compacted volume', WCfmt(finished,3)+' m3'],
        ['Compaction allowance', WCfmt(i.compact,0)+'%'],
        ['Loose volume to order', WCfmt(loose,3)+' m3 / '+WCfmt(loose*1.30795,2)+' yd3'],
        ['Bulk density', i.density+' t/m3'],
        ['Weight', WCfmt(tonnes,3)+' tonnes / '+WCfmt(tonnes*1.10231,2)+' US tons'],
        ['Bulk bags at '+i.bagT+' t', String(bags)]
      ]}]
    };
  },
  diagram: function (r,i){
    var W=560,H=200,s=SVG.open(W,H),m=48;
    if(i.shape==='circle'){ var cx=W/2,cy=104,rad=62;
      s+='<circle cx="'+cx+'" cy="'+cy+'" r="'+rad+'" class="part"/>';
      s+=SVG.text(cx,cy+4,WCfmt(r.area,1)+' m2',12);
    } else { var bw=W-2*m, bh=92;
      s+=SVG.rect(m,54,bw,bh,'part'); s+=SVG.text(W/2,54+bh/2,WCfmt(r.area,1)+' m2 at '+WCfmt(i.depth,0)+' deep',12); }
    s+=SVG.text(W/2,26,r.label,12);
    s+=SVG.text(W/2,H-14, WCfmt(r.tonnes,2)+' tonnes  -  '+WCfmt(r.loose,2)+' m3 loose  -  '+r.bags+' bulk bags',12);
    return s+SVG.close();
  }
};
"""}
