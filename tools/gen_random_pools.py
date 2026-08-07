# -*- coding: utf-8 -*-
"""
tools/gen_random_pools.py
生成 data/random_pools.js：随机时局（v0.2）事件池。
- 8 个时期桶：shangzhou / qinhan / weijin / tang / song / yuan / ming / qing
- 每桶 calamity(灾) 与 boon(祥瑞) 配对，逐维净漂移≈0（按 baseChanges 计算）
- 总类型数 ≥ 500
- 输出 window.COH_RANDOM_POOLS = {...}

运行：python tools/gen_random_pools.py
"""
import json, os

DIMS = ["treasury", "people", "military", "court", "health", "tech"]

def E(eid, title, kind, major, phase, res, chg, desc, flavor="", comment="", weight=1, unlockTech=False):
    return {
        "id": eid, "title": title, "kind": kind, "major": bool(major),
        "phase": phase, "resilience": res or {},
        "baseChanges": chg, "description": desc,
        "flavor": flavor or ("事出突兀，朝野震动。" if kind == "calamity" else "上天眷佑，四海乂安。"),
        "comment": comment or ("史官谨书，俟后观之。" if kind == "calamity" else "景命维新，可为休祥。"),
        "weight": weight,
        "unlockTech": unlockTech,
    }

POOLS = {}

# ===================== 夏商周 (shangzhou) =====================
s = []
s += [
E("sz_tianming","天命玄鸟","boon",False,None,{},{"people":6,"court":3},"春分玄鸟至，万民以为天命所归，诸侯咸悦。"),
E("sz_hejue","河决孟津","calamity",False,None,{"treasury":"treasury"},{"people":-7,"treasury":-4},"大河决于孟津，禾稼漂没，迁徙者众。"),
E("sz_han","旱魃为虐","calamity",False,None,{"people":"people"},{"people":-8,"treasury":-2},"赤地千里，井泉涸竭，饿殍载道。"),
E("sz_rongdi","戎狄内侵","calamity",False,None,{"military":"military"},{"military":-6,"people":-3},"北狄南下了，边邑被掠，烽火屡惊。"),
E("sz_jishen","祭祀获麟","boon",False,None,{},{"court":5,"people":3},"郊祀获白麟，以为仁兽至，天心可格。"),
E("sz_busi","卜筮大吉","boon",False,None,{},{"court":4,"health":2},"龟筮偕从，宗庙安妥，王心乃豫。"),
E("sz_zhuhou","诸侯来朝","boon",False,None,{},{"court":6,"people":4},"四方诸侯修贄来朝，共尊天子。"),
E("sz_huang","蝗飞蔽天","calamity",False,None,{"people":"people"},{"people":-7,"treasury":-2},"飞蝗蔽天，禾稼俱尽，民多流亡。"),
E("sz_wugu","五谷丰登","boon",False,None,{},{"people":7,"treasury":3},"岁和年丰，廪实而知礼节，野无饿殍。"),
E("sz_hanchao","寒潮伤稼","calamity",False,None,{"people":"people"},{"people":-5,"health":-2},"朔风折稼，稚耋冻馁，药石难继。"),
E("sz_fangguo","方国叛逆","calamity",False,None,{"military":"military"},{"military":-7,"court":-2},"畔国不共王职，干戈相向，王師出征。"),
E("sz_nong","籍田礼成","boon",False,"即位",{},{"people":5,"treasury":2},"王亲耕籍田，率天下先农，兆庶劝课。"),
E("sz_ding","九鼎安稳","boon",False,None,{},{"court":6,"people":3},"鼎彝不移，社稷有凭，讴歌盈野。"),
E("sz_yi","疫气流行","calamity",False,None,{"health":"health"},{"health":-7,"people":-3},"疠疫起，门庭相染，巫医奔走。"),
E("sz_liang","霖雨伤禾","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-2},"积雨连旬，禾烂于亩，饥色在野。"),
E("sz_feng","风调雨顺","boon",False,None,{},{"people":6,"treasury":3},"风雨以时，百谷用成，颂声作矣。"),
E("sz_xing","星陨如雨","calamity",False,None,{"court":"court"},{"court":-5,"health":-1},"星陨如雨，保章氏惧，以为天命将改。"),
E("sz_shou","白雉来翔","boon",False,None,{},{"court":4,"people":3},"越裳献白雉，远方慕义，重译来王。"),
E("sz_shan","山崩壅川","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-3},"山崩壅川，道途阻绝，转运维艰。"),
E("sz_yu","禹河安流","boon",False,None,{},{"treasury":5,"people":4},"九河既导，水患底平，桑土可居。"),
E("sz_zhen","地震坏庐","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-3},"地维震动，墙屋倾颓，民多露处。"),
E("sz_geng","耕织并茂","boon",False,None,{},{"people":6,"treasury":2},"男务耕女务织，布帛菽粟充盈。"),
E("sz_jie","桀纣之戒","calamity",False,"暮年",{"court":"court"},{"court":-6,"people":-2},"闾巷讹言暴主复生，人心惶惶。"),
E("sz_xian","贤辅在位","boon",False,None,{},{"court":6,"people":3},"良弼进谋，王道荡荡，庶政允厘。"),
E("sz_kuang","矿脉新出","boon",False,None,{},{"treasury":6,"people":2},"山出金石，百工兴作，府藏稍实。"),
E("sz_hu","湖泽鱼盐","boon",False,None,{},{"treasury":5,"people":3},"陂池鱼盐之利兴，关市之征足。"),
E("sz_you","游观劳民","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-2},"离宫别馆屡兴，征发不已，农时失所。"),
E("sz_ci","赐胙颁瑞","boon",False,None,{},{"court":4,"people":3},"大飨颁胙，诸侯受瑞，礼成而欢。"),
E("sz_feng2","丰镐繁庶","boon",False,None,{},{"people":6,"court":2},"都邑殷繁，八荒辐辏，歌咏之声达于四境。"),
E("sz_luan","鸾凤来仪","boon",False,None,{},{"court":5,"people":3},"箫韶九成，凤皇来仪，以为至治之应。"),
E("sz_shu","鼠疫横行","calamity",False,None,{"health":"health"},{"health":-6,"people":-2},"鼠耗为殃，疫病随起，阡陌萧然。"),
E("sz_tian","天雨粟米","boon",False,None,{},{"people":7,"treasury":2},"传有天雨嘉谷，虽异事而兆丰。"),
E("sz_bing","冰泮鱼惊","calamity",False,None,{"people":"people"},{"people":-4,"treasury":-1},"春冰早泮，鱼不上 lags，渔者失所。"),
E("sz_li","礼废乐崩","calamity",False,None,{"court":"court"},{"court":-5,"people":-1},"典章寖废，雅颂不闻，僭越时作。"),
E("sz_xian2","贤才汇征","boon",False,None,{},{"court":6,"people":2},"侧席求贤，岩穴之士咸集于朝。"),
E("sz_jie2","节用爱民","boon",False,None,{},{"treasury":3,"people":5},"薄赋敛省浮费，藏富于民，闾阎稍裕。"),
E("sz_yong","庸蜀来王","boon",False,None,{},{"court":4,"military":2},"庸蜀诸戎慕义来享，边徼以宁。"),
E("sz_huang2","荒服不至","calamity",False,None,{"court":"court"},{"court":-4,"military":-2},"荒服诸侯不至，威信稍损。"),
E("sz_nai","蚕丝岁登","boon",False,None,{},{"treasury":4,"people":3},"蚕事既登，缣纩充裕，女红劝矣。"),
E("sz_shou2","兽蹄鸟迹","calamity",False,None,{"people":"people"},{"people":-5,"health":-1},"禽兽逼人，田猎无功，山泽之利耗。"),
E("sz_jing","京观纪功","boon",False,None,{},{"military":5,"court":2},"振旅献俘，告功宗庙，戎心慑服。"),
E("sz_li2","厉鬼为祟","calamity",False,"暮年",{"health":"health"},{"health":-5,"court":-1},"巫觋言厉鬼为祟，宫中惴惴。"),
E("sz_feng3","封建亲贤","boon",False,None,{},{"court":5,"military":2},"封建亲戚，以为蕃屏，宗周赖之。"),
E("sz_tao","陶渔兴利","boon",False,None,{},{"treasury":4,"people":2},"陶渔之利溥，器用不乏，市易以通。"),
E("sz_han2","旱魃再虐","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-2},"连岁不雨，雩祭无应，沟洫尽涸。"),
E("sz_he2","河清献瑞","boon",False,None,{},{"court":5,"people":2},"大河清彻，古以为圣人出之符。"),
E("sz_bing2","兵车闲久","boon",False,None,{},{"military":3,"treasury":2},"久无兵革，马放南山，府库少耗。"),
E("sz_yi2","夷夏杂处","calamity",False,None,{"court":"court"},{"court":-4,"people":-1},"夷夏错居，礼俗相妨，讼狱繁兴。"),
E("sz_jia","嘉禾合穗","boon",False,None,{},{"people":6,"court":1},"嘉禾同颖，以为太平之符，荐于宗庙。"),
E("sz_tai","泰运方隆","boon",False,None,{},{"court":4,"people":4},"时和岁丰，上下交泰，颂声洋溢。"),
E("sz_xiong","凶荒荐臻","calamity",False,None,{"people":"people"},{"people":-7,"treasury":-3},"水旱继作，凶荒荐臻，赈赡不给。"),
E("sz_xuan","宣室求贤","boon",False,None,{},{"court":5,"people":2},"坐宣室而访道，俊乂在官，百度惟贞。"),
E("sz_man","蛮荆来威","boon",False,None,{},{"military":5,"court":2},"蛮荆既威，南服底定，师旅言旋。"),
E("sz_diao","凋瘵未苏","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-2},"疮痍未复，凋瘵满目，流冗未归。"),
E("sz_fu","苻瑞丛集","boon",False,None,{},{"court":5,"people":3},"芝草生庭，神雀集幕，符瑞丛集。"),
E("sz_li3","力役繁重","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-1},"城浚池筑，力役繁兴，农不得休。"),
E("sz_de","德音遐宣","boon",False,None,{},{"court":4,"people":4},"德音不瑕，四方风动，远人向化。"),
E("sz_jian","俭约率下","boon",False,None,{},{"treasury":4,"people":3},"衣帛食肉有节，俭约之风行于上下。"),
E("sz_huo","火灾延燔","calamity",False,None,{"treasury":"treasury"},{"treasury":-6,"people":-2},"廪庾不戒于火，积粟延燔，饥备陡虚。"),
E("sz_shun","舜风被野","boon",False,None,{},{"people":6,"court":2},"孝悌力田，舜风被野，比屋可封。"),
E("sz_gou","沟洫既潴","boon",False,None,{},{"treasury":3,"people":4},"沟洫修而水利通，潦不为患，稼穑乃登。"),
E("sz_yao","瑶台虚耗","calamity",False,None,{"treasury":"treasury"},{"treasury":-5,"people":-2},"琼台瑶室之役频，帑藏虚耗，民力殚矣。"),
]
POOLS["shangzhou"] = s

# ===================== 秦汉 (qinhan) =====================
q = []
q += [
E("qh_chidi","匈奴犯边","calamity",False,None,{"military":"military"},{"military":-7,"people":-3,"treasury":-3},"匈奴入寇，杀略吏民，烽火达于甘泉。"),
E("qh_feng","关中丰熟","boon",False,None,{},{"people":6,"treasury":3},"关中大熟，太仓充溢，罢癃得养。"),
E("qh_zhi","驰道初成","boon",False,None,{},{"military":4,"treasury":2},"驰道通九州，师旅转输捷于往昔。"),
E("qh_fen","焚书议起","calamity",False,None,{"court":"court"},{"court":-6,"people":-2},"燔诗书百家语，儒生悒悒，谤讟潜生。"),
E("qh_he","河决瓠子","calamity",False,None,{"treasury":"treasury"},{"people":-7,"treasury":-5},"河决瓠子，注巨野，梁楚之地皆为壑。"),
E("qh_kan","垦田日广","boon",False,None,{},{"people":6,"treasury":2},"实边垦田，陌阡弥望，流民著籍。"),
E("qh_yi","疫疠时起","calamity",False,None,{"health":"health"},{"health":-6,"people":-3},"时疫流行，军屯多陨，转饷屡乏。"),
E("qh_xian","贤良对策","boon",False,None,{},{"court":6,"people":2},"诏举贤良，对策殿廷，治术稍振。"),
E("qh_fu","复除徭赋","boon",False,None,{},{"treasury":-2,"people":6},"赦除宿负，复其徭赋，黔首少苏。"),
E("qh_lu","漕粟艰难","calamity",False,None,{"treasury":"treasury"},{"treasury":-5,"people":-2},"漕挽阻远，关东之粟难继京师。"),
E("qh_nan","南越内附","boon",False,None,{},{"court":5,"military":2},"南越王请为藩臣，岭表悉平。"),
E("qh_zai","灾异屡见","calamity",False,None,{"court":"court"},{"court":-5,"health":-1},"日食星孛相继，博士言阴阳失和。"),
E("qh_cang","常平仓立","boon",False,None,{},{"people":5,"treasury":2},"设常平仓，谷贱则籴贵则粜，民无菜色。"),
E("qh_xing","星孛长空","calamity",False,None,{"court":"court"},{"court":-4,"health":-1},"彗星见东方，术士以为兵革之象。"),
E("qh_shu","疏河安流","boon",False,None,{},{"treasury":4,"people":4},"塞瓠子决河，梁楚复为沃壤。"),
E("qh_li","吏治澄清","boon",False,None,{},{"court":5,"people":3},"二千石皆良吏，囹圄空虚，盗贼衰息。"),
E("qh_kou","流民就食","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-2},"关东流民填塞道路，鬻子以食。"),
E("qh_jian","减租劝农","boon",False,None,{},{"treasury":-2,"people":6},"三十税一，力田者众，野无旷土。"),
E("qh_bing","并海盐饶","boon",False,None,{},{"treasury":6,"people":2},"煮海为盐，笼山为钱，国用乃饶。"),
E("qh_huo","火焚都仓","calamity",False,None,{"treasury":"treasury"},{"treasury":-6,"people":-2},"太仓不戒于火，红腐之粟半为灰烬。"),
E("qh_lu2","鲁壁藏书","boon",False,None,{},{"court":4,"people":2},"坏壁得古文，经术复明，儒林称庆。"),
E("qh_xiong","凶年罢祭","calamity",False,None,{"people":"people"},{"people":-5,"court":-1},"岁凶礼废，粢盛不备，群祀权停。"),
E("qh_tun","屯田实边","boon",False,None,{},{"military":5,"treasury":1},"戍卒屯田，且耕且守，转输之费省。"),
E("qh_qiang","羌乱陇右","calamity",False,None,{"military":"military"},{"military":-6,"people":-2},"诸羌叛于陇右，护羌校尉战不利。"),
E("qh_li2","礼官议制","boon",False,None,{},{"court":5,"people":2},"定礼制正法度，章程粲然，海内望风。"),
E("qh_shui","水衡钱足","boon",False,None,{},{"treasury":5,"people":2},"水衡都尉理财有方，禁钱充溢。"),
E("qh_you","游徼失政","calamity",False,None,{"court":"court"},{"court":-4,"people":-2},"亭徼废弛，盗贼公行，闾里不安。"),
E("qh_jiao","郊祀雍畤","boon",False,None,{},{"court":4,"health":2},"亲郊雍畤，荐馨享德，神人胥悦。"),
E("qh_jian2","谏争盈庭","calamity",False,"壮年",{"court":"court"},{"court":-5,"health":-1},"大夫数廷争，上意不怿，中外惶惧。"),
E("qh_cang2","仓储丰羡","boon",False,None,{},{"treasury":5,"people":4},"太仓粟红腐，郡国廪庾皆满。"),
E("qh_li3","厉疫再作","calamity",False,None,{"health":"health"},{"health":-5,"people":-2},"时气复发，老幼相枕而死。"),
E("qh_xiu","秀材辈出","boon",False,None,{},{"court":5,"people":2},"学校兴，秀材辈出，风化翕然。"),
E("qh_shu2","属国安辑","boon",False,None,{},{"military":4,"court":2},"置属国以处降胡，烽燧少警。"),
E("qh_fa","法网稍密","calamity",False,None,{"court":"court"},{"court":-4,"people":-2},"律令滋章，赭衣塞路，小民易犯。"),
E("qh_ben","本业兴殖","boon",False,None,{},{"people":6,"treasury":2},"重本抑末，农桑并茂，末技稍戢。"),
E("qh_jie","节驿省费","boon",False,None,{},{"treasury":4,"people":2},"邮驿简省，传车稀发，疲民得息。"),
E("qh_huang","黄老清净","boon",False,None,{},{"court":4,"people":4},"无为而治，与民休息，刑罚大省。"),
E("qh_zhan","战乱初平","calamity",False,None,{"military":"military"},{"military":-6,"people":-3},"干戈乍息，疮痍满目，丁壮凋零。"),
E("qh_feng2","丰沛故旧","boon",False,None,{},{"court":4,"people":3},"褒录功宗，故旧咸秩，宗亲辑睦。"),
E("qh_li4","吏惰民偷","calamity",False,None,{"court":"court"},{"court":-4,"people":-1},"长吏因循，案牍山积，奸弊滋生。"),
E("qh_jiao2","椒房戚里","calamity",False,"暮年",{"court":"court"},{"court":-5,"treasury":-2},"外戚用事，恩泽侯者众，府库为耗。"),
E("qh_tian","田租轻减","boon",False,None,{},{"treasury":-2,"people":6},"屡减田租，农夫乐业，畎亩增辟。"),
E("qh_shan","山泽之禁","calamity",False,None,{"people":"people"},{"people":-4,"treasury":-1},"禁山泽陂池，樵采渔钓皆罪，民失其资。"),
E("qh_wu","武备修举","boon",False,None,{},{"military":5,"court":2},"讲武肄射，楼船缮完，边备孔固。"),
E("qh_di","狄道不靖","calamity",False,None,{"military":"military"},{"military":-5,"people":-2},"西陲小丑跳梁，凉州驿骚。"),
E("qh_ru","儒术大兴","boon",False,None,{},{"court":5,"people":3},"表章六经，置博士弟子，儒术遂昌。"),
E("qh_cang3","仓庾告罄","calamity",False,None,{"treasury":"treasury"},{"treasury":-6,"people":-2},"水旱相仍，太仓见底，平粜无米。"),
E("qh_fu2","赋均田平","boon",False,None,{},{"people":5,"treasury":2},"限民名田，兼并稍戢，细民有恒产。"),
E("qh_jing","京畿安堵","boon",False,None,{},{"court":4,"people":3},"辇毂之下盗息，编户安堵，讼狱稀简。"),
E("qh_han","旱涝叠更","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-2},"先潦后旱，再更其虐，播种失时。"),
E("qh_de","德泽旁流","boon",False,None,{},{"people":6,"court":2},"鳏寡孤独养济有政，德泽流于穷阎。"),
E("qh_gong","功令严明","boon",False,None,{},{"court":4,"military":2},"课最赏罚信，百司震肃，事无留滞。"),
E("qh_yao","徭戍道远","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-1},"谪戍万里，道毙者多，闾左骚动。"),
E("qh_shou","寿考作人","boon",False,"暮年",{},{"health":4,"people":2},"耆老稠叠，黄发儿齿者多，以为仁寿之征。"),
E("qh_zhen","振贷贫乏","boon",False,None,{},{"treasury":-3,"people":6},"发仓廪振贫民，全活甚众。"),
E("qh_li5","蠹吏侵渔","calamity",False,None,{"court":"court"},{"court":-4,"people":-2},"豪右交通县官，侵渔细民，怨声载路。"),
]
POOLS["qinhan"] = q

# ===================== 三国两晋南北朝隋 (weijin) =====================
w = []
w += [
E("wj_hu","胡骑南下","calamity",False,None,{"military":"military"},{"military":-7,"people":-3},"八王既乱，胡羯乘衅，中原鼎沸。"),
E("wj_nan","南渡衣冠","boon",False,None,{},{"court":5,"people":3},"士族南奔，江左立国，文物赖以不坠。"),
E("wj_liang","粮运阻绝","calamity",False,None,{"treasury":"treasury"},{"treasury":-5,"military":-2},"运道梗阻，军无见粮，士气沮丧。"),
E("wj_jing","荆州丰稔","boon",False,None,{},{"people":6,"treasury":2},"荆州沃壤岁登，转输上流，师旅不乏。"),
E("wj_rong","戎虏互市","boon",False,None,{},{"treasury":4,"military":2},"开关互市，驼马络绎，边患以纾。"),
E("wj_yi","时疫军中","calamity",False,None,{"health":"health"},{"health":-6,"military":-2},"疫气入营，将卒枕藉，锐气大损。"),
E("wj_qing","清谈误政","calamity",False,None,{"court":"court"},{"court":-5,"people":-1},"虚无放诞，尸位者众，庶务浸废。"),
E("wj_tun","屯田淮上","boon",False,None,{},{"military":5,"treasury":1},"且耕且守于淮，兵民两利，北顾少忧。"),
E("wj_shui","水军练成","boon",False,None,{},{"military":5,"court":1},"楼船习战，蒙冲连舳，长江天堑益固。"),
E("wj_han","旱蝗并作","calamity",False,None,{"people":"people"},{"people":-7,"treasury":-2},"旱蝗继至，中州萧条，人相食。"),
E("wj_fo","佛图大盛","boon",False,None,{},{"court":4,"people":3},"塔庙相望，译经渐广，风俗稍安。"),
E("wj_zha","佞幸用事","calamity",False,None,{"court":"court"},{"court":-6,"people":-2},"近习弄权，忠良见疏，朝纲日紊。"),
E("wj_liang2","良守抚民","boon",False,None,{},{"court":4,"people":5},"廉守在郡，劝课农桑，流亡复业。"),
E("wj_xiong","凶奴陷城","calamity",True,None,{"military":"military"},{"military":-10,"people":-5,"treasury":-3},"羯胡陷一郡，守将死之，烽燧照宫阙。"),
E("wj_jian","减赋安流","boon",False,None,{},{"treasury":-2,"people":6},"蠲流民之赋，给复十年，荆棘生而人户增。"),
E("wj_zen","甑釜生尘","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-2},"连岁军兴，甑釜屡空，菜色在道。"),
E("wj_shan","善政兴学","boon",False,None,{},{"court":4,"people":3},"立学官养士，弦诵之声达于里巷。"),
E("wj_qi","畿甸清晏","boon",False,None,{},{"court":4,"people":3},"辇毂无警，市不易肆，黎庶乐业。"),
E("wj_luan","乱兵剽掠","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-2},"散卒为盗，村落被掠，保聚艰难。"),
E("wj_he","河清见底","boon",False,None,{},{"court":4,"people":2},"黄河数度澄清，时人以为休明之符。"),
E("wj_wen","文教蔚然","boon",False,None,{},{"court":5,"people":2},"文章藻丽，人物风流，江左风尚冠绝。"),
E("wj_bing","冰合渡师","boon",False,None,{},{"military":5,"court":1},"天寒冰合，师得飞渡，奇功可立。"),
E("wj_zai","灾祥杂糅","calamity",False,None,{"court":"court"},{"court":-4,"health":-1},"彗孛经天，太史频奏，朝野汹惧。"),
E("wj_tian","田庐渐复","boon",False,None,{},{"people":5,"treasury":2},"招怀离散，田庐粗复，鸡犬相闻。"),
E("wj_jie","羯寇再逼","calamity",False,None,{"military":"military"},{"military":-6,"people":-2},"羯勒复寇，边亭日骇，征调不休。"),
E("wj_chan","禅代有礼","boon",False,None,{},{"court":5,"people":2},"禅让从容，赦书广被，鼎革少血刃。"),
E("wj_seng","僧尼赈饥","boon",False,None,{},{"people":5,"treasury":1},"寺观设粥，全活饿殍，慈悲之名远播。"),
E("wj_hu2","胡汉杂处","calamity",False,None,{"court":"court"},{"court":-4,"people":-1},"错居猜嫌，衅端时启，吏不能禁。"),
E("wj_du","度田均赋","boon",False,None,{},{"people":4,"treasury":3},"校核田亩，赋役稍均，豪强敛手。"),
E("wj_you","游军劫粮","calamity",False,None,{"treasury":"treasury"},{"treasury":-5,"military":-1},"游骑截粮道，积粟委敌，士有饥色。"),
E("wj_feng","烽燧肃清","boon",False,None,{},{"military":4,"court":2},"斥候严明，烽燧不惊，边庭宁谧。"),
E("wj_li2","吏治颓坏","calamity",False,None,{"court":"court"},{"court":-4,"people":-2},"纲纪纵弛，墨吏横行，民不堪命。"),
E("wj_shu","著述繁兴","boon",False,None,{},{"court":4,"people":1},"史汉注疏迭出，典籍大备，儒林称盛。"),
E("wj_can","残破未起","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-2},"兵燹之余，井邑丘墟，绥抚无力。"),
E("wj_jian2","俭素化下","boon",False,None,{},{"treasury":3,"people":4},"抑奢靡尚俭素，府库稍充，风化归厚。"),
E("wj_nu","奴婢逃亡","calamity",False,None,{"people":"people"},{"people":-4,"treasury":-1},"蓄奴之家多叛亡，庄园凋落，佃作失时。"),
E("wj_fo2","浮图成灾","calamity",False,None,{"treasury":"treasury"},{"treasury":-5,"court":-1},"造像穷极工巧，倾帑以奉，农桑坐废。"),
E("wj_shui2","水利修复","boon",False,None,{},{"people":5,"treasury":2},"修陂塘通灌溉，亢旱有备，岁乃中熟。"),
E("wj_bing2","兵甲朽蠹","calamity",False,None,{"military":"military"},{"military":-5,"court":-1},"承平日久，甲兵朽蠹，猝有警则张皇。"),
E("wj_xian","贤王保境","boon",False,None,{},{"court":4,"military":3},"宗王镇藩，抚御得宜，一方安堵。"),
E("wj_li3","流民南附","boon",False,None,{},{"people":5,"court":1},"中州流人相率南来，编户日增，墝埆尽辟。"),
E("wj_zhen","振穷恤孤","boon",False,None,{},{"treasury":-2,"people":6},"开仓赡穷，存问孤寡，和气充塞。"),
E("wj_jing2","京邑再火","calamity",False,None,{"treasury":"treasury"},{"treasury":-5,"people":-2},"建康火作，庐舍荡尽，商旅裹足。"),
E("wj_wen2","文武功全","boon",False,None,{},{"court":4,"military":3},"朝有谋臣野有战将，内外恃以无恐。"),
E("wj_hu3","胡酋内附","boon",False,None,{},{"military":4,"court":2},"部落率众归化，列置郡县，边患寖息。"),
E("wj_sui","隋文混一","boon",True,None,{"military":"military"},{"military":8,"court":5,"people":4},"天步将泰，区宇渐一，黎庶引领。"),
E("wj_yun","运河初凿","boon",False,None,{},{"treasury":3,"people":4},"广通渠成，关河转运便，南粮北输。"),
E("wj_li4","礼崩乐坏","calamity",False,None,{"court":"court"},{"court":-4,"people":-1},"雅乐零落，朝会无仪，识者忧之。"),
E("wj_can2","残虐失民","calamity",False,"暮年",{"court":"court"},{"court":-5,"people":-3},"赋重役烦，民心思变，揭竿者众。"),
E("wj_feng2","风谣颂平","boon",False,None,{},{"people":5,"court":2},"里巷作歌颂太平，熙熙然有元气。"),
]
POOLS["weijin"] = w

# ===================== 隋唐五代 (tang) =====================
t = []
t += [
E("tg_locust","蝗灾","calamity",False,None,{"people":"people"},{"people":-7,"treasury":-2},"飞蝗蔽天，禾稼俱尽，饿殍载道。"),
E("tg_river","黄河决口","calamity",False,None,{"treasury":"treasury"},{"people":-5,"treasury":-4},"河决于棣，注巨野，梁宋化为壑。"),
E("tg_plague","疫病","calamity",False,None,{"health":"health"},{"health":-7,"people":-3},"疠气流行，闾巷相染，医巫奔走。"),
E("tg_raid","边衅","calamity",False,None,{"military":"military"},{"military":-6,"people":-2},"小羌窃发，亭障数惊，转饷稍劳。"),
E("tg_tujue","突厥大入","calamity",True,None,{"military":"military"},{"military":-10,"people":-4,"treasury":-3},"突厥入寇，烽燧照甘泉，边将失利。"),
E("tg_star","星变","calamity",False,None,{"court":"court"},{"court":-5,"health":-1},"彗孛经天，司天奏变法度，上心忧勤。"),
E("tg_fire","宫中火灾","calamity",False,None,{"treasury":"treasury"},{"treasury":-5,"people":-1},"禁中失火，掖廷延燔，帑藏小损。"),
E("tg_refugee","流民就食","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-2},"关辅饥民累累就食，鬻子满路。"),
E("tg_harvest","丰年","boon",False,None,{},{"people":8,"treasury":3},"元气既复，岁乃大熟，野无饿莩。"),
E("tg_omens","祥瑞","boon",False,None,{},{"court":6,"people":3},"符瑞丛集，芝草生庭，史馆书之。"),
E("tg_trade","商旅通畅","boon",False,None,{},{"treasury":4,"people":2},"舟车所至，货殖流通，关市之征足。"),
E("tg_caoyun","漕运通畅","boon",False,None,{},{"treasury":3,"people":1},"汴渠通利，东南之粟日至，太仓有继。"),
E("tg_market","互市","boon",False,None,{},{"military":8,"treasury":2},"互市于缘边，驼马入贡，戎心易驯。"),
E("tg_medicine","太医效验","boon",False,None,{},{"health":8,"people":2},"医学署奏效，时疫寻止，老幼得全。"),
E("tg_win","边功","boon",False,None,{},{"military":8,"court":1},"偏师克捷，虏帐徙遁，北门稍安。"),
E("tg_granary","义仓丰储","boon",False,None,{},{"people":8,"treasury":3},"义仓充溢，凶年可赈，民无菜色。"),
E("tg_remit","蠲租诏下","boon",False,None,{},{"treasury":-3,"people":6},"诏蠲逋租，疲甿得苏，歌咏载路。"),
E("tg_temple","寺观兴造","calamity",False,None,{"treasury":"treasury"},{"treasury":-5,"court":-1},"造寺穷丽，度僧无算，农桑坐废。"),
E("tg_flood2","霖潦伤稼","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-2},"积雨连月，陇亩淹没，秋成失望。"),
E("tg_plain","太平颂声","boon",False,None,{},{"court":5,"people":4},"海内乂安，路不拾遗，颂声洋溢。"),
E("tg_rebel","盗起山林","calamity",False,None,{"military":"military"},{"military":-5,"people":-2},"逃户相聚为盗，州郡讨之未平。"),
E("tg_exam","贡举得人","boon",False,None,{},{"court":6,"people":2},"礼闱得士，草茅登科，文治浸兴。"),
E("tg_frontier","藩镇效顺","boon",False,None,{},{"court":4,"military":4},"节将入朝，献版图马匹，朝廷威重。"),
E("tg_drought2","井泉涸竭","calamity",False,None,{"people":"people"},{"people":-5,"health":-1},"亢阳不雨，井泉涸，汲远劳弊。"),
E("tg_canton","岭南献琛","boon",False,None,{},{"treasury":5,"court":2},"岭南献犀象珠贝，舶货充府藏。"),
E("tg_quake","地动坏城","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-2},"地震坏城郭庐舍，压溺者众。"),
E("tg_farm","屯田丰殖","boon",False,None,{},{"military":5,"treasury":2},"营田既登，兵食自足，省转输之费。"),
E("tg_eunuch","宦者预政","calamity",False,None,{"court":"court"},{"court":-5,"people":-1},"中官渐预朝权，宰相奏事多沮。"),
E("tg_audit","黜陟分明","boon",False,None,{},{"court":5,"people":3},"考课精核，贪墨者贬，循吏显擢。"),
E("tg_border2","回纥助顺","boon",False,None,{},{"military":6,"court":1},"回纥遣兵助讨，戎捷屡闻。"),
E("tg_poor","贫窭流散","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-1},"赋重民贫，邑里流散，籍减半矣。"),
E("tg_river2","河清献寿","boon",False,None,{},{"court":4,"people":2},"河清千里，群臣上寿，以为圣德所感。"),
E("tg_li2","吏治澄清","boon",False,None,{},{"court":5,"people":3},"良二千石在郡，盗息讼简，民用和睦。"),
E("tg_warlord","骄将跋扈","calamity",False,None,{"military":"military"},{"military":-4,"court":-2},"藩帅稍骄，拒命不时，尾大之患萌。"),
E("tg_silk","蚕织岁登","boon",False,None,{},{"treasury":4,"people":3},"蚕丝之利倍常，缣帛充斥关市。"),
E("tg_plague2","时气再作","calamity",False,None,{"health":"health"},{"health":-5,"people":-2},"温疫复行，监狱多囚染，恤刑未遍。"),
E("tg_chan","禅寺钟鼓","boon",False,None,{},{"court":3,"people":3},"名刹讲经，士女云集，风教稍和。"),
E("tg_famine","粟价腾踊","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-1},"粟价翔贵，贫者不能自存，道殣相望。"),
E("tg_canal","渠道溉田","boon",False,None,{},{"people":5,"treasury":2},"决渠灌田，亢旱有备，亩收倍常。"),
E("tg_party","朋党相攻","calamity",False,None,{"court":"court"},{"court":-5,"people":-1},"牛李分朋，论奏相轧，庶政牵制。"),
E("tg_envoy","四夷来朝","boon",False,None,{},{"court":5,"people":2},"新罗渤海遣使修贡，冠盖相望。"),
E("tg_store","太仓红腐","boon",False,None,{},{"treasury":5,"people":3},"太仓陈陈相因，红腐不可较，府藏殷实。"),
E("tg_bandit","海寇掠商","calamity",False,None,{"treasury":"treasury"},{"treasury":-4,"people":-2},"海隅群盗掠市舶，番商裹足。"),
E("tg_tea","茶税充盈","boon",False,None,{},{"treasury":4,"people":1},"榷茶之利兴，岁时入倍，用度少窘。"),
E("tg_flood3","江淮水潦","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-2},"江淮并涨，田庐漂没，漕运亦梗。"),
E("tg_li3","礼官议礼","boon",False,None,{},{"court":4,"people":2},"修订礼典，郊庙有仪，文物粲然。"),
E("tg_reform","新政初布","boon",False,None,{},{"court":4,"people":3},"厘百司之弊，条教焕然，中外向风。"),
E("tg_tujue2","突厥请和","boon",False,None,{},{"military":6,"court":2},"突厥遣使请和，输马纳款，烽燧少警。"),
E("tg_star2","山崩石裂","calamity",False,None,{"court":"court"},{"court":-4,"health":-1},"华山崩，石裂有声，太史言阴盛。"),
E("tg_bumper","两河丰稔","boon",False,None,{},{"people":6,"treasury":2},"河南河北皆大熟，流亡复归，阡陌尽辟。"),
E("tg_eunuch2","阉竖弄权","calamity",False,"暮年",{"court":"court"},{"court":-5,"treasury":-2},"北司权重，废置天子如弈棋，社稷将危。"),
E("tg_silk2","织染精巧","boon",False,None,{},{"treasury":4,"people":2},"织染署巧丽逾前，蕃客争市，利入增倍。"),
E("tg_rebel2","藩镇构兵","calamity",True,None,{"military":"military"},{"military":-9,"people":-4,"court":-2},"骄帅称兵，连衡数镇，中原复沸。"),
E("tg_pardon","大赦覃恩","boon",False,None,{},{"court":4,"people":4},"肆赦罪囚，旌表门闾，欢心大洽。"),
]
POOLS["tang"] = t

# ===================== 宋辽金夏 (song) =====================
g = []
g += [
E("sg_liao","辽骑南下","calamity",False,None,{"military":"military"},{"military":-7,"people":-3,"treasury":-2},"辽师入寇，边书告急，岁币之议复起。"),
E("sg_feng","两浙丰登","boon",False,None,{},{"people":7,"treasury":3},"两浙圩田大熟，米舟蔽江，物价乃平。"),
E("sg_dang","党争迭起","calamity",False,None,{"court":"court"},{"court":-6,"people":-1},"新旧之党交攻，奏疏相诋，政事几废。"),
E("sg_sui","岁币议成","boon",False,None,{},{"court":4,"treasury":-3},"输币息民，边氛暂戢，生灵免锋镝。"),
E("sg_he","黄河决曹","calamity",False,None,{"treasury":"treasury"},{"people":-6,"treasury":-5},"河决曹村，注梁山泊，京东皆为壑。"),
E("sg_keju","科举得士","boon",False,None,{},{"court":6,"people":2},"礼部放榜，寒畯登科，文运方隆。"),
E("sg_yi","疫起京师","calamity",False,None,{"health":"health"},{"health":-6,"people":-2},"时疫作于京师，太医局施药，死者犹众。"),
E("sg_shi","市舶殷盛","boon",False,None,{},{"treasury":6,"people":2},"番舶至者倍常，乳香犀象之利充府。"),
E("sg_famine","米价踊贵","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-1},"连歉米踊贵，贫民枵腹，盗刼时闻。"),
E("sg_xining","新法颁行","boon",False,None,{},{"court":4,"treasury":3},"理财诸法次第行，府库稍实，议论亦兴。"),
E("sg_xia","西夏犯边","calamity",False,None,{"military":"military"},{"military":-6,"people":-2,"treasury":-2},"夏人寇环庆，堡寨多陷，调发旁午。"),
E("sg_cang","义仓备荒","boon",False,None,{},{"people":6,"treasury":2},"诸路义仓积谷，凶岁可赈，民志以定。"),
E("sg_zhai","灾异数见","calamity",False,None,{"court":"court"},{"court":-5,"health":-1},"日蚀星变相继，谏官言时政阙失。"),
E("sg_yue","岳祠封祀","boon",False,None,{},{"court":4,"health":1},"东封西祀，祥瑞纷陈，颂声作于郡国。"),
E("sg_jin","金人渝盟","calamity",True,None,{"military":"military"},{"military":-10,"people":-5,"court":-2},"金人败盟南下，边将望风，两河震骇。"),
E("sg_nan","南渡驻跸","boon",False,None,{},{"court":5,"people":3},"六飞南渡，行在粗安，人心稍定。"),
E("sg_yun","运河通漕","boon",False,None,{},{"treasury":4,"people":2},"疏汴通漕，东南粟麦达于行在。"),
E("sg_li","吏惰案积","calamity",False,None,{"court":"court"},{"court":-4,"people":-2},"州县因循，滞狱山积，冤抑莫伸。"),
E("sg_fu","富商大贾","boon",False,None,{},{"treasury":5,"people":2},"通商惠工，泉布流衍，关市之入日广。"),
E("sg_bing","冰合渡江","boon",False,None,{},{"military":5,"court":1},"天寒冰合，师徒得济，恢复有期。"),
E("sg_han","旱蝗仍岁","calamity",False,None,{"people":"people"},{"people":-7,"treasury":-2},"仍岁旱蝗，赤地千里，人至相食。"),
E("sg_xue","学校丕兴","boon",False,None,{},{"court":5,"people":2},"州县皆置学，教养兼施，风俗归厚。"),
E("sg_jian","减租恤农","boon",False,None,{},{"treasury":-2,"people":6},"下宽大之诏，损上益下，农亩劝矣。"),
E("sg_fan","蕃部惊扰","calamity",False,None,{"military":"military"},{"military":-5,"people":-1},"蕃部小不安，亭障微警，措置未定。"),
E("sg_li2","理财得宜","boon",False,None,{},{"treasury":5,"court":1},"会计精明，无滥支之费，用度乃裕。"),
E("sg_zhe","折变病民","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-1},"杂变之征无名，输纳倍称，细民困毙。"),
E("sg_xi","西鄙受降","boon",False,None,{},{"military":6,"court":1},"边将纳降，城寨复归，烽燧少警。"),
E("sg_fo","佛老并崇","boon",False,None,{},{"court":3,"people":2},"寺观崇奉，斋醮屡行，民俗以安。"),
E("sg_luan","乱兵焚掠","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-2},"溃卒为乱，焚掠村聚，保聚维艰。"),
E("sg_he2","河清献瑞","boon",False,None,{},{"court":4,"people":1},"大河澄清，史臣书瑞，廷臣上表。"),
E("sg_wen","文治蔚然","boon",False,None,{},{"court":5,"people":2},"儒先辈出，经术文章为后世宗。"),
E("sg_jin2","金价腾踊","calamity",False,None,{"treasury":"treasury"},{"treasury":-5,"people":-2},"楮币浸轻，物价腾踊，公私交困。"),
E("sg_tun","营田垦荒","boon",False,None,{},{"military":4,"people":3},"募兵垦荒，且耕且守，边储稍实。"),
E("sg_zhi","制举直言","boon",False,None,{},{"court":5,"people":2},"诏求直言，草茅得尽所怀，治道有益。"),
E("sg_li3","蠹吏为奸","calamity",False,None,{"court":"court"},{"court":-4,"people":-2},"猾胥舞文，隐蔽田赋，贫者重困。"),
E("sg_yao","徭赋繁重","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-1},"夫役骈兴，春不得耕，秋不得获。"),
E("sg_shan","善政绥怀","boon",False,None,{},{"court":4,"people":4},"良守令拊循，流亡复业，鸡犬相闻。"),
E("sg_jin3","金使要盟","calamity",False,None,{"court":"court"},{"court":-5,"treasury":-2},"强敌索衅，要盟城下，国体少损。"),
E("sg_si","私盐充斥","calamity",False,None,{"treasury":"treasury"},{"treasury":-4,"people":-1},"私贩横行，榷利大损，捕之急则变。"),
E("sg_yu","御前画学","boon",False,None,{},{"court":3,"people":2},"画院待诏，艺事精绝，四方风慕。"),
E("sg_zhen","振赡饥鸿","boon",False,None,{},{"treasury":-3,"people":6},"发廪振饥，全活以万计，和气充塞。"),
E("sg_feng2","风谣颂平","boon",False,None,{},{"people":5,"court":2},"里巷作歌颂承平，熙熙然有元气。"),
E("sg_xia2","夏国请和","boon",False,None,{},{"military":5,"court":1},"夏人遣使修贡，边亭息警。"),
E("sg_zai","灾伤检放","boon",False,None,{},{"treasury":-2,"people":5},"灾伤蠲其租，不使流离，仁声远播。"),
E("sg_li4","礼文繁缛","calamity",False,None,{"court":"court"},{"court":-3,"treasury":-1},"议礼纷纷，文具寖盛，实惠或少。"),
E("sg_tai","太仓充溢","boon",False,None,{},{"treasury":5,"people":3},"诸路上供足，太仓盈羡，岁计有羡。"),
E("sg_huang","蝗越淮界","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-1},"飞蝗渡淮，淮甸告饥，捕瘗不给。"),
E("sg_chan","禅讲盛行","boon",False,None,{},{"court":3,"people":2},"禅宗讲席遍山林，缁素向风。"),
E("sg_jian2","俭约省费","boon",False,None,{},{"treasury":4,"people":3},"宫禁省约，不兴土木，民力少宽。"),
E("sg_bing2","冰消舟阻","calamity",False,None,{"treasury":"treasury"},{"treasury":-3,"people":-1},"春冰早泮，漕舟胶滞，上供后期。"),
E("sg_xi2","熙丰遗法","calamity",False,None,{"court":"court"},{"court":-4,"people":-1},"绍述之说行，异议者斥，党祸再萌。"),
E("sg_wu","武备讲明","boon",False,None,{},{"military":5,"court":1},"修武备整师律，器械精利，边声稍壮。"),
E("sg_can","残破未苏","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-2},"兵火之余，井邑萧条，绥抚未遑。"),
]
POOLS["song"] = g

# ===================== 元 (yuan) =====================
y = []
y += [
E("yn_flood","河决北流","calamity",False,None,{"treasury":"treasury"},{"people":-6,"treasury":-5},"河决北徙，没民田庐，赈役旁午。"),
E("yn_pasture","马政蕃息","boon",False,None,{},{"military":6,"treasury":1},"孳息蕃马，太仆闲厩充牣，兵势益张。"),
E("yn_revolt","盗起齐鲁","calamity",False,None,{"military":"military"},{"military":-6,"people":-3},"红巾啸聚，州郡失守，羽檄交驰。"),
E("yn_grain","海运通达","boon",False,None,{},{"treasury":5,"people":2},"海运粮艘达直沽，京师廪实，罢河运之劳。"),
E("yn_plague","大疫","calamity",True,None,{"health":"health"},{"health":-8,"people":-4},"疠气大行，都邑为空，医药莫救。"),
E("yn_trade","舶商辐辏","boon",False,None,{},{"treasury":6,"people":2},"番舶集泉广，珠贝珍异之利充府。"),
E("yn_drought","连岁亢旱","calamity",False,None,{"people":"people"},{"people":-7,"treasury":-2},"赤地连年，禾稼尽槁，人相食。"),
E("yn_pacify","边徼宁谧","boon",False,None,{},{"military":5,"court":2},"宗王就藩，朔漠少警，烽燧不惊。"),
E("yn_corrupt","赃吏横行","calamity",False,None,{"court":"court"},{"court":-5,"people":-2},"墨吏满前，括财无艺，黎庶怨咨。"),
E("yn_canal","通惠河成","boon",False,None,{},{"treasury":4,"people":3},"通惠河成，漕舟入都城，贸迁便甚。"),
E("yn_star","彗长竟天","calamity",False,None,{"court":"court"},{"court":-4,"health":-1},"彗出西方，太史频奏，中外汹惧。"),
E("yn_audit","考课稍明","boon",False,None,{},{"court":4,"people":3},"厘冗官明黜陟，宿弊少革。"),
E("yn_rebel","叛乱相仍","calamity",True,None,{"military":"military"},{"military":-9,"people":-4,"treasury":-2},"诸道并叛，省台征讨无功，社稷摇矣。"),
E("yn_herd","牧地广阔","boon",False,None,{},{"military":5,"treasury":1},"牧场弥望，马驼羊只以千万计，军用饶。"),
E("yn_famine","粟贵如珠","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-1},"饥馑荐臻，斗米余篇，殍殣盈途。"),
E("yn_charity","义仓赈饥","boon",False,None,{},{"people":6,"treasury":2},"发义廪振饥，全活甚众，凶不为害。"),
E("yn_tibet","吐蕃款附","boon",False,None,{},{"court":4,"military":2},"乌思藏来献，舆图益广，西陲以宁。"),
E("yn_quake","地震坏城","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-2},"地震坏宫阙庐舍，压溺者不可胜计。"),
E("yn_silk","丝绢远销","boon",False,None,{},{"treasury":5,"people":2},"锦绮行于海外，互市之利岁增。"),
E("yn_tax","赋敛繁苛","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-1},"包银科差无艺，民不堪命，逃者众。"),
E("yn_pardon","肆赦覃恩","boon",False,None,{},{"court":4,"people":4},"大赦天下，蠲逋负，欢心大洽。"),
E("yn_court","宫廷晏安","boon",False,"暮年",{},{"court":3,"health":2},"禁掖无事，岁时游豫，晏然自得。"),
E("yn_locust","蝗蔽日","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-2},"飞蝗蔽日，禾黍一空，捕瘗不给。"),
E("yn_scholar","儒术复用","boon",False,None,{},{"court":5,"people":2},"兴学校行贡举，儒者稍进，文治渐修。"),
E("yn_bandit","海商被劫","calamity",False,None,{"treasury":"treasury"},{"treasury":-4,"people":-1},"海岛群盗掠番船，市舶之利损。"),
E("yn_store","太仓陈红","boon",False,None,{},{"treasury":5,"people":3},"岁漕足额，太仓陈陈相因，国计殷实。"),
E("yn_cold","朔漠苦寒","calamity",False,None,{"health":"health"},{"health":-5,"people":-1},"奇寒伤稼伤人，边地尤甚。"),
E("yn_road","驿传修举","boon",False,None,{},{"court":4,"military":1},"驿站完具，使命通达，边情上闻速。"),
E("yn_reform","更张庶务","boon",False,None,{},{"court":4,"people":3},"裁冗省费，与民休息，流亡稍复。"),
E("yn_oppress","豪强兼并","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-1},"势家夺民田，细民失所，讼狱繁兴。"),
E("yn_mission","四方来朝","boon",False,None,{},{"court":5,"people":1},"高丽占城交趾修贡，冠盖相望。"),
E("yn_fire","火药局灾","calamity",False,None,{"treasury":"treasury"},{"treasury":-5,"people":-2},"武库不戒于火，军资延燔，边备稍虚。"),
E("yn_fish","渔盐之利","boon",False,None,{},{"treasury":4,"people":2},"立盐运司，渔盐之课充，用度少窘。"),
E("yn_li","吏道杂进","calamity",False,None,{"court":"court"},{"court":-4,"people":-1},"色目胥吏并用，铨法寖紊，清议短之。"),
E("yn_rain","甘澍应时","boon",False,None,{},{"people":6,"treasury":2},"时雨既降，百谷用成，农庆大有。"),
E("yn_war","边将骄恣","calamity",False,None,{"military":"military"},{"military":-4,"court":-2},"藩将渐骄，不奉约束，尾大之患萌。"),
E("yn_buddha","帝师崇奉","boon",False,None,{},{"court":3,"people":2},"尊礼帝师，梵宇庄严，倾动一时。"),
E("yn_poor","贫者无立","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-1},"富者田连阡陌，贫者亡立锥，怨咨载路。"),
E("yn_iron","铁冶大兴","boon",False,None,{},{"treasury":4,"military":2},"置铁冶提举，兵农之器饶，课利亦厚。"),
E("yn_revolt2","妖民惑众","calamity",False,None,{"court":"court"},{"court":-4,"people":-2},"妖言相煽，聚徒甚众，捕之乃散。"),
E("yn_grain2","义廪丰积","boon",False,None,{},{"people":6,"treasury":2},"诸路义仓积谷至厚，虽灾不害。"),
E("yn_quake2","山裂涌泉","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-1},"山崩裂涌黑泉，田庐陷没，民徙他邑。"),
E("yn_pacify2","藩王入觐","boon",False,None,{},{"court":4,"military":2},"诸王述职，献版图弓矢，朝廷威重。"),
E("yn_li2","理财失宜","calamity",False,None,{"treasury":"treasury"},{"treasury":-4,"people":-1},"楮币滥发，物重钱轻，公私交病。"),
E("yn_hunt","搜狩讲武","boon",False,None,{},{"military":4,"health":1},"行围讲武，士马精强，畿甸肃然。"),
E("yn_flood2","江淮并溢","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-2},"江淮并涨，田庐漂没，漕亦受阻。"),
E("yn_silk2","织染精巧","boon",False,None,{},{"treasury":4,"people":1},"纳石失等织巧夺天工，远蕃争市。"),
E("yn_tax2","劝农诏下","boon",False,None,{},{"treasury":-2,"people":6},"诏劝农桑，给牛种，流民著籍者众。"),
E("yn_rebel3","群盗如毛","calamity",True,None,{"military":"military"},{"military":-8,"people":-4},"群盗蜂起，郡邑昼闭，征剿不给。"),
]
POOLS["yuan"] = y

# ===================== 明 (ming) =====================
m = []
m += [
E("mg_flood","黄河决张秋","calamity",False,None,{"treasury":"treasury"},{"people":-6,"treasury":-5},"河决张秋，运道梗阻，竭帑以塞。"),
E("mg_peace","四裔宾服","boon",False,None,{},{"court":5,"military":2},"诸番修贡，边亭息警，海宇乂安。"),
E("mg_eunuch","厂卫横行","calamity",False,None,{"court":"court"},{"court":-6,"people":-2},"缇骑四出，告讦成风，士大夫重足。"),
E("mg_tribute","西洋宝船","boon",False,None,{},{"treasury":6,"court":2},"宝船远归，香料珍奇充溢内府。"),
E("mg_drought","畿辅大旱","calamity",False,None,{"people":"people"},{"people":-7,"treasury":-2},"北畿赤地，井泉涸，赈恤不给。"),
E("mg_exam","南宫抡才","boon",False,None,{},{"court":6,"people":2},"开科取士，寒俊满朝，文治浸兴。"),
E("mg_wokou","倭寇掠海","calamity",True,None,{"military":"military"},{"military":-8,"people":-4,"treasury":-2},"倭舶连艘登陆，焚掠濒海，官兵失利。"),
E("mg_canal","漕河畅通","boon",False,None,{},{"treasury":4,"people":2},"漕河深通，岁运四百万石达京，廪实。"),
E("mg_plague","时疫都下","calamity",False,None,{"health":"health"},{"health":-6,"people":-2},"疫作京师，施药棺殍，死者相藉。"),
E("mg_store","太仓红腐","boon",False,None,{},{"treasury":5,"people":3},"太仓粟陈因红腐，九边粮饷有继。"),
E("mg_party","门户相攻","calamity",False,None,{"court":"court"},{"court":-6,"people":-1},"东林与齐楚浙党交讦，朝端如水火。"),
E("mg_north","北虏款塞","boon",False,None,{},{"military":5,"court":2},"俺答款塞，边市开，烽燧少警。"),
E("mg_famine","米珠薪桂","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-1},"岁凶价踊，贫民枵腹，道殣相望。"),
E("mg_granary","预备仓备","boon",False,None,{},{"people":6,"treasury":2},"预备仓积谷，凶年振赡，民志以定。"),
E("mg_star","星变示儆","calamity",False,None,{"court":"court"},{"court":-4,"health":-1},"彗孛见于东方，修省之诏屡下。"),
E("mg_audit","考成法行","boon",False,None,{},{"court":5,"people":3},"立考成课吏，惰者黜勤者陟，百事修举。"),
E("mg_rebel","矿盗起事","calamity",False,None,{"military":"military"},{"military":-5,"people":-2},"矿徒聚众，攻剽州邑，官兵捕之急。"),
E("mg_trade","市舶抽分","boon",False,None,{},{"treasury":5,"people":1},"番舶抽分有则，饷需稍充。"),
E("mg_li","吏治澄清","boon",False,None,{},{"court":5,"people":3},"抚按得人，墨吏屏迹，闾阎乐业。"),
E("mg_fire","西苑火灾","calamity",False,None,{"treasury":"treasury"},{"treasury":-5,"people":-1},"西苑不戒于火，珍玩帷帐尽煨烬。"),
E("mg_tun","军屯丰殖","boon",False,None,{},{"military":5,"treasury":1},"九边屯田登，兵食自足，省转输。"),
E("mg_locust","蝗越淮泗","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-2},"飞蝗渡淮，泗上告饥，捕瘗不给。"),
E("mg_omens","符瑞丛出","boon",False,None,{},{"court":4,"people":2},"白雉嘉禾之瑞迭见，史馆书之。"),
E("mg_tax","赋役不均","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-1},"田亩诡寄，赋役偏重细民，逃亡相属。"),
E("mg_pardon","大赦覃恩","boon",False,None,{},{"court":4,"people":4},"肆赦罪囚，存问高年，欢心大洽。"),
E("mg_jin","金白之乱","calamity",True,None,{"military":"military"},{"military":-9,"people":-4,"court":-2},"叛酋陷城，羽檄交驰，社稷震骇。"),
E("mg_silk","织染精巧","boon",False,None,{},{"treasury":4,"people":2},"苏杭织造精丽，四方商贾骈集。"),
E("mg_quake","地震坏城","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-2},"地震坏城垣庐舍，压溺者众。"),
E("mg_school","社学遍设","boon",False,None,{},{"court":4,"people":3},"社学乡塾遍郡县，童蒙知学。"),
E("mg_war","边将骄恣","calamity",False,None,{"military":"military"},{"military":-4,"court":-2},"总兵渐骄，侵饷冒功，尾大之患萌。"),
E("mg_yun","云贵底定","boon",False,None,{},{"military":5,"court":1},"土司向化，改流设官，南服以宁。"),
E("mg_poor","流民载道","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-1},"灾伤流民就食他方，邑里萧然。"),
E("mg_iron","铁冶大兴","boon",False,None,{},{"treasury":4,"military":2},"铁冶所出兵农器饶，课程亦厚。"),
E("mg_party2","台谏风闻","calamity",False,None,{"court":"court"},{"court":-4,"people":-1},"言官风闻论劾，大臣日夕迁除，政事牵制。"),
E("mg_rain","甘澍应时","boon",False,None,{},{"people":6,"treasury":2},"时雨既降，秋成有望，农庆大有。"),
E("mg_bandit","海盗张甚","calamity",False,None,{"treasury":"treasury"},{"treasury":-4,"people":-2},"巨寇纵横海上，劫夺商舶，市易不通。"),
E("mg_li2","蠲租恤民","boon",False,None,{},{"treasury":-2,"people":6},"诏蠲灾租，与民休息，田里少苏。"),
E("mg_temple","斋醮糜费","calamity",False,"暮年",{"treasury":"treasury"},{"treasury":-5,"court":-1},"玄修斋醮无虚日，帑藏虚耗，谏者获罪。"),
E("mg_border","北边防固","boon",False,None,{},{"military":5,"court":2},"修边墙增戍守，胡马不敢南牧。"),
E("mg_famine2","凶荒荐臻","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-2},"水旱继作，凶荒荐臻，赈赡不给。"),
E("mg_charity","义民输粟","boon",False,None,{},{"people":5,"treasury":2},"义民纳米补官，仓庾稍实，全活颇多。"),
E("mg_reform","一条鞭行","boon",False,None,{},{"treasury":4,"people":3},"赋役合并折银，民便之，隐漏稍清。"),
E("mg_li3","礼文繁缛","calamity",False,None,{"court":"court"},{"court":-3,"treasury":-1},"议礼之争纷如，文具寖盛，实惠或少。"),
E("mg_store2","京库充羡","boon",False,None,{},{"treasury":5,"people":3},"内帑岁入有羡，水旱得以便振。"),
E("mg_rebel2","民变蜂起","calamity",True,None,{"military":"military"},{"military":-8,"people":-4,"court":-2},"民不堪命，揭竿响应，郡县多陷。"),
E("mg_fo","梵刹崇奉","boon",False,None,{},{"court":3,"people":2},"寺观鼎新，斋醮屡举，民俗稍安。"),
E("mg_li4","吏惰案积","calamity",False,None,{"court":"court"},{"court":-4,"people":-2},"有司因循，滞狱山积，冤抑莫伸。"),
E("mg_envoy","四夷来王","boon",False,None,{},{"court":5,"people":1},"朝鲜安南琉球修贡，冠盖相望。"),
E("mg_flood2","江淮并溢","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-2},"江淮并涨，田庐漂没，漕舟胶滞。"),
E("mg_farm","农田水利","boon",False,None,{},{"people":5,"treasury":2},"浚陂塘通沟洫，旱潦有备，亩收倍常。"),
E("mg_eunuch2","中官贪墨","calamity",False,None,{"treasury":"treasury"},{"treasury":-5,"court":-1},"矿税使四出，搜括无艺，商旅罢市。"),
E("mg_audit2","清丈田亩","boon",False,None,{},{"treasury":4,"people":2},"清丈亩实，隐田出赋，国与民两利。"),
E("mg_star2","山崩石裂","calamity",False,None,{"court":"court"},{"court":-4,"health":-1},"泰山崩，石走，太史言阴盛阳微。"),
E("mg_bumper","两畿丰稔","boon",False,None,{},{"people":6,"treasury":2},"南北两畿并熟，流亡复归，闾阎充实。"),
E("mg_poor2","贫窭难活","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-1},"赋重役烦，贫者鬻妻孥以偿，怨咨载路。"),
E("mg_pardon2","肆赦矜疑","boon",False,None,{},{"court":4,"people":4},"录矜疑之囚，施 scarf 泽，和气充塞。"),
]
POOLS["ming"] = m

# ===================== 清 (qing) =====================
c = []
c += [
E("qg_flood","黄淮并涨","calamity",False,None,{"treasury":"treasury"},{"people":-6,"treasury":-5},"黄淮并溢，泗州祖陵浸，竭帑以工。"),
E("qg_pax","四海宾服","boon",False,None,{},{"court":5,"military":2},"群藩修贡，边宇宁谧，海宴河清。"),
E("qg_rebel","台湾郑氏","calamity",True,None,{"military":"military"},{"military":-8,"people":-3,"treasury":-2},"海疆未靖，水师屡战，转饷浩繁。"),
E("qg_canal","漕运畅达","boon",False,None,{},{"treasury":4,"people":2},"漕艘衔尾达通州，太仓有继，京师长赡。"),
E("qg_drought","畿辅大旱","calamity",False,None,{"people":"people"},{"people":-7,"treasury":-2},"北直赤地，井泉涸，赈贷不给。"),
E("qg_exam","恩科抡才","boon",False,None,{},{"court":6,"people":2},"开恩科广额，寒士兴起，文运方隆。"),
E("qg_plague","时疫流行","calamity",False,None,{"health":"health"},{"health":-6,"people":-2},"疫气行于乡邑，施药棺殍，死者相藉。"),
E("qg_store","库藏充溢","boon",False,None,{},{"treasury":6,"people":2},"户部帑银岁溢，虽有水旱得以便振。"),
E("qg_party","党争复作","calamity",False,None,{"court":"court"},{"court":-5,"people":-1},"南北党人相攻，章奏纷如，庶事牵制。"),
E("qg_outer","外藩晏然","boon",False,None,{},{"court":4,"military":3},"漠南漠北悉臣，秋狝讲武，边声甚壮。"),
E("qg_famine","米价腾踊","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-1},"连歉米踊贵，贫民枵腹，道殣相望。"),
E("qg_granary","常平积谷","boon",False,None,{},{"people":6,"treasury":2},"常平仓额满，平市栉沐，民无菜色。"),
E("qg_star","星变修省","calamity",False,None,{"court":"court"},{"court":-4,"health":-1},"彗见紫微，下诏修省，求直言。"),
E("qg_audit","耗羡归公","boon",False,None,{},{"court":5,"treasury":2},"火耗归公养廉，墨吏稍戢，库藏渐实。"),
E("qg_rebel2","苗疆不靖","calamity",False,None,{"military":"military"},{"military":-5,"people":-2},"苗疆煽乱，官兵进剿，转饷旁午。"),
E("qg_trade","海关贸易","boon",False,None,{},{"treasury":6,"people":2},"粤海设关，番舶来市，关税充饶。"),
E("qg_li","吏治澄清","boon",False,None,{},{"court":5,"people":3},"督抚得人，州县畏法，闾阎乐业。"),
E("qg_fire","宫中火灾","calamity",False,None,{"treasury":"treasury"},{"treasury":-5,"people":-1},"禁城不戒于火，殿宇延燔，帑藏小损。"),
E("qg_tun","屯垦实边","boon",False,None,{},{"military":5,"treasury":1},"遣屯垦于边，且耕且守，转输之费省。"),
E("qg_locust","蝗越黄淮","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-2},"飞蝗渡河，淮徐告饥，捕瘗不给。"),
E("qg_omens","嘉瑞频呈","boon",False,None,{},{"court":4,"people":2},"嘉禾芝草之瑞迭见，史臣书之。"),
E("qg_tax","赋役不均","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-1},"版图隐漏，赋役偏重穷檐，逋逃相属。"),
E("qg_pardon","大赦覃恩","boon",False,None,{},{"court":4,"people":4},"肆赦罪囚，鳏寡存问，欢心大洽。"),
E("qg_jin","金川之役","calamity",True,None,{"military":"military"},{"military":-9,"people":-4,"treasury":-3},"两金川抗命，悬师深入，转饷万金。"),
E("qg_silk","织造精丽","boon",False,None,{},{"treasury":4,"people":2},"江宁苏杭织造精丽，四方商贾骈集。"),
E("qg_quake","地震坏城","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-2},"地震坏城郭庐舍，压溺者不可胜计。"),
E("qg_school","义学遍设","boon",False,None,{},{"court":4,"people":3},"义学蒙馆遍乡里，童蒙知向学。"),
E("qg_war","将骄兵惰","calamity",False,None,{"military":"military"},{"military":-4,"court":-2},"承平将卒骄惰，操演寖废，猝警张皇。"),
E("qg_yun","云贵底定","boon",False,None,{},{"military":5,"court":1},"改土归流，边徼向化，南服以宁。"),
E("qg_poor","流民就食","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-1},"灾伤流民载道，邑里萧条，绥抚未遑。"),
E("qg_iron","矿厂大兴","boon",False,None,{},{"treasury":4,"military":2},"滇铜黔铅之厂兴，钱法兵备两利。"),
E("qg_party2","言路纷争","calamity",False,None,{"court":"court"},{"court":-4,"people":-1},"台谏风闻互劾，大臣席不暇暖，政令数易。"),
E("qg_rain","甘澍应时","boon",False,None,{},{"people":6,"treasury":2},"时雨既降，百谷用成，农庆大有。"),
E("qg_bandit","海盗张甚","calamity",False,None,{"treasury":"treasury"},{"treasury":-4,"people":-2},"洋盗纵横，劫夺商舶，海市不通。"),
E("qg_li2","减赋予民","boon",False,None,{},{"treasury":-2,"people":6},"诏减漕赋，损上益下，田里少苏。"),
E("qg_temple","崇佛糜费","calamity",False,"暮年",{"treasury":"treasury"},{"treasury":-5,"court":-1},"崇奉梵修无度，内帑虚耗，谏者获谴。"),
E("qg_border","卡伦严整","boon",False,None,{},{"military":5,"court":2},"边卡罗列，巡哨严明，朔漠无警。"),
E("qg_famine2","凶荒荐臻","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-2},"水旱继作，凶荒荐臻，赈赡不给。"),
E("qg_charity","义仓振饥","boon",False,None,{},{"people":5,"treasury":2},"社义仓并设，凶岁大振，全活甚众。"),
E("qg_reform","摊丁入亩","boon",False,None,{},{"treasury":4,"people":3},"丁随地起，无苛派之扰，民稍宽。"),
E("qg_li3","典礼繁缛","calamity",False,None,{"court":"court"},{"court":-3,"treasury":-1},"议礼陈仪寖盛，实惠或少，识者忧之。"),
E("qg_store2","内帑丰饶","boon",False,None,{},{"treasury":5,"people":2},"户部帑项岁溢，水旱得以便振，国计赖之。"),
E("qg_water","水利修举","boon",False,None,{},{"people":5,"treasury":2},"浚河筑塘，旱潦有备，亩收倍常。"),
E("qg_li4","吏惰案积","calamity",False,None,{"court":"court"},{"court":-4,"people":-2},"有司因循，滞狱山积，冤抑莫伸。"),
E("qg_foreign","四夷来朝","boon",False,None,{},{"court":5,"people":1},"朝鲜暹罗荷兰修贡，帆樯相望。"),
E("qg_flood2","江淮水潦","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-2},"江淮并涨，田庐漂没，漕舟胶滞。"),
E("qg_farm","农田水利","boon",False,None,{},{"people":5,"treasury":2},"沟洫既治，亢旱有备，野无旷土。"),
E("qg_eunuch","宦寺干政","calamity",False,"暮年",{"court":"court"},{"court":-5,"people":-1},"内监渐预朝权，廷臣奏事多沮。"),
E("qg_bumper","两江丰稔","boon",False,None,{},{"people":6,"treasury":2},"江浙并熟，流亡复归，闾阎充实。"),
E("qg_rebel3","教案萌动","calamity",False,None,{"court":"court"},{"court":-4,"people":-2},"邪说聚众，愚民易惑，捕之乃散。"),
E("qg_tea","茶马互市","boon",False,None,{},{"treasury":4,"military":1},"茶马交易蕃息，边储稍实，戎心易驯。"),
E("qg_cold","朔漠奇寒","calamity",False,None,{"health":"health"},{"health":-4,"people":-1},"口外奇寒伤稼伤人，边地尤甚。"),
E("qg_pardon2","肆赦矜疑","boon",False,None,{},{"court":4,"people":4},"录矜疑之囚，施旷荡之恩，和气充塞。"),
E("qg_li5","里甲扰民","calamity",False,None,{"people":"people"},{"people":-4,"treasury":-1},"里甲科派无名，鸡犬为竭，细民重困。"),
E("qg_silk2","织染精巧","boon",False,None,{},{"treasury":4,"people":1},"江南三织造精丽，远蕃争市。"),
E("qg_quake2","山崩石裂","calamity",False,None,{"court":"court"},{"court":-4,"health":-1},"华山崩石走，太史言阴盛阳微。"),
E("qg_yamen","衙署肃清","boon",False,None,{},{"court":4,"people":3},"大吏严察属官，墨吏屏迹，闾阎乐业。"),
E("qg_poor2","贫窭难活","calamity",False,None,{"people":"people"},{"people":-5,"treasury":-1},"赋重役烦，贫者鬻妻孥以偿，怨咨载路。"),
E("qg_mint","钱法通畅","boon",False,None,{},{"treasury":4,"people":1},"鼓铸得法，钱价平稳，市易以通。"),
E("qg_bandit2","盐枭私贩","calamity",False,None,{"treasury":"treasury"},{"treasury":-4,"people":-1},"私盐充斥，榷利大损，捕之急则变。"),
E("qg_envoy2","藩部朝贡","boon",False,None,{},{"court":4,"military":2},"漠西漠北献琛，舆图益广，西陲以宁。"),
E("qg_famine3","旱涝叠更","calamity",False,None,{"people":"people"},{"people":-6,"treasury":-2},"先潦后旱，再更其虐，播种失时。"),
E("qg_audit2","清厘隐田","boon",False,None,{},{"treasury":4,"people":2},"清丈亩实，隐田出赋，国与民两利。"),
]
POOLS["qing"] = c

# 均衡补充波：补足总数≥500，且净漂移≈0（4 灾 + 4 祥，按维配对），不引入新的单向偏置。
CORRECT = {
  "shangzhou": [
    E("szx_1","岁凶民困","calamity",False,None,{"people":"people"},{"people":-4},"岁凶民困，道有殣者，赈恤不给。"),
    E("szx_2","赋敛小急","calamity",False,None,{"treasury":"treasury"},{"treasury":-4},"关市薄敛偶急，府藏小损。"),
    E("szx_3","边亭小警","calamity",False,None,{"military":"military"},{"military":-4},"方国小衅，边亭微警，戍卒劳于候望。"),
    E("szx_4","宗彝小阙","calamity",False,None,{"court":"court"},{"court":-4},"祀典小阙，保章忧之，朝仪稍紊。"),
    E("szx_5","野蚕成茧","boon",False,None,{},{"people":4},"野蚕成茧，丝枲有资，妇子得衣。"),
    E("szx_6","山泽之利","boon",False,None,{},{"treasury":4},"山出金石，泽生鱼盐，关市之征足。"),
    E("szx_7","裒旅治兵","boon",False,None,{},{"military":4},"裒旅治兵，搜狩有礼，军容肃然。"),
    E("szx_8","宾服来享","boon",False,None,{},{"court":4},"荒服来享，共执壤奠，礼成而欢。"),
  ],
  "qinhan": [
    E("qhx_1","关东水潦","calamity",False,None,{"people":"people"},{"people":-4},"关东水潦，田庐小损，转输稍劳。"),
    E("qhx_2","漕挽小梗","calamity",False,None,{"treasury":"treasury"},{"treasury":-4},"漕挽小梗，关东之粟后时。"),
    E("qhx_3","亭徼小惊","calamity",False,None,{"military":"military"},{"military":-4},"亭徼小惊，烽燧微举，戍卒戒严。"),
    E("qhx_4","奏议纷然","calamity",False,None,{"court":"court"},{"court":-4},"奏议纷然，大臣数异论，庶务小滞。"),
    E("qhx_5","熟田增辟","boon",False,None,{},{"people":4},"劝农熟田增辟，阡陌弥望。"),
    E("qhx_6","少府饶羡","boon",False,None,{},{"treasury":4},"少府饶羡，禁钱充溢，用度少窘。"),
    E("qhx_7","楼船缮完","boon",False,None,{},{"military":4},"楼船缮完，江海有备，波靖不惊。"),
    E("qhx_8","儒林彬彬","boon",False,None,{},{"court":4},"儒林彬彬，正音复明，风化归厚。"),
  ],
  "weijin": [
    E("wjx_1","淮泗小饥","calamity",False,None,{"people":"people"},{"people":-4},"淮泗小饥，赈贷稍给，民未大困。"),
    E("wjx_2","运道小滞","calamity",False,None,{"treasury":"treasury"},{"treasury":-4},"运道小滞，转输后期，上供小缺。"),
    E("wjx_3","边戍小劳","calamity",False,None,{"military":"military"},{"military":-4},"边戍小劳，斥候戒严，烽燧时举。"),
    E("wjx_4","清谈小弊","calamity",False,None,{"court":"court"},{"court":-4},"清谈小弊，尸位者众，庶务寖废。"),
    E("wjx_5","流人复业","boon",False,None,{},{"people":4},"流人相率复业，墝埆尽辟。"),
    E("wjx_6","互市小利","boon",False,None,{},{"treasury":4},"互市小利，驼马络绎，关市少饶。"),
    E("wjx_7","水军小练","boon",False,None,{},{"military":4},"水军小练，蒙冲连舳，江防益固。"),
    E("wjx_8","文雅蔚然","boon",False,None,{},{"court":4},"文雅蔚然，人物风流，江左风尚。"),
  ],
  "tang": [
    E("tgx_1","畿甸小饥","calamity",False,None,{"people":"people"},{"people":-4},"畿甸小饥，赈恤便给，民未大困。"),
    E("tgx_2","关市小敛","calamity",False,None,{"treasury":"treasury"},{"treasury":-4},"关市小敛，舟车之征偶急。"),
    E("tgx_3","亭障小惊","calamity",False,None,{"military":"military"},{"military":-4},"亭障小惊，烽燧微举，边将戒严。"),
    E("tgx_4","谏争小烦","calamity",False,None,{"court":"court"},{"court":-4},"谏争小烦，大臣数廷论，庶务小滞。"),
    E("tgx_5","圩田增辟","boon",False,None,{},{"people":4},"圩田增辟，稻蟹之利倍常。"),
    E("tgx_6","舟车小利","boon",False,None,{},{"treasury":4},"舟车小利，货殖流通，关市少饶。"),
    E("tgx_7","边师小捷","boon",False,None,{},{"military":4},"边师小捷，虏帐小徙，北门少安。"),
    E("tgx_8","文物彬然","boon",False,None,{},{"court":4},"文物彬然，雅颂复作，朝仪粲然。"),
  ],
  "song": [
    E("sgx_1","两浙小歉","calamity",False,None,{"people":"people"},{"people":-4},"两浙小歉，赈贷便给，民未大困。"),
    E("sgx_2","折变小扰","calamity",False,None,{"treasury":"treasury"},{"treasury":-4},"折变小扰，输纳偶重，细民小困。"),
    E("sgx_3","堡寨小惊","calamity",False,None,{"military":"military"},{"military":-4},"堡寨小惊，亭障微警，戍卒戒严。"),
    E("sgx_4","党论小烦","calamity",False,None,{"court":"court"},{"court":-4},"党论小烦，章奏相轧，庶务小滞。"),
    E("sgx_5","圩田增辟","boon",False,None,{},{"people":4},"圩田增辟，米舟蔽江，物价乃平。"),
    E("sgx_6","舶利小饶","boon",False,None,{},{"treasury":4},"舶利小饶，番货充斥，府藏少羡。"),
    E("sgx_7","水军小练","boon",False,None,{},{"military":4},"水军小练，楼船习战，海防益固。"),
    E("sgx_8","学校彬然","boon",False,None,{},{"court":4},"学校彬然，教养兼施，儒风归厚。"),
  ],
  "yuan": [
    E("ynx_1","北鄙小警","calamity",False,None,{"people":"people"},{"people":-4},"北鄙小警，亭障微惊，转饷稍劳。"),
    E("ynx_2","包银小急","calamity",False,None,{"treasury":"treasury"},{"treasury":-4},"包银小急，科差偶重，民稍困。"),
    E("ynx_3","牧监小失","calamity",False,None,{"military":"military"},{"military":-4},"牧监小失，孳息偶减，兵备小虚。"),
    E("ynx_4","色目小弊","calamity",False,None,{"court":"court"},{"court":-4},"色目胥吏小弊，铨法寖紊。"),
    E("ynx_5","劝农著籍","boon",False,None,{},{"people":5},"诏劝农桑给牛种，流民著籍者众。"),
    E("ynx_6","义廪振饥","boon",False,None,{},{"people":5},"发义廪振饥，全活甚众，凶不为害。"),
    E("ynx_7","互市小利","boon",False,None,{},{"treasury":4},"互市小利，驼马络绎，关市少饶。"),
    E("ynx_8","驿传小修","boon",False,None,{},{"court":4},"驿传小修，使命通达，边情上闻速。"),
  ],
  "ming": [
    E("mgx_1","南畿小歉","calamity",False,None,{"people":"people"},{"people":-4},"南畿小歉，赈贷便给，民未大困。"),
    E("mgx_2","织造小费","calamity",False,None,{"treasury":"treasury"},{"treasury":-4},"织造小费，内帑偶虚，工价小增。"),
    E("mgx_3","边卒小惊","calamity",False,None,{"military":"military"},{"military":-4},"边卒小惊，烽燧微举，戍守戒严。"),
    E("mgx_4","言路小烦","calamity",False,None,{"court":"court"},{"court":-4},"言路小烦，风闻论劾，庶务小滞。"),
    E("mgx_5","屯田增辟","boon",False,None,{},{"people":4},"屯田增辟，兵农两利，野无旷土。"),
    E("mgx_6","市舶小饶","boon",False,None,{},{"treasury":4},"市舶小饶，番货充斥，饷需少充。"),
    E("mgx_7","边师小捷","boon",False,None,{},{"military":4},"边师小捷，胡马不敢南牧。"),
    E("mgx_8","吏治小清","boon",False,None,{},{"court":4},"抚按小清，墨吏屏迹，闾阎乐业。"),
  ],
  "qing": [
    E("qgx_1","畿辅小歉","calamity",False,None,{"people":"people"},{"people":-4},"畿辅小歉，赈贷便给，民未大困。"),
    E("qgx_2","关市小敛","calamity",False,None,{"treasury":"treasury"},{"treasury":-4},"关市小敛，舟车之征偶急。"),
    E("qgx_3","卡伦小警","calamity",False,None,{"military":"military"},{"military":-4},"卡伦小警，巡哨微举，边备戒严。"),
    E("qgx_4","言路小烦","calamity",False,None,{"court":"court"},{"court":-4},"言路小烦，风闻论劾，庶务小滞。"),
    E("qgx_5","农田增辟","boon",False,None,{},{"people":4},"农田增辟，流民著籍，野无旷土。"),
    E("qgx_6","海关小饶","boon",False,None,{},{"treasury":4},"海关小饶，番舶来市，关税少羡。"),
    E("qgx_7","巡哨小修","boon",False,None,{},{"military":4},"巡哨小修，卡伦严明，朔漠无警。"),
    E("qgx_8","吏治小清","boon",False,None,{},{"court":4},"督抚小清，州县畏法，闾阎乐业。"),
  ],
}
for _tag, _lst in CORRECT.items():
    POOLS[_tag] += _lst

# ---- 民间创新（研发科技）：低权重(0.2)，概率小但有可能的民间自发技术突破 ----
# baseChanges 净中性：tech+3（研发红利），court-2/people-1（新法微扰）。对失败链四维净 -3，
# 桶均值≈-3/n（n≈60 → -0.05），远低于报警阈值 -0.5*n，不破坏无偏契约。
# unlockTech=True：结算时免费解锁一个 age<=eraLevel 且未拥有的当世科技节点（见 index.html applyFolkInnovation）。
INNOV = {
    "shangzhou": ("sz_minjian", "氓隶献桔槔", "有野人负桔槔之械来献，引水甚便，巫史讥其淫巧，然民用赖之。"),
    "qinhan":    ("qh_minjian", "田父献代田", "有田父献代田之法，力省而收倍，乡里效之，或讥烦苛。"),
    "weijin":    ("wj_minjian", "巧匠献水碓", "有巧匠作水碓之利，舂米不劳，然豪右专利，闾阎或怨。"),
    "tang":      ("tang_minjian", "羁旅献曲辕", "有羁旅献曲辕之犁，耕垦便捷，州县长吏疑其扰民。"),
    "song":      ("song_minjian", "市井献活字", "有市井献活字之术，印书甚速，然士林疑其乱经。"),
    "yuan":      ("yuan_minjian", "番商献火铳", "有番商献火铳之模，军前可试，廷臣忧其难制。"),
    "ming":      ("ming_minjian", "匠户献新机", "有匠户献织机之新制，巧捷倍常，税监欲专其利。"),
    "qing":      ("qing_minjian", "夷匠献蒸汽", "有夷匠献蒸汽之模，巧夺天工，朝野骇其异术。"),
}
for _tag, (_id, _title, _desc) in INNOV.items():
    POOLS[_tag].append(E(_id, _title, "innovation", False, None, {},
                          {"tech": 3, "court": -2, "people": -1}, _desc,
                          flavor="民间巧思，往往出于畎亩之间。",
                          comment="史官评曰：民之所利，虽微必录，然新法初行，利弊相半。",
                          weight=0.2, unlockTech=True))

def drift_of(bucket):
    d = {k: 0 for k in DIMS}
    for e in bucket:
        for k, v in e["baseChanges"].items():
            d[k] += v
    return d

# ---- 逐维净漂移闭合（平衡根因修复）----
# 原校验只报警"失败链四维负漂移"，并明文接受 court 正偏/health 负偏，导致 court 被系统性顶高（最易满 100）、
# health 被抽干却不计入结局 —— 随机冲击反而系统性抬高终局评级（"随机暗助评分"）。
# 此处对每个桶的 treasury/people/military/court 正偏，追加中性抵消 calamity 事件（每维 step=4），
# 把净漂移压回≈0；health 负偏保留（现计入结局评分，作真实 sink，不在此闭合）。
BALANCE_STEP = 4
BALANCE_THR = 0.1  # 单事件均值阈值；原值 0.5 过松，导致 court 每事件 +0.4 的长局累积通胀被放过。收紧到 0.1：任何维度每事件均值 >0.1 即补中性抵消事件，使随机池回到"逐维净漂移≈0"的设计初衷。
GENERIC_DRAIN = {
    "treasury": ("帑藏小损", "关市薄敛偶急，府藏小损，用度稍窘。"),
    "people":   ("民力小疲", "徭役小急，民力稍疲，闾阎小困。"),
    "military": ("边戍小劳", "亭徼小惊，戍卒劳于候望，烽燧微举。"),
    "court":    ("朝局小扰", "浮议时起，朝局小有纷纭，庶务微滞。"),
}
def close_balance(tag, pool):
    n = len(pool)
    d = drift_of(pool)
    for k in ["treasury", "people", "military", "court"]:
        surplus = d[k]  # 正偏需抵消
        if surplus <= BALANCE_THR * n:
            continue
        i, need = 0, surplus
        while need > 0:
            eid = f"{tag}_bal_{k[0]}{i}"
            title, desc = GENERIC_DRAIN[k]
            pool.append(E(eid, title, "calamity", False, None, {}, {k: -BALANCE_STEP}, desc,
                           flavor="事出细微，无大患而足以为戒。",
                           comment="史官谨书，俟后观之。", weight=1))
            need -= BALANCE_STEP
            i += 1
for _tag, _bucket in POOLS.items():
    close_balance(_tag, _bucket)

# ---- 校验与输出 ----
total = 0
FAIL_DIMS = ["treasury", "people", "military", "court"]  # 失败链四维：仅其负漂移会系统性推向崩盘，须报警
print("=== 随机时局池平衡校验（失败链四维负偏 AND 各维正偏均报警；health 负偏为真实 sink 保留）===")
for tag, bucket in POOLS.items():
    total += len(bucket)
    d = drift_of(bucket)
    n = len(bucket)
    # 报警规则：负偏宽松（仅 -0.5*n 抓崩盘级危险，轻微负漂移是健康 sink，不必报警）；正偏严格（+0.1*n 抓 court 式通胀）
    fail_neg = [k for k in FAIL_DIMS if d[k] < -0.5 * n]
    pos_warn = [k for k in DIMS if d[k] > 0.1 * n]
    flag = "OK" if (not fail_neg and not pos_warn) else (
        ("**失败链负偏:" + ",".join(fail_neg) + "**" if fail_neg else "") +
        (" 正偏:" + ",".join(pos_warn) if pos_warn else ""))
    print(f"{tag:10s} 事件数={n:3d}  净漂移 T{d['treasury']:+4d} P{d['people']:+4d} M{d['military']:+4d} C{d['court']:+4d} H{d['health']:+4d}  {flag}")
print(f"总事件数 = {total}  (要求 >=500: {'OK' if total>=500 else '不足'})")

out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
out_path = os.path.join(out_dir, "random_pools.js")
os.makedirs(out_dir, exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    f.write("// 随机时局（v0.2）事件池：由 tools/gen_random_pools.py 生成，勿手改。\n")
    f.write("// 8 时期桶，自动生效外生冲击；净漂移≈0（见生成器校验打印）。\n")
    f.write("window.COH_RANDOM_POOLS = ")
    f.write(json.dumps(POOLS, ensure_ascii=False, separators=(",", ":")))
    f.write(";\n")
print(f"已写出 {out_path}")