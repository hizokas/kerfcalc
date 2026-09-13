SPEC = {'slug': 'flooring-plank-calculator',
 'h1': 'Flooring Plank Layout Calculator',
 'title_tag': 'Flooring Calculator — Plank Rows, Last Row Width, Stagger and Waste',
 'description': 'Calculate flooring rows, balanced edge widths, starter and end pieces, joint stagger and a '
                'conservative box estimate. Supports millimetres and inches.',
 'card_desc': 'Rows, last-row width, joint stagger and boxes to buy for any plank flooring.',
 'category': 'Finishing',
 'intro': 'Plan edge-row widths before cutting flooring. Enter the gap, minimum stagger and minimum piece sizes from '
          'your product instructions, then compare the layout and a conservative box estimate.',
 'notes': [('Balance narrow edge rows',
            'Divide the laying width by the plank width. If the final row is narrower than your chosen minimum, share '
            'one full plank width plus that final strip between the first and last rows. The diagram shows the '
            'adjusted widths. An exact multiple of the plank width ends with a full row, not a zero-width strip.'),
           ('Worked example: balancing a 10 mm strip',
            'A 5,000 × 4,020 mm room with 10 mm gaps leaves 4,980 × 4,000 mm. With 1,200 × 190 mm planks, 21 full '
            'widths leave a 10 mm strip. For a 50 mm minimum edge width, use 22 rows: the first and last are 100 mm '
            'wide, with 20 full rows between them. A 300 mm minimum stagger gives a four-row sequence of 1,200, 300, '
            '600 and 900 mm starters.'),
           ('End pieces can invalidate an otherwise correct stagger',
            'In the example, the first row ends with 180 mm. If your product requires a 300 mm minimum end piece, the '
            'calculator flags this: revise the starting pattern before cutting. A valid distance between joints alone '
            'does not make a complete installation plan. Regular repeating patterns may also be unsuitable for your '
            'chosen product.'),
           ('How the ordering estimate works',
            'Each drawn piece is counted as one new plank; offcuts are not reused between rows or across ripped rows. '
            'The example has 110 pieces, or 121 planks with 10% extra: 16 boxes of eight, containing 128 planks. This '
            'deliberately conservative estimate can exceed an area-based allowance. An actual cutting plan may reduce '
            'it; damaged boards, product restrictions and room details may increase it.'),
           ('Use the instructions for your exact flooring',
            'Gap, stagger and minimum widths vary with the flooring system. <a '
            'href="https://int.quick-step.com/en/laminate/installation">Quick-Step’s laminate installation guide</a>, '
            'for example, recommends at least 30 cm between adjacent end joints and a last row at least 5 cm wide. '
            'Confirm the current instructions for your specific product, including substrate, moisture, expansion and '
            'pattern requirements. The input defaults are examples.'),
           ('Scope and units',
            'This tool models straight planks of one size in a rectangular room. It does not plan doorways, islands, '
            'diagonal laying, locking-edge reuse or saw kerf. All length inputs follow the mm/inch selector; output '
            'floor areas remain in m². Very dense layouts use a simplified outline to keep the page responsive.')],
 'js': 'var SPEC = {\n'
       '  fields: [\n'
       "    {id:'roomL', label:'Room length', value:5000, unit:'length', group:'Room', min:0, hint:'Along the "
       "direction of the planks'},\n"
       "    {id:'roomW', label:'Room width', value:4000, unit:'length', group:'Room', min:0},\n"
       "    {id:'gap', label:'Expansion gap on each side', value:10, unit:'length', group:'Room', min:0},\n"
       "    {id:'plankL', label:'Plank length', value:1200, unit:'length', group:'Plank', min:0},\n"
       "    {id:'plankW', label:'Plank width', value:190, unit:'length', group:'Plank', min:0},\n"
       "    {id:'stagger', label:'Minimum end-joint stagger', value:300, unit:'length', group:'Plank', min:0},\n"
       "    {id:'minEdge', label:'Minimum edge-row width', value:50, unit:'length', group:'Plank', min:0},\n"
       "    {id:'minEnd', label:'Minimum end-piece length', value:300, unit:'length', group:'Plank', min:0, hint:'Use "
       "the requirements for your flooring product'},\n"
       "    {id:'perBox', label:'Planks per box', value:8, group:'Ordering', min:1, step:1},\n"
       "    {id:'waste', label:'Extra allowance (%)', value:10, group:'Ordering', min:0}\n"
       '  ],\n'
       '  compute: function(i) {\n'
       "    var positive=['roomL','roomW','plankL','plankW','stagger'];\n"
       "    var nonnegative=['gap','minEdge','minEnd','waste'];\n"
       "    if (positive.some(function(f){return !Number.isFinite(i[f]) || i[f]<=0;})) return {ok:false,errors:['Enter "
       "finite, positive room, plank and stagger dimensions.']};\n"
       '    if (nonnegative.some(function(f){return !Number.isFinite(i[f]) || i[f]<0;})) return '
       "{ok:false,errors:['Gap, minimum pieces and allowance must be finite and non-negative.']};\n"
       "    if (!Number.isSafeInteger(i.perBox) || i.perBox<1 || i.waste>100) return {ok:false,errors:['Enter a "
       "positive whole number of planks per box and an allowance from 0 to 100%.']};\n"
       '    var L=i.roomL-2*i.gap, Wd=i.roomW-2*i.gap;\n'
       "    if (!(L>0 && Wd>0)) return {ok:false,errors:['The expansion gaps leave no laying area.']};\n"
       "    if (i.stagger>i.plankL/2) return {ok:false,errors:['This regular stagger pattern supports a minimum up to "
       "half the plank length. Review the product requirements and plank length.']};\n"
       "    if (i.minEdge>i.plankW || i.minEnd>i.plankL) return {ok:false,errors:['Minimum piece dimensions cannot "
       "exceed a full plank.']};\n"
       '    var ceil=function(v){return Math.ceil(v-1e-10);};\n'
       '    var rows=ceil(Wd/i.plankW);\n'
       "    if (!Number.isSafeInteger(rows) || rows<1 || rows>2000 || L/i.plankL>10000) return {ok:false,errors:['This "
       "planner supports up to 2,000 rows and 10,000 plank lengths per row. Check the dimensions.']};\n"
       '    var originalLast=Wd-(rows-1)*i.plankW;\n'
       '    var firstRow=rows===1 ? Wd : i.plankW, lastRow=originalLast, ripFirst=null;\n'
       '    if (rows>1 && originalLast<i.minEdge) { firstRow=lastRow=(i.plankW+originalLast)/2; ripFirst=firstRow; }\n'
       '    var nPattern=Math.max(2,Math.min(12,Math.floor(i.plankL/i.stagger+1e-10)));\n'
       '    var step=i.plankL/nPattern, rowData=[], totalPlanks=0, minPiece=Infinity;\n'
       '    for (var row=0;row<rows;row++) {\n'
       '      var start=Math.min(L,row%nPattern===0 ? i.plankL : (row%nPattern)*step);\n'
       '      var count=1+Math.max(0,ceil((L-start)/i.plankL));\n'
       '      var end=count===1 ? start : L-start-(count-2)*i.plankL;\n'
       '      var width=row===0 ? firstRow : (row===rows-1 ? lastRow : i.plankW);\n'
       '      rowData.push({start:start,end:end,count:count,width:width});\n'
       '      totalPlanks+=count; minPiece=Math.min(minPiece,start,end);\n'
       '    }\n'
       '    var withWaste=ceil(totalPlanks*(1+i.waste/100)), boxes=ceil(withWaste/i.perBox);\n'
       "    var toM=i.unit==='in' ? .0254 : .001, area=i.roomL*toM*i.roomW*toM, layingArea=L*toM*Wd*toM;\n"
       '    if (![area,layingArea,step].every(Number.isFinite) || !Number.isSafeInteger(withWaste) || '
       "!Number.isSafeInteger(boxes*i.perBox)) return {ok:false,errors:['The result is outside the supported range. "
       "Check the dimensions.']};\n"
       "    var u=i.unit==='in' ? ' in' : ' mm', fmt=function(v){return WCfmt(v,2)+u;}, warnings=[];\n"
       "    if (ripFirst) warnings.push('The unbalanced final row is '+fmt(originalLast)+'. Cut both edge rows to "
       "'+fmt(firstRow)+'.');\n"
       "    if (Math.min(firstRow,lastRow)<i.minEdge) warnings.push('The edge row remains below your minimum width. "
       "Change the layout or plank width.');\n"
       "    if (minPiece+1e-9<i.minEnd) warnings.push('This pattern produces an end piece of '+fmt(minPiece)+', below "
       "your '+fmt(i.minEnd)+' minimum. Adjust the starting pattern before installation; this is not a ready-to-cut "
       "plan.');\n"
       '    return '
       '{ok:true,rows:rows,L:L,Wd:Wd,firstRow:firstRow,lastRow:lastRow,originalLast:originalLast,ripFirst:ripFirst,\n'
       '      '
       'rowData:rowData,nPattern:nPattern,actualStagger:step,totalPlanks:totalPlanks,withWaste:withWaste,boxes:boxes,area:area,layingArea:layingArea,\n'
       '      warnings:warnings,\n'
       "      stats:[{value:String(rows),label:'Rows'},{value:String(withWaste),label:'Planks incl. "
       "extra'},{value:String(boxes),label:'Boxes'},{value:WCfmt(area,2),label:'m² gross floor'}],\n"
       "      tables:[{title:'Layout and ordering',head:['Item','Value'],rows:[\n"
       "        ['Laying dimensions after gaps',fmt(L)+' × '+fmt(Wd)],\n"
       "        ['Laying area after gaps',WCfmt(layingArea,3)+' m²'],\n"
       "        ['First row width',fmt(firstRow)],['Last row width',fmt(lastRow)],\n"
       "        ['Full-width rows',String(rowData.filter(function(r){return "
       'Math.abs(r.width-i.plankW)<i.plankW*1e-9;}).length)],\n'
       "        ['Regular pattern repeat',String(nPattern)+' rows'],['Joint spacing in regular pattern',fmt(step)],\n"
       "        ['Plank pieces before extra',String(totalPlanks)],['Offcut reuse assumed','None — one new plank per "
       "piece'],\n"
       "        ['With '+WCfmt(i.waste,1)+'% extra',String(withWaste)],['Boxes of '+i.perBox,String(boxes)+' "
       "('+(boxes*i.perBox)+' planks)']\n"
       "      ]},{title:'First rows of the repeating pattern — check end pieces',head:['Row','Width','Starter "
       "length','Last piece','Pieces'],rows:rowData.slice(0,nPattern).map(function(r,k){return "
       '[String(k+1),fmt(r.width),fmt(r.start),fmt(r.end),String(r.count)];})}],\n'
       "      note:'Conservative rectangular-room estimate: each piece uses a fresh plank, with no offcut reuse. "
       'Starter lengths are remaining pieces, not amounts to cut off. The regular pattern meets the requested joint '
       'spacing, but check all warnings and your manufacturer’s pattern, end-piece, gap and edge-width requirements. '
       "The drawing is schematic.'\n"
       '    };\n'
       '  },\n'
       '  diagram:function(r,i) {\n'
       '    var W=640,H=360,m=28,s=SVG.open(W,H),sc=Math.min((W-2*m)/i.roomL,(H-2*m-24)/i.roomW);\n'
       '    var x0=m,y0=m+16,rw=i.roomL*sc,rh=i.roomW*sc,g=i.gap*sc;\n'
       "    s+=SVG.rect(x0,y0,rw,rh,'ghost');\n"
       '    var dense=r.rows>80 || r.totalPlanks>2000;\n'
       "    if (dense) s+=SVG.rect(x0+g,y0+g,r.L*sc,r.Wd*sc,'part');\n"
       '    else {\n'
       '      var yy=y0+g;\n'
       '      for(var row=0;row<r.rows;row++) {\n'
       '        var data=r.rowData[row],xx=x0+g,hh=data.width*sc;\n'
       '        for(var col=0;col<data.count;col++) {\n'
       '          var length=col===0 ? data.start : (col===data.count-1 ? data.end : i.plankL);\n'
       "          s+=SVG.rect(xx,yy,length*sc,hh,'part');xx+=length*sc;\n"
       '        }\n'
       '        yy+=hh;\n'
       '      }\n'
       '    }\n'
       "    s+=SVG.text(W/2,20,(dense?'Simplified layout · ':'')+r.rows+' rows · '+r.boxes+' boxes',13);\n"
       "    s+=SVG.text(W/2,H-8,'Edge rows: '+WCfmt(r.firstRow,2)+' / '+WCfmt(r.lastRow,2)+(i.unit==='in'?' in':' "
       "mm'),12);\n"
       '    return s+SVG.close();\n'
       '  }\n'
       '};\n'}
