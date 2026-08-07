# -*- coding: utf-8 -*-
"""补入武则天（武周 690-705）——中国史上唯一女皇帝，原库完全缺席，
致中宗在位区间吞掉武周十五年。dynasty 取「唐」以匹配 DYNASTIES 映射表。"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'emperors')
P = os.path.join(BASE, '04-tang-wudai.json')

def rd(*pairs):
    """构造 5 项 relationDeltas"""
    out = []
    for p in pairs:
        out.append(dict(p) if p else {})
    while len(out) < 5: out.append({})
    return out

WU = {
  "id": "wu_zetian",
  "dynasty": "唐",
  "name": "武曌",
  "templeName": "则天皇帝",
  "reignStart": 690,
  "reignEnd": 705,
  "evaluation": "革唐命而立武周，中国史上唯一女皇帝；上承贞观、下启开元",
  "background": "武曌，并州文水人，工部尚书武士彟之女。太宗时入宫为才人，赐号武媚；太宗崩，出家感业寺。高宗永徽六年立为皇后，显庆后与帝并称二圣，高宗患风眩，百司奏事多决于后。中宗立而旋废，睿宗立而囚之别殿，太后临朝称制六年。天授元年九月，革唐命，改国号周，自称圣神皇帝，都洛阳，号神都。神龙元年正月，张柬之等诛二张，逼禅位于中宗，是年十一月崩于上阳宫，遗制去帝号，称则天大圣皇后。",
  "eraContext": "唐室之统既移，李氏诸王与关陇旧族心怀异图，故广开告密、任用酷吏以慑之；又破格取士、亲策贡人于洛城殿，拔狄仁杰、姚崇、宋璟于寒素，士林之路遂宽。北有突厥默啜，东北有契丹之乱，边事不宁；而漕运通、户口增，海内粗安。继嗣之争悬于李、武之间，一念所决，即定天下归属。",
  "reignPremise": "以女子之身受天下，然天下终须还与谁人：李氏之子，抑或武氏之侄？",
  "voiceTag": "冷峻",
  "initStats": {"treasury": 62, "people": 60, "military": 58, "court": 40, "health": 58, "tech": 60},
  "tier": "A",
  "cast": [
    {"id": "wu_direnjie", "name": "狄仁杰", "role": "股肱谏臣", "voiceTag": "质朴"},
    {"id": "wu_laijunchen", "name": "来俊臣", "role": "罗织酷吏", "voiceTag": "冷峻"},
    {"id": "wu_zhangyizhi", "name": "张易之兄弟", "role": "内廷幸臣", "voiceTag": "华赡"}
  ],
  "events": [
    {
      "year": 690, "month": 9,
      "title": "革唐命",
      "description": "天授元年九月，傅游艺率关中百姓上表请改国号，群臣、宗戚、远夷、沙门凡六万人俱上请。乃御则天门，赦天下，改唐为周，自称圣神皇帝，降睿宗为皇嗣，赐姓武。",
      "historicalChoice": 0,
      "choices": [
        "受尊号称帝，改国号为周",
        "仍临朝称制，不改唐祚",
        "还政皇嗣，退居后宫",
        "先立武氏诸侄为王，缓称尊号",
        "遍封李氏诸王以安宗室，然后即位"
      ],
      "historicalOutcome": "唐祚移于周李氏益危",
      "id": "wu_zetian_e0",
      "relationDeltas": rd({"宗室": -8, "士大夫": -4}, {"宗室": 2}, {"宗室": 4, "士大夫": 2}, {"宗室": -5}, {"宗室": 1, "士大夫": -2}),
      "branches": [{"setFlags": ["usurped", "reform"]}, {}, {}, {}, {}]
    },
    {
      "year": 691, "month": None,
      "title": "告密与酷吏",
      "description": "置铜匦于朝堂，四方告密者驿马续食以闻。周兴、来俊臣、索元礼辈罗织《告密罗织经》，讯囚有定百脉、突地吼诸酷法，宗室大臣坐诛流者以千数，朝士入朝辄与家人诀。",
      "historicalChoice": 0,
      "choices": [
        "广开告密之门，任酷吏以慑异图",
        "存铜匦而禁诬告，坐反坐之法",
        "尽罢酷吏，付狱于大理正断",
        "只诛首恶，宥其胁从",
        "以宗室为质而不兴大狱"
      ],
      "historicalOutcome": "罗织大兴人人自危而位固",
      "id": "wu_zetian_e1",
      "relationDeltas": rd({"宗室": -10, "士大夫": -8}, {"士大夫": -2}, {"士大夫": 6, "宗室": 3}, {"士大夫": 2}, {"宗室": -3}),
      "branches": [{"setFlags": ["scholar_purge"]}, {}, {"setFlags": ["amnesty"]}, {}, {}]
    },
    {
      "year": 690, "month": 2,
      "title": "策问贡士于洛城殿",
      "description": "亲策贡人于洛城殿，殿试自此始；又诏内外九品以上及百姓皆得自举，试官、员外置官纷然。滥进虽多，而狄仁杰、姚元崇、宋璟辈皆由是拔于寒素。",
      "historicalChoice": 0,
      "choices": [
        "亲策贡士、许人自举，破格用人",
        "仍循常调，铨选一委吏部",
        "专用武氏子弟与北门学士",
        "复行九品中正，以门第定选",
        "增置武举，兼取材勇"
      ],
      "historicalOutcome": "殿试始寒门骤进冗官亦滋",
      "id": "wu_zetian_e2",
      "relationDeltas": rd({"士大夫": 6, "宗室": -3}, {"士大夫": 1}, {"士大夫": -6, "宗室": 4}, {"士大夫": -4, "宗室": 5}, {"边将": 5, "士大夫": 1}),
      "branches": [{"setFlags": ["reform"]}, {}, {}, {}, {}]
    },
    {
      "year": 696, "month": 5,
      "title": "营州之乱",
      "description": "契丹松漠都督李尽忠、归诚州刺史孙万荣以营州都督赵文翽侵侮，举兵杀翽，据营州，自号无上可汗，河北大震。诏梁王武三思、武攸宜等讨之，官军再败于硖石谷、东硖石。",
      "historicalChoice": 0,
      "choices": [
        "以武氏诸王为帅出讨，兼结突厥夹击",
        "遣宿将王孝杰专征，不用外戚",
        "许契丹自治，罢营州都督府以息事",
        "尽发河北丁壮筑城自守，不与野战",
        "厚币赂突厥默啜，使代我讨之"
      ],
      "historicalOutcome": "官军屡败终借突厥而定",
      "id": "wu_zetian_e3",
      "relationDeltas": rd({"边将": -5, "宗室": 4}, {"边将": 6, "宗室": -3}, {"边将": -4}, {"边将": -2, "商贾": -2}, {"边将": -3, "商贾": -4}),
      "branches": [{"setFlags": ["war_loss"]}, {"setFlags": ["war_win"]}, {}, {}, {}]
    },
    {
      "year": 698, "month": 3,
      "title": "还储庐陵",
      "description": "武承嗣、武三思数使人说太后，以「自古天子未有以异姓为嗣者」求为太子。狄仁杰对曰：姑侄之与母子孰亲？陛下立子，则千秋万岁后配食太庙；立侄，未闻侄为天子而祔姑于庙者。乃密遣使召庐陵王于房州，复立为皇太子。",
      "historicalChoice": 0,
      "choices": [
        "召庐陵王还，复立为皇太子",
        "立武承嗣为太子，以周传周",
        "立皇嗣旦为储，不召庐陵",
        "悬储不定，使李武互相牵制",
        "为李武立誓明堂，约以共辅"
      ],
      "historicalOutcome": "庐陵还储唐祚不绝",
      "id": "wu_zetian_e4",
      "relationDeltas": rd({"宗室": 10, "士大夫": 8}, {"宗室": -10, "士大夫": -6}, {"宗室": 3, "士大夫": 2}, {"宗室": -4, "士大夫": -3}, {"宗室": 4, "士大夫": 3}),
      "branches": [{"setFlags": ["long_peace"], "clearFlags": ["usurped"]}, {"setFlags": ["usurped"]}, {}, {}, {}],
      "tier": "major"
    },
    {
      "year": 705, "month": 1,
      "title": "神龙政变",
      "description": "帝久疾居长生院，惟张易之、昌宗侍侧，宰相不得见。宰相张柬之与桓彦范、敬晖、崔玄暐、袁恕己结右羽林卫，斩二张于迎仙院庑下，勒兵至长生殿。帝惊起问：谁为乱者？对曰：二张谋反，臣等已诛之。翌日传位太子，复国号唐。",
      "historicalChoice": 0,
      "choices": [
        "传位太子，去帝号复唐",
        "召诸武举兵，与羽林相持",
        "诛张柬之等五王以自保",
        "退居上阳宫而不去帝号",
        "召边将勤王，移驾长安"
      ],
      "historicalOutcome": "二张诛帝禅位唐祚复归",
      "id": "wu_zetian_e5",
      "relationDeltas": rd({"宗室": 6, "士大夫": 6}, {"宗室": -8, "边将": -5}, {"士大夫": -10}, {"宗室": -2, "士大夫": -2}, {"边将": 4, "宗室": -4}),
      "branches": [{"setFlags": ["long_peace"]}, {}, {"setFlags": ["scholar_purge"]}, {}, {}]
    }
  ]
}

d = json.load(open(P, encoding='utf-8'))
emps = d['emperors']
if any(e.get('id') == 'wu_zetian' for e in emps):
    print('已存在，跳过'); sys.exit(0)
# 插到中宗之前（按 reignStart 690 < 705）
idx = next(i for i, e in enumerate(emps) if e.get('id') == 'tang_zongzhong')
emps.insert(idx, WU)
if isinstance(d.get('_meta'), dict):
    d['_meta']['emperorCount'] = len(emps)
with open(P, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print('已插入 wu_zetian 于下标 %d，唐五代君主数 %d' % (idx, len(emps)))
