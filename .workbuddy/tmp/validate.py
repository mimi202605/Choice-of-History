import json, glob, re
files = sorted(glob.glob("data/emperors/*.json"))
canon = {"id","dynasty","name","templeName","reignStart","reignEnd","evaluation","background","initStats","eraContext","tier","events"}
stat = {"treasury","people","military","court","health","tech"}
evf = {"year","month","title","description","historicalChoice","choices","historicalOutcome"}
placeholder_re = re.compile(r"(史料稀缺|多出传说|占位|TODO|TBD|待补|未知|待定|暂无|略)")
allids={}
problems=[]
total_ev=0
for f in files:
    d=json.load(open(f,encoding="utf-8"))
    for e in d["emperors"]:
        n=e.get("name","?")
        # fields
        for k in canon:
            if k not in e: problems.append((f,n,"missing field "+k))
        # id uniqueness
        i=e.get("id")
        if i in allids: problems.append((f,n,"DUP id "+i+" in "+allids[i]))
        else: allids[i]=f
        # background/era
        if len(e.get("background","").strip())<60: problems.append((f,n,"bg short "+str(len(e.get("background","")))))
        if not e.get("eraContext","").strip(): problems.append((f,n,"era empty"))
        if placeholder_re.search(e.get("background","")+e.get("eraContext","")): problems.append((f,n,"PLACEHOLDER in text"))
        # initStats
        for s in stat:
            v=e.get("initStats",{}).get(s)
            if not isinstance(v,(int,float)) or not (0<=v<=100): problems.append((f,n,"bad stat "+s))
        # events
        for ev in e.get("events",[]):
            total_ev+=1
            for k in evf:
                if k not in ev: problems.append((f,n,"ev missing "+k))
            ch=ev.get("choices",[])
            if not isinstance(ch,list) or len(ch)<4 or len(ch)>6: problems.append((f,n,"choices len "+str(len(ch))))
            if not isinstance(ev.get("historicalOutcome",""),str) or not ev["historicalOutcome"].strip(): problems.append((f,n,"empty outcome"))
            # historicalChoice valid index
            hc=ev.get("historicalChoice",0)
            if not isinstance(hc,int) or hc<0 or hc>=len(ch): problems.append((f,n,"bad hc "+str(hc)))
        # extra keys (warn, not fatal)
        for k in e.keys():
            if k not in canon: problems.append((f,n,"EXTRA key "+k))

print("Files:",len(files),"Total emperors:",len(allids),"Total events:",total_ev)
print("PROBLEMS:",len(problems))
for p in problems[:60]:
    print("  ",p)
