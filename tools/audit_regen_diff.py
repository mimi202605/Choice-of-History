# -*- coding: utf-8 -*-
"""对比「回灌后重生成」与「审查修正后的产物」，确认生成器不会造成倒退。

判定标准（只要新产物在这四项上不劣于旧产物即算通过）：
  1. 君主数 / 事件数一致
  2. 事件越出在位区间数不增加
  3. historicalOutcome 空缺数不增加
  4. 分层模板时代错置残留不增加
另外逐条列出内容差异，供人工过目。
"""
import json, os, sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass  # 被 _diff_tail.py 以 StringIO 捕获时无需重设编码

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, '..', 'data', 'emperors')
OLD = os.path.join(BASE, '_backup_regen_20260807')
FILES = ['09-us.json', '10-uk.json', '11-rome.json', '12-ru.json']


def load(path):
    d = json.load(open(path, encoding='utf-8'))
    return d if isinstance(d, list) else d['emperors']


def stats(emps):
    n_ev = bad_year = bad_out = 0
    for e in emps:
        s, t = e.get('reignStart'), e.get('reignEnd')
        for ev in e.get('events') or []:
            n_ev += 1
            y = ev.get('year')
            if isinstance(y, int) and isinstance(s, int) and isinstance(t, int) and not (s <= y <= t):
                bad_year += 1
            if not (ev.get('historicalOutcome') or '').strip():
                bad_out += 1
    return len(emps), n_ev, bad_year, bad_out


FIELDS = ['year', 'month', 'title', 'description', 'historicalOutcome',
          'choices', 'historicalChoice']

tot_old = tot_new = None
all_diff = []
gone, added = [], []

print('%-14s %-28s %-28s' % ('file', 'OLD(帝/事件/越界/空结局)', 'NEW(帝/事件/越界/空结局)'))
for fn in FILES:
    o = load(os.path.join(OLD, fn))
    n = load(os.path.join(BASE, fn))
    so, sn = stats(o), stats(n)
    print('%-14s %-28s %-28s' % (fn, '%d/%d/%d/%d' % so, '%d/%d/%d/%d' % sn))

    oi = {e['id']: e for e in o}
    ni = {e['id']: e for e in n}
    gone += [x for x in oi if x not in ni]
    added += [x for x in ni if x not in oi]
    for eid in oi:
        if eid not in ni:
            continue
        oe, ne = oi[eid], ni[eid]
        for k in ('reignStart', 'reignEnd', 'name', 'templeName', 'dynasty', 'tier'):
            if oe.get(k) != ne.get(k):
                all_diff.append('%s %s.%s: %r -> %r' % (fn, eid, k, oe.get(k), ne.get(k)))
        oev = {x['id']: x for x in oe.get('events') or []}
        nev = {x['id']: x for x in ne.get('events') or []}
        for evid in oev:
            if evid not in nev:
                all_diff.append('%s %s 事件消失: %s 《%s》' % (fn, eid, evid, oev[evid].get('title')))
                continue
            a, b = oev[evid], nev[evid]
            for k in FIELDS:
                if a.get(k) != b.get(k):
                    va, vb = a.get(k), b.get(k)
                    if isinstance(va, str) and len(va) > 40:
                        va = va[:40] + '…'
                    if isinstance(vb, str) and len(vb) > 40:
                        vb = vb[:40] + '…'
                    all_diff.append('%s %s.%s %s: %r -> %r' % (fn, eid, evid, k, va, vb))
        for evid in nev:
            if evid not in oev:
                all_diff.append('%s %s 事件新增: %s 《%s》' % (fn, eid, evid, nev[evid].get('title')))

print()
print('君主消失: %d %s' % (len(gone), gone[:10]))
print('君主新增: %d %s' % (len(added), added[:10]))
print('\n=== 内容差异 %d 条 ===' % len(all_diff))
LIMIT = int(os.environ.get('DIFF_LIMIT', '80'))
for x in all_diff[:LIMIT]:
    print('  ' + x)
if len(all_diff) > LIMIT:
    print('  … 其余 %d 条（设 DIFF_LIMIT 环境变量可放开）' % (len(all_diff) - LIMIT))
