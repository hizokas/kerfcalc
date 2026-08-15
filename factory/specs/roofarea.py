SPEC = {
"slug":"roof-area-calculator",
"h1":"Roof Area & Material Calculator",
"title_tag":"Roof Area Calculator — Sloped Area, Squares, Bundles and Underlayment",
"description":"True sloped roof area from the footprint and pitch, in squares and square metres, with bundle counts, ridge and hip lengths, and waste allowance.",
"card_desc":"True sloped area from footprint and pitch, with squares, bundles, ridge and hip lengths.",
"category":"Framing",
"intro":"The footprint is not the roof. A 6:12 pitch adds about 12% to the area and a 12:12 adds 41%, which is the difference between ordering enough and going back to the merchant. Enter the plan size and the pitch, get the real surface.",
"notes":[("Where the slope factor comes from","It is the hypotenuse over the run: for a rise of R in 12, the factor is sqrt(12*12 + R*R) / 12. A 6:12 works out at 1.118, so every square metre of footprint is 1.118 square metres of roof."),
("What a square is","A roofing square is 100 square feet, or about 9.29 square metres. Shingles are sold by the bundle, typically three bundles to the square, but check the wrapper because it varies."),
("Waste allowance","10% is normal on a simple gable. Hips, valleys, dormers and anything cut on the rake push it to 15% or more, because every cut piece leaves an offcut you cannot use."),
("What this does not do","It does not size structure, and it does not account for the specific coursing of your material. Complex roofs should be measured plane by plane.")],
"js":"""
var SPEC = {
  fields: [
    {id:'a', label:'Footprint length', value:12000, unit:'length', group:'Roof', min:0},
    {id:'b', label:'Footprint width', value:8000, unit:'length', group:'Roof', min:0},
    {id:'pitch', label:'Pitch, rise in 12', value:6, group:'Roof', min:0, hint:'6 means 6:12'},
    {id:'shape', label:'Roof shape', type:'select', value:'gable', group:'Roof', options:[
      {value:'gable', label:'Simple gable'},
      {value:'hip', label:'Hip roof'}]},
    {id:'overhang', label:'Eaves overhang', value:400, unit:'length', group:'Roof', min:0},
    {id:'waste', label:'Waste allowance (%)', value:10, group:'Materials', min:0},
    {id:'perBundle', label:'Coverage per bundle (m2)', value:3.1, group:'Materials', min:0.1, hint:'3.1 m2 is typical'}
  ],
  compute: function (i) {
    var k=i.unit==='in'?0.0254:0.001;
    var A=i.a*k+2*i.overhang*k, B=i.b*k+2*i.overhang*k;
    if(!(A>0&&B>0)) return {ok:false, errors:['Footprint length and width must be greater than zero.']};
    if(i.pitch<0) return {ok:false, errors:['Pitch cannot be negative.']};

    var slope=Math.sqrt(144+i.pitch*i.pitch)/12;
    var deg=Math.atan(i.pitch/12)*180/Math.PI;
    var footprint=A*B;
    var area=footprint*slope;
    var withWaste=area*(1+Math.max(0,i.waste)/100);
    var squares=withWaste/9.2903;
    var bundles=Math.ceil(withWaste/i.perBundle);

    var ridge, hips=0;
    if (i.shape==='gable'){ ridge=A; }
    else { var shorter=Math.min(A,B); ridge=Math.abs(A-B);
           var hipRun=Math.sqrt(Math.pow(shorter/2,2)+Math.pow(shorter/2,2));
           hips=4*Math.sqrt(Math.pow(hipRun,2)+Math.pow((shorter/2)*(i.pitch/12),2)); }

    return {ok:true, area:area, withWaste:withWaste, slope:slope, deg:deg, ridge:ridge, hips:hips, A:A, B:B,
      stats:[
        {value:WCfmt(area,1), label:'m2 of roof'},
        {value:WCfmt(squares,1), label:'Squares to order'},
        {value:String(bundles), label:'Bundles'},
        {value:WCfmt(slope,3), label:'Slope factor'}
      ],
      tables:[{title:'Breakdown', head:['Item','Value'], rows:[
        ['Footprint incl. overhang', WCfmt(A,2)+' x '+WCfmt(B,2)+' m = '+WCfmt(footprint,1)+' m2'],
        ['Pitch', i.pitch+':12 = '+WCfmt(deg,2)+' degrees'],
        ['Slope factor', WCfmt(slope,4)+' (adds '+WCfmt((slope-1)*100,1)+'%)'],
        ['True roof area', WCfmt(area,2)+' m2 / '+WCfmt(area*10.7639,0)+' ft2'],
        ['With '+WCfmt(i.waste,0)+'% waste', WCfmt(withWaste,2)+' m2'],
        ['Roofing squares', WCfmt(squares,2)],
        ['Bundles at '+i.perBundle+' m2', String(bundles)],
        ['Ridge length', WCfmt(ridge,2)+' m'],
        ['Hip length total', i.shape==='hip'?WCfmt(hips,2)+' m':'not a hip roof']
      ]}]
    };
  },
  diagram: function (r,i){
    var W=560,H=230,s=SVG.open(W,H),m=50;
    var run=(W-2*m)/2, rise=run*(i.pitch/12);
    rise=Math.min(rise,110);
    var baseY=H-52, apexY=baseY-rise;
    s+=SVG.poly([[m,baseY],[W/2,apexY],[W-m,baseY]],'part');
    s+=SVG.line(m,baseY,W-m,baseY,' class="dim"');
    s+=SVG.text(W/2,baseY+22,'span '+WCfmt(r.B,2)+' m',11);
    s+=SVG.text(W/2,apexY-12, i.pitch+':12  ('+WCfmt(r.deg,1)+' deg)',12);
    s+=SVG.text(W/2,26,'Slope factor '+WCfmt(r.slope,3)+' - footprint x '+WCfmt(r.slope,3)+' = real area',12);
    s+=SVG.text(W/2,H-16, WCfmt(r.area,1)+' m2 of roof, '+WCfmt(r.withWaste,1)+' m2 to order',12);
    return s+SVG.close();
  }
};
"""}
