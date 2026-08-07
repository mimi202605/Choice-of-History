import json
with open("data/emperors/04-tang-wudai.json", encoding="utf-8") as fh:
    data = json.load(fh)
# find emperor with most events
best = max(data["emperors"], key=lambda e: len(e.get("events",[])))
print("NAME:", best["name"])
print(json.dumps(best, ensure_ascii=False, indent=2)[:3500])
print("\n=== ALL FIELD KEYS across all emperors in all files ===")
keys=set()
import glob
for f in glob.glob("data/emperors/*.json"):
    d=json.load(open(f,encoding="utf-8"))
    for e in d["emperors"]:
        keys.update(e.keys())
print(sorted(keys))
# event sub-field keys
evkeys=set()
for f in glob.glob("data/emperors/*.json"):
    d=json.load(open(f,encoding="utf-8"))
    for e in d["emperors"]:
        for ev in e.get("events",[]):
            evkeys.update(ev.keys())
print("EVENT SUBKEYS:", sorted(evkeys))
