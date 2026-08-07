import json, glob, re
files = sorted(glob.glob("data/emperors/*.json"))
canon = {"id","dynasty","name","templeName","reignStart","reignEnd","evaluation","background","initStats","eraContext","tier","events"}
stat = {"treasury","people","military","court","health","tech"}
evf = {"year","month","title","description","historicalChoice","choices","historicalOutcome"}
ph = re.compile(r"(史料稀缺|多出传说|占位|TODO|TBD|待补|暂无|待定)")
allids={}; problems=[]; total_ev=0; minbg=999; minera=999
for f in files:
    d=json.load(open(f,encoding="utf-8"))
    for e in d["emperors"]:
        n=e.get("name","?"); i=e.get("id")
        if i in allids: problems.append((f,n,"DUP id "+i)); 
        else: allids[i]=f
        bg=len(e.get("background","").strip()); minbg=min(minbg,bg)
        if bg<80: problems.append((f,n,"bg<80 "+str(bg)))
        ec=len(e.get("eraContext","").strip()); minera=min(minera,ec)
        if ec<50: problems.append((f,n,"era<50 "+str(ec)))
        if ph.search(e.get("background","")+e.get("eraContext","")): problems.append((f,n,"PLACEHOLDER"))
        for s in stat:
            v=e.get("initStats",{}).get(s)
            if not isinstance(v,(int,float)) or not(0<=v<=100): problems.append((f,n,"stat "+s))
        for ev in e.get("events",[]):
            total_ev+=1
            for k in evf:
                if k not in ev: problems.append((f,n,"evmiss "+k))
            ch=ev.get("choices",[])
            if not isinstance(ch,list) or len(ch)<4 or len(ch)>6: problems.append((f,n,"chlen "+str(len(ch))))
            hc=ev.get("historicalChoice",0)
            if not isinstance(hc,int) or hc<0 or hc>=len(ch): problems.append((f,n,"badhc"))
        for k in e.keys():
            if k not in canon: problems.append((f,n,"EXTRA "+k))
print("Files:",len(files),"Emperors:",len(allids),"Events:",total_ev)
print("min bg:",minbg,"min era:",minera)
# dynasty coverage
from collections import Counter
dyn=Counter()
for f in files:
    d=json.load(open(f,encoding="utf-8"))
    for e in d["emperors"]: dyn[e["dynasty"]]+=1
print("Dynasties:",dict(dyn))
print("PROBLEMS:",len(problems))
for p in problems[:50]: print("  ",p)
