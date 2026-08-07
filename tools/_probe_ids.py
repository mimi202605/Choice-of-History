# -*- coding: utf-8 -*-
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'emperors')
targets = {
 '11-rome.json': ['rome_romulus_augustulus', 'rome_michael8', 'rome_constantine11'],
 '10-uk.json': ['uk_james2', 'uk_charles3'],
 '12-ru.json': ['ru_brezhnev', 'ru_andropov', 'ru_chernenko', 'ru_gorbachev', 'ru_medvedev'],
}
for fn, ids in targets.items():
    d = json.load(open(os.path.join(BASE, fn), encoding='utf-8'))
    emps = d if isinstance(d, list) else d['emperors']
    idx = {e['id']: e for e in emps}
    for eid in ids:
        e = idx.get(eid)
        if not e:
            print('MISS', eid)
            continue
        print('== %s %s (%s~%s)' % (fn, eid, e['reignStart'], e['reignEnd']))
        for ev in e.get('events') or []:
            print('   %-28s y=%-6s m=%-4s <%s>' % (ev.get('id'), ev.get('year'), ev.get('month'), ev.get('title')))
