// 逻辑沙盒：镜像新函数，验证「可追溯叙事」端到端正确（仅用于本次验证，跑完即删）
const fs = require("fs");
const tree = JSON.parse(fs.readFileSync("data/tech_tree.json", "utf8"));
const nodes = tree.nodes || [];
const ATTR_CN = { treasury: "国库", people: "民心", military: "军事", court: "朝政", health: "健康", tech: "科技" };
function tnName(n) { return n.name; }
const TECH_DOMAINS = [
  { re: /北伐|亲征|讨|伐|征|战|出兵|进攻|攘|拓土|平[定寇]|剿|大举|示威|边患|寇|叛|戎|师|烽|御|守边|拓疆|鏖战|克复/, branch: "mil", attr: "military", war: true },
  { re: /税|赋|商|市|盐铁|矿|铸币|钱|货|贸|府库|国库|度支|漕|关市|市易|岁入/, branch: "com", attr: "treasury" },
  { re: /民|饥|荒|赈|蠲|免役|农|桑|垦|灾|流民|疾苦|和籴/, branch: "agri", attr: "people" },
  { re: /官|吏|党争|谏|劾|弊政|朝政|礼制|科[举学]|士人|清议|台谏/, branch: "civ", attr: "court" },
  { re: /疫|疾|病|医|药|瘟|疠|瘴|疾疫|时疫|疴/, branch: "med", attr: "health" }
];
function eventDomain(ev) {
  const text = (ev.title || "") + " " + (ev.description || "") + " " + ((ev.choices || []).map(c => c.text || "").join(" "));
  for (const d of TECH_DOMAINS) { if (d.re.test(text)) return d; }
  return null;
}
const state = { ownedTechs: {}, playerTechs: {} };
const com = nodes.filter(n => n.branch === "com");
let lvl = 0;
for (const n of com) { if (lvl >= 14) break; const L = Math.min(n.maxLevel || 3, 1 + (lvl % 3)); state.ownedTechs[n.id] = L; lvl += L; }
state.playerTechs["com_05_02"] = 3; state.ownedTechs["com_05_02"] = 3;
state.playerTechs["com_08_01"] = 2; state.ownedTechs["com_08_01"] = 2;
function branchTechLevels(br) { let s = 0; for (const id in state.ownedTechs) { const n = nodes.find(x => x.id === id); if (n && n.branch === br) s += (state.ownedTechs[id] || 0); } return s; }
function collectBranchTechs(branchId) {
  const owned = state.ownedTechs || {}; const out = []; let branchName = "";
  for (const n of nodes) { if (n.branch !== branchId) continue; if (!branchName && n.branchName) branchName = n.branchName; const lv = owned[n.id] || 0; if (lv > 0) out.push({ id: n.id, name: tnName(n), level: lv }); }
  out.sort((a, b) => b.level - a.level); return { techs: out, branchName };
}
function techEventAttrBonus(ev) {
  const d = eventDomain(ev); if (!d) return {}; const lvl = branchTechLevels(d.branch); if (lvl <= 0) return {};
  const cap = d.war ? 10 : 6; const k = d.war ? 0.5 : 0.35; const bonus = Math.min(cap, Math.round(lvl * k)); if (bonus <= 0) return {};
  const { techs, branchName } = collectBranchTechs(d.branch);
  return { [d.attr]: { value: bonus, branch: d.branch, branchName, totalLevel: lvl, cap, k, contributors: techs } };
}
function techBonusNarrative(teb) {
  let s = ""; for (const k in teb) { const b = teb[k]; const top = (b.contributors || []).slice(0, 4).map(c => c.name + " Lv." + c.level).join("、"); const more = (b.contributors || []).length > 4 ? (" 等 " + b.contributors.length + " 项") : ""; const src = top ? ("，主力：" + top + more) : ""; s += "科技增益：" + ATTR_CN[k] + " +" + b.value + "（「" + (b.branchName || b.branch) + "」领域 · 共 " + b.totalLevel + " 级" + src + "）。"; } return s;
}
const ev = { title: "盐铁专营", description: "府库空虚，请开矿铸币以充实国库岁入", choices: [{ text: "准奏" }] };
const teb = techEventAttrBonus(ev);
console.log("matched domain:", eventDomain(ev).branch, "| com 分支总等级:", branchTechLevels("com"));
console.log("NARRATIVE =>", techBonusNarrative(teb));
console.log("contributor count:", (teb.treasury ? teb.treasury.contributors.length : 0));
const narr = techBonusNarrative(teb);
const ok = narr.includes("科技增益：国库 +") && narr.includes("「财货」领域") && narr.includes("共") && narr.includes("级") && narr.includes("主力：");
console.log(ok ? "PASS: 可追溯（领域+总级+主力科技）" : "FAIL: 仍不可追溯");

// 战争事件路径
const wev = { title: "北伐匈奴", description: "大举出兵征讨，拓土守边", choices: [{ text: "命将出征" }] };
const wteb = techEventAttrBonus(wev);
console.log("WAR NARRATIVE =>", techBonusNarrative(wteb));
// 无匹配事件
const nev = { title: "闲棋", description: "庭院闲坐", choices: [{ text: "罢了" }] };
console.log("NO-MATCH NARRATIVE =>", JSON.stringify(techBonusNarrative(techEventAttrBonus(nev))));
