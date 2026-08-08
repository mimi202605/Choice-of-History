# -*- coding: utf-8 -*-
"""
择决千秋 · 科技具体作用注入器（非破坏式增强）
============================================
给 data/tech_tree.json 中每个科技节点补充：
  - node["effect"]   : 结构化效果数组（type/target/perTier/cap），供引擎解析
  - node["effectDesc"]: 一句话具体作用文案（含随时代放大的数值），供科技卡展示
重写 node["functionDesc"] = 原功能介绍 + 具体作用文案。

设计约束（见对话）：
  - 效果种类由 (分支×轨道) 决定 → 81 种不同机制原型；数值随 age(时代档) 与 level 放大。
  - 所有 magnitude 有 rationale，但未经 playtest，标 [待playtest校准]。
  - 不重跑 gen_techtree.py（保住已清理的命名/占位修复）；先备份再改，可逆。
"""
import json, os, shutil, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE, "data", "tech_tree.json")

ATTR_CN = {"treasury": "国库", "people": "民心", "military": "军事", "court": "朝政", "health": "健康", "tech": "科技"}
CRISIS_CN = {"flood": "水患", "famine": "饥荒", "epidemic": "疫疠", "wound": "战伤", "dispute": "讼争", "curse": "妖异"}
FACTION_CN = {"宗室": "宗室", "士大夫": "士大夫", "边将": "边将", "商贾": "商贾"}
DIM_CN = {"treasury": "国库", "people": "民心", "military": "军事", "court": "朝政", "health": "健康", "tech": "科技"}

# 81 个 special → 效果数组。perTier 含义：
#   passive/relation/score : 每档(tier)×每级 的绝对增量（passive 为每年正月结算的点数）
#   shield/eventLess/autoResolve/costLess/warEdge : 每档×每级的「百分点」
#     - warEdge winBonus : 战争胜算 +%
#     - warEdge lossMitigate : 战败军事损失 −%
# 差异化原则（第二轮重排）：
#   ① type×target×perTier 三元组尽量唯一 —— 首版有 17 条轨道共用 passive/treasury/0.06，
#      玩家点开卡片看到一模一样的文案，「每项作用不同」的承诺就落空了。
#   ② score 按分支语义散到五维（原先全砸「朝政」，史评通道只有一个出口）。
#   ③ 「料敌」解锁原本无 special 挂载，补给 map（舆图）—— UNLOCK_DOMAIN 四个 key 现已全部有出口。
#   ④ 双效果组合用于「该轨道确实有两重史实作用」的场合（如户版＝税基+史评），不为凑数而加。
EFFECTS = {
    # ===== 农政：以「岁入/民食/灾备」三条线区分 =====
    "yield":      [{"type": "passive", "target": "treasury", "perTier": 0.09, "cap": 2.0}],
    "flood":      [{"type": "shield", "target": "flood", "perTier": 8, "cap": 50}],
    "fertility":  [{"type": "passive", "target": "people", "perTier": 0.07, "cap": 1.6}],
    "seed":       [{"type": "eventLess", "target": "famine", "perTier": 6, "cap": 40}],
    "tool":       [{"type": "passive", "target": "treasury", "perTier": 0.06, "cap": 1.4},
                  {"type": "passive", "target": "tech", "perTier": 0.02, "cap": 0.5}],
    "storage":    [{"type": "shield", "target": "famine", "perTier": 8, "cap": 50}],
    "landlaw":    [{"type": "relation", "target": "士大夫", "perTier": 1, "cap": 8}],
    "reclaim":    [{"type": "passive", "target": "treasury", "perTier": 0.05, "cap": 1.2},
                  {"type": "passive", "target": "people", "perTier": 0.03, "cap": 0.8}],
    "pasture":    [{"type": "passive", "target": "treasury", "perTier": 0.04, "cap": 1.0},
                  {"type": "passive", "target": "military", "perTier": 0.03, "cap": 0.8}],
    # ===== 军工：胜算(winBonus) 与 减损(lossMitigate) 两条线，梯度按兵种价值 =====
    "armor":      [{"type": "warEdge", "target": "lossMitigate", "perTier": 10, "cap": 50}],
    "weapon":     [{"type": "warEdge", "target": "winBonus", "perTier": 2.0, "cap": 15}],
    "formation":  [{"type": "warEdge", "target": "winBonus", "perTier": 1.8, "cap": 14}],
    "defense":    [{"type": "warEdge", "target": "lossMitigate", "perTier": 8, "cap": 40}],
    "cavalry":    [{"type": "warEdge", "target": "winBonus", "perTier": 2.2, "cap": 16}],
    "navy":       [{"type": "warEdge", "target": "winBonus", "perTier": 1.6, "cap": 12}],
    "gunpowder":  [{"type": "warEdge", "target": "winBonus", "perTier": 2.5, "cap": 18}],
    "intel":      [{"type": "warEdge", "target": "winBonus", "perTier": 1.4, "cap": 10}],
    "logistics":  [{"type": "warEdge", "target": "lossMitigate", "perTier": 9, "cap": 45}],
    # ===== 营造 =====
    "palace":     [{"type": "score", "target": "court", "perTier": 1, "cap": 4}],
    "bridge":     [{"type": "passive", "target": "treasury", "perTier": 0.05, "cap": 1.2},
                  {"type": "passive", "target": "people", "perTier": 0.02, "cap": 0.5}],
    "road":       [{"type": "passive", "target": "court", "perTier": 0.06, "cap": 1.4}],
    "hydraulics": [{"type": "shield", "target": "flood", "perTier": 9, "cap": 55}],
    "smelt":      [{"type": "passive", "target": "tech", "perTier": 0.07, "cap": 1.6},
                  {"type": "passive", "target": "military", "perTier": 0.02, "cap": 0.5}],
    "machine":    [{"type": "passive", "target": "treasury", "perTier": 0.07, "cap": 1.6}],
    "brick":      [{"type": "score", "target": "people", "perTier": 1, "cap": 4}],
    "city":       [{"type": "passive", "target": "treasury", "perTier": 0.05, "cap": 1.2},
                  {"type": "relation", "target": "商贾", "perTier": 1, "cap": 6}],
    "ship":       [{"type": "passive", "target": "treasury", "perTier": 0.06, "cap": 1.5},
                  {"type": "passive", "target": "military", "perTier": 0.02, "cap": 0.5}],
    # ===== 商工 =====
    "market":     [{"type": "passive", "target": "treasury", "perTier": 0.08, "cap": 1.8}],
    "coin":       [{"type": "costLess", "target": "research", "perTier": 4, "cap": 25}],
    "workshop":   [{"type": "passive", "target": "treasury", "perTier": 0.07, "cap": 1.6},
                  {"type": "passive", "target": "tech", "perTier": 0.02, "cap": 0.5}],
    "shipping":   [{"type": "passive", "target": "treasury", "perTier": 0.075, "cap": 1.7}],
    "saltiron":   [{"type": "passive", "target": "treasury", "perTier": 0.09, "cap": 2.0},
                  {"type": "passive", "target": "court", "perTier": 0.02, "cap": 0.5}],
    "teahorse":   [{"type": "relation", "target": "边将", "perTier": 1, "cap": 8}],
    "bank":       [{"type": "costLess", "target": "research", "perTier": 3, "cap": 20},
                  {"type": "relation", "target": "商贾", "perTier": 1, "cap": 6}],
    "mining":     [{"type": "passive", "target": "tech", "perTier": 0.06, "cap": 1.5}],
    "craft":      [{"type": "passive", "target": "treasury", "perTier": 0.05, "cap": 1.2},
                  {"type": "passive", "target": "tech", "perTier": 0.03, "cap": 0.8}],
    # ===== 文教 =====
    "school":     [{"type": "relation", "target": "士大夫", "perTier": 1, "cap": 8},
                  {"type": "passive", "target": "people", "perTier": 0.02, "cap": 0.5}],
    "exam":       [{"type": "score", "target": "court", "perTier": 1, "cap": 4},
                  {"type": "unlock", "target": "选才", "label": "选才", "domain": "court"}],
    "history":    [{"type": "score", "target": "court", "perTier": 1, "cap": 3},
                  {"type": "relation", "target": "士大夫", "perTier": 1, "cap": 5}],
    "book":       [{"type": "score", "target": "people", "perTier": 1, "cap": 4},
                  {"type": "relation", "target": "士大夫", "perTier": 1, "cap": 4}],
    "math":       [{"type": "passive", "target": "tech", "perTier": 0.07, "cap": 1.6}],
    "geo":        [{"type": "warEdge", "target": "winBonus", "perTier": 2.0, "cap": 12},
                  {"type": "passive", "target": "tech", "perTier": 0.02, "cap": 0.5}],
    "diplomacy":  [{"type": "relation", "target": "边将", "perTier": 1, "cap": 8},
                  {"type": "relation", "target": "商贾", "perTier": 1, "cap": 4}],
    "ritual":     [{"type": "relation", "target": "宗室", "perTier": 1, "cap": 8}],
    "educate":    [{"type": "passive", "target": "people", "perTier": 0.07, "cap": 1.6},
                  {"type": "relation", "target": "士大夫", "perTier": 1, "cap": 3}],
    # ===== 医养 =====
    "herb":       [{"type": "shield", "target": "epidemic", "perTier": 7, "cap": 50}],
    "acup":       [{"type": "passive", "target": "health", "perTier": 0.07, "cap": 1.6}],
    "formula":    [{"type": "shield", "target": "epidemic", "perTier": 6, "cap": 45}],
    "surgery":    [{"type": "shield", "target": "wound", "perTier": 7, "cap": 50}],
    # 防疫＝既减损又降发生率（首版误用 autoResolve，与 shield 走同一通道且文案重复）
    "epidemic":   [{"type": "shield", "target": "epidemic", "perTier": 9, "cap": 60},
                  {"type": "eventLess", "target": "epidemic", "perTier": 5, "cap": 35}],
    "health":     [{"type": "passive", "target": "health", "perTier": 0.06, "cap": 1.5}],
    "gyne":       [{"type": "passive", "target": "health", "perTier": 0.05, "cap": 1.2},
                  {"type": "passive", "target": "people", "perTier": 0.03, "cap": 0.8}],
    "vet":        [{"type": "passive", "target": "people", "perTier": 0.05, "cap": 1.2},
                  {"type": "passive", "target": "military", "perTier": 0.02, "cap": 0.6}],
    "shaman":     [{"type": "passive", "target": "health", "perTier": 0.04, "cap": 1.0},
                  {"type": "shield", "target": "curse", "perTier": 4, "cap": 25}],
    # ===== 天文数理 =====
    "calendar":   [{"type": "score", "target": "people", "perTier": 1, "cap": 4},
                  {"type": "eventLess", "target": "famine", "perTier": 3, "cap": 20}],
    "astro":      [{"type": "score", "target": "court", "perTier": 1, "cap": 4},
                  {"type": "passive", "target": "tech", "perTier": 0.02, "cap": 0.5}],
    "mathclassic":[{"type": "passive", "target": "tech", "perTier": 0.07, "cap": 1.6},
                  {"type": "score", "target": "court", "perTier": 1, "cap": 2}],
    "survey":     [{"type": "warEdge", "target": "winBonus", "perTier": 1.8, "cap": 12},
                  {"type": "passive", "target": "tech", "perTier": 0.02, "cap": 0.5}],
    "map":        [{"type": "warEdge", "target": "winBonus", "perTier": 2.0, "cap": 12},
                  {"type": "unlock", "target": "料敌", "label": "料敌", "domain": "war"}],
    "weather":    [{"type": "eventLess", "target": "famine", "perTier": 6, "cap": 40},
                  {"type": "eventLess", "target": "flood", "perTier": 4, "cap": 25}],
    "physics":    [{"type": "passive", "target": "tech", "perTier": 0.08, "cap": 1.8}],
    "chem":       [{"type": "passive", "target": "tech", "perTier": 0.06, "cap": 1.5},
                  {"type": "shield", "target": "epidemic", "perTier": 3, "cap": 20}],
    "natural":    [{"type": "score", "target": "health", "perTier": 1, "cap": 3},
                  {"type": "passive", "target": "health", "perTier": 0.04, "cap": 1.0}],
    # ===== 律礼 =====
    "penal":      [{"type": "relation", "target": "士大夫", "perTier": 1, "cap": 8},
                  {"type": "shield", "target": "dispute", "perTier": 4, "cap": 25}],
    "rituallaw":  [{"type": "relation", "target": "宗室", "perTier": 1, "cap": 6},
                  {"type": "relation", "target": "士大夫", "perTier": 1, "cap": 4}],
    "landdeed":   [{"type": "shield", "target": "dispute", "perTier": 8, "cap": 50}],
    "census":     [{"type": "score", "target": "treasury", "perTier": 1, "cap": 4},
                  {"type": "passive", "target": "treasury", "perTier": 0.04, "cap": 1.0}],
    "censor":     [{"type": "relation", "target": "士大夫", "perTier": 1, "cap": 6},
                  {"type": "score", "target": "court", "perTier": 1, "cap": 3},
                  {"type": "eventLess", "target": "dispute", "perTier": 3, "cap": 20}],
    "border":     [{"type": "relation", "target": "边将", "perTier": 1, "cap": 8},
                  {"type": "warEdge", "target": "winBonus", "perTier": 1.5, "cap": 10}],
    "clan":       [{"type": "relation", "target": "宗室", "perTier": 1, "cap": 8},
                  {"type": "score", "target": "court", "perTier": 1, "cap": 2}],
    "militarylaw":[{"type": "warEdge", "target": "lossMitigate", "perTier": 8, "cap": 40},
                  {"type": "relation", "target": "边将", "perTier": 1, "cap": 5}],
    "lawsuit":    [{"type": "shield", "target": "dispute", "perTier": 7, "cap": 45}],
    # ===== 方技玄术 =====
    "alchemy":    [{"type": "passive", "target": "health", "perTier": 0.05, "cap": 1.2},
                  {"type": "passive", "target": "tech", "perTier": 0.03, "cap": 0.8}],
    "divin":      [{"type": "unlock", "target": "占断", "label": "占断", "domain": "crisis"}],
    "fengshui":   [{"type": "score", "target": "people", "perTier": 1, "cap": 3},
                  {"type": "passive", "target": "court", "perTier": 0.03, "cap": 0.8}],
    "fangji":     [{"type": "passive", "target": "health", "perTier": 0.06, "cap": 1.5},
                  {"type": "passive", "target": "tech", "perTier": 0.02, "cap": 0.5}],
    "kanYu":      [{"type": "warEdge", "target": "winBonus", "perTier": 1.6, "cap": 12},
                  {"type": "score", "target": "military", "perTier": 1, "cap": 3}],
    "talisman":   [{"type": "shield", "target": "curse", "perTier": 6, "cap": 40}],
    "fate":       [{"type": "unlock", "target": "占验", "label": "占验", "domain": "any"}],
    "dunjia":     [{"type": "warEdge", "target": "winBonus", "perTier": 1.8, "cap": 12},
                  {"type": "shield", "target": "curse", "perTier": 3, "cap": 20}],
    "witch":      [{"type": "warEdge", "target": "winBonus", "perTier": 1.5, "cap": 10},
                  {"type": "shield", "target": "curse", "perTier": 4, "cap": 25}],
}

UNSEEN = set(EFFECTS.keys())


def tier_of(age):
    return 1 if age <= 3 else (2 if age <= 7 else 3)


def fmt(sp, age):
    t = sp["type"]
    tg = sp.get("target", "")
    pt = sp.get("perTier", 0)
    cap = sp.get("cap", 0)
    tier = tier_of(age)
    if t == "passive":
        step = pt * tier
        return "每年正月「%s」+%.2f（每级叠加，封顶%.1f/年）" % (ATTR_CN.get(tg, tg), step, cap)
    if t in ("shield", "eventLess", "autoResolve"):
        pct = pt * tier
        cn = CRISIS_CN.get(tg, tg)
        # 三者共用同一条百分比通道，但语义不同，文案必须能区分——
        # 否则同时挂 shield+autoResolve 的节点（如「疫疠」）会输出两句一模一样的描述。
        if t == "shield":
            return "「%s」类灾异结算损失−%d%%·每级（封顶%d%%）" % (cn, pct, cap)
        if t == "autoResolve":
            return "「%s」既发则自行缓解，危害再削−%d%%·每级（封顶%d%%）" % (cn, pct, cap)
        return "「%s」类灾异触发率−%d%%·每级（封顶%d%%）" % (cn, pct, cap)
    if t == "warEdge":
        pct = pt * tier
        label = "战争胜算 +" if tg == "winBonus" else "战败军事损失 −"
        return "%s%d%%·每级（封顶%d%%）" % (label, pct, cap)
    if t == "relation":
        step = pt * tier
        return "派系「%s」好感 +%d·每级（封顶%d）" % (FACTION_CN.get(tg, tg), step, cap)
    if t == "costLess":
        pct = pt * tier
        return "研究科技耗费 −%d%%·每级（封顶%d%%）" % (pct, cap)
    if t == "score":
        step = pt * tier
        return "终局史评「%s」+%d·每级（封顶%d）" % (DIM_CN.get(tg, tg), step, cap)
    if t == "unlock":
        return "相关事件解锁特殊抉择：「%s」" % sp.get("label", tg)
    if t == "ability":
        return "可发动「%s」（冷却%d月）" % (sp.get("label", tg), sp.get("cooldown", 3))
    return ""


def main():
    if not os.path.exists(JSON_PATH):
        print("FATAL: 未找到", JSON_PATH)
        return
    # 备份
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = JSON_PATH + ".bak_effects_" + ts
    shutil.copy2(JSON_PATH, bak)
    print("已备份 ->", os.path.basename(bak))

    data = json.load(open(JSON_PATH, encoding="utf-8"))
    nodes = data.get("nodes", [])
    n_total = len(nodes)
    n_eff = 0
    n_desc = 0
    missing = []
    specials_seen = set()

    for n in nodes:
        sp_list = EFFECTS.get(n.get("special"))
        if sp_list is None:
            missing.append(n.get("id"))
            continue
        specials_seen.add(n["special"])
        UNSEEN.discard(n["special"])
        # 写结构化 effect（深拷贝，避免脚本间共享引用）
        n["effect"] = [dict(s) for s in sp_list]
        eff = "; ".join(fmt(s, n["age"]) for s in sp_list)
        n["effectDesc"] = eff
        base = (n.get("functionDesc") or "").strip()
        # 去掉旧版可能已追加的 effectDesc 残留（以「｜」分隔标记）
        if "｜" in base:
            base = base.split("｜", 1)[0].strip()
        # 幂等保护：若节点原本就没有「一句话作用」，上一轮会把 functionDesc 直接写成 eff，
        # 再跑一次时 base 就等于 eff，拼出「eff ｜ eff」重复文案（曾波及 196 个节点）。
        # 这里显式识别并清空，保证脚本可反复运行。
        if base == eff:
            base = ""
        n["functionDesc"] = (base + " ｜ " + eff) if base else eff
        n_eff += 1
        n_desc += 1

    json.dump(data, open(JSON_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("节点总数:", n_total, " | 写入 effect:", n_eff, " | 写入 effectDesc:", n_desc)
    print("EFFECTS 覆盖 special 数:", len(specials_seen), "/", len(EFFECTS))

    # 唯一性自检：轨道级效果签名(type/target/perTier 三元组集合)重复率。
    # 「每项科技作用都不相同」的可量化口径 —— 完全同签名的轨道，玩家看到的卡片文案会一模一样。
    sig_map = {}
    for k, v in EFFECTS.items():
        sig = tuple(sorted((s["type"], s.get("target"), s.get("perTier")) for s in v))
        sig_map.setdefault(sig, []).append(k)
    dups = {s: ks for s, ks in sig_map.items() if len(ks) > 1}
    uniq = len(sig_map)
    print("轨道效果签名: %d/%d 唯一 (%.0f%%)" % (uniq, len(EFFECTS), uniq * 100.0 / len(EFFECTS)))
    if dups:
        print("仍然同签名的轨道组（文案会重复，可接受但需知悉）：")
        for s, ks in sorted(dups.items(), key=lambda x: -len(x[1])):
            print("   ", "、".join(ks), "->", s[0][0] + "/" + str(s[0][1]) + "/" + str(s[0][2]))
    if UNSEEN:
        print("⚠ 未使用的 EFFECTS key（数据里无对应 special）:", sorted(UNSEEN))
    if missing:
        print("⚠ 数据中无 effect 映射的节点 special:", missing[:20], "...共", len(missing))


if __name__ == "__main__":
    main()
