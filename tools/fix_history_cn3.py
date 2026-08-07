# -*- coding: utf-8 -*-
"""中国篇第三轮微调：纪年口径统一（唐敬宗/文宗交界）"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'emperors')

p = os.path.join(BASE, '04-tang-wudai.json')
d = json.load(open(p, encoding='utf-8'))
emps = d if isinstance(d, list) else d['emperors']
idx = {e['id']: e for e in emps}

# 敬宗李湛：宝历二年（826）十二月被弑。原 reignEnd=827 用公历折算，
# 与文宗 reignStart=826（中历）口径不一，造成 1 年重叠。统一为通行纪年 824~826。
e = idx['tang_jingzong']
print('唐敬宗 reignEnd %s -> 826' % e['reignEnd']); e['reignEnd'] = 826
for ev in e['events']:
    if ev.get('year') == 827:
        print('  ev《%s》 y 827 -> 826' % ev['title']); ev['year'] = 826
        if ev['title'] == '为宦官所弑':
            ev['month'] = 12
            ev['description'] = '宝历二年十二月，夜猎还宫，与宦官刘克明等饮博，烛灭遇弑于室内，年十八。'
        if ev['title'] == '刘克明之逆':
            ev['month'] = 12

# 文宗李昂：宝历二年十二月由王守澄等迎立，次年正月改元大和。
e = idx['tang_wenzong']
for ev in e['events']:
    if ev.get('title') == '即位受制' and ev.get('year') == 827:
        ev['year'] = 826; ev['month'] = 12
        ev['description'] = '宝历二年十二月，宦官王守澄、梁守谦等诛刘克明，迎江王涵入宫即位，明年改元大和。帝虽即位，禁军神策尽在家奴之手。'
        print('唐文宗《即位受制》 y 827 -> 826')

e['events'].sort(key=lambda x: (x.get('year') if isinstance(x.get('year'), int) else 9999,
                                x.get('month') if isinstance(x.get('month'), int) else 0))
idx['tang_jingzong']['events'].sort(key=lambda x: (x.get('year') if isinstance(x.get('year'), int) else 9999,
                                                   x.get('month') if isinstance(x.get('month'), int) else 0))
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\n04-tang-wudai.json 已写回')
