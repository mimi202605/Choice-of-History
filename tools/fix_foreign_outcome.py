# -*- coding: utf-8 -*-
"""
补全外国篇 historicalOutcome 空缺。
策略：从已经过史实核准的 description 末句派生（不新增史实断言，零风险）。
"""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'emperors')
FILES = ['09-us.json', '10-uk.json', '11-rome.json', '12-ru.json']

SPLIT = re.compile(r'[。；;！!？?]')

def derive(desc, title):
    if not desc:
        return title
    parts = [p.strip() for p in SPLIT.split(desc) if p.strip()]
    if not parts:
        return title
    # 末句通常即结果；若末句过短（<6字）则并入前一句
    tail = parts[-1]
    if len(tail) < 6 and len(parts) >= 2:
        tail = parts[-2] + '，' + tail
    # 去掉开头的时间状语（如「1688年」「十一月」「其后」）
    tail = re.sub(r'^(公元)?[前]?\d+年[，,]?', '', tail)
    tail = re.sub(r'^\d+月[，,]?', '', tail)
    if len(tail) > 30:
        tail = tail[:30]
    return tail.rstrip('，,、')

total = filled = 0
for fn in FILES:
    p = os.path.join(BASE, fn)
    d = json.load(open(p, encoding='utf-8'))
    emps = d if isinstance(d, list) else d['emperors']
    n = 0
    for e in emps:
        for ev in e.get('events') or []:
            total += 1
            if not (ev.get('historicalOutcome') or '').strip():
                ev['historicalOutcome'] = derive(ev.get('description'), ev.get('title'))
                n += 1; filled += 1
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('%-14s 补全 %d 条' % (fn, n))

print('\n外国事件 %d 条，本次补全 %d 条 historicalOutcome' % (total, filled))
