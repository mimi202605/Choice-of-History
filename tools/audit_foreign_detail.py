# -*- coding: utf-8 -*-
import json, os, re, collections

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'emperors')
FILES = ['09-us.json','10-uk.json','11-rome.json','12-ru.json']

TPL_TITLES = set(['国会党争','报刊攻讦','议会不信任','殖民地危机','元老院龃龉','军团哗变','杜马与革命','饥荒与请愿'])

rows_dead = []
rows_tpl  = []
per_file = collections.OrderedDict()

for fn in FILES:
    p = os.path.join(BASE, fn)
    data = json.load(open(p, encoding='utf-8'))
    emps = data if isinstance(data, list) else data.get('emperors', data)
    per_file[fn] = {'emperors': len(emps), 'events': 0, 'tpl': 0, 'dead': 0, 'noout': 0}
    for e in emps:
        s = e.get('reignStart'); t = e.get('reignEnd')
        for i, ev in enumerate(e.get('events') or []):
            per_file[fn]['events'] += 1
            y = ev.get('year')
            title = ev.get('title','')
            is_tpl = title in TPL_TITLES
            if is_tpl: per_file[fn]['tpl'] += 1
            if not (ev.get('historicalOutcome') or '').strip():
                per_file[fn]['noout'] += 1
            if isinstance(y,int) and isinstance(t,int) and y > t:
                per_file[fn]['dead'] += 1
                rows_dead.append((fn, e.get('id'), e.get('name'), s, t, i, y, title, is_tpl))
            if is_tpl:
                rows_tpl.append((fn, e.get('id'), e.get('name'), s, t, i, y, title))

print('=== 分文件统计 ===')
for k,v in per_file.items():
    print(f"{k}: 君主{v['emperors']} 事件{v['events']} 模板{v['tpl']}({v['tpl']*100//max(1,v['events'])}%) 死后事件{v['dead']} 无结局{v['noout']}")

print()
print('=== 死后/退位后事件（共 %d）===' % len(rows_dead))
for r in rows_dead:
    print(f"{r[0]} | {r[1]} {r[2]} 在位{r[3]}~{r[4]} | events[{r[5]}] year={r[6]} 《{r[7]}》 模板={r[8]}")

print()
print('=== 模板事件分布（共 %d）===' % len(rows_tpl))
by_t = collections.Counter(r[7] for r in rows_tpl)
for k,c in by_t.most_common():
    print(f"  {k}: {c}")
