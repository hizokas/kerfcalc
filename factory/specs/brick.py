SPEC = {
"slug":"brick-block-calculator",
"h1":"Brick &amp; Block Quantity Calculator",
"title_tag":"Brick Calculator — Bricks per Square Metre, Mortar Volume, Sand and Cement",
"description":"Bricks or blocks per square metre from any unit size and joint width, total for your wall, mortar volume, and the sand and cement to mix it.",
"card_desc":"Units per square metre from any brick size and joint, plus mortar, sand and cement.",
"category":"Finishing",
"intro":"Brick sizes and joint widths differ by country and by product, so a fixed number per square metre is always wrong somewhere. Enter your actual unit size and joint and this works it out from geometry, then adds the mortar.",
"notes":[("Where the count comes from","Each brick occupies its own size plus one joint in each direction. So the area of one unit including its joints is (length + joint) times (height + joint), and the count per square metre is one divided by that. Nothing is assumed about your brick."),
("Mortar volume","The mortar is the difference between the wall volume and the volume of the units in it. Add 10 to 20 percent for what falls off the board, stays in the mixer and fills frogs and perforations."),
("Single skin, double skin","A wall two units thick uses twice the bricks and more than twice the mortar, because the collar joint between the skins is mortar too. Set the number of skins and it is included."),
("What this does not do","It does not specify a mortar mix, allow for wall ties, movement joints or reinforcement, and it does not know whether your wall needs a designer. It counts material.")],
"js":"""
var SPEC = {
  fields: [
    {id:'wallL', label:'Wall length', value:5000, unit:'length', group:'Wall', min:0},
    {id:'wallH', label:'Wall height', value:2400, unit:'length', group:'Wall', min:0},
    {id:'skins', label:'Number of skins', value:1, group:'Wall', min:1, step:1},
    {id:'openings', label:'Openings to deduct (m2)', value:0, group:'Wall', min:0},
    {id:'unitL', label:'Unit length', value:215, unit:'length', group:'Unit', min:0},
    {id:'unitH', label:'Unit height', value:65, unit:'length', group:'Unit', min:0},
    {id:'unitW', label:'Unit width (thickness)', value:102.5, unit:'length', group:'Unit', min:0},
    {id:'joint', label:'Joint thickness', value:10, unit:'length', group:'Unit', min:0},
    {id:'waste', label:'Breakage allowance (%)', value:5, group:'Ordering', min:0},
    {id:'mortarWaste', label:'Mortar allowance (%)', value:15, group:'Ordering', min:0}
  ],
  compute: function (i) {
    var k = i.unit === 'in' ? 0.0254 : 0.001;
    var L=i.wallL*k, Hh=i.wallH*k, uL=i.unitL*k, uH=i.unitH*k, uW=i.unitW*k, j=i.joint*k;
    if (!(L>0 && Hh>0)) return {ok:false, errors:['Wall length and height must be greater than zero.']};
    if (!(uL>0 && uH>0 && uW>0)) return {ok:false, errors:['Unit dimensions must be greater than zero.']};

    var skins = Math.max(1, Math.round(i.skins));
    var area = Math.max(0, L*Hh - Math.max(0,i.openings));
    if (area <= 0) return {ok:false, errors:['The openings deduct more than the whole wall.']};

    var perM2 = 1/((uL+j)*(uH+j));
    var units = area*perM2*skins;
    var unitsOrder = Math.ceil(units*(1+Math.max(0,i.waste)/100));

    var wallVol = area*(uW*skins + (skins>1 ? j*(skins-1) : 0));
    var unitVol = units*(uL*uH*uW);
    var mortar = Math.max(0, wallVol - unitVol);
    var mortarOrder = mortar*(1+Math.max(0,i.mortarWaste)/100);

    // Melange 1:4 en volume : le sable est l'essentiel du volume du mortier
    var sand = mortarOrder*1.0;            // m3 de sable humide, approche
    var cementKg = sand*1440/4;            // 1 volume de ciment pour 4 de sable
    var bags = Math.ceil(cementKg/25);

    var warn=[];
    if (j > uH*0.3) warn.push('The joint is very thick relative to the unit height \u2014 check the numbers.');

    return {ok:true, perM2:perM2, units:units, unitsOrder:unitsOrder, mortarOrder:mortarOrder,
      area:area, L:L, Hh:Hh, skins:skins,
      warnings: warn,
      stats:[
        {value: WCfmt(perM2,1), label:'Units per m2'},
        {value: String(unitsOrder), label:'Units to order'},
        {value: WCfmt(mortarOrder,3), label:'m3 of mortar'},
        {value: String(bags), label:'25 kg cement bags'}
      ],
      tables:[{title:'Take-off', head:['Item','Value'], rows:[
        ['Wall face area', WCfmt(area,2)+' m2'],
        ['Skins', String(skins)],
        ['Unit size', WCfmt(i.unitL,1)+' \u00d7 '+WCfmt(i.unitH,1)+' \u00d7 '+WCfmt(i.unitW,1)],
        ['Joint', WCfmt(i.joint,1)],
        ['Units per m2 per skin', WCfmt(perM2,2)],
        ['Units needed', WCfmt(units,0)],
        ['With '+WCfmt(i.waste,0)+'% breakage', String(unitsOrder)],
        ['Mortar volume', WCfmt(mortar,4)+' m3'],
        ['With '+WCfmt(i.mortarWaste,0)+'% allowance', WCfmt(mortarOrder,3)+' m3'],
        ['Sand (approx)', WCfmt(sand,2)+' m3'],
        ['Cement at 1:4 by volume', WCfmt(cementKg,0)+' kg = '+String(bags)+' bags of 25 kg']
      ]}],
      note:'Counts come from your actual unit size and joint, not from a standard table \u2014 so they hold for any brick or block anywhere.'
    };
  },
  diagram: function (r, i) {
    var W=600,H=300,m=40,s=SVG.open(W,H);
    var sc=Math.min((W-2*m)/r.L,(H-110)/Math.max(r.Hh,0.1));
    var x0=m,y0=60,ww=r.L*sc,wh=r.Hh*sc;
    var k = i.unit === 'in' ? 0.0254 : 0.001;
    var bw=(i.unitL*k+i.joint*k)*sc, bh=(i.unitH*k+i.joint*k)*sc;
    var rows=Math.min(40,Math.floor(wh/Math.max(bh,1)));
    for(var rr=0; rr<rows; rr++){
      var off = (rr%2)*bw/2;
      for(var cc=-1; cc*bw-off < ww; cc++){
        var x=x0+cc*bw-off;
        var x1=Math.max(x,x0), x2=Math.min(x+bw-1.2, x0+ww);
        if (x2>x1) s+=SVG.rect(x1, y0+rr*bh, x2-x1, Math.max(1,bh-1.2), 'part');
      }
    }
    s+=SVG.text(W/2,30, WCfmt(r.perM2,1)+' units/m2  \u00b7  '+r.unitsOrder+' to order', 13);
    s+=SVG.text(W/2,H-16, WCfmt(r.area,2)+' m2  \u00b7  '+WCfmt(r.mortarOrder,3)+' m3 of mortar', 12);
    return s+SVG.close();
  }
};
"""}
