import json, sys

p = "data/tech_tree.json"
d = json.load(open(p, encoding="utf-8"))
byid = {n["id"]: n for n in d["nodes"]}

# (目标id, 前置id, 说明) — 15 处跨分支/底层技术缺失前置
adds = [
    ("mil_09_05", "eng_08_05", "蒸汽舰←蒸汽机(跨分支)"),
    ("eng_09_08", "eng_08_05", "汽车←蒸汽机(跨分支)"),
    ("mil_10_08", "eng_09_08", "摩托化←汽车(跨分支)"),
    ("mil_10_04", "eng_09_08", "装甲骑←汽车(跨分支)"),
    ("eng_10_02", "eng_09_08", "高速路←汽车(跨分支)"),
    ("com_08_03", "eng_08_08", "轮船招商←轮船(跨分支)"),
    ("com_09_03", "eng_08_08", "远洋轮←轮船(跨分支)"),
    ("mil_08_00", "eng_08_04", "铁甲←现代冶(跨分支)"),
    ("mil_09_06", "eng_08_04", "速射炮←现代冶(跨分支)"),
    ("eng_09_03", "eng_09_05", "水电站←电动机(跨分支)"),
    ("com_10_08", "sci_09_07", "塑料工←现代化学(跨分支)"),
    ("com_13_08", "sci_10_08", "生物工←分子生物(跨分支)"),
    ("med_10_02", "sci_09_07", "化学药←现代化学(跨分支)"),
    ("mil_08_07", "sci_08_06", "电报谍←物理学(跨分支)"),
    ("mil_11_06", "sci_08_06", "激光武←物理学(跨分支)"),
]

ok, bad, skip = [], [], []
for tid, pid, label in adds:
    t = byid.get(tid); pr = byid.get(pid)
    if not t: bad.append((label, "目标不存在 " + tid)); continue
    if not pr: bad.append((label, "前置不存在 " + pid)); continue
    if pr["age"] > t["age"]: bad.append((label, "前置age%d>目标age%d" % (pr["age"], t["age"]))); continue
    pre = t.setdefault("prereq", [])
    if pid in pre: skip.append((label, "已存在跳过")); continue
    pre.append(pid); ok.append((label, "已追加 %s(%s,age%d)" % (pid, pr["name"], pr["age"])))

# 环路检测 (DFS)
sys.setrecursionlimit(10000)
WHITE, GRAY, BLACK = 0, 1, 2
color = {n["id"]: WHITE for n in d["nodes"]}
cycle = []
def dfs(u):
    color[u] = GRAY
    for v in byid[u].get("prereq", []):
        if v not in byid: continue
        if color[v] == GRAY: cycle.append((u, v)); return True
        if color[v] == WHITE and dfs(v): return True
    color[u] = BLACK
    return False
has_cycle = False
for n in d["nodes"]:
    if color[n["id"]] == WHITE and dfs(n["id"]):
        has_cycle = True; break

if has_cycle:
    print("⚠️ 检测到依赖环路:", cycle)
    print("已中止写入，请检查。")
    sys.exit(1)

json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("=== 成功追加 ===")
for o in ok: print("  ✅", o)
print("=== 已存在跳过 ===")
for s in skip: print("  ➖", s)
print("=== 异常 ===")
for b in bad: print("  ⚠️", b)
print("=== 环路检测 ===")
print("  ✅ 无环路" if not has_cycle else "  ⚠️ 有环路")
print("=== 改后相关节点 prereq ===")
for tid, pid, label in adds:
    n = byid[tid]
    print("  %s %s prereq=%s" % (tid, n["name"], n.get("prereq")))
