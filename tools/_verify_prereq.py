import re, json, sys

raw = open("data/tech_data.js", encoding="utf-8").read()
i = raw.index("window.TECH_TREE")
j = raw.index("{", i)
depth = 0
k = j
while k < len(raw):
    c = raw[k]
    if c == "{": depth += 1
    elif c == "}":
        depth -= 1
        if depth == 0:
            break
    k += 1
tree = json.loads(raw[j:k + 1])
nodes = tree["nodes"]
byid = {n["id"]: n for n in nodes}

checks = [
    ("mil_09_05", "eng_08_05", "蒸汽舰←蒸汽机"),
    ("eng_09_08", "eng_08_05", "汽车←蒸汽机"),
    ("mil_10_08", "eng_09_08", "摩托化←汽车"),
    ("mil_10_04", "eng_09_08", "装甲骑←汽车"),
    ("eng_10_02", "eng_09_08", "高速路←汽车"),
    ("com_08_03", "eng_08_08", "轮船招商←轮船"),
    ("com_09_03", "eng_08_08", "远洋轮←轮船"),
    ("mil_08_00", "eng_08_04", "铁甲←现代冶"),
    ("mil_09_06", "eng_08_04", "速射炮←现代冶"),
    ("eng_09_03", "eng_09_05", "水电站←电动机"),
    ("com_10_08", "sci_09_07", "塑料工←现代化学"),
    ("com_13_08", "sci_10_08", "生物工←分子生物"),
    ("med_10_02", "sci_09_07", "化学药←现代化学"),
    ("mil_08_07", "sci_08_06", "电报谍←物理学"),
    ("mil_11_06", "sci_08_06", "激光武←物理学"),
]
allok = True
print("=== tech_data.js 运行期数据校验 ===")
for tid, pid, label in checks:
    n = byid.get(tid)
    has = n and pid in (n.get("prereq") or [])
    allok = allok and has
    print(("  ✅" if has else "  ❌") + " %s | %s prereq=%s" % (label, tid, n.get("prereq") if n else "节点缺失"))

WHITE, GRAY, BLACK = 0, 1, 2
color = {n["id"]: WHITE for n in nodes}
cyc = []
def dfs(u):
    color[u] = GRAY
    for v in (byid[u].get("prereq") or []):
        if v not in byid: continue
        if color[v] == GRAY: cyc.append((u, v)); return True
        if color[v] == WHITE and dfs(v): return True
    color[u] = BLACK
    return False
hc = any(color[n["id"]] == WHITE and dfs(n["id"]) for n in nodes)
print("=== 环路复检 ===")
print("  ✅ 无环路" if not hc else "  ⚠️ 有环路: " + str(cyc))
print("=== 总判定 ===")
print("  ✅ 全部 15 条前置已写入运行期数据" if (allok and not hc) else "  ❌ 存在缺失")
