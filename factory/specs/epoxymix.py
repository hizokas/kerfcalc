SPEC = {
"slug":"epoxy-mix-ratio-calculator",
"h1":"Epoxy Mix Ratio Calculator",
"title_tag":"Epoxy Mix Ratio Calculator — Parts A and B by Volume or Weight",
"description":"How much resin and hardener to measure for any batch, from the ratio on your product's label, by volume or by weight with your product's specific gravities.",
"card_desc":"Parts A and B for any batch size, by volume or weight, from the ratio on your label.",
"category":"Finishing",
"intro":"Get the ratio wrong and the pour never cures. This takes the ratio printed on your product's label — 1:1, 2:1, 100:45, anything — and a batch size, and tells you exactly how much part A and part B to measure, by volume or by weight.",
"notes":[("Volume ratio and weight ratio are different numbers","Resin and hardener have different densities, so a 2:1 by volume product is NOT 2:1 by weight. Your data sheet states which one the printed ratio is, and usually gives both. Enter the ratio as your label states it, and pick the matching mode."),
("Weighing is more accurate","A scale reads to the gram; measuring cups trap film and misread menisci. If your data sheet gives the weight ratio, use it with a scale. If it only gives volume and you want to weigh, enter the specific gravity of each part from the data sheet and the tool converts."),
("Never adjust the ratio to change cure speed","More hardener does not cure faster — it leaves permanently soft resin. The ratio is chemistry, not seasoning. Change cure speed by changing product or temperature, never proportions."),
("Mix more than you pour","The film left on the bucket and stick is real: mix 5-10% extra. The batch size here should already include your waste allowance — the epoxy volume calculator on this site works that out.")],
"js":"""
var SPEC = {
  fields: [
    {id:'ra', label:'Ratio — parts A (resin)', value:2, group:'The ratio on your label', min:0.01,
     hint:'e.g. 2 for a 2:1, 100 for a 100:45'},
    {id:'rb', label:'Ratio — parts B (hardener)', value:1, group:'The ratio on your label', min:0.01},
    {id:'rtype', label:'That ratio is stated', type:'select', value:'vol', group:'The ratio on your label',
     options:[{value:'vol',label:'By volume'},{value:'wt',label:'By weight'}]},
    {id:'batch', label:'Batch size, total mixed', value:1000, group:'The batch', min:1,
     hint:'In ml, or in grams if working by weight'},
    {id:'btype', label:'Measure the batch', type:'select', value:'vol', group:'The batch',
     options:[{value:'vol',label:'By volume (ml)'},{value:'wt',label:'By weight (g)'}]},
    {id:'sga', label:'Specific gravity, part A (only to convert)', value:1.1, group:'Only if converting volume to weight', min:0.5,
     hint:'From the data sheet; ~1.1 typical for epoxy resin'},
    {id:'sgb', label:'Specific gravity, part B', value:1.0, group:'Only if converting volume to weight', min:0.5,
     hint:'~0.9-1.0 typical for hardeners'}
  ],
  compute: function (i) {
    if (!(i.ra>0 && i.rb>0 && i.batch>0))
      return {ok:false, errors:['Ratio parts and batch size must be greater than zero.']};

    var unit = i.btype==='vol' ? 'ml' : 'g';
    var A, B, conv = false;

    if (i.rtype === i.btype) {
      // Meme grandeur des deux cotes : simple proportion.
      A = i.batch * i.ra/(i.ra+i.rb);
      B = i.batch * i.rb/(i.ra+i.rb);
    } else if (i.rtype==='vol' && i.btype==='wt') {
      // Ratio en volume, pesee au gramme : chaque part pese volume x densite.
      conv = true;
      if (!(i.sga>0 && i.sgb>0)) return {ok:false, errors:['Enter both specific gravities to convert volume to weight.']};
      var wa = i.ra*i.sga, wb = i.rb*i.sgb;          // poids relatifs
      A = i.batch * wa/(wa+wb);
      B = i.batch * wb/(wa+wb);
    } else {
      // Ratio en poids, mesure en volume : chaque part occupe poids / densite.
      conv = true;
      if (!(i.sga>0 && i.sgb>0)) return {ok:false, errors:['Enter both specific gravities to convert weight to volume.']};
      var va = i.ra/i.sga, vb = i.rb/i.sgb;
      A = i.batch * va/(va+vb);
      B = i.batch * vb/(va+vb);
    }

    var warn = [];
    if (conv) warn.push('Converted between volume and weight using the specific gravities you entered — check them against your data sheet, they differ between products.');

    return {ok:true, A:A, B:B, unit:unit,
      warnings:warn,
      stats:[
        {value: WCfmt(A,1)+' '+unit, label:'Part A (resin)'},
        {value: WCfmt(B,1)+' '+unit, label:'Part B (hardener)'},
        {value: WCfmt(i.ra,2)+' : '+WCfmt(i.rb,2), label:'Ratio ('+(i.rtype==='vol'?'volume':'weight')+')'},
        {value: WCfmt(i.batch,0)+' '+unit, label:'Total batch'}
      ],
      tables:[{title:'Pour sequence', head:['Step','What to do'], rows:[
        ['1', 'Tare the container on the scale (or use a marked cup).'],
        ['2', 'Add part A to '+WCfmt(A,1)+' '+unit+'.'],
        ['3', 'Add part B until the total reads '+WCfmt(i.batch,0)+' '+unit+' ('+WCfmt(B,1)+' '+unit+' of B).'],
        ['4', 'Mix 3 minutes, scrape walls and bottom, transfer to a clean cup, mix again briefly.']
      ]}],
      note:'The printed ratio is chemistry — never change it to speed up or slow down the cure.'
    };
  },
  diagram: function (r, i) {
    var W=560, H=200, s=SVG.open(W,H);
    s += SVG.text(W/2, 24, 'The batch, to proportion', 13);
    var total = r.A + r.B, m=70, bw=W-2*m, y=60, h=56;
    var aw = bw * r.A/total;
    s += SVG.rect(m, y, aw, h, 'part');
    s += SVG.rect(m+aw, y, bw-aw, h, 'ghost', ' style="fill:var(--accent);fill-opacity:.35"');
    s += SVG.text(m+aw/2, y+h/2+4, 'A  '+WCfmt(r.A,1)+' '+r.unit, 12);
    s += SVG.text(m+aw+(bw-aw)/2, y+h/2+4, 'B  '+WCfmt(r.B,1)+' '+r.unit, 12);
    s += SVG.line(m, y+h+18, m+bw, y+h+18, ' class="dim"');
    s += SVG.text(W/2, y+h+34, 'total '+WCfmt(i.batch,0)+' '+r.unit, 11);
    return s + SVG.close();
  }
};
"""}
