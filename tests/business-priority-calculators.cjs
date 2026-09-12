const fs=require('node:fs'),vm=require('node:vm'),cp=require('node:child_process'),assert=require('node:assert/strict');
const context=vm.createContext({WCfmt:(n,d)=>n.toFixed(d)});
vm.runInContext(cp.execFileSync('python3',['-c',"import runpy;print(runpy.run_path('factory/specs/rebar.py')['SPEC']['js'])"],{encoding:'utf8'}),context);
const defaults={unit:'mm',len:6000,wid:4000,spacing:200,cover:50,dia:12,stock:6000,lapDia:40};
const calc=x=>context.SPEC.compute({...defaults,...x}),close=(a,b)=>assert.ok(Math.abs(a-b)<1e-7,`${a} != ${b}`);
let r=calc({});assert.equal(r.ok,true);assert.equal(r.nL,21);assert.equal(r.nW,31);close(r.totalM,244.8);assert.equal(r.stockCount,52);close(r.spW,195);assert.ok(r.spL<=200);
r=calc({len:12000});assert.equal(r.piecesL,3);close(r.tables[0].rows[0][4],12860);assert.equal(r.stockCount,63+61);
// At precisely 2 stocks minus 1 lap, two pieces suffice.
assert.equal(calc({len:11620}).piecesL,2);
for(const x of [{spacing:0},{stock:0},{lapDia:-1},{len:Infinity},{cover:0},{len:12000,lapDia:500}])assert.equal(calc(x).ok,false);
const imperial={unit:'in'};for(const k of ['len','wid','spacing','cover','dia','stock'])imperial[k]=defaults[k]/25.4;
r=calc(imperial);close(r.totalM,244.8);close(r.weight,calc({}).weight);assert.equal(r.nL,21);assert.equal(r.nW,31);
const stair=fs.readFileSync('public/stair-stringer-calculator.html','utf8');vm.runInContext(stair.slice(stair.indexOf('var MM_PER_IN'),stair.indexOf('/* ===== PURE CALC END')),context);
const s=context.computeStairStringer({unit:'mm',totalRise:2800,targetRiser:175,going:250,nosing:25,treadThickness:32,floorFinish:18,throat:89,fitRun:false});
assert.equal(s.ok,true);assert.equal(s.riserCount,16);assert.equal(s.treadCount,15);close(s.riserHeight,175);close(s.totalRunUsed,3750);close(s.firstRiserCut,161);
const joint=fs.readFileSync('public/box-joint-layout.html','utf8');vm.runInContext(joint.slice(joint.indexOf('function computeJointLayout'),joint.indexOf('/* === PURE CALCULATION — end')),context);
const j=context.computeJointLayout({unit:'mm',jointType:'box',boardWidth:150,tailBoardThickness:18,pinBoardThickness:18,tailWidth:10,pinWidth:4,angleRatio:8,halfPinEnds:true,mirrorMating:false});
assert.equal(j.ok,true);assert.equal(j.segmentCount,15);close(j.tailWidth,10);assert.equal(j.check.ok,true);
console.log('PASS: rebar defaults, splice boundaries, invalid inputs, inch equivalence; stair and joint worked examples.');
