# -*- coding: utf-8 -*-
"""
enrich_data.py —— 为 data/emperors/0*.json 的内置皇帝增量注入体验优化所需字段。

注入内容（均为可选字段，缺失时才写，幂等可重跑，绝不破坏既有结构）：
  - emperor.initRelations       : 阵营好感度初值（影响 2.1/2.4 连锁与多结局）
  - emperor.historicalAnchors   : 史材锚点（1.1 参数化抽取，供 AI 月约束真实史实）
  - emperor.midCrisisAnchors    : 中段定时炸弹（5.2 加压）
  - emperor.materialTarget      : 期望硬触史事件数下限（信息字段）
  - event.tier / gating         : 大事件分级与状态门控（1.2/2.2）
  - event.branches              : 各选项旗标分支（setFlags/clearFlags/nextEventId），按索引对齐 choices
  - event.relationDeltas        : 各选项关系增量，按索引对齐 choices
  - 中段大事件的 follow-up 余波事件（演示 nextEventId 连锁）

用法：python3 tools/enrich_data.py
"""
import json, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMP_DIR = os.path.join(ROOT, "data", "emperors")
FILES = sorted(glob.glob(os.path.join(EMP_DIR, "0*.json")))

# ---- 立场推断（对齐 index.html 的 hintFromText 顺序）----
STANCE_RULES = [
    (re.compile(r"北伐|亲征|讨|伐|征|战|出击|出兵|进攻|主动|攘|拓土|平[定寇]|剿|大举|示威"), "进取"),
    (re.compile(r"守|稳|缓|待|按兵|不战|固守|持重|徐图|姑息|养|罢|减役|息民|不轻"), "保守"),
    (re.compile(r"改|废|创|兴[学宫]|科举|新法|变革|革新|行.*制|劝农|办学|均输|变法|更铸|整饬|设"), "革新"),
    (re.compile(r"和|抚|赦|赈|蠲|免|招降|和亲|安抚|宽|赈济|平粜|怀柔|厚赐|通商|薄赋|罢弊政|罪己"), "怀柔"),
    (re.compile(r"诛|杀|废黜|黜|严|镇压|铁腕|惩治|禁|族|严厉打击|籍没|易帅|严捕|骤夺"), "铁腕"),
]
def stance_of(text):
    t = text or ""
    for rx, s in STANCE_RULES:
        if rx.search(t):
            return s
    return None

# ---- 立场 → 关系增量（键须与 initRelations 一致）----
STANCE_REL = {
    "进取": {"边将": 3, "士大夫": -2},
    "保守": {"宗室": 2, "士大夫": 2},
    "革新": {"士大夫": -3, "商贾": 1},
    "怀柔": {"士大夫": 1, "商贾": 2},
    "铁腕": {"士大夫": -4, "边将": 2},
}

# ---- 大事件判定关键词（标题）----
MAJOR_KW = ["之战", "之变", "之祸", "之狱", "篡", "改革", "变法", "迁都", "亡",
            "即位", "称帝", "称王", "称制", "禅让", "新政", "之乱", "起义",
            "兵变", "之叛", "灭", "夺门", "靖难", "朋党", "党争"]

FOLLOWUP_CHOICES = [
    "乘势固本，安内攘外以定人心",
    "稍事休养，与民休息，徐图后效",
    "整肃朝纲，明赏罚以肃百僚",
    "广开言路，纳忠谏以通下情",
    "严刑峻法，震慑不轨以靖四方",
]
CRISIS_CHOICES = [
    "厉精图治，躬亲庶务以挽颓势",
    "赦宥罪戾，蠲免租赋以安民心",
    "整军经武，以备不虞之患",
    "崇儒重道，收士大夫之望",
    "稍事因循，徐观其变",
]

def default_relations(dynasty):
    r = {"宗室": 50, "士大夫": 40, "边将": 30, "商贾": 10}
    if dynasty in ("汉", "唐"):
        r["士大夫"] = 45; r["边将"] = 40
    elif dynasty in ("宋",):
        r["士大夫"] = 45; r["边将"] = 25; r["商贾"] = 20
    elif dynasty in ("明",):
        r["士大夫"] = 45; r["宗室"] = 55; r["边将"] = 35
    elif dynasty in ("元", "清"):
        r["宗室"] = 60; r["士大夫"] = 35; r["边将"] = 30
    elif dynasty in ("秦", "隋"):
        r["士大夫"] = 40; r["边将"] = 35
    return r

def enrich_emperor(emp):
    changed = False
    emp_id = emp.get("id") or (emp.get("dynasty", "") + "_" + emp.get("name", ""))
    reign_start = emp.get("reignStart")
    reign_end = emp.get("reignEnd")
    span = max(1, (reign_end or reign_start or 1) - (reign_start or 0) + 1)

    # initRelations
    if "initRelations" not in emp:
        emp["initRelations"] = default_relations(emp.get("dynasty", ""))
        changed = True

    # materialTarget
    if "materialTarget" not in emp:
        emp["materialTarget"] = max(6, (span + 2) // 3)
        changed = True

    events = emp.get("events") or []
    # 为所有事件补 id（统一，便于门控/分支/去重）
    for i, ev in enumerate(events):
        if not ev.get("id"):
            ev["id"] = "%s_e%d" % (emp_id, i)
            changed = True

    # 计算各选项立场 + 关系增量
    for i, ev in enumerate(events):
        choices = ev.get("choices") or []
        if len(choices) != 5:
            continue  # 仅对标准 5 选项事件注入分支/关系，保证索引对齐
        # relationDeltas
        if "relationDeltas" not in ev:
            rds = []
            for c in choices:
                s = stance_of(c)
                rds.append(dict(STANCE_REL.get(s)) if s else {})
            ev["relationDeltas"] = rds
            changed = True

    # 标注大事件 tier/gating/branches
    majors = []
    for i, ev in enumerate(events):
        if ev.get("tier") in ("major",) :
            # 幂等校正：若选项数非 5，旧分支长度可能错位，重置为 None 保证对齐
            if len(ev.get("choices") or []) != 5:
                ev["branches"] = None
            majors.append(i); continue
        if "tier" in ev and ev.get("tier") != "daily":
            continue
        title = ev.get("title", "") or ""
        mid_year = reign_start + span // 2
        near_mid = abs((ev.get("year") or reign_start) - mid_year) <= max(2, span // 12)
        is_major = any(k in title for k in MAJOR_KW) or near_mid
        if is_major:
            ev["tier"] = "major"
            ev["gating"] = {}
            # 分支：每个选项置独立旗标；首选项可串联余波（仅对标准 5 选项事件注入，保证索引对齐）
            if len(ev.get("choices") or []) == 5:
                ev["branches"] = [
                    {"setFlags": ["did_%s_%d" % (ev["id"], j)],
                     "clearFlags": [], "nextEventId": None}
                    for j in range(5)
                ]
            else:
                ev["branches"] = None
            majors.append(i)
            changed = True

    # 限制大事件数量（避免过载）
    cap = max(2, min(5, (span + 17) // 18))
    if len(majors) > cap:
        # 保留最靠近中点的 cap 个
        mid_year = reign_start + span // 2
        majors.sort(key=lambda i: abs((events[i].get("year") or reign_start) - mid_year))
        keep = set(majors[:cap])
        for i in majors[cap:]:
            events[i].pop("tier", None)
            events[i].pop("gating", None)
            events[i].pop("branches", None)
            # relationDeltas 保留（关系始终演化）
        majors = majors[:cap]
        changed = True

    # 中段大事件 → follow-up 余波（演示 nextEventId 连锁）
    if majors:
        mid_year = reign_start + span // 2
        mi = min(majors, key=lambda i: abs((events[i].get("year") or reign_start) - mid_year))
        parent = events[mi]
        if parent.get("branches"):
            fb_id = parent["id"] + "_fb"
            # 避免重复添加
            if not any(e.get("id") == fb_id for e in events):
                fb = {
                    "id": fb_id,
                    "year": None,
                    "month": None,
                    "title": (parent.get("title", "") + "·余波"),
                    "description": "「%s」之余波未平，朝野观望，陛下需善其后，以定人心。" % parent.get("title", ""),
                    "choices": list(FOLLOWUP_CHOICES),
                    "historicalChoice": -1,
                    "historicalOutcome": "",
                    "tier": "major",
                    "gating": {"requiresFlags": ["did_%s_0" % parent["id"]]},
                    "relationDeltas": [dict(STANCE_REL.get(stance_of(c)) or {}) for c in FOLLOWUP_CHOICES],
                    "isFollowup": True,
                }
                events.append(fb)
                changed = True
            # 父事件首选项串联余波
            if parent["branches"][0].get("nextEventId") is None:
                parent["branches"][0]["nextEventId"] = fb_id
                changed = True

    # historicalAnchors（1.1）
    if "historicalAnchors" not in emp:
        anchors = []
        # 来自既有事件
        for i, ev in enumerate(events):
            if ev.get("isFollowup"):
                continue
            y = ev.get("year")
            if y is None:
                continue
            anchors.append({
                "id": "%s_anc%d" % (emp_id, i),
                "year": y,
                "month": ev.get("month"),
                "topic": ev.get("title", ""),
                "figures": [],
                "keywords": [],
                "premise": (ev.get("description") or ev.get("title") or "")[:60],
                "weight": 2,
            })
        # 来自背景段落
        bg = emp.get("background") or ""
        sents = [s for s in re.split(r"[。！？]", bg) if len(s) >= 24]
        n = min(2, len(sents))
        for k in range(n):
            frac = (k + 1) / (n + 1)
            y = reign_start + int(span * frac)
            anchors.append({
                "id": "%s_bg%d" % (emp_id, k),
                "year": y,
                "month": None,
                "topic": "背景·" + sents[k][:10],
                "figures": [],
                "keywords": [],
                "premise": sents[k][:60],
                "weight": 1,
            })
        emp["historicalAnchors"] = anchors
        changed = True

    # midCrisisAnchors（5.2）
    if "midCrisisAnchors" not in emp and reign_start and reign_end:
        emp["midCrisisAnchors"] = [{
            "atProgress": 0.5,
            "event": {
                "title": (emp.get("name", "") + "中年之厄"),
                "description": "%s中叶，%s御宇既久，积弊渐生，或水旱，或兵戈，或党论，朝野多有异辞，陛下需定夺。" % (emp.get("era", ""), emp.get("name", "")),
                "choices": list(CRISIS_CHOICES),
                "historicalChoice": -1,
            }
        }]
        changed = True

    return changed

def main():
    total_changed = 0
    total_emps = 0
    total_events = 0
    total_majors = 0
    total_followups = 0
    total_anchors = 0
    for f in FILES:
        data = json.load(open(f, "r", encoding="utf-8"))
        emps = data.get("emperors") or []
        file_changed = False
        for emp in emps:
            total_emps += 1
            total_events += len(emp.get("events") or [])
            if enrich_emperor(emp):
                file_changed = True
                total_changed += 1
            total_majors += sum(1 for e in emp.get("events", []) if e.get("tier") == "major")
            total_followups += sum(1 for e in emp.get("events", []) if e.get("isFollowup"))
            total_anchors += len(emp.get("historicalAnchors") or [])
        if file_changed:
            json.dump(data, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            print("已更新:", os.path.basename(f))
    print("皇帝:", total_emps, " 事件:", total_events,
          " 大事件:", total_majors, " 余波:", total_followups,
          " 锚点:", total_anchors, " 变更皇帝:", total_changed)

if __name__ == "__main__":
    main()
