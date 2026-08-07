// tools/montecarlo.js
// 最小 Monte Carlo 模拟器 —— 用于回填 index.html 三处 [PLACEHOLDER · Monte Carlo 验证路径]：
//   1) OUTCOME_LIMIT ±10/±20 是否使单事件约占总量 10% 且可被对冲（月均净 delta≈中性 + 合理方差）
//   2) 中段加压危机率是否 ≤8%（每月为"数值危机"的占比）
//   3) 随机时局致崩盘占比是否 < 总崩盘 15%（崩盘触发维的最后一次负向来源是否为 random）
//
// 设计：从 index.html 正则抽取平衡常量（单一真相，避免 magic number 漂移）；从 data/random_pools.js
// 加载真实随机池。模拟"中性玩家"：每月事件后果在 ±limit 内均匀抽取并施加 +2 安全网（复刻 applyOutcome/fallbackOutcome），
// 随机冲击按 P_RAND 从真实池抽样并施加韧性缩放 + 耦合。复刻 nextMonth 的健康回血/衰减、失败链、被动健康衰减。
// 注意：AI 事件真实分布未知，本模拟只验证"机制层"在中性玩家下的稳态；AI 偏置是独立未知量，需在实机 playtest 另测。
//
// 运行：node tools/montecarlo.js

const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');

// ---------- 常量抽取（与 index.html 单一真相同步） ----------
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
function constVal(name, fallback) {
  const m = html.match(new RegExp('const\\s+' + name + '\\s*=\\s*(-?\\d+(?:\\.\\d+)?)\\s*;'));
  if (!m) { console.warn(`[warn] 未从 index.html 抽到常量 ${name}，用回退值 ${fallback}`); return fallback; }
  return parseFloat(m[1]);
}
const LIMIT_NORMAL   = constVal('OUTCOME_LIMIT_NORMAL', 10);
const LIMIT_CRISIS   = constVal('OUTCOME_LIMIT_CRISIS', 20);
const FAIL_WARN      = constVal('FAIL_WARN', 15);
const FAIL_LOW       = constVal('FAIL_LOW', 10);
const FAIL_LOW_MONTHS= constVal('FAIL_LOW_MONTHS', 3);
const FAIL_CRIT_MONTHS=constVal('FAIL_CRIT_MONTHS', 2);
const FAIL_PENALTY   = constVal('FAIL_PENALTY', 3);
const P_RAND         = constVal('P_RAND', 0.18);
const MID_THRESHOLD  = constVal('MID_PRESSURE_THRESHOLD', 0.4);
const MID_CRISIS_PROB= constVal('MID_CRISIS_PROB', 0.35);
// 健康回血/衰减阈值（nextMonth 内联 magic number，与源码保持一致）
const HEAL_AVG_HI = 55, HEAL_AVG_LO = 30, HEALTH_DECAY_CAP = -2;
const RAND_COOLDOWN = 1;

const DIMS = ['treasury', 'people', 'military', 'court', 'health', 'tech'];
const FAIL_DIMS = ['treasury', 'people', 'military', 'court'];
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const randInt = (lo, hi) => lo + Math.floor(Math.random() * (hi - lo + 1));

// ---------- 随机池加载 ----------
const rp = fs.readFileSync(path.join(ROOT, 'data/random_pools.js'), 'utf8');
const mm = rp.match(/COH_RANDOM_POOLS\s*=\s*(\{[\s\S]*\})\s*;/);
if (!mm) { console.error('无法解析 data/random_pools.js'); process.exit(1); }
const POOLS = JSON.parse(mm[1]);

function eraTagOf(y) {
  if (y < -221) return 'shangzhou';
  if (y < 220) return 'qinhan';
  if (y < 618) return 'weijin';
  if (y < 960) return 'tang';
  if (y < 1271) return 'song';
  if (y < 1368) return 'yuan';
  if (y < 1644) return 'ming';
  return 'qing';
}
const ERAS = ['shangzhou', 'qinhan', 'weijin', 'tang', 'song', 'yuan', 'ming', 'qing'];

function samplePool(arr) {
  let total = 0;
  for (const e of arr) total += (e.weight || 1);
  let r = Math.random() * total;
  for (const e of arr) { r -= (e.weight || 1); if (r <= 0) return e; }
  return arr[arr.length - 1];
}

function scaleByResilience(chg, res, stats) {
  const out = {};
  for (const k in chg) {
    let v = chg[k];
    if (v < 0) {
      const refDim = (res && res[k]) || k;
      const prep = clamp(stats[refDim] / 100, 0, 1);
      const factor = 1.3 - 0.6 * prep;
      v = Math.round(v * factor);
    }
    out[k] = v;
  }
  return out;
}

function applyCoupling(stats) {
  if (stats.military > 75) stats.treasury = clamp(stats.treasury - 1, 0, 100);
  if (stats.court < 25)    stats.people   = clamp(stats.people - 1, 0, 100);
  if (stats.treasury < 20) stats.military = clamp(stats.military - 1, 0, 100);
}

function applyRandom(stats, ev, lastSource) {
  const scaled = scaleByResilience(ev.baseChanges || {}, ev.resilience || {}, stats);
  const limit = ev.major ? LIMIT_CRISIS : LIMIT_NORMAL;
  for (const k of DIMS) {
    let v = clamp(scaled[k] || 0, -limit, limit);
    if (v !== 0) { stats[k] = clamp(stats[k] + v, 0, 100); lastSource[k] = 'random'; }
  }
  applyCoupling(stats);
}

function applyEvent(stats, limit, lastSource) {
  const sc = {};
  for (const k of DIMS) sc[k] = Math.round((Math.random() * 2 - 1) * limit);
  // +2 安全网：六维全 ≤0 时给最低非健康维 +2（复刻 applyOutcome / fallbackOutcome）
  if (DIMS.every(k => (sc[k] || 0) <= 0)) {
    const needy = DIMS.filter(k => k !== 'health' && stats[k] < 50);
    const target = needy.length ? needy.reduce((a, b) => stats[a] < stats[b] ? a : b) : 'people';
    sc[target] = (sc[target] || 0) + 2;
  }
  for (const k of DIMS) {
    if ((sc[k] || 0) !== 0) { stats[k] = clamp(stats[k] + sc[k], 0, 100); lastSource[k] = 'event'; }
  }
  applyCoupling(stats);
}

function stepFailure(state) {
  for (const k of FAIL_DIMS) {
    const v = state.stats[k];
    const c = state._fail[k] || (state._fail[k] = { danger: 0 });
    if (v <= FAIL_LOW) {
      c.danger++;
      if (c.danger === FAIL_LOW_MONTHS) {
        state.stats[k] = clamp(state.stats[k] - FAIL_PENALTY, 0, 100);
        FAIL_DIMS.forEach(o => { if (o !== k) state.stats[o] = clamp(state.stats[o] - 1, 0, 100); });
      }
      if (c.danger >= FAIL_LOW_MONTHS + FAIL_CRIT_MONTHS) return k;
    } else {
      c.danger = 0;
    }
  }
  return null;
}

function verdictOf(gov) {
  if (gov >= 68) return '明君';
  if (gov >= 52) return '庸君';
  if (gov >= 36) return '昏君';
  return '亡国之主';
}

function simulate() {
  const era = ERAS[randInt(0, ERAS.length - 1)];
  // 反推一个属于该 era 的即位年份
  const span_by_era = {
    shangzhou: [-1100, -600], qinhan: [-220, 200], weijin: [220, 600], tang: [620, 950],
    song: [960, 1260], yuan: [1271, 1360], ming: [1368, 1640], qing: [1644, 1900],
  };
  const [lo, hi] = span_by_era[era];
  const reignStart = randInt(lo, hi);
  const ascendAge = randInt(20, 55);
  const reignSpan = randInt(8, 40);
  const reignEnd = reignStart + reignSpan;

  const stats = {
    treasury: randInt(40, 70), people: randInt(40, 70), military: randInt(40, 70),
    court: randInt(45, 75), health: randInt(60, 85), tech: randInt(20, 50),
  };
  const state = { stats, _fail: {}, year: reignStart, month: 1, _monthSinceRandom: 99, lastSource: {}, lowStreak: 0 };

  let months = 0, crisisMonths = 0, playerMonths = 0, randomMonths = 0, courtMax = 0;
  const netDelta = { treasury: 0, people: 0, military: 0, court: 0, health: 0, tech: 0 };
  let endReason = 'timeout', endDim = null, randomCaused = false;
  const MAX_MONTHS = 960;

  while (months < MAX_MONTHS) {
    const before = { ...stats };
    // —— 健康回血/衰减（复刻 nextMonth 开头）——
    const avg4 = (stats.treasury + stats.people + stats.military + stats.court) / 4;
    if (avg4 >= HEAL_AVG_HI) stats.health = clamp(stats.health + 1, 0, 100);
    else if (avg4 < HEAL_AVG_LO) stats.health = clamp(stats.health - 1, 0, 100);
    if (avg4 < HEAL_AVG_LO) state.lowStreak++; else state.lowStreak = 0;
    if (state.lowStreak >= 6) {
      const lowest = Object.entries(stats).filter(([k]) => k !== 'health' && k !== 'tech').sort((a, b) => a[1] - b[1])[0];
      if (lowest) stats[lowest[0]] = clamp(stats[lowest[0]] - 2, 0, 100);
    }
    // —— 被动健康衰减（年龄/超期）——
    let passive = 0;
    const yearsInReign = state.year - reignStart;
    if (ascendAge != null) {
      const ageYears = ascendAge + yearsInReign;
      if (ageYears > 70) passive -= 1;
      if (ageYears > 80) passive -= 1;
    } else {
      const prog = yearsInReign / reignSpan;
      if (prog > 0.66) passive -= 1;
      if (prog > 0.85) passive -= 1;
    }
    if (state.year > reignEnd) { const over = state.year - reignEnd; passive -= Math.min(2, Math.floor(over / 3)); }
    if (passive < HEALTH_DECAY_CAP) passive = HEALTH_DECAY_CAP;
    if (passive !== 0) stats.health = clamp(stats.health + passive, 0, 100);

    // —— 失败链 ——
    const collapseDim = stepFailure(state);
    if (collapseDim) { endReason = 'collapse'; endDim = collapseDim; randomCaused = (state.lastSource[collapseDim] === 'random'); }
    else if (stats.health <= 0) { endReason = 'death'; }
    else {
      // —— 本月事件 ——
      if (state._monthSinceRandom >= RAND_COOLDOWN && Math.random() < P_RAND) {
        applyRandom(stats, samplePool(POOLS[era]), state.lastSource);
        randomMonths++;
        state._monthSinceRandom = 0;
      } else {
        const span = Math.max(1, reignEnd - reignStart);
        const prog = (state.year - reignStart) / span;
        const bell = Math.exp(-Math.pow((prog - 0.5) / 0.18, 2));
        const healthFactor = 1 - stats.health / 100;
        const pressure = clamp(0.35 * bell + 0.4 * healthFactor, 0, 1);
        let limit = LIMIT_NORMAL;
        if (pressure > MID_THRESHOLD && Math.random() < MID_CRISIS_PROB * pressure) { limit = LIMIT_CRISIS; crisisMonths++; }
        applyEvent(stats, limit, state.lastSource);
        playerMonths++;
      }
      state._monthSinceRandom++;
      state.month++;
      if (state.month > 12) { state.month = 1; state.year++; }
    }

    // 本月末：累计净 delta
    for (const k of DIMS) netDelta[k] += stats[k] - before[k];
    courtMax = Math.max(courtMax, stats.court);
    months++;

    if (endReason !== 'timeout') break;
  }

  const gov = (stats.treasury + stats.people + stats.military + stats.court + stats.health) / 5;
  return { months, crisisMonths, playerMonths, randomMonths, courtMax, endReason, endDim, randomCaused, netDelta, finalStats: { ...stats }, gov, verdict: verdictOf(gov) };
}

// ---------- 跑批 ----------
const N = 3000;
const agg = {
  months: 0, crisisMonths: 0, playerMonths: 0, randomMonths: 0,
  courtMaxSum: 0, courtPinned: 0,
  endReasons: {}, verdicts: {}, endDims: {},
  collapseTotal: 0, randomCausedCollapse: 0,
  netDeltaSum: { treasury: 0, people: 0, military: 0, court: 0, health: 0, tech: 0 },
  netDeltaSqSum: { treasury: 0, people: 0, military: 0, court: 0, health: 0, tech: 0 },
  govSum: 0,
};
let monthCount = 0;
for (let i = 0; i < N; i++) {
  const r = simulate();
  agg.months += r.months;
  agg.crisisMonths += r.crisisMonths;
  agg.playerMonths += r.playerMonths;
  agg.randomMonths += r.randomMonths;
  agg.courtMaxSum += r.courtMax;
  if (r.courtMax >= 95) agg.courtPinned++;
  agg.endReasons[r.endReason] = (agg.endReasons[r.endReason] || 0) + 1;
  agg.verdicts[r.verdict] = (agg.verdicts[r.verdict] || 0) + 1;
  if (r.endReason === 'collapse') {
    agg.collapseTotal++;
    agg.endDims[r.endDim] = (agg.endDims[r.endDim] || 0) + 1;
    if (r.randomCaused) agg.randomCausedCollapse++;
  }
  for (const k of DIMS) {
    agg.netDeltaSum[k] += r.netDelta[k];
    agg.netDeltaSqSum[k] += r.netDelta[k] * r.netDelta[k];
  }
  agg.govSum += r.gov;
  monthCount += r.months;
}

// ---------- 输出 ----------
const pct = x => (100 * x / N).toFixed(1) + '%';
const line = (label, val) => console.log('  ' + label.padEnd(22) + val);
console.log('=== Choice-of-History · Monte Carlo 平衡验证（N=' + N + ' 局，中性玩家假设）===');
console.log('常量（自 index.html 抽取）：LIMIT_NORMAL=' + LIMIT_NORMAL + ' LIMIT_CRISIS=' + LIMIT_CRISIS +
            ' P_RAND=' + P_RAND + ' MID_THRESHOLD=' + MID_THRESHOLD + ' MID_CRISIS_PROB=' + MID_CRISIS_PROB);
console.log('');
console.log('【1) 月均净 delta / 维（机制层漂移；接近 0 = 可被对冲，非单维锁死）】');
for (const k of DIMS) {
  const mean = agg.netDeltaSum[k] / monthCount;
  const variance = Math.max(0, agg.netDeltaSqSum[k] / monthCount - mean * mean);
  const std = Math.sqrt(variance);
  line(k, '月均 ' + (mean >= 0 ? '+' : '') + mean.toFixed(4) + ' / 标准差 ' + std.toFixed(3));
}
console.log('');
console.log('【2) 危机率（每月为"数值危机"的占比，目标 ≤8%）】');
line('危机月 / 玩家事件月', agg.crisisMonths + ' / ' + agg.playerMonths + ' = ' + (agg.playerMonths ? (100 * agg.crisisMonths / agg.playerMonths).toFixed(2) + '%' : 'n/a'));
line('危机月 / 总月', (100 * agg.crisisMonths / monthCount).toFixed(2) + '%');
console.log('');
console.log('【3) 崩盘归因（随机时局致崩盘占比，目标 < 总崩盘 15%）】');
line('总崩盘局数', agg.collapseTotal + ' (' + pct(agg.collapseTotal) + ')');
line('其中随机触发', agg.randomCausedCollapse + ' (' + (agg.collapseTotal ? (100 * agg.randomCausedCollapse / agg.collapseTotal).toFixed(1) + '% of 崩盘' : 'n/a') + ')');
line('崩盘触发维分布', JSON.stringify(agg.endDims));
console.log('');
console.log('【结局与终局】');
line('平均在位月', (agg.months / N).toFixed(1) + ' 月（≈' + (agg.months / N / 12).toFixed(1) + ' 年）');
line('平均终局 govAvg', (agg.govSum / N).toFixed(1) + ' / 100（含 health 不含 tech）');
line('court 顶满(≥95)率', pct(agg.courtPinned));
line('结局分布', JSON.stringify(agg.verdicts));
line('终局原因', JSON.stringify(agg.endReasons));
console.log('');
console.log('说明：本模拟仅验证"机制层"在中性玩家下的稳态；AI 事件真实数值分布为独立未知量，须在实机 playtest 另测。');
