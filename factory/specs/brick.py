SPEC = {'slug': 'brick-block-calculator',
 'h1': 'Brick &amp; Block Quantity Calculator',
 'title_tag': 'Brick & Block Calculator — Quantity, Mortar Volume and Bags',
 'description': 'Estimate bricks or blocks from wall area, openings and joint size. Calculate geometric mortar volume '
                'and premixed bags using your product yield.',
 'card_desc': 'Brick and block quantities, joint volume and product-specific mortar bags.',
 'category': 'Finishing',
 'intro': 'Estimate bricks or blocks for a rectangular wall using the actual unit size and mortar joints. Deduct '
          'openings, choose an ordering allowance and enter your premixed mortar yield to estimate bags.',
 'notes': [('How many bricks per square metre?',
            'Divide 1 by (brick length + joint) × (brick height + joint), with dimensions in metres. A 215 × 65 mm '
            'brick with 10 mm joints gives 59.26 units/m² per skin, commonly rounded to about 60. This is an area '
            'estimate; end joints, bond, corners, cuts and special bricks need a separate take-off.'),
           ('Worked example: a 5 m × 2.4 m wall',
            'With no openings, 215 × 65 × 102.5 mm bricks and 10 mm joints, one skin has 12 m² of face area and an '
            'estimated 711.11 bricks. A 5% breakage allowance gives 747 bricks to order. The geometric joint volume is '
            '0.2114 m³; adding 15% gives 0.2431 m³. If your selected premixed mortar yields 12 litres per bag, that is '
            '21 bags. The 12-litre yield is an example, not a default for all products.'),
           ('Separate skins and solid collar joints',
            'Skins must use the same unit dimensions. For an outer brick skin and an inner block skin, calculate each '
            'separately. Collar joint thickness defaults to zero: enter only a deliberately mortar-filled joint '
            'between adjacent skins. Never enter an empty or insulated cavity as a mortar joint.'),
           ('What the mortar estimate includes',
            'This geometry assumes rectangular units and full-width bed and vertical joints. It excludes frogs, '
            'perforation filling, hollow-block face-shell bedding, grout and edge effects. Enter an allowance '
            'appropriate to your product and method. For hollow blocks or specialist systems, use the manufacturer’s '
            'mortar consumption figures.'),
           ('Which sand, cement or bagged mortar?',
            'No mortar mix is prescribed. For premixed mortar, enter the mixed-volume yield in litres per bag from the '
            'selected product data sheet. Zero leaves the bag count unset. Sand and cement cannot be reliably inferred '
            'from wet joint volume alone: mix specification, moisture and batch yield matter. See the <a '
            'href="https://www.ibstock.co.uk/resources-hub">Ibstock technical resources</a> for brickwork guidance and '
            'confirm your mortar product specification.'),
           ('Units and drawing',
            'Wall and unit lengths follow the mm/inch selector. Opening area stays in square metres, and bag yield '
            'stays in litres. The drawing is a capped schematic of the gross wall; it does not locate openings or '
            'provide a laying plan.')],
 'js': '\n'
       'var SPEC = {\n'
       '  fields: [\n'
       "    {id:'wallL', label:'Wall length', value:5000, unit:'length', group:'Wall', min:0},\n"
       "    {id:'wallH', label:'Wall height', value:2400, unit:'length', group:'Wall', min:0},\n"
       "    {id:'skins', label:'Number of skins', value:1, group:'Wall', min:1, step:1},\n"
       "    {id:'collar', label:'Mortar-filled collar joint only', value:0, unit:'length', group:'Wall', min:0},\n"
       "    {id:'openings', label:'Openings to deduct (m2)', value:0, group:'Wall', min:0},\n"
       "    {id:'unitL', label:'Unit length', value:215, unit:'length', group:'Unit', min:0},\n"
       "    {id:'unitH', label:'Unit height', value:65, unit:'length', group:'Unit', min:0},\n"
       "    {id:'unitW', label:'Unit width (thickness)', value:102.5, unit:'length', group:'Unit', min:0},\n"
       "    {id:'joint', label:'Joint thickness', value:10, unit:'length', group:'Unit', min:0},\n"
       "    {id:'waste', label:'Breakage allowance (%)', value:5, group:'Ordering', min:0},\n"
       "    {id:'bagYield', label:'Premixed yield (litres/bag; 0 = skip)', value:0, group:'Ordering', min:0},\n"
       "    {id:'mortarWaste', label:'Mortar allowance (%)', value:15, group:'Ordering', min:0}\n"
       '  ],\n'
       '  compute: function (i) {\n'
       "    var positive=['wallL','wallH','unitL','unitH','unitW'];\n"
       "    var nonnegative=['joint','openings','waste','mortarWaste','bagYield'];\n"
       '    if (positive.some(function(f){return !Number.isFinite(i[f]) || i[f]<=0;})) return {ok:false, '
       "errors:['Enter finite, positive wall and unit dimensions.']};\n"
       '    if (nonnegative.some(function(f){return !Number.isFinite(i[f]) || i[f]<0;})) return {ok:false, '
       "errors:['Openings, joints, allowances and bag yield must be finite and non-negative.']};\n"
       "    if (!Number.isInteger(i.skins) || i.skins<1 || i.skins>20) return {ok:false, errors:['Enter a whole number "
       "of skins from 1 to 20.']};\n"
       "    if (i.skins>1 && (!Number.isFinite(i.collar) || i.collar<0)) return {ok:false, errors:['Enter a finite, "
       "non-negative mortar-filled collar joint.']};\n"
       "    if (i.waste>100 || i.mortarWaste>100) return {ok:false, errors:['Allowances must be between 0 and 100 "
       "percent.']};\n"
       "    var k = i.unit === 'in' ? 0.0254 : 0.001;\n"
       '    var L=i.wallL*k, Hh=i.wallH*k, uL=i.unitL*k, uH=i.unitH*k, uW=i.unitW*k, j=i.joint*k;\n'
       '    var skins=i.skins, collar=skins>1 ? i.collar*k : 0;\n'
       '    var area=L*Hh-i.openings;\n'
       "    if (!(area>0)) return {ok:false, errors:['Openings must be smaller than the gross wall area.']};\n"
       '\n'
       '    var perM2 = 1/((uL+j)*(uH+j));\n'
       '    var units = area*perM2*skins;\n'
       '    var unitsOrder = Math.ceil(units*(1+Math.max(0,i.waste)/100));\n'
       '\n'
       '    var wallVol = area*(uW*skins + collar*(skins-1));\n'
       '    var unitVol = units*(uL*uH*uW);\n'
       '    var mortar = Math.max(0, wallVol - unitVol);\n'
       '    var mortarOrder = mortar*(1+Math.max(0,i.mortarWaste)/100);\n'
       '\n'
       '    var bags=i.bagYield>0 ? Math.ceil(mortarOrder*1000/i.bagYield) : null;\n'
       '    if (![perM2,units,unitsOrder,area,mortarOrder].every(Number.isFinite) || !Number.isSafeInteger(unitsOrder) '
       "|| unitsOrder<1 || (bags!==null && !Number.isSafeInteger(bags))) return {ok:false, errors:['The result is "
       "outside the supported range; check dimensions and product yield.']};\n"
       '\n'
       '    var warn=[];\n'
       "    if (j > uH*0.3) warn.push('The joint is very thick relative to the unit height — check the numbers.');\n"
       '\n'
       '    return {ok:true, perM2:perM2, units:units, unitsOrder:unitsOrder, mortarOrder:mortarOrder,\n'
       '      mortar:mortar, bags:bags, collar:collar, area:area, L:L, Hh:Hh, skins:skins,\n'
       '      warnings: warn,\n'
       '      stats:[\n'
       "        {value: WCfmt(perM2,1), label:'Units per m2'},\n"
       "        {value: String(unitsOrder), label:'Units to order'},\n"
       "        {value: WCfmt(mortarOrder,3), label:'m3 of mortar'},\n"
       "        {value: bags===null ? '—' : String(bags), label:'Premixed mortar bags'}\n"
       '      ],\n'
       "      tables:[{title:'Take-off', head:['Item','Value'], rows:[\n"
       "        ['Wall face area', WCfmt(area,2)+' m2'],\n"
       "        ['Skins', String(skins)],\n"
       "        ['Unit size', WCfmt(i.unitL,1)+' × '+WCfmt(i.unitH,1)+' × '+WCfmt(i.unitW,1)],\n"
       "        ['Joint', WCfmt(i.joint,1)],\n"
       "        ['Units per m2 per skin', WCfmt(perM2,2)],\n"
       "        ['Units needed', WCfmt(units,0)],\n"
       "        ['With '+WCfmt(i.waste,0)+'% breakage', String(unitsOrder)],\n"
       "        ['Mortar volume', WCfmt(mortar,4)+' m3'],\n"
       "        ['With '+WCfmt(i.mortarWaste,0)+'% allowance', WCfmt(mortarOrder,3)+' m3'],\n"
       "        ['Mortar-filled collar between skins', WCfmt(collar*1000,1)+' mm'],\n"
       "        ['Premixed mortar bags', bags===null ? 'Enter product yield to calculate' : String(bags)+' at "
       "'+WCfmt(i.bagYield,2)+' litres/bag']\n"
       '      ]}],\n'
       "      note:'Area-based estimate, not an exact bond or cut plan. Openings remain in m² in both unit modes. Use "
       "product-specific mortar consumption for hollow blocks and special bedding systems.'\n"
       '    };\n'
       '  },\n'
       '  diagram: function (r, i) {\n'
       '    var W=600,H=300,m=40,s=SVG.open(W,H);\n'
       '    var sc=Math.min((W-2*m)/r.L,(H-110)/Math.max(r.Hh,0.1));\n'
       '    var x0=m,y0=60,ww=r.L*sc,wh=r.Hh*sc;\n'
       "    var k = i.unit === 'in' ? 0.0254 : 0.001;\n"
       '    var bw=(i.unitL*k+i.joint*k)*sc, bh=(i.unitH*k+i.joint*k)*sc;\n'
       '    var rows=Math.min(40,Math.floor(wh/Math.max(bh,1)));\n'
       '    var dense=ww/bw>100 || wh/bh>40;\n'
       "    if (dense) { s+=SVG.rect(x0,y0,ww,wh,'part'); rows=0; }\n"
       '    for(var rr=0; rr<rows; rr++){\n'
       '      var off = (rr%2)*bw/2;\n'
       '      for(var cc=-1; cc<102 && cc*bw-off < ww; cc++){\n'
       '        var x=x0+cc*bw-off;\n'
       '        var x1=Math.max(x,x0), x2=Math.min(x+bw-1.2, x0+ww);\n'
       "        if (x2>x1) s+=SVG.rect(x1, y0+rr*bh, x2-x1, Math.max(1,bh-1.2), 'part');\n"
       '      }\n'
       '    }\n'
       "    s+=SVG.text(W/2,30, (dense ? 'Simplified wall · ' : '')+WCfmt(r.perM2,1)+' units/m2  ·  '+r.unitsOrder+' "
       "to order', 13);\n"
       "    s+=SVG.text(W/2,H-16, WCfmt(r.area,2)+' m2  ·  '+WCfmt(r.mortarOrder,3)+' m3 of mortar', 12);\n"
       '    return s+SVG.close();\n'
       '  }\n'
       '};\n'}
