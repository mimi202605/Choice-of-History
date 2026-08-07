# 外国篇（us/uk/rome/ru）增补事件注入器
# 读取 tools/fe_*.py 的 NEW_EVENTS，按皇帝 id 注入对应 JSON，
# 解析描述中的真实年份并在 [reignStart,reignEnd] 内分配唯一可达年份，
# 若区间内无空位（极短在位/既有事件占满）则跳过该事件，避免产生不可达冲突。
# 随后由 build_data.js 重建 coh_data.js。
import sys, re, json, importlib.util

ROOT = "."
MAP = [
    ("data/emperors/09-us.json",   "tools/fe_us.py"),
    ("data/emperors/10-uk.json",   "tools/fe_uk.py"),
    ("data/emperors/11-rome.json", "tools/fe_rome.py"),
    ("data/emperors/12-ru.json",   "tools/fe_ru.py"),
]

YEAR_RE = re.compile(r"(前)?(\d+)年")

def load_fe(path):
    spec = importlib.util.spec_from_file_location("_fe", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.NEW_EVENTS

def parse_year(desc):
    m = YEAR_RE.search(desc)
    if not m:
        return None
    y = int(m.group(2))
    if m.group(1) == "前":
        y = -y
    return y

def to_int(v):
    if isinstance(v, str):
        v = v.strip()
        if v.startswith("前"):
            return -int(v[1:])
        return int(v)
    return int(v)

def assign_year(real_year, start, end, used):
    """在 [start,end] 内找未使用的年份，优先 real_year，否则就近向外搜索。
    若区间内无空位，返回 (None, True) 表示应跳过该事件。"""
    if real_year is not None and start <= real_year <= end and real_year not in used:
        return real_year, False
    if real_year is None:
        cand = list(range(start, end + 1))
    else:
        ry = max(start, min(end, real_year))
        order = [ry]
        step = 1
        while True:
            a = ry - step
            b = ry + step
            if a >= start:
                order.append(a)
            if b <= end:
                order.append(b)
            step += 1
            if a < start and b > end:
                break
        cand = order
    for y in cand:
        if start <= y <= end and y not in used:
            return y, (y != real_year)
    return None, True

def build_event(eid, idx, t):
    title, desc, hidx, choices, rds, flags = t
    branches = [({"setFlags": f} if f else {}) for f in flags]
    if "，" in desc:
        outcome = desc.split("，", 1)[1].rstrip("。")
    else:
        outcome = desc
    return {
        "year": None,  # 由调用方在分配年份后填
        "month": None,
        "title": title,
        "description": desc,
        "historicalChoice": hidx,
        "choices": list(choices),
        "historicalOutcome": outcome,
        "id": f"{eid}_fe{idx}",
        "relationDeltas": [dict(d) for d in rds],
        "branches": branches,
    }

def main():
    report = []
    for jpath, fepath in MAP:
        data = json.load(open(jpath, encoding="utf-8"))
        ne = load_fe(fepath)
        before_total = sum(len(e.get("events", [])) for e in data["emperors"])
        added = 0
        skipped = 0
        covered = 0
        warns = []
        for e in data["emperors"]:
            eid = e.get("id")
            if eid not in ne:
                continue
            covered += 1
            start = to_int(e.get("reignStart"))
            end = to_int(e.get("reignEnd"))
            used = set()
            for ev in e.get("events", []):
                y = ev.get("year")
                if isinstance(y, int):
                    used.add(y)
            for idx, t in enumerate(ne[eid]):
                real_year = parse_year(t[1])
                year, collided = assign_year(real_year, start, end, used)
                if year is None:
                    skipped += 1
                    warns.append(f"{eid}_fe{idx}: 跳过(区间内无空位, real={real_year}, 区间 {start}-{end})")
                    continue
                ev = build_event(eid, idx, t)
                ev["year"] = year
                used.add(year)
                if collided:
                    warns.append(f"{eid}_fe{idx}: 年份 {year} 偏离真实年 {real_year} (区间 {start}-{end})")
                e["events"].append(ev)
                added += 1
            e["events"].sort(key=lambda x: (x.get("year") if isinstance(x.get("year"), int) else 10**9))
        after_total = sum(len(e.get("events", [])) for e in data["emperors"])
        # 幂等保护：仅当确实新增了事件才写回
        if added > 0:
            json.dump(data, open(jpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        report.append((jpath, covered, before_total, after_total, added, skipped, warns))
    print("=== 注入报告 ===")
    for jpath, covered, before, after, added, skipped, warns in report:
        print(f"{jpath}: 覆盖皇帝={covered} 事件 {before} -> {after} (新增 {added}, 跳过 {skipped})")
        for w in warns[:50]:
            print("    ⚠", w)
        if not warns:
            print("    无年份冲突/越界")

if __name__ == "__main__":
    main()
