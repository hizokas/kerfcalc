SPEC = {
"slug":"stud-wall-layout",
"h1":"Stud Wall Layout Calculator",
"title_tag":"Stud Wall Calculator — Stud Count, Positions and Plate Lengths",
"description":"Stud positions at 400 or 600 mm centres (16 or 24 in), corrected so sheet edges land on a stud, with plate lengths and a full material list.",
"card_desc":"Stud positions with the first-stud correction so sheet edges land on framing, plus the material list.",
"category":"Framing",
"intro":"Stud positions worked out so that sheet edges land on framing, which is the part people get wrong. The first stud is pulled back by half a stud thickness so the sheet breaks on the centre of the fourth stud rather than the edge of it.",
"notes":[("Why the first stud is offset","Sheets are measured from the wall end, studs are measured to centres. If you set the first stud at a full spacing from the end, the sheet edge lands on the far side of a stud with nothing to fix to. Pulling the first one back by half a stud thickness fixes it."),
("400 or 600 centres","600 mm (24 in) uses fewer studs and is common for non-loadbearing partitions. 400 mm (16 in) is stiffer, better under tile or heavy cladding, and required in plenty of loadbearing situations."),
("Openings","Door and window openings need their own trimmers, cripples and a header sized for the load. That is a structural question and deliberately outside this tool."),
("What this does not do","It does not size anything structurally, and it does not tell you whether the wall can be built this way. It lays out a straight run.")],
"js":"""
var SPEC = {
  fields: [
    {id:'wallLen', label:'Wall length', value:6000, unit:'length', group:'Wall', min:0},
    {id:'hgt', label:'Wall height', value:2400, unit:'length', group:'Wall', min:0},
    {id:'spacing', label:'Stud spacing (centres)', value:400, unit:'length', group:'Wall', min:1},
    {id:'studW', label:'Stud thickness', value:38, unit:'length', group:'Wall', min:1, hint:'38 mm = 1.5 in'},
    {id:'plates', label:'Number of plates', value:3, group:'Wall', min:1, step:1, hint:'1 bottom + 2 top is common'},
    {id:'stockLen', label:'Plate stock length', value:4800, unit:'length', group:'Materials', min:1},
    {id:'noggins', label:'Rows of noggins', value:1, group:'Materials', min:0, step:1}
  ],
  compute: function (i) {
    var L=i.wallLen, sp=i.spacing, t=i.studW;
    if(!(L>0)) return {ok:false, errors:['Wall length must be greater than zero.']};
    if(!(sp>0)) return {ok:false, errors:['Stud spacing must be greater than zero.']};
    if(!(t>0)) return {ok:false, errors:['Stud thickness must be greater than zero.']};
    if(sp<=t) return {ok:false, errors:['Spacing must be larger than the stud thickness.']};

    // Ces positions sont des CENTRES. Le premier montant est en bout de mur
    // (centre a une demi-epaisseur), les suivants tombent sur l'entraxe plein.
    // Le bord d'un panneau pose depuis le bout arrive alors au CENTRE d'un
    // montant, avec une demi-epaisseur d'appui de chaque cote du joint.
    // C'est le tracage qui est recule d'une demi-epaisseur, pas le centre :
    // reculer le centre faisait tomber le joint sur la face exterieure du
    // montant, donc sans aucun appui pour le panneau suivant.
    var pos=[];
    pos.push(t/2);
    for(var x=sp; x<L-t/2; x+=sp) pos.push(x);
    var last=L-t/2;
    if (last-pos[pos.length-1] > 1) pos.push(last);
    var spare = pos.length>1 ? (pos[pos.length-1]-pos[pos.length-2]) : 0;

    var plates=Math.max(1,Math.round(i.plates));
    var plateLen=L*plates;
    var plateSticks=Math.ceil(plateLen/Math.max(1,i.stockLen));
    var nogRows=Math.max(0,Math.round(i.noggins));
    var nogCount=nogRows*Math.max(0,pos.length-1);
    var nogLen=nogRows*(L-pos.length*t);

    var warn=[];
    if (spare>0 && spare<sp*0.4 && pos.length>2) warn.push('The last bay is only '+WCfmt(spare,0)+' — normal at the end of a run, just make sure the closing stud is fixed properly.');

    return {ok:true, pos:pos, L:L, warnings:warn,
      stats:[
        {value:String(pos.length), label:'Studs'},
        {value:WCfmt(plateLen,0), label:'Plate length total'},
        {value:String(plateSticks), label:'Plate sticks'},
        {value:String(nogCount), label:'Noggins'}
      ],
      tables:[
        {title:'Stud positions (centres from the wall end)', head:['#','Centre','Bay to next'],
         rows: pos.map(function(p,n){ return [String(n+1), WCfmt(p,1), n<pos.length-1?WCfmt(pos[n+1]-p,1):'-']; })},
        {title:'Material list', head:['Item','Quantity'], rows:[
          ['Studs at '+WCfmt(i.hgt,0)+' long', String(pos.length)],
          ['Plates', String(plates)+' runs, '+WCfmt(plateLen,0)+' total'],
          ['Plate stock at '+WCfmt(i.stockLen,0), String(plateSticks)+' lengths'],
          ['Noggins', String(nogCount)+' pieces, '+WCfmt(Math.max(0,nogLen),0)+' total'],
          ['Spacing', WCfmt(sp,0)+' centres'],
          ['Second stud centre', WCfmt(pos[1]!==undefined?pos[1]:pos[0],1)+' (full spacing, so a sheet edge breaks on a stud centre)']
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
