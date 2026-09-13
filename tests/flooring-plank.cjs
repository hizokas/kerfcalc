const vm=require('node:vm'),cp=require('node:child_process'),a=require('node:assert/strict'),fs=require('node:fs');
const js=cp.execFileSync('python3',['-c',"import runpy;print(runpy.run_path('factory/specs/flooring.py')['SPEC']['js'])"],{encoding:'utf8'}).trim();
const html=fs.readFileSync('public/flooring-plank-calculator.html','utf8');a.ok(html.includes(js));
let rects=[];const c=vm.createContext({WCfmt:(n,d)=>n.toFixed(d),SVG:{open:()=>'<svg>',close:()=>'</svg>',rect:(x,y,w,h,type)=>{rects.push({x,y,w,h,type});return '<rect/>';},text:()=>''}});vm.runInContext(js,c);
const defaults=Object.fromEntries(c.SPEC.fields.map(f=>[f.id,f.value]));const calc=x=>c.SPEC.compute({...defaults,...x});const near=(x,y)=>a.ok(Math.abs(x-y)<1e-7,`${x} != ${y}`);
let input={roomW:4020},r=calc(input);a.equal(r.ok,true);a.equal(r.rows,22);near(r.originalLast,10);near(r.firstRow,100);near(r.lastRow,100);near(r.actualStagger,300);a.equal(r.totalPlanks,110);a.equal(r.withWaste,121);a.equal(r.boxes,16);a.equal(r.rowData[0].end,180);a.ok(r.warnings.some(w=>w.includes('below your')));
rects=[];c.SPEC.diagram(r,{...defaults,...input});const scale=rects[0].w/defaults.roomL;near(rects[1].h/scale,100);near(rects[6].h/scale,190);near(rects.at(-1).h/scale,100);
r=calc({roomW:3820});a.equal(r.rows,20);near(r.lastRow,190);a.equal(r.ripFirst,null);
r=calc({roomW:120});a.equal(r.rows,1);near(r.firstRow,100);near(r.lastRow,100);
r=calc({stagger:450});near(r.actualStagger,600);a.equal(r.nPattern,2); // previous round(1200/450)=3 incorrectly gave400
r=calc({roomL:2520});a.equal(r.rowData[0].count,3);a.equal(r.rowData[1].count,3);r=calc({roomL:2420});a.equal(r.rowData[0].count,2);a.equal(r.rowData[1].count,3); // shifted row needs an additional fresh plank
const inches={unit:'in',roomW:4020/25.4};for(const f of c.SPEC.fields)if(f.unit==='length' && f.id!=='roomW')inches[f.id]=f.value/25.4;
r=calc(inches);a.equal(r.rows,22);near(r.firstRow*25.4,100);a.equal(r.totalPlanks,110);a.equal(r.boxes,16);near(r.area,20.1);
for(const bad of [{roomL:Infinity},{roomW:NaN},{gap:-1},{gap:3000},{plankL:0},{stagger:601},{stagger:0},{minEdge:200},{minEnd:1201},{minEnd:NaN},{perBox:1.5},{perBox:0},{waste:101},{roomW:1e12}])a.equal(calc(bad).ok,false,JSON.stringify(bad));
for(const width of [50,100,190,191,380,381,3980,4000])for(const length of [50,300,1200,2400,4980]) {
 const i={roomW:width+20,roomL:length+20},r=calc(i);a.equal(r.ok,true);near(r.rowData.reduce((s,x)=>s+x.width,0),width);
 for(const row of r.rowData){a.ok(row.start>0 && row.end>0 && row.width>0);near(row.count===1?row.start:row.start+row.end+(row.count-2)*1200,length);}
}
r=calc({roomW:190020});a.equal(r.ok,true);rects=[];c.SPEC.diagram(r,{...defaults,roomW:190020});a.equal(rects.length,2);
for(const stagger of [100,300,450,600]) {
 const r=calc({stagger});
 const joints=row=>Array.from({length:row.count-1},(_,k)=>row.start+k*1200);
 for(let k=1;k<r.rowData.length;k++)for(const x of joints(r.rowData[k-1]))for(const y of joints(r.rowData[k]))a.ok(Math.abs(x-y)+1e-7>=stagger,'actual adjacent joints meet minimum, including pattern wrap');
}
for(const f of c.SPEC.fields)a.ok(html.includes(`id="${f.id}"`));
console.log('PASS flooring: balanced/full/single rows, actual diagram widths, stagger minimum, cut-piece counts, end warnings, imperial equivalence, row coverage and bounded rendering');
