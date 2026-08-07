# -*- coding: utf-8 -*-
"""中国篇史实错误修正（保留玩法结构：choices/relationDeltas/branches 一律不动）"""
import json, os, sys, copy
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'emperors')

log = []

def load(fn):
    return json.load(open(os.path.join(BASE, fn), encoding='utf-8'))

def save(fn, d):
    with open(os.path.join(BASE, fn), 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def emps_of(d):
    return d if isinstance(d, list) else d['emperors']

def find(d, eid):
    for e in emps_of(d):
        if e.get('id') == eid: return e
    raise KeyError(eid)

def ev_of(e, eid):
    for ev in e.get('events') or []:
        if ev.get('id') == eid: return ev
    raise KeyError(eid)

def setf(obj, key, val, tag):
    old = obj.get(key)
    if old != val:
        obj[key] = val
        log.append('%-26s %s: %r -> %r' % (tag, key, (old[:40] + '…') if isinstance(old, str) and len(old) > 40 else old,
                                            (val[:40] + '…') if isinstance(val, str) and len(val) > 40 else val))

# ==================== 04 唐五代 ====================
d = load('04-tang-wudai.json')

# C7 高宗·诛长孙无忌：显庆四年(659)，非永徽四年(653)，year 原 650
e = find(d, 'tang_gaozong'); ev = ev_of(e, 'tang_gaozong_e0')
setf(ev, 'year', 659, 'C7 高宗诛长孙无忌')
setf(ev, 'description', '显庆四年，许敬宗构陷长孙无忌谋反，削爵流黔州，寻逼令自缢，关陇元勋尽去，武后之势始固。', 'C7 高宗诛长孙无忌')

# C8 高宗·吐谷浑：龙朔三年(663)亡于吐蕃，非"总章二年薛仁贵灭"
ev = ev_of(e, 'tang_gaozong_e3')
setf(ev, 'title', '吐谷浑覆亡', 'C8 高宗吐谷浑')
setf(ev, 'description', '龙朔三年，吐蕃禄东赞攻灭吐谷浑，可汗诺曷钵与弘化公主奔凉州求内附。青海尽入吐蕃，河陇门户洞开。', 'C8 高宗吐谷浑')
setf(ev, 'historicalOutcome', '吐谷浑亡吐蕃逼河陇', 'C8 高宗吐谷浑')

# C9 高宗·驾崩：弘道元年(683)，非调露二年(680)
ev = ev_of(e, 'tang_gaozong_e5')
setf(ev, 'description', '弘道元年十二月高宗崩于洛阳贞观殿，年五十六。太子显即位，是为中宗，军国大事听天后处分。', 'C9 高宗驾崩')

# C5 中宗在位区间：684 年首次在位仅五十五日即废，正式在位为神龙元年(705)复辟至景龙四年(710)
e = find(d, 'tang_zongzhong')
setf(e, 'reignStart', 705, 'C5 中宗在位')
setf(e, 'evaluation', (e.get('evaluation') or '') + '（嗣圣元年首践祚五十五日即废，神龙元年复辟，此为复辟之朝）', 'C5 中宗在位')

# C1/C2/C3 玄宗
e = find(d, 'tang_xuanzong')
setf(e, 'reignEnd', 756, 'C1 玄宗在位')
setf(e, 'evaluation', (e.get('evaluation') or '') + '（天宝十五载马嵬后北奔灵武，肃宗即位，玄宗退为太上皇，宝应元年崩）', 'C1 玄宗在位')
ev = ev_of(e, 'tang_xuanzong_e4')
setf(ev, 'year', 756, 'C2 马嵬坡之变')
setf(ev, 'description', '天宝十五载六月，玄宗幸蜀至马嵬驿，六军不发，请诛国忠。陈玄礼率将士杀杨国忠，又迫玄宗赐杨贵妃死，军乃发。', 'C2 马嵬坡之变')
ev = ev_of(e, 'tang_xuanzong_e5')
setf(ev, 'year', 756, 'C3 玄宗归政')
setf(ev, 'title', '灵武称制与归政', 'C3 玄宗归政')
setf(ev, 'description', '天宝十五载七月，太子亨自立于灵武，改元至德，遥尊玄宗为太上皇。玄宗在蜀闻之，遣使奉传国宝册，自此退居兴庆宫，不复预政。', 'C3 玄宗归政')
setf(ev, 'historicalOutcome', '肃宗立玄宗为太上皇', 'C3 玄宗归政')

# C4 肃宗 background：崩于宝应元年(762)，非乾元元年(758)
e = find(d, 'tang_suzong')
setf(e, 'background', (e.get('background') or '').replace('乾元元年崩', '宝应元年崩'), 'C4 肃宗崩年')

# C10 武宗·平泽潞：会昌四年(844)平
e = find(d, 'tang_wuzong'); ev = ev_of(e, 'tang_wuzong_e2')
setf(ev, 'year', 844, 'C10 武宗平泽潞')

# C11/C12/C13 懿宗：王仙芝(874)、黄巢(875)、陷广州(879) 皆僖宗朝事，懿宗咸通十四年(873)已崩
e = find(d, 'tang_yizong')
ev = ev_of(e, 'tang_yizong_e0')
setf(ev, 'year', 868, 'C11 懿宗·庞勋')
setf(ev, 'title', '庞勋之乱', 'C11 懿宗·庞勋')
setf(ev, 'description', '咸通九年，戍桂州徐州兵期满不得代，推粮料判官庞勋北还，据徐州举兵，淮泗大震，官军屡败。', 'C11 懿宗·庞勋')
setf(ev, 'historicalOutcome', '庞勋乱起徐泗骚然', 'C11 懿宗·庞勋')
ev = ev_of(e, 'tang_yizong_e1')
setf(ev, 'year', 869, 'C11 懿宗·同昌')
setf(ev, 'title', '同昌公主之丧', 'C11 懿宗·同昌')
setf(ev, 'description', '咸通十年，爱女同昌公主薨。帝痛甚，杀翰林医官韩宗劭等二十余人，收其亲族三百余口下狱，宰相刘瞻谏而遭贬。', 'C11 懿宗·同昌')
setf(ev, 'historicalOutcome', '医官族诛谏臣坐贬', 'C11 懿宗·同昌')
ev = ev_of(e, 'tang_yizong_e2')
setf(ev, 'year', 873, 'C12 懿宗·迎佛骨')
setf(ev, 'title', '迎佛骨于凤翔', 'C12 懿宗·迎佛骨')
setf(ev, 'description', '咸通十四年三月，迎佛骨于凤翔法门寺，倾府库以饰宝帐香舆，自开远门至安福门夹道观者如堵，帝御安福门降楼膜拜。', 'C12 懿宗·迎佛骨')
setf(ev, 'historicalOutcome', '倾帑迎佛骨国用益匮', 'C12 懿宗·迎佛骨')
ev = ev_of(e, 'tang_yizong_e3')
setf(ev, 'year', 873, 'C13 懿宗·驾崩')
setf(ev, 'description', '咸通十四年七月懿宗崩，年四十一。宦官刘行深、韩文约立第五子普王俨，是为僖宗，年十二。', 'C13 懿宗·驾崩')
setf(ev, 'historicalOutcome', '僖宗冲龄立宦官立君', 'C13 懿宗·驾崩')

# C14 昭宗·刘季述之变：光化三年(900)，非大顺元年(890)；被立者为太子李裕(德王)
e = find(d, 'tang_zhaozong'); ev = ev_of(e, 'tang_zhaozong_e1')
setf(ev, 'description', '光化三年十一月，宦官刘季述等拥兵入宫，幽昭宗于少阳院，矫诏立太子李裕为帝。次年正月崔胤结孙德昭诛季述，昭宗复位。', 'C14 昭宗刘季述')

# C15 后梁末帝·汴州陷落：龙德三年(923)，"龙纪元年"为唐昭宗年号(889)
e = find(d, 'houliang_modi') if any(x.get('id') == 'houliang_modi' for x in emps_of(d)) else None
for cand in emps_of(d):
    if cand.get('name') == '朱友贞':
        for ev in cand.get('events') or []:
            if ev.get('title') == '汴州陷落':
                setf(ev, 'description', '龙德三年十月，晋王李存勖破汴州，友贞命都指挥使皇甫麟弑己而死，梁亡，凡十七年。', 'C15 后梁亡')

# C16 后周恭帝·陈桥兵变：显德七年(960)正月，"乾德元年"为宋太祖年号(963)
for cand in emps_of(d):
    if cand.get('name') == '柴宗训':
        for ev in cand.get('events') or []:
            if ev.get('title') == '陈桥兵变':
                setf(ev, 'description', '显德七年正月，赵匡胤于陈桥驿黄袍加身，回师汴梁，恭帝禅位于宋，周亡。宋建隆元年始。', 'C16 陈桥兵变')

save('04-tang-wudai.json', d)

# ==================== 03 晋南北朝隋 ====================
d = load('03-jin-nanbeichao-sui.json')
# C17 隋文帝·科举初萌：开皇七年(587)诏诸州岁贡三人，非开皇十五年
e = find(d, 'sui_wendi'); ev = ev_of(e, 'sui_wendi_e8')
setf(ev, 'year', 587, 'C17 隋文帝科举')
setf(ev, 'description', '开皇七年，制诸州岁贡三人，以志行修谨、清平干济课试取人，九品中正之法渐废，科举之制初萌，为中国选官制度一大变革。', 'C17 隋文帝科举')
# C23 隋炀帝：仁寿四年(604)七月即位，大业元年(605)改元
e = find(d, 'sui_yangdi')
setf(e, 'reignStart', 604, 'C23 隋炀帝即位')
save('03-jin-nanbeichao-sui.json', d)

# ==================== 05 宋辽金夏 ====================
d = load('05-song-liao-jin-xixia.json')
# C18 宋孝宗·淳熙之治：淳熙元年 = 1174
e = find(d, 'song_xiaozong'); ev = ev_of(e, 'song_xiaozong_e5')
setf(ev, 'year', 1174, 'C18 淳熙之治')
save('05-song-liao-jin-xixia.json', d)

# ==================== 06 元 ====================
d = load('06-yuan.json')
# C19 元英宗·颁大元通制：至治三年 = 1323
e = find(d, 'yuan_yingzong'); ev = ev_of(e, 'yuan_yingzong_e1')
setf(ev, 'year', 1323, 'C19 大元通制')
# C22 元文宗两度在位，与明宗(1329)重叠
for cand in emps_of(d):
    if cand.get('name') == '图帖睦尔':
        setf(cand, 'evaluation', (cand.get('evaluation') or '') + '（天历元年首立，次年让位明宗，明宗暴崩后复位至至顺三年）', 'C22 元文宗')
save('06-yuan.json', d)

# ==================== 07 明 ====================
d = load('07-ming.json')
e = find(d, 'ming_yingzong')
# C20 英宗两段在位：正统1435-1449、天顺1457-1464，中隔景泰八年
setf(e, 'evaluation', (e.get('evaluation') or '') + '（正统一四三五—一四四九、天顺一四五七—一四六四，中隔景泰八年）', 'C20 明英宗在位')
# C21《废胡立孙》为宣德三年(1428)宣宗之事，非英宗所为
ev = ev_of(e, 'ming_yingzong_e1')
setf(ev, 'year', 1436, 'C21 明英宗易事')
setf(ev, 'title', '罢下西洋与开中盐法', 'C21 明英宗易事')
setf(ev, 'description', '正统元年，诏罢下西洋官军，封舟朽于龙江；又弛银禁，改南畿浙江税粮折银百万余两输京，号金花银。海事既息，度支渐倚白银。', 'C21 明英宗易事')
setf(ev, 'historicalOutcome', '罢宝船立金花银海权自此绝', 'C21 明英宗易事')
save('07-ming.json', d)

print('\n'.join(log))
print('\n合计修改 %d 处' % len(log))
