SPEC = {
"slug":"grout-calculator",
"h1":"Grout &amp; Adhesive Calculator",
"title_tag":"Grout Calculator — Kilograms of Grout and Adhesive for Any Tile Size",
"description":"Grout volume and weight from tile size, joint width and joint depth, plus tile adhesive by trowel notch, with bags to buy.",
"card_desc":"Grout and adhesive by weight from tile size, joint width and trowel notch, with bags to buy.",
"category":"Finishing",
"intro":"Grout is sold in bags and used by the joint. Small tiles with wide joints can need five times the grout of large-format tiles in the same room, which is why one bag is never the answer. Enter your tile and joint and get the real figure.",
"notes":[("Where the volume comes from","Per square metre, the joints form a grid. The grout volume is the joint width times the joint depth times the total joint length, and the joint length depends entirely on tile size \u2014 which is why small tiles drink grout."),
("Joint depth is usually the tile thickness","Grout normally fills the full depth of the tile. If you are grouting over an uneven bed or the adhesive has squeezed up into the joints, the effective depth is less and you will use less."),
("Adhesive by notch","Trowel notch size sets the bed thickness, roughly: 6 mm notch about 3 kg per square metre, 10 mm about 5, 12 mm about 6.5. Back-buttering large tiles roughly doubles it. Manufacturer figures beat these."),
("What this does not do","It does not choose a grout or adhesive for your situation. Wet areas, underfloor heating, movement joints and porous tiles all change the specification.")],
"js":"""
var SPEC = {
  fields: [
    {id:'area', label:'Area to tile (m2)', value:20, group:'Area', min:0},
    {id:'tileL', label:'Tile length', value:600, unit:'length', group:'Tile', min:0},
    {id:'tileW', label:'Tile width', value:300, unit:'length', group:'Tile', min:0},
    {id:'joint', label:'Joint width', value:3, unit:'length', group:'Tile', min:0},
    {id:'depth', label:'Joint depth', value:10, unit:'length', group:'Tile', min:0,
     hint:'Usually the tile thickness'},
    {id:'notch', label:'Trowel notch', type:'select', value:'10', group:'Adhesive', options:[
      {value:'6', label:'6 mm notch'},
      {value:'8', label:'8 mm notch'},
      {value:'10', label:'10 mm notch'},
      {value:'12', label:'12 mm notch'}]},
    {id:'butter', label:'Back-buttering large tiles', type:'check', value:false, group:'Adhesive'},
    {id:'grNext', label:'Grout bag size (kg)', value:5, group:'Ordering', min:0.5},
    {id:'adBag', label:'Adhesive bag size (kg)', value:20, group:'Ordering', min:1},
    {id:'waste', label:'Waste allowance (%)', value:10, group:'Ordering', min:0}
  ],
  compute: function (i) {
    var k = i.unit === 'in' ? 25.4 : 1;
    var tl=i.tileL*k, tw=i.tileW*k, j=i.joint*k, d=i.depth*k;   // en mm
    if (!(i.area>0)) return {ok:false, errors:['The area must be greater than zero.']};
    if (!(tl>0 && tw>0)) return {ok:false, errors:['Tile dimensions must be greater than zero.']};
    if (!(j>0)) return {ok:false, errors:['Joint width must be greater than zero.']};

    // Volume de joint par m2 : (L+W)/(L x W) x largeur x profondeur, en mm3 par mm2
    var perM2mm3 = ((tl+tw)/(tl*tw))*j*d*1e6;      // mm3 par m2
    var litresPerM2 = perM2mm3/1e6;                 // 1 litre = 1e6 mm3
    var grKgPerM2 = litresPerM2*1.6;                // densite du coulis ~1.6 kg/l
    var grTotal = grKgPerM2*i.area*(1+Math.max(0,i.waste)/100);
    var grBags = Math.ceil(grTotal/Math.max(0.5,i.grNext));

    var NOTCH={'6':3,'8':4,'10':5,'12':6.5};
    var adPerM2 = NOTCH[i.notch]*(i.butter?1.9:1);
    var adTotal = adPerM2*i.area*(1+Math.max(0,i.waste)/100);
    var adBags = Math.ceil(adTotal/Math.max(1,i.adBag));

    var warn=[];
    if (grKgPerM2 > 2) warn.push('At '+WCfmt(grKgPerM2,2)+' kg per m2 this is a grout-hungry combination \u2014 small tiles with wide joints. Worth double-checking the joint width.');

    return {ok:true, grKgPerM2:grKgPerM2, grTotal:grTotal, grBags:grBags,
      adPerM2:adPerM2, adTotal:adTotal, adBags:adBags, area:i.area,
      warnings: warn,
      stats:[
        {value: WCfmt(grTotal,1), label:'kg of grout'},
        {value: String(grBags), label:'Grout bags'},
        {value: WCfmt(adTotal,0), label:'kg of adhesive'},
        {value: String(adBags), label:'Adhesive bags'}
      ],
      tables:[{title:'Working', head:['Item','Value'], rows:[
        ['Area', WCfmt(i.area,2)+' m2'],
        ['Tile', WCfmt(i.tileL,0)+' \u00d7 '+WCfmt(i.tileW,0)],
        ['Joint', WCfmt(i.joint,1)+' wide \u00d7 '+WCfmt(i.depth,1)+' deep'],
        ['Grout per m2', WCfmt(grKgPerM2,3)+' kg  ('+WCfmt(litresPerM2,3)+' litres)'],
        ['Grout total incl. waste', WCfmt(grTotal,2)+' kg'],
        ['Bags of '+WCfmt(i.grNext,1)+' kg', String(grBags)],
        ['Adhesive per m2', WCfmt(adPerM2,1)+' kg  ('+i.notch+' mm notch'+(i.butter?', back-buttered':'')+')'],
        ['Adhesive total incl. waste', WCfmt(adTotal,1)+' kg'],
        ['Bags of '+WCfmt(i.adBag,0)+' kg', String(adBags)]
      ]}],
      note:'Grout volume comes from the geometry of your joints. Adhesive figures are typical coverages by notch size \u2014 the bag always beats a calculator.'
    };
  },
  diagram: function (r, i) {
    var W=560,H=280,m=45,s=SVG.open(W,H);
    var cols=5, rows=3, gw=(W-2*m)/cols, gh=140/rows;
    var jw=Math.max(2, Math.min(10, i.joint*1.6));
    for(var a=0;a<cols;a++) for(var b=0;b<rows;b++)
      s+=SVG.rect(m+a*gw+jw/2, 70+b*gh+jw/2, gw-jw, gh-jw, 'part');
    s+=SVG.text(W/2,34, WCfmt(r.grKgPerM2,2)+' kg of grout per m2', 14);
    s+=SVG.text(W/2,H-16, WCfmt(r.grTotal,1)+' kg total  \u00b7  '+r.grBags+' bags  \u00b7  adhesive '+WCfmt(r.adTotal,0)+' kg', 12);
    return s+SVG.close();
  }
};
"""}
