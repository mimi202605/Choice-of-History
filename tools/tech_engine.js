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
    "宋": 6, "辽": 6, "金": 6, "西夏": 6, "元": 6,
    "明": 7, "清": 8,
    "未来近": 9, "未来中": 11, "未来远": 13, "终末": 14,
  };

  const ATTR_CN = { treasury: "国库", people: "民心", military: "军事", court: "朝政", health: "健康", tech: "科技" };
  const ATTRS = ["treasury", "people", "military", "court", "health", "tech"];

  // 超前科技衰减：差距越大，落地效率越低，但永不为 0（知识本身有价值）
  function aheadDamp(gap) {
    if (gap <= 0) return 1;
    return Math.max(0.15, 1 - 0.18 * gap);
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
      return DYNASTY_ERA[emperor.dynasty] || 1;
    }

    /** 取某朝代的时代预设（皇帝初始科技树） */
    presetFor(dynasty) {
      const p = this.presets[dynasty];
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

      const attrBonus = { treasury: 0, people: 0, military: 0, court: 0, health: 0, tech: 0 };
      const specials = {};
      const perBranch = {};
      const aheadTechs = [];
      let totalLevels = 0, aheadLevels = 0, ownCount = 0;

      for (const id in ownedTechs) {
        const node = this.nodeById[id];
        const lvl = ownedTechs[id];
        if (!node || lvl <= 0) continue;
        ownCount++;
        totalLevels += lvl;

        const gap = node.age - eraLevel;
        const factor = aheadDamp(gap);
        const isAhead = gap > 0;

        // 主/次属性增益
        for (const a in node.bonusPerLevel) {
          attrBonus[a] += node.bonusPerLevel[a] * lvl * factor;
        }
        // 特殊增益 → 对应属性
        const sattr = node.specialAttr || this.specialToAttr[node.special];
        if (sattr) attrBonus[sattr] += lvl * factor;
        specials[node.special] = (specials[node.special] || 0) + lvl;

        // 分支聚合
        if (!perBranch[node.branch]) perBranch[node.branch] = { name: node.branchName, count: 0, levels: 0, attrBonus: 0 };
        perBranch[node.branch].count++;
        perBranch[node.branch].levels += lvl;

        if (isAhead) {
          aheadLevels += lvl;
          aheadTechs.push({
            id: node.id, name: node.name, branch: node.branchName, track: node.track,
            age: node.age, ageName: node.ageName, gap: gap, level: lvl,
            factor: +factor.toFixed(2),
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
        if (sattr) branchAttr[b][sattr] += lvl * factor;
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
        ahead: {
          count: aheadTechs.length,
          levels: aheadLevels,
          maxGap: aheadTechs.length ? aheadTechs[0].gap : 0,
          attrBonus: aheadAttrBonus,
          techs: aheadTechs,
        },
        aiSummary: this._aiSummary(emperor, eraLevel, eraName, attrBonusR, aheadAttrBonus, aheadTechs, ownCount, totalLevels),
      };
      return profile;
    }

    _nodeAttrBonus(node, lvl, factor) {
      const b = {};
      for (const a in node.bonusPerLevel) b[a] = node.bonusPerLevel[a] * lvl * factor;
      const sattr = node.specialAttr || this.specialToAttr[node.special];
      if (sattr) b[sattr] = (b[sattr] || 0) + lvl * factor;
      const out = {};
      for (const a in b) out[a] = Math.round(b[a]);
      return out;
    }

    /** 生成给 AI（大语言模型）阅读的科技档案叙述 */
    _aiSummary(emperor, eraLevel, eraName, attrBonus, aheadAttr, aheadTechs, ownCount, totalLevels) {
      const top = ATTRS.slice().sort((a, b) => Math.abs(attrBonus[b]) - Math.abs(attrBonus[a]))
        .filter(a => attrBonus[a] !== 0)
        .map(a => `${ATTR_CN[a]}+${attrBonus[a]}`).join("、");
      let s = `【科技档案】${emperor.dynasty || "皇帝"}身处「${eraName}」(时代等级${eraLevel})，`;
      s += `已拥科技 ${ownCount} 项、累计 ${totalLevels} 级；`;
      s += `六维增益：${top || "无"}。`;
      if (aheadTechs.length) {
        const maxGap = aheadTechs[0].gap;
        s += `其越代科技 ${aheadTechs.length} 项，最高跨越 ${maxGap} 个时代：`;
        s += aheadTechs.slice(0, 8).map(t =>
          `${t.name}(${t.branch}·${t.ageName}，领先${t.gap}代，lv${t.level}，落地效率${Math.round(t.factor * 100)}%)`
        ).join("；") + "。";
        const real = ATTRS.filter(a => aheadAttr[a] !== 0);
        if (real.length) {
          s += `越代科技虽因时代基础薄弱而衰减，仍实质提升其${real.map(a => ATTR_CN[a]).join("、")}（${real.map(a => ATTR_CN[a] + "+" + aheadAttr[a]).join("、")}），`;
          s += `应被视为「穿越者之能」：朝臣或以「奇技淫巧」非之，然其带来之国力与变局不可小觑。`;
        } else {
          s += `然因时代鸿沟过巨，越代科技之增益近乎为零，仅余「名」而无「实」，史官当记其「好异梦而远人事」。`;
        }
      } else {
        s += `暂无超越当世的科技，科技树与时代相称。`;
      }
      return s;
    }

    /** 解锁/升级某节点需要的科技点数（基于已拥有等级） */
    costToUpgrade(node, currentLevel) {
      if (currentLevel >= node.maxLevel) return null;
      return node.cost.base + node.cost.perLevel * currentLevel;
    }
  }

  // Node / 浏览器导出
  if (typeof module !== "undefined" && module.exports) module.exports = { TechEngine, DYNASTY_ERA, aheadDamp };
  global.TechEngine = TechEngine;
  global.TECH_DYNASTY_ERA = DYNASTY_ERA;
})(typeof window !== "undefined" ? window : globalThis);
