# -*- coding: utf-8 -*-
"""
择决千秋 · 科技具体作用注入器（非破坏式增强，按 age 差异化版）
======================================================
给 data/tech_tree.json 中每个科技节点补充：
  - node["effect"]   : 结构化效果数组（type/target/perTier/cap），供引擎解析
  - node["effectDesc"]: 一句话具体作用文案（含随时代放大的数值），供科技卡展示
重写 node["functionDesc"] = 原功能介绍 + 具体作用文案。

设计约束（见对话，2026-08-08 → 第四轮修正）：
  - **粒度升级为 (special, age)**：旧版按「时代分带」(early/mid/late/peak 4 档) 注入，
    同一轨道、落在同一档的相邻 age 必然拿到完全相同的 effect（如曲辕犁 age5 与占城稻
    age6 同为 yield+mid → 效果文案一字不差）。本轮改为每个科技按其 age(1..14) 取一条
    **专属演进序列**，相邻 age 的效果类型强制不同 → 每个科技都体现出差异化。
  - **短码序列**：每个 special 写一条 14 段空格分隔的短码串（复合用 '+' 连接），
    脚本按 (age-1) 取对应段。短码 → (type/target/perTier/cap) 见 SHORTCODE。
  - **全部当代通道**：passive(每年正月属性) / shield(灾异损失−) / eventLess(灾异触发−)
    / warEdge(战争) / relation(派系) / costLess(研究费−) / unlock(特殊抉择)。
    **已移除 score（终评）通道**——用户明确要求「影响当代的」。
  - 引擎缩放公式保持 tierOfAge(age) 不变（age≤3→1, ≤7→2, ≥8→3），本脚本只改效果「类型」
    的 age 分布，不动 perTier 数值体系，避免动摇全局平衡。
  - 相邻 age 类型不同是硬约束（脚本自检会报雷同）；跨带重复的类型因 tier 数值不同
    而使文案数值也不同，不会「完全相同」。
  - 不重跑 gen_techtree.py（保住已清理的命名/占位修复）；先备份再改，可逆。
"""
import json, os, shutil, datetime
from tech_funcdesc_sequences import FUNC_DESC

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE, "data", "tech_tree.json")

ATTR_CN = {"treasury": "国库", "people": "民心", "military": "军事", "court": "朝政", "health": "健康", "tech": "科技"}
CRISIS_CN = {"flood": "水患", "famine": "饥荒", "epidemic": "疫疠", "wound": "战伤", "dispute": "讼争", "curse": "妖异"}
FACTION_CN = {"宗室": "宗室", "士大夫": "士大夫", "边将": "边将", "商贾": "商贾"}

# 短码 → (type, target, perTier, cap)。复合项在序列里用 '+' 连接（如 "T+Sm"）。
SHORTCODE = {
    # 属性 passive
    "T": ("passive", "treasury", 0.06, 1.4),
    "P": ("passive", "people", 0.05, 1.2),
    "M": ("passive", "military", 0.05, 1.2),
    "C": ("passive", "court", 0.05, 1.2),
    "H": ("passive", "health", 0.05, 1.2),
    "K": ("passive", "tech", 0.06, 1.4),
    # 派系 relation
    "Z": ("relation", "宗室", 1, 8),
    "Sc": ("relation", "士大夫", 1, 6),
    "Sm": ("relation", "商贾", 1, 6),
    "G": ("relation", "边将", 1, 8),
    # 灾盾 shield
    "Ff": ("shield", "famine", 8, 50),
    "Fl": ("shield", "flood", 8, 50),
    "Ep": ("shield", "epidemic", 7, 50),
    "Wd": ("shield", "wound", 7, 45),
    "Ds": ("shield", "dispute", 5, 30),
    "Cu": ("shield", "curse", 5, 30),
    # 灾减 eventLess
    "ef": ("eventLess", "famine", 6, 40),
    "el": ("eventLess", "flood", 5, 30),
    "ee": ("eventLess", "epidemic", 5, 35),
    "ed": ("eventLess", "dispute", 4, 25),
    "ec": ("eventLess", "curse", 4, 25),
    # 战争 warEdge
    "Wb": ("warEdge", "winBonus", 2.0, 15),
    "Wl": ("warEdge", "lossMitigate", 8, 45),
    # 费减 costLess
    "Cr": ("costLess", "research", 3, 20),
}

# 每个 special 一条 14 段序列（空格分隔，对应 age 1..14；相邻段类型不同，
# 复合用 '+'）。序列即该轨道的「历史演进弧」：早期基础作用 → 中期扩展 → 后期高阶/复合。
# 设计原则：相邻 age 必不同；跨带重复的类型因 tier 数值不同而文案数值也不同。
EFFECTS = {
    # ===== 农政 =====
    "yield":      "T Sm ef Fl P T Sm ef Fl P T+Sm ef Fl Sm",
    "flood":      "Fl Ff el ef Fl Ff el ef Fl Ff el ef Fl Ff",
    "fertility":  "P T P T K P T P T K P T P T",
    "seed":       "ef Ff ef Ff ee ef Ff ef Ff ee ef Ff ef Ff",
    "tool":       "T K T K M T K T K M T K T K",
    "storage":    "Ff T Ff P Ff T Ff P Ff T Ff P Ff T",
    "landlaw":    "Sc P Sc T Sc P Sc T Sc P Sc T Sc P Sc",
    "reclaim":    "T P T P G T P T P G T P T P",
    "pasture":    "T M T M G T M T M G T M T M",
    # ===== 军工 =====
    "armor":      "Wl M Wl M Wl M Wl M G Wl M Wl M Wl",
    "weapon":     "Wb M Wb M Wb M Wb M G Wb M Wb M Wb",
    "formation":  "Wb G Wb G Wb G Wb G M Wb G Wb G Wb",
    "defense":    "Wl M Wl M Wl M Wl M Wd Wl M Wl M Wl",
    "cavalry":    "Wb M Wb M Wb M Wb M G Wb M Wb M Wb",
    "navy":       "Wb M Wb M Wb M Wb M G Wb M Wb M Wb",
    "gunpowder":  "Wb K Wb K Wb K Wb K G Wb K Wb K Wb",
    "intel":      "Wb G Wb G Wb G Wb G M Wb G Wb G Wb",
    "logistics":  "Wl M Wl M Wl M Wl M Sm Wl M Wl M Wl",
    # ===== 营造 =====
    "palace":     "C Z C Z P C Z C Z P C Z C Z P",
    "bridge":     "T P T P Sm T P T P Sm T P T P",
    "road":       "C Sc C Sc T C Sc C Sc T C Sc C Sc",
    "hydraulics": "Fl Ff el Fl Ff el Fl Ff el Fl Ff el Fl Ff",
    "smelt":      "K M K M Sm K M K M Sm K M K M",
    "machine":    "T K T K Sm T K T K Sm T K T K",
    "brick":      "C Z C Z P C Z C Z P C Z C Z P",
    "city":       "T Sm T Sm P T Sm T Sm P T Sm T Sm",
    "ship":       "T M T M Sm T M T M G T M T M",
    # ===== 商工 =====
    "market":     "T Sm T Sm P T Sm T Sm P T Sm T Sm",
    "coin":       "Cr T Cr T Sm Cr T Cr T Sm Cr T Cr T",
    "workshop":   "T K T K Sm T K T K Sm T K T K",
    "shipping":   "T Sm T Sm Wb T Sm T Sm Wb T Sm T Sm",
    "saltiron":   "T C T C Sm T C T C Sm T C T C",
    "teahorse":   "G Sm G Sm Wb G Sm G Sm Wb G Sm G Sm",
    "bank":       "Cr Sm Cr Sm T Cr Sm Cr Sm T Cr Sm Cr Sm",
    "mining":     "K M K M Sm K M K M Sm K M K M",
    "craft":      "T K T K Sm T K T K Sm T K T K",
    # ===== 文教 =====
    "school":     "Sc P Sc P Sm Sc P Sc P Sm Sc P Sc P",
    "exam":       "C U:选才 C Sc C P C Sc C P C Sc C P",
    "history":    "C Sc C Sc P C Sc C Sc P C Sc C Sc",
    "book":       "P Sc P Sc K P Sc P Sc K P Sc P Sc",
    "math":       "K C K C Sc K C K C Sm K C K C",
    "geo":        "Wb K Wb K G Wb K Wb K G Wb K Wb K",
    "diplomacy":  "G Sm G Sm Wb G Sm G Sm Wb G Sm G Sm",
    "ritual":     "Z Sc Z Sc C Z Sc Z Sc P Z Sc Z Sc",
    "educate":    "P Sc P Sc C P Sc P Sc C P Sc P Sc",
    # ===== 医养 =====
    "herb":       "Ep H Ep H Sc Ep H Ep H Sc Ep H Ep H",
    "acup":       "H P H P Sc H P H P Sc H P H P",
    "formula":    "Ep H Ep H Sc Ep H Ep H Sm Ep H Ep H",
    "surgery":    "Wd H Wd H Sc Wd H Wd H G Wd H Wd H",
    "epidemic":   "Ep ee Ep ee H Ep ee Ep ee H Ep ee Ep ee",
    "health":     "H P H P Sc H P H P Sm H P H P",
    "gyne":       "H P H P Sc H P H P Sm H P H P",
    "vet":        "P M P M G P M P M G P M P M",
    "shaman":     "H Cu H Cu Sc H Cu H Cu Sm H Cu H Cu",
    # ===== 天文数理 =====
    "calendar":   "P ef P ef K P ef P ef Sc P ef P ef",
    "astro":      "C K C K Wb C K C K Sc C K C K",
    "mathclassic":"K C K C Sc K C K C Sm K C K C",
    "survey":     "Wb K Wb K G Wb K Wb K Sc Wb K Wb K",
    "map":        "Wb U:料敌 Wb K G Wb U:料敌 Wb K G Wb U:料敌 Wb K",
    "weather":    "ef el ef el P ef el ef el P ef el ef el",
    "physics":    "K C K C Sc K C K C Sm K C K C",
    "chem":       "K Ep K Ep Sm K Ep K Ep Sm K Ep K Ep",
    "natural":    "H K H K Sc H K H K Sm H K H K",
    # ===== 律礼 =====
    "penal":      "Sc Ds Sc Ds C Sc Ds Sc Ds G Sc Ds Sc Ds",
    "rituallaw":  "Z Sc Z Sc C Z Sc Z Sc P Z Sc Z Sc",
    "landdeed":   "Ds T Ds T Sc Ds T Ds T Sc Ds T Ds T",
    "census":     "T C T C Sc T C T C Sm T C T C",
    "censor":     "Sc ed Sc ed C Sc ed Sc ed G Sc ed Sc ed",
    "border":     "G Wb G Wb C G Wb G Wb Z G Wb G Wb",
    "clan":       "Z C Z C P Z C Z C Sc Z C Z C",
    "militarylaw":"Wl G Wl G C Wl G Wl G Sc Wl G Wl G",
    "lawsuit":    "Ds C Ds C Sc Ds C Ds C P Ds C Ds C",
    # ===== 方技玄术 =====
    "alchemy":    "H K H K Sc H K H K Sm H K H K",
    "divin":      "U:占断 Sc U:占断 Z U:占断 Sc U:占断 Z U:占断 Sc U:占断 Z U:占断 Sc U:占断",
    "fengshui":   "C P C P Sc C P C P Sm C P C P",
    "fangji":     "H K H K Sc H K H K Sm H K H K",
    "kanYu":      "Wb M Wb M G Wb M Wb M Sc Wb M Wb M",
    "talisman":   "Cu H Cu H Sc Cu H Cu H Sm Cu H Cu H",
    "fate":       "U:占验 Z U:占验 Sc U:占验 Z U:占验 Sc U:占验 Z U:占验 Sc U:占验 Z",
    "dunjia":     "Wb Cu Wb Cu G Wb Cu Wb Cu Sc Wb Cu Wb Cu",
    "witch":      "Wb Cu Wb Cu G Wb Cu Wb Cu Sm Wb Cu Wb Cu",
}


def tier_of(age):
    return 1 if age <= 3 else (2 if age <= 7 else 3)


def parse_code(code):
    """单段短码 → effect 列表（支持 '+' 复合）。U:label 为解锁。"""
    out = []
    for c in code.split("+"):
        c = c.strip()
        if not c:
            continue
        if c.startswith("U:"):
            out.append({"type": "unlock", "target": c[2:]})
        elif c in SHORTCODE:
            t, tg, pt, cap = SHORTCODE[c]
            out.append({"type": t, "target": tg, "perTier": pt, "cap": cap})
        else:
            raise ValueError("未知短码: %r" % c)
    return out


def fmt(sp, age):
    t = sp["type"]
    tg = sp.get("target", "")
    pt = sp.get("perTier", 0)
    cap = sp.get("cap", 0)
    tier = tier_of(age)
    if t == "passive":
        step = pt * tier
        return "每年正月「%s」+%.2f（每级叠加，封顶%.1f/年）" % (ATTR_CN.get(tg, tg), step, cap)
    if t in ("shield", "eventLess"):
        pct = pt * tier
        cn = CRISIS_CN.get(tg, tg)
        if t == "shield":
            return "「%s」类灾异结算损失−%d%%·每级（封顶%d%%）" % (cn, pct, cap)
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
    if t == "unlock":
        return "相关事件解锁特殊抉择：「%s」" % tg
    return ""


def main():
    if not os.path.exists(JSON_PATH):
        print("FATAL: 未找到", JSON_PATH)
        return
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
    unused = set(EFFECTS.keys())
    dup_fatal = False

    for n in nodes:
        sp = n.get("special")
        if sp is None or sp not in EFFECTS:
            missing.append(n.get("id"))
            continue
        unused.discard(sp)
        seq = EFFECTS[sp].split()
        if len(seq) < 1:
            missing.append(n.get("id") + "(空序列)")
            continue
        idx = min(max(n["age"] - 1, 0), len(seq) - 1)
        codes = seq[idx]
        try:
            eff_list = parse_code(codes)
        except ValueError as e:
            print("⚠ 解析失败 %s (%s): %s" % (n.get("id"), sp, e))
            dup_fatal = True
            missing.append(n.get("id"))
            continue
        n["effect"] = [dict(s) for s in eff_list]
        eff = "；".join(fmt(s, n["age"]) for s in eff_list)
        n["effectDesc"] = eff
        # 功能介绍优先按 (special, age) 取专属演进段，不再复用轨道统一句
        fseq = FUNC_DESC.get(sp)
        if fseq:
            fparts = fseq.split("‖")
            base = fparts[min(max(n["age"] - 1, 0), len(fparts) - 1)]
        else:
            # 兜底：保留旧逻辑（读现有 functionDesc 前半段）
            base = (n.get("functionDesc") or "").strip()
            if "｜" in base:
                base = base.split("｜", 1)[0].strip()
            if base == eff:
                base = ""
        n["functionDesc"] = (base + " ｜ " + eff) if base else eff
        n_eff += 1
        n_desc += 1

    json.dump(data, open(JSON_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("节点总数:", n_total, " | 写入 effect:", n_eff, " | 写入 effectDesc:", n_desc)
    print("EFFECTS 覆盖 special 数:", len(EFFECTS) - len(unused), "/", len(EFFECTS))

    # 差异化自检：每个 special 的 14 段，相邻 age 的 (type,target) 组合必不同（硬约束）。
    # 注意：国库/民心 的 type 同为 passive、水患/饥荒盾 同为 shield，
    # 故比较最小粒度 (type,target) 组合，而非仅顶层 type，否则会误报雷同。
    def sig(code):
        effs = parse_code(code)
        return tuple(sorted((e["type"], e.get("target")) for e in effs))

    mono = None
    for sp, s in EFFECTS.items():
        seq = s.split()
        prev = None
        for i, code in enumerate(seq):
            sg = sig(code)
            if sg == prev:
                if mono is None:
                    mono = []
                mono.append("%s@age%d(%s)" % (sp, i + 1, code))
            prev = sg
    if mono:
        print("⚠ 相邻 age 类型雷同（应消除）:", mono)
        dup_fatal = True
    else:
        print("✅ 全部 81 线 14 段相邻 age 主类型均不同，差异化达成")

    # score 残留检查
    left_score = [sp for sp in EFFECTS for code in EFFECTS[sp].split()
                  for e in parse_code(code) if e.get("type") == "score"]
    if left_score:
        print("⚠ 仍含 score 通道的 special:", sorted(set(left_score)))
        dup_fatal = True
    else:
        print("✅ 无 score（终评）通道残留")

    if unused:
        print("⚠ EFFECTS 中无对应节点的 special:", sorted(unused))
    if missing:
        print("⚠ 数据中无 effect 映射的节点:", missing[:20], "...共", len(missing))
    if dup_fatal:
        print("⚠ 存在致命问题，未回滚（备份已存），请检查后重跑。")


if __name__ == "__main__":
    main()
