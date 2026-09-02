SPEC = {
"slug":"wallpaper-calculator",
"h1":"Wallpaper Calculator With Pattern Repeat",
"title_tag":"Wallpaper Calculator — Rolls Needed Including Pattern Repeat and Drop Match",
"description":"How many rolls of wallpaper you need once the pattern repeat and drop match are accounted for, with usable drops per roll and waste per drop.",
"card_desc":"Rolls needed once the pattern repeat is accounted for \u2014 the part most calculators ignore.",
"category":"Finishing",
"intro":"Most wallpaper calculators divide the wall area by the roll area and get it wrong. The pattern repeat is what decides it: with a 64 cm repeat on a 2.4 m wall you lose most of a drop every time, and that is the difference between four rolls and six.",
"notes":[("Why the repeat changes everything","Each drop has to start at the same point in the pattern, so you cut to the next whole repeat above the wall height. A 2400 wall with a 640 repeat means cutting drops of 2560 \u2014 160 wasted on every single drop."),
("Straight match and offset match","A straight match lines up across the seam at the same height. An offset or drop match shifts by half a repeat each drop, which means you alternate between two starting points \u2014 it wastes less overall, because the offcut of one drop starts the next."),
("Always buy from one batch","Rolls printed in different batches differ slightly in colour, and the seam between them is visible on a wall. Buy the extra roll now; matching a batch later is usually impossible."),
("What this does not do","It counts drops on plain walls. Alcoves, chimney breasts, stairwells and papering around windows all change the count, and stairwells in particular waste far more than the arithmetic suggests.")],
"js":"""
var SPEC = {
  fields: [
    {id:'perimeter', label:'Total wall length', value:16000, unit:'length', group:'Room', min:0,
     hint:'Add up the walls you are papering'},
    {id:'height', label:'Wall height', value:2400, unit:'length', group:'Room', min:0},
    {id:'doors', label:'Doors to deduct', value:1, group:'Room', min:0, step:1},
    {id:'windows', label:'Windows to deduct', value:2, group:'Room', min:0, step:1},
    {id:'rollW', label:'Roll width', value:530, unit:'length', group:'Paper', min:0},
    {id:'rollL', label:'Roll length', value:10050, unit:'length', group:'Paper', min:0},
    {id:'repeat', label:'Pattern repeat', value:640, unit:'length', group:'Paper', min:0,
     hint:'0 for a plain paper'},
    {id:'match', label:'Match type', type:'select', value:'straight', group:'Paper', options:[
      {value:'free', label:'Free match / plain'},
      {value:'straight', label:'Straight match'},
      {value:'offset', label:'Offset (drop) match'}]},
    {id:'trim', label:'Trim allowance per drop', value:100, unit:'length', group:'Paper', min:0}
  ],
  compute: function (i) {
    var P=i.perimeter, Hh=i.height;
    if (!(P>0 && Hh>0)) return {ok:false, errors:['Wall length and height must be greater than zero.']};
    if (!(i.rollW>0 && i.rollL>0)) return {ok:false, errors:['Roll width and length must be greater than zero.']};

    // Deduction : une porte ~0.9 m de large, une fenetre ~1.2 m.
    // Les largeurs sont en millimetres : on les ramene dans l'unite saisie,
    // sinon en pouces la deduction vaut cinq fois le perimetre de la piece.
    var toMm = i.unit === 'in' ? 25.4 : 1;
    var deduct = (Math.max(0,i.doors)*900 + Math.max(0,i.windows)*1200)/toMm;
    var netP = Math.max(0, P - deduct);
    var drops = Math.ceil(netP/i.rollW);

    var cutLength;
    if (i.repeat > 0 && i.match !== 'free') {
      var needed = Hh + i.trim;
      cutLength = Math.ceil(needed/i.repeat)*i.repeat;
    } else {
      cutLength = Hh + i.trim;
    }
    var wastePerDrop = cutLength - Hh;

    var dropsPerRoll = Math.floor(i.rollL/cutLength);
    if (dropsPerRoll < 1) return {ok:false, errors:['A single drop is longer than a whole roll. Check the roll length and the repeat.']};

    // Chaque le doit sortir d'un seul tenant : on ne recolle pas deux chutes.
    // Le nombre de les par rouleau est donc plafonne par la longueur du rouleau,
    // et un raccord saute consomme davantage de papier, jamais moins.
    var rolls = Math.ceil(drops/dropsPerRoll);

    var totalWaste = drops*wastePerDrop;
    var warn=[];
    if (wastePerDrop > i.repeat*0.6) warn.push('You lose '+WCfmt(wastePerDrop,0)+' on every drop \u2014 most of a repeat. A paper with a smaller repeat would use noticeably less.');
    if (rolls > 0) warn.push('Buy all rolls from the same batch number. Different batches differ in colour and the seam shows.');

    return {ok:true, drops:drops, cutLength:cutLength, dropsPerRoll:dropsPerRoll, rolls:rolls,
      wastePerDrop:wastePerDrop, netP:netP, Hh:Hh,
      warnings: warn,
      stats:[
        {value: String(rolls), label:'Rolls to buy'},
        {value: String(drops), label:'Drops needed'},
        {value: WCfmt(cutLength,0), label:'Cut length per drop'},
        {value: String(dropsPerRoll), label:'Drops per roll'}
      ],
      tables:[{title:'Working', head:['Item','Value'], rows:[
        ['Wall length', WCfmt(P,0)],
        ['Deducted for openings', WCfmt(deduct,0)+'  ('+i.doors+' door(s), '+i.windows+' window(s))'],
        ['Length to paper', WCfmt(netP,0)],
        ['Roll width', WCfmt(i.rollW,0)],
        ['Drops needed', String(drops)],
        ['Wall height', WCfmt(Hh,0)],
        ['Pattern repeat', i.repeat>0 ? WCfmt(i.repeat,0) : 'plain'],
        ['Cut length per drop', WCfmt(cutLength,0)],
        ['Wasted per drop', WCfmt(wastePerDrop,0)],
        ['Total waste', WCfmt(totalWaste*toMm/1000,2)+' m of paper'],
        ['Drops per roll', String(dropsPerRoll)],
        ['Rolls to buy', String(rolls)]
      ]}],
      note:'Cut length is rounded up to the next whole pattern repeat so every drop starts at the same point in the design.'
    };
  },
  diagram: function (r, i) {
    var W=600,H=300,m=45,s=SVG.open(W,H);
    var n=Math.min(r.drops,9);
    var dw=(W-2*m)/n, top=60, hh=170;
    for(var k=0;k<n;k++){
      var x=m+k*dw;
      s+=SVG.rect(x+1,top,dw-3,hh,'part');
      if (i.repeat>0){
        var reps=Math.max(1,Math.round(r.Hh/i.repeat));
        for(var q=1;q<=reps;q++){
          var yy=top+hh*q/(reps+ (r.wastePerDrop/Math.max(1,r.Hh)));
          if (yy<top+hh) s+=SVG.line(x+2,yy,x+dw-3,yy,' class="dim"');
        }
      }
    }
    s+=SVG.text(W/2,30,r.drops+' drops  \u00b7  '+r.rolls+' rolls  \u00b7  cut '+WCfmt(r.cutLength,0)+' each',13);
    s+=SVG.text(W/2,H-16,'waste '+WCfmt(r.wastePerDrop,0)+' per drop from the '+WCfmt(i.repeat,0)+' repeat',12);
    return s+SVG.close();
  }
};
"""}
