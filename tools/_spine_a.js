// P3 铺陈：Tier A 名帝完整 spine（reignPremise + voiceTag + cast）
// 仅用于 tools/_inject_spine.js 合并进 data/emperors/*.json
// 已有 3 帝（qing_taizu/tang_taizong/song_gaozong）手写精修版保留，此处跳过不覆盖
module.exports = {
  // ===== 夏 =====
  xia_jie: {
    reignPremise: "末世之君，能否以威权镇住离心之诸侯、挽将倾之夏鼎？酒池肉林之下，诸侯已畔、民心已离，而王纲犹系于一身之喜怒——此其一生之张力。",
    voiceTag: "冷峻",
    cast: [
      { id: "guanlongfeng", name: "关龙逄", role: "忠谏之臣", voiceTag: "冷峻" },
      { id: "woding", name: "沃丁", role: "诸侯离心者", voiceTag: "质朴" }
    ]
  },
  // ===== 商 =====
  shang_tang: {
    reignPremise: "诸侯之长为桀所囚，能否以仁德聚天下之心、革暴夏之命？鸣条一役，天命所归者究竟是德还是兵——此其一生之问。",
    voiceTag: "质朴",
    cast: [
      { id: "yiyin", name: "伊尹", role: "佐命元勋·阿衡", voiceTag: "华赡" },
      { id: "zhonghui", name: "仲虺", role: "左相", voiceTag: "质朴" }
    ]
  },
  shang_pangen: {
    reignPremise: "都邑五迁、民心胥怨，能否以迁殷之举安动摇之社稷、复成汤之旧业？盘庚之志在定，而定之者究竟是威还是诚——此其张力。",
    voiceTag: "质朴",
    cast: [
      { id: "yinmin", name: "殷之旧族", role: "迁都反对者", voiceTag: "质朴" },
      { id: "zhenchen", name: "贞人", role: "卜筮之官", voiceTag: "质朴" }
    ]
  },
  shang_wuding: {
    reignPremise: "自幼落魄民间、知小人之劳，能否以梦得贤、中兴既衰之商室？武丁之醒，究竟是天命之眷还是人才之幸——此其问。",
    voiceTag: "华赡",
    cast: [
      { id: "fuhaop", name: "妇好", role: "女将·后妃", voiceTag: "质朴" },
      { id: "fuyue", name: "傅说", role: "版筑之贤", voiceTag: "华赡" }
    ]
  },
  shang_dixin: {
    reignPremise: "天资绝人、材力过人，能否以一人之智驭将裂之诸侯、守数百年之商祚？聪明足以拒谏、辩足以饰非，而亡国之祸恰生于此——此其张力。",
    voiceTag: "冷峻",
    cast: [
      { id: "bigan", name: "比干", role: "剖心之忠", voiceTag: "冷峻" },
      { id: "jizi", name: "箕子", role: "佯狂之贤", voiceTag: "冷峻" },
      { id: "feilian", name: "费仲", role: "便嬖之佞", voiceTag: "冷峻" }
    ]
  },
  // ===== 汉 =====
  han_wendi: {
    reignPremise: "以代王入继大统、起于功臣环伺之中，能否以黄老之静、养秦末以来凋敝之民？无为而治者，究竟是守成之智还是积弱之始——此其问。",
    voiceTag: "华赡",
    cast: [
      { id: "zhiangya", name: "贾谊", role: "少年献策者", voiceTag: "华赡" },
      { id: "chaocuo", name: "晁错", role: "削藩谋划者", voiceTag: "华赡" }
    ]
  },
  han_jingdi: {
    reignPremise: "承文景之蓄、值七国之叛，能否以削藩之果断、固中央集权之局？平乱易而削本难，郡国并行之弊究竟何时可绝——此其张力。",
    voiceTag: "冷峻",
    cast: [
      { id: "zhouyaFu", name: "周亚夫", role: "平叛大将", voiceTag: "冷峻" },
      { id: "chaocuo", name: "晁错", role: "削藩倡议者", voiceTag: "华赡" }
    ]
  },
  han_xuandi: {
    reignPremise: "巫蛊之祸中流落民间、知闾阎疾苦，能否以霸王道杂之、振昭宣中兴之局？由贱入尊者，究竟更恤民还是更疑臣——此其问。",
    voiceTag: "华赡",
    cast: [
      { id: "huoguang", name: "霍光", role: "废立之权臣", voiceTag: "冷峻" },
      { id: "weixiang", name: "魏相", role: "宰辅", voiceTag: "华赡" }
    ]
  },
  shu_liubei: {
    reignPremise: "织席贩履之身、以仁义立帜，能否于曹孙夹隙间、续汉室将熄之灯？兴复汉室者，究竟是理想之炬还是虚名之累——此其一生之张力。",
    voiceTag: "质朴",
    cast: [
      { id: "zhugeliang", name: "诸葛亮", role: "鞠躬之相", voiceTag: "华赡" },
      { id: "guanyu", name: "关羽", role: "万人敌·义弟", voiceTag: "质朴" },
      { id: "zhangfei", name: "张飞", role: "猛将·义弟", voiceTag: "质朴" }
    ]
  },
  // ===== 晋 =====
  jin_wudi: {
    reignPremise: "受魏禅而一天下、却封建诸王以疑异姓，能否以怠惰之政、守平吴后之太平？去猜忌而种宗室之祸，统一之业竟成分裂之因——此其张力。",
    voiceTag: "华赡",
    cast: [
      { id: "yanghu", name: "羊祜", role: "平吴谋划者", voiceTag: "华赡" },
      { id: "simakai", name: "司马凯", role: "宗室疑忌者", voiceTag: "冷峻" }
    ]
  },
  jin_huidi: {
    reignPremise: "愚騃之质、居至尊之位，能否于权臣宗室之挟、保一己之安？何不食肉糜之问，究竟是昏聩还是乱世之可怜——此其悲剧。",
    voiceTag: "冷峻",
    cast: [
      { id: "jiananfeng", name: "贾南风", role: "悍后·弄权者", voiceTag: "冷峻" },
      { id: "simalun", name: "司马伦", role: "篡逆之宗室", voiceTag: "冷峻" }
    ]
  },
  jin_huaidi: {
    reignPremise: "承惠帝之乱、值永嘉之祸，能否于胡骑蹂躏中、存晋室一线之脉？天子蒙尘、怀愍相及，而中原已非汉家之土——此其痛。",
    voiceTag: "冷峻",
    cast: [
      { id: "gongshi", name: "公卿殉难者", role: "被戮朝臣", voiceTag: "冷峻" }
    ]
  },
  jin_mindi: {
    reignPremise: "继怀帝被虏、守长安孤城，能否于饥馑围城之中、延晋祚最后一息？帝弑而西晋亡，而江东已在酝酿新局——此其终。",
    voiceTag: "冷峻",
    cast: [
      { id: "changanmin", name: "长安残民", role: "饿殍之众", voiceTag: "质朴" }
    ]
  },
  jin_yuandi: {
    reignPremise: "琅邪王播越江左、依士族而立，能否以偏安之局、存华夏之正朔？王与马共天下者，究竟是权宜还是隐患——此其张力。",
    voiceTag: "华赡",
    cast: [
      { id: "wangdao", name: "王导", role: "江左管夷吾", voiceTag: "华赡" },
      { id: "wangdun", name: "王敦", role: "坐大之镇将", voiceTag: "冷峻" }
    ]
  },
  jin_mingdi: {
    reignPremise: "少年聪察、欲抑王敦之横，能否于元舅跋扈间、振皇权之坠绪？英年而崩，而庾亮之辈已伏异日之忧——此其憾。",
    voiceTag: "华赡",
    cast: [
      { id: "yuliang", name: "庾亮", role: "外戚·辅政", voiceTag: "华赡" }
    ]
  },
  // ===== 南朝宋齐梁陈 =====
  song_wudi: {
    reignPremise: "北府寒人、以军功篡晋，能否以武人之身、立寒门可为之新朝？代晋者众而能安者寡，门阀之势究竟可抑否——此其问。",
    voiceTag: "质朴",
    cast: [
      { id: "liamuzhi", name: "刘穆之", role: "谋主", voiceTag: "华赡" },
      { id: "tandaoji", name: "檀道济", role: "猛将", voiceTag: "质朴" }
    ]
  },
  song_wendi: {
    reignPremise: "守成之主、欲比隆汉文，能否以元嘉之政、成北伐恢复之伟功？自毁长城、仓促北顾，治世之君竟启溃败之端——此其张力。",
    voiceTag: "华赡",
    cast: [
      { id: "tandaoji", name: "檀道济", role: "见杀之将", voiceTag: "质朴" },
      { id: "yingzhan", name: "范晔", role: "纂史谋叛者", voiceTag: "华赡" }
    ]
  },
  qi_gaodi: {
    reignPremise: "萧齐代宋、亦以武人起家，能否于篡弑相仍之局、稍安江南之民？前车之鉴在侧，而子孙之祸已萌——此其悲。",
    voiceTag: "质朴",
    cast: [
      { id: "xiaozixian", name: "萧子显", role: "史臣·宗室", voiceTag: "华赡" }
    ]
  },
  liang_wudi: {
    reignPremise: "起兵夺齐、享国四纪，能否以佞佛之诚、赎早年征伐之罪、安江左之心？舍身同泰、侯景之乱猝发，佞佛者竟亡于佛寺之侧——此其讽。",
    voiceTag: "华赡",
    cast: [
      { id: "zhoulian", name: "周舍", role: "近臣", voiceTag: "华赡" },
      { id: "houjing", name: "侯景", role: "叛将·祸首", voiceTag: "冷峻" }
    ]
  },
  chen_wudi: {
    reignPremise: "岭南寒微、以孤忠立陈，能否于梁末崩坏之中、存江南一线之祀？国小力弱而志在存统，偏安者亦有守土之责——此其烈。",
    voiceTag: "质朴",
    cast: [
      { id: "chendian", name: "陈茜", role: "继业之侄", voiceTag: "质朴" }
    ]
  },
  chen_houzhu: {
    reignPremise: "生于深宫、长于妇人之手，能否于隋兵压境之时、不以玉树后庭之曲误江左之江山？醉梦者醒时已无国可守——此其哀。",
    voiceTag: "华赡",
    cast: [
      { id: "zhanglihua", name: "张丽华", role: "宠妃", voiceTag: "华赡" },
      { id: "kongfan", name: "孔范", role: "狎客·佞臣", voiceTag: "华赡" }
    ]
  },
  // ===== 北魏北周 =====
  wei_daowudi: {
    reignPremise: "代北鲜卑、初入中原，能否以离散部落之举、立封建之魏室？拓跋之兴在武，而其患亦在未能化胡为汉——此其初局。",
    voiceTag: "质朴",
    cast: [
      { id: "cuihong", name: "崔宏", role: "制礼之汉臣", voiceTag: "华赡" }
    ]
  },
  wei_taiwudi: {
    reignPremise: "雄略之主、一统北方，能否以灭佛之烈、强鲜卑之俗、抗南朝之文？武功盖世而刑戮过甚，统一者亦埋分裂之种——此其张力。",
    voiceTag: "冷峻",
    cast: [
      { id: "cuihao", name: "崔浩", role: "国史见诛者", voiceTag: "华赡" },
      { id: "tuobatao", name: "宗室宿将", role: "统军者", voiceTag: "质朴" }
    ]
  },
  wei_xiaowendi: {
    reignPremise: "迁都洛阳、易服改姓，能否以全盘汉化、熔胡汉为一炉、固百年之魏？化之深者其民附，而其衅亦生于代人之怨——此其大赌。",
    voiceTag: "华赡",
    cast: [
      { id: "tuobaxi", name: "拓跋禧", role: "反对汉化之宗室", voiceTag: "质朴" },
      { id: "lichong", name: "李冲", role: "汉化佐命", voiceTag: "华赡" }
    ]
  },
  beizhou_wudi: {
    reignPremise: "宇文篡西魏、灭佛崇儒，能否以关陇之基、灭北齐而启隋唐之先？灭佛者得兵农之众，而三教之争已伏——此其局。",
    voiceTag: "冷峻",
    cast: [
      { id: "yuwentai", name: "宇文泰", role: "关陇奠基者", voiceTag: "冷峻" },
      { id: "yangjian", name: "杨坚", role: "托孤之婿", voiceTag: "冷峻" }
    ]
  },
  // ===== 隋 =====
  sui_wendi: {
    reignPremise: "以外戚篡周、一天下而止数百年之裂，能否以开皇之俭、立千年相因之制？混一之业成于孤猜，而祸亦起于易储——此其张力。",
    voiceTag: "冷峻",
    cast: [
      { id: "gaojiong", name: "高颎", role: "谋主·见疏", voiceTag: "华赡" },
      { id: "yangsui", name: "杨素", role: "酷吏能臣", voiceTag: "冷峻" }
    ]
  },
  sui_yangdi: {
    reignPremise: "承文帝之富、欲以一人之雄心、通运河营东都取辽东，能否以功盖万世之役、不竭当世之民？大业者成亦炀、败亦炀——此其讽。",
    voiceTag: "华赡",
    cast: [
      { id: "yuwenhuaji", name: "宇文化及", role: "弑君之逆", voiceTag: "冷峻" },
      { id: "peiju", name: "裴矩", role: "逢迎西域者", voiceTag: "华赡" }
    ]
  },
  // ===== 唐（除太宗/高宗已铺）=====
  tang_gaozu: {
    reignPremise: "太原留守、因儿辈之逼而起兵，能否以迟暮之身、当开国之任、制将成之局？倡义在子而受禅在父，唐室之兴究竟谁之功——此其暧昧。",
    voiceTag: "华赡",
    cast: [
      { id: "peiji", name: "裴寂", role: "首谋之昵", voiceTag: "华赡" },
      { id: "lishimin", name: "李世民", role: "次子·天策", voiceTag: "华赡" }
    ]
  },
  tang_xuanzong: {
    reignPremise: "开元之治、天宝之乱，同一人而兼盛世之君与衰世之主，能否于梨园鼙鼓之间、不辜负少年揽辔之志？盛世之所由兴者正其所以亡——此其巨讽。",
    voiceTag: "华赡",
    cast: [
      { id: "yaoguanxiu", name: "姚崇", role: "开元贤相", voiceTag: "华赡" },
      { id: "lilianying", name: "李林甫", role: "口蜜腹剑", voiceTag: "冷峻" },
      { id: "yangguifei", name: "杨贵妃", role: "宠溺之祸", voiceTag: "华赡" }
    ]
  },
  tang_dezong: {
    reignPremise: "志削藩镇、初则奉天蒙尘，能否于姑息与强干之间、寻中兴之实？始疑而终信、始强而终柔，建中之政竟成后世积弱之样——此其憾。",
    voiceTag: "冷峻",
    cast: [
      { id: "luqi", name: "卢杞", role: "奸相·构陷", voiceTag: "冷峻" },
      { id: "liSheng", name: "李晟", role: "收复长安者", voiceTag: "冷峻" }
    ]
  },
  tang_xianzong: {
    reignPremise: "以贞观开元为志、力平僭叛之藩，能否以元和中兴、雪安史以来之耻？削藩者用兵而国疲，强主干者亦启阉祸——此其局。",
    voiceTag: "华赡",
    cast: [
      { id: "duyou", name: "杜佑", role: "通典之臣", voiceTag: "华赡" },
      { id: "peidu", name: "裴度", role: "平蔡之相", voiceTag: "华赡" }
    ]
  },
  tang_wenzong: {
    reignPremise: "慨然有除去阉宦之志、谋甘露而败，能否于北司之握兵、挽将坠之唐纲？天子欲除患而反为患所制，可为流涕者在此——此其悲。",
    voiceTag: "华赡",
    cast: [
      { id: "lixun", name: "李训", role: "甘露谋主", voiceTag: "华赡" },
      { id: "zhengzhutang", name: "郑注", role: "甘露共谋", voiceTag: "华赡" }
    ]
  },
  // ===== 后梁唐晋周 =====
  houliang_taizu: {
    reignPremise: "黄巢余孽、以篡唐起家，能否以盗贼之身、正九五之位、服中原之望？得国不以正者，其臣亦不以正视之——此其患。",
    voiceTag: "质朴",
    cast: [
      { id: "jingxiang", name: "敬翔", role: "谋臣", voiceTag: "华赡" }
    ]
  },
  houtang_zhuangzong: {
    reignPremise: "沙陀骁将、以三矢之誓灭梁，能否于十指之上、不溺伶人之戏、守创业之难？忧劳可以兴国、逸豫可以亡身，庄宗一身兼之——此其鉴。",
    voiceTag: "质朴",
    cast: [
      { id: "guoliang", name: "郭崇韬", role: "佐命·见杀", voiceTag: "华赡" },
      { id: "lingren", name: "伶人", role: "乱政者", voiceTag: "质朴" }
    ]
  },
  houtang_mingzong: {
    reignPremise: "蕃将无文、以兵变得国，能否以小康之政、稍苏五代之民？兵革之间、粗安即是恩，而嗣胤之祸已伏——此其幸与不幸。",
    voiceTag: "质朴",
    cast: [
      { id: "anChongHui", name: "安重诲", role: "权枢密", voiceTag: "冷峻" }
    ]
  },
  houjin_gaozu: {
    reignPremise: "借契丹之援、称儿皇帝而割燕云，能否以屈辱之盟、保一隅之位？石郎之辱，中原之耻，而契丹之患自此无已——此其痛。",
    voiceTag: "冷峻",
    cast: [
      { id: "jingyanguang", name: "景延广", role: "主战召祸者", voiceTag: "冷峻" }
    ]
  },
  houzhou_taizu: {
    reignPremise: "郭威以兵变立周、约法恤民，能否于五代之季、开粗安之局、为混一者铺路？乱世之良吏，而天不假年——此其惜。",
    voiceTag: "质朴",
    cast: [
      { id: "chaiRong", name: "柴荣", role: "养子·继业", voiceTag: "冷峻" }
    ]
  },
  houzhou_shizong: {
    reignPremise: " ten载天子、志在一统，能否以高平之锐、南征北伐、完周公未竟之业？惜乎在位日浅，而赵氏之篡已在肘腋——此其憾。",
    voiceTag: "冷峻",
    cast: [
      { id: "wangPu", name: "王朴", role: "平边策者", voiceTag: "华赡" },
      { id: "zhaoKuangyin", name: "赵匡胤", role: "殿前都点检", voiceTag: "冷峻" }
    ]
  },
  // ===== 宋（除太祖/太宗/真宗/仁宗/神宗/哲宗/徽宗/钦宗/高宗/孝宗/宁宗/理宗/帝昺 见下或已有）=====
  // 注：song_taizu/song_taizong/song_zhenzong/song_renzong/song_shenzong/song_zhezong/song_huizong/song_qinzong/song_gaozong/song_xiaozong/song_ningzong/song_lizong/song_dibing 在下方单独列出
  // ===== 辽 =====
  liao_taizu: {
    reignPremise: "契丹八部之雄、建元称帝，能否以草原之俗、立兼治农牧之辽？胡汉分治者得长久，而兄弟相及之制已伏内争——此其局。",
    voiceTag: "质朴",
    cast: [
      { id: "yeluucha", name: "耶律曷鲁", role: "佐命·迭剌", voiceTag: "质朴" }
    ]
  },
  liao_taizong: {
    reignPremise: "援石晋而取燕云、遂入中原，能否以契丹之兵、守汉地之民心？得之易而守之难，打草谷之虐终使胡马北还——此其诫。",
    voiceTag: "质朴",
    cast: [
      { id: "zhangli", name: "张砺", role: "汉臣·见疏", voiceTag: "华赡" }
    ]
  },
  liao_shengzong: {
    reignPremise: "幼冲嗣位、承萧后之政，能否以澶渊之盟、开宋辽百年之太平？以战迫和、以和养民，北朝之盛在此——此其智。",
    voiceTag: "华赡",
    cast: [
      { id: "xiaochuohou", name: "萧绰", role: "承天太后", voiceTag: "华赡" },
      { id: "handerang", name: "韩德让", role: "汉相·宠任", voiceTag: "华赡" }
    ]
  },
  liao_xingzong: {
    reignPremise: "母后临朝、躬亲政后渐尚浮奢，能否于番汉之间、守圣宗之成规？守成易而励精难，辽之衰象已见于此——此其渐。",
    voiceTag: "华赡",
    cast: [
      { id: "zhaoguoren", name: "赵国君", role: "权幸", voiceTag: "冷峻" }
    ]
  },
  // ===== 金 =====
  jin_taizu: {
    reignPremise: "完颜部之雄、起兵叛辽，能否以苦寒之众、灭百年之契丹、与宋鼎足？阿骨打之兴在誓，而灭辽之锐亦启伐宋之贪——此其势。",
    voiceTag: "质朴",
    cast: [
      { id: "wanyanxieye", name: "完颜斜也", role: "弟·国论", voiceTag: "质朴" }
    ]
  },
  jin_taizong: {
    reignPremise: "继兄之业、灭辽俘宋，能否以草创之制、治两河新附之民？取之骤者理之疏，而伪齐之设已见羁縻之困——此其初。",
    voiceTag: "质朴",
    cast: [
      { id: "wolibu", name: "完颜斡离不", role: "伐宋统军", voiceTag: "质朴" }
    ]
  },
  jin_hailingwang: {
    reignPremise: "弑君自立、迁都燕京而图混一，能否以暴厉之才、并南宋而成一统？弑逆者失其本，采石一败而身死瓜洲——此其狂与戮。",
    voiceTag: "冷峻",
    cast: [
      { id: "tudan", name: "徒单氏", role: "后族", voiceTag: "冷峻" }
    ]
  },
  jin_shizong: {
    reignPremise: "起于海陵之乱、以节俭守成，能否以小尧舜之政、苏海陵所弊之金？拨乱易而反奢难，北地之安在此一代——此其贤。",
    voiceTag: "华赡",
    cast: [
      { id: "shizongchen", name: "守成旧臣", role: "谏议者", voiceTag: "华赡" }
    ]
  },
  jin_zhangzong: {
    reignPremise: "承世宗之盛、文雅好儒，能否以承平之治、不坠武备、备蒙古之将兴？治文而弛武，泰和之安恰邻大患——此其危。",
    voiceTag: "华赡",
    cast: [
      { id: "tudan", name: "徒单镒", role: "宗室贤相", voiceTag: "华赡" }
    ]
  },
  jin_aizong: {
    reignPremise: "承衰末之运、欲振而不可为，能否于蔡州围城之中、存金室最后一节？君死社稷、臣殉其难，而百年之金竟亡于野旷——此其烈。",
    voiceTag: "冷峻",
    cast: [
      { id: "wanyanchenghui", name: "完颜承晖", role: "殉国大臣", voiceTag: "冷峻" }
    ]
  },
  // ===== 西夏 =====
  xixia_jingzong: {
    reignPremise: "党项拓跋、脱宋自立、创西夏文字，能否以一隅之羌、立于宋辽金之间而不亡？小国周旋于强邻，而兴州之业赖此——此其智。",
    voiceTag: "质朴",
    cast: [
      { id: "yeli", name: "野利氏", role: "后族·谋臣", voiceTag: "质朴" }
    ]
  },
  // ===== 元 =====
  yuan_taizong: {
    reignPremise: "拖雷之子、承成吉思汗之穹庐，能否以兄弟叔侄之猜、定大汗之继、竟灭金之业？中原之得在兵，而争位之衅已启——此其局。",
    voiceTag: "质朴",
    cast: [
      { id: "yilihuozhen", name: "耶律楚材", role: "治汉地者", voiceTag: "华赡" }
    ]
  },
  yuan_xianzong: {
    reignPremise: "蒙哥汗、以攻蜀而陨钓鱼城，能否以大汗之威、竟平宋之未尽？天不假年，而忽必烈之代已兆——此其变。",
    voiceTag: "质朴",
    cast: [
      { id: "hubilie", name: "忽必烈", role: "弟·总漠南", voiceTag: "华赡" }
    ]
  },
  yuan_wenzong: {
    reignPremise: "两都之争中即位、雅好文事，能否于骨肉相屠之后、以文饰武、安衅端未息之朝？夺位者修书而难弭仇，元之衰由此深——此其讽。",
    voiceTag: "华赡",
    cast: [
      { id: "saitemuer", name: "燕铁木儿", role: "拥立之权臣", voiceTag: "冷峻" }
    ]
  },
  yuan_huizong: {
    reignPremise: "承末造之运、用番僧而怠政，能否于红巾四起、群雄并逐之中、保大都之孤灯？天子北遁、元亡而朔漠之元犹存——此其终。",
    voiceTag: "冷峻",
    cast: [
      { id: "tuotuohuashi", name: "脱脱", role: "更化又见疏", voiceTag: "华赡" }
    ]
  },
  // ===== 明（仁宗/宣宗/孝宗 见下）=====
  // ===== 清（太宗 见下）=====
  qing_taizong: {
    reignPremise: "继父之业、改国号为清、侵朝鲜伐明朝，能否以守成兼开拓、完入主中原之前局？绕道蒙古、不入山海关而撼明边，大谋已定——此其雄。",
    voiceTag: "质朴",
    cast: [
      { id: "hongtaiji", name: "多尔衮", role: "弟·摄政", voiceTag: "冷峻" },
      { id: "fanwencheng", name: "范文程", role: "汉谋", voiceTag: "华赡" }
    ]
  }
};
