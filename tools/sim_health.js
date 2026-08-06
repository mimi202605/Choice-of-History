// 健康轨迹模拟器：用真实引擎在离线/速通模式下跑通，逐月记录健康变化并区分
// 「事件结算」与「被动衰减（nextMonth 里的年迈/平均/溢出）」两类来源。
// 目的：定位健康度异常快速下降 bug，并量化整体难度。
const fs = require("fs");
const vm = require("vm");
const path = require("path");

const ROOT = "D:/工作/2026/开发的软件/Choice-of-History";
const INDEX = path.join(ROOT, "index.html");
const DATA = path.join(ROOT, "data/emperors/coh_data.js");

function stubEl() {
  return {
    value: "", textContent: "", innerHTML: "", checked: false,
    classList: { add(){}, remove(){}, contains(){ return false; } },
    style: {},
    addEventListener(){}, click(){}, focus(){},
  };
}

function runSim(emperorId, strategy) {
  const html = fs.readFileSync(INDEX, "utf8");
  const m = html.match(/"use strict";([\s\S]*?)\n<\/script>/);
  let body = m[1];
  const data = fs.readFileSync(DATA, "utf8");

  const localStorage = {
    store: {},
    getItem(k){ return this.store[k] ?? null; },
    setItem(k, v){ this.store[k] = v; },
    removeItem(k){ delete this.store[k]; },
  };
  const sandbox = {
    console, setTimeout: (fn)=>{ fn(); return 0; }, clearTimeout(){},
    setInterval(){}, clearInterval(){}, Math, JSON, Date, Array, Object, Set, Map, Promise,
    AbortController: function(){ this.abort=()=>{}; this.signal={}; },
    fetch: async ()=>({ ok:false, status:0, json: async()=>({}), text: async()=>"" }),
    localStorage,
    document: { getElementById: ()=>stubEl(), querySelectorAll: ()=>[], querySelector: ()=>null, addEventListener(){} },
    window: {},
  };
  sandbox.window = sandbox;
  sandbox.globalThis = sandbox;
  sandbox.window.scrollTo = ()=>{};
  sandbox.window.COH_CONFIG = { apiBase:"", model:"", builtinCred:"" };

  const driver = `
  (function(){
    loadSettings();
    settings.builtin=false; settings.fastMode=true; settings.offlineMode=true;
    const emp = EMPEROR_REGISTRY.find(e=>e.id===${JSON.stringify(emperorId)});
    if(!emp){ globalThis.__ERR="no emperor "+${JSON.stringify(emperorId)}; globalThis.__DONE=true; return; }
    pendingEmperor=emp; startGame();

    function bestChoice(){
      const opts=currentEvent.choices||[];
      let best=-1, bestScore=Infinity;
      const savedState=state, savedEvent=currentEvent;
      for(let i=0;i<opts.length;i++){
        const cState=JSON.parse(JSON.stringify(state));
        cState.usedAnchors=new Set([...(state.usedAnchors||[])]);
        state=cState; currentEvent=savedEvent;
        try{ fallbackOutcome(opts[i]); }catch(e){}
        const hLoss=Math.max(0, savedState.stats.health - state.stats.health);
        let totalLoss=0;
        for(const k of ["treasury","people","military","court","health","tech"]){
          totalLoss+=Math.max(0, savedState.stats[k]-state.stats[k]);
        }
        const score=hLoss*3 + totalLoss;
        if(score<bestScore){ bestScore=score; best=i; }
        state=savedState; currentEvent=savedEvent;
      }
      return best;
    }

    const timeline=[];
    let guard=0;
    while(guard++ < 2000 && state.stats.health>0 && state.year <= emp.reignEnd+12){
      const h0=state.stats.health;
      let i = (${JSON.stringify(strategy)}==="smart") ? bestChoice() : Math.floor(Math.random()*currentEvent.choices.length);
      if(i<0) i=0;
      makeChoice(i);
      const h1=state.stats.health;
      const eventDelta=h1-h0;
      if(state.stats.health<=0){ timeline.push({year:state.year,month:state.month,eventDelta,passiveDelta:0,health:0,dead:"event"}); break; }
      const h1b=state.stats.health;
      nextMonth();
      const h2=state.stats.health;
      timeline.push({year:state.year,month:state.month,eventDelta,passiveDelta:h2-h1b,health:h2});
      if(state.year>emp.reignEnd+12) break;
    }
    globalThis.__TIMELINE=timeline;
    globalThis.__REIGN={start:emp.reignStart, end:emp.reignEnd};
    globalThis.__DONE=true;
  })();
  `;

  try {
    const ctx = vm.createContext(sandbox);
    new vm.Script(data + "\n" + body + "\n" + driver, { filename: "sim.js" }).runInContext(ctx);
  } catch (e) {
    return { error: e.message, stack: (e.stack||"").split("\n").slice(0,3).join(" | ") };
  }
  if (sandbox.__ERR) return { error: sandbox.__ERR };
  return { timeline: sandbox.__TIMELINE, reign: sandbox.__REIGN };
}

const emperors = ["qin_shihuang","han_wudi","tang_taizong","tang_xuanzong","song_taizu",
  "ming_chengzu","ming_sizong","qing_kangxi","qing_qianlong","sui_wendi"];

// ---- 随机/普通玩家：测正常在位期内的真实难度 ----
console.log("=== 随机玩家难度测试（每位 8 局，速通模式）===");
console.log("格式：皇帝 | 正常在位期驾崩率 | 平均终局健康 | 平均在位年数");
for (const id of emperors) {
  let deadNormal=0, sumEndHealth=0, sumReignYears=0, runs=8;
  for (let s=0; s<runs; s++) {
    const r = runSim(id, "random");
    if (r.error) { runs--; continue; }
    const tl = r.timeline;
    const last = tl[tl.length-1];
    const end = r.reign.end;
    sumEndHealth += (last?last.health:0);
    sumReignYears += (last?last.year - r.reign.start:0);
    // 是否死在正常在位期（year<=reignEnd）
    const diedNormal = last && last.dead && last.year <= end;
    if (diedNormal) deadNormal++;
  }
  if (runs===0) { console.log(id, "无数据"); continue; }
  console.log(`[${id}] 正常期驾崩率=${Math.round(100*deadNormal/runs)}% | 平均终局健康=${Math.round(sumEndHealth/runs)} | 平均在位=${Math.round(sumReignYears/runs)}年`);
}

// ---- 理性玩家健康轨迹（诊断） ----
console.log("\n=== 理性玩家健康轨迹诊断 ===");
console.log("格式：皇帝 | 健康@即位后N年 | 正常在位期最低 | 终局");
let diedCount=0;
for (const id of emperors) {
  const r = runSim(id, "smart");
  if (r.error) { console.log(id, "ERR", r.error); continue; }
  const tl = r.timeline;
  const last = tl[tl.length-1];
  const died = last && last.dead;
  if (died) diedCount++;
  const { start, end } = r.reign;
  const span = end - start;
  const byYear = {};
  let minNormal = 100;
  for (const t of tl) {
    byYear[t.year] = t.health;
    if (t.year <= end) minNormal = Math.min(minNormal, t.health);
  }
  const step = span > 40 ? 10 : 5;
  const marks = [];
  for (let y = start; y <= end; y += step) {
    if (byYear[y] != null) marks.push(`+${(y-start)}y:${byYear[y]}`);
  }
  if (byYear[end+1] != null) marks.push(`超期:${byYear[end+1]}`);
  console.log(`[${id}] ${marks.join(" ")} | 正常期最低=${minNormal} | 终局=${last?last.health:'?'} ${died?'★驾崩@'+last.year:'活到'+last.year}`);
}
