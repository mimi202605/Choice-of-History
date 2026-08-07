import json, glob
for f in ["data/emperors/01-xia-shang-zhou-qin.json","data/emperors/03-jin-nanbeichao-sui.json","data/emperors/04-tang-wudai.json","data/emperors/05-song-liao-jin-xixia.json"]:
    d=json.load(open(f,encoding="utf-8"))
    print("\n#####", f.split("/")[-1])
    for e in d["emperors"]:
        bg=len(e.get("background","")); ec=bool(e.get("eraContext","").strip()); nev=len(e.get("events",[]))
        flag = bg<40 or (not ec) or nev<3
        if flag:
            print(f"  {e['name']} | dynasty={e['dynasty']} | reign={e['reignStart']}-{e['reignEnd']} | bg={bg} era={ec} ev={nev}")
            print(f"      bg: {e.get('background','')[:60]}")
