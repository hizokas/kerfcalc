SPEC = {
"slug":"concrete-volume-calculator",
"h1":"Concrete Volume Calculator",
"title_tag":"Concrete Calculator — Slabs, Footings and Columns, With Bag Counts",
"description":"Concrete volume for slabs, footings, columns and post holes, in cubic metres and cubic yards, with the number of 20 kg, 25 kg, 40 lb, 60 lb or 80 lb bags.",
"card_desc":"Volume for slabs, footings, columns and post holes, plus how many bags that actually is.",
"category":"Finishing",
"intro":"Volume for the pour you are actually doing, with the bag count worked out. Ready-mix is sold by volume and bags are sold by weight, so the two numbers are given side by side.",
"notes":[("Why order more than the calculated volume","Subgrade is never perfectly flat and forms bow outward under the weight. 5-10% over is standard, and running short mid-pour leaves a cold joint you cannot undo."),
("Bags or ready-mix?","Bags stop making sense somewhere around half a cubic metre. Past that you are mixing for hours and the first batch is setting before the last is poured."),
("Post holes","The hole volume minus the post volume is what actually gets filled. For several identical holes this adds up quickly, so the tool subtracts the post."),
("What this does not do","It does not specify a concrete mix, reinforcement or thickness. Those depend on load and ground conditions and are not a calculator question.")],
"js":"""
var SPEC = {
  fields: [
    {id:'shape', label:'What are you pouring', type:'select', value:'slab', group:'Shape', options:[
      {value:'slab', label:'Slab / pad'},
      {value:'footing', label:'Strip footing'},
      {value:'column', label:'Round column'},
      {value:'posthole', label:'Post holes'}]},
    {id:'a', label:'Length', value:5000, unit:'length', group:'Dimensions', min:0},
    {id:'b', label:'Width', value:3000, unit:'length', group:'Dimensions', min:0, hint:'Ignored for round shapes'},
    {id:'d', label:'Thickness / depth', value:100, unit:'length', group:'Dimensions', min:0},
    {id:'dia', label:'Diameter', value:300, unit:'length', group:'Dimensions', min:0, hint:'Columns and post holes'},
    {id:'postDia', label:'Post diameter', value:100, unit:'length', group:'Dimensions', min:0, hint:'Subtracted from the hole'},
    {id:'count', label:'How many', value:1, group:'Dimensions', min:1, step:1},
    {id:'over', label:'Over-order allowance (%)', value:8, group:'Ordering', min:0},
    {id:'bag', label:'Bag size', type:'select', value:'20kg', group:'Ordering', options:[
      {value:'20kg', label:'20 kg bag (\u2248 0.009 m\u00b3)'},
      {value:'25kg', label:'25 kg bag (\u2248 0.0113 m\u00b3)'},
      {value:'40lb', label:'40 lb bag (\u2248 0.011 yd\u00b3)'},
      {value:'60lb', label:'60 lb bag (\u2248 0.017 yd\u00b3)'},
      {value:'80lb', label:'80 lb bag (\u2248 0.022 yd\u00b3)'}]}
  ],
  compute: function (i) {
    var k = i.unit === 'in' ? 0.0254 : 0.001;   // vers mètres
    var a=i.a*k, b=i.b*k, d=i.d*k, dia=i.dia*k, pd=i.postDia*k;
    var n = Math.max(1, Math.round(i.count));
    var m3=0, label='', errs=[];

    if (i.shape==='slab')      { if(!(a>0&&b>0&&d>0)) errs.push('Length, width and thickness must all be greater than zero.'); m3=a*b*d; label='Slab '+WCfmt(a,2)+' \u00d7 '+WCfmt(b,2)+' \u00d7 '+WCfmt(d*1000,0)+' mm'; }
    else if (i.shape==='footing'){ if(!(a>0&&b>0&&d>0)) errs.push('Length, width and depth must all be greater than zero.'); m3=a*b*d; label='Footing '+WCfmt(a,2)+' m long'; }
    else if (i.shape==='column'){ if(!(dia>0&&d>0)) errs.push('Diameter and height must be greater than zero.'); m3=Math.PI*Math.pow(dia/2,2)*d; label='Column \u00d8'+WCfmt(dia*1000,0)+' mm'; }
    else                        { if(!(dia>0&&d>0)) errs.push('Hole diameter and depth must be greater than zero.');
                                  if(pd>=dia) errs.push('The post is as wide as the hole — nothing left to fill.');
                                  m3=(Math.PI*Math.pow(dia/2,2)-Math.PI*Math.pow(pd/2,2))*d; label='Post hole \u00d8'+WCfmt(dia*1000,0)+' mm'; }

    if (errs.length) return {ok:false, errors:errs};

    var total = m3*n;
    var withOver = total*(1+Math.max(0,i.over)/100);
    var yd3 = withOver*1.30795;
    var perBag = {'20kg':0.009,'25kg':0.0113,'40lb':0.00841,'60lb':0.01300,'80lb':0.01682}[i.bag];
    var bags = Math.ceil(withOver/perBag);

    var warn = [];
    if (withOver > 0.5) warn.push('Over half a cubic metre — mixing this from bags means ' + bags + ' of them. Ready-mix is usually cheaper and always more consistent past this point.');

    return {ok:true, m3:total, withOver:withOver, yd3:yd3, bags:bags, each:m3, n:n, label:label,
      warnings: warn,
      stats:[
        {value: WCfmt(withOver,3), label:'Cubic metres to order'},
        {value: WCfmt(yd3,2), label:'Cubic yards'},
        {value: String(bags), label:'Bags of '+i.bag},
        {value: WCfmt(total,3), label:'Calculated volume'}
      ],
      tables:[{title:'Breakdown', head:['Item','Value'], rows:[
        ['Shape', label],
        ['Volume each', WCfmt(m3,4)+' m\u00b3'],
        ['How many', String(n)],
        ['Calculated total', WCfmt(total,4)+' m\u00b3'],
        ['Over-order allowance', WCfmt(i.over,0)+'%'],
        ['Order this', WCfmt(withOver,3)+' m\u00b3 / '+WCfmt(yd3,2)+' yd\u00b3'],
        ['Bags needed', String(bags)+' \u00d7 '+i.bag]
      ]}],
      note:'Ready-mix is sold by volume, bags by weight — both numbers are above so you can price either way.'
    };
  },
  diagram: function (r, i) {
    var W=560,H=220,m=45,s=SVG.open(W,H);
    if (i.shape==='column'||i.shape==='posthole'){
      var cx=W/2, rad=52, top=40, hgt=110;
      s+='<ellipse cx="'+cx+'" cy="'+top+'" rx="'+rad+'" ry="16" class="part"/>';
      s+=SVG.rect(cx-rad, top, rad*2, hgt, 'part');
      s+='<ellipse cx="'+cx+'" cy="'+(top+hgt)+'" rx="'+rad+'" ry="16" class="part"/>';
      if(i.shape==='posthole'){ var pr=rad*(i.postDia/Math.max(1,i.dia));
        s+=SVG.rect(cx-pr, top-16, pr*2, hgt+16, 'ghost');
        s+='<ellipse cx="'+cx+'" cy="'+(top-16)+'" rx="'+pr+'" ry="6" class="ghost"/>'; }
      s+=SVG.text(cx, H-24, r.label+' \u00b7 '+WCfmt(r.each,4)+' m\u00b3 each', 12);
    } else {
      var bw=W-2*m, bh=78, x=m, y=52, dep=26;
      s+=SVG.poly([[x,y],[x+dep,y-dep],[x+bw+dep,y-dep],[x+bw,y]],'part');
      s+=SVG.poly([[x+bw,y],[x+bw+dep,y-dep],[x+bw+dep,y+bh-dep],[x+bw,y+bh]],'part');
      s+=SVG.rect(x,y,bw,bh,'part');
      s+=SVG.text(x+bw/2, y+bh/2+4, r.label, 13);
      s+=SVG.text(x+bw/2, H-20, WCfmt(r.withOver,3)+' m\u00b3 to order \u00b7 '+r.bags+' bags', 12);
    }
    return s+SVG.close();
  }
};
"""}
