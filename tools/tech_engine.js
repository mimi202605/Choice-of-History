/* =============================================================================
 * Choice of History —— 科技树计算引擎 (tech_engine.js)
 * -----------------------------------------------------------------------------
 * 职责：
 *   1. 由「皇帝(朝代/时代) + 玩家已加点科技树」计算六维属性增益；
 *   2. 识别「超前科技」(age > 皇帝时代)，按差距衰减后仍给予真实增益；
 *   3. 产出 AI 可读的 techProfile（含超前科技清单与叙述文案），供大语言模型
 *      理解玩家所拥有的越代科技，并据以生成事件后果与叙事。
 *
 * 用法（浏览器 / Node 通用）：
 *   const engine = new TechEngine(treeJson, presetsJson);
 *   const profile = engine.compute(emperor, ownedTechs);
 *   // emperor: {dynasty, eraLevel?}  eraLevel 缺省由 dynasty 推导
 *   // ownedTechs: { "agri_03_00": 3, ... }  节点id -> 等级
 * ========================================================================== */
(function (global) {
  "use strict";

  // 朝代 → 时代等级（与 tools/gen_techtree.py 保持一致）
  const DYNASTY_ERA = {
    "夏": 1, "商": 2, "周": 2, "秦": 3,
    "汉": 4, "新": 4, "三国": 4,
    "晋": 5, "南北朝": 5, "隋": 5, "唐": 5, "五代": 5,
    // 南北朝诸朝（应属中古 era5；皇帝 dynasty 字段用具体朝名，此处补全映射）
    "齐": 5, "梁": 5, "陈": 5, "北魏": 5, "东魏": 5, "西魏": 5, "北齐": 5, "北周": 5,
    // 五代诸朝（应属中古 era5；同上，补全子朝映射）
    "后梁": 5, "后唐": 5, "后晋": 5, "后汉": 5, "后周": 5,
    "宋": 6, "辽": 6, "金": 6, "西夏": 6, "元": 6,
    "明": 7, "清": 8,
    "未来近": 9, "未来中": 11, "未来远": 13, "终末": 14,
    // 外国篇 period（与 tools/gen_techtree.py 的 DYNASTY_ERA 同步）
    "开国立宪": 8, "扩张与分裂": 8, "重建与崛起": 9, "冷战与当代": 11,
    "诺曼—金雀花": 6, "都铎—斯图亚特": 7, "汉诺威—温莎": 8,
    "王政": 3, "共和": 4, "帝国": 5, "拜占庭": 6,
    "留里克王朝": 5, "罗曼诺夫王朝": 7, "苏联": 9, "俄罗斯联邦": 11,
  };

  // 子朝代 → 父朝代（汇总朝）：皇帝 dynasty 字段常写具体朝名（后梁/北魏…），
  // 而 DYNASTY_ERA / 预设只登记汇总朝（五代/南北朝）。查不到时回退到父朝，
  // 既补 era 映射、也能借到父朝初始科技树，杜绝缺映射掉到 era1（蒙昧石器时代）。
  const DYN_SUB_TO_PARENT = {
    "齐": "南北朝", "梁": "南北朝", "陈": "南北朝",
    "北魏": "南北朝", "东魏": "南北朝", "西魏": "南北朝", "北齐": "南北朝", "北周": "南北朝",
    "后梁": "五代", "后唐": "五代", "后晋": "五代", "后汉": "五代", "后周": "五代",
  };

  const ATTR_CN = { treasury: "国库", people: "民心", military: "军事", court: "朝政", health: "健康", tech: "科技" };
  const ATTRS = ["treasury", "people", "military", "court", "health", "tech"];

  // 越代梯度（代际对称轴 · 超前侧）：按 gap 分 t1/t2/t3+ 三档
  //  t1 领先1代：实用效率最高、减免稳定（广度保稳定）
  //  t2 领先2代：实用效率中、减免中
  //  t3+ 领先3代及以上：实用效率最低（知识难落地）、减免低概率高爆发（深度博爆发）
  const AHEAD_TIERS = {
    1: { name: "稳健·越一代", factor: 0.85, mit: { base: 0.50, min: 0.25, max: 0.45 } },
    2: { name: "进取·越二代", factor: 0.60, mit: { base: 0.42, min: 0.30, max: 0.55 } },
    3: { name: "奇术·越三代+", factor: 0.38, mit: { base: 0.30, min: 0.40, max: 0.78 } },
  };
  function gapTier(gap) { return gap <= 0 ? 0 : (gap === 1 ? 1 : (gap === 2 ? 2 : 3)); }
  function tierCfg(gap) { const t = gapTier(gap); return AHEAD_TIERS[t] || AHEAD_TIERS[3]; }
  function aheadDamp(gap) {
    if (gap <= 0) return 1;
    const t = gapTier(gap);
    if (t === 1) return AHEAD_TIERS[1].factor;
    if (t === 2) return AHEAD_TIERS[2].factor;
    // t3+：更深越代实用效率更低，但保底 0.15（知识本身有价值，只是难落地）
    return Math.max(0.15, AHEAD_TIERS[3].factor - 0.05 * (gap - 3));
  }

  class TechEngine {
    constructor(tree, presets) {
      this.tree = tree;
      this.presets = presets && presets.dynasties ? presets.dynasties : (presets || {});
      this.nodeById = {};
      (tree.nodes || []).forEach(n => { this.nodeById[n.id] = n; });
      this.specialToAttr = (tree.meta && tree.meta.specialToAttr) || {};
      this.ages = (tree.meta && tree.meta.ages) || [];
      this.branches = (tree.meta && tree.meta.branches) || [];
    }

    eraLevelOf(emperor) {
      if (emperor.eraLevel) return emperor.eraLevel;
      const d = emperor.dynasty;
      const k = DYNASTY_ERA[d] ? d : (DYN_SUB_TO_PARENT[d] || d);
      return DYNASTY_ERA[k] || 1;
    }

    /** 取某朝代的时代预设（皇帝初始科技树） */
    presetFor(dynasty) {
      const k = this.presets[dynasty] ? dynasty : (DYN_SUB_TO_PARENT[dynasty] || dynasty);
      const p = this.presets[k];
      if (!p) return {};
      const out = {};
      for (const id in p.techs) out[id] = p.techs[id];
      return out;
    }

    /**
     * 核心计算：返回 techProfile
     */
    compute(emperor, ownedTechs) {
      ownedTechs = ownedTechs || {};
      const eraLevel = this.eraLevelOf(emperor);
      const eraName = (this.ages.find(a => a.id === eraLevel) || {}).name || ("时代" + eraLevel);
      const civ = this.civOf(emperor);

      const attrBonus = { treasury: 0, people: 0, military: 0, court: 0, health: 0, tech: 0 };
      const specials = {};
      const perBranch = {};
      const aheadTechs = [];
      let totalLevels = 0, aheadLevels = 0, ownCount = 0;
      let presentCount = 0, aheadCount = 0, legacyCount = 0;

      for (const id in ownedTechs) {
        const node = this.nodeById[id];
        const lvl = ownedTechs[id];
        if (!node || lvl <= 0) continue;
        ownCount++;
        totalLevels += lvl;

        const gap = node.age - eraLevel;
        const factor = aheadDamp(gap);
        const isAhead = gap > 0;
        if (gap > 0) aheadCount++;
        else if (gap === 0) presentCount++;
        else legacyCount++;

        // 主/次属性增益
        for (const a in node.bonusPerLevel) {
          attrBonus[a] += node.bonusPerLevel[a] * lvl * factor;
        }
        // 特殊增益 → 对应属性（specialBonus 随时代缩放，缺省为 1）
        const sattr = node.specialAttr || this.specialToAttr[node.special];
        if (sattr) attrBonus[sattr] += (node.specialBonus || 1) * lvl * factor;
        specials[node.special] = (specials[node.special] || 0) + lvl;

        // 分支聚合
        if (!perBranch[node.branch]) perBranch[node.branch] = { name: this._civBranchName(node, civ), count: 0, levels: 0, attrBonus: 0 };
        perBranch[node.branch].count++;
        perBranch[node.branch].levels += lvl;

        if (isAhead) {
          aheadLevels += lvl;
          aheadTechs.push({
            id: node.id, name: this._civName(node, civ), branch: this._civBranchName(node, civ), track: this._civTrackName(node, civ),
            age: node.age, ageName: node.ageName, gap: gap, level: lvl,
            factor: +factor.toFixed(2), tier: gapTier(gap),
            bonus: this._nodeAttrBonus(node, lvl, factor),
            desc: node.desc,
          });
        }
      }

      // 四舍五入属性（六维为整数）
      const attrBonusR = {};
      ATTRS.forEach(a => { attrBonusR[a] = Math.round(attrBonus[a]); });
      aheadTechs.sort((x, y) => y.gap - x.gap || y.level - x.level);

      // 超前科技对六维的额外贡献（单独统计，便于 AI 叙述）
      const aheadAttrBonus = {};
      aheadTechs.forEach(t => {
        for (const a in t.bonus) aheadAttrBonus[a] = (aheadAttrBonus[a] || 0) + t.bonus[a];
      });
      ATTRS.forEach(a => { aheadAttrBonus[a] = Math.round(aheadAttrBonus[a] || 0); });

      // —— 代际对称轴 · 落后侧：eraDeficit ——
      // 仅历史时代(eraLevel<=8)启用；当「越代科技数 > 当世科技数」即视其重未来而轻当世，
      // 对民心/朝政/军事/国库施加微弱持续侵蚀（每单位0.5、封顶8）；补全当世科技(present>=ahead)即消。
      // 未来沙盒朝代(eraLevel>8)几乎全树皆"超前"，落后无意义，故禁用，以免一开局即被碾碎。
      const DEFICIT_PER_UNIT = 0.5, DEFICIT_CAP = 8;
      let deficitUnits = 0, eraDeficit = 0, deficitActive = false;
      if (eraLevel <= 8) {
        deficitUnits = Math.max(0, aheadCount - presentCount);
        eraDeficit = Math.min(DEFICIT_CAP, deficitUnits * DEFICIT_PER_UNIT);
        deficitActive = deficitUnits > 0;
      }
      // 奇术声望(wonder)：领先三代以上科技按 (gap*level) 累计，纯叙事/声望用途，不计入实用增益
      let wonder = 0;
      aheadTechs.forEach(t => { if (gapTier(t.gap) === 3) wonder += t.gap * t.level; });

      // 每分支 attrBonus（含超前衰减）
      for (const b in perBranch) {
        let s = 0;
        for (const a of ATTRS) s += attrBonusR[a]; // 占位，实际由分支节点累加更准确
        perBranch[b].attrBonus = s;
      }
      // 精确按分支累加
      const branchAttr = {};
      for (const id in ownedTechs) {
        const node = this.nodeById[id]; const lvl = ownedTechs[id];
        if (!node || lvl <= 0) continue;
        const factor = aheadDamp(node.age - eraLevel);
        const b = node.branch;
        branchAttr[b] = branchAttr[b] || { treasury: 0, people: 0, military: 0, court: 0, health: 0, tech: 0 };
        for (const a in node.bonusPerLevel) branchAttr[b][a] += node.bonusPerLevel[a] * lvl * factor;
        const sattr = node.specialAttr || this.specialToAttr[node.special];
        if (sattr) branchAttr[b][sattr] += (node.specialBonus || 1) * lvl * factor;
      }
      for (const b in perBranch) {
        perBranch[b].attrBonus = {};
        ATTRS.forEach(a => perBranch[b].attrBonus[a] = Math.round((branchAttr[b] || {})[a] || 0));
      }

      const profile = {
        emperor: emperor.dynasty || "?",
        eraLevel, eraName,
        totalTechsOwned: ownCount,
        totalLevels,
        attrBonus: attrBonusR,
        specials,
        perBranch,
        presentCount, aheadCount, legacyCount,
        wonder,
        ahead: {
          count: aheadTechs.length,
          levels: aheadLevels,
          maxGap: aheadTechs.length ? aheadTechs[0].gap : 0,
          attrBonus: aheadAttrBonus,
          techs: aheadTechs,
        },
        eraDeficit: { units: deficitUnits, points: +eraDeficit.toFixed(2), active: deficitActive, capped: eraDeficit >= DEFICIT_CAP },
        aiSummary: this._aiSummary(emperor, eraLevel, eraName, attrBonusR, aheadAttrBonus, aheadTechs, ownCount, totalLevels, presentCount, aheadCount, deficitActive, wonder),
      };
      return profile;
    }

    _nodeAttrBonus(node, lvl, factor) {
      const b = {};
      for (const a in node.bonusPerLevel) b[a] = node.bonusPerLevel[a] * lvl * factor;
      const sattr = node.specialAttr || this.specialToAttr[node.special];
      if (sattr) b[sattr] = (b[sattr] || 0) + (node.specialBonus || 1) * lvl * factor;
      const out = {};
      for (const a in b) out[a] = Math.round(b[a]);
      return out;
    }

    /** 生成给 AI（大语言模型）阅读的科技档案叙述 */
    _aiSummary(emperor, eraLevel, eraName, attrBonus, aheadAttr, aheadTechs, ownCount, totalLevels, presentCount, aheadCount, deficitActive, wonder) {
      const top = ATTRS.slice().sort((a, b) => Math.abs(attrBonus[b]) - Math.abs(attrBonus[a]))
        .filter(a => attrBonus[a] !== 0)
        .map(a => `${ATTR_CN[a]}+${attrBonus[a]}`).join("、");
      let s = `【科技档案】${emperor.dynasty || "皇帝"}身处「${eraName}」(时代等级${eraLevel})，`;
      s += `已拥科技 ${ownCount} 项、累计 ${totalLevels} 级；`;
      s += `六维增益：${top || "无"}。`;
      if (aheadTechs.length) {
        const tc = { 1: 0, 2: 0, 3: 0 };
        aheadTechs.forEach(t => { tc[gapTier(t.gap)]++; });
        const tierDesc = [tc[1] ? `稳健越代${tc[1]}项` : "", tc[2] ? `进取越代${tc[2]}项` : "", tc[3] ? `奇术越代${tc[3]}项` : ""].filter(Boolean).join("、");
        s += `其越代科技 ${aheadTechs.length} 项（${tierDesc}）：`;
        s += aheadTechs.slice(0, 8).map(t =>
          `${t.name}(${t.branch}·${t.ageName}，领先${t.gap}代[${AHEAD_TIERS[gapTier(t.gap)].name}]，lv${t.level}，落地效率${Math.round(t.factor * 100)}%)`
        ).join("；") + "。";
        const real = ATTRS.filter(a => aheadAttr[a] !== 0);
        if (real.length) {
          s += `越代科技因时代基础薄弱而衰减（越深越难落地）：仍实质提升其${real.map(a => ATTR_CN[a]).join("、")}（${real.map(a => ATTR_CN[a] + "+" + aheadAttr[a]).join("、")}）；`;
          s += `其中领先三代以上者（奇术）增益最薄却积「奇术声望」(wonder ${wonder})，朝臣或以「奇技淫巧」非之，然其带来之变局不可小觑。`;
        } else {
          s += `然因时代鸿沟过巨，越代科技之增益近乎为零，仅余「名」而无「实」，史官当记其「好异梦而远人事」。`;
        }
      } else {
        s += `暂无超越当世的科技，科技树与时代相称。`;
      }
      if (deficitActive) {
        s += `然其重未来之术而轻当世之基：当世科技(${presentCount}项)少于越代科技(${aheadCount}项)，科技落后于世，民心/朝政/军事/国库皆受微弱侵蚀（补全当世科技即消）。`;
      }
      return s;
    }

    // —— 按文明显示名解析（cn 一律返回中文原值）——
    civOf(emperor) { return (emperor && emperor.civilization) || "cn"; }

    _civName(node, civ) {
      if (civ === "cn" || !node.names) return node.name;
      if (civ === "rome") return node.names.rome || node.name;
      return node.names.foreign || node.name; // us / uk / ru
    }
    _civBranchName(node, civ) {
      const c = node.civBranch || null;
      if (!c || civ === "cn") return node.branchName;
      if (civ === "rome") return c.rome || node.branchName;
      return c.foreign || node.branchName;
    }
    _civTrackName(node, civ) {
      const c = node.trackNames || null;
      if (!c || civ === "cn") return node.track;
      if (civ === "rome") return c.rome || node.track;
      return c.foreign || node.track;
    }

    /** 解锁/升级某节点需要的科技点数（基于已拥有等级） */
    costToUpgrade(node, currentLevel) {
      if (currentLevel >= node.maxLevel) return null;
      return node.cost.base + node.cost.perLevel * currentLevel;
    }
  }

  // Node / 浏览器导出
  if (typeof module !== "undefined" && module.exports) module.exports = { TechEngine, DYNASTY_ERA, aheadDamp, gapTier, tierCfg, AHEAD_TIERS };
  global.TechEngine = TechEngine;
  global.TECH_DYNASTY_ERA = DYNASTY_ERA;
  global.TECH_AHEAD_TIERS = AHEAD_TIERS;
  global.gapTier = gapTier;
  global.tierCfg = tierCfg;
})(typeof window !== "undefined" ? window : globalThis);
