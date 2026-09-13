SPEC = {
'slug': 'metal-weight-calculator',
'h1': 'Metal Weight Calculator',
'title_tag': 'Metal Weight Calculator — Bar, Tube, Sheet and Angle in Steel, Aluminium, Brass',
'description': 'Weight of round bar, square bar, tube, sheet, plate and angle in steel, stainless, aluminium, brass and copper, with total weight and price.',
'card_desc': 'Weight of bar, tube, sheet and angle in any common metal, with totals and cost.',
'category': 'Sheet goods',
'intro': 'Estimate mass from a metal section, length and piece count. Use the preset density or enter the exact alloy density, then compare the result with your supplier mass table.',
'notes': [('How is metal weight calculated?', 'Cross-section area x length x density gives mass. With dimensions converted to metres and density in kg/m3, the result is kilograms. Multiply by the whole-number piece count for the total.'), ('Which density should I use?', 'The metal presets are approximate starting values, not specifications for every alloy. Enter the density from your alloy data sheet in the custom field when you have it. For example, the Copper Development Association lists C26000 brass specific gravity as 8.53, corresponding to approximately 8530 kg/m3.'), ('How do hollow sections work?', 'Round tube area is pi/4 x (outside diameter squared - inside diameter squared). Rectangular tube area is outer width x outer height minus the inner rectangle. The wall thickness is removed from both sides of each inside dimension.'), ('Why can supplier weights differ?', 'This calculator uses ideal sharp corners. Real tube corner radii, angle fillets, seams, dimensional tolerances, finishes and alloy density can change the actual mass. Use the supplier section table when those details matter; no fixed accuracy percentage is promised.'), ('What does the drawing show?', 'The cross-section keeps the proportions of your entered dimensions. Sheet and flat bar use width and thickness; rectangular tube uses outside width and height; angle uses both outside leg lengths. Very thin sections may be difficult to see at screen scale.'), ('Does this check strength or lifting capacity?', 'No. This estimates material mass only. Section strength and equipment capacity require their own specifications and checks.')],
"js": """
var SPEC = {
  fields: [
    {id:'shape', label:'Shape', type:'select', value:'round', group:'Section', options:[
      {value:'round', label:'Round bar'},
      {value:'square', label:'Square bar'},
      {value:'flat', label:'Flat bar / plate'},
      {value:'tube', label:'Round tube'},
      {value:'sqtube', label:'Rectangular / square tube'},
      {value:'sheet', label:'Sheet'},
      {value:'angle', label:'Angle / L-section'}]},
    {id:'metal', label:'Metal', type:'select', value:'steel', group:'Section', options:[
      {value:'steel', label:'Mild steel (7850)'},
      {value:'stainless', label:'Stainless (8000)'},
      {value:'alu', label:'Aluminium (2700)'},
      {value:'brass', label:'Brass (8500)'},
      {value:'copper', label:'Copper (8960)'},
      {value:'castiron', label:'Cast iron (7200)'},
      {value:'lead', label:'Lead (11340)'}]},
    {id:'density', label:'Custom density (kg/m3)', value:0, group:'Section', min:0, hint:'0 uses the selected metal estimate. Enter your alloy data sheet value to override it.'},
    {id:'d1', label:'Diameter / width', value:25, unit:'length', group:'Dimensions', min:0},
    {id:'d2', label:'Thickness / height / second leg', value:25, unit:'length', group:'Dimensions', min:0,
     hint:'Thickness for sheet/flat bar; outer height for tube; second leg for angle'},
    {id:'wall', label:'Wall / leg thickness', value:2, unit:'length', group:'Dimensions', min:0, hint:'Tubes and angle'},
    {id:'len', label:'Length', value:1000, unit:'length', group:'Dimensions', min:0},
    {id:'qty', label:'How many pieces', value:1, group:'Dimensions', min:1, step:1},
    {id:'price', label:'Price per kg', value:0, group:'Cost', min:0, hint:'In whatever currency you buy in. 0 to skip the cost.'}
  ],
  compute: function (i) {
    var DENS = {steel:7850, stainless:8000, alu:2700, brass:8500, copper:8960, castiron:7200, lead:11340};
    var MNAME = {steel:'Mild steel', stainless:'Stainless', alu:'Aluminium', brass:'Brass',
                 copper:'Copper', castiron:'Cast iron', lead:'Lead'};
    if (!Object.prototype.hasOwnProperty.call(DENS,i.metal) || ['round','square','flat','tube','sqtube','sheet','angle'].indexOf(i.shape)<0)
      return {ok:false,errors:['Choose a listed metal and section shape.']};
    if (!Number.isFinite(i.density)||i.density<0 || !Number.isFinite(i.price)||i.price<0)
      return {ok:false,errors:['Density override and price must be finite numbers, zero or greater.']};
    if (!Number.isSafeInteger(i.qty)||i.qty<1)
      return {ok:false,errors:['Piece count must be a positive whole number.']};
    var required=['d1','len'];
    if (['flat','sheet','sqtube','angle'].indexOf(i.shape)>=0) required.push('d2');
    if (['tube','sqtube','angle'].indexOf(i.shape)>=0) required.push('wall');
    if (required.some(function(key){return !Number.isFinite(i[key])||i[key]<=0;}))
      return {ok:false,errors:['Enter positive finite dimensions for the selected section.']};
    var rho = i.density>0?i.density:DENS[i.metal];
    var k = i.unit === 'in' ? 0.0254 : 0.001;
    var d1=i.d1*k, d2=i.d2*k, wall=i.wall*k, L=i.len*k;
    if (!(L>0)) return {ok:false, errors:['Length must be greater than zero.']};

    var area, label;
    if (i.shape==='round')      { if(!(d1>0)) return {ok:false,errors:['Diameter must be greater than zero.']};
                                  area=Math.PI*d1*d1/4; label='Round bar Ø'+WCfmt(i.d1,1); }
    else if (i.shape==='square'){ if(!(d1>0)) return {ok:false,errors:['Side must be greater than zero.']};
                                  area=d1*d1; label='Square bar '+WCfmt(i.d1,1); }
    else if (i.shape==='flat' || i.shape==='sheet') {
                                  if(!(d1>0 && d2>0)) return {ok:false,errors:['Both dimensions must be greater than zero.']};
                                  area=d1*d2; label=(i.shape==='sheet'?'Sheet ':'Flat bar ')+WCfmt(i.d1,1)+' × '+WCfmt(i.d2,1); }
    else if (i.shape==='tube')  { if(!(d1>0)) return {ok:false,errors:['Outside diameter must be greater than zero.']};
                                  if(!(wall>0)) return {ok:false,errors:['Wall thickness must be greater than zero.']};
                                  if(2*wall>=d1) return {ok:false,errors:['The wall is thicker than the radius — that is solid bar.']};
                                  var bore=d1-2*wall; area=Math.PI*(d1*d1-bore*bore)/4;
                                  label='Tube Ø'+WCfmt(i.d1,1)+' × '+WCfmt(i.wall,1)+' wall'; }
    else if (i.shape==='angle') { if(!(d1>0 && d2>0)) return {ok:false,errors:['Both legs must be greater than zero.']};
                                  if(!(wall>0)) return {ok:false,errors:['Leg thickness must be greater than zero.']};
                                  if(wall>=Math.min(d1,d2)) return {ok:false,errors:['The leg thickness is larger than the leg — that is solid bar.']};
                                  // Deux ailes qui se recouvrent sur un carre d'epaisseur : on ne le compte qu'une fois.
                                  area=wall*(d1+d2-wall);
                                  label='Angle '+WCfmt(i.d1,1)+' × '+WCfmt(i.d2,1)+' × '+WCfmt(i.wall,1); }
    else                        { if(!(d1>0 && d2>0)) return {ok:false,errors:['Both sides must be greater than zero.']};
                                  if(!(wall>0)) return {ok:false,errors:['Wall thickness must be greater than zero.']};
                                  if(2*wall>=Math.min(d1,d2)) return {ok:false,errors:['The wall is too thick for that section.']};
                                  area=d1*d2-(d1-2*wall)*(d2-2*wall);
                                  label='Rectangular tube '+WCfmt(i.d1,1)+' × '+WCfmt(i.d2,1)+' × '+WCfmt(i.wall,1); }

    var kgPerM = area*rho;
    var each = kgPerM*L;
    var n = i.qty;
    var total = each*n;
    var cost = i.price>0 ? total*i.price : null;

    if (![area,kgPerM,each,total].every(function(v){return Number.isFinite(v)&&v>0;}) || (cost!==null&&!Number.isFinite(cost)))
      return {ok:false,errors:['These dimensions or quantities exceed the calculation range.']};
    label += i.unit==='in'?' in':' mm';
    var stats = [
      {value: WCfmt(each,3), label:'kg each'},
      {value: WCfmt(total,2), label:'kg total'},
      {value: WCfmt(kgPerM,3), label:'kg per metre'},
      {value: String(n), label:'Pieces'}
    ];
    if (cost !== null) stats.push({value:WCfmt(cost,2), label:'Estimated cost'});

    return {ok:true, each:each, total:total, kgPerM:kgPerM, label:label, area:area, rho:rho,
      stats: stats,
      tables:[{title:'Working', head:['Item','Value'], rows:[
        ['Section', label],
        ['Metal', (i.density>0?'Custom density':MNAME[i.metal])+' at '+WCfmt(rho,0)+' kg/m3'],
        ['Cross-section area', WCfmt(area*1e6,2)+' mm2'],
        ['Weight per metre', WCfmt(kgPerM,4)+' kg/m'],
        ['Length each', WCfmt(L,3)+' m'],
        ['Weight each', WCfmt(each,4)+' kg'],
        ['Pieces', String(n)],
        ['Total weight', WCfmt(total,3)+' kg  ('+WCfmt(total*2.20462,1)+' lb)'],
        ['Cost', cost !== null ? WCfmt(cost,2) : '—']
      ]}],
      note:'Ideal geometry estimate: corners are sharp; fillets, corner radii, seams and coatings are excluded. Use the supplier mass table for actual stock and lifting or transport decisions.'
    };
  },
  diagram: function (r, i) {
    var W=520,H=290,cx=W/2,cy=139,s=SVG.open(W,H);
    var round=i.shape==='round'||i.shape==='tube';
    var outerH=(round||i.shape==='square')?i.d1:i.d2;
    var scale=Math.min(310/i.d1,150/outerH);
    var w=i.d1*scale,h=outerH*scale,t=i.wall*scale,x=cx-w/2,y=cy-h/2;
    if (round) {
      s+='<circle cx="'+cx+'" cy="'+cy+'" r="'+w/2+'" class="part"/>';
      if(i.shape==='tube')s+='<circle cx="'+cx+'" cy="'+cy+'" r="'+((i.d1-2*i.wall)*scale/2)+'" fill="var(--surface)" stroke="var(--accent)" stroke-width="1.5"/>';
    } else if (i.shape==='angle') {
      s+='<path d="M'+x+' '+y+' h'+t+' v'+(h-t)+' h'+(w-t)+' v'+t+' h-'+w+' z" class="part"/>';
    } else {
      s+=SVG.rect(x,y,w,h,'part');
      if(i.shape==='sqtube')s+='<rect x="'+(x+t)+'" y="'+(y+t)+'" width="'+(w-2*t)+'" height="'+(h-2*t)+'" fill="var(--surface)" stroke="var(--accent)" stroke-width="1.5"/>';
    }
    s+=SVG.text(cx,26,r.label,12);
    s+=SVG.text(cx,239,WCfmt(r.kgPerM,3)+' kg/m  |  '+WCfmt(r.total,3)+' kg total',12);
    s+=SVG.text(cx,274,'Section proportions shown; ideal sharp corners',11);
    return s+SVG.close();
  }
};
"""
}
