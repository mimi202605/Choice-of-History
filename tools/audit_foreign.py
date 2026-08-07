# -*- coding: utf-8 -*-
"""史实审查：外国君主（美/英/罗马/俄）专项"""
import json, os, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMP_DIR = os.path.join(BASE, 'data', 'emperors')
FILES = ['09-us.json', '10-uk.json', '11-rome.json', '12-ru.json']

# 通用填充事件标题（generator 模板）
FILLER_TITLES = set()

# 外国时代错置词表：(词, 最早年份, 说明)
FTERMS = [
    ("议会不信任", 1782, "不信任动议惯例始于1782年诺斯内阁倒台"),
    ("下院",       1341, "英格兰下议院与上议院分立约1341年"),
    ("殖民地",     1585, "英格兰海外殖民地始于1585罗阿诺克/1607詹姆斯敦"),
    ("内阁",       1721, "英国内阁制与首相制始于沃波尔"),
    ("首相",       1721, "同上"),
    ("杜马",       1906, "国家杜马设于1906年"),
    ("宪政",       1789, "近代宪政"),
    ("революция", 1789, ""),
    ("革命党",     1860, "近代革命政党"),
    ("农奴解放",   1861, "1861年农奴制改革"),
    ("铁路",       1825, "1825年斯托克顿-达灵顿铁路"),
    ("电报",       1837, "1837年电报"),
    ("报刊",       1605, "近代报纸始于17世纪初"),
    ("报纸",       1605, "同上"),
    ("舆论",       1605, "近代大众舆论以报刊为载体"),
    ("政党",       1678, "英国辉格/托利党争约1678起"),
    ("国会",       1789, "美国国会1789年成立"),
    ("最高法院",   1789, "美国最高法院1789年设立"),
    ("联邦储备",   1913, "美联储1913年"),
    ("元老院",     -509, "罗马共和国元老院（王政期为长老会议）"),
    ("保民官",     -494, "平民保民官设于前494年"),
    ("独裁官",     -501, "独裁官职约前501年设"),
    ("基督",        30, "基督教起源"),
    ("教皇",       380, "罗马主教称号演进"),
    ("东正教",    1054, "东西教会大分裂"),
]

FACT_FIELDS = ('description', 'historicalOutcome')


def main():
    all_e = []
    for f in FILES:
        d = json.load(open(os.path.join(EMP_DIR, f), encoding='utf-8'))
        for e in d['emperors']:
            e['_file'] = f
            all_e.append(e)

    # 1. 统计事件标题频次 -> 找模板填充事件
    freq = {}
    for e in all_e:
        for ev in e.get('events', []):
            freq.setdefault(ev.get('title'), []).append(e['id'])
    print('===== 高频重复事件标题（疑为模板填充） =====')
    for t, ids in sorted(freq.items(), key=lambda kv: -len(kv[1])):
        if len(ids) >= 3:
            print(f'  「{t}」 × {len(ids)}   e.g. {ids[:6]}')
            FILLER_TITLES.add(t)

    # 2. 死后事件（超出在位末年）
    print('\n===== 君主已死/退位后仍发生的事件 =====')
    n = 0
    for e in all_e:
        for ev in e.get('events', []):
            y = ev.get('year')
            if isinstance(y, int) and y > e['reignEnd']:
                n += 1
                print(f"  [{e['_file']}] {e['id']} 卒/终于{e['reignEnd']} -> 事件{y}《{ev.get('title')}》")
    print('  合计:', n)

    # 3. 时代错置
    print('\n===== 外国时代错置 =====')
    m = 0
    for e in all_e:
        for kw, minyear, note in FTERMS:
            for ev in e.get('events', []):
                y = ev.get('year') if isinstance(ev.get('year'), int) else e['reignEnd']
                for fld in FACT_FIELDS:
                    txt = ev.get(fld) or ''
                    if kw in txt and y < minyear:
                        m += 1
                        print(f"  [{e['_file']}] {e['id']} ({y}) 「{kw}」<{minyear} :: {txt[:60]}  // {note}")
    print('  合计:', m)

    # 4. historicalOutcome 缺失
    print('\n===== historicalOutcome 空缺统计 =====')
    tot = miss = 0
    for e in all_e:
        for ev in e.get('events', []):
            tot += 1
            if not (ev.get('historicalOutcome') or '').strip():
                miss += 1
    print(f'  外国事件总数 {tot}，historicalOutcome 为空 {miss} ({miss*100//max(tot,1)}%)')

    # 5. relationDeltas / historicalChoice 完整性
    nod = sum(1 for e in all_e for ev in e.get('events', []) if not ev.get('relationDeltas'))
    print(f'  缺 relationDeltas 的外国事件: {nod}')


if __name__ == '__main__':
    main()
