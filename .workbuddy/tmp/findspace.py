import json, glob
for f in glob.glob("data/emperors/*.json"):
    d=json.load(open(f,encoding="utf-8"))
    for e in d["emperors"]:
        for k in e.keys():
            if k.strip()!=k:
                print(f"{f.split('/')[-1]}: emperor '{e.get('name')}' has key {k!r}")
