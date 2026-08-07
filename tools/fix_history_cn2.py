# -*- coding: utf-8 -*-
"""为被改写的事件同步 choices（数量恒为 5，historicalChoice=0 仍指史实之择，
relationDeltas / branches 下标对齐不动）"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'emperors')

NEW_CHOICES = {
 '04-tang-wudai.json': {
   'tang_gaozong_e3': [
     '纳诺曷钵内附，置安乐州以处其众',
     '发兵西讨，为吐谷浑复国',
     '遣使责吐蕃，许其和亲息兵',
     '闭凉州拒纳，坐观二虏相持',
     '徙吐谷浑余部于灵夏，实边为兵',
   ],
   'tang_xuanzong_e5': [
     '遣使奉传国宝册，承太子灵武之立',
     '责其擅立，另诏诸王分领天下兵马',
     '暂不表态，观河北战局而后决',
     '召其还蜀面奏，君父之礼不可废',
     '下罪己诏，尽以军国付之',
   ],
   'tang_yizong_e0': [
     '命康承训为帅，借沙陀朱邪赤心之骑击之',
     '许其归乡免罪，以招抚息兵',
     '厚给赏赐，就地补为方镇牙兵',
     '徙戍卒于岭南别镇，散其党与',
     '弃徐泗不守，退保汴宋以待其敝',
   ],
   'tang_yizong_e1': [
     '杀翰林医官，收其亲族三百余口下狱',
     '厚葬公主而释医官，以示宽仁',
     '贬医官于岭表，不及其族',
     '纳宰相刘瞻之谏，罢狱释囚',
     '罢一切乐悬葬仪，减损以恤民力',
   ],
   'tang_yizong_e2': [
     '倾府库饰宝帐香舆，御安福门降楼膜拜',
     '止于禁中礼佛，不出内库之财',
     '依宪宗故事，迎而旋送归塔',
     '纳谏臣议，罢迎佛骨之请',
     '括天下僧田以充其费，不动国帑',
   ],
 },
 '07-ming.json': {
   'ming_yingzong_e1': [
     '罢下西洋官军，改折金花银输京',
     '留宝船于龙江，岁一遣使抚远夷',
     '弛海禁许民市舶，官收其税',
     '仍旧输本色米，不开折银之例',
     '尽鬻宝船之材，以充九边军饷',
   ],
 },
}

log = []
for fn, m in NEW_CHOICES.items():
    p = os.path.join(BASE, fn)
    d = json.load(open(p, encoding='utf-8'))
    emps = d if isinstance(d, list) else d['emperors']
    for e in emps:
        for ev in e.get('events') or []:
            eid = ev.get('id')
            if eid in m:
                old = ev.get('choices') or []
                new = m[eid]
                assert len(new) == len(old) == 5, (eid, len(old), len(new))
                ev['choices'] = new
                log.append('%-22s 《%s》 choices 已同步' % (eid, ev.get('title')))
                log.append('     旧[0] %s' % old[0])
                log.append('     新[0] %s' % new[0])
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

print('\n'.join(log))
