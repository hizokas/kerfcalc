SPEC = {
"slug":"stud-wall-layout",
"h1":"Stud Wall Layout Calculator",
"title_tag":"Stud Wall Calculator — Stud Count, Positions and Plate Lengths",
"description":"Calculate stud count, centre positions, clear bay widths, noggins and plate-stock length for a straight wall. Metric and imperial units, with a worked example.",
"card_desc":"Stud centres, clear bay widths and material quantities for a straight wall run.",
"category":"Framing",
"intro":"Count studs and lay out a straight wall from one reference end. Results give stud centres, clear bay widths, noggin quantities and a plate-stock length estimate. Enter the actual stud cut length, excluding plates.",
"notes":[('Centres and marking lines are different', 'The first end stud has its centre at half its thickness. Regular interior centres are at one spacing, two spacings and so on from the wall end. A near-face marking line is half a stud thickness before each centre. Do not subtract half a thickness from the centre itself.'), ('Worked example: a 6,000 mm straight run', 'With 400 mm spacing and 38 mm studs, the centres are 19, 400, 800, 1,200 … 5,600 and 5,981 mm: 16 studs. The first and last clear bays are 343 mm; the 13 middle clear bays are 362 mm. One row therefore has 15 noggins totalling 5,392 mm before cutting allowances. Three plate runs total 18,000 mm, or at least four 4,800 mm stock lengths by total length alone.'), ('How many studs for a 12-foot wall at 16 inches?', 'For a 144-inch run, 16-inch spacing and 1.5-inch actual stud thickness, the centres are 0.75, 16, 32, 48, 64, 80, 96, 112, 128 and 143.25 inches: 10 studs. This straight-run count excludes opening framing, corner assemblies, intersections and spares.'), ('Choosing spacing and matching sheets', 'Enter the spacing specified for your wall and cladding. Metric 400/600 mm and imperial 16/24 inches are different dimensions, not exact conversions. Panel joints must be checked against the actual framing layout. Spacing suitability depends on the wall system, panel rating and applicable design requirements; this tool does not select it.'), ('Cut lengths and buying materials', 'Stud cut length excludes the top and bottom plates. The plate-stock count divides total plate length by stock length and rounds up; it is a lower bound, not a cutting plan. Check joint locations, kerf, offcuts and waste before ordering. Noggins use clear bay widths, not centre spacing.'), ('Openings and unusual end bays', 'Doors, windows, corners and wall intersections need additional framing and their own details. If a regular centre causes overlap with the closing stud, the tool stops instead of returning an impossible layout. This calculator does not size headers or verify structural capacity.')],
"js":"""
var SPEC = {
  fields: [
    {id:'wallLen', label:'Wall length', value:6000, unit:'length', group:'Wall', min:0},
    {id:'hgt', label:'Stud cut length', value:2400, unit:'length', group:'Wall', min:0},
    {id:'spacing', label:'Stud spacing (centres)', value:400, unit:'length', group:'Wall', min:1},
    {id:'studW', label:'Stud thickness', value:38, unit:'length', group:'Wall', min:1, hint:'Use actual material thickness'},
    {id:'plates', label:'Number of plates', value:3, group:'Wall', min:1, step:1, hint:'1 bottom + 2 top is common'},
    {id:'stockLen', label:'Plate stock length', value:4800, unit:'length', group:'Materials', min:1},
    {id:'noggins', label:'Rows of noggins', value:1, group:'Materials', min:0, step:1}
  ],
  compute: function (i) {
    var L=i.wallLen, sp=i.spacing, t=i.studW;
    if(!Number.isFinite(L)||!(L>0)) return {ok:false, errors:['Wall length must be greater than zero.']};
    if(!Number.isFinite(sp)||!(sp>0)) return {ok:false, errors:['Stud spacing must be greater than zero.']};
    if(!Number.isFinite(t)||!(t>0)) return {ok:false, errors:['Stud thickness must be greater than zero.']};
    if(sp<=t) return {ok:false, errors:['Spacing must be larger than the stud thickness.']};

    // Ces positions sont des CENTRES. Le premier montant est en bout de mur
    // (centre a une demi-epaisseur), les suivants tombent sur l'entraxe plein.
    // Le bord d'un panneau pose depuis le bout arrive alors au CENTRE d'un
    // montant, avec une demi-epaisseur d'appui de chaque cote du joint.
    // C'est le tracage qui est recule d'une demi-epaisseur, pas le centre :
    // reculer le centre faisait tomber le joint sur la face exterieure du
    // montant, donc sans aucun appui pour le panneau suivant.
    if(L<2*t) return {ok:false, errors:['The wall must fit two end studs without overlap.']};
    if(!Number.isFinite(i.hgt)||i.hgt<=0||!Number.isFinite(i.stockLen)||i.stockLen<=0) return {ok:false, errors:['Stud cut length and plate stock length must be finite and greater than zero.']};
    if(!Number.isInteger(i.plates)||i.plates<1||i.plates>20||!Number.isInteger(i.noggins)||i.noggins<0||i.noggins>100) return {ok:false, errors:['Use whole numbers: 1–20 plates and 0–100 noggin rows.']};
    if(L/sp>498) return {ok:false, errors:['This layout supports up to 500 studs. Split a longer run into sections.']};
    var pos=[];
    pos.push(t/2);
    for(var x=sp; x<L-t/2; x+=sp) pos.push(x);
    var last=L-t/2;
    var endGap=last-pos[pos.length-1];
    if(endGap>1e-7 && endGap<t-1e-7) return {ok:false, errors:['A regular stud overlaps the closing end stud for these dimensions. This end detail needs a separate layout; adjust the run or spacing to match your actual design.']};
    if (endGap > 1e-7) pos.push(last);
    if(pos.some(function(p,n){return n>0 && p-pos[n-1]<t-1e-7;})) return {ok:false, errors:['These positions overlap near the first end stud. Check the spacing and actual material thickness.']};
    var spare = pos.length>1 ? (pos[pos.length-1]-pos[pos.length-2]) : 0;

    var plates=Math.max(1,Math.round(i.plates));
    var plateLen=L*plates;
    var plateSticks=Math.ceil(plateLen/i.stockLen);
    var nogRows=Math.max(0,Math.round(i.noggins));
    var clearBays=pos.slice(1).map(function(p,n){return Math.max(0,p-pos[n]-t);});
    var nogCount=nogRows*clearBays.filter(function(g){return g>1e-7;}).length;
    var nogLen=nogRows*clearBays.reduce(function(a,b){return a+b;},0);

    var warn=['Plate stock is a length-only minimum. Joint positions, cuts, waste and usable offcuts can increase the purchase quantity.'];
    if (spare>0 && spare<sp*0.4 && pos.length>2) warn.push('The last bay is only '+WCfmt(spare,0)+' — normal at the end of a run, just make sure the closing stud is fixed properly.');

    return {ok:true, pos:pos, clearBays:clearBays, L:L, warnings:warn,
      stats:[
        {value:String(pos.length), label:'Studs'},
        {value:WCfmt(plateLen,0), label:'Plate length total'},
        {value:String(plateSticks), label:'Plate stock minimum'},
        {value:String(nogCount), label:'Noggins'}
      ],
      tables:[
        {title:'Stud positions (centres from the wall end)', head:['#','Centre','Centre to next','Clear bay to next'],
         rows: pos.map(function(p,n){ return [String(n+1), WCfmt(p,1), n<pos.length-1?WCfmt(pos[n+1]-p,1):'-', n<clearBays.length?WCfmt(clearBays[n],1):'-']; })},
        {title:'Material list', head:['Item','Quantity'], rows:[
          ['Studs at '+WCfmt(i.hgt,0)+' long', String(pos.length)],
          ['Plates', String(plates)+' runs, '+WCfmt(plateLen,0)+' total'],
          ['Plate stock at '+WCfmt(i.stockLen,0), String(plateSticks)+' lengths minimum, before cuts / waste'],
          ['Noggins', String(nogCount)+' pieces, '+WCfmt(Math.max(0,nogLen),0)+' total'],
          ['Spacing', WCfmt(sp,0)+' centres'],
          ['Second stud centre', WCfmt(pos[1]!==undefined?pos[1]:pos[0],1)+' (check actual sheet joints against these positions)']
        ]}
      ],
      note:'Positions are to stud centres, measured from the same end of the wall throughout. Mark them all from one end rather than measuring stud to stud, or the error accumulates.'
    };
  },
  diagram: function (r,i){
    var W=760,H=190,m=28,s=SVG.open(W,H);
    var sc=(W-2*m)/r.L, y=42, h=96, t=Math.max(3,i.studW*sc);
    s+=SVG.rect(m,y-10,r.L*sc,8,'part');
    s+=SVG.rect(m,y+h+2,r.L*sc,8,'part');
    r.pos.forEach(function(p,n){
      var x=m+p*sc-t/2;
      s+=SVG.rect(x,y,t,h,'part');
      if(n%2===0||r.pos.length<14) s+=SVG.text(m+p*sc, y+h+26, WCfmt(p,0), 9);
    });
    s+=SVG.text(W/2,20,r.pos.length+' studs at '+WCfmt(i.spacing,0)+' centres over '+WCfmt(r.L,0),12);
    return s+SVG.close();
  }
};
"""}
