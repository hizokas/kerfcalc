SPEC = {
"slug":"epoxy-resin-calculator",
"h1":"Epoxy Resin Volume &amp; Cost Calculator",
"title_tag":"Epoxy Resin Calculator — River Table Volume, Litres and Cost",
"description":"Resin volume for river tables, slab pours and coatings, with waste allowance, litre and gallon conversion, cost per pour and a scaled diagram of the pour.",
"card_desc":"River table and pour volume with waste allowance, litres or gallons, and the cost of the pour.",
"category":"Finishing",
"intro":"Resin is too expensive to guess. This works out the true volume of a river channel or slab pour, adds a waste allowance you control, converts to the litres or gallons on the tin, and prices the pour — with the geometry drawn so you can check it against the real slab.",
"notes":[("How the river channel is estimated","The channel is measured as an average width times length times depth. A live-edge channel is irregular — measure its width every 200 mm or so, average the readings, and use that. The diagram shows what the average-width rectangle looks like against your dimensions."),
("Why the waste allowance","Mixing losses, the film left in the bucket, overflow into the seal coat and absorption into the wood typically eat 5 to 15 percent. Deep-pour epoxies on well-sealed wood waste less; first pours on thirsty timber waste more. It is an input, not a hidden markup."),
("Maximum pour depth","Every epoxy has a maximum depth per pour — exceed it and the pour overheats, yellows or cracks. That limit is on YOUR product's data sheet, not in this tool: enter it and the tool splits the volume into pours."),
("Litres, gallons, and board feet do not mix","Resin kits are sold by total volume of the two parts combined. The figure here is that combined volume — compare it directly to the kit size on the label."),
("What this does not do","It does not know your product's mixing ratio, pot life, or exotherm limits — read the data sheet. And it does not estimate seal coats for porous surfaces; add those to the waste allowance instead.")],
"js":"""
var SPEC = {
  fields: [
    {id:'shape', label:'What are you pouring', type:'select', value:'river', group:'The pour',
     options:[{value:'river',label:'River channel (average width)'},
              {value:'slab',label:'Full rectangular pour / mold'},
              {value:'coat',label:'Surface coating (thin flood coat)'}]},
    {id:'len', label:'Length', value:1800, unit:'length', group:'The pour', min:0},
    {id:'wid', label:'Width (average, for a river)', value:120, unit:'length', group:'The pour', min:0,
     hint:'Measure the channel every 200 mm and average it'},
    {id:'dep', label:'Depth / coat thickness', value:40, unit:'length', group:'The pour', min:0},
    {id:'waste', label:'Waste allowance %', value:10, group:'Allowances', min:0, step:1,
     hint:'Mixing losses, bucket film, absorption: 5-15% typical'},
    {id:'maxpour', label:'Max depth per pour (0 = single pour)', value:0, unit:'length', group:'Allowances', min:0,
     hint:'From your resin data sheet'},
    {id:'price', label:'Price per litre of mixed resin (0 = skip cost)', value:0, group:'Cost', min:0,
     hint:'Kit price divided by kit litres'}
  ],
  compute: function (i) {
    var mm = i.unit !== 'in';
    var toL = function(v){ return mm ? v/1e6 : v*0.0163871; };  // mm3->cm3->L ; in3->L
    if (!(i.len>0 && i.wid>0 && i.dep>0))
      return {ok:false, errors:['Length, width and depth must all be greater than zero.']};

    var volRaw = i.len * i.wid * i.dep;           // en unites cubes saisies
    var litres = toL(volRaw) * (mm ? 1000 : 1);   // mm: mm3 -> L directement via /1e6 (cm3) puis... voir note
    // Correction d'unites, ecrite noir sur blanc :
    // mm3 -> litres = /1 000 000 ; in3 -> litres = x 0.0163871
    litres = mm ? volRaw/1e6 : volRaw*0.0163871;

    var withWaste = litres * (1 + Math.max(0,i.waste)/100);
    var gallons = withWaste / 3.78541;

    var pours = 1, perPour = withWaste;
    if (i.maxpour > 0 && i.maxpour < i.dep) {
      pours = Math.ceil(i.dep / i.maxpour);
      perPour = withWaste / pours;
    }
    var cost = i.price > 0 ? withWaste * i.price : null;

    var warn = [];
    if (mm && i.dep > 50 && i.maxpour === 0)
      warn.push('A pour deeper than 50 mm is beyond many table-top epoxies. Check your product\\'s maximum depth and enter it above to plan the pours.');
    if (!mm && i.dep > 2 && i.maxpour === 0)
      warn.push('A pour deeper than 2 in is beyond many table-top epoxies. Check your product\\'s maximum depth and enter it above to plan the pours.');

    var stats = [
      {value: WCfmt(withWaste,2)+' L', label:'Mixed resin to buy'},
      {value: WCfmt(gallons,2)+' gal', label:'US gallons'},
      {value: String(pours), label:'Pour'+(pours>1?'s':'')},
      cost !== null ? {value: WCfmt(cost,0), label:'Cost of the pour'}
                    : {value: WCfmt(litres,2)+' L', label:'Net volume, no waste'}
    ];

    return {ok:true, litres:litres, withWaste:withWaste, pours:pours, u: mm?'mm':'in',
      warnings:warn, stats:stats,
      tables:[{title:'The arithmetic', head:['Item','Value'], rows:[
        ['Volume', WCfmt(i.len,0)+' x '+WCfmt(i.wid,0)+' x '+WCfmt(i.dep,0)+' = '+WCfmt(litres,2)+' L net'],
        ['Waste allowance', WCfmt(i.waste,0)+'% -> '+WCfmt(withWaste-litres,2)+' L'],
        ['Total mixed resin', WCfmt(withWaste,2)+' L  ('+WCfmt(gallons,2)+' US gal)'],
        ['Pours', pours>1 ? pours+' pours of ~'+WCfmt(perPour,2)+' L, max '+WCfmt(i.maxpour,0)+' '+(mm?'mm':'in')+' deep each' : 'single pour'],
        ['Cost', cost !== null ? WCfmt(cost,2)+' at '+WCfmt(i.price,2)+' per litre' : 'enter a price per litre to see it']
      ]}],
      note:'Compare the total to the KIT size on the label — kits quote the combined volume of resin plus hardener.'
    };
  },
  diagram: function (r, i) {
    var W=560, H=250, s=SVG.open(W,H), m=55;
    s += SVG.text(W/2, 24, i.shape==='river' ? 'River channel as the average-width rectangle' : 'The pour, to scale', 13);
    var sc = Math.min((W-2*m)/i.len, 90/i.wid);
    var pw = i.len*sc, ph = Math.max(10, i.wid*sc), x0=(W-pw)/2, y0=54;
    if (i.shape==='river') {
      // La dalle en fantome, le canal en accent au milieu.
      s += SVG.rect(x0, y0-18, pw, ph+36, 'ghost');
      s += SVG.rect(x0, y0, pw, ph, 'part');
      s += SVG.text(x0+pw/2, y0+ph/2+4, 'channel', Math.min(12, ph-2));
    } else {
      s += SVG.rect(x0, y0, pw, ph, 'part');
    }
    s += SVG.line(x0, y0+ph+26, x0+pw, y0+ph+26, ' class="dim"');
    s += SVG.text(x0+pw/2, y0+ph+40, WCfmt(i.len,0)+' '+r.u+' long, '+WCfmt(i.wid,0)+' '+r.u+' wide (average)', 11);
    // Coupe : profondeur et nombre de coulees.
    var cy = y0+ph+66, cw=160, cd=Math.max(14, Math.min(46, i.dep*sc*2));
    s += SVG.rect(W/2-cw/2, cy, cw, cd, 'part');
    for (var k=1; k<r.pours; k++)
      s += SVG.line(W/2-cw/2, cy+cd*k/r.pours, W/2+cw/2, cy+cd*k/r.pours, ' stroke-dasharray="5 3"');
    s += SVG.text(W/2, cy+cd+16, 'section: '+WCfmt(i.dep,0)+' '+r.u+' deep'+(r.pours>1?' in '+r.pours+' pours':''), 11);
    return s + SVG.close();
  }
};
"""}
