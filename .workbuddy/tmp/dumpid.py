import json
for f in ["data/emperors/01-xia-shang-zhou-qin.json","data/emperors/03-jin-nanbeichao-sui.json","data/emperors/04-tang-wudai.json","data/emperors/05-song-liao-jin-xixia.json"]:
    d=json.load(open(f,encoding="utf-8"))
    names=set()
    print("\n#####", f.split("/")[-1])
    for e in d["emperors"]:
        bg=len(e.get("background","")); ec=bool(e.get("eraContext","").strip()); nev=len(e.get("events",[]))
        if bg<40 or (not ec) or nev<3:
            print(f"  {e['name']} | id={e['id']} | bg={bg} era={ec} ev={nev}")
