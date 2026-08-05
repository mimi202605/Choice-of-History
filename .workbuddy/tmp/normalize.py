# -*- coding: utf-8 -*-
import json, glob, os
from datetime import datetime

files = sorted(glob.glob("data/emperors/*.json"))
req_fields = ["id","dynasty","name","templeName","reignStart","reignEnd",
              "evaluation","background","initStats","eraContext","tier","events"]
stat_fields = ["treasury","people","military","court","health","tech"]
event_fields = ["year","month","title","description","historicalChoice","choices","historicalOutcome"]

def norm_event(ev):
    for f in event_fields:
        if f not in ev:
            if f in ("year","month","historicalChoice"):
                ev[f] = None if f in ("year","month") else 0
            elif f == "choices":
                ev[f] = []
            else:
                ev[f] = ""
    # ensure 4-5 choices
    if len(ev["choices"]) < 4:
        ev["choices"] = (ev["choices"] + ["徐图之，待时而后动","大赦天下，与民休息","分权大臣，各司其职","遣使四方，通好息兵"])[:5]
    return ev

total_emps = 0
for f in files:
    d = json.load(open(f, encoding="utf-8"))
    # normalize top-level whitespace keys
    for k in list(d.keys()):
        if k != k.strip():
            d[k.strip()] = d.pop(k)
    emps = d["emperors"]
    fixed_keys = 0
    for e in emps:
        # normalize emperor-level whitespace keys
        for k in list(e.keys()):
            if k != k.strip():
                e[k.strip()] = e.pop(k); fixed_keys += 1
        for rf in req_fields:
            if rf not in e:
                e[rf] = "" if rf in ("evaluation","background","eraContext","tier","templeName") else ("" if rf in ("id","dynasty","name") else [])
        # initStats
        if not isinstance(e.get("initStats"), dict):
            e["initStats"] = {}
        for sf in stat_fields:
            if sf not in e["initStats"] or not isinstance(e["initStats"][sf], (int,float)):
                e["initStats"][sf] = 50
        # events
        e["events"] = [norm_event(ev) for ev in e.get("events", [])]
        if not e["tier"]:
            e["tier"] = "B"
    d["_meta"] = {
        "schemaVersion": 2,
        "group": d.get("group",""),
        "generatedAt": datetime.now().strftime("%Y-%m-%d"),
        "emperorCount": len(emps)
    }
    json.dump(d, open(f,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    total_emps += len(emps)
    print(f"{os.path.basename(f)}: emperors={len(emps)} fixed_keys={fixed_keys} meta added")
print("TOTAL emperors across files:", total_emps)
