# -*- coding: utf-8 -*-
"""外国篇史实修正：
  F1 模板事件按「文明 + 时代」重新落名，消除时代错置（议会/杜马/殖民地/军团等）
  F2 事件年份钳制到在位区间内，消除「君主已崩仍有事件」
  F3 顺带补全模板事件的 historicalOutcome
玩法结构保持不变：choices 数量、historicalChoice、relationDeltas、branches 全部不动，
仅替换 title / description / historicalOutcome / year / month。
"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'emperors')

# ---- 分层模板池：key = 原模板标题；value = [(下限年, 上限年, 新标题, 新描述, 新结局)] ----
LAYERS = {
 '议会不信任': [
   (-9999, 1214, '御前会议之争',
    '御前会议（Curia Regis）诸臣与主教各执一词，敕令难下、人事难定，封臣观望。',
    '御前争议久悬，敕令迟行'),
   (1215, 1340, '大议会与征税',
    '大宪章之后，大议会（magnum concilium）以「无共同同意不得课税」相抗，助军金迟迟不下。',
    '男爵持约拒赋，军费告匮'),
   (1341, 1640, '两院争贡赋',
    '上下两院分立，下院握钱袋而争条陈，先陈冤抑、后议拨款，御前请款屡遭驳回。',
    '下院持款相持，御用不充'),
   (1641, 1720, '国会争权',
    '国会与御前争兵权、税权与教务，弹劾大臣、悬置岁入，朝野分党。',
    '国会持权相抗，政令两歧'),
   (1721, 9999, '议会不信任',
    '下院提出不信任案，内阁摇摇欲坠，首相进退失据。',
    '不信任案过，内阁改组'),
 ],
 '殖民地危机': [
   (-9999, 1582, '属地骚动',
    '海外属地（爱尔兰边区、加莱、诺曼底旧领）赋役苛重，守臣失驭，土豪叛服不常。',
    '属地骚然，驻军不敷'),
   (1583, 1782, '殖民地危机',
    '海外殖民地抗税抗令，总督告急，本土商人与议会各持一议。',
    '殖民地骚动，商路受阻'),
   (1783, 9999, '帝国属地危机',
    '自治领与属地要求扩权，总督与本土大臣龃龉，帝国之维系日耗。',
    '属地扩权，帝国渐弛'),
 ],
 '杜马与革命': [
   (-9999, 1477, '维彻鼓动',
    '城邦维彻（вече）大会鸣钟聚众，市民与商贾责王公不职，欲另立他人。',
    '维彻鸣钟，王公见逐之危'),
   (1478, 1699, '波雅尔杜马之争',
    '波雅尔杜马（Боярская дума）门阀以「门第序位」（местничество）相争，政令壅塞、征调迟滞。',
    '门阀争序，政令壅滞'),
   (1700, 1904, '贵族与近臣之争',
    '参政院、近侍与近卫团各结朋党，或请扩贵族之权，或请复旧制，朝议纷然。',
    '近卫结党，宫廷倾轧'),
   (1905, 9999, '杜马与革命',
    '国家杜马与革命党并起，要求宪政与放权，罢工蔓延都会。',
    '杜马发难，宪政之请难拒'),
 ],
 '饥荒与请愿': [
   (-9999, 1499, '荒年与流亡',
    '连年歉收，村社饥馑，农人弃地流亡，什一税与贡赋皆无所出。',
    '饥馑流亡，贡赋无所出'),
   (1500, 1860, '饥荒与农奴逃亡',
    '荒歉大作，农奴成群南逃投哥萨克，地主告缺人力，庄园荒废。',
    '农奴逃亡，庄园荒废'),
   (1861, 9999, '饥荒与请愿',
    '饥荒蔓延数省，村社与地方自治局连章请愿，请赈请免。',
    '灾民请愿，赈务告急'),
 ],
 '元老院龃龉': [
   (-9999, -510, '长老会议龃龉',
    '百人长老会议（patres）与库里亚大会相持，王命不行，贵族各拥其部族。',
    '长老掣肘，王命难行'),
   (-509, 475, '元老院龃龉',
    '元老院内部派系倾轧，法令受阻、人事难定。',
    '元老分党，法令壅塞'),
   (476, 9999, '宫廷与教会之争',
    '皇宫内侍、大牧首与元老遗族各争其权，教义之争牵动人事，敕令屡遭驳回。',
    '宫廷教会相持，敕令难行'),
 ],
 '军团哗变': [
   (-9999, -510, '部族征召之争',
    '库里亚各部族抗拒征召，谓王擅兴师、不循古礼，兵不满伍。',
    '部族抗征，兵不满伍'),
   (-509, -108, '公民兵拒征',
    '有产公民苦于连年征调，田荒债积，拒赴征兵集会，护民官从中鼓噪。',
    '公民拒征，兵源枯竭'),
   (-107, 475, '军团哗变',
    '边省军团因欠饷或将帅野心哗变，兵锋内向。',
    '军团哗变，兵锋内向'),
   (476, 9999, '军区将领异动',
    '各军区（θέματα）将领拥兵自重，或索赏，或觊觎紫袍，京畿震恐。',
    '军区拥兵，紫袍可危'),
 ],
 # 美国：1789 年后全程适用，仅补结局
 '国会党争': [(-9999, 9999, '国会党争',
    '国会两党相攻，法案受阻、人事任命被搁置，报章推波助澜。',
    '两党相攻，法案搁浅')],
 '报刊攻讦': [(-9999, 9999, '报刊攻讦',
    '党派报刊连日攻讦，谣诼纷起，声望受损，阁员亦受牵连。',
    '报章攻讦，声望受损')],
}

FILES = ['09-us.json', '10-uk.json', '11-rome.json', '12-ru.json']

n_layer = n_clamp = n_out = 0
detail_layer, detail_clamp = [], []

for fn in FILES:
    p = os.path.join(BASE, fn)
    d = json.load(open(p, encoding='utf-8'))
    emps = d if isinstance(d, list) else d['emperors']
    for e in emps:
        s, t = e.get('reignStart'), e.get('reignEnd')
        evs = e.get('events') or []
        # --- F1 模板分层 ---
        for ev in evs:
            title = ev.get('title')
            if title not in LAYERS: continue
            y = ev.get('year') if isinstance(ev.get('year'), int) else s
            if not isinstance(y, int): y = s
            # 用「钳制后的年份」判定时代，避免用越界年份选错层
            yy = y
            if isinstance(s, int) and isinstance(t, int):
                yy = max(s, min(t, y))
            for lo, hi, nt, nd, no in LAYERS[title]:
                if lo <= yy <= hi:
                    if ev.get('title') != nt or ev.get('description') != nd:
                        detail_layer.append('%s | %s(%s~%s) y=%s 《%s》->《%s》' % (fn, e.get('name'), s, t, yy, title, nt))
                        n_layer += 1
                    ev['title'] = nt
                    ev['description'] = nd
                    if not (ev.get('historicalOutcome') or '').strip():
                        ev['historicalOutcome'] = no
                        n_out += 1
                    break
        # --- F2 年份钳制 ---
        if isinstance(s, int) and isinstance(t, int):
            used = {}
            for ev in evs:
                y = ev.get('year')
                if not isinstance(y, int): continue
                ny = max(s, min(t, y))
                if ny != y:
                    detail_clamp.append('%s | %s(%s~%s) 《%s》 year %s -> %s' % (fn, e.get('name'), s, t, ev.get('title'), y, ny))
                    ev['year'] = ny
                    n_clamp += 1
                used.setdefault(ev['year'], []).append(ev)
            # 同年多事件：以 month 排开，避免同年同月堆叠
            for yv, group in used.items():
                if len(group) > 1:
                    step = max(1, 12 // len(group))
                    for k, ev in enumerate(group):
                        if ev.get('month') in (None, 0):
                            ev['month'] = min(12, 1 + k * step)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

print('=== F1 模板按时代重落名：%d 处 ===' % n_layer)
for x in detail_layer[:60]: print('  ' + x)
if len(detail_layer) > 60: print('  … 其余 %d 处同型' % (len(detail_layer) - 60))
print()
print('=== F2 年份钳制回在位区间：%d 处 ===' % n_clamp)
for x in detail_clamp: print('  ' + x)
print()
print('=== F3 补全模板事件 historicalOutcome：%d 处 ===' % n_out)
