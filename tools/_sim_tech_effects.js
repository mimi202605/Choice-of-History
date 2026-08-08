// 科技具体作用·数值压测：复刻 index.html 的 computeTechEffects 聚合逻辑，
// 在「全树满级」「典型中局」两种场景下检查各通道是否被封顶约束住（通胀体检）。
const fs = require("fs"), path = require("path");
const ROOT = path.join(__dirname, "..");
const tree = JSON.parse(fs.readFileSync(path.join(ROOT, "data/tech_tree.json"), "utf8"));
const nodes = tree.nodes || [];
const byId = {}; nodes.forEach(n => byId[n.id] = n);

// 与 index.html 引擎常量保持一致（改引擎须同步改此处，否则压测结论失真）
const PASSIVE_YEAR_CAP = 3;   // 单维被动每年封顶
const REL_TOTAL_CAP    = 25;  // 派系好感科技加成总封顶
const SCORE_TOTAL_CAP  = 8;   // 终评单维加成总封顶
const COSTLESS_CAP     = 30;  // 研究费减免封顶（researchTech 内 techCostFor 施加）
const WAREDGE_CAP      = 60;  // 单通道战争优势封顶
const WAR_BREADTH_CAP  = 0.15;// warWinChance 内 军备广度(militaryTechLevel，含预设)封顶
const WAR_ELITE_CAP    = 0.20;// warWinChance 内 军工尖端(warEdge，纯自研)封顶
const tierOfAge = a => a <= 3 ? 1 : (a <= 7 ? 2 : 3);

function compute(owned) {
  const E = { passive: {}, shields: {}, eventLess: {}, warEdge: { winBonus: 0, lossMitigate: 0 }, relations: {}, costLess: {}, score: {}, unlocks: [] };
  for (const id in owned) {
    const lvl = owned[id]; if (!lvl) continue;
    const node = byId[id]; if (!node || !node.effect) continue;
    const tier = tierOfAge(node.age || 1);
    for (const sp of node.effect) {
      const mag = sp.perTier * tier * lvl;
      switch (sp.type) {
        case "passive": E.passive[sp.target] = (E.passive[sp.target] || 0) + Math.min(sp.cap, mag); break;
        case "shield": case "autoResolve": E.shields[sp.target] = Math.min(sp.cap, (E.shields[sp.target] || 0) + mag); break;
        case "eventLess": E.eventLess[sp.target] = Math.min(sp.cap, (E.eventLess[sp.target] || 0) + mag); break;
        case "warEdge": { const wt = sp.target === "winBonus" ? "winBonus" : "lossMitigate"; E.warEdge[wt] = Math.min(WAREDGE_CAP, (E.warEdge[wt] || 0) + mag); break; }
        case "relation": E.relations[sp.target] = (E.relations[sp.target] || 0) + Math.min(sp.cap, mag); break;
        case "costLess": E.costLess[sp.target] = Math.min(sp.cap, (E.costLess[sp.target] || 0) + mag); break;
        case "score": E.score[sp.target] = (E.score[sp.target] || 0) + Math.min(sp.cap, mag); break;
        case "unlock": if (E.unlocks.indexOf(sp.target) < 0) E.unlocks.push(sp.target); break;
      }
    }
  }
  // 全局通道封顶（与 index.html computeTechEffects 末尾一致）
  for (const k in E.passive)   if (E.passive[k]   > PASSIVE_YEAR_CAP) E.passive[k]   = PASSIVE_YEAR_CAP;
  for (const k in E.relations) if (E.relations[k] > REL_TOTAL_CAP)    E.relations[k] = REL_TOTAL_CAP;
  for (const k in E.score)     if (E.score[k]     > SCORE_TOTAL_CAP)  E.score[k]     = SCORE_TOTAL_CAP;
  for (const k in E.costLess)  if (E.costLess[k]  > COSTLESS_CAP)     E.costLess[k]  = COSTLESS_CAP;
  return E;
}

// 复刻 index.html warWinChance()：军备广度(含预设)与军工尖端(纯自研)两条独立封顶，互不吞噬
function winChance(E, mil, weaponLvl) {
  const breadth = Math.min(WAR_BREADTH_CAP, (weaponLvl || 0) * 0.01);
  const elite   = Math.min(WAR_ELITE_CAP, (E.warEdge.winBonus || 0) / 100);
  return Math.max(0.1, Math.min(0.9, 0.5 + (mil - 50) / 200 + breadth + elite));
}

function report(tag, E) {
  const fx = o => Object.keys(o).filter(k => o[k]).map(k => k + ":" + (+o[k]).toFixed(1)).join(" ") || "-";
  console.log("\n=== " + tag + " ===");
  console.log("  passive   ", fx(E.passive));
  console.log("  shields   ", fx(E.shields));
  console.log("  eventLess ", fx(E.eventLess));
  console.log("  warEdge   ", "win:" + E.warEdge.winBonus.toFixed(1) + " lossMit:" + E.warEdge.lossMitigate.toFixed(1));
  console.log("  relations ", fx(E.relations));
  console.log("  costLess  ", fx(E.costLess));
  console.log("  score     ", fx(E.score));
  console.log("  unlocks   ", E.unlocks.join("、") || "-");
  // 胜算体检：军事 30/50/70 三档，军工等级取 warEdge 对应量级的粗估
  const wl = Math.round((E.warEdge.winBonus || 0) / 2);
  console.log("  胜算(军事30/50/70, 军工lv≈" + wl + ")",
    [30, 50, 70].map(m => Math.round(winChance(E, m, wl) * 100) + "%").join(" / "));
}

// 场景 A：全树满级（理论上限，现实不可达，仅测封顶）
const full = {}; nodes.forEach(n => full[n.id] = n.maxLevel);
report("A 全树满级（" + nodes.length + " 节点）", compute(full));

// 场景 B：典型中局 —— 时代≤6 的节点随机取 40 项，各 2 级
const pool = nodes.filter(n => n.age <= 6);
const mid = {};
for (let i = 0; i < 40 && i < pool.length; i++) mid[pool[(i * 37) % pool.length].id] = 2;
report("B 典型中局（40 项 × 2 级，时代≤6）", compute(mid));

// 场景 C：军事单开 —— 军工相关 special 全满
const warSp = new Set(["weapon", "gunpowder", "armor", "cavalry", "navy", "formation"]);
const war = {}; nodes.filter(n => warSp.has(n.special)).forEach(n => war[n.id] = n.maxLevel);
report("C 军工单开全满（" + Object.keys(war).length + " 节点）", compute(war));

// 场景 D：开局预设基线 —— 仅供参考。
// 【口径提示】index.html 的 computeTechEffects 现读 state.playerTechs（玩家自研增量），
// 预设科技【不计入实效】，故下列数字仅代表「若误按 ownedTechs 聚合」的失控情形，
// 保留作回归哨兵：一旦有人把口径改回 ownedTechs，这组数字会立刻暴露开局即封顶。
const presets = JSON.parse(fs.readFileSync(path.join(ROOT, "data/tech_presets.json"), "utf8")).dynasties || {};
for (const dyn of ["夏", "汉", "清"]) {
  const p = presets[dyn]; if (!p || !p.techs) continue;
  report("D[哨兵·不应发生] 若把预设计入实效·" + dyn + "（era" + p.eraLevel + "，" + p.techCount + " 项）", compute(p.techs));
}

// 场景 E：真实游玩基线 —— 玩家自研 N 级（当前口径下这才是实际生效的量）。
// 科技点是六维之一(0~100)、研究即扣，时代5 每级 7 点 → 一朝现实自研约 10~30 级。
const pool5 = nodes.filter(n => n.age <= 5);
for (const N of [10, 20, 30]) {
  const own = {}; for (let i = 0; i < N; i++) own[pool5[(i * 67) % pool5.length].id] = 1;
  report("E 玩家自研 " + N + " 级（时代≤5 散点·均摊流）", compute(own));
}
const warPool = nodes.filter(n => warSp.has(n.special) && n.age <= 5);
const spec = {}; for (let i = 0; i < 20 && i < warPool.length; i++) spec[warPool[i].id] = 1;
report("E 玩家自研 20 级（军工专精流）", compute(spec));
