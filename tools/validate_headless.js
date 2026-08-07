#!/usr/bin/env node
/* 择决千秋 — 无头回归验证
 * 目标：在不启动浏览器的情况下，把 index.html 的内联主脚本加载进 Node 的 vm 沙箱，
 * 用 mock 的 DOM/localStorage/fetch 跑通真实游戏引擎，验证 6 大模块（1.1/1.2/2.1/2.2/2.4/5.2/7.2）
 * 的代码改动完整落地、无回归、可通过。
 *
 * 覆盖：
 *  (a) 内联脚本语法可编译（vm.Script 不抛错）
 *  (b) 多皇帝「速通/离线」模式完整通关无异常
 *  (c) flags / relations / _branchQueue 旗标分支串联可达
 *  (d) 中段定时炸弹（midCrisisAnchors）按进度触发
 *  (e) 多结局（evalEnding）可达且默认回退正确
 *  (f) 压强曲线中段隆起
 *  (g) doSave -> doLoad 往返一致（含 usedAnchors 的 Set 重建）
 *  (h) AI 合并调用路径（mock fetch）生成可玩事件且后果结算生效
 *  (i) 源码不再内联任何共享明文凭据（grep BUILTIN_CRED_CIPHER 为 0）
 */
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.resolve(__dirname, "..");
const INDEX = path.join(ROOT, "index.html");
const DATA = path.join(ROOT, "data", "emperors", "coh_data.js");

// ---------- 轻量 DOM / 环境 mock ----------
function makeClassList() {
  const s = new Set();
  return {
    add: (c) => s.add(c),
    remove: (c) => s.delete(c),
    contains: (c) => s.has(c),
    toggle: (c) => (s.has(c) ? (s.delete(c), false) : (s.add(c), true)),
  };
}
function makeCtx() {
  return new Proxy(
    {},
    {
      get(t, p) {
        if (p in t) return t[p];
        return () => {};
      },
      set(t, p, v) {
        t[p] = v;
        return true;
      },
    }
  );
}
function makeEl() {
  const el = {
    _text: "",
    style: {},
    value: "",
    checked: false,
    width: 600,
    height: 200,
    classList: makeClassList(),
    set textContent(v) {
      this._text = v;
    },
    get textContent() {
      return this._text;
    },
    innerHTML: "",
    addEventListener() {},
    removeEventListener() {},
    appendChild() {},
    focus() {},
    click() {},
    getContext() {
      return CTX;
    },
    querySelector() {
      return makeEl();
    },
    querySelectorAll() {
      return [];
    },
    getBoundingClientRect() {
      return { width: 0, height: 0, top: 0, left: 0 };
    },
  };
  return el;
}
const CTX = makeCtx();
const elCache = {};
function getEl(id) {
  if (!elCache[id]) elCache[id] = makeEl();
  return elCache[id];
}

const localStore = new Map();
const localStorage = {
  getItem: (k) => (localStore.has(k) ? localStore.get(k) : null),
  setItem: (k, v) => localStore.set(k, String(v)),
  removeItem: (k) => localStore.delete(k),
};

// mock fetch：返回 OpenAI 风格 {choices:[{message:{content: JSON字符串}}]}
// 始终返回「完整事件 + 顶层后果」合并结构，使生成路径与后果路径（callAI 的 isOutcome 分支）都能被满足。
const fetchState = { n: 0 };
function mockFetch(url, opts) {
  fetchState.n++;
  const labels = ["进取·冒险", "保守·稳重", "革新·远图", "怀柔·安抚", "铁腕·果决"];
  const payload = {
    eventTitle: "AI生成之政事",
    eventDescription: "时值多事之秋，群臣议事，陛下需定夺。",
    choices: [0, 1, 2, 3, 4].map((i) => ({ text: "选项" + (i + 1), hint: labels[i] })),
    outcomes: [0, 1, 2, 3, 4].map((i) => ({
      outcomeDescription: "AI后果" + (i + 1) + "，朝野翕然。",
      historianComment: "史官评曰：事在人为。",
      statChanges: { treasury: 1, people: 1, military: 0, court: 0, health: 0, tech: 0 },
    })),
    outcomeDescription: "AI推演之后果，事遂而定。",
    historianComment: "史官谨书。",
    statChanges: { treasury: 1, people: 1, military: 0, court: 0, health: 0, tech: 0 },
  };
  return Promise.resolve({
    ok: true,
    status: 200,
    json: () => Promise.resolve({ choices: [{ message: { content: JSON.stringify(payload) } }] }),
    text: () => Promise.resolve(""),
  });
}

const sandbox = {};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;
sandbox.console = console;
sandbox.setTimeout = setTimeout;
sandbox.clearTimeout = clearTimeout;
sandbox.AbortController = AbortController;
sandbox.fetch = mockFetch;
sandbox.confirm = () => true;
sandbox.Math = Math;
sandbox.JSON = JSON;
sandbox.Date = Date;
sandbox.document = {
  getElementById: getEl,
  querySelector: () => makeEl(),
  querySelectorAll: () => [],
  addEventListener: () => {},
  get activeElement() {
    return null;
  },
  scrollTo: () => {},
};
sandbox.localStorage = localStorage;
sandbox.window.scrollTo = () => {};
sandbox.innerWidth = 1024;
sandbox.innerHeight = 768;
sandbox.devicePixelRatio = 1;
sandbox.requestAnimationFrame = (cb) => setTimeout(() => { try { cb(Date.now()); } catch (e) {} }, 0);
sandbox.cancelAnimationFrame = (id) => clearTimeout(id);
sandbox.__fetchCount = fetchState;

vm.createContext(sandbox);

// ---------- 1) 载入皇帝数据库（提供 window.COH_BUILTIN_EMPERORS） ----------
const dataSrc = fs.readFileSync(DATA, "utf8");
try {
  vm.runInContext(dataSrc, sandbox, { filename: "coh_data.js" });
} catch (e) {
  console.error("载入 coh_data.js 失败:", e);
  process.exit(2);
}

// ---------- 2) 提取内联主脚本，剥离顶层初始化 IIFE，追加驱动 ----------
const html = fs.readFileSync(INDEX, "utf8");
// 精确锚定内联主脚本：以 <script> + 换行 + "use strict"; 开头，避免误匹配注释里的 <script> 文本
const m = html.match(/<script>\s*"use strict";([\s\S]*?)<\/script>/);
if (!m) {
  console.error("未找到内联主脚本");
  process.exit(2);
}
let body = '"use strict";' + m[1];
const initIdx = body.indexOf("/* ============ 初始化 ============ */");
if (initIdx >= 0) body = body.slice(0, initIdx); // 移除顶层 IIFE（避免异步竞态），改由驱动显式 loadEmperorData

const driver = `
;(async function(){
  const REPORT = { pass:true, errors:[], checks:[], playthroughs:[], branch:null, midCrisis:null, saveLoad:null, endings:null, pressure:null, ai:null };
  function check(name, cond, detail){ REPORT.checks.push({name, ok:!!cond, detail:detail||""}); if(!cond) REPORT.pass=false; }
  try{
    await loadEmperorData();
    check("皇帝数据加载", EMPEROR_REGISTRY.length>50, "count="+EMPEROR_REGISTRY.length);
    const foreignCount = EMPEROR_REGISTRY.filter(e=>e.civilization && e.civilization!=="cn").length;
    check("外国首领数据加载", foreignCount>=150, "foreignCount="+foreignCount);
    for(const cid of ["us","uk","rome","ru"]){
      const rep = EMPEROR_REGISTRY.find(e=>(e.civilization||"cn")===cid);
      check("外国文明已注册:"+cid, !!rep, rep?rep.id:"缺失");
    }

    // (b) 速通/离线完整通关（含外国文明代表）
    const ids=["qin_shihuang","han_wudi","tang_taizong","ming_chengzu","qing_qianlong","han_gaozu","song_huizong","jin_huidi",
               "us_washington","uk_william1","rome_augustus","ru_peter1"];
    for(const id of ids){
      const emp=EMPEROR_REGISTRY.find(e=>e.id===id);
      if(!emp){ REPORT.errors.push("缺少皇帝 "+id); REPORT.pass=false; continue; }
      settings=Object.assign({},settings,{fastMode:true,offlineMode:true,builtin:true});
      pendingEmperor=emp; startGame();
      let months=0; const cap=(emp.reignEnd-emp.reignStart+12)*12; let ended=false;
      while(months<cap){
        if(!currentEvent){ REPORT.errors.push(id+" 无 currentEvent @month "+months); REPORT.pass=false; break; }
        if(!Array.isArray(currentEvent.choices)||currentEvent.choices.length<1){ REPORT.errors.push(id+" 选项异常"); REPORT.pass=false; break; }
        const pick=Math.floor(Math.random()*currentEvent.choices.length);
        makeChoice(pick);
        if(cohEnded){ ended=true; break; }
        if(state.stats.health<=0){ ended=true; break; }
        nextMonth();
        if(cohEnded){ ended=true; break; }
        months++;
      }
      REPORT.playthroughs.push({id,months,ended,health:state.stats.health,flags:Object.keys(state.flags||{}).length,rel:Object.keys(state.relations||{}).length,metrics:state.monthsPlayed?{hem:state.historyEventMonths,am:state.anchorMonths,mp:state.monthsPlayed}:null});
      check("通关无异常:"+id, true, "");
      check("有进度:"+id, months>0||ended, "months="+months);
    }

    // (g) 存档/读档往返（注意：doLoad 末尾会立即 enterMonth，使 monthsPlayed+1；flags/relations 不受影响）
    {
      const emp=EMPEROR_REGISTRY.find(e=>e.id==="qin_shihuang");
      pendingEmperor=emp; settings=Object.assign({},settings,{fastMode:true,offlineMode:true}); startGame();
      for(let k=0;k<6;k++){ if(currentEvent){ makeChoice(Math.floor(Math.random()*currentEvent.choices.length)); if(state.stats.health<=0) break; nextMonth(); } }
      doSave("coh_save_1");
      const saved=JSON.parse(localStorage.getItem("coh_save_1"));
      state.flags={}; state.relations={}; state.usedAnchors=new Set();
      doLoad("coh_save_1");
      check("读档 usedAnchors 重建为 Set", state.usedAnchors instanceof Set, "type="+(typeof state.usedAnchors));
      check("读档 usedAnchors 内容一致", JSON.stringify([...(state.usedAnchors||[])].sort())===JSON.stringify((saved.usedAnchors||[]).slice().sort()), JSON.stringify([...state.usedAnchors]));
      check("读档 flags 一致", JSON.stringify(Object.keys(state.flags).sort())===JSON.stringify(Object.keys(saved.flags||{}).sort()), JSON.stringify(Object.keys(state.flags)));
      check("读档 relations 一致", JSON.stringify(state.relations)===JSON.stringify(saved.relations), "");
      check("读档 year/month 一致", state.year===saved.year && state.month===saved.month, "y="+state.year+"/"+saved.year+" m="+state.month+"/"+saved.month);
      check("读档 monthsPlayed 较存档+1（读档即入下一月，属设计行为）", state.monthsPlayed===saved.monthsPlayed+1, "loaded="+state.monthsPlayed+" saved="+saved.monthsPlayed);
      check("读档 flags/relations 未被 enterMonth 篡改", JSON.stringify(state.relations)===JSON.stringify(saved.relations), "");
      REPORT.saveLoad={saved, after:{flags:Object.keys(state.flags), usedAnchors:[...state.usedAnchors], monthsPlayed:state.monthsPlayed, year:state.year, month:state.month}};
    }

    // (c) 旗标分支串联（含 relations 增量与 nextEventId 队列）
    {
      const craft={ id:"__t_branch", dynasty:"汉", name:"分支帝", templeName:"分支帝", reignStart:1, reignEnd:20, era:"测", evaluation:"x", eraContext:"x", background:"x",
        initStats:{treasury:60,people:60,military:60,court:60,health:80,tech:30}, tier:"A",
        events:[
          { id:"ev_a", year:1, month:null, title:"起始大事件", description:"测", choices:["甲","乙","丙","丁","戊"], historicalChoice:-1, historicalOutcome:"", tier:"major", gating:null,
            branches:[ {setFlags:["flagA"], nextEventId:"ev_b"}, null, null, null, null ],
            relationDeltas:[ {士大夫:-10, 边将:5}, null, null, null, null ] },
          { id:"ev_b", year:2, month:null, title:"后续事件", description:"分支串联", choices:["子","丑","寅","卯","辰"], historicalChoice:-1, historicalOutcome:"", tier:"daily", isFollowup:true }
        ],
        initRelations:{宗室:50,士大夫:40,边将:30,商贾:10}, historicalAnchors:[], midCrisisAnchors:[] };
      EMPEROR_REGISTRY.push(craft); const d=DYNASTIES.find(x=>x.id==="han"); if(d) d.emperors.push(craft);
      pendingEmperor=craft; settings=Object.assign({},settings,{fastMode:true,offlineMode:true}); startGame();
      check("首个事件为门控大事件", currentEvent && currentEvent.title==="起始大事件", currentEvent&&currentEvent.title);
      const relBefore=state.relations["士大夫"];
      makeChoice(0);
      check("分支 setFlags 生效", state.flags["flagA"]===true, JSON.stringify(state.flags));
      check("分支 relationDeltas 生效", state.relations["士大夫"]===relBefore-10, "before="+relBefore+" after="+state.relations["士大夫"]);
      check("分支 _branchQueue 入队", !!state._branchQueue, JSON.stringify(state._branchQueue&&state._branchQueue.id));
      const y0=state.year, mm0=state.month;
      nextMonth();
      check("队列事件被载入（不推进月份）", currentEvent && currentEvent.title==="后续事件", currentEvent&&currentEvent.title);
      check("队列载入未推进月份", state.year===y0 && state.month===mm0, "y="+state.year+" m="+state.month);
      REPORT.branch={flagA:state.flags.flagA, rel:state.relations["士大夫"], queued:currentEvent&&currentEvent.title};
    }

    // (d) 中段定时炸弹
    {
      const craft2={ id:"__t_mid", dynasty:"汉", name:"中段帝", templeName:"中段帝", reignStart:1, reignEnd:30, era:"测", evaluation:"x", eraContext:"x", background:"x",
        initStats:{treasury:60,people:60,military:60,court:60,health:80,tech:30}, tier:"A", events:[],
        initRelations:{宗室:50,士大夫:40,边将:30,商贾:10}, historicalAnchors:[],
        midCrisisAnchors:[ { atProgress:0.1, event:{ id:"mid1", year:null, month:null, title:"中段危机", description:"x", choices:["a","b","c","d","e"], historicalChoice:-1, historicalOutcome:"" } } ] };
      EMPEROR_REGISTRY.push(craft2); const d=DYNASTIES.find(x=>x.id==="han"); if(d) d.emperors.push(craft2);
      pendingEmperor=craft2; settings=Object.assign({},settings,{fastMode:true,offlineMode:true}); startGame();
      let fired=false, guard=0;
      while(guard<60){
        if(currentEvent && currentEvent.title==="中段危机"){ fired=true; break; }
        if(!currentEvent) break;
        makeChoice(0); if(state.stats.health<=0) break; nextMonth(); guard++;
      }
      check("中段定时炸弹触发", fired, "year="+state.year);
      REPORT.midCrisis={fired, year:state.year};
    }

    // (e) 多结局
    {
      const mk=(st,r)=>evalEnding({stats:st, relations:r||{}, flags:{}});
      const e1=mk({treasury:60,military:80,people:50,court:50,health:50,tech:30},{});
      const e2=mk({treasury:60,people:70,court:70,military:50,health:50,tech:30},{});
      const e3=mk({treasury:30,people:20,military:30,court:30,health:50,tech:30},{});
      const e4=mk({treasury:60,people:50,court:40,military:30,health:50,tech:30},{士大夫:-40});
      const e5=mk({treasury:50,people:50,military:50,court:50,health:50,tech:50},{});
      check("结局:一统寰宇", e1&&e1.title==="一统寰宇", JSON.stringify(e1));
      check("结局:治世仁主", e2&&e2.title==="治世仁主", JSON.stringify(e2));
      check("结局:季世之主", e3&&e3.title==="季世之主", JSON.stringify(e3));
      check("结局:清议倾国", e4&&e4.title==="清议倾国", JSON.stringify(e4));
      check("结局:默认回退为 null", e5===null, JSON.stringify(e5));
      REPORT.endings={e1:e1&&e1.title,e2:e2&&e2.title,e3:e3&&e3.title,e4:e4&&e4.title,e5:e5};
    }

    // (f) 压强中段隆起
    {
      const emp=EMPEROR_REGISTRY.find(e=>e.id==="qin_shihuang");
      const pEarly=computePressure({emperor:emp, stats:emp.initStats, year:emp.reignStart});
      const pMid=computePressure({emperor:emp, stats:emp.initStats, year:Math.round((emp.reignStart+emp.reignEnd)/2)});
      check("压强中段>=早期", pMid>=pEarly, "early="+pEarly.toFixed(3)+" mid="+pMid.toFixed(3));
      REPORT.pressure={early:pEarly, mid:pMid};
    }

    // (h) AI 合并调用路径
    {
      // 非内置凭据路径：避免 vm 沙箱中 Web Crypto 异步解密挂起；凭据可用性与 AI 生成路径仍完整验证
      window.COH_CONFIG=null;
      settings=Object.assign({},settings,{fastMode:false,offlineMode:false,builtin:false,api:"http://mock",key:"k",model:"m"});
      _aiProbed=true;
      const emp=EMPEROR_REGISTRY.find(e=>e.id==="qin_shihuang");
      const cr=await resolveCreds();
      REPORT.ai={ avail:aiAvailable(), credKey:(cr&&cr.key)||null, fetchCalls:0 };
      pendingEmperor=emp; startGame();
      // 冲刷微任务（AI 生成走 fetch Promise 链，无需宏任务定时器）
      let _g=0; while(_g<300){ await Promise.resolve(); _g++; }
      REPORT.ai.fetchCalls = (globalThis.__fetchCount && globalThis.__fetchCount.n) || 0;
      check("AI 凭据解析成功", !!(cr&&cr.key), JSON.stringify(cr));
      check("AI 模式可用", aiAvailable()===true, "avail="+aiAvailable());
      check("AI fetch 被调用", REPORT.ai.fetchCalls>0, "calls="+REPORT.ai.fetchCalls);
      check("AI 生成 currentEvent", !!(currentEvent&&currentEvent.choices&&currentEvent.choices.length===5), currentEvent&&currentEvent.title);
      if(currentEvent&&currentEvent.choices.length===5){
        const h0=state.history.length;
        makeChoice(0);
        check("AI 后果结算入 history", state.history.length>h0, "history="+state.history.length);
      }
      REPORT.ai.title=currentEvent&&currentEvent.title;
      REPORT.ai.choices=currentEvent&&currentEvent.choices.length;
    }
  }catch(err){
    REPORT.pass=false; REPORT.errors.push("EXCEPTION: "+(err&&err.stack||err));
  }
  globalThis.__TEST_RESULT=REPORT;
})();
`;

(async () => {
let script;
try {
  script = new vm.Script(body + "\n" + driver, { filename: "inline+driver.js" });
} catch (e) {
  console.error("内联脚本编译失败（语法错误）:", e);
  process.exit(2);
}
try {
  script.runInContext(sandbox, { filename: "inline+driver.js" });
} catch (e) {
  console.error("运行期异常:", e);
  process.exit(2);
}

// 等待驱动（含 AI 的 60ms 等待）完成
const result = await new Promise((res) => {
  const t0 = Date.now();
  const tick = () => {
    if (sandbox.__TEST_RESULT) return res(sandbox.__TEST_RESULT);
    if (Date.now() - t0 > 5000) return res({ pass: false, errors: ["超时未产出结果"], checks: [] });
    setTimeout(tick, 20);
  };
  tick();
});

// ---------- 输出报告 ----------
console.log("\n========== 择决千秋 无头回归验证 ==========");
// (i) 7.2 静态校验：内联脚本不得再内联任何共享明文凭据（在 vm 外对 body 做 grep）
const noInlineCred = !/BUILTIN_CRED_CIPHER|BUILTIN_ENC_DISPLAY/.test(body);
if (!noInlineCred) {
  console.log("  [FAIL] 源码仍内联共享明文凭据 (BUILTIN_CRED_CIPHER / BUILTIN_ENC_DISPLAY)");
}
let fail = 0;
for (const c of result.checks) {
  console.log((c.ok ? "  [PASS] " : "  [FAIL] ") + c.name + (c.detail ? "  (" + c.detail + ")" : ""));
  if (!c.ok) fail++;
}
if (result.errors.length) {
  console.log("\n-- 错误 --");
  for (const e of result.errors) console.log("  " + e);
}
console.log("\n-- 明细 --");
console.log("  通关:", JSON.stringify(result.playthroughs, null, 0));
console.log("  分支:", JSON.stringify(result.branch));
console.log("  中段危机:", JSON.stringify(result.midCrisis));
console.log("  存档往返:", JSON.stringify(result.saveLoad));
console.log("  结局:", JSON.stringify(result.endings));
console.log("  压强:", JSON.stringify(result.pressure));
console.log("  AI:", JSON.stringify(result.ai));
console.log("\n  通过检查: " + (result.checks.length - fail) + "/" + result.checks.length);
console.log("  总判定: " + (result.pass && fail === 0 && noInlineCred ? "PASS" : "FAIL"));
console.log("==========================================\n");

process.exit(result.pass && fail === 0 && noInlineCred ? 0 : 1);
})();
