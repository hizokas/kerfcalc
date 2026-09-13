SPEC = {'slug': 'roof-area-calculator',
 'h1': 'Roof Area & Material Calculator',
 'title_tag': 'Roof Area Calculator — Sloped Area, Squares, Bundles and Hips',
 'description': 'True sloped roof area from the footprint and pitch, in squares and square metres, with bundle counts, '
                'ridge and hip lengths, and waste allowance.',
 'card_desc': 'True sloped area from footprint and pitch, with squares, bundles, ridge and hip lengths.',
 'category': 'Framing',
 'intro': 'Calculate the sloped area of a rectangular gable or equal-pitch hip roof. Enter the wall footprint and a '
          'horizontal overhang on all four sides, or use the full roof plan dimensions with zero overhang. Bundle '
          'coverage must come from your selected product.',
 'notes': [('From horizontal plan to sloped area',
            'For pitch R:12, multiply the horizontal roof plan area by √(1 + (R/12)²). At 6:12 the multiplier is '
            '1.118034; at 12:12 it is 1.414214. Both roof types give the same total area for the same rectangular plan '
            'and uniform pitch.'),
           ('Worked example: a 12 m × 8 m roof footprint',
            'A 400 mm horizontal overhang on all sides gives a 12.8 × 8.8 m roof plan: 112.64 m². At 6:12 pitch the '
            'sloped area is 125.94 m². With 10% extra, allow 138.53 m². An example product covering 3.1 m² per bundle '
            'needs 45 bundles. Use the unrounded area for ordering, then round up the final bundle count.'),
           ('Gable and hip lengths',
            'For the example gable, the ridge follows the length input and is 12.8 m. Its two eaves total 25.6 m; the '
            'four sloping rake edges total 19.68 m. For an equal-pitch hip roof over the same plan, the ridge is 4 m, '
            'the four hips total 26.4 m and eaves total 43.2 m. A square hip plan has a point apex and zero ridge '
            'length.'),
           ('Footprint and overhang',
            'The overhang input is a horizontal plan distance, added twice to both footprint dimensions. On a gable '
            'roof this assumes the same projection at eaves and gable ends. For unequal projections, enter the '
            'complete roof plan length and width and set overhang to zero. The cross-section spans the width for a '
            'gable and the shorter dimension for a hip roof.'),
           ('Squares, bundle coverage and extra material',
            'One roofing square is exactly 100 ft², or 9.290304 m². Use installed coverage from the package, not a '
            'fixed bundles-per-square assumption; see <a '
            'href="https://www.gaf.com/en-us/blog/your-home/what-is-a-roofing-square-f955fe18-daf9-4b0c-b78e-28ca178caa35">GAF’s '
            'explanation of roofing squares</a>. Extra percentage is chosen by you; 10% is an example. Ridge and hip '
            'caps, starter strips, underlayment, flashings and fasteners are separate items, not included in the '
            'field-shingle bundle count.'),
           ('Limits of this model',
            'The hip calculation assumes equal pitches on every plane, a rectangular plan and a common eaves level. '
            'Intersecting roofs, valleys, dormers, unequal slopes and stepped eaves need a plane-by-plane take-off. '
            'This is a geometry and material estimate, not structural sizing or a check that a covering is suitable '
            'for the pitch. Length inputs follow mm/inches; coverage and output areas stay in m².')],
 'js': '\n'
       'var SPEC = {\n'
       '  fields: [\n'
       "    {id:'a', label:'Footprint length', value:12000, unit:'length', group:'Roof', min:0},\n"
       "    {id:'b', label:'Footprint width', value:8000, unit:'length', group:'Roof', min:0},\n"
       "    {id:'pitch', label:'Pitch, rise in 12', value:6, group:'Roof', min:0, hint:'6 means 6:12'},\n"
       "    {id:'shape', label:'Roof shape', type:'select', value:'gable', group:'Roof', options:[\n"
       "      {value:'gable', label:'Simple gable'},\n"
       "      {value:'hip', label:'Hip roof'}]},\n"
       "    {id:'overhang', label:'Horizontal overhang on all sides', value:400, unit:'length', group:'Roof', min:0},\n"
       "    {id:'waste', label:'Waste allowance (%)', value:10, group:'Materials', min:0},\n"
       "    {id:'perBundle', label:'Coverage per bundle (m2)', value:3.1, group:'Materials', min:0.1, hint:'Installed "
       "coverage from product label; always m2'}\n"
       '  ],\n'
       '  compute: function (i) {\n'
       "    if (['a','b','pitch','perBundle'].some(function(f){return !Number.isFinite(i[f]) || i[f]<=0;})) return "
       "{ok:false, errors:['Enter finite, positive footprint dimensions, pitch and bundle coverage.']};\n"
       "    if (['overhang','waste'].some(function(f){return !Number.isFinite(i[f]) || i[f]<0;}) || i.waste>100) "
       "return {ok:false, errors:['Overhang must be finite and non-negative; extra material must be from 0 to "
       "100%.']};\n"
       "    if (['gable','hip'].indexOf(i.shape)===-1) return {ok:false, errors:['Select gable or hip roof.']};\n"
       "    var k=i.unit==='in'?0.0254:0.001;\n"
       '    var A=i.a*k+2*i.overhang*k, B=i.b*k+2*i.overhang*k;\n'
       '    var slope=Math.hypot(1,i.pitch/12);\n'
       '    var deg=Math.atan(i.pitch/12)*180/Math.PI;\n'
       '    var footprint=A*B;\n'
       '    var area=footprint*slope;\n'
       '    var withWaste=area*(1+Math.max(0,i.waste)/100);\n'
       '    var squares=withWaste/9.290304;\n'
       '    var bundles=Math.ceil(withWaste/i.perBundle);\n'
       '\n'
       '    var ridge, hips=0, eaves, rakes=0;\n'
       "    if (i.shape==='gable') { ridge=A; eaves=2*A; rakes=2*B*slope; }\n"
       '    else { var shorter=Math.min(A,B); ridge=Math.abs(A-B);\n'
       '      hips=4*Math.hypot(shorter/2,shorter/2,(shorter/2)*(i.pitch/12));\n'
       '      eaves=2*(A+B);\n'
       '    }\n'
       '    if (![A,B,area,withWaste,slope,ridge,hips,eaves,rakes,squares].every(Number.isFinite) || !(area>0) || '
       "!Number.isSafeInteger(bundles) || bundles<1) return {ok:false, errors:['The result is outside the supported "
       "range. Check the dimensions and bundle coverage.']};\n"
       '\n'
       '    return {ok:true, area:area, withWaste:withWaste, slope:slope, deg:deg, ridge:ridge, hips:hips, '
       'eaves:eaves, rakes:rakes, bundles:bundles, squares:squares, A:A, B:B,\n'
       '      stats:[\n'
       "        {value:WCfmt(area,1), label:'m2 of roof'},\n"
       "        {value:WCfmt(squares,1), label:'Squares to order'},\n"
       "        {value:String(bundles), label:'Bundles'},\n"
       "        {value:WCfmt(slope,3), label:'Slope factor'}\n"
       '      ],\n'
       "      tables:[{title:'Breakdown', head:['Item','Value'], rows:[\n"
       "        ['Footprint incl. overhang', WCfmt(A,2)+' x '+WCfmt(B,2)+' m = '+WCfmt(footprint,1)+' m2'],\n"
       "        ['Pitch', i.pitch+':12 = '+WCfmt(deg,2)+' degrees'],\n"
       "        ['Slope factor', WCfmt(slope,4)+' (adds '+WCfmt((slope-1)*100,1)+'%)'],\n"
       "        ['True roof area', WCfmt(area,2)+' m2 / '+WCfmt(area/0.09290304,0)+' ft2'],\n"
       "        ['With '+WCfmt(i.waste,0)+'% waste', WCfmt(withWaste,2)+' m2'],\n"
       "        ['Roofing squares', WCfmt(squares,2)],\n"
       "        ['Bundles at '+i.perBundle+' m2', String(bundles)],\n"
       "        ['Ridge length', WCfmt(ridge,2)+' m'],\n"
       "        ['Eaves total', WCfmt(eaves,2)+' m'],\n"
       "        ['Sloping rake edges total', i.shape==='gable'?WCfmt(rakes,2)+' m':'none on this hip model'],\n"
       "        ['Hip length total', i.shape==='hip'?WCfmt(hips,2)+' m':'not a hip roof']\n"
       '      ]}]\n'
       '    };\n'
       '  },\n'
       '  diagram: function (r,i){\n'
       '    var W=560,H=230,s=SVG.open(W,H),m=50;\n'
       '    var ratio=i.pitch/12, run=Math.min((W-2*m)/2,100/ratio), rise=run*ratio;\n'
       "    var left=W/2-run, right=W/2+run, span=i.shape==='hip'?Math.min(r.A,r.B):r.B;\n"
       '    var baseY=H-52, apexY=baseY-rise;\n'
       "    s+=SVG.poly([[left,baseY],[W/2,apexY],[right,baseY]],'part');\n"
       '    s+=SVG.line(left,baseY,right,baseY,\' class="dim"\');\n'
       "    s+=SVG.text(W/2,baseY+22,'span '+WCfmt(span,2)+' m',11);\n"
       "    s+=SVG.text(W/2,apexY-12, i.pitch+':12  ('+WCfmt(r.deg,1)+' deg)',12);\n"
       "    s+=SVG.text(W/2,26,'Slope factor '+WCfmt(r.slope,3)+' - footprint x '+WCfmt(r.slope,3)+' = real "
       "area',12);\n"
       "    s+=SVG.text(W/2,H-16, WCfmt(r.area,1)+' m2 of roof, '+WCfmt(r.withWaste,1)+' m2 to order',12);\n"
       '    return s+SVG.close();\n'
       '  }\n'
       '};\n'}
