# -*- coding: utf-8 -*-
"""同一朝代内在位区间重叠 / 断代空洞检测"""
import json, os, glob, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'emperors')

# 只对"单线继承"朝代做严格检测（并立政权朝代跳过）
STRICT = {'唐','宋','明','清','元','隋','秦','西汉','东汉','汉','新','晋','西晋','东晋'}

for p in sorted(glob.glob(os.path.join(BASE,'*.json'))):
    if 'coh_data' in p: continue
    d = json.load(open(p, encoding='utf-8'))
    emps = d if isinstance(d,list) else d.get('emperors',d)
    by_dyn = collections.defaultdict(list)
    for e in emps:
        by_dyn[e.get('dynasty') or e.get('civilization') or '?'].append(e)
    for dyn, lst in by_dyn.items():
        if dyn not in STRICT and dyn not in ('us','uk','rome','ru'):
            continue
        lst = [e for e in lst if isinstance(e.get('reignStart'),int) and isinstance(e.get('reignEnd'),int)]
        lst.sort(key=lambda e: (e['reignStart'], e['reignEnd']))
        for a, b in zip(lst, lst[1:]):
            ov = a['reignEnd'] - b['reignStart']
            gap = b['reignStart'] - a['reignEnd']
            if ov >= 2:
                print('[重叠%2d年] %-28s %-8s %s~%s  ||  %-8s %s~%s' % (
                    ov, os.path.basename(p)+'/'+dyn, a.get('name'), a['reignStart'], a['reignEnd'],
                    b.get('name'), b['reignStart'], b['reignEnd']))
            if gap >= 3:
                print('[空洞%2d年] %-28s %-8s 止%s  ->  %-8s 始%s' % (
                    gap, os.path.basename(p)+'/'+dyn, a.get('name'), a['reignEnd'], b.get('name'), b['reignStart']))
