#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理皇帝 events 中的历史重复 bug。

判定规则：
- 以 (title, year, month) 为分组键。
- 每组若 >1 条，视为重复事件组。
- 组内保留「最完整」的一条：
    score = (有 branches 且非空 ? 2 : 0)
          + (tier == "major" ? 1 : 0)
          + (有 gating 且非空 ? 1 : 0)
  并列时取数组中最先出现的下标（即 e3 这类带 choices/反馈跳转的完整事件优先保留）。
- 删除其余退化副本（纯拷贝、或 branches 被剥空的残本）。

仅回写发生变更的文件，最大限度缩小 diff。
"""
import json, glob, os
from collections import defaultdict

SRC = "data/emperors"

def completeness(ev):
    s = 0
    br = ev.get("branches")
    if isinstance(br, list) and len(br) > 0:
        s += 2
    if ev.get("tier") == "major":
        s += 1
    g = ev.get("gating")
    if isinstance(g, dict) and len(g) > 0:
        s += 1
    return s

def keyof(ev):
    return (ev.get("title"), ev.get("year"), ev.get("month"))

def dedup_emperor(e):
    """返回 (去重后events, 删除记录[(removed_id, kept_id)] )"""
    evs = e.get("events") or []
    groups = defaultdict(list)
    for i, ev in enumerate(evs):
        groups[keyof(ev)].append(i)
    remove_idx = set()
    removed = []  # (removed_id, kept_id)
    for k, idxs in groups.items():
        if len(idxs) <= 1:
            continue
        # 选 score 最高、并列取最早
        best = None
        for i in idxs:
            sc = completeness(evs[i])
            if best is None or sc > best[1] or (sc == best[1] and i < best[0]):
                best = (i, sc)
        keep_i = best[0]
        for i in idxs:
            if i != keep_i:
                remove_idx.add(i)
                removed.append((evs[i].get("id"), evs[keep_i].get("id")))
    if not remove_idx:
        return evs, []
    new_evs = [ev for i, ev in enumerate(evs) if i not in remove_idx]
    return new_evs, removed

def main():
    files = sorted(glob.glob(os.path.join(SRC, "*.json")))
    total_removed = 0
    changed_files = []
    report_lines = []
    for f in files:
        if "_backup_" in f:
            continue
        data = json.load(open(f, encoding="utf-8"))
        emps = data.get("emperors", [])
        file_removed = 0
        for e in emps:
            new_evs, removed = dedup_emperor(e)
            if removed:
                e["events"] = new_evs
                file_removed += len(removed)
                for rid, kid in removed:
                    report_lines.append(f"  {e.get('id')}: 删 {rid}  -> 留 {kid}")
        if file_removed > 0:
            json.dump(data, open(f, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=2)
            changed_files.append((os.path.basename(f), file_removed))
            total_removed += file_removed
    print("=== 清理报告 ===")
    print(f"共删除重复事件: {total_removed} 条")
    for fn, n in changed_files:
        print(f"  变更文件 {fn}: 删 {n} 条")
    print("\n明细:")
    for line in report_lines:
        print(line)
    print("\n无重复事件的文件未改动。")

if __name__ == "__main__":
    main()
