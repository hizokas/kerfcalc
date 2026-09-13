const vm=require('node:vm'),cp=require('node:child_process'),a=require('node:assert/strict'),fs=require('node:fs');
const js=cp.execFileSync('python3',['-c',"import runpy;print(runpy.run_path('factory/specs/roofarea.py')['SPEC']['js'])"],{encoding:'utf8'}).trim();
const html=fs.readFileSync('public/roof-area-calculator.html','utf8');a.ok(html.includes(js));
let points,texts;const c=vm.createContext({WCfmt:(n,d)=>n.toFixed(d),SVG:{open:()=>'<svg>',close:()=>'</svg>',poly:p=>{points=p;return '';},line:()=>'',text:(x,y,t)=>{texts.push(t);return '';}}});vm.runInContext(js,c);
const defaults=Object.fromEntries(c.SPEC.fields.map(f=>[f.id,f.value]));const calc=x=>c.SPEC.compute({...defaults,...x});const near=(x,y)=>a.ok(Math.abs(x-y)<1e-8,`${x} != ${y}`);
let r=calc({});a.equal(r.ok,true);near(r.area,12.8*8.8*Math.sqrt(1.25));near(r.withWaste,r.area*1.1);a.equal(r.bundles,45);near(r.ridge,12.8);near(r.eaves,25.6);near(r.rakes,17.6*Math.sqrt(1.25));near(r.squares,r.withWaste/9.290304);
r=calc({shape:'hip'});near(r.ridge,4);near(r.hips,26.4);near(r.eaves,43.2);near(r.rakes,0);
r=calc({shape:'hip',a:8000,b:8000});near(r.ridge,0);near(r.hips,26.4);
const inches={unit:'in'};for(const f of c.SPEC.fields)if(f.unit==='length')inches[f.id]=f.value/25.4;near(calc(inches).area,calc({}).area);a.equal(calc(inches).bundles,45);
for(const pitch of [1,6,12,24,120]) {r=calc({pitch});texts=[];c.SPEC.diagram(r,{...defaults,pitch});near((points[0][1]-points[1][1])/(points[1][0]-points[0][0]),pitch/12);a.ok(points[1][1]>50);}
r=calc({shape:'hip',a:6000,b:12000});texts=[];c.SPEC.diagram(r,{...defaults,shape:'hip',a:6000,b:12000});a.ok(texts.includes('span 6.80 m'));
for(const bad of [{a:-1},{a:0},{b:NaN},{pitch:Infinity},{pitch:0},{overhang:-1},{waste:101},{waste:NaN},{perBundle:0},{perBundle:Infinity},{shape:'unknown'},{a:1e308,b:1e308}])a.equal(calc(bad).ok,false,JSON.stringify(bad));
for(const f of c.SPEC.fields)a.ok(html.includes(`id="${f.id}"`));
console.log('PASS roof: gable/hip/square geometry, material quantities, imperial equivalence, slope-accurate drawing and finite validation');
