SPEC = {
'slug': 'paint-coverage-calculator',
'h1': 'Paint Coverage Calculator',
'title_tag': 'Paint Calculator — Litres and Gallons by Room, Coats and Openings',
'description': 'Estimate wall and ceiling paint in litres and US gallons. Enter measured openings, coats, separate primer coverage and tin sizes, with an optional extra allowance.',
'card_desc': 'Litres or gallons per coat with openings subtracted, rounded up to real tin sizes.',
'category': 'Finishing',
'intro': 'Enter your room and opening sizes to estimate colour paint and primer separately, then round each product up to tins you can buy.',
'notes': [('Which coverage rate should I enter?', 'Use the m2 per litre per coat stated for the paint and surface you have chosen. Coverage depends on both the product and the surface. The starting values here are editable examples, not a product specification.'), ('How are doors and windows subtracted?', 'Opening area equals count x average width x average height. Enter measured sizes. If openings differ, choose averages whose width x height equals the mean opening area, or calculate sections separately. Reveal surfaces and trim are not included.'), ('How many coats do I need?', 'Follow the selected product instructions for your surface and colour change. The calculator lets you choose colour and primer coats separately. Some paints specify a one-coat system; there is no universal two-coat rule.'), ('Why is primer calculated separately?', 'Primer has its own coverage, coat count and tin size. Enabling it applies those values to the same area as the colour paint. Estimate it separately if only part of the room needs primer.'), ('What is the extra allowance?', 'It is an optional percentage added before each product is rounded up to whole tins. Leave it at zero for the geometric estimate. Choose any additional allowance based on your own project and product guidance.')],
"js": """
var SPEC = {
  fields: [
    {id:'len', label:'Room length', value:5000, unit:'length', group:'Room', min:0},
    {id:'wid', label:'Room width', value:4000, unit:'length', group:'Room', min:0},
    {id:'hgt', label:'Wall height', value:2400, unit:'length', group:'Room', min:0},
    {id:'ceiling', label:'Include the ceiling', type:'check', value:false, group:'Room'},
    {id:'doors', label:'Number of doors', value:1, group:'Openings', min:0, step:1, hint:'Count openings with the dimensions entered below'},
    {id:'windows', label:'Number of windows', value:2, group:'Openings', min:0, step:1, hint:'Use average dimensions if the windows differ'},
    {id:'doorW', label:'Average door width', value:900, unit:'length', group:'Openings', min:0},
    {id:'doorH', label:'Average door height', value:2000, unit:'length', group:'Openings', min:0},
    {id:'windowW', label:'Average window width', value:1200, unit:'length', group:'Openings', min:0},
    {id:'windowH', label:'Average window height', value:1200, unit:'length', group:'Openings', min:0},
    {id:'coats', label:'Coats', value:2, group:'Paint', min:1, step:1},
    {id:'cover', label:'Coverage per litre (m2)', value:11, group:'Paint', min:1, hint:'m2 per litre per coat, from your chosen product label'},
    {id:'tin', label:'Colour tin size (litres)', value:2.5, group:'Paint', min:0.1},
    {id:'allowance', label:'Extra allowance (%)', value:0, group:'Paint', min:0, hint:'Optional extra for losses or touch-ups; added to both products'},
    {id:'primer', label:'Include primer', type:'check', value:false, group:'Primer'},
    {id:'primerCoats', label:'Primer coats', value:1, group:'Primer', min:1, step:1},
    {id:'primerCover', label:'Primer coverage (m2 per litre)', value:10, group:'Primer', min:0.1, hint:'Separate product label coverage; used when primer is included'},
    {id:'primerTin', label:'Primer tin size (litres)', value:2.5, group:'Primer', min:0.1}
  ],
  compute: function (i) {
    var positive=['len','wid','hgt','cover','tin'];
    if (i.doors>0) positive.push('doorW','doorH');
    if (i.windows>0) positive.push('windowW','windowH');
    if (i.primer) positive.push('primerCover','primerTin');
    if (positive.some(function(key){return !Number.isFinite(i[key]) || i[key]<=0;}))
      return {ok:false,errors:['Use positive finite dimensions, coverage rates and tin sizes for the products and openings included.']};
    if (['doors','windows'].some(function(key){return !Number.isInteger(i[key]) || i[key]<0;}))
      return {ok:false,errors:['Door and window counts must be whole numbers, zero or greater.']};
    if (!Number.isInteger(i.coats)||i.coats<1||i.coats>20 || (i.primer&&(!Number.isInteger(i.primerCoats)||i.primerCoats<1||i.primerCoats>20)))
      return {ok:false,errors:['Enter a whole number of coats from 1 to 20 for each included product.']};
    if (!Number.isFinite(i.allowance)||i.allowance<0||i.allowance>100)
      return {ok:false,errors:['Extra allowance must be between 0 and 100 percent.']};
    var k=i.unit==='in'?0.0254:0.001;
    var L=i.len*k,W=i.wid*k,H=i.hgt*k;
    var wallGross=2*(L+W)*H,ceil=i.ceiling?L*W:0;
    var doorA=i.doors?i.doors*i.doorW*k*i.doorH*k:0;
    var winA=i.windows?i.windows*i.windowW*k*i.windowH*k:0;
    var openings=doorA+winA;
    if (openings>wallGross) return {ok:false,errors:['The opening area exceeds the gross wall area. Check the counts and average sizes.']};
    var wallNet=wallGross-openings,paintArea=wallNet+ceil;
    var coats=i.coats,totalCoats=coats+(i.primer?i.primerCoats:0);
    var factor=1+i.allowance/100;
    var baseLitres=paintArea*coats/i.cover,litres=baseLitres*factor;
    var primerL=i.primer?paintArea*i.primerCoats/i.primerCover*factor:0;
    var tins=Math.ceil(litres/i.tin),primerTins=i.primer?Math.ceil(primerL/i.primerTin):0;
    if (![paintArea,litres,primerL,tins,primerTins].every(Number.isFinite) || !Number.isSafeInteger(tins) || !Number.isSafeInteger(primerTins))
      return {ok:false,errors:['These inputs exceed the calculation range. Check dimensions and product quantities.']};
    var warn=[];
    if (i.ceiling) warn.push('Ceiling and walls use the same selected colour product. Calculate them separately when the paints differ.');
    if (i.primer) warn.push('Primer is applied to the same net area here. Calculate separately when only some surfaces need primer.');

    return {ok:true, litres:litres, tins:tins, paintArea:paintArea, primerL:primerL, primerTins:primerTins, warnings:warn,
      stats:[
        {value: WCfmt(paintArea,1), label:'m2 to cover'},
        {value: WCfmt(litres,1), label:'Litres of colour'},
        {value: String(tins), label:'Tins of '+i.tin+' L'},
        {value: String(totalCoats), label:'Coats in total'}
      ],
      tables:[{title:'Breakdown', head:['Item','Value'], rows:[
        ['Wall area gross', WCfmt(wallGross,2)+' m2'],
        ['Doors', WCfmt(i.doors,0)+' ('+WCfmt(doorA,2)+' m2)'],
        ['Windows', WCfmt(i.windows,0)+' ('+WCfmt(winA,2)+' m2)'],
        ['Wall area net', WCfmt(wallNet,2)+' m2'],
        ['Ceiling', i.ceiling ? WCfmt(ceil,2)+' m2' : 'not included'],
        ['Area per coat', WCfmt(paintArea,2)+' m2 / '+WCfmt(paintArea/0.09290304,2)+' ft2'],
        ['Extra allowance', WCfmt(i.allowance,1)+'%'],
        ['Colour before allowance', WCfmt(baseLitres,2)+' L'],
        ['Colour needed', WCfmt(litres,2)+' L / '+WCfmt(litres/3.785411784,2)+' US gal'],
        ['Tins of colour', String(tins)+' x '+i.tin+' L'],
        ['Primer needed', i.primer ? WCfmt(primerL,2)+' L / '+WCfmt(primerL/3.785411784,2)+' US gal' + ' ('+primerTins+' x '+i.primerTin+' L tins)' : 'none']
      ]}]
    };
  },
  diagram: function (r,i){
    var W=560,H=210,s=SVG.open(W,H),m=40;
    var k=i.unit==='in'?0.0254:0.001, L=i.len*k, Wd=i.wid*k, Hh=i.hgt*k;
    var sc=Math.min((W-2*m)/(L+Wd), (H-70)/Hh);
    var x=m,y=44,h=Hh*sc;
    s+=SVG.rect(x,y,L*sc,h,'part'); s+=SVG.text(x+L*sc/2,y+h/2,'wall '+WCfmt(L,2)+' m',11);
    x+=L*sc+8;
    s+=SVG.rect(x,y,Wd*sc,h,'part'); s+=SVG.text(x+Wd*sc/2,y+h/2,'wall '+WCfmt(Wd,2)+' m',11);
    s+=SVG.text(W/2,26,'Two of each wall, '+WCfmt(Hh,2)+' m high',12);
    s+=SVG.text(W/2,H-14, WCfmt(r.paintArea,1)+' m2 per coat  -  '+WCfmt(r.litres,1)+' L  -  '+r.tins+' tins',12);
    return s+SVG.close();
  }
};
"""
}
