SPEC = {
"slug":"flooring-plank-calculator",
"h1":"Flooring Plank Layout Calculator",
"title_tag":"Flooring Calculator — Plank Rows, Last Row Width, Stagger and Waste",
"description":"Rows of planks, the width of the last row, end-joint stagger, boxes to buy and waste allowance for laminate, engineered and solid flooring.",
"card_desc":"Rows, last-row width, joint stagger and boxes to buy for any plank flooring.",
"category":"Finishing",
"intro":"The last row of flooring is the one that ruins a job \u2014 a 20 mm sliver against the wall that no one can fit and everyone can see. This works out the row widths first, tells you to rip the first row instead, and gives you the stagger and the boxes to buy.",
"notes":[("Why you rip the first row","If the last row comes out narrower than about a third of a plank, split the difference: take the shortfall, add a full plank width, halve it, and rip the first row to that. Both edge rows then look deliberate instead of one looking like a mistake."),
("Expansion gap is not optional","Wood and laminate move with humidity. The gap around the perimeter lets them, and the skirting hides it. Skip it and the floor peaks in the middle of summer."),
("Staggering end joints","End joints in adjacent rows should be well offset \u2014 a common rule of thumb is at least twice the plank width, never less than 150 mm. Rows that line up read as a repeating pattern and weaken the floor."),
("What this does not do","It lays out a rectangular room. Doorways, hearths, islands and diagonal layouts all change the count, and diagonal laying adds roughly 15 percent waste on its own.")],
"js":"""
var SPEC = {
  fields: [
    {id:'roomL', label:'Room length', value:5000, unit:'length', group:'Room', min:0,
     hint:'Along the direction of the planks'},
    {id:'roomW', label:'Room width', value:4000, unit:'length', group:'Room', min:0},
    {id:'gap', label:'Expansion gap', value:10, unit:'length', group:'Room', min:0},
    {id:'plankL', label:'Plank length', value:1200, unit:'length', group:'Plank', min:0},
    {id:'plankW', label:'Plank width', value:190, unit:'length', group:'Plank', min:0},
    {id:'stagger', label:'Minimum end-joint stagger', value:300, unit:'length', group:'Plank', min:0},
    {id:'perBox', label:'Planks per box', value:8, group:'Ordering', min:1, step:1},
    {id:'waste', label:'Waste allowance (%)', value:10, group:'Ordering', min:0}
  ],
  compute: function (i) {
    var L=i.roomL-2*i.gap, Wd=i.roomW-2*i.gap;
    if (!(i.roomL>0 && i.roomW>0)) return {ok:false, errors:['Room dimensions must be greater than zero.']};
    if (!(L>0 && Wd>0)) return {ok:false, errors:['The expansion gap leaves no floor. Check the numbers.']};
    if (!(i.plankL>0 && i.plankW>0)) return {ok:false, errors:['Plank dimensions must be greater than zero.']};

    var fullRows = Math.floor(Wd/i.plankW);
    var lastRow = Wd - fullRows*i.plankW;
    var rows = lastRow > 0.5 ? fullRows+1 : fullRows;

    // Si la derniere rangee est trop etroite, on repartit sur la premiere
    var ripFirst = null;
    if (lastRow > 0.5 && lastRow < i.plankW/3) {
      ripFirst = (lastRow + i.plankW)/2;
    }

    var perRow = Math.ceil(L/i.plankL);
    var totalPlanks = rows*perRow;
    // La surface est annoncee en m2 : il faut convertir la saisie, sinon le
    // mode pouces divise par 645 (25,4 au carre).
    var toMm = i.unit === 'in' ? 25.4 : 1;
    var area = (i.roomL*toMm)*(i.roomW*toMm)/1e6;
    var withWaste = Math.ceil(totalPlanks*(1+Math.max(0,i.waste)/100));
    var boxes = Math.ceil(withWaste/Math.max(1,i.perBox));

    // Le decalage de coupe de depart qui garantit l'ecart entre joints
    var offsetStep = Math.max(i.stagger, i.plankW*2);
    var startCuts = [];
    var nPattern = Math.max(2, Math.round(i.plankL/offsetStep));
    for (var k=0;k<Math.min(rows,nPattern);k++) startCuts.push(WCfmt(i.plankL*(k%nPattern)/nPattern,0));

    var warn=[];
    if (ripFirst) warn.push('The last row would be only '+WCfmt(lastRow,0)+' wide. Rip the first row to '+WCfmt(ripFirst,0)+' instead, and both edges will match.');
    if (offsetStep > i.plankL/2) warn.push('Your stagger is more than half a plank \u2014 with this plank length the pattern will repeat every other row.');

    return {ok:true, rows:rows, perRow:perRow, lastRow:lastRow, ripFirst:ripFirst,
      totalPlanks:totalPlanks, boxes:boxes, L:L, Wd:Wd, area:area,
      warnings: warn,
      stats:[
        {value: String(rows), label:'Rows'},
        {value: String(withWaste), label:'Planks to buy'},
        {value: String(boxes), label:'Boxes'},
        {value: WCfmt(area,2), label:'m2 of floor'}
      ],
      tables:[{title:'Layout', head:['Item','Value'], rows:[
        ['Room', WCfmt(i.roomL,0)+' \u00d7 '+WCfmt(i.roomW,0)],
        ['Laying area after gaps', WCfmt(L,0)+' \u00d7 '+WCfmt(Wd,0)],
        ['Full rows', String(fullRows)],
        ['Last row width', WCfmt(lastRow,1)],
        ['Rip the first row to', ripFirst ? WCfmt(ripFirst,1) : 'not needed'],
        ['Planks per row', String(perRow)],
        ['Planks needed', String(totalPlanks)],
        ['With '+WCfmt(i.waste,0)+'% waste', String(withWaste)],
        ['Boxes of '+String(i.perBox), String(boxes)],
        ['Starting cut lengths', startCuts.join(', ')]
      ]}],
      note:'Start each row with a different offcut length so end joints never line up. The starting cuts above give a repeating pattern that respects your stagger.'
    };
  },
  diagram: function (r, i) {
    var W=640,H=360,m=28,s=SVG.open(W,H);
    var sc=Math.min((W-2*m)/i.roomL,(H-2*m-24)/i.roomW);
    var x0=m,y0=m+16,rw=i.roomL*sc,rh=i.roomW*sc;
    s+=SVG.rect(x0,y0,rw,rh,'ghost');
    var g=i.gap*sc, pw=i.plankW*sc, pl=i.plankL*sc;
    var nPattern=Math.max(2,Math.round(i.plankL/Math.max(i.stagger,i.plankW*2)));
    for (var row=0; row<r.rows; row++){
      var yy=y0+g+row*pw;
      if (yy > y0+rh-g) break;
      var hh=Math.min(pw, y0+rh-g-yy);
      var off=(i.plankL*(row%nPattern)/nPattern)*sc;
      var xx=x0+g-off;
      while (xx < x0+rw-g){
        var x1=Math.max(xx,x0+g), x2=Math.min(xx+pl,x0+rw-g);
        if (x2>x1) s+=SVG.rect(x1,yy,x2-x1,Math.max(0,hh-1),'part');
        xx+=pl;
      }
    }
    s+=SVG.text(W/2,20,r.rows+' rows  \u00b7  '+r.perRow+' planks per row  \u00b7  '+r.boxes+' boxes',13);
    s+=SVG.text(W/2,H-8, r.ripFirst ? 'rip the first row to '+WCfmt(r.ripFirst,0) : 'last row '+WCfmt(r.lastRow,0)+' wide', 12);
    return s+SVG.close();
  }
};
"""}
