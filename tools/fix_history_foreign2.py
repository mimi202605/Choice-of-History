# -*- coding: utf-8 -*-
"""
外国篇残余史实修正（第二轮）
只改 title/description/choices/historicalOutcome/year/month，
保留 id / historicalChoice / relationDeltas / branches —— 玩法结构零改动。
"""
import json, os, sys, io
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'emperors')

# key: (file, emperor_id, event_index) -> patch dict
PATCH = {
    # ── 罗马篇：军区制（θέματα，行于 7–12 世纪）越界 ──────────────────────
    ('11-rome.json', 'rome_romulus_augustulus', 1): dict(
        year=475, month=9, title='蛮族佣兵索地',
        description='意大利境内日耳曼佣兵（foederati）索取三分之一田土为饷，奥雷斯特不许，营中鼓噪。',
        choices=['许其田土', '断然拒绝', '折以金帛', '拆散其部', '拖延待援'],
        historicalOutcome='拒之，佣兵推奥多亚克为主，西帝国倾覆在即',
    ),
    ('11-rome.json', 'rome_romulus_augustulus', 2): dict(
        year=475, month=10, title='拉文纳朝议',
        description='幼帝拥虚位于拉文纳，实权在其父奥雷斯特；元老遗族与蛮族将佐各持一议，东帝亦不承其号。',
        choices=['倚重父帅', '结好元老', '遣使求东帝册命', '厚赂蛮将', '闭门不问'],
        historicalOutcome='东帝不认，元老离心，孤悬拉文纳',
    ),
    ('11-rome.json', 'rome_michael8', 3): dict(
        year=1262, month=None, title='普罗尼亚封授之争',
        description='军区旧制已废，代以普罗尼亚（pronoia）封地养兵；封授不均，将佐怨望，边地骑士索加田租。',
        choices=['加封安抚', '收回滥授', '改折现钱', '募雇佣兵代之', '暂置不论'],
        historicalOutcome='封授愈广，国赋愈薄，兵仍不强',
    ),
    ('11-rome.json', 'rome_constantine11', 2): dict(
        year=1452, month=None, title='城防与佣兵',
        description='狄奥多西城墙年久失修，库帑空竭；热那亚、威尼斯佣兵索饷，守陴之众不满八千。',
        choices=['熔教产铸饷', '厚币留佣兵', '增征市税', '遣使乞援西方', '收缩守内城'],
        historicalOutcome='熔器求援皆不足，以寡守孤城',
    ),

    # ── 英国篇：《权利法案》系 1689 年、詹姆斯二世出亡之后 ────────────────
    ('10-uk.json', 'uk_james2', 1): dict(
        year=1688, month=11,
        description='威廉率荷军登陆托贝，军民响应，詹姆斯出亡法国，不流血而易主。',
    ),
    ('10-uk.json', 'uk_james2', 2): dict(
        year=1688, month=6, title='王子诞生',
        description='王后诞下王子詹姆斯·弗朗西斯，天主教一系将永续，七位显贵密函邀威廉入英。',
        choices=['昭告天下正统', '安抚新教诸侯', '罢黜异议大臣', '召荷兰女婿共商', '增募常备军'],
        historicalOutcome='王子既生，新教绝望，七贤密邀威廉',
    ),
    ('10-uk.json', 'uk_charles3', 3): dict(
        year=2023, month=None, title='王国领之议',
        description='苏格兰与北爱各有异声，加勒比诸王国领议废君主为共和；君主须超然于政争而不失体统。',
        choices=['亲巡抚绥', '一切付诸民意', '削减王室用度', '重申联合王国之谊', '缄默不预'],
        historicalOutcome='数国相继议废君统，王室以简朴与巡访应之',
    ),

    # ── 俄国篇：苏联/当代不存在「杜马与革命」「饥荒与请愿」 ─────────────
    ('12-ru.json', 'ru_brezhnev', 3): dict(
        year=1965, month=None, title='粮荒与购粮',
        description='集体农庄连年歉收，须以硬通货自西方购粮，计划体制之短遭内外訾议。',
        choices=['扩大自留地', '增拨农机化肥', '举债购粮', '压低城市定量', '整肃农业干部'],
        historicalOutcome='年年购粮于西方，农政积弊终未除',
    ),
    ('12-ru.json', 'ru_andropov', 2): dict(
        year=1983, month=7, title='政治局与整肃',
        description='政治局元老盘踞不去，部委因循怠惰；欲兴纪律整顿，则触动既得之群。',
        choices=['大举整肃', '拔擢新进', '厉行劳动纪律', '暗设专案调查', '徐图缓进'],
        historicalOutcome='严纪律、查怠工，未及深改而病殁',
    ),
    ('12-ru.json', 'ru_andropov', 3): dict(
        year=1984, month=None, title='粮荒与购粮',
        description='农产不足自给，年耗巨额外汇购粮；油价既落，国库益窘。',
        choices=['扩大自留地', '增拨农机化肥', '举债购粮', '压低城市定量', '整肃农业干部'],
        historicalOutcome='油价既落，购粮愈艰，财力日蹙',
    ),
    ('12-ru.json', 'ru_chernenko', 1): dict(
        year=1984, month=None, title='政治局与整肃',
        description='老成凋谢，政治局议事迟滞；前任整顿之政，或续或废，众莫能定。',
        choices=['尽复旧章', '续行整顿', '拔擢新进', '闭门养疴', '委事于书记处'],
        historicalOutcome='守成而已，整顿之政遂寝',
    ),
    ('12-ru.json', 'ru_chernenko', 2): dict(
        year=1985, month=None, title='短缺与排队',
        description='日用之物匮乏，商店长队不绝；军费浩繁，民生之给日削。',
        choices=['增拨轻工业', '削减军费', '严打投机', '扩大合作社', '一仍其旧'],
        historicalOutcome='匮乏如故，民心渐离',
    ),
    ('12-ru.json', 'ru_gorbachev', 3): dict(
        year=1986, month=None, title='物价与短缺',
        description='加速战略未见其效，物资益缺；禁酒令折损税入，黑市与代币券并行。',
        choices=['放开物价', '扩大企业自主', '整顿禁酒之令', '增印钞票补贴', '重申计划纪律'],
        historicalOutcome='改革未及物价，短缺与黑市俱长',
    ),
    ('12-ru.json', 'ru_medvedev', 3): dict(
        year=2009, month=None, title='杜马与政争',
        description='国家杜马诸党就任期、选制与反腐相争；金融危机方过，舆情汹汹。',
        choices=['延长任期', '推动反腐立法', '扶植新党', '整肃地方长官', '维持现状'],
        historicalOutcome='延总统任期至六年，反腐之令多成具文',
    ),
}

changed = 0
by_file = {}
for (fn, eid, idx), patch in PATCH.items():
    by_file.setdefault(fn, []).append((eid, idx, patch))

for fn, items in by_file.items():
    p = os.path.join(BASE, fn)
    d = json.load(open(p, encoding='utf-8'))
    emps = d if isinstance(d, list) else d['emperors']
    index = {e['id']: e for e in emps}
    for eid, idx, patch in items:
        e = index.get(eid)
        if not e:
            print('  [MISS] %s %s' % (fn, eid)); continue
        evs = e.get('events') or []
        if idx >= len(evs):
            print('  [MISS] %s %s ev[%d]' % (fn, eid, idx)); continue
        ev = evs[idx]
        old = ev.get('title')
        for k, v in patch.items():
            ev[k] = v
        # 选项数须与 relationDeltas / branches 对齐
        n = len(ev.get('choices') or [])
        for key in ('relationDeltas', 'branches'):
            arr = ev.get(key)
            if isinstance(arr, list) and len(arr) != n:
                print('  [WARN] %s %s ev[%d] %s 长度 %d != choices %d' % (fn, eid, idx, key, len(arr), n))
        print('  %s %-26s ev[%d] 《%s》 -> 《%s》 y=%s' % (fn, eid, idx, old, ev.get('title'), ev.get('year')))
        changed += 1
    # 事件按年月重排，避免时间倒置
    for e in emps:
        evs = e.get('events') or []
        evs.sort(key=lambda x: (x.get('year') if isinstance(x.get('year'), int) else 0,
                                x.get('month') if isinstance(x.get('month'), int) else 0))
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print('\n共修正 %d 处事件，并对四国全部君主事件按年月重排。' % changed)
