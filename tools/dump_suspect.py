# -*- coding: utf-8 -*-
import json, glob, os, sys
sys.stdout.reconfigure(encoding='utf-8')
TARGETS = [
 ('04-tang-wudai.json','李治',[0,3,5]),
 ('04-tang-wudai.json','李炎',[2]),
 ('04-tang-wudai.json','李漼',[0,1,2,3]),
 ('04-tang-wudai.json','李晔',[1]),
 ('04-tang-wudai.json','朱友贞',[0]),
 ('04-tang-wudai.json','柴宗训',[0]),
 ('03-jin-nanbeichao-sui.json','杨坚',[8]),
 ('05-song-liao-jin-xixia.json','赵佶',[1]),
 ('05-song-liao-jin-xixia.json','赵扩',[1]),
 ('05-song-liao-jin-xixia.json','赵昚',[5]),
 ('05-song-liao-jin-xixia.json','赵昺',[3]),
 ('05-song-liao-jin-xixia.json','完颜璟',[4]),
 ('06-yuan.json','硕德八剌',[1]),
 ('08-qing.json','颙琰',[2]),
 ('08-qing.json','载淳',[2]),
]
for fn, nm, idxs in TARGETS:
    p = os.path.join('data','emperors',fn)
    d = json.load(open(p, encoding='utf-8'))
    emps = d if isinstance(d,list) else d.get('emperors',d)
    for e in emps:
        if e.get('name') != nm: continue
        for i in idxs:
            evs = e.get('events') or []
            if i >= len(evs): continue
            ev = evs[i]
            print('### %s | %s(%s~%s) ev[%d] id=%s year=%s' % (fn, nm, e.get('reignStart'), e.get('reignEnd'), i, ev.get('id'), ev.get('year')))
            print('  T: %s' % ev.get('title'))
            print('  D: %s' % ev.get('description'))
            print('  O: %s' % (ev.get('historicalOutcome') or '(空)'))
            print()
