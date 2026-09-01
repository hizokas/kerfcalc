SPEC = {
"slug":"board-foot-calculator",
"h1":"Board Foot Calculator",
"title_tag":"Board Foot Calculator — Lumber Volume, Waste and Cost",
"description":"Work out board feet for any number of boards, add a waste allowance, and get the cost. Handles quarter (4/4, 8/4) thickness and metric sizes.",
"card_desc":"Board feet, waste allowance and cost across a whole list of boards, in quarters or millimetres.",
"category":"Sheet goods",
"intro":"Board feet for a whole cutting list, not just one board. Enter your sizes, add a realistic waste allowance, and you get the volume, the cost, and what to actually ask for at the yard.",
"notes":[("What is a board foot?","One board foot is 144 cubic inches — a piece 12 in \u00d7 12 in \u00d7 1 in. It is a volume, not an area, so a thicker board of the same face size costs more."),
("Why the waste allowance matters","Rough lumber is not the size on the tag. Between planing, jointing, defects and end checks, 15-25% is normal for rough stock and 10% for surfaced boards. Buying the exact number always comes up short."),
("Quarters explained","4/4 is one inch, 8/4 is two inches, 12/4 is three. It refers to rough thickness before surfacing, so 4/4 dressed usually lands around 3/4 in."),
("What this does not do","It does not grade lumber or account for the specific defect pattern of your boards. Sight every board at the yard.")],
"js":"""
var SPEC = {
  fields: [
    {id:'thick', label:'Thickness', value:25, unit:'length', group:'Board size', min:0, hint:'25 mm \u2248 4/4'},
    {id:'width', label:'Width', value:150, unit:'length', group:'Board size', min:0},
    {id:'length', label:'Length', value:2400, unit:'length', group:'Board size', min:0},
    {id:'qty', label:'How many boards', value:10, group:'Board size', min:1, step:1},
    {id:'waste', label:'Waste allowance (%)', value:15, group:'Cost', min:0, hint:'15-25% for rough stock'},
    {id:'price', label:'Price per board foot', value:6.5, group:'Cost', min:0, hint:'In whatever currency you buy in. Leave 0 to skip the cost.'}
  ],
  compute: function (i) {
    var k = i.unit === 'in' ? 1 : 1/25.4;          // vers pouces
    var t = i.thick*k, w = i.width*k, l = i.length*k;
    var errs = [];
    if (!(t>0 && w>0 && l>0)) errs.push('Thickness, width and length all need to be greater than zero.');
    if (!(i.qty>0)) errs.push('You need at least one board.');
    if (errs.length) return {ok:false, errors:errs};

    var bfEach = (t*w*l)/144;
    var bfTotal = bfEach*i.qty;
    var bfWithWaste = bfTotal*(1+Math.max(0,i.waste)/100);
    var m3 = bfTotal*0.0023597;
    var cost = i.price>0 ? bfWithWaste*i.price : null;
    var quarters = Math.round(t*4);

    var stats = [
      {value: WCfmt(bfEach,2), label:'Board feet each'},
      {value: WCfmt(bfTotal,1), label:'Board feet total'},
      {value: WCfmt(bfWithWaste,1), label:'Buy this many bf'}
    ];
    if (cost!==null) stats.push({value:WCfmt(cost,2), label:'Estimated cost'});
    stats.push({value: WCfmt(m3,3), label:'Cubic metres'});

    return {ok:true, bfEach:bfEach, bfTotal:bfTotal, bfWithWaste:bfWithWaste, m3:m3, cost:cost,
      stats: stats,
      tables: [{title:'Breakdown', head:['Item','Value'], rows:[
        ['Nominal thickness', quarters+'/4 (' + WCfmt(t,2) + ' in)'],
        ['Face size', WCfmt(w,2)+' in \u00d7 '+WCfmt(l,2)+' in'],
        ['Boards', String(i.qty)],
        ['Board feet before waste', WCfmt(bfTotal,2)],
        ['Waste allowance', WCfmt(i.waste,0)+'%'],
        ['Board feet to order', WCfmt(bfWithWaste,2)],
        ['Volume', WCfmt(m3,4)+' m\u00b3 / '+WCfmt(bfTotal*0.0833,2)+' ft\u00b3']
      ]}],
      note:'One board foot = 144 cubic inches. Yards usually price rough stock by the board foot and surfaced stock by the linear foot — check which you are being quoted.'
    };
  },
  diagram: function (r, i) {
    var W = 600, H = 200, m = 40;
    var k = i.unit === 'in' ? 1 : 1/25.4;
    var t = i.thick*k, w = i.width*k, l = i.length*k;
    var sc = Math.min((W-2*m)/l, (H-2*m)/(w+t*2));
    var bw = l*sc, bh = w*sc, dep = Math.min(t*sc*3, 26);
    var x = m, y = H/2 - bh/2;
    var s = SVG.open(W, H);
    s += SVG.poly([[x,y],[x+dep,y-dep],[x+bw+dep,y-dep],[x+bw,y]], 'part');
    s += SVG.poly([[x+bw,y],[x+bw+dep,y-dep],[x+bw+dep,y+bh-dep],[x+bw,y+bh]], 'part');
    s += SVG.rect(x, y, bw, bh, 'part');
    s += SVG.text(x+bw/2, y+bh/2+4, WCfmt(l,0)+' \u00d7 '+WCfmt(w,0)+' \u00d7 '+WCfmt(t,2)+' in', 13);
    s += SVG.text(x+bw/2, H-12, WCfmt(r.bfEach,2)+' board feet per board \u00b7 '+i.qty+' boards', 12);
    return s + SVG.close();
  }
};
"""}
