# -*- coding: utf-8 -*-
"""对比 _backup_audit_20260807 与现状，统计本次史实修正的精确改动面"""
import json, os, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'emperors')
BK = os.path.join(BASE, '_backup_audit_20260807')

FIELDS = ['title', 'description', 'historicalOutcome', 'year', 'month', 'choices', 'historicalChoice']
tot = {'新增君主': 0, '在位区间修正': 0, '事件改标题': 0, '事件改年月': 0,
       '事件改描述': 0, '事件改选项': 0, '补全结局': 0, 'background修正': 0}
rows = []

for p in sorted(glob.glob(os.path.join(BASE, '*.json'))):
    fn = os.path.basename(p)
    bp = os.path.join(BK, fn)
    if not os.path.exists(bp):
        continue
    new = json.load(open(p, encoding='utf-8'))
    old = json.load(open(bp, encoding='utf-8'))
    ne = new if isinstance(new, list) else new['emperors']
    oe = old if isinstance(old, list) else old['emperors']
    om = {e['id']: e for e in oe}
    for e in ne:
        o = om.get(e['id'])
        if o is None:
            tot['新增君主'] += 1
            rows.append('%s  [新增君主] %s %s %s~%s' % (fn, e['id'], e['name'], e['reignStart'], e['reignEnd']))
            continue
        if e.get('reignStart') != o.get('reignStart') or e.get('reignEnd') != o.get('reignEnd'):
            tot['在位区间修正'] += 1
            rows.append('%s  [在位] %s %s: %s~%s -> %s~%s' % (fn, e['id'], e['name'],
                        o.get('reignStart'), o.get('reignEnd'), e.get('reignStart'), e.get('reignEnd')))
        if (e.get('background') or '') != (o.get('background') or ''):
            tot['background修正'] += 1
            rows.append('%s  [背景] %s %s' % (fn, e['id'], e['name']))
        oev = {ev.get('id'): ev for ev in (o.get('events') or []) if ev.get('id')}
        for ev in (e.get('events') or []):
            ov = oev.get(ev.get('id'))
            if ov is None:
                continue
            if ev.get('title') != ov.get('title'):
                tot['事件改标题'] += 1
                rows.append('%s  [标题] %s: 《%s》->《%s》' % (fn, ev.get('id'), ov.get('title'), ev.get('title')))
            if ev.get('year') != ov.get('year') or ev.get('month') != ov.get('month'):
                tot['事件改年月'] += 1
                rows.append('%s  [年月] %s 《%s》: %s.%s -> %s.%s' % (fn, ev.get('id'), ev.get('title'),
                            ov.get('year'), ov.get('month'), ev.get('year'), ev.get('month')))
            if (ev.get('description') or '') != (ov.get('description') or ''):
                tot['事件改描述'] += 1
            if (ev.get('choices') or []) != (ov.get('choices') or []):
                tot['事件改选项'] += 1
            if not (ov.get('historicalOutcome') or '').strip() and (ev.get('historicalOutcome') or '').strip():
                tot['补全结局'] += 1

print('=== 改动面统计 ===')
for k, v in tot.items():
    print('  %-14s %d' % (k, v))
print('\n=== 明细（在位/标题/年月/新增，共 %d 条）===' % len(rows))
for r in rows:
    print(' ', r)
