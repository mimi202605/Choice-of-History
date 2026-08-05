import json, glob
# DYNASTIES ids present in index.html after edit
dyn_ids={"xia","shang","zhou","qin","han","xin","three","jin","nanbei","sui","tang","wudai","song","liao","jin2","xixia","yuan","ming","qing"}
# map (as updated)
map={"夏":"xia","商":"shang","周":"zhou","秦":"qin","汉":"han","新":"xin","三国":"three","晋":"jin",
"齐":"nanbei","梁":"nanbei","陈":"nanbei","北魏":"nanbei","东魏":"nanbei","西魏":"nanbei","北齐":"nanbei","北周":"nanbei","南北朝":"nanbei",
"隋":"sui","唐":"tang",
"后梁":"wudai","后唐":"wudai","后晋":"wudai","后汉":"wudai","后周":"wudai","五代十国":"wudai",
"宋":"song","辽":"liao","金":"jin2","西夏":"xixia","元":"yuan","明":"ming","清":"qing"}
# hardcoded ids in index.html
hardcoded={"han_gaozu","han_wudi","han_guangwu","yuan_shizu","ming_taizu","ming_chengzu","ming_sizong","qing_kangxi","qing_yongzong","qing_qianlong"}
allids=set(hardcoded); orphan=[]; unmapped=[]; dup=[]; json_ids=set()
for f in sorted(glob.glob("data/emperors/*.json")):
    d=json.load(open(f,encoding="utf-8"))
    for e in d["emperors"]:
        i=e["id"]
        if i in json_ids: dup.append(i)
        json_ids.add(i)
        if i in allids: dup.append(("COLLIDE",i))  # json==hardcoded
        allids.add(i)
        did=map.get(e["dynasty"])
        if did is None: unmapped.append((e["dynasty"],e["name"]))
        elif did not in dyn_ids: orphan.append((did,e["name"]))
print("total unique ids (json+hardcoded):",len(allids))
print("json-only ids:",len(json_ids))
print("DUP:",dup)
print("UNMAPPED dynasty:",set(u[0] for u in unmapped), unmapped[:5])
print("ORPHAN (maps to nonexistent tab):",orphan[:5])
print("ALL MAPPED OK" if not dup and not unmapped and not orphan else "ISSUES")
