# -*- coding: utf-8 -*-
"""中国篇：事件年份越出在位区间的分类（即位前 / 崩后）"""
import json, glob, os, sys
sys.stdout.reconfigure(encoding='utf-8')
pre, post = [], []
for p in sorted(glob.glob('data/emperors/0*.json')) + ['data/emperors/06-yuan.json','data/emperors/07-ming.json','data/emperors/08-qing.json']:
    if 'coh_data' in p or not os.path.exists(p): continue
    if os.path.basename(p)[:2] in ('09','10','11','12'): continue
    d = json.load(open(p, encoding='utf-8'))
    emps = d if isinstance(d,list) else d.get('emperors',d)
    for e in emps:
        s, t = e.get('reignStart'), e.get('reignEnd')
        for i, ev in enumerate(e.get('events') or []):
            y = ev.get('year')
            if not isinstance(y,int) or not isinstance(s,int) or not isinstance(t,int): continue
            if y < s: pre.append((os.path.basename(p), e.get('name'), s, t, i, y, ev.get('title'), s-y))
            elif y > t: post.append((os.path.basename(p), e.get('name'), s, t, i, y, ev.get('title'), y-t))
seen=set()
print('=== 崩/退位之后的事件（%d，重点）===' % len(post))
for r in sorted(post, key=lambda x:-x[7]):
    print('%-30s %-9s 在位%s~%s ev[%d] y=%s 《%s》 超出%d年' % r)
print()
print('=== 即位之前的事件（%d，多为合理"潜邸事"）===' % len(pre))
for r in sorted(pre, key=lambda x:-x[7])[:20]:
    print('%-30s %-9s 在位%s~%s ev[%d] y=%s 《%s》 提前%d年' % r)
