SPEC = {
"slug":"fence-post-planner",
"h1":"Fence Post Spacing Calculator",
"title_tag":"Fence Calculator — Post Spacing, Rails, Pickets and Concrete",
"description":"Even post spacing across a fence run with no short bay at the end, plus rails, pickets, concrete per hole and a full material list.",
"card_desc":"Even post spacing with no stubby last bay, plus rails, pickets and concrete per hole.",
"category":"Framing",
"intro":"Set posts at a fixed spacing and the last bay ends up a stubby half-width that looks wrong for the life of the fence. This works backwards instead: it finds the bay size closest to your target that divides the run exactly.",
"notes":[("Why even bays matter","A run of 2.4 m bays finishing with a 0.7 m offcut is the first thing anyone notices. Dividing the run evenly costs nothing and the difference in bay size is usually under 100 mm."),
("How deep should posts go?","A common rule of thumb is a quarter to a third of the above-ground height, and at least below the local frost line. Ground conditions, exposure and fence height all change this."),
("Picket spacing","The gap is set by taste and privacy, but pickets and gaps have to divide the bay evenly or the last one is a rip. The tool adjusts the gap slightly to make it come out."),
("What this does not do","It does not check whether the fence is within a boundary, needs consent, or can take the wind load at that height. All three catch people out.")],
"js":"""
var SPEC = {
  fields: [
    {id:'runLen', label:'Total fence run', value:20000, unit:'length', group:'Fence', min:0},
    {id:'target', label:'Target bay spacing', value:2400, unit:'length', group:'Fence', min:1},
    {id:'postW', label:'Post width', value:100, unit:'length', group:'Fence', min:1},
    {id:'height', label:'Fence height above ground', value:1800, unit:'length', group:'Fence', min:0},
    {id:'rails', label:'Rails per bay', value:3, group:'Materials', min:0, step:1},
    {id:'picketW', label:'Picket width', value:90, unit:'length', group:'Materials', min:0, hint:'0 to skip pickets'},
    {id:'picketGap', label:'Target gap between pickets', value:10, unit:'length', group:'Materials', min:0},
    {id:'holeDia', label:'Post hole diameter', value:300, unit:'length', group:'Materials', min:0},
    {id:'holeDepth', label:'Post hole depth', value:600, unit:'length', group:'Materials', min:0}
  ],
  compute: function (i) {
    var L=i.runLen;
    if(!(L>0)) return {ok:false, errors:['Fence run must be greater than zero.']};
    if(!(i.target>0)) return {ok:false, errors:['Target bay spacing must be greater than zero.']};
    if(i.target>L) return {ok:false, errors:['The target bay is longer than the whole run.']};

    var bays=Math.max(1, Math.round(L/i.target));
    var bay=L/bays;
    var posts=bays+1;
    var clear=bay-i.postW;
    if(clear<=0) return {ok:false, errors:['Posts are wider than the bay — increase the spacing or use narrower posts.']};

    var railLen=bays*i.rails*clear;
    var pickets=0, gapActual=0;
    if(i.picketW>0){
      var pitch=i.picketW+Math.max(0,i.picketGap);
      var perBay=Math.max(1, Math.round((clear+Math.max(0,i.picketGap))/pitch));
      gapActual=(clear-perBay*i.picketW)/Math.max(1,(perBay-1));
      pickets=perBay*bays;
    }
    var k=i.unit==='in'?0.0254:0.001;
    var holeVol=Math.PI*Math.pow(i.holeDia*k/2,2)*(i.holeDepth*k);
    var postVol=Math.pow(i.postW*k,2)*(i.holeDepth*k);
    var concrete=Math.max(0,(holeVol-postVol))*posts;

    var warn=[];
    if (Math.abs(bay-i.target)>i.target*0.15) warn.push('Even bays come out at '+WCfmt(bay,0)+', which is a fair way from your '+WCfmt(i.target,0)+' target. Adding or removing one bay may suit better.');
    if (i.holeDepth < i.height/4) warn.push('Hole depth is under a quarter of the fence height — shallow for a fence this tall in most ground.');

    return {ok:true, bays:bays, bay:bay, posts:posts, clear:clear, L:L, warnings:warn,
      stats:[
        {value:String(posts), label:'Posts'},
        {value:WCfmt(bay,0), label:'Bay spacing'},
        {value:String(bays), label:'Bays'},
        {value:WCfmt(concrete,3), label:'m3 of concrete'}
      ],
      tables:[
        {title:'Post positions (centres from the start)', head:['#','Centre'],
         rows: Array.apply(null,{length:posts}).map(function(_,n){ return [String(n+1), WCfmt(n*bay,1)]; })},
        {title:'Material list', head:['Item','Quantity'], rows:[
          ['Posts', String(posts)+' at '+WCfmt(i.height+i.holeDepth,0)+' long'],
          ['Bays', String(bays)+' at '+WCfmt(bay,1)+' centres'],
          ['Clear span between posts', WCfmt(clear,1)],
          ['Rails', String(bays*i.rails)+' at '+WCfmt(clear,0)+' ('+WCfmt(railLen,0)+' total)'],
          ['Pickets', i.picketW>0 ? String(pickets)+' at '+WCfmt(i.picketW,0)+' wide, gap '+WCfmt(gapActual,1) : 'none'],
          ['Concrete per hole', WCfmt(Math.max(0,holeVol-postVol),4)+' m3'],
          ['Concrete total', WCfmt(concrete,3)+' m3']
        ]}
      ],
      note:'Post positions are centres measured from the start of the run. Set them all from a string line rather than post to post.'
    };
  },
  diagram: function (r,i){
    var W=760,H=180,s=SVG.open(W,H),m=30;
    var sc=(W-2*m)/r.L, y=48, h=90, pw=Math.max(4,i.postW*sc);
    for(var n=0;n<r.posts;n++){
      var x=m+n*r.bay*sc-pw/2;
      s+=SVG.rect(x,y,pw,h,'part');
      if(r.posts<=16) s+=SVG.text(m+n*r.bay*sc, y+h+22, WCfmt(n*r.bay,0), 9);
    }
    for(var b=0;b<r.bays;b++){
      var x1=m+b*r.bay*sc+pw/2, x2=m+(b+1)*r.bay*sc-pw/2;
      for(var q=1;q<=Math.max(1,i.rails);q++){
        var yy=y+h*q/(Math.max(1,i.rails)+1);
        s+=SVG.line(x1,yy,x2,yy,' class="dim"');
      }
    }
    s+=SVG.text(W/2,24, r.posts+' posts, '+r.bays+' equal bays of '+WCfmt(r.bay,0)+' over '+WCfmt(r.L,0), 12);
    return s+SVG.close();
  }
};
"""}
