const vm=require('node:vm'),cp=require('node:child_process'),a=require('node:assert/strict'),fs=require('node:fs');
const js=cp.execFileSync('python3',['-c',"import runpy;print(runpy.run_path('factory/specs/brick.py')['SPEC']['js'])"],{encoding:'utf8'}).trim();
const html=fs.readFileSync('public/brick-block-calculator.html','utf8');a.ok(html.includes(js));
let rectCount=0;const c=vm.createContext({WCfmt:(n,d)=>n.toFixed(d),SVG:{open:()=>'<svg>',close:()=>'</svg>',rect:()=>{rectCount++;return '<rect/>';},text:()=>''}});vm.runInContext(js,c);
const defaults=Object.fromEntries(c.SPEC.fields.map(f=>[f.id,f.value]));const calc=x=>c.SPEC.compute({...defaults,...x});const near=(x,y)=>a.ok(Math.abs(x-y)<1e-9,`${x} != ${y}`);
let r=calc({bagYield:12});a.equal(r.ok,true);near(r.perM2,1/(.225*.075));near(r.units,711.1111111111111);a.equal(r.unitsOrder,747);near(r.mortar,.2113777777777779);a.equal(r.bags,21);
const single=r;r=calc({skins:2});near(r.mortarOrder,single.mortarOrder*2);a.equal(r.bags,null);
r=calc({skins:2,collar:10});near(r.mortarOrder,(single.mortar*2+.12)*1.15);
r=calc({openings:2});near(r.area,10);near(r.units,single.units*10/12);
const inches={unit:'in',bagYield:12};for(const f of c.SPEC.fields)if(f.unit==='length')inches[f.id]=f.value/25.4;
near(calc(inches).mortarOrder,single.mortarOrder);a.equal(calc(inches).unitsOrder,747);
a.equal(calc({joint:0}).mortarOrder,0);a.equal(calc({collar:NaN}).ok,true);
for(const bad of [{wallL:Infinity},{wallH:NaN},{unitL:0},{joint:-1},{openings:12},{openings:-1},{skins:1.2},{skins:Infinity},{skins:21},{skins:2,collar:NaN},{waste:101},{mortarWaste:Infinity},{bagYield:-1},{bagYield:NaN}])a.equal(calc(bad).ok,false,JSON.stringify(bad));
for(const input of [{},{unitL:.00001,unitH:.00001},{wallL:1e9}]){rectCount=0;r=calc(input);a.equal(r.ok,true);c.SPEC.diagram(r,{...defaults,...input});a.ok(rectCount<=4080,'schematic stays bounded');}
for(const f of c.SPEC.fields)a.ok(html.includes(`id="${f.id}"`));
console.log('PASS brick/block: quantities, openings, premix yield, separate skins/collar, imperial equivalence, invalid inputs and bounded schematic');
