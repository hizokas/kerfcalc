SPEC = {'slug': 'compound-miter-calculator',
 'h1': 'Compound Miter Angle Calculator',
 'title_tag': 'Compound Miter Calculator — Crown Molding Miter and Bevel Angles',
 'description': 'Calculate saw miter and bevel magnitudes for crown molding laid flat, using spring angle and measured '
                'wall angle. Includes non-square corner examples.',
 'card_desc': 'Saw miter and bevel settings for crown and sloped work, with the formulas shown.',
 'category': 'Joinery',
 'intro': 'Find the miter and bevel settings for crown molding cut flat on the saw table. Measure the spring angle '
          'from the wall and enter the smaller angle between the wall lines. The results are angle magnitudes; cutting '
          'directions depend on the piece and saw setup.',
 'notes': [('Measure the spring angle from the wall',
            'Spring angle here is the angle between the installed crown and the vertical wall. A 38° spring profile is '
            'therefore 52° from the ceiling. These settings are for crown laid flat, not nested at its installed angle '
            'against the fence.'),
           ('Which corner angle should I enter?',
            'Enter the smaller included angle between the wall lines, greater than 0° and less than 180°. For a normal '
            'square inside or outside corner, enter 90°. If you measured a reflex angle such as 267°, enter 360 − 267 '
            '= 93°. Inside/outside changes the orientation of the cuts, not their magnitudes under this convention.'),
           ('The corrected formulas',
            'With spring angle S and included corner angle C: miter = atan(sin(S) / tan(C/2)); bevel = asin(cos(S) × '
            'cos(C/2)). Evaluate trigonometric functions in degrees. As the corner approaches a straight 180°, both '
            'settings approach zero. Multiplying by tan(C/2) instead of dividing only agrees at a 90° corner.'),
           ('Worked examples for 38° spring crown',
            'At a 90° corner, use miter 31.62° and bevel 33.86°. At 93°, they become 30.30° and 32.85°. At 120°, they '
            'are 19.57° and 23.20°. These magnitudes agree with the <a '
            'href="https://sbebuilders.com/cgi-bin/geometry/crown_table.cgi">SBE Builders crown molding tables</a>. '
            'Keep the actual measured spring angle; rounding it to a whole degree changes the result.'),
           ('Setup and test cuts',
            'The results do not specify left/right saw directions or which offcut to keep. Those depend on '
            'inside/outside, the end being cut, profile orientation and saw capabilities. Follow the setup chart for '
            'your saw and make a mirrored test pair in scrap. The <a '
            'href="https://www.boschtools.com/us/en/ocsmedia/2610051827_GCM12SD_0918.pdf">Bosch GCM12SD manual</a> '
            'includes separate crown setup directions for each corner and end.'),
           ('Scope',
            'This model assumes two pieces of the same crown profile and spring angle meeting at a wall corner below a '
            'level ceiling. Unequal spring angles, sloping ceilings and arbitrary compound assemblies require a '
            'different geometric model. A numerical result does not confirm that your saw can reach or accurately '
            'reproduce the settings.')],
 'js': '\n'
       'var SPEC = {\n'
       '  fields: [\n'
       "    {id:'spring', label:'Spring angle (degrees)', value:38, group:'Moulding', min:1, max:89, hint:'Angle "
       "between crown and vertical wall'},\n"
       "    {id:'corner', label:'Corner angle (degrees)', value:90, group:'Corner', min:1, max:179, hint:'Smaller wall "
       "angle; square inside/outside = 90'},\n"
       "    {id:'type', label:'Corner type', type:'select', value:'inside', group:'Corner', options:[\n"
       "      {value:'inside', label:'Inside corner'},\n"
       "      {value:'outside', label:'Outside corner'}]}\n"
       '  ],\n'
       '  compute: function (i) {\n'
       '    var errs=[];\n'
       "    if(!(i.spring>0 && i.spring<90)) errs.push('Spring angle must be between 0 and 90 degrees.');\n"
       "    if(!(i.corner>0 && i.corner<180)) errs.push('Corner angle must be between 0 and 180 degrees.');\n"
       "    if(['inside','outside'].indexOf(i.type)===-1) errs.push('Select inside or outside corner.');\n"
       '    if(errs.length) return {ok:false, errors:errs};\n'
       '\n'
       '    var d2r=Math.PI/180, r2d=180/Math.PI;\n'
       '    var S=i.spring*d2r, C=i.corner*d2r;\n'
       '    var miter=Math.atan(Math.sin(S)/Math.tan(C/2))*r2d;\n'
       '    var bevel=Math.asin(Math.cos(S)*Math.cos(C/2))*r2d;\n'
       '    var saw=90-miter;\n'
       '\n'
       '    var warn=[];\n'
       "    if (Math.abs(i.corner-90)>5) warn.push('That corner is '+WCfmt(Math.abs(i.corner-90),1)+' degrees off "
       "square — worth re-measuring before you cut anything expensive.');\n"
       "    if (miter>50||bevel>50) warn.push('These settings are beyond the range of some mitre saws. Check the saw "
       "reaches them before cutting.');\n"
       '\n'
       '    return {ok:true, miter:miter, bevel:bevel, saw:saw, warnings:warn,\n'
       '      stats:[\n'
       "        {value:WCfmt(miter,2)+String.fromCharCode(176), label:'Miter angle'},\n"
       "        {value:WCfmt(bevel,2)+String.fromCharCode(176), label:'Bevel angle'},\n"
       "        {value:WCfmt(i.spring,2)+String.fromCharCode(176), label:'Spring angle'},\n"
       "        {value:WCfmt(i.corner,1)+String.fromCharCode(176), label:'Corner'}\n"
       '      ],\n'
       "      tables:[{title:'Saw settings', head:['Setting','Value','Where it comes from'], rows:[\n"
       "        ['Miter', WCfmt(miter,2)+String.fromCharCode(176), 'atan(sin('+WCfmt(i.spring,2)+') / "
       "tan('+WCfmt(i.corner/2,2)+'))'],\n"
       "        ['Bevel', WCfmt(bevel,2)+String.fromCharCode(176), 'asin(cos('+WCfmt(i.spring,2)+') x "
       "cos('+WCfmt(i.corner/2,2)+'))'],\n"
       "        ['Miter, if your saw reads from 90', WCfmt(saw,2)+String.fromCharCode(176), '90 minus the miter'],\n"
       "        ['Corner type', i.type==='inside'?'Inside':'Outside', 'Magnitudes only; use the saw setup chart for "
       "cutting direction'],\n"
       "        ['Pieces per corner', '2', 'Same profile and spring angle; mirrored test pair']\n"
       '      ]}],\n'
       "      note:'Cut a test pair in scrap and offer them up before touching the real moulding. Check the measured "
       "angles, saw setup and fit of both test pieces.'\n"
       '    };\n'
       '  },\n'
       '  diagram: function (r,i){\n'
       '    var W=560,H=240,s=SVG.open(W,H),cx=W/2,cy=150,L=150;\n'
       '    var half=i.corner/2*Math.PI/180;\n'
       '    var x1=cx-Math.sin(half)*L, y1=cy-Math.cos(half)*L;\n'
       '    var x2=cx+Math.sin(half)*L, y2=cy-Math.cos(half)*L;\n'
       "    s+=SVG.poly([[x1,y1],[cx,cy],[x2,y2]],'ghost');\n"
       '    s+=SVG.line(cx,cy,x1,y1,\' stroke-width="2.5"\');\n'
       '    s+=SVG.line(cx,cy,x2,y2,\' stroke-width="2.5"\');\n'
       '    s+=\'<path d="M \'+(cx-30*Math.sin(half))+\' \'+(cy-30*Math.cos(half))+\' A 30 30 0 0 1 '
       '\'+(cx+30*Math.sin(half))+\' \'+(cy-30*Math.cos(half))+\'" fill="none" stroke="currentColor" '
       'stroke-width="1"/>\';\n'
       '    s+=SVG.text(cx,cy-42,WCfmt(i.corner,1)+String.fromCharCode(176),13);\n'
       "    s+=SVG.text(cx,26,'Set the saw to these two numbers',12);\n"
       "    s+=SVG.text(cx,H-38,'Miter '+WCfmt(r.miter,2)+String.fromCharCode(176)+'    Bevel "
       "'+WCfmt(r.bevel,2)+String.fromCharCode(176),15);\n"
       "    s+=SVG.text(cx,H-16,'Spring angle '+WCfmt(i.spring,2)+String.fromCharCode(176)+' - "
       "'+(i.type==='inside'?'inside':'outside')+' corner',11);\n"
       '    return s+SVG.close();\n'
       '  }\n'
       '};\n'}
