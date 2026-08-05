import json, glob, re
placeholder_re = re.compile(r"(史料稀缺|多出传说|占位|TODO|TBD|待补|待定|暂无)")
for f in ["01-xia-shang-zhou-qin.json","03-jin-nanbeichao-sui.json","04-tang-wudai.json","05-song-liao-jin-xixia.json"]:
    d=json.load(open("data/emperors/"+f,encoding="utf-8"))
    need=[]
    for e in d["emperors"]:
        bg=e.get("background",""); ec=e.get("eraContext",""); nev=len(e.get("events",[]))
        if len(bg.strip())<80 or placeholder_re.search(bg+ec) or len(ec.strip())<40 or nev<4 or placeholder_re.search(ec):
            need.append(e["name"])
    print(f"\n{f}: {len(need)} need enrichment")
    print("  ", " ".join(need))
