# -*- coding: utf-8 -*-
import json, os, collections, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'emperors')

TERMS = {
 'uk': {
   '议会': (1265, '孟福尔议会1265'),
   '下院': (1341, '两院分立1341'),
   '上院': (1341, '两院分立1341'),
   '不信任': (1742, '沃波尔倒台'),
   '内阁': (1721, '沃波尔首相制'),
   '首相': (1721, '沃波尔'),
   '殖民地': (1583, '纽芬兰1583/詹姆斯敦1607'),
   '报刊': (1621, '英格兰最早新闻纸'),
   '大宪章': (1215, ''),
   '国教': (1534, '至尊法案'),
   '联合王国': (1707, '英苏合并'),
   '自治领': (1867, '加拿大自治领'),
 },
 'ru': {
   '杜马': (1906, '国家杜马1906'),
   '革命': (1825, '十二月党人1825'),
   '沙皇': (1547, '伊凡四世加冕'),
   '农奴解放': (1861, ''),
   '东正教': (1054, '东西教会大分裂'),
   '苏维埃': (1905, ''),
   '宪政': (1905, '十月诏书'),
   '枢密院': (1711, '参政院'),
   '西伯利亚': (1582, '叶尔马克东征'),
   '彼得堡': (1703, ''),
 },
 'rome': {
   '保民官': (-494, '平民撤离后设'),
   '皇帝': (-27, '奥古斯都'),
   '元首': (-27, ''),
   '基督教': (33, ''),
   '主教': (100, ''),
   '行省': (-241, '西西里首个行省'),
   '禁卫军': (-27, '奥古斯都设'),
   '十二铜表法': (-450, ''),
   '君士坦丁堡': (330, ''),
   '教皇': (200, ''),
 },
 'us': {
   '国会': (1789, ''),
   '联邦': (1789, ''),
   '内战': (1861, ''),
   '废奴': (1865, '十三修正案'),
   '铁路': (1830, ''),
   '电报': (1844, ''),
   '美联储': (1913, ''),
   '大萧条': (1929, ''),
   '冷战': (1947, ''),
   '民权法案': (1964, ''),
 },
}
FILES = {'09-us.json':'us','10-uk.json':'uk','11-rome.json':'rome','12-ru.json':'ru'}
FIELDS = ['description','historicalOutcome','title']
EFIELDS = ['background','eraContext','evaluation']

hits = []
for fn, civ in FILES.items():
    d = json.load(open(os.path.join(BASE,fn), encoding='utf-8'))
    emps = d if isinstance(d,list) else d.get('emperors',d)
    for e in emps:
        s = e.get('reignStart')
        for f in EFIELDS:
            txt = e.get(f) or ''
            for w,(y0,note) in TERMS[civ].items():
                if w in txt and isinstance(s,int) and s < y0:
                    hits.append((fn,e['id'],e['name'],s,'emp.'+f,w,y0,note,txt[:60]))
        for i,ev in enumerate(e.get('events') or []):
            yy = ev.get('year') if isinstance(ev.get('year'),int) else s
            for f in FIELDS:
                txt = ev.get(f) or ''
                for w,(y0,note) in TERMS[civ].items():
                    if w in txt and isinstance(yy,int) and yy < y0:
                        hits.append((fn,e['id'],e['name'],yy,'ev[%d].%s'%(i,f),w,y0,note,(ev.get('title','')+' | '+txt)[:70]))

print('=== 外国篇时代错置命中 %d ===' % len(hits))
cnt = collections.Counter(h[5] for h in hits)
for w,c in cnt.most_common(): print('  %s: %d' % (w,c))
print()
for h in sorted(hits, key=lambda x:(x[0],x[3])):
    print('%s | %s %s y=%s | %s | [%s]应>=%s (%s) | %s' % (h[0],h[1],h[2],h[3],h[4],h[5],h[6],h[7],h[8]))
