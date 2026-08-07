# -*- coding: utf-8 -*-
"""对照权威纪年表核查在位年代（抽取高知名度君主）"""
import json, os, glob, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'emperors')

# name/templeName 关键字 -> (标准 reignStart, reignEnd)  依《中国历代纪年表》
REF = {
 '秦始皇': (-246, -210),   # 前247即秦王位(或前246)，前221称帝，前210崩
 '汉高祖': (-206, -195),
 '汉武帝': (-141, -87),
 '汉光武帝': (25, 57),
 '汉献帝': (189, 220),
 '曹丕': (220, 226),
 '刘备': (221, 223),
 '孙权': (229, 252),
 '晋武帝': (265, 290),
 '隋文帝': (581, 604),
 '隋炀帝': (604, 618),
 '唐高祖': (618, 626),
 '唐太宗': (626, 649),
 '武则天': (690, 705),
 '唐玄宗': (712, 756),
 '宋太祖': (960, 976),
 '宋太宗': (976, 997),
 '宋徽宗': (1100, 1126),
 '宋高宗': (1127, 1162),
 '元世祖': (1260, 1294),
 '明太祖': (1368, 1398),
 '明成祖': (1402, 1424),
 '明思宗': (1627, 1644),
 '清太祖': (1616, 1626),
 '清圣祖': (1661, 1722),
 '清世宗': (1722, 1735),
 '清高宗': (1735, 1796),
 '光绪': (1875, 1908),
 '宣统': (1908, 1912),
 # 外国
 '乔治·华盛顿': (1789, 1797),
 '亚伯拉罕·林肯': (1861, 1865),
 '富兰克林·罗斯福': (1933, 1945),
 '征服者威廉': (1066, 1087),
 '亨利八世': (1509, 1547),
 '伊丽莎白一世': (1558, 1603),
 '维多利亚': (1837, 1901),
 '奥古斯都': (-27, 14),
 '图拉真': (98, 117),
 '君士坦丁': (306, 337),
 '查士丁尼': (527, 565),
 '伊凡四世': (1547, 1584),
 '彼得一世': (1682, 1725),
 '叶卡捷琳娜二世': (1762, 1796),
 '尼古拉二世': (1894, 1917),
}

found = {}
for p in sorted(glob.glob(os.path.join(BASE,'*.json'))):
    if 'coh_data' in p: continue
    d = json.load(open(p, encoding='utf-8'))
    emps = d if isinstance(d,list) else d.get('emperors',d)
    for e in emps:
        for k in REF:
            nm = (e.get('name') or '') + '|' + (e.get('templeName') or '')
            if k in nm and k not in found:
                found[k] = (os.path.basename(p), e.get('id'), e.get('name'), e.get('templeName'), e.get('reignStart'), e.get('reignEnd'))

print('%-14s %-10s %-12s %-12s %s' % ('人物','游戏在位','权威在位','偏差','文件'))
bad = 0
for k,(ref_s,ref_e) in REF.items():
    if k not in found:
        print('%-14s  [未找到]' % k); continue
    fn,i,nm,tn,s,t = found[k]
    ds = (s-ref_s) if isinstance(s,int) else None
    de = (t-ref_e) if isinstance(t,int) else None
    flag = '' if (ds==0 and de==0) else ('  <== 偏差 %+d/%+d' % (ds,de))
    if flag: bad += 1
    print('%-14s %-11s %-12s %s %s' % (k, '%s~%s'%(s,t), '%s~%s'%(ref_s,ref_e), flag, fn))
print()
print('偏差条目: %d / %d' % (bad, len(REF)))
