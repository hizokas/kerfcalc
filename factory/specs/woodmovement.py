SPEC = {
"slug":"wood-movement-calculator",
"h1":"Wood Movement Calculator",
"title_tag":"Wood Movement Calculator - Seasonal Expansion by Species and Cut",
"description":"How much a board will shrink and swell across its width between seasons, from USDA Forest Products Laboratory dimensional change coefficients for 130 species, flatsawn or quartersawn.",
"card_desc":"Seasonal expansion across the grain for 130 species, from published USDA coefficients - flatsawn or quartersawn.",
"category":"Joinery",
"intro":"A 300 mm flatsawn oak panel can move 5 mm between a damp summer and a heated winter. Glue it solid and it splits. This works out the real figure for your species, your cut and your workshop, using the dimensional change coefficients published by the USDA Forest Products Laboratory.",
"notes":[
("Where the numbers come from","The coefficients are Table 13-5 of the Wood Handbook (USDA Forest Products Laboratory, General Technical Report FPL-GTR-190), a public-domain reference. Nothing here is estimated or interpolated: if a species is not in that table it is not in this list."),
("The equation","Change in dimension = starting width x coefficient x change in moisture content, in percentage points. That is equation 13-2 of the Wood Handbook. It is a straight-line approximation validated between 6% and 14% moisture content, which covers almost all indoor furniture."),
("Why the cut matters more than the species","Tangential movement - the flatsawn face - is roughly twice radial movement in most species. Quartersawing the same board can halve the problem. That is why quartersawn stock is worth its price for wide panels, door frames and anything that has to stay flat."),
("How humidity becomes moisture content","Wood settles at an equilibrium moisture content set by the air around it. This tool converts your relative humidity and temperature using the Hailwood-Horrobin equation as fitted by Simpson, equation 4-5 of the Wood Handbook. At 21 C the results reproduce the published table exactly: 30% RH gives 6.2%, 65% gives 12.0%, 80% gives 16.0%."),
("What relative humidity should I use","Measure it. A cheap hygrometer in the room the piece will live in, read in February and again in August, beats any table. If you cannot, a heated house in a temperate winter typically sits at 25-35% and an unconditioned summer at 60-75% - but a coastal workshop and a centrally heated flat are different worlds."),
("What this does not cover","Movement along the grain is negligible and is ignored, which is correct for solid timber and wrong for nothing you are likely to build. Thickness moves like width and follows the same coefficients. Plywood and MDF barely move at all - do not use this for them. And a board that is still drying will move far more than this on its way to equilibrium.")],
"js":"""
var SPEC = {
  fields: [
    {id:'species', label:'Species', type:'select', value:'46', group:'The board',
     options:[
      {value:"0",label:"Hardwood - Alder, red"},
      {value:"1",label:"Hardwood - Apple"},
      {value:"2",label:"Hardwood - Ash, black"},
      {value:"3",label:"Hardwood - Ash, green"},
      {value:"4",label:"Hardwood - Ash, Oregon"},
      {value:"5",label:"Hardwood - Ash, pumpkin"},
      {value:"6",label:"Hardwood - Ash, white"},
      {value:"7",label:"Hardwood - Aspen, quaking"},
      {value:"8",label:"Hardwood - Basswood, American"},
      {value:"9",label:"Hardwood - Beech, American"},
      {value:"10",label:"Hardwood - Birch, paper"},
      {value:"11",label:"Hardwood - Birch, river"},
      {value:"12",label:"Hardwood - Birch, sweet"},
      {value:"13",label:"Hardwood - Birch, yellow"},
      {value:"14",label:"Hardwood - Buckeye, yellow"},
      {value:"15",label:"Hardwood - Butternut"},
      {value:"16",label:"Hardwood - Catalpa, northern"},
      {value:"17",label:"Hardwood - Cherry, black"},
      {value:"18",label:"Hardwood - Chestnut, American"},
      {value:"19",label:"Hardwood - Cottonwood, black"},
      {value:"20",label:"Hardwood - Cottonwood, eastern"},
      {value:"21",label:"Hardwood - Elm, American"},
      {value:"22",label:"Hardwood - Elm, cedar"},
      {value:"23",label:"Hardwood - Elm, rock"},
      {value:"24",label:"Hardwood - Elm, slippery"},
      {value:"25",label:"Hardwood - Elm, winged"},
      {value:"26",label:"Hardwood - Hackberry"},
      {value:"27",label:"Hardwood - Hickory, pecan"},
      {value:"28",label:"Hardwood - Hickory, true"},
      {value:"29",label:"Hardwood - Holly, American"},
      {value:"30",label:"Hardwood - Honeylocust"},
      {value:"31",label:"Hardwood - Locust, black"},
      {value:"32",label:"Hardwood - Madrone, Pacific"},
      {value:"33",label:"Hardwood - Magnolia, cucumbertree"},
      {value:"34",label:"Hardwood - Magnolia, southern"},
      {value:"35",label:"Hardwood - Magnolia, sweetbay"},
      {value:"36",label:"Hardwood - Maple, bigleaf"},
      {value:"37",label:"Hardwood - Maple, black"},
      {value:"38",label:"Hardwood - Maple, red"},
      {value:"39",label:"Hardwood - Maple, silver"},
      {value:"40",label:"Hardwood - Maple, sugar (hard maple)"},
      {value:"41",label:"Hardwood - Oak, black"},
      {value:"42",label:"Hardwood - Oak, California red"},
      {value:"43",label:"Hardwood - Oak, live"},
      {value:"44",label:"Hardwood - Oak, Oregon white"},
      {value:"45",label:"Hardwood - Oak, overcup"},
      {value:"46",label:"Hardwood - Oak, red (commercial)"},
      {value:"47",label:"Hardwood - Oak, water / laurel / willow"},
      {value:"48",label:"Hardwood - Oak, white (commercial)"},
      {value:"49",label:"Hardwood - Persimmon, common"},
      {value:"50",label:"Hardwood - Sassafras"},
      {value:"51",label:"Hardwood - Sweetgum"},
      {value:"52",label:"Hardwood - Sycamore, American"},
      {value:"53",label:"Hardwood - Tanoak"},
      {value:"54",label:"Hardwood - Tupelo, black"},
      {value:"55",label:"Hardwood - Tupelo, water"},
      {value:"56",label:"Hardwood - Walnut, black"},
      {value:"57",label:"Hardwood - Willow, black"},
      {value:"58",label:"Hardwood - Willow, Pacific"},
      {value:"59",label:"Hardwood - Yellow-poplar (tulipwood)"},
      {value:"60",label:"Softwood - Baldcypress"},
      {value:"61",label:"Softwood - Cedar, Alaska yellow"},
      {value:"62",label:"Softwood - Cedar, Atlantic white"},
      {value:"63",label:"Softwood - Cedar, eastern red"},
      {value:"64",label:"Softwood - Cedar, incense"},
      {value:"65",label:"Softwood - Cedar, northern white"},
      {value:"66",label:"Softwood - Cedar, Port-Orford"},
      {value:"67",label:"Softwood - Cedar, western red"},
      {value:"68",label:"Softwood - Douglas-fir, coast"},
      {value:"69",label:"Softwood - Douglas-fir, interior north"},
      {value:"70",label:"Softwood - Douglas-fir, interior west"},
      {value:"71",label:"Softwood - Fir, balsam"},
      {value:"72",label:"Softwood - Fir, California red"},
      {value:"73",label:"Softwood - Fir, grand"},
      {value:"74",label:"Softwood - Fir, noble"},
      {value:"75",label:"Softwood - Fir, Pacific silver"},
      {value:"76",label:"Softwood - Fir, subalpine"},
      {value:"77",label:"Softwood - Fir, white"},
      {value:"78",label:"Softwood - Hemlock, eastern"},
      {value:"79",label:"Softwood - Hemlock, western"},
      {value:"80",label:"Softwood - Larch, western"},
      {value:"81",label:"Softwood - Pine, eastern white"},
      {value:"82",label:"Softwood - Pine, jack"},
      {value:"83",label:"Softwood - Pine, Jeffrey"},
      {value:"84",label:"Softwood - Pine, loblolly"},
      {value:"85",label:"Softwood - Pine, lodgepole"},
      {value:"86",label:"Softwood - Pine, longleaf"},
      {value:"87",label:"Softwood - Pine, pond"},
      {value:"88",label:"Softwood - Pine, ponderosa"},
      {value:"89",label:"Softwood - Pine, red"},
      {value:"90",label:"Softwood - Pine, shortleaf"},
      {value:"91",label:"Softwood - Pine, slash"},
      {value:"92",label:"Softwood - Pine, sugar"},
      {value:"93",label:"Softwood - Pine, Virginia"},
      {value:"94",label:"Softwood - Pine, western white"},
      {value:"95",label:"Softwood - Redwood, old growth"},
      {value:"96",label:"Softwood - Redwood, second growth"},
      {value:"97",label:"Softwood - Spruce, black"},
      {value:"98",label:"Softwood - Spruce, Engelmann"},
      {value:"99",label:"Softwood - Spruce, red"},
      {value:"100",label:"Softwood - Spruce, Sitka"},
      {value:"101",label:"Softwood - Spruce, white"},
      {value:"102",label:"Softwood - Tamarack"},
      {value:"103",label:"Imported - Andiroba (crabwood)"},
      {value:"104",label:"Imported - Angelique"},
      {value:"105",label:"Imported - Apitong / keruing"},
      {value:"106",label:"Imported - Avodire"},
      {value:"107",label:"Imported - Balsa"},
      {value:"108",label:"Imported - Banak"},
      {value:"109",label:"Imported - Cativo"},
      {value:"110",label:"Imported - Cuangare"},
      {value:"111",label:"Imported - Greenheart"},
      {value:"112",label:"Imported - Iroko"},
      {value:"113",label:"Imported - Khaya (African mahogany)"},
      {value:"114",label:"Imported - Lauan, dark red (Philippine mahogany)"},
      {value:"115",label:"Imported - Lauan, light red (Philippine mahogany)"},
      {value:"116",label:"Imported - Limba"},
      {value:"117",label:"Imported - Mahogany (American)"},
      {value:"118",label:"Imported - Meranti"},
      {value:"119",label:"Imported - Obeche"},
      {value:"120",label:"Imported - Okoume"},
      {value:"121",label:"Imported - Parana pine"},
      {value:"122",label:"Imported - Pau marfim"},
      {value:"123",label:"Imported - Primavera"},
      {value:"124",label:"Imported - Ramin"},
      {value:"125",label:"Imported - Santa Maria"},
      {value:"126",label:"Imported - Spanish-cedar"},
      {value:"127",label:"Imported - Teak"}
     ]},
    {id:'cut', label:'How it is sawn', type:'select', value:'flat', group:'The board',
     options:[{value:'flat',label:'Flatsawn / plain sawn (tangential)'},
              {value:'quarter',label:'Quartersawn (radial)'},
              {value:'unsure',label:'Not sure - assume the worst'}]},
    {id:'width', label:'Width across the grain', value:300, unit:'length', group:'The board', min:0,
     hint:'The full width of the panel or top, not one board'},
    {id:'mode', label:'Work from', type:'select', value:'rh', group:'Conditions',
     options:[{value:'rh',label:'Relative humidity'},
              {value:'mc',label:'Moisture content I have measured'}]},
    {id:'tunit', label:'Temperature scale', type:'select', value:'C', group:'Conditions',
     options:[{value:'C',label:'Celsius'},{value:'F',label:'Fahrenheit'}]},
    {id:'temp', label:'Room temperature', value:20, group:'Conditions',
     hint:'Only used to convert humidity to moisture content'},
    {id:'rhLo', label:'Driest season, RH %', value:30, group:'Conditions', min:1, step:1, hint:'Winter, heating on'},
    {id:'rhHi', label:'Dampest season, RH %', value:65, group:'Conditions', min:1, step:1, hint:'Late summer'},
    {id:'mcLo', label:'Driest moisture content %', value:6, group:'If working from moisture content', min:0, step:0.1, hint:'Ignored unless Work from is set to moisture content'},
    {id:'mcHi', label:'Dampest moisture content %', value:12, group:'If working from moisture content', min:0, step:0.1, hint:'Ignored unless Work from is set to moisture content'}
  ],

  compute: function (i) {
    var SP = SPEC._species;
    var idx = parseInt(i.species, 10);
    if (!(idx >= 0 && idx < SP.length)) return {ok:false, errors:['Pick a species.']};
    var sp = SP[idx];

    var W = parseFloat(i.width);
    if (!(W > 0)) return {ok:false, errors:['Width must be greater than zero.']};

    // Coefficient : tangentiel pour du debit sur dosse, radial sur quartier.
    // "Pas sur" retient le tangentiel, qui est toujours le plus defavorable.
    var C = (i.cut === 'quarter') ? sp[1] : sp[2];
    var cutName = i.cut === 'quarter' ? 'quartersawn (radial)'
                : i.cut === 'flat' ? 'flatsawn (tangential)'
                : 'unknown - tangential assumed';

    var mcLo, mcHi, emcNote = '';
    if (i.mode === 'mc') {
      mcLo = parseFloat(i.mcLo); mcHi = parseFloat(i.mcHi);
      if (!(isFinite(mcLo) && isFinite(mcHi))) return {ok:false, errors:['Enter both moisture contents.']};
    } else {
      var T = parseFloat(i.temp);
      if (i.tunit === 'F') T = (T - 32) * 5 / 9;
      if (!isFinite(T)) return {ok:false, errors:['Enter a room temperature.']};
      if (T < -1 || T > 60) return {ok:false, errors:['Temperature is outside the range the equation was fitted over. Use something between about 0 and 60 C (32 to 140 F).']};
      var rl = parseFloat(i.rhLo), rh = parseFloat(i.rhHi);
      if (!(rl > 0 && rl < 100 && rh > 0 && rh < 100))
        return {ok:false, errors:['Both humidity figures must be between 1 and 99 percent.']};
      mcLo = SPEC._emc(T, rl); mcHi = SPEC._emc(T, rh);
      emcNote = 'Equilibrium moisture content worked out from the air, not measured.';
    }

    if (mcHi < mcLo) { var t = mcLo; mcLo = mcHi; mcHi = t; }

    var dMC   = mcHi - mcLo;
    var move  = W * C * dMC;
    var wLo   = W * (1 - C * (( (mcLo + mcHi) / 2) - mcLo));
    var wHi   = W * (1 + C * ((mcHi - ((mcLo + mcHi) / 2))));
    var pct   = 100 * move / W;
    var per100 = 100 * C * dMC;

    var warn = [];
    if (mcLo < 6 || mcHi > 14) {
      warn.push('Your range runs from ' + WCfmt(mcLo,1) + '% to ' + WCfmt(mcHi,1) +
        '% moisture content. The coefficient is only validated between 6% and 14% - outside that the figure is indicative, and always on the low side.');
    }
    if (dMC < 0.05) warn.push('The two conditions are almost identical, so there is nothing to allow for. Check you have entered a dry season and a damp one.');
    if (i.cut === 'unsure') warn.push('Cut not specified, so the tangential coefficient is used. If the board turns out to be quartersawn the real movement will be roughly ' + WCfmt(100*sp[1]/sp[2],0) + '% of this.');
    if (i.cut === 'flat' && pct > 2) warn.push('Over 2% across the width. On a panel this wide, flatsawn, a fixed fastening will split it - it has to float.');

    var u = i.unit === 'in' ? 'in' : 'mm';
    var dp = i.unit === 'in' ? 3 : 1;

    return {ok:true, move:move, W:W, wLo:wLo, wHi:wHi, u:u, dp:dp, pct:pct,
      warnings: warn,
      stats:[
        {value: WCfmt(move, dp) + ' ' + u, label:'Total seasonal movement'},
        {value: WCfmt(move/2, dp) + ' ' + u, label:'Each side of mid-position'},
        {value: WCfmt(pct, 2) + '%', label:'Of the width'},
        {value: WCfmt(mcLo,1) + '-' + WCfmt(mcHi,1) + '%', label:'Moisture content range'}
      ],
      tables:[
        {title:'The calculation', head:['Item','Value'], rows:[
          ['Species', sp[0]],
          ['Cut', cutName],
          ['Coefficient used', C.toFixed(5) + ' per 1% moisture content'],
          ['Radial coefficient (quartersawn)', sp[1].toFixed(5)],
          ['Tangential coefficient (flatsawn)', sp[2].toFixed(5)],
          ['Moisture content, dry season', WCfmt(mcLo,1) + '%'],
          ['Moisture content, damp season', WCfmt(mcHi,1) + '%'],
          ['Change in moisture content', WCfmt(dMC,1) + ' percentage points'],
          ['Starting width', WCfmt(W, dp) + ' ' + u],
          ['Movement', WCfmt(move, dp) + ' ' + u + '  (' + WCfmt(per100,2) + ' ' + u + ' per 100 ' + u + ')'],
          ['Narrowest', WCfmt(wLo, dp) + ' ' + u],
          ['Widest', WCfmt(wHi, dp) + ' ' + u]
        ]},
        {title:'What to leave', head:['Detail','Allowance'], rows:[
          ['Panel in a grooved frame, gap at each edge', WCfmt(move/2, dp) + ' ' + u + ' - fit the panel at mid-season, centred'],
          ['Extra groove depth each side, over the gap', WCfmt(move/2, dp) + ' ' + u + ' so the panel never pulls out of the groove'],
          ['Slotted fastening for a top, slot length', WCfmt(move, dp) + ' ' + u + ' beyond the screw shank'],
          ['Drawer side in its opening, total clearance', WCfmt(move, dp) + ' ' + u + ' if the sides are this wide'],
          ['Breadboard end, outer tenons', 'elongate the mortises by ' + WCfmt(move/2, dp) + ' ' + u + ' each way, glue the centre only']
        ]}
      ],
      note: emcNote
    };
  },

  diagram: function (r, i) {
    var W = 560, H = 296, s = SVG.open(W, H);
    var m = 50, avail = W - 2*m - 60;
    var scale = avail / (r.wHi || 1);
    var wLo = r.wLo * scale, wHi = r.wHi * scale, y = 56, h = 78;

    s += SVG.text(W/2, 26, 'Same board, driest season and dampest', 13);

    // Planche au plus etroit, pleine ; la bande gagnee en saison humide est
    // remplie en accentue pour qu'on la voie : a l'echelle vraie elle ne fait
    // que quelques pixels, et un trait fantome seul passait inapercu.
    // Le remplissage passe par style= et non fill= : la regle CSS .ghost{fill:none}
    // l'emporte sur un attribut de presentation.
    s += SVG.rect(m, y, wLo, h, 'part');
    s += SVG.rect(m + wLo, y, Math.max(2, wHi - wLo), h, 'ghost',
                  ' style="fill:var(--accent);fill-opacity:.85;stroke:var(--accent)"');
    s += SVG.text(m + wLo/2, y + h/2 + 4, 'dry ' + WCfmt(r.wLo, r.dp) + ' ' + r.u, 12);

    // Ligne de rappel vers l'etiquette, posee hors de la planche.
    var mid = m + wLo + Math.max(1, (wHi - wLo)/2), ly = y + h + 22;
    s += SVG.line(mid, y + h, mid, ly, ' class="dim"');
    s += SVG.line(mid, ly, m + wHi + 26, ly, ' class="dim"');
    s += SVG.text(m + wHi + 30, ly + 4, WCfmt(r.move, r.dp) + ' ' + r.u, 12, 'start');
    s += SVG.text(m + wHi + 30, ly + 20, 'to scale', 10, 'start');
    s += SVG.text(W/2, y + h + 42, 'damp ' + WCfmt(r.wHi, r.dp) + ' ' + r.u +
                  '   -   ' + WCfmt(r.pct, 2) + '% of the width', 12);

    // Detail du bord : ce que le chiffre veut dire dans une rainure.
    var dy = 208;
    s += SVG.line(m, dy - 18, W - m, dy - 18, ' class="dim" stroke-dasharray="2 4"');
    s += SVG.rect(40, dy, 92, 66, 'ghost', ' style="fill:var(--line);fill-opacity:.45"');
    s += SVG.rect(110, dy + 18, 22, 30, 'ghost', ' style="fill:var(--surface)"');
    s += SVG.rect(120, dy + 23, 148, 20, 'part');
    s += SVG.line(112, dy + 10, 112, dy + 56, ' class="dim" stroke-dasharray="3 3"');
    s += SVG.text(86, dy + 58, 'stile', 11);
    s += SVG.text(200, dy + 37, 'panel', 11);
    s += SVG.text(292, dy + 20, 'gap ' + WCfmt(r.move/2, r.dp) + ' ' + r.u + ' at each edge', 11, 'start');
    s += SVG.text(292, dy + 38, 'plus ' + WCfmt(r.move/2, r.dp) + ' ' + r.u + ' groove depth', 11, 'start');
    s += SVG.text(292, dy + 56, 'edge detail, not to scale', 10, 'start');
    return s + SVG.close();
  },

  // Teneur en eau d'equilibre : Hailwood-Horrobin a deux hydrates,
  // ajustement de Simpson, equation 4-5 du Wood Handbook. T en Celsius.
  _emc: function (T, RH) {
    var h = RH / 100;
    var W  = 349 + 1.29*T + 0.0135*T*T;
    var K  = 0.805 + 0.000736*T - 0.00000273*T*T;
    var K1 = 6.27 - 0.00938*T - 0.000303*T*T;
    var K2 = 1.91 + 0.0407*T - 0.000293*T*T;
    var Kh = K*h;
    return 1800/W * ( Kh/(1-Kh) + (K1*Kh + 2*K1*K2*Kh*Kh) / (1 + K1*Kh + K1*K2*Kh*Kh) );
  },

  _species: [
    ["Alder, red",0.00151,0.00256],
    ["Apple",0.00205,0.00376],
    ["Ash, black",0.00172,0.00274],
    ["Ash, green",0.00169,0.00274],
    ["Ash, Oregon",0.00141,0.00285],
    ["Ash, pumpkin",0.00126,0.00219],
    ["Ash, white",0.00169,0.00274],
    ["Aspen, quaking",0.00119,0.00234],
    ["Basswood, American",0.00230,0.00330],
    ["Beech, American",0.00190,0.00431],
    ["Birch, paper",0.00219,0.00304],
    ["Birch, river",0.00162,0.00327],
    ["Birch, sweet",0.00256,0.00338],
    ["Birch, yellow",0.00256,0.00338],
    ["Buckeye, yellow",0.00123,0.00285],
    ["Butternut",0.00116,0.00223],
    ["Catalpa, northern",0.00085,0.00169],
    ["Cherry, black",0.00126,0.00248],
    ["Chestnut, American",0.00116,0.00234],
    ["Cottonwood, black",0.00123,0.00304],
    ["Cottonwood, eastern",0.00133,0.00327],
    ["Elm, American",0.00144,0.00338],
    ["Elm, cedar",0.00183,0.00419],
    ["Elm, rock",0.00165,0.00285],
    ["Elm, slippery",0.00169,0.00315],
    ["Elm, winged",0.00183,0.00419],
    ["Hackberry",0.00165,0.00315],
    ["Hickory, pecan",0.00169,0.00315],
    ["Hickory, true",0.00259,0.00411],
    ["Holly, American",0.00165,0.00353],
    ["Honeylocust",0.00144,0.00230],
    ["Locust, black",0.00158,0.00252],
    ["Madrone, Pacific",0.00194,0.00451],
    ["Magnolia, cucumbertree",0.00180,0.00312],
    ["Magnolia, southern",0.00187,0.00230],
    ["Magnolia, sweetbay",0.00162,0.00293],
    ["Maple, bigleaf",0.00126,0.00248],
    ["Maple, black",0.00165,0.00353],
    ["Maple, red",0.00137,0.00289],
    ["Maple, silver",0.00102,0.00252],
    ["Maple, sugar (hard maple)",0.00165,0.00353],
    ["Oak, black",0.00123,0.00230],
    ["Oak, California red",0.00123,0.00230],
    ["Oak, live",0.00230,0.00338],
    ["Oak, Oregon white",0.00144,0.00327],
    ["Oak, overcup",0.00183,0.00462],
    ["Oak, red (commercial)",0.00158,0.00369],
    ["Oak, water / laurel / willow",0.00151,0.00350],
    ["Oak, white (commercial)",0.00180,0.00365],
    ["Persimmon, common",0.00278,0.00403],
    ["Sassafras",0.00137,0.00216],
    ["Sweetgum",0.00183,0.00365],
    ["Sycamore, American",0.00172,0.00296],
    ["Tanoak",0.00169,0.00423],
    ["Tupelo, black",0.00176,0.00308],
    ["Tupelo, water",0.00144,0.00267],
    ["Walnut, black",0.00190,0.00274],
    ["Willow, black",0.00112,0.00308],
    ["Willow, Pacific",0.00099,0.00319],
    ["Yellow-poplar (tulipwood)",0.00158,0.00289],
    ["Baldcypress",0.00130,0.00216],
    ["Cedar, Alaska yellow",0.00095,0.00208],
    ["Cedar, Atlantic white",0.00099,0.00187],
    ["Cedar, eastern red",0.00106,0.00162],
    ["Cedar, incense",0.00112,0.00180],
    ["Cedar, northern white",0.00101,0.00229],
    ["Cedar, Port-Orford",0.00158,0.00241],
    ["Cedar, western red",0.00111,0.00234],
    ["Douglas-fir, coast",0.00165,0.00267],
    ["Douglas-fir, interior north",0.00130,0.00241],
    ["Douglas-fir, interior west",0.00165,0.00263],
    ["Fir, balsam",0.00099,0.00241],
    ["Fir, California red",0.00155,0.00278],
    ["Fir, grand",0.00112,0.00245],
    ["Fir, noble",0.00148,0.00293],
    ["Fir, Pacific silver",0.00151,0.00327],
    ["Fir, subalpine",0.00088,0.00259],
    ["Fir, white",0.00112,0.00245],
    ["Hemlock, eastern",0.00102,0.00237],
    ["Hemlock, western",0.00144,0.00274],
    ["Larch, western",0.00155,0.00323],
    ["Pine, eastern white",0.00071,0.00212],
    ["Pine, jack",0.00126,0.00230],
    ["Pine, Jeffrey",0.00148,0.00234],
    ["Pine, loblolly",0.00165,0.00259],
    ["Pine, lodgepole",0.00148,0.00234],
    ["Pine, longleaf",0.00176,0.00263],
    ["Pine, pond",0.00165,0.00259],
    ["Pine, ponderosa",0.00133,0.00216],
    ["Pine, red",0.00130,0.00252],
    ["Pine, shortleaf",0.00158,0.00271],
    ["Pine, slash",0.00187,0.00267],
    ["Pine, sugar",0.00099,0.00194],
    ["Pine, Virginia",0.00144,0.00252],
    ["Pine, western white",0.00141,0.00259],
    ["Redwood, old growth",0.00120,0.00205],
    ["Redwood, second growth",0.00101,0.00229],
    ["Spruce, black",0.00141,0.00237],
    ["Spruce, Engelmann",0.00130,0.00248],
    ["Spruce, red",0.00130,0.00274],
    ["Spruce, Sitka",0.00148,0.00263],
    ["Spruce, white",0.00130,0.00274],
    ["Tamarack",0.00126,0.00259],
    ["Andiroba (crabwood)",0.00137,0.00274],
    ["Angelique",0.00180,0.00312],
    ["Apitong / keruing",0.00243,0.00527],
    ["Avodire",0.00126,0.00226],
    ["Balsa",0.00102,0.00267],
    ["Banak",0.00158,0.00312],
    ["Cativo",0.00078,0.00183],
    ["Cuangare",0.00183,0.00342],
    ["Greenheart",0.00390,0.00430],
    ["Iroko",0.00153,0.00205],
    ["Khaya (African mahogany)",0.00141,0.00201],
    ["Lauan, dark red (Philippine mahogany)",0.00133,0.00267],
    ["Lauan, light red (Philippine mahogany)",0.00126,0.00241],
    ["Limba",0.00151,0.00187],
    ["Mahogany (American)",0.00172,0.00238],
    ["Meranti",0.00126,0.00289],
    ["Obeche",0.00106,0.00183],
    ["Okoume",0.00194,0.00212],
    ["Parana pine",0.00137,0.00278],
    ["Pau marfim",0.00158,0.00312],
    ["Primavera",0.00106,0.00180],
    ["Ramin",0.00133,0.00308],
    ["Santa Maria",0.00187,0.00278],
    ["Spanish-cedar",0.00141,0.00219],
    ["Teak",0.00101,0.00186]
  ]
};
"""}
