const vm=require('node:vm'),cp=require('node:child_process'),a=require('node:assert/strict'),fs=require('node:fs');
const js=cp.execFileSync('python3',['-c',"import runpy;print(runpy.run_path('factory/specs/miter.py')['SPEC']['js'])"],{encoding:'utf8'}).trim();
const html=fs.readFileSync('public/compound-miter-calculator.html','utf8');a.ok(html.includes(js));
const c=vm.createContext({WCfmt:(n,d)=>n.toFixed(d)});vm.runInContext(js,c);const calc=x=>c.SPEC.compute({spring:38,corner:90,type:'inside',...x});
const near=(x,y,t=.005)=>a.ok(Math.abs(x-y)<t,`${x} != ${y}`);
// Independent published SBE Builders flat-crown reference values, 38-degree spring.
for(const [corner,miter,bevel] of [[45,56.06756,46.72125],[60,46.83931,43.03440],[90,31.62,33.86],[93,30.29522,32.84927],[120,19.57,23.20],[135,14.31,17.55]]) {
 const r=calc({corner});a.equal(r.ok,true);near(r.miter,miter);near(r.bevel,bevel);near(calc({corner,type:'outside'}).miter,r.miter,1e-10);
}
near(calc({spring:45}).miter,35.26438968);near(calc({spring:45}).bevel,30);
a.ok(calc({corner:179.99}).miter<.01);a.ok(calc({corner:179.99}).bevel<.01);
a.ok(calc({spring:38.4}).tables[0].rows[0][2].includes('38.40'));a.ok(calc({corner:120}).tables[0].rows[0][2].includes('/ tan(60.00)'));
for(const bad of [{spring:0},{spring:90},{spring:NaN},{spring:Infinity},{corner:0},{corner:180},{corner:267},{corner:NaN},{type:'bogus'}])a.equal(calc(bad).ok,false,JSON.stringify(bad));
console.log('PASS compound miter: published acute/right/obtuse reference angles, outside magnitudes, near-straight limit, displayed formula and invalid inputs');
