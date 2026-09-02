SPEC = {
"slug":"metal-weight-calculator",
"h1":"Metal Weight Calculator",
"title_tag":"Metal Weight Calculator — Bar, Tube, Sheet and Angle in Steel, Aluminium, Brass",
"description":"Weight of round bar, square bar, tube, sheet, plate and angle in steel, stainless, aluminium, brass and copper, with total weight and price.",
"card_desc":"Weight of bar, tube, sheet and angle in any common metal, with totals and cost.",
"category":"Sheet goods",
"intro":"Before you order it, before you lift it, before you work out what the trailer can carry. Choose the shape and the metal, enter the dimensions, and get the weight per metre, the total, and the cost if you know the rate.",
"notes":[("Where the densities come from","These are standard handbook densities in kg per cubic metre: mild steel 7850, stainless 8000, aluminium 2700, brass 8500, copper 8960, cast iron 7200, lead 11340. Alloys vary by a percent or two, which is well inside the tolerance of the stock itself."),
("Tube weight is the difference of two cylinders","A tube weighs the same as the solid bar of its outside diameter minus the bar of its bore. Which is why doubling the wall thickness of a thin tube nearly doubles its weight, but barely changes the outside size."),
("Why the merchant weight differs","Rolling tolerances, mill scale and paint all add a little. Structural sections are also sold to nominal sizes that are not quite the real ones. Expect a couple of percent either way."),
("What this does not do","It weighs geometry. It does not check whether a section is strong enough, which depends on span, load and how it is fixed.")],
"js":"""
var SPEC = {
  fields: [
    {id:'shape', label:'Shape', type:'select', value:'round', group:'Section', options:[
      {value:'round', label:'Round bar'},
      {value:'square', label:'Square bar'},
      {value:'flat', label:'Flat bar / plate'},
      {value:'tube', label:'Round tube'},
      {value:'sqtube', label:'Square tube'},
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
    {id:'d1', label:'Diameter / width', value:25, unit:'length', group:'Dimensions', min:0},
    {id:'d2', label:'Height / second side', value:25, unit:'length', group:'Dimensions', min:0,
     hint:'Flat bar, square tube, sheet'},
    {id:'wall', label:'Wall / leg thickness', value:2, unit:'length', group:'Dimensions', min:0, hint:'Tubes and angle'},
    {id:'len', label:'Length', value:1000, unit:'length', group:'Dimensions', min:0},
    {id:'qty', label:'How many pieces', value:1, group:'Dimensions', min:1, step:1},
    {id:'price', label:'Price per kg', value:0, group:'Cost', min:0, hint:'In whatever currency you buy in. 0 to skip the cost.'}
  ],
  compute: function (i) {
    var DENS = {steel:7850, stainless:8000, alu:2700, brass:8500, copper:8960, castiron:7200, lead:11340};
    var MNAME = {steel:'Mild steel', stainless:'Stainless', alu:'Aluminium', brass:'Brass',
                 copper:'Copper', castiron:'Cast iron', lead:'Lead'};
    var rho = DENS[i.metal];
    var k = i.unit === 'in' ? 0.0254 : 0.001;
    var d1=i.d1*k, d2=i.d2*k, wall=i.wall*k, L=i.len*k;
    if (!(L>0)) return {ok:false, errors:['Length must be greater than zero.']};

    var area, label;
    if (i.shape==='round')      { if(!(d1>0)) return {ok:false,errors:['Diameter must be greater than zero.']};
                                  area=Math.PI*d1*d1/4; label='Round bar \u00d8'+WCfmt(i.d1,1); }
    else if (i.shape==='square'){ if(!(d1>0)) return {ok:false,errors:['Side must be greater than zero.']};
                                  area=d1*d1; label='Square bar '+WCfmt(i.d1,1); }
    else if (i.shape==='flat' || i.shape==='sheet') {
                                  if(!(d1>0 && d2>0)) return {ok:false,errors:['Both dimensions must be greater than zero.']};
                                  area=d1*d2; label=(i.shape==='sheet'?'Sheet ':'Flat bar ')+WCfmt(i.d1,1)+' \u00d7 '+WCfmt(i.d2,1); }
    else if (i.shape==='tube')  { if(!(d1>0)) return {ok:false,errors:['Outside diameter must be greater than zero.']};
                                  if(!(wall>0)) return {ok:false,errors:['Wall thickness must be greater than zero.']};
                                  if(2*wall>=d1) return {ok:false,errors:['The wall is thicker than the radius \u2014 that is solid bar.']};
                                  var bore=d1-2*wall; area=Math.PI*(d1*d1-bore*bore)/4;
                                  label='Tube \u00d8'+WCfmt(i.d1,1)+' \u00d7 '+WCfmt(i.wall,1)+' wall'; }
    else if (i.shape==='angle') { if(!(d1>0 && d2>0)) return {ok:false,errors:['Both legs must be greater than zero.']};
                                  if(!(wall>0)) return {ok:false,errors:['Leg thickness must be greater than zero.']};
                                  if(wall>=Math.min(d1,d2)) return {ok:false,errors:['The leg thickness is larger than the leg \u2014 that is solid bar.']};
                                  // Deux ailes qui se recouvrent sur un carre d'epaisseur : on ne le compte qu'une fois.
                                  area=wall*(d1+d2-wall);
                                  label='Angle '+WCfmt(i.d1,1)+' \u00d7 '+WCfmt(i.d2,1)+' \u00d7 '+WCfmt(i.wall,1); }
    else                        { if(!(d1>0 && d2>0)) return {ok:false,errors:['Both sides must be greater than zero.']};
                                  if(!(wall>0)) return {ok:false,errors:['Wall thickness must be greater than zero.']};
                                  if(2*wall>=Math.min(d1,d2)) return {ok:false,errors:['The wall is too thick for that section.']};
                                  area=d1*d2-(d1-2*wall)*(d2-2*wall);
                                  label='Square tube '+WCfmt(i.d1,1)+' \u00d7 '+WCfmt(i.d2,1)+' \u00d7 '+WCfmt(i.wall,1); }

    var kgPerM = area*rho;
    var each = kgPerM*L;
    var n = Math.max(1, Math.round(i.qty));
    var total = each*n;
    var cost = i.price>0 ? total*i.price : null;

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
        ['Metal', (MNAME[i.metal]||i.metal)+' at '+WCfmt(rho,0)+' kg/m3'],
        ['Cross-section area', WCfmt(area*1e6,2)+' mm2'],
        ['Weight per metre', WCfmt(kgPerM,4)+' kg/m'],
        ['Length each', WCfmt(L,3)+' m'],
        ['Weight each', WCfmt(each,4)+' kg'],
        ['Pieces', String(n)],
        ['Total weight', WCfmt(total,3)+' kg  ('+WCfmt(total*2.20462,1)+' lb)'],
        ['Cost', cost !== null ? WCfmt(cost,2) : '\u2014']
      ]}],
      note:'Densities are standard handbook figures. Real stock varies a percent or two with alloy, rolling tolerance and finish.'
    };
  },
  diagram: function (r, i) {
    var W=520,H=250,cx=W/2,cy=120,s=SVG.open(W,H);
    if (i.shape==='round'){ s+='<circle cx="'+cx+'" cy="'+cy+'" r="62" class="part"/>'; }
    else if (i.shape==='tube'){ s+='<circle cx="'+cx+'" cy="'+cy+'" r="62" class="part"/>';
      var br=62*Math.max(0.1,(i.d1-2*i.wall)/Math.max(i.d1,1));
      s+='<circle cx="'+cx+'" cy="'+cy+'" r="'+br+'" fill="var(--surface)" stroke="var(--accent)" stroke-width="1.5"/>'; }
    else if (i.shape==='sqtube'){ s+=SVG.rect(cx-62,cy-52,124,104,'part');
      var w=62*Math.max(0.1,(i.d1-2*i.wall)/Math.max(i.d1,1));
      s+='<rect x="'+(cx-w)+'" y="'+(cy-w*0.84)+'" width="'+(2*w)+'" height="'+(2*w*0.84)+'" fill="var(--surface)" stroke="var(--accent)" stroke-width="1.5"/>'; }
    else if (i.shape==='square'){ s+=SVG.rect(cx-55,cy-55,110,110,'part'); }
    else if (i.shape==='angle'){
      var aw=Math.max(6,62*Math.max(0.08,i.wall/Math.max(i.d1,1)));
      s+='<path d="M'+(cx-62)+' '+(cy-62)+' h'+aw+' v'+(124-aw)+' h'+(124-aw)+' v'+aw+' h-124 z" class="part"/>'; }
    else { s+=SVG.rect(cx-95,cy-32,190,64,'part'); }
    s+=SVG.text(cx,cy+4,WCfmt(r.kgPerM,2)+' kg/m',13);
    s+=SVG.text(cx,26,r.label,13);
    s+=SVG.text(cx,H-16,WCfmt(r.total,2)+' kg in total',12);
    return s+SVG.close();
  }
};
"""}
