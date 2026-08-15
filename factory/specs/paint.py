SPEC = {
"slug":"paint-coverage-calculator",
"h1":"Paint Coverage Calculator",
"title_tag":"Paint Calculator — Litres and Gallons by Room, Coats and Openings",
"description":"Paint quantity for walls and ceiling, with doors and windows subtracted, primer included, and the number of tins to buy rather than a raw litre figure.",
"card_desc":"Litres or gallons per coat with openings subtracted, rounded up to real tin sizes.",
"category":"Finishing",
"intro":"Most paint calculators give you a litre figure you cannot buy. This one subtracts your doors and windows, allows for coats and primer, and tells you how many tins to actually put in the trolley.",
"notes":[("Why coverage varies so much","A smooth sealed wall takes far less than bare plaster, new render or a porous masonry block. The tin quotes the best case; the first coat on new work can drink half again as much."),
("Do I subtract openings?","Below about 10% of the wall area it makes little difference and the extra is useful. Above that, on a room with patio doors, ignoring it means buying a tin you do not need."),
("Two coats is not optional","Any colour change needs two, and one coat over primer will look patchy in raking light however good the paint is."),
("What this does not do","It does not judge whether you need primer. Bare plaster, new timber, stains and strong colour changes do; sound painted walls in a similar shade usually do not.")],
"js":"""
var SPEC = {
  fields: [
    {id:'len', label:'Room length', value:5000, unit:'length', group:'Room', min:0},
    {id:'wid', label:'Room width', value:4000, unit:'length', group:'Room', min:0},
    {id:'hgt', label:'Wall height', value:2400, unit:'length', group:'Room', min:0},
    {id:'ceiling', label:'Include the ceiling', type:'check', value:false, group:'Room'},
    {id:'doors', label:'Number of doors', value:1, group:'Openings', min:0, step:1, hint:'Assumed 2.0 x 0.9 m'},
    {id:'windows', label:'Number of windows', value:2, group:'Openings', min:0, step:1, hint:'Assumed 1.2 x 1.2 m'},
    {id:'coats', label:'Coats', value:2, group:'Paint', min:1, step:1},
    {id:'primer', label:'Add a primer coat', type:'check', value:false, group:'Paint'},
    {id:'cover', label:'Coverage per litre (m2)', value:11, group:'Paint', min:1, hint:'10-12 typical, 6-8 on bare plaster'},
    {id:'tin', label:'Tin size (litres)', value:2.5, group:'Paint', min:0.1}
  ],
  compute: function (i) {
    var k = i.unit === 'in' ? 0.0254 : 0.001;
    var L=i.len*k, W=i.wid*k, H=i.hgt*k;
    if (!(L>0&&W>0&&H>0)) return {ok:false, errors:['Room length, width and height must all be greater than zero.']};
    if (!(i.cover>0)) return {ok:false, errors:['Coverage per litre must be greater than zero.']};

    var wallGross = 2*(L+W)*H;
    var ceil = i.ceiling ? L*W : 0;
    var doorA = Math.max(0,i.doors)*2.0*0.9;
    var winA  = Math.max(0,i.windows)*1.2*1.2;
    var openings = doorA+winA;
    if (openings >= wallGross) return {ok:false, errors:['The doors and windows add up to more than the wall area — check the counts.']};

    var wallNet = wallGross-openings;
    var paintArea = wallNet+ceil;
    var coats = Math.max(1, Math.round(i.coats));
    var totalCoats = coats + (i.primer?1:0);
    var litres = paintArea*coats/i.cover;
    var primerL = i.primer ? paintArea/i.cover : 0;
    var tins = Math.ceil(litres/i.tin);
    var primerTins = i.primer ? Math.ceil(primerL/i.tin) : 0;
    var pctOpen = 100*openings/wallGross;

    var warn=[];
    if (pctOpen>25) warn.push('Openings are '+WCfmt(pctOpen,0)+'% of the wall area — worth measuring them properly rather than using the standard sizes.');
    if (i.cover>13) warn.push('Coverage above 13 m2 per litre is optimistic for anything but a sealed, previously painted wall.');

    return {ok:true, litres:litres, tins:tins, paintArea:paintArea, warnings:warn,
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
        ['Area per coat', WCfmt(paintArea,2)+' m2'],
        ['Colour needed', WCfmt(litres,2)+' L / '+WCfmt(litres*0.264,2)+' US gal'],
        ['Tins of colour', String(tins)+' x '+i.tin+' L'],
        ['Primer needed', i.primer ? WCfmt(primerL,2)+' L ('+primerTins+' tins)' : 'none']
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
"""}
