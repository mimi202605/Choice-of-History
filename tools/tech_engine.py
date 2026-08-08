# -*- coding: utf-8 -*-
"""
Choice of History —— 科技树计算引擎（Python 参考实现 + 演示）
与 tools/tech_engine.js 逻辑一致，便于服务端/离线校验与 AI 调试。
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

DYNASTY_ERA = {
    "夏": 1, "商": 2, "周": 2, "秦": 3,
    "汉": 4, "新": 4, "三国": 4,
    "晋": 5, "南北朝": 5, "隋": 5, "唐": 5, "五代": 5,
    # 南北朝诸朝（应属中古 era5；皇帝 dynasty 字段用具体朝名）
    "齐": 5, "梁": 5, "陈": 5, "北魏": 5, "东魏": 5, "西魏": 5, "北齐": 5, "北周": 5,
    # 五代诸朝（应属中古 era5）
    "后梁": 5, "后唐": 5, "后晋": 5, "后汉": 5, "后周": 5,
    "宋": 6, "辽": 6, "金": 6, "西夏": 6, "元": 6,
    "明": 7, "清": 8,
    "未来近": 9, "未来中": 11, "未来远": 13, "终末": 14,
}
# 子朝代 → 父朝代（汇总朝）：皇帝 dynasty 字段常写具体朝名，查不到时回退到父朝，
# 既补 era 映射、也能借到父朝初始科技树，杜绝缺映射掉到 era1（蒙昧石器时代）。
DYN_SUB_TO_PARENT = {
    "齐": "南北朝", "梁": "南北朝", "陈": "南北朝",
    "北魏": "南北朝", "东魏": "南北朝", "西魏": "南北朝", "北齐": "南北朝", "北周": "南北朝",
    "后梁": "五代", "后唐": "五代", "后晋": "五代", "后汉": "五代", "后周": "五代",
}
ATTRS = ["treasury", "people", "military", "court", "health", "tech"]
ATTR_CN = {"treasury": "国库", "people": "民心", "military": "军事", "court": "朝政", "health": "健康", "tech": "科技"}


def ahead_damp(gap):
    if gap <= 0:
        return 1.0
    return max(0.15, 1 - 0.18 * gap)


class TechEngine:
    def __init__(self, tree, presets):
        self.tree = tree
        self.presets = presets.get("dynasties", presets) if isinstance(presets, dict) else {}
        self.node_by_id = {n["id"]: n for n in tree["nodes"]}
        self.special_to_attr = tree["meta"]["specialToAttr"]
        self.ages = tree["meta"]["ages"]
        self.branches = tree["meta"]["branches"]

    def era_level_of(self, emperor):
        if emperor.get("eraLevel"):
            return emperor["eraLevel"]
        d = emperor.get("dynasty")
        k = d if d in DYNASTY_ERA else DYN_SUB_TO_PARENT.get(d, d)
        return DYNASTY_ERA.get(k, 1)

    def preset_for(self, dynasty):
        k = dynasty if dynasty in self.presets else DYN_SUB_TO_PARENT.get(dynasty, dynasty)
        p = self.presets.get(k)
        return dict(p["techs"]) if p else {}

    def compute(self, emperor, owned):
        era = self.era_level_of(emperor)
        era_name = next((a["name"] for a in self.ages if a["id"] == era), f"时代{era}")
        attr_bonus = {a: 0 for a in ATTRS}
        specials = {}
        per_branch = {}
        ahead = []
        own_count = total_levels = ahead_levels = 0

        for tid, lvl in owned.items():
            node = self.node_by_id.get(tid)
            if not node or lvl <= 0:
                continue
            own_count += 1
            total_levels += lvl
            gap = node["age"] - era
            factor = ahead_damp(gap)
            is_ahead = gap > 0
            for a, v in node["bonusPerLevel"].items():
                attr_bonus[a] += v * lvl * factor
            sattr = node.get("specialAttr") or self.special_to_attr.get(node["special"])
            if sattr:
                attr_bonus[sattr] += lvl * factor
            specials[node["special"]] = specials.get(node["special"], 0) + lvl
            b = per_branch.setdefault(node["branch"], {"name": node["branchName"], "count": 0, "levels": 0, "attrBonus": {a: 0 for a in ATTRS}})
            b["count"] += 1
            b["levels"] += lvl
            for a, v in node["bonusPerLevel"].items():
                b["attrBonus"][a] += v * lvl * factor
            if sattr:
                b["attrBonus"][sattr] += lvl * factor
            if is_ahead:
                ahead_levels += lvl
                bonus = {}
                for a, v in node["bonusPerLevel"].items():
                    bonus[a] = round(v * lvl * factor)
                if sattr:
                    bonus[sattr] = bonus.get(sattr, 0) + round(lvl * factor)
                ahead.append({
                    "id": tid, "name": node["name"], "branch": node["branchName"], "track": node["track"],
                    "age": node["age"], "ageName": node["ageName"], "gap": gap, "level": lvl,
                    "factor": round(factor, 2), "bonus": bonus, "desc": node["desc"],
                })

        attr_bonus_r = {a: round(attr_bonus[a]) for a in ATTRS}
        ahead.sort(key=lambda x: (-x["gap"], -x["level"]))
        ahead_attr = {a: 0 for a in ATTRS}
        for t in ahead:
            for a, v in t["bonus"].items():
                ahead_attr[a] += v
        ahead_attr = {a: round(v) for a, v in ahead_attr.items()}
        for b in per_branch.values():
            b["attrBonus"] = {a: round(v) for a, v in b["attrBonus"].items()}

        return {
            "emperor": emperor.get("dynasty", "?"), "eraLevel": era, "eraName": era_name,
            "totalTechsOwned": own_count, "totalLevels": total_levels,
            "attrBonus": attr_bonus_r, "specials": specials, "perBranch": per_branch,
            "ahead": {"count": len(ahead), "levels": ahead_levels,
                      "maxGap": ahead[0]["gap"] if ahead else 0, "attrBonus": ahead_attr, "techs": ahead},
            "aiSummary": self._ai_summary(emperor, era, era_name, attr_bonus_r, ahead_attr, ahead, own_count, total_levels),
        }

    def _ai_summary(self, emperor, era, era_name, attr_bonus, ahead_attr, ahead, own, levels):
        top = [f"{ATTR_CN[a]}+{attr_bonus[a]}" for a in ATTRS if attr_bonus[a] != 0]
        top.sort(key=lambda x: -int(x.split("+")[1]))
        s = f"【科技档案】{emperor.get('dynasty','皇帝')}身处「{era_name}」(时代等级{era})，"
        s += f"已拥科技 {own} 项、累计 {levels} 级；六维增益：{('、'.join(top)) or '无'}。"
        if ahead:
            s += f"其越代科技 {len(ahead)} 项，最高跨越 {ahead[0]['gap']} 个时代："
            s += "；".join(f"{t['name']}({t['branch']}·{t['ageName']}，领先{t['gap']}代，lv{t['level']}，落地效率{round(t['factor']*100)}%)" for t in ahead[:8]) + "。"
            real = {a: v for a, v in ahead_attr.items() if v != 0}
            if real:
                gain_txt = "、".join(f"{ATTR_CN[a]}+{v}" for a, v in real.items())
                s += f"越代科技虽因时代基础薄弱而衰减，仍实质提升其{'、'.join(ATTR_CN[a] for a in real)}（{gain_txt}），"
                s += "应被视为「穿越者之能」：朝臣或以「奇技淫巧」非之，然其带来之国力与变局不可小觑。"
            else:
                s += "然因时代鸿沟过巨，越代科技之增益近乎为零，仅余「名」而无「实」，史官当记其「好异梦而远人事」。"
        else:
            s += "暂无超越当世的科技，科技树与时代相称。"
        return s


def main():
    tree = json.load(open(os.path.join(DATA, "tech_tree.json"), encoding="utf-8"))
    presets = json.load(open(os.path.join(DATA, "tech_presets.json"), encoding="utf-8"))
    eng = TechEngine(tree, presets)

    print("=" * 70)
    print("演示 A：秦始皇（时代3）—— 仅用时代预设")
    print("=" * 70)
    owned = eng.preset_for("秦")
    p = eng.compute({"dynasty": "秦"}, owned)
    print("预置科技数:", p["totalTechsOwned"], "| 时代:", p["eraName"])
    print("六维增益:", p["attrBonus"])
    print("超前科技:", p["ahead"]["count"])
    print("AI摘要:", p["aiSummary"][:160], "...")

    print("\n" + "=" * 70)
    print("演示 B：秦始皇 + 玩家用科技点数点出多项「超前科技」（穿越者）")
    print("=" * 70)
    # 额外解锁：信息时代(11)的精准农业、智能单兵；星际(14)的奇点甲、恒星农业
    extra = {"agri_11_00": 3, "mil_11_00": 3, "mil_14_00": 2, "agri_14_00": 2, "sci_12_01": 1}
    owned2 = dict(owned); owned2.update(extra)
    p2 = eng.compute({"dynasty": "秦"}, owned2)
    print("总科技数:", p2["totalTechsOwned"], "| 累计等级:", p2["totalLevels"])
    print("六维增益:", p2["attrBonus"])
    print("超前科技数:", p2["ahead"]["count"], "| 最高领先:", p2["ahead"]["maxGap"], "代")
    print("超前科技贡献:", p2["ahead"]["attrBonus"])
    print("\n--- 越代科技清单（供 AI 读取）---")
    for t in p2["ahead"]["techs"]:
        print(f"  {t['name']}｜{t['branch']}/{t['track']}｜{t['ageName']}｜领先{t['gap']}代｜lv{t['level']}｜效率{t['factor']}｜+{t['bonus']}")
    print("\n--- AI 可读档案 ---")
    print(p2["aiSummary"])

    print("\n" + "=" * 70)
    print("演示 C：康熙（清，时代8）—— 满预设 + 洋务/近代科技")
    print("=" * 70)
    owned3 = eng.preset_for("清")
    owned3.update({"eng_09_02": 2, "com_10_08": 1, "sci_11_02": 1})
    p3 = eng.compute({"dynasty": "清"}, owned3)
    print("六维增益:", p3["attrBonus"], "| 超前:", p3["ahead"]["count"])
    print("AI摘要:", p3["aiSummary"])


if __name__ == "__main__":
    main()
