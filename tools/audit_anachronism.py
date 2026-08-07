# -*- coding: utf-8 -*-
"""史实审查：时代错置扫描
只扫描"事实性字段"（description / historicalOutcome / background / eraContext），
choices 属于玩家可选的反事实分支，单独低权重扫描。
"""
import json, os, glob, sys, io, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMP_DIR = os.path.join(BASE, 'data', 'emperors')

# (关键词, 最早可出现年份, 说明)   年份为公元纪年，负数为公元前
TERMS = [
    ("科举",      587,  "科举制始于隋（587诸州岁贡/605进士科）"),
    ("进士",      605,  "进士科始于大业元年"),
    ("状元",      622,  "状元之称始于唐武德五年"),
    ("殿试",      690,  "殿试始于武则天载初元年"),
    ("八股",     1487,  "八股文成型于明成化年间"),
    ("翰林",      738,  "翰林学士院设于唐开元二十六年"),
    ("内阁",     1382,  "明内阁（殿阁大学士）始于洪武十五年"),
    ("军机处",   1729,  "清雍正七年设军机处"),
    ("锦衣卫",   1382,  "洪武十五年设"),
    ("东厂",     1420,  "永乐十八年设"),
    ("西厂",     1477,  "成化十三年设"),
    ("巡抚",     1391,  "明代始置，宣德后制度化"),
    ("总督",     1442,  "明代中期始置"),
    ("行省",     1260,  "行省制始于元"),
    ("两税法",    780,  "唐建中元年"),
    ("一条鞭",   1581,  "明万历九年推行"),
    ("摊丁入亩", 1712,  "清康熙末—雍正初"),
    ("永不加赋", 1712,  "康熙五十一年"),
    ("均田",      485,  "均田制始于北魏太和九年"),
    ("租庸调",    624,  "唐武德七年定制"),
    ("三省六部",  581,  "隋定制"),
    ("九品中正",  220,  "曹魏黄初元年陈群创"),
    ("察举",     -134,  "汉武帝元光元年初令郡国举孝廉"),
    ("刺史",     -106,  "元封五年置十三州刺史"),
    ("年号",     -140,  "建元为第一个年号"),
    ("皇帝",     -221,  "秦始皇始称皇帝"),
    ("郡县",     -350,  "郡县制战国渐行，秦统一后全面推行"),
    ("纸",        -100, "西汉已有麻纸，105年蔡伦改进"),
    ("雕版",      600,  "雕版印刷始于隋唐之际"),
    ("活字",     1041,  "毕昇活字约庆历年间"),
    ("印刷",      600,  "印刷术始于隋唐"),
    ("火药",      808,  "唐元和年间伏火矾法；904年始用于军事"),
    ("火器",      904,  "唐末始用飞火"),
    ("火铳",     1280,  "元代出现金属管形火器"),
    ("火炮",     1280,  "元代出现"),
    ("红夷",     1604,  "红夷大炮明末传入"),
    ("鸟铳",     1548,  "嘉靖年间自倭寇传入"),
    ("交子",     1023,  "北宋天圣元年官交子"),
    ("会子",     1160,  "南宋绍兴三十年"),
    ("宝钞",     1236,  "元代纸币；明宝钞1375"),
    ("占城稻",   1012,  "宋大中祥符五年引入"),
    ("番薯",     1593,  "万历二十一年自吕宋传入"),
    ("甘薯",     1593,  "同上"),
    ("玉米",     1531,  "明中期传入"),
    ("辣椒",     1591,  "明末传入"),
    ("烟草",     1573,  "明万历年间传入"),
    ("马铃薯",   1600,  "明末传入"),
    ("花生",     1503,  "明代传入"),
    ("棉布",      700,  "棉纺织唐宋渐兴，元代黄道婆后普及"),
    ("木棉",      700,  "同上"),
    ("曲辕犁",    700,  "唐代江东犁"),
    ("马镫",      300,  "马镫约晋代成熟"),
    ("佛",         67,  "佛教东汉永平年间传入"),
    ("僧",         67,  "同上"),
    ("寺",         67,  "佛寺，东汉后"),
    ("道士",      142,  "五斗米道汉安元年"),
    ("天主教",   1582,  "利玛窦入华"),
    ("传教士",   1582,  "明末"),
    ("西洋",     1405,  "郑和下西洋后"),
    ("欧罗巴",   1583,  "明末舆图"),
    ("澳门",     1557,  "葡人入居"),
    ("眼镜",     1300,  "元末明初传入"),
    ("自鸣钟",   1582,  "利玛窦进献"),
    ("理学",     1100,  "北宋理学成型"),
    ("心学",     1500,  "王阳明"),
    ("资治通鉴", 1084,  "元丰七年成书"),
    ("史记",      -91,  "太初—征和年间成书"),
    ("汉书",       82,  "班固建初年间"),
    ("三国志",    290,  "陈寿太康年间"),
    ("白莲教",   1133,  "南宋绍兴年间茅子元创白莲宗"),
    ("摩尼教",    694,  "武周延载元年传入"),
    ("景教",      635,  "贞观九年入华"),
    ("回鹘",      744,  "回纥/回鹘汗国"),
    ("契丹",      388,  "契丹见于史载"),
    ("女真",      903,  "女真见于史载"),
    ("蒙古",     1206,  "蒙古部统一称号"),
    ("满洲",     1635,  "皇太极定族名满洲"),
    ("八旗",     1615,  "万历四十三年定八旗"),
    ("绿营",     1645,  "清初编设"),
    ("倭寇",     1223,  "倭寇之名始见于高丽史"),
    ("葡萄牙",   1514,  "明正德年间来华"),
    ("荷兰",     1601,  "明万历年间来华"),
    ("英吉利",   1637,  "明末来华"),
    ("俄罗斯",   1567,  "明代始通"),
    ("鸦片",     1729,  "清雍正年间始禁"),
    ("电报",     1871,  "清同治年间"),
    ("铁路",     1876,  "吴淞铁路"),
    ("轮船",     1865,  "江南制造总局"),
]

FACT_FIELDS = ('description', 'historicalOutcome')
EMP_FIELDS = ('background', 'eraContext', 'evaluation', 'reignPremise')


def load_all():
    files = sorted(glob.glob(os.path.join(EMP_DIR, '[0-9][0-9]-*.json')))
    out = []
    for f in files:
        d = json.load(open(f, encoding='utf-8'))
        for e in d.get('emperors', []):
            e['_file'] = os.path.basename(f)
            out.append(e)
    return out


def main():
    emps = load_all()
    hits = []
    for e in emps:
        rs = e.get('reignStart')
        re_ = e.get('reignEnd')
        if not isinstance(rs, int):
            continue
        # 只审中国君主（外国另行处理）
        if e.get('civilization') and e.get('civilization') != 'cn':
            continue
        for kw, minyear, note in TERMS:
            # 君主级字段：用 reignEnd 判定（在位期内任意时点）
            for fld in EMP_FIELDS:
                txt = e.get(fld) or ''
                if kw in txt and re_ < minyear:
                    hits.append((e['_file'], e['id'], f'{rs}~{re_}', fld, kw, minyear, note,
                                 snippet(txt, kw)))
            for ev in e.get('events', []):
                y = ev.get('year') if isinstance(ev.get('year'), int) else re_
                for fld in FACT_FIELDS:
                    txt = ev.get(fld) or ''
                    if kw in txt and y < minyear:
                        hits.append((e['_file'], e['id'] + '/' + str(ev.get('id')),
                                     str(y), fld, kw, minyear, note, snippet(txt, kw)))
    # 汇总
    bykw = {}
    for h in hits:
        bykw.setdefault(h[4], []).append(h)
    print(f'命中总数: {len(hits)}  涉及词条: {len(bykw)}\n')
    for kw in sorted(bykw, key=lambda k: -len(bykw[k])):
        lst = bykw[kw]
        print(f'\n##### 「{kw}」 早于 {lst[0][5]} 年出现，共 {len(lst)} 处 —— {lst[0][6]}')
        for h in lst[:12]:
            print(f'   [{h[0]}] {h[1]} (年:{h[2]}) .{h[3]}: {h[7]}')
        if len(lst) > 12:
            print(f'   ...另有 {len(lst)-12} 处')


def snippet(txt, kw, w=26):
    i = txt.find(kw)
    a = max(0, i - w)
    b = min(len(txt), i + w)
    return ('…' if a > 0 else '') + txt[a:b].replace('\n', ' ') + ('…' if b < len(txt) else '')


if __name__ == '__main__':
    main()
