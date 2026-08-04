# -*- coding: utf-8 -*-
"""G2 汉新三国 皇帝事件库 生成器 - 第二部分：东汉+三国"""

def build_part2():
    emperors = []

    # ========== 东汉 ==========

    # 1. 汉光武帝 刘秀 (A)
    emperors.append({
        "id": "han_guangwudi",
        "dynasty": "汉",
        "name": "刘秀",
        "templeName": "汉光武帝",
        "reignStart": 25, "reignEnd": 57,
        "evaluation": "再造汉室，柔道治天下",
        "background": "景帝九世孙，起于春陵。新莽末年与兄縯起兵，初属更始。昆阳一战破莽百万之师。后渡河招抚河北，自立为帝，定都洛阳，史称东汉。十二年平定群雄，统一天下。",
        "initStats": {"treasury": 55, "people": 50, "military": 75, "court": 70, "health": 72, "tech": 30},
        "eraContext": "新莽乱后天下分崩，群雄割据。光武起于微末，以河北为基，平定赤眉、隗嚣、公孙述等。统一后退功臣进文吏，柔道治国，偃武修文，外戚与功臣并用。",
        "tier": "A",
        "events": [
            {"year": 25, "month": 6, "title": "鄗城称帝", "description": "光武平定河北，诸将劝进。光武辞之再三，乃于鄗南千秋亭即皇帝位，改元建武。燔燎告天禋于六宗望于群神，建汉家社稷于洛阳。", "historicalChoice": 0, "choices": ["即帝位鄗城，改元建武", "奉更始为帝，自居藩辅", "立宗室长者以续正统", "缓即位以观天下之势", "都邺城以制中原"], "historicalOutcome": "光武称帝建元，开东汉二百年基业"},
            {"year": 25, "month": 10, "title": "定都洛阳", "description": "光武入洛阳，遂定都焉。时更始降赤眉，赤眉入长安。光武遣邓禹西入关击赤眉，自定关东。洛阳居天下之中，漕运四通，遂为帝都。", "historicalChoice": 0, "choices": ["定都洛阳，居中以制四方", "都长安以继西汉正统", "都邺城以据河北根本", "都南阳以近故里", "两京并立以备不虞"], "historicalOutcome": "光武定都洛阳，东汉因称后汉"},
            {"year": 27, "month": null, "title": "赤眉降汉", "description": "赤眉入长安粮尽东归，光武遣冯异击之于华阴。赤眉逢大雪，樊崇等奉更始传国玺降于光武。光武赐樊崇等田宅，后竟诛之。", "historicalChoice": 0, "choices": ["受赤眉降，安置樊崇等", "尽诛赤眉以绝后患", "收赤眉为军以充兵力", "赦其众而散归乡里", "令赤眉击隗嚣以将功赎罪"], "historicalOutcome": "赤眉降汉，关中渐定"},
            {"year": 30, "month": null, "title": "平定关东", "description": "光武遣将平定关东群雄。耿弇破张步于齐，岑彭破秦丰于南阳，朱祐破董宪于东海。关东既平，乃专意西伐隗嚣公孙述。", "historicalChoice": 0, "choices": ["遣将分路平定关东", "亲征关东以速定之", "招降关东群雄以息兵", "令功臣各镇一方", "缓图关东先定西陲"], "historicalOutcome": "关东平，光武专意西伐"},
            {"year": 32, "month": null, "title": "得陇望蜀", "description": "光武亲征隗嚣于陇右，嚣将高峻降。岑彭进军破蜀将田戎于荆门。光武诏岑彭曰人苦不知足，既平陇复望蜀。遂图公孙述。", "historicalChoice": 0, "choices": ["亲征陇右，乘胜图蜀", "令岑彭专征蜀地", "招降公孙述以罢兵", "守陇而不进蜀", "令隗嚣旧部伐蜀"], "historicalOutcome": "光武平陇望蜀，统一在即"},
            {"year": 36, "month": null, "title": "灭公孙述", "description": "岑彭、吴汉伐蜀。彭为刺客所杀，汉代之。汉入成都，纵兵大掠，杀公孙述妻族。光武怒责之。蜀地平，天下一统。", "historicalChoice": 0, "choices": ["遣吴汉灭蜀，统一天下", "招降公孙述以安蜀民", "令岑彭缓图蜀地", "罢兵蜀地待其自乱", "令蜀将自相攻伐"], "historicalOutcome": "吴汉灭公孙述，天下一统"},
            {"year": 37, "month": null, "title": "退功臣进文吏", "description": "天下既平，光武退功臣以列侯就第，不以吏职任之。贾复邓禹等皆去兵权，崇经术修儒雅。功臣得保首领，文吏进用，开东汉右文之政。", "historicalChoice": 0, "choices": ["退功臣就第，进文吏治国", "任功臣为郡守以镇四方", "令功臣典兵备边", "杂用功臣文吏", "削功臣爵位以收权"], "historicalOutcome": "退功臣进文吏，东汉功臣得全"},
            {"year": 39, "month": null, "title": "度田令", "description": "光武下诏度田，核实天下垦田户口。河南南阳帝乡多近臣，刺史太守不敢核实。光武遣使按验，杀河南尹张伋等十余人。度田终未竟。", "historicalChoice": 0, "choices": ["严行度田，杀抗拒者以立威", "宽行度田以安豪强", "罢度田以免激变", "令豪强自占田以省纷争", "增田租以代度田"], "historicalOutcome": "度田令遭豪强抵抗，杀守令十余人终未竟"},
            {"year": 43, "month": null, "title": "废郭后立阴", "description": "光武废郭皇后为中山王太后，立贵人阴氏为皇后。废太子强为东海王，立阳为皇太子，即后来的明帝。强让太子之位，光武许之。", "historicalChoice": 0, "choices": ["废郭立阴，改易储君", "固立郭后太子以正名分", "两宫并尊以息争", "令群臣议废立之事", "缓议以观后嗣"], "historicalOutcome": "废郭立阴，东海王让太子之位"},
            {"year": 48, "month": null, "title": "匈奴分裂", "description": "匈奴分裂为南北，南匈奴八部立比为呼韩邪单于，请内附。光武议之，耿国请如宣帝故事受其降。南匈奴入居塞内，为汉藩屏。", "historicalChoice": 0, "choices": ["纳南匈奴内附为藩屏", "拒南匈奴令其自存", "纳南匈奴而徙之远方", "令南匈奴击北匈奴", "厚赂南匈奴而不纳附"], "historicalOutcome": "南匈奴内附，北匈奴孤弱"},
            {"year": 50, "month": null, "title": "营建太学", "description": "光武起太学于洛阳，复置五经博士。四方学者云集京师，诸生横经受业。又访求雅乐，修明堂辟雍灵台，复兴礼乐之制。", "historicalChoice": 0, "choices": ["营太学，复五经博士", "广立郡国学校以教天下", "罢博士唯留实用之学", "征名儒入朝不立太学", "以私学代官学以省费"], "historicalOutcome": "太学立，儒风大振，东汉文教兴"},
            {"year": 57, "month": 2, "title": "光武崩", "description": "光武崩于南宫，年六十二。遗诏薄葬。太子庄嗣位为明帝。光武再造汉室，柔道治国，与民休息，开建武、永平之治。", "historicalChoice": 0, "choices": ["太子庄嗣位，承光武之业", "令太后辅政以固幼主", "择宗室长者摄政", "令功臣共辅太子", "遗命重臣辅政以制外戚"], "historicalOutcome": "明帝嗣位承光武之业，开永平之治"},
        ],
    })

    # 2. 汉明帝 刘庄 (A)
    emperors.append({
        "id": "han_mingdi",
        "dynasty": "汉",
        "name": "刘庄",
        "templeName": "汉明帝",
        "reignStart": 57, "reignEnd": 75,
        "evaluation": "遵奉建武，永平之治",
        "background": "光武第四子，母阴皇后。初名阳，立为太子后改名庄。即位后遵奉建武之政，吏得其职，海内安宁，与民休息，称为永平之治。",
        "initStats": {"treasury": 65, "people": 65, "military": 65, "court": 72, "health": 68, "tech": 32},
        "eraContext": "光武之后天下初定，外戚与功臣并用。明帝崇儒重法，限制外戚阴氏马氏。北匈奴寇边，西域诸国盼汉保护。佛教始入中国。",
        "tier": "A",
        "events": [
            {"year": 58, "month": null, "title": "遵奉建武", "description": "明帝即位，遵奉建武之政，后妃之家不得封侯。东平王苍为骠骑将军辅政，明帝友悌，待苍甚厚。苍数辞辅政，明帝乃听之。", "historicalChoice": 0, "choices": ["遵建武旧制，限外戚封侯", "厚封外戚以固根本", "任用宗室辅政以制外戚", "令功臣共辅以分其权", "亲揽万机不假人权"], "historicalOutcome": "明帝遵建武之制，外戚不得封侯"},
            {"year": 60, "month": null, "title": "图功臣云台", "description": "明帝思中兴之功，图画建武名臣二十八将于南宫云台，号云台二十八将。又益王常等四人，合三十二人。邓禹为首，马援以椒房之亲独不与。", "historicalChoice": 0, "choices": ["图功臣云台，不预椒房亲", "图功臣并及马援以全功", "罢图功臣以省浮费", "令功臣后人世袭其爵", "厚赐功臣后人以酬先朝"], "historicalOutcome": "云台二十八将图成，马援以亲不预"},
            {"year": 64, "month": null, "title": "遣使天竺", "description": "帝闻西域有佛，遣郎中蔡愔、博士弟子秦景使天竺求之。愔等至大月氏，遇沙门迦叶摩腾、竺法兰，得佛经四十二章及释迦立像，以白马驮归洛阳。", "historicalChoice": 0, "choices": ["遣使天竺求佛法", "禁佛以正中国之教", "令沙门自行传法不遣使", "厚赂西域以求佛经", "缓求佛法先定北边"], "historicalOutcome": "佛教始入中国，白马寺立"},
            {"year": 65, "month": null, "title": "楚王英案", "description": "楚王英好黄老浮屠，为浮屠斋戒祭祀。英后坐谋逆废徙丹阳，自杀。明帝穷治楚狱，连逮数千人，系狱者岁余。寒朗力辩其冤，帝感悟，多所赦出。", "historicalChoice": 0, "choices": ["穷治楚狱，后纳寒朗之谏", "宽宥楚王以全骨肉", "严惩首恶而不株连", "令群臣公议楚王之罪", "赦楚王复其国以安宗室"], "historicalOutcome": "楚王英自杀，株连数千人后多赦出"},
            {"year": 66, "month": null, "title": "北匈奴寇边", "description": "北匈奴数寇边，河西郡县白日闭门。明帝欲遵武帝故事击之，议者以为天下初定不宜用兵。耿秉请击之，明帝纳其议，图谋北伐。", "historicalChoice": 0, "choices": ["谋击北匈奴以安边", "守边不出待其内乱", "令南匈奴击北匈奴", "遣使和亲以缓边衅", "徙边民于内地以避祸"], "historicalOutcome": "明帝谋击北匈奴，后遣窦固出塞"},
            {"year": 73, "month": null, "title": "窦固击匈奴", "description": "明帝遣耿秉窦固出击北匈奴。固至天山击呼衍王，取伊吾卢地。假司马班超从军，超使西域，以三十六人镇鄯善于窴，西域诸国遣子入侍。", "historicalChoice": 0, "choices": ["遣窦固击匈奴，令班超使西域", "令窦固专征不遣班超", "守边不出待匈奴内乱", "令南匈奴击北匈奴", "招降西域诸国以制匈奴"], "historicalOutcome": "窦固取伊吾，班超通西域"},
            {"year": 74, "month": null, "title": "复西域都护", "description": "窦固破车师，复置西域都护戊己校尉。以陈睦为都护，耿恭关宠为戊己校尉屯车师。明帝崩后焉耆龟兹反，杀都护，耿恭困守疏勒。", "historicalChoice": 0, "choices": ["复西域都护，屯兵车师", "令西域诸国为属国不设官", "罢西域以省军费", "令班超专镇西域", "分封西域诸王以分其势"], "historicalOutcome": "复西域都护，明帝崩后旋失"},
            {"year": 75, "month": 8, "title": "明帝崩", "description": "明帝崩于东宫，遗诏无起寝庙。太子炟嗣位为章帝。明帝永平之政，海内安宁，户口岁增，与光武并称建武永平之治。", "historicalChoice": 0, "choices": ["太子炟嗣位，承永平之业", "令太后辅政以固幼主", "择宗室长者摄政", "令功臣共辅太子", "遗命东平王苍辅政"], "historicalOutcome": "章帝嗣位承永平之业，东汉极盛"},
        ],
    })

    # 3. 汉章帝 刘炟 (B)
    emperors.append({
        "id": "han_zhangdi",
        "dynasty": "汉",
        "name": "刘炟",
        "templeName": "汉章帝",
        "reignStart": 75, "reignEnd": 88,
        "evaluation": "宽厚长者，章和之治",
        "background": "明帝第五子，母贾贵人，养于马皇后。即位后宽厚仁恕，与民休息。班超定西域，白虎观议经，东汉称极盛。",
        "initStats": {"treasury": 68, "people": 68, "military": 60, "court": 65, "health": 60, "tech": 32},
        "eraContext": "明章之际东汉极盛。章帝宽厚，外戚马氏窦氏并用。班超经营西域五十余国皆降。白虎观议经统一经学。然宽纵渐生，外戚窦氏渐起。",
        "tier": "B",
        "events": [
            {"year": 77, "month": null, "title": "班超西域", "description": "班超在西域以少击众，镇鄯善于窴疏勒。章帝初欲召超还，超留疏勒。超率西域诸国兵击莎车龟兹，西域五十余国皆遣质子内属。", "historicalChoice": 0, "choices": ["令班超留西域经营诸国", "召班超还以省军费", "增兵西域助班超", "令西域诸国自相制衡", "罢西域以息民力"], "historicalOutcome": "班超定西域五十余国皆降汉"},
            {"year": 79, "month": null, "title": "白虎观议", "description": "章帝诏诸儒集白虎观议五经同异，如石渠故事。侍中丁鸿、太常楼望等参与，班固撰集其议为《白虎通义》。亲称制临决，经学统一。", "historicalChoice": 0, "choices": ["集白虎观议经，亲制临决", "广立诸家博士不专一", "罢诸说独立一统", "令郡国各立学官", "以谶纬决经义之异"], "historicalOutcome": "白虎观议经，《白虎通义》成"},
            {"year": 84, "month": null, "title": "外戚窦氏", "description": "章帝立窦勋女为皇后，窦氏渐盛。窦皇后无子，养太子肇。窦皇后兄窦宪为大司马，外戚窦氏自此渐起，终成东汉外戚之祸。", "historicalChoice": 0, "choices": ["立窦氏为后，开窦氏外戚", "另择良家女为后以远外戚", "限窦氏之权不授要职", "令群臣议选皇后", "立宗室女以正名分"], "historicalOutcome": "窦氏为后，外戚窦氏渐起"},
            {"year": 86, "month": null, "title": "宽厚之政", "description": "章帝宽厚仁恕，每存宽宥。孔僖以直谏得幸，章帝不罪。然政尚宽简，禁纲渐弛，外戚宦官渐萌。后世以为宽有过之。", "historicalChoice": 0, "choices": ["尚宽简以与民休息", "申明法纪以严纲纪", "宽猛相济以适中道", "令御史严察百官", "增刑罚以止奸"], "historicalOutcome": "章帝宽厚，然禁网渐弛"},
            {"year": 88, "month": 2, "title": "章帝崩", "description": "章帝崩于章德前殿，太子肇嗣位为和帝，年十岁。窦太后临朝，窦宪辅政。章帝宽厚之政虽称章和之治，然外戚窦氏自此专权。", "historicalChoice": 0, "choices": ["太子肇嗣位，窦太后临朝", "择宗室长者摄政", "令功臣共辅幼主", "令东平王苍辅政", "缓即位以观时变"], "historicalOutcome": "和帝嗣位年幼，窦太后临朝称制"},
        ],
    })

    # 4. 汉和帝 刘肇 (B)
    emperors.append({
        "id": "han_hedi",
        "dynasty": "汉",
        "name": "刘肇",
        "templeName": "汉和帝",
        "reignStart": 88, "reignEnd": 105,
        "evaluation": "诛窦氏，亲揽万机",
        "background": "章帝第四子，母梁贵人，养于窦皇后。十岁即位，窦太后临朝，窦宪辅政。后与宦官郑众谋诛窦氏，亲揽万机。班超定西域，蔡伦造纸。",
        "initStats": {"treasury": 65, "people": 65, "military": 62, "court": 55, "health": 55, "tech": 33},
        "eraContext": "窦宪辅政大破北匈奴，然专权跋扈。和帝年长，与宦官郑众谋诛窦氏。宦官用事自此始。班超经营西域，甘英使大秦。蔡伦改进造纸。",
        "tier": "B",
        "events": [
            {"year": 89, "month": null, "title": "窦宪破匈奴", "description": "窦宪将兵击北匈奴，大破之于稽落山，登燕然山刻石勒功。北匈奴单于远遁，窦宪威震天下，拜大将军位三公上。", "historicalChoice": 0, "choices": ["令窦宪击匈奴以立威", "守边不令窦宪专征", "令南匈奴击北匈奴", "招降北匈奴以罢兵", "亲征以振军威"], "historicalOutcome": "窦宪破北匈奴勒石燕然，威震天下"},
            {"year": 92, "month": null, "title": "诛窦氏", "description": "窦宪谋逆，和帝与宦官郑众谋，收宪大将军印绶，迫令自杀。窦氏宗族皆免归故郡。和帝始亲揽万机，以郑众为大长秋，宦官用事自此始。", "historicalChoice": 0, "choices": ["用宦官郑众诛窦氏", "用儒臣诛窦氏以远宦官", "宽赦窦氏以安外戚", "令功臣共议窦氏之罪", "废窦后以绝其根"], "historicalOutcome": "和帝诛窦氏亲政，宦官用事自此始"},
            {"year": 97, "month": null, "title": "甘英使大秦", "description": "班超遣掾甘英使大秦，至条支临西海。安息西界船人谓英曰海水广大往来者逢善风三月乃得渡，英乃还。大秦通汉之愿未遂。", "historicalChoice": 0, "choices": ["令班超遣甘英使大秦", "罢使大秦以省劳费", "增兵西域以通商路", "令西域诸国通使大秦", "厚赂安息以通大秦"], "historicalOutcome": "甘英至西海而还，大秦未通"},
            {"year": 102, "month": null, "title": "班超归汉", "description": "班超在西域三十一年，年老思归，上书乞生入玉门关。妹昭亦上书代请。和帝征超还，超至洛阳月余病卒。西域都护任尚代之。", "historicalChoice": 0, "choices": ["征班超还，以任尚代之", "令班超留西域终老", "增援班超以固西域", "令班超子勇代父之任", "罢西域以息军费"], "historicalOutcome": "班超归汉月余卒，任尚代之不能抚"},
            {"year": 105, "month": null, "title": "蔡伦造纸", "description": "中常侍蔡伦用树皮麻头敝布鱼网造纸，奏上和帝。帝善其能，自是天下莫不从用，称蔡侯纸。造纸术自此始。和帝崩，殇帝立。", "historicalChoice": 0, "choices": ["用蔡伦造纸以广文教", "禁造纸以守竹帛旧制", "令蔡伦改进纸以充军用", "厚赐蔡伦而不推广", "令郡国自造纸以省费"], "historicalOutcome": "蔡伦造纸天下从用，文教大盛"},
            {"year": 105, "month": 12, "title": "和帝崩", "description": "和帝崩于章德前殿，少子隆生始百余日嗣位为殇帝。和帝诛窦氏亲政，然宦官用事，东汉宦官外戚之争自此起。", "historicalChoice": 0, "choices": ["少子隆嗣位为殇帝", "择宗室长者入继", "令太后邓氏临朝称制", "令功臣共辅幼主", "缓立储以观时变"], "historicalOutcome": "殇帝立生百余日，邓太后临朝"},
        ],
    })

    # 5. 汉殇帝 刘隆 (B)
    emperors.append({
        "id": "han_shangdi",
        "dynasty": "汉",
        "name": "刘隆",
        "templeName": "汉殇帝",
        "reignStart": 105, "reignEnd": 106,
        "evaluation": "婴儿天子，在位八月",
        "background": "和帝少子，生始百余日即位。邓太后临朝称制。在位八月而崩，年二岁。迎立安帝。",
        "initStats": {"treasury": 60, "people": 60, "military": 55, "court": 40, "health": 30, "tech": 33},
        "eraContext": "殇帝婴孺，邓太后临朝。邓骘辅政，外戚邓氏专权。羌人叛于西陲，用兵连年。东汉始衰。",
        "tier": "B",
        "events": [
            {"year": 106, "month": null, "title": "邓太后临朝", "description": "殇帝生百余日即位，邓太后临朝称制。太后兄邓骘为车骑将军辅政。邓太后有才略，然外戚邓氏自此专权。", "historicalChoice": 0, "choices": ["令邓太后临朝，邓骘辅政", "择宗室长者摄政", "令功臣共辅幼主", "废殇帝立长者以亲政", "缓临朝以观时变"], "historicalOutcome": "邓太后临朝称制，邓氏专权"},
            {"year": 106, "month": null, "title": "西羌之叛", "description": "先零羌滇零叛，自称天子于北地。寇三辅，断陇道。邓骘将兵击之，大败。羌祸自此连年，东汉军费大增，国用渐匮。", "historicalChoice": 0, "choices": ["遣邓骘击羌以平叛", "招降羌人以息兵", "徙边民于内地以避祸", "令凉州豪族自募兵御羌", "和亲羌人以缓边衅"], "historicalOutcome": "邓骘败于羌，西陲大乱"},
            {"year": 106, "month": 8, "title": "殇帝崩", "description": "殇帝崩于襁褓，年二岁。邓太后与邓骘迎章帝孙清河王庆子祐入继，是为安帝。邓太后仍临朝称制，直至死。", "historicalChoice": 0, "choices": ["迎清河王子祐入继为安帝", "择章帝他孙入继", "立和帝他子以续正统", "令群臣议择宗室贤者", "立宗室长者亲政"], "historicalOutcome": "安帝入继，邓太后仍临朝称制"},
        ],
    })

    # 6. 汉安帝 刘祜 (B)
    emperors.append({
        "id": "han_andi",
        "dynasty": "汉",
        "name": "刘祜",
        "templeName": "汉安帝",
        "reignStart": 106, "reignEnd": 125,
        "evaluation": "昏庸之主，外戚宦官并用",
        "background": "章帝孙，清河王刘庆之子。殇帝崩，邓太后迎立之。在位二十年，前为邓太后所制，后宠阎皇后，宦官用事。西域叛弃，西羌连年。",
        "initStats": {"treasury": 50, "people": 50, "military": 45, "court": 40, "health": 50, "tech": 33},
        "eraContext": "邓太后临朝十六年，邓氏专权。太后崩后安帝亲政，诛邓氏用阎氏。班勇复通西域。宦官樊丰等用事，朝政大乱。羌祸连年国用匮。",
        "tier": "B",
        "events": [
            {"year": 107, "month": null, "title": "罢西域都护", "description": "西域诸国叛，攻都护任尚。安帝从群臣议罢西域都护，征还班勇。西域自此绝汉五十余年，北匈奴复寇河西。", "historicalChoice": 0, "choices": ["罢西域都护以省军费", "增兵西域以固藩屏", "令班勇留西域经营", "招降西域诸国以罢兵", "徙河西民于内地以避祸"], "historicalOutcome": "罢西域都护，西域弃汉五十余年"},
            {"year": 121, "month": null, "title": "邓氏败阎氏起", "description": "邓太后崩，安帝亲政。有司奏邓氏谋逆，废邓皇后，邓骘免官自杀，邓氏宗族免归故郡。立阎姬为皇后，阎氏外戚起。", "historicalChoice": 0, "choices": ["诛邓氏，立阎氏为后", "宽赦邓氏以安外戚", "抑外戚用儒臣辅政", "令群臣共辅以分其权", "留邓氏辅政以酬旧功"], "historicalOutcome": "邓氏败阎氏起，外戚之祸不已"},
            {"year": 123, "month": null, "title": "班勇复通西域", "description": "班勇请复通西域，安帝以勇为西域长史将兵五百人出屯柳中。勇破车师降焉耆龟兹，西域复通。然汉威不及班超时。", "historicalChoice": 0, "choices": ["遣班勇复通西域", "罢西域不复通", "增兵西域助班勇", "令西域诸国自相制衡", "招降北匈奴以通西域"], "historicalOutcome": "班勇复通西域，然汉威不及前"},
            {"year": 124, "month": null, "title": "废太子保", "description": "安帝宠阎皇后，皇后谮太子保之母王圣。安帝废太子保为济阴王。阎皇后欲立幼弱以专权。朝臣多谏不能入。", "historicalChoice": 0, "choices": ["废太子保为济阴王", "固立太子保以正名分", "令群臣议废立之事", "缓议储位以待时", "立宗室他子入继"], "historicalOutcome": "废太子保，阎氏欲立幼弱专权"},
            {"year": 125, "month": 3, "title": "安帝崩", "description": "安帝崩于叶县，阎皇后与兄阎显迎立北乡侯懿为少帝。懿立二百余日崩。宦官孙程等诛阎氏，迎济阴王保入继，是为顺帝。", "historicalChoice": 0, "choices": ["阎氏立北乡侯懿为少帝", "迎济阴王保入继亲政", "择宗室长者摄政", "令群臣共辅以分其权", "立宗室他子入继"], "historicalOutcome": "北乡侯立旋崩，宦官迎顺帝"},
        ],
    })

    # 7. 汉少帝 北乡侯懿 (B)
    emperors.append({
        "id": "han_shaodi_yi",
        "dynasty": "汉",
        "name": "刘懿",
        "templeName": "汉少帝（北乡侯）",
        "reignStart": 125, "reignEnd": 125,
        "evaluation": "阎氏所立，在位七月",
        "background": "章帝孙，济北王刘寿之子。安帝崩，阎皇后与兄阎显迎立之。在位七月而崩。宦官孙程等诛阎氏，迎顺帝。",
        "initStats": {"treasury": 48, "people": 48, "military": 42, "court": 35, "health": 40, "tech": 33},
        "eraContext": "阎氏专权立幼弱。宦官孙程等十九侯谋诛阎氏。东汉宦官外戚之争至此烈。",
        "tier": "B",
        "events": [
            {"year": 125, "month": 4, "title": "阎氏立帝", "description": "安帝崩于南巡途。阎皇后与兄显密谋，迎立北乡侯懿为帝。阎太后临朝称制，阎显辅政，杀安帝亲信以固权。", "historicalChoice": 0, "choices": ["阎氏立北乡侯以专权", "迎济阴王保入继亲政", "择宗室长者摄政", "令群臣议择宗室贤者", "立章帝他孙以续正统"], "historicalOutcome": "阎氏立少帝专权，朝议汹汹"},
            {"year": 125, "month": 10, "title": "少帝崩", "description": "少帝懿立七月而崩。宦官孙程等十九人谋诛阎氏，迎济阴王保入继为顺帝。阎显等伏诛，阎太后迁离宫。", "historicalChoice": 0, "choices": ["宦官迎顺帝，诛阎氏", "令功臣诛阎氏迎顺帝", "阎氏另立宗室以专权", "令群臣共议择贤而立", "立章帝他孙以续正统"], "historicalOutcome": "宦官孙程等诛阎氏迎顺帝，十九侯封"},
        ],
    })

    # 8. 汉顺帝 刘保 (B)
    emperors.append({
        "id": "han_shundi",
        "dynasty": "汉",
        "name": "刘保",
        "templeName": "汉顺帝",
        "reignStart": 125, "reignEnd": 144,
        "evaluation": "宦官拥立，梁氏渐起",
        "background": "安帝太子，废为济阴王。北乡侯崩，宦官孙程等诛阎氏迎立之。在位二十年，宦官十九侯用事，后立梁皇后，梁氏外戚渐起。",
        "initStats": {"treasury": 52, "people": 52, "military": 48, "court": 42, "health": 50, "tech": 33},
        "eraContext": "宦官拥立顺帝，十九侯用事。后立梁皇后，兄梁商辅政，梁冀继之。宦官外戚并用，朝政渐乱。张衡制浑天仪地动仪。",
        "tier": "B",
        "events": [
            {"year": 126, "month": null, "title": "十九侯封", "description": "孙程等十九宦官诛阎氏迎顺帝，皆封列侯，号十九侯。宦官用事自此盛，与外戚并擅朝政。虞诩等屡谏不能入。", "historicalChoice": 0, "choices": ["封十九侯以酬拥立之功", "厚赐宦官而不封侯", "抑宦官用儒臣辅政", "令功臣共辅以分其权", "诛宦官以正朝纲"], "historicalOutcome": "十九侯封，宦官专权自此盛"},
            {"year": 132, "month": null, "title": "立梁皇后", "description": "顺帝立梁商女为皇后，梁商为大将军辅政。商死后子冀嗣，梁氏外戚自此渐盛，终成东汉最大外戚之祸。", "historicalChoice": 0, "choices": ["立梁氏为后，开梁氏外戚", "另择良家女为后以远外戚", "限梁氏之权不授要职", "令群臣议选皇后", "立宗室女以正名分"], "historicalOutcome": "梁氏为后，外戚梁氏渐起"},
            {"year": 136, "month": null, "title": "张纲八使", "description": "顺帝遣张纲等八使分行天下，纠察贪墨。纲埋车轮于洛阳都亭曰豺狼当道安问狐狸，劾大将军梁冀兄弟。顺帝不能用。", "historicalChoice": 0, "choices": ["遣八使纠察，然不能用其言", "重用张纲以抑梁氏", "罢八使以安权贵", "令御史常察百官", "厚赐张纲而不纳其谏"], "historicalOutcome": "张纲劾梁冀不能用，外戚益横"},
            {"year": 141, "month": null, "title": "梁冀执政", "description": "大将军梁商薨，子冀嗣为大将军。冀专权跋扈，顺帝不能制。梁氏一门前后七侯三后六贵人二大将军，东汉外戚之祸至梁氏极。", "historicalChoice": 0, "choices": ["任梁冀辅政，开梁氏专权", "抑梁冀用宗室辅政", "令群臣共辅以分其权", "外放梁冀就国以远之", "厚赐梁冀而不授要职"], "historicalOutcome": "梁冀辅政，东汉外戚之祸至极"},
            {"year": 144, "month": 8, "title": "顺帝崩", "description": "顺帝崩于玉堂前殿，太子炳嗣位为冲帝，年二岁。梁太后临朝，梁冀辅政。梁氏专权自此极，终至弑帝。", "historicalChoice": 0, "choices": ["太子炳嗣位，梁太后临朝", "择宗室长者摄政", "令功臣共辅幼主", "立宗室长者亲政", "缓即位以观时变"], "historicalOutcome": "冲帝立年二岁，梁氏临朝专权"},
        ],
    })

    # 9. 汉冲帝 刘炳 (B)
    emperors.append({
        "id": "han_chongdi",
        "dynasty": "汉",
        "name": "刘炳",
        "templeName": "汉冲帝",
        "reignStart": 144, "reignEnd": 145,
        "evaluation": "婴孺之主，在位五月",
        "background": "顺帝子，二岁即位。梁太后临朝，梁冀辅政。在位五月而崩。迎立质帝。",
        "initStats": {"treasury": 48, "people": 48, "military": 42, "court": 32, "health": 28, "tech": 33},
        "eraContext": "冲帝婴孺，梁太后临朝称制，梁冀辅政专权。九江徐扬农民起义，范容周生等聚众数万。东汉之乱益甚。",
        "tier": "B",
        "events": [
            {"year": 144, "month": null, "title": "梁氏临朝", "description": "冲帝二岁即位，梁太后临朝称制，大将军梁冀辅政。梁氏专权，朝政尽出梁冀。李固等屡谏不能入。", "historicalChoice": 0, "choices": ["令梁太后临朝，梁冀辅政", "择宗室长者摄政", "令功臣共辅幼主", "废冲帝立长者亲政", "缓临朝以观时变"], "historicalOutcome": "梁太后临朝，梁冀专权"},
            {"year": 145, "month": 1, "title": "冲帝崩", "description": "冲帝崩于玉堂前殿，年三岁。梁冀与李固议择宗室可立者。固请立年长有德者，冀欲立幼弱以便专权。", "historicalChoice": 0, "choices": ["梁冀择幼弱入继以便专权", "从李固立年长有德者", "令群臣议择贤而立", "立章帝后裔以续正统", "立渤海王鸿子缵入继"], "historicalOutcome": "梁冀立质帝，李固争之不得"},
        ],
    })

    # 10. 汉质帝 刘缵 (B)
    emperors.append({
        "id": "han_zhidi",
        "dynasty": "汉",
        "name": "刘缵",
        "templeName": "汉质帝",
        "reignStart": 145, "reignEnd": 146,
        "evaluation": "童言被害，梁冀弑君",
        "background": "章帝玄孙，渤海王刘鸿之子。八岁即位。聪慧，目梁冀为跋扈将军。梁冀恐，置毒饼中弑之。在位一年余。",
        "initStats": {"treasury": 46, "people": 46, "military": 40, "court": 30, "health": 50, "tech": 33},
        "eraContext": "梁冀专权弑君。质帝聪慧目冀为跋扈将军，冀惧而弑之。李固杜乔等忠臣与梁氏之争烈。",
        "tier": "B",
        "events": [
            {"year": 146, "month": null, "title": "跋扈将军", "description": "质帝年八岁聪慧，尝朝会目梁冀谓群臣曰此跋扈将军也。冀闻之大惧，恐帝长后不能制，遂萌弑逆之心。", "historicalChoice": 0, "choices": ["帝直言，冀惧而生弑心", "帝隐忍不发以待长成", "帝召李固等谋除梁冀", "帝厚赐梁冀以释其疑", "帝令群臣制衡梁冀"], "historicalOutcome": "质帝童言，梁冀惧而生弑心"},
            {"year": 146, "month": 6, "title": "饼毒弑君", "description": "梁冀置毒于饼中进帝。帝食之毒发，急呼水。冀止不给水，帝遂崩。李固伏尸号哭，议立清河王蒜。冀另立蠡吾侯志，是为桓帝。", "historicalChoice": 0, "choices": ["梁冀毒饼弑质帝", "帝早除梁冀以免祸", "帝召李固等入卫", "帝避梁冀以全性命", "帝让位于梁冀以求免"], "historicalOutcome": "质帝被弑，梁冀立桓帝"},
            {"year": 146, "month": null, "title": "议立桓帝", "description": "质帝崩，李固杜乔议立清河王蒜。梁冀欲立妹夫蠡吾侯志，参曹腾等宦官劝冀立志。冀遂立志为帝，是为桓帝。固乔皆被杀。", "historicalChoice": 0, "choices": ["梁冀立蠡吾侯志为桓帝", "从李固立清河王蒜", "令群臣议择贤而立", "立章帝后裔以续正统", "立勃海王鸿后裔入继"], "historicalOutcome": "梁冀立桓帝，李固杜乔被杀"},
        ],
    })

    # 11. 汉桓帝 刘志 (B)
    emperors.append({
        "id": "han_huandi",
        "dynasty": "汉",
        "name": "刘志",
        "templeName": "汉桓帝",
        "reignStart": 146, "reignEnd": 167,
        "evaluation": "诛梁冀，党锢之祸",
        "background": "章帝曾孙，蠡吾侯刘翼之子。梁冀立之。在位二十二年，前为梁冀所制，后与宦官谋诛梁氏。宦官五侯用事，党锢之祸起。",
        "initStats": {"treasury": 50, "people": 48, "military": 45, "court": 38, "health": 48, "tech": 33},
        "eraContext": "梁冀专权二十余年，桓帝与宦官谋诛之。宦官五侯封，专权乱政。党人议政讥刺宦官，第一次党锢之祸起。西羌复叛，段颎破之。",
        "tier": "B",
        "events": [
            {"year": 159, "month": null, "title": "诛梁冀", "description": "桓帝与宦官单超徐璜等五人谋，发兵围梁冀第。冀自杀，夷三族。梁氏所废免者三百余家。封五宦官为侯，号五侯，宦官专权自此盛。", "historicalChoice": 0, "choices": ["用宦官诛梁氏，封五侯", "用儒臣诛梁氏以远宦官", "宽赦梁氏以安外戚", "令功臣共议梁氏之罪", "废梁后以绝其根"], "historicalOutcome": "桓帝诛梁冀，五侯用事宦官专权"},
            {"year": 166, "month": null, "title": "党锢之祸", "description": "宦官专权，士大夫李膺陈蕃等议政讥刺。宦官告膺等养太学游士共为部党诽讪朝廷。桓帝下膺等二百余人于狱，后赦归田里禁锢终身。", "historicalChoice": 0, "choices": ["下党人狱，禁锢终身", "赦党人以广言路", "令党人与宦官和解", "抑宦官以用党人", "令群臣公议党人之罪"], "historicalOutcome": "第一次党锢之祸，党人禁锢终身"},
            {"year": 167, "month": 12, "title": "桓帝崩", "description": "桓帝崩于德阳前殿，无嗣。窦皇后与父窦武迎立解读亭侯宏为灵帝。窦武与陈蕃谋诛宦官，事泄被杀。第二次党锢之祸起。", "historicalChoice": 0, "choices": ["窦后迎灵帝入继", "择宗室长者入继亲政", "令功臣共辅以择贤", "立章帝后裔以续正统", "立桓帝从子入继"], "historicalOutcome": "灵帝入继，窦武陈蕃谋诛宦官败"},
        ],
    })

    # 12. 汉灵帝 刘宏 (B)
    emperors.append({
        "id": "han_lingdi",
        "dynasty": "汉",
        "name": "刘宏",
        "templeName": "汉灵帝",
        "reignStart": 168, "reignEnd": 189,
        "evaluation": "昏庸之主，黄巾乱汉",
        "background": "章帝玄孙，解读亭侯刘苌之子。桓帝无嗣，窦后迎立之。在位二十二年，宦官十常侍专权，党锢之祸再起。黄巾起义，东汉名存实亡。",
        "initStats": {"treasury": 45, "people": 40, "military": 40, "court": 30, "health": 45, "tech": 33},
        "eraContext": "灵帝朝宦官十常侍专权，卖官鬻爵。第二次党锢之祸，党人诛杀殆尽。黄巾起义天下大乱，州郡割据之端已现。灵帝设西园八校尉以分何进之权。",
        "tier": "B",
        "events": [
            {"year": 168, "month": null, "title": "窦武陈蕃", "description": "窦武陈蕃谋诛宦官，事泄。宦官曹节王甫等先发，矫诏诛武蕃。窦太后迁南宫，党人株连者千余人。第二次党锢之祸起。", "historicalChoice": 0, "choices": ["宦官先发诛窦武陈蕃", "窦武先发诛宦官", "令太后调和以息事", "令群臣公议两方之罪", "外放宦官以远之"], "historicalOutcome": "宦官诛窦武陈蕃，第二次党锢之祸"},
            {"year": 169, "month": null, "title": "党锢再起", "description": "曹节等奏党人李膺杜密范滂等为钩党，请下州郡考治。灵帝从之，党人死徙废禁者六七百人，天下儒宗皆罹其祸。", "historicalChoice": 0, "choices": ["从宦官穷治党人", "赦党人以广言路", "止株连但治首恶", "令群臣公议党人之罪", "抑宦官以用党人"], "historicalOutcome": "第二次党锢之祸，党人诛杀殆尽"},
            {"year": 178, "month": null, "title": "西园卖官", "description": "灵帝开西园卖官，二千石二千万、四百石四百万。又立鸿都门学以辞赋书画取士。朝政大乱，吏治败坏。", "historicalChoice": 0, "choices": ["开西园卖官以充私库", "禁卖官以正吏治", "令富户捐输以助国用", "增田租以充国用", "节用减征以纾民困"], "historicalOutcome": "西园卖官吏治大坏，国用虽充而政乱"},
            {"year": 184, "month": 3, "title": "黄巾起义", "description": "张角号太平道，徒众数十万遍布青徐幽冀荆扬豫八州。约定甲子年三月五日同日起事。事泄，角提前起兵，天下大乱。", "historicalChoice": 0, "choices": ["赦党人共讨黄巾以平乱", "遣将分路击黄巾", "令州郡自募兵以平乱", "招降张角以息兵", "亲征以振军威"], "historicalOutcome": "赦党人共讨黄巾，州郡自此拥兵"},
            {"year": 189, "month": 4, "title": "灵帝崩", "description": "灵帝崩于嘉德殿。何皇后子辩即位为少帝，何进辅政。何进与袁绍谋诛宦官，召董卓入京。宦官杀何进，袁绍尽诛宦官。董卓入京废少帝。", "historicalChoice": 0, "choices": ["少帝辩嗣位，何进辅政", "立陈留王协以续正统", "令太后临朝称制", "令功臣共辅幼主", "择宗室长者摄政"], "historicalOutcome": "少帝立何进辅政，董卓入京汉室乱"},
        ],
    })

    # 13. 汉少帝弘农王 刘辩 (B)
    emperors.append({
        "id": "han_hongnongwang",
        "dynasty": "汉",
        "name": "刘辩",
        "templeName": "汉少帝（弘农王）",
        "reignStart": 189, "reignEnd": 189,
        "evaluation": "幼主被废，旋见鸩杀",
        "background": "灵帝长子，母何皇后。即位年十四，舅何进辅政。何进谋诛宦官召董卓，反为宦官所杀。袁绍尽诛宦官，董卓入京废少帝为弘农王。",
        "initStats": {"treasury": 40, "people": 38, "military": 35, "court": 25, "health": 45, "tech": 33},
        "eraContext": "灵帝崩后宦官外戚同归于尽。董卓入京专权，废少帝立献帝。关东诸侯起兵讨卓，三国乱世自此始。",
        "tier": "B",
        "events": [
            {"year": 189, "month": 5, "title": "何进谋宦官", "description": "何进欲诛宦官，太后不从。进召董卓将兵入京以胁太后。宦官先发杀何进。袁绍引兵入宫尽诛宦官二千余人。", "historicalChoice": 0, "choices": ["何进召董卓入京胁太后", "何进自诛宦官不召外兵", "太后调和以息事", "令群臣公议宦官之罪", "赦宦官以安内廷"], "historicalOutcome": "何进被杀袁绍诛宦官，董卓入京"},
            {"year": 189, "month": 9, "title": "董卓废帝", "description": "董卓入京专权，欲废少帝立陈留王协。卓会群臣于崇德殿，废少帝为弘农王，立协为献帝。卓自为太尉领前将军事。", "historicalChoice": 0, "choices": ["董卓废少帝立献帝", "拒卓之议固立少帝", "令群臣公议废立", "禅位于陈留王以避祸", "召关东诸侯勤王"], "historicalOutcome": "董卓废少帝立献帝，专权乱政"},
            {"year": 190, "month": 1, "title": "弘农王鸩", "description": "董卓废弘农王为弘农王，旋遣李儒鸩杀之。王饮鸩不死，儒强灌之，王死年十八。关东诸侯起兵讨卓，三国乱世始。", "historicalChoice": 0, "choices": ["董卓鸩杀弘农王", "弘农王早逃以求免死", "卓留弘农王以安人心", "卓令弘农王就国不杀", "卓厚养弘农王以掩物议"], "historicalOutcome": "弘农王被鸩杀，关东诸侯起兵讨卓"},
        ],
    })

    # 14. 汉献帝 刘协 (A)
    emperors.append({
        "id": "han_xiandi",
        "dynasty": "汉",
        "name": "刘协",
        "templeName": "汉献帝",
        "reignStart": 189, "reignEnd": 220,
        "evaluation": "颠沛流离，终禅魏室",
        "background": "灵帝次子，母王美人。董卓废少帝立之。九岁即位，先后为董卓李傕郭汜所挟。东归洛阳后为曹操迎于许，建都许。在位三十一年，终禅位于曹丕。",
        "initStats": {"treasury": 35, "people": 35, "military": 30, "court": 25, "health": 50, "tech": 33},
        "eraContext": "汉室名存实亡，董卓李傕曹操相继挟天子。关东群雄割据，曹操迎献帝都许，挟天子以令诸侯。官渡赤壁之战定三分之势。最终禅位于曹丕。",
        "tier": "A",
        "events": [
            {"year": 189, "month": 9, "title": "董卓立帝", "description": "董卓废少帝为弘农王，立陈留王协为献帝，年九岁。卓自为太尉领前将军事，专断朝政。献帝如傀儡，汉室名存实亡。", "historicalChoice": 0, "choices": ["董卓立献帝以专权", "固立少帝拒卓之议", "令群臣公议废立", "禅让于宗室长者以避祸", "召关东诸侯勤王"], "historicalOutcome": "董卓立献帝专权，汉室名存实亡"},
            {"year": 190, "month": 2, "title": "迁都长安", "description": "关东诸侯起兵讨卓。卓欲迁都长安以避之，烧洛阳宫庙民居二百里。挟献帝西迁长安，发掘诸陵。天下分崩，群雄割据自此始。", "historicalChoice": 0, "choices": ["从卓迁都长安", "留洛阳以拒关东联军", "迁都于南阳以避卓", "禅让于关东盟主", "遣使求和于关东"], "historicalOutcome": "董卓挟献帝迁长安，洛阳焚毁"},
            {"year": 192, "month": 4, "title": "王允诛董卓", "description": "司徒王允与中郎将吕布谋诛董卓。献帝病新愈，大会未央殿。卓入宫，吕布置伏刺杀之。允录尚书事，旋为李傕郭汜所杀。", "historicalChoice": 0, "choices": ["用王允吕布诛董卓", "赦董卓以安其部", "令董卓就国以远之", "召关东诸侯入卫", "厚赐董卓以缓其逆"], "historicalOutcome": "董卓被诛，王允旋为李傕郭汜所杀"},
            {"year": 195, "month": null, "title": "东归洛阳", "description": "李傕郭汜相攻，献帝东归洛阳。途中艰难百战，群臣饥困。建安元年七月至洛阳，宫室残破，百官采野谷为食。曹操闻之，迎帝都许。", "historicalChoice": 0, "choices": ["东归洛阳以图复兴", "留长安以避路险", "依附关东诸侯之一", "南奔荆州刘表", "西入凉州依马腾"], "historicalOutcome": "献帝东归洛阳，曹操迎之入许"},
            {"year": 196, "month": null, "title": "迁都许", "description": "曹操迎献帝都许，建宗庙社稷。帝以操为司空行车骑将军事，百官总己以听。曹操挟天子以令诸侯，征伐四方，汉政皆决于操。", "historicalChoice": 0, "choices": ["从曹操迁都许", "留洛阳以观时变", "依袁绍以图复兴", "南奔荆州刘表", "西入关中依马腾"], "historicalOutcome": "曹操迎献帝都许，挟天子令诸侯"},
            {"year": 200, "month": null, "title": "衣带诏", "description": "献帝密诏董承等诛曹操，藏于衣带中。事泄，操诛董承等三族。操入宫收董贵人，帝请免不得。伏皇后益惧，与父完谋。", "historicalChoice": 0, "choices": ["密诏董承诛曹操", "隐忍待时以图后举", "公开下诏讨曹操", "禅让于曹操以避祸", "外结诸侯共讨曹操"], "historicalOutcome": "衣带诏泄，董承等被诛"},
            {"year": 200, "month": 10, "title": "官渡之战", "description": "袁绍将十万众南下攻曹操，操兵少粮尽。操袭绍粮草于乌巢，绍军大溃。操尽得绍众，统一北方。献帝益为操所制。", "historicalChoice": 0, "choices": ["助曹操破袁绍以固帝位", "密助袁绍以图曹操", "中立以观两虎之斗", "南奔荆州刘表以避祸", "遣使调停以息兵"], "historicalOutcome": "曹操破袁绍，统一北方，献帝益困"},
            {"year": 208, "month": null, "title": "赤壁之战", "description": "曹操南征荆州，致书孙权会猎于吴。孙刘联军拒操于赤壁。操败北归，天下三分之势成。献帝在许，无能为力。", "historicalChoice": 0, "choices": ["中立以观三分之势", "密助孙刘以制曹操", "助曹操南征以图统一", "南奔荆州以避兵祸", "遣使调停以息兵"], "historicalOutcome": "赤壁之战曹操败，天下三分成"},
            {"year": 213, "month": null, "title": "曹操封魏公", "description": "曹操平定北方，群臣请封魏公加九锡。献帝诏封操魏公，以冀州十郡为魏国。董昭等请进操爵魏王，献帝不能制。", "historicalChoice": 0, "choices": ["诏封曹操魏公加九锡", "拒封以正君臣之分", "令群臣公议封爵之事", "禅让于曹操以避祸", "厚赐曹操而不封公"], "historicalOutcome": "曹操封魏公加九锡，篡汉在即"},
            {"year": 216, "month": null, "title": "曹操进魏王", "description": "献帝进曹操爵为魏王，冕十有二旒，乘金根车，驾六马，设天子旌旗。曹丕立为魏太子。汉室名号仅存，禅代之势必行。", "historicalChoice": 0, "choices": ["进曹操魏王以尊之", "拒进爵以正名分", "令群臣公议进爵之事", "禅让于曹操以避祸", "密召忠臣图曹操"], "historicalOutcome": "曹操进魏王，仪同天子"},
            {"year": 219, "month": null, "title": "立魏太子", "description": "曹操立曹丕为魏太子。群臣劝操正位，操曰若天命在吾吾为周文王矣。操旋病，次年正月薨于洛阳。曹丕嗣魏王。", "historicalChoice": 0, "choices": ["立曹丕为魏太子以定储", "立曹植以文才为嗣", "立曹彰以武勇为嗣", "令群臣议择贤而立", "缓立储以观后嗣"], "historicalOutcome": "曹丕立为魏太子，旋嗣魏王"},
            {"year": 220, "month": 10, "title": "禅让曹丕", "description": "曹操薨，曹丕嗣魏王。群臣劝进，献帝禅位于丕。丕即皇帝位，改元黄初，国号魏。废献帝为山阳公，汉祚终，传四百余年。", "historicalChoice": 0, "choices": ["禅让于曹丕以顺天命", "拒禅让以守汉祚", "密召刘备入卫以图复兴", "南奔孙权以避祸", "令群臣公议去就"], "historicalOutcome": "献帝禅让曹丕，汉亡魏兴"},
        ],
    })

    # ========== 三国魏 ==========

    # 15. 曹操 (wei_wudi, 追尊)
    emperors.append({
        "id": "wei_wudi",
        "dynasty": "魏",
        "name": "曹操",
        "templeName": "魏武帝（追尊）",
        "reignStart": 196, "reignEnd": 220,
        "evaluation": "治世能臣，乱世奸雄",
        "background": "沛国谯人，宦官曹腾之孙。举孝廉为郎，讨黄巾起家。建安元年迎献帝都许，挟天子以令诸侯。统一北方，进魏王。子丕代汉，追尊武皇帝。",
        "initStats": {"treasury": 55, "people": 50, "military": 80, "court": 65, "health": 60, "tech": 35},
        "eraContext": "汉末大乱群雄逐鹿。曹操挟天子以令诸侯，屯田积谷，唯才是举。袁绍据河北、刘备依荆州、孙权据江东。官渡赤壁两战定三分之势。",
        "tier": "A",
        "events": [
            {"year": 196, "month": null, "title": "迎帝都许", "description": "曹操闻献帝东归洛阳，遣曹洪西迎。操至洛阳，以洛阳残破请帝都许。帝以操为大将军，封武平侯。挟天子以令诸侯自此始。", "historicalChoice": 0, "choices": ["迎帝都许以挟天子令诸侯", "留帝洛阳以尊汉室", "迎帝于邺以制河北", "不迎帝以避嫌疑", "迎帝于谯以近故里"], "historicalOutcome": "曹操迎献帝都许，挟天子令诸侯"},
            {"year": 196, "month": null, "title": "屯田制", "description": "曹操用枣祗韩浩议，兴屯田以充军食。许下屯田得谷百万斛，于是州郡置田官。所在积谷，征伐四方无运粮之劳。", "historicalChoice": 0, "choices": ["兴屯田以充军食", "令民输粟以充军费", "募民垦荒以增户口", "购粮于豪强以充军食", "减兵以省军费"], "historicalOutcome": "屯田兴，军食足，曹操征伐无运粮之劳"},
            {"year": 197, "month": null, "title": "宛城之败", "description": "曹操南征张绣于宛。操纳绣叔母邹氏，绣怒反。袭操营，杀操长子昂侄安民爱将典韦。操伤，仅以身免。后绣复降。", "historicalChoice": 0, "choices": ["纳邹氏致张绣反", "不纳邹氏以安绣", "厚赐张绣以结其心", "早除张绣以绝后患", "徙张绣远方以远之"], "historicalOutcome": "张绣反，曹操丧子丧将"},
            {"year": 198, "month": null, "title": "灭吕布", "description": "吕布袭刘备据下邳。操东征布，决泗沂水灌下邳。布将侯成等执布降。操缢杀布及陈宫，收张辽。徐州平。", "historicalChoice": 0, "choices": ["东征灭吕布取徐州", "招降吕布以用其勇", "联吕布以制袁绍", "令刘备击吕布", "缓图吕布先定河北"], "historicalOutcome": "操灭吕布，徐州平"},
            {"year": 199, "month": null, "title": "唯才是举", "description": "操下求贤令，曰若必廉士而后可用，则齐桓何以霸世。唯才是举，不仁不孝而有治国用兵之术者皆得举用。开魏晋九品中正之先。", "historicalChoice": 0, "choices": ["唯才是举，不问德行", "德才兼备以选官", "重德轻才以正风俗", "令郡国举孝廉以继汉制", "征辟名士不拘一格"], "historicalOutcome": "操唯才是举，人才归之如流水"},
            {"year": 200, "month": 10, "title": "官渡之战", "description": "袁绍将十万众南下，操兵少粮尽。操纳许攸计，袭绍粮草于乌巢。绍将张郃高览降操，绍军大溃。操尽得绍众，统一北方。", "historicalChoice": 0, "choices": ["袭乌巢烧绍粮以决战", "坚守待绍粮尽自溃", "遣使求和以缓兵", "退守许都以保帝", "令刘表击绍以分其势"], "historicalOutcome": "操破袁绍于官渡，统一北方"},
            {"year": 207, "month": null, "title": "北征乌桓", "description": "操北征三郡乌桓，至无终遇秋水。用田畴为导，出卢龙塞，越白檀历平冈，于白狼山斩乌桓蹋顿。北方边患暂息，辽东公孙康斩袁尚首降。", "historicalChoice": 0, "choices": ["北征乌桓以平边患", "令公孙康自击乌桓", "守边不出待乌桓内乱", "联鲜卑共击乌桓", "徙边民于内地以避祸"], "historicalOutcome": "操破乌桓，北方平"},
            {"year": 208, "month": null, "title": "赤壁之战", "description": "操南下取荆州，致书孙权会猎于吴。孙刘联军拒操于赤壁，黄盖诈降火攻。操军大败，烧船自乌林走华容。三分之势成。", "historicalChoice": 0, "choices": ["顺江东下与孙刘决战", "缓进以招降孙权", "先取刘备再图孙权", "守荆州以观时变", "北归以图后举"], "historicalOutcome": "操败于赤壁，三分之势成"},
            {"year": 211, "month": null, "title": "破马超", "description": "操西征马超韩遂于关中。用贾诩反间计，离间超遂。操自潼关渡河，大破超遂。关中平，凉州次第归附。", "historicalChoice": 0, "choices": ["西征破马超定关中", "招降马超以用其勇", "守潼关以拒马超", "令夏侯渊击马超", "联韩遂以制马超"], "historicalOutcome": "操破马超韩遂，关中平"},
            {"year": 213, "month": null, "title": "进魏公", "description": "董昭等劝操进爵魏公加九锡。操辞让再三乃受。以冀州十郡为魏国，置百官。汉祚虽存，禅代之势已成。", "historicalChoice": 0, "choices": ["受魏公加九锡以固权", "拒进爵以尊汉室", "厚赐群臣而不进爵", "令群臣公议进爵之事", "缓进爵以观天下"], "historicalOutcome": "操进魏公加九锡，禅汉之势成"},
            {"year": 215, "month": null, "title": "取汉中", "description": "操西征张鲁取汉中。鲁降，操以夏侯渊留守汉中。司马懿劝操乘胜取蜀，操曰人苦无足既得陇复望蜀。后刘备取汉中。", "historicalChoice": 0, "choices": ["取汉中后不进蜀", "乘胜取蜀以图刘备", "令张鲁守汉中为藩屏", "徙汉中民于关中", "留大军守汉中以制蜀"], "historicalOutcome": "操取汉中不进蜀，后为刘备所取"},
            {"year": 216, "month": null, "title": "进魏王", "description": "献帝进操魏王，冕十二旒，乘金根车驾六马，设天子旌旗。立曹丕为魏太子。操虽不称帝，仪制同天子矣。", "historicalChoice": 0, "choices": ["进魏王，仪同天子", "拒进魏王以尊汉室", "进魏王而不设天子仪", "令群臣公议进爵之事", "缓进爵以观后嗣"], "historicalOutcome": "操进魏王仪同天子，禅代在即"},
            {"year": 219, "month": null, "title": "关羽襄樊", "description": "关羽攻曹仁于襄樊，水淹七军，擒于禁斩庞德，威震华夏。操议迁都以避之。司马懿劝结孙权击关羽。吕蒙袭荆州杀羽。", "historicalChoice": 0, "choices": ["结孙权袭荆州以解樊围", "亲征关羽以解樊围", "迁都以避关羽之锋", "令曹仁坚守待变", "遣使招降关羽"], "historicalOutcome": "操结孙权袭荆州，关羽败死"},
            {"year": 220, "month": 1, "title": "操薨洛阳", "description": "操病薨于洛阳，年六十六。太子丕嗣魏王丞相。群臣劝进，献帝禅让于丕。丕追尊操为武皇帝，庙号太祖。", "historicalChoice": 0, "choices": ["操薨，丕嗣魏王", "令群臣共辅以分其权", "择操他子入继", "还政献帝以安汉室", "令宗室长者摄政"], "historicalOutcome": "操薨，丕嗣位旋代汉建魏"},
        ],
    })

    # 16. 魏文帝 曹丕 (A)
    emperors.append({
        "id": "wei_wendi",
        "dynasty": "魏",
        "name": "曹丕",
        "templeName": "魏文帝",
        "reignStart": 220, "reignEnd": 226,
        "evaluation": "代汉建魏，立九品中正",
        "background": "曹操次子。建安二十二年立为魏太子。操薨，嗣魏王丞相。同年受汉禅，建魏，都洛阳。在位七年，立九品中正制，三征孙权。",
        "initStats": {"treasury": 60, "people": 55, "military": 65, "court": 70, "health": 55, "tech": 35},
        "eraContext": "曹丕代汉建魏，立九品中正制以选官。孙权称藩于魏以备刘备。夷陵之战后孙权叛魏自立。三路伐吴无功。蜀汉据益州，东吴据江东，三国鼎立。",
        "tier": "A",
        "events": [
            {"year": 220, "month": 10, "title": "受禅建魏", "description": "献帝禅位于曹丕。丕三让乃受，即皇帝位，改元黄初，国号魏。废献帝为山阳公。汉亡，传四百二十六年。魏承汉统，都洛阳。", "historicalChoice": 0, "choices": ["受禅代汉，建魏称帝", "拒禅让以守魏王之位", "虚帝号令献帝亲政", "另择宗室入继汉统", "令群臣公议去就"], "historicalOutcome": "曹丕代汉建魏，汉亡"},
            {"year": 220, "month": null, "title": "九品中正", "description": "丕用陈群议，立九品中正制。州郡置中正，以九品论人才。初以才行论品，后渐为门阀所把持，上品无寒门下品无势族。", "historicalChoice": 0, "choices": ["立九品中正制以选官", "复汉察举孝廉之制", "行唯才是举之策", "令郡国自选官吏", "征辟名士不拘门第"], "historicalOutcome": "九品中正制立，门阀渐起"},
            {"year": 221, "month": null, "title": "刘备称帝", "description": "刘备闻曹丕代汉，于成都即帝位，国号汉，史称蜀汉。备以兴复汉室为名，将伐孙权报荆州之仇。丕受刘备称帝之书，议讨之。", "historicalChoice": 0, "choices": ["受刘备称帝之实，议伐蜀", "结孙权共讨刘备", "令孙权伐蜀以坐收渔利", "中立以观吴蜀之争", "遣使招降刘备"], "historicalOutcome": "刘备称帝建蜀，三国之势成"},
            {"year": 222, "month": null, "title": "孙权称藩", "description": "刘备伐吴，孙权惧，遣使称藩于魏请降。丕受权降，封权为吴王加九锡。权虽受封，然仍自置百官，不朝魏。", "historicalChoice": 0, "choices": ["受孙权降，封吴王", "拒孙权降令其自存", "封孙权而不加九锡", "令孙权入朝以试忠逆", "联刘备共伐孙权"], "historicalOutcome": "丕封孙权吴王，权不受魏制"},
            {"year": 222, "month": null, "title": "夷陵之战", "description": "刘备伐吴，陆逊拒之。逊坚守不出，待备军疲怠，以火攻大破备于夷陵。备走白帝。丕闻吴胜，议伐吴。孙权遂叛魏。", "historicalChoice": 0, "choices": ["乘吴蜀之衅伐吴", "联吴伐蜀以分其地", "中立以观吴蜀之变", "遣使调停以息兵", "令吴蜀自相耗而后图之"], "historicalOutcome": "夷陵之战吴胜，孙权叛魏"},
            {"year": 224, "month": null, "title": "三路伐吴", "description": "丕自将伐吴，三路并进。曹休出洞口、曹仁出濡须、曹真出南郡。吴将吕范朱桓等拒之。魏军无功而还，吴亦疲弊。", "historicalChoice": 0, "choices": ["三路伐吴以图江东", "守淮南以观孙权之变", "联蜀共伐孙权", "遣使招降孙权", "亲征濡须以决胜负"], "historicalOutcome": "三路伐吴无功，魏吴相持于淮南"},
            {"year": 225, "month": null, "title": "再伐吴", "description": "丕再次南征至广陵。时江水盛寒，舟不得入江。丕望江叹曰魏虽有武骑千群无所用之，未可图也。乃还。", "historicalChoice": 0, "choices": ["再伐吴至广陵无功而还", "固守淮南不再南征", "联蜀共伐孙权", "遣使招降孙权以息兵", "令水军练战以图后举"], "historicalOutcome": "丕再伐吴无功，遂罢南征"},
            {"year": 226, "month": null, "title": "禁外戚宦官", "description": "丕下诏妇人不得预政，群臣不得奏事太后，后族不得辅政。又限宦官之权。此诏为防汉末外戚宦官之祸，然不能久行。", "historicalChoice": 0, "choices": ["禁外戚宦官干政以正朝纲", "用外戚辅政以固根本", "用宦官以防权臣", "令宗室辅政以制外戚", "亲揽万机不假人权"], "historicalOutcome": "丕禁外戚宦官，然不能久行"},
            {"year": 226, "month": 5, "title": "文帝崩", "description": "丕崩于嘉福殿，年四十。太子叡嗣位为明帝。丕托曹真陈群司马懿辅政。魏承汉后，立国七年，三国之势已成。", "historicalChoice": 0, "choices": ["太子叡嗣位，曹真等辅政", "令太后辅政以固幼主", "择宗室长者摄政", "令群臣共辅以分其权", "独任一权臣以专责成"], "historicalOutcome": "明帝嗣位，曹真陈群司马懿辅政"},
        ],
    })

    # 17. 魏明帝 曹叡 (A)
    emperors.append({
        "id": "wei_mingdi",
        "dynasty": "魏",
        "name": "曹叡",
        "templeName": "魏明帝",
        "reignStart": 226, "reignEnd": 239,
        "evaluation": "拒亮御吴，末年奢靡",
        "background": "曹丕长子，母甄皇后。即位后诸葛亮屡次北伐，叡遣曹真司马懿拒之。又御孙权于合肥。末年大兴土木，营洛阳宫室，托孤失人，司马懿渐起。",
        "initStats": {"treasury": 62, "people": 58, "military": 70, "court": 65, "health": 50, "tech": 35},
        "eraContext": "明帝朝诸葛亮北伐，司马懿据守。孙权称帝，魏吴相持于合肥。辽东公孙渊自立为燕王。明帝末年大兴土木，托孤于曹爽司马懿，埋下高平陵之变。",
        "tier": "A",
        "events": [
            {"year": 227, "month": null, "title": "诸葛亮北伐", "description": "诸葛亮上出师表，率军北伐魏。赵云据箕谷为疑兵，亮自率军攻祁山。天水南安安定三郡叛魏应亮。叡遣曹真张郃拒之。", "historicalChoice": 0, "choices": ["遣曹真张郃拒诸葛亮", "亲征长安以拒亮", "令司马懿专征诸葛亮", "守长安不出待亮粮尽", "令孙权伐蜀以分亮势"], "historicalOutcome": "张郃破马谡于街亭，亮退兵"},
            {"year": 228, "month": null, "title": "街亭之战", "description": "诸葛亮用马谡守街亭。谡违亮节制，舍水就山。魏将张郃绝其汲道，大破谡。亮退兵汉中，挥泪斩马谡。叡诏赦天水三郡。", "historicalChoice": 0, "choices": ["令张郃破马谡于街亭", "令司马懿速战以决胜负", "守长安待亮粮尽自退", "令曹真截亮归路", "亲征以振军威"], "historicalOutcome": "张郃破街亭，亮退兵斩马谡"},
            {"year": 228, "month": null, "title": "石亭之战", "description": "吴鄱阳太守周鲂诈降诱魏。曹休将十万步骑至皖。陆逊大破休于石亭。休走至夹石，死者万余。休惭愤发病死。", "historicalChoice": 0, "choices": ["令曹休击吴致石亭之败", "止曹休勿信周鲂之降", "令司马懿接应曹休", "亲征以督诸军", "守淮南以观吴变"], "historicalOutcome": "曹休败于石亭惭愤病死"},
            {"year": 229, "month": null, "title": "营洛阳宫", "description": "明帝营洛阳宫，起昭阳太极殿、总章观。又起芳林园，置景阳山。群臣屡谏，叡不能止。府库渐虚，民力困弊。", "historicalChoice": 0, "choices": ["大兴土木营洛阳宫", "罢营宫室以恤民力", "减省规模但求实用", "令郡国共役以分其劳", "以刑徒充役不扰平民"], "historicalOutcome": "明帝营宫室，府库虚民力困"},
            {"year": 231, "month": null, "title": "诸葛亮再北伐", "description": "诸葛亮复出祁山围祁山。叡遣司马懿拒之。懿畏亮，坚守不出。亮以巾帼之服激懿，懿仍不出。亮粮尽退兵，张郃追之膝中矢死。", "historicalChoice": 0, "choices": ["令司马懿坚守不出拒亮", "令司马懿速战以决胜负", "亲征长安以督诸军", "令曹真截亮归路", "遣使议和以息兵"], "historicalOutcome": "懿坚守不出，亮退兵张郃追死"},
            {"year": 234, "month": null, "title": "五丈原", "description": "诸葛亮出斜谷屯五丈原，与司马懿对峙。亮分兵屯田为久驻之计。叡令懿但拒不战。亮病薨于军中，蜀军退。", "historicalChoice": 0, "choices": ["令懿坚守待亮自毙", "令懿出击以决胜负", "亲征以督诸军", "遣奇兵袭汉中", "令孙权伐蜀以分亮势"], "historicalOutcome": "亮薨于五丈原，蜀军退"},
            {"year": 237, "month": null, "title": "公孙渊自立", "description": "辽东公孙渊自立为燕王，置百官。明帝遣幽州刺史毌丘俭击之，败还。明帝乃召司马懿征辽东。", "historicalChoice": 0, "choices": ["遣司马懿征辽东", "遣毌丘俭再击辽东", "招降公孙渊以安辽东", "令鲜卑共讨公孙渊", "缓图辽东先御蜀吴"], "historicalOutcome": "司马懿征辽东，平之"},
            {"year": 238, "month": null, "title": "平定辽东", "description": "司马懿将兵四万征辽东，围襄平。公孙渊突围被杀，辽东平。懿诛公孙氏及公卿以下二千余人。辽东遂入魏版图。", "historicalChoice": 0, "choices": ["令懿平辽东诛公孙氏", "招降辽东以省军费", "令公孙氏守辽东为藩屏", "徙辽东民于内地", "留公孙氏部以制鲜卑"], "historicalOutcome": "懿平辽东，公孙氏灭"},
            {"year": 239, "month": 1, "title": "明帝崩", "description": "明帝崩于嘉福殿，年三十六。太子芳年八岁嗣位。明帝托孤于大将军曹爽、太尉司马懿。司马懿自此渐起，终成高平陵之变。", "historicalChoice": 0, "choices": ["太子芳嗣位，曹爽司马懿辅政", "令太后辅政以固幼主", "择宗室长者摄政", "令群臣共辅以分其权", "独任曹爽以专责成"], "historicalOutcome": "齐王芳嗣位，曹爽司马懿辅政"},
        ],
    })

    # 18. 魏齐王 曹芳 (B)
    emperors.append({
        "id": "wei_qiwangfang",
        "dynasty": "魏",
        "name": "曹芳",
        "templeName": "魏齐王",
        "reignStart": 239, "reignEnd": 254,
        "evaluation": "幼主在位，司马专权",
        "background": "曹叡养子，生父任城王曹楷。八岁即位，曹爽司马懿辅政。曹爽专权，懿称病。高平陵之变后司马懿专政。后芳为司马师所废。",
        "initStats": {"treasury": 55, "people": 52, "military": 58, "court": 40, "health": 50, "tech": 35},
        "eraContext": "齐王芳朝曹爽与司马懿争权。高平陵之变司马懿诛曹爽，司马氏专权。王凌毌丘俭诸葛诞三叛皆败。蜀姜维屡北伐，吴孙权薨后乱。",
        "tier": "B",
        "events": [
            {"year": 239, "month": null, "title": "曹爽辅政", "description": "齐王芳八岁即位，大将军曹爽、太尉司马懿辅政。爽用何晏邓飏等，专断朝政，懿称病不预事。爽渐骄奢，懿阴图之。", "historicalChoice": 0, "choices": ["任曹爽辅政，懿称病", "令司马懿共辅以制曹爽", "用宗室辅政以制权臣", "令群臣共辅以分其权", "亲揽万机不假人权"], "historicalOutcome": "曹爽辅政专权，司马懿称病待变"},
            {"year": 244, "month": null, "title": "曹爽伐蜀", "description": "曹爽欲立威名，将兵七万伐蜀。蜀将王平拒之于兴势。爽军不得进，粮尽退兵。损兵折将，关中虚耗。爽威名大损。", "historicalChoice": 0, "choices": ["令曹爽伐蜀以立威", "止曹爽伐蜀以省军费", "令司马懿伐蜀以代之", "守关中以观蜀变", "联吴伐蜀以分其势"], "historicalOutcome": "曹爽伐蜀大败，威名损"},
            {"year": 249, "month": null, "title": "高平陵之变", "description": "曹爽陪齐王芳谒高平陵。司马懿起兵闭洛阳城门，奏废爽。芳不能制。爽犹豫不决，终降。懿诛爽及何晏等三族。司马氏专权。", "historicalChoice": 0, "choices": ["任司马懿诛曹爽以专权", "令曹爽拒懿以保权", "调和两方以息争", "令群臣公议两方之罪", "外放司马懿以远之"], "historicalOutcome": "高平陵之变，司马氏专权"},
            {"year": 251, "month": null, "title": "王凌之叛", "description": "太尉王凌谋废齐王芳立楚王彪，事泄。司马懿击凌，凌降自杀。懿尽诛凌党，赐楚王彪死。司马氏益固。", "historicalChoice": 0, "choices": ["令懿平王凌之叛", "赦王凌以息兵", "令群臣公议王凌之罪", "徙楚王彪远方不杀", "亲征以振军威"], "historicalOutcome": "懿平王凌，司马氏益固"},
            {"year": 254, "month": 9, "title": "芳被废", "description": "齐王芳不亲政事，宠幸近臣。司马师废芳为齐王，立高贵乡公髦。芳在位十五年，无权柄，终为司马氏所废。", "historicalChoice": 0, "choices": ["司马师废芳立髦", "固立齐王芳以正名分", "令群臣公议废立之事", "立宗室长者入继亲政", "令太后临朝称制"], "historicalOutcome": "齐王芳被废，高贵乡公立"},
        ],
    })

    # 19. 魏高贵乡公 曹髦 (B)
    emperors.append({
        "id": "wei_gaoxianggongmao",
        "dynasty": "魏",
        "name": "曹髦",
        "templeName": "魏高贵乡公",
        "reignStart": 254, "reignEnd": 260,
        "evaluation": "不甘为傀，讨贼被杀",
        "background": "曹丕之孙，东海王曹霖之子。司马师废齐王芳迎立之。髦聪慧有志，不甘为司马氏傀儡。讨司马昭，为成济所杀。年二十。",
        "initStats": {"treasury": 50, "people": 50, "military": 45, "court": 30, "health": 55, "tech": 35},
        "eraContext": "高贵乡公朝司马师薨，弟昭继专权。毌丘俭文钦诸葛诞三叛皆败。髦不甘为傀儡，谓司马昭之心路人皆知，讨昭被杀。",
        "tier": "B",
        "events": [
            {"year": 255, "month": null, "title": "毌丘俭反", "description": "扬州都督毌丘俭、刺史文钦起兵讨司马师。师新割瘤疾，强起击之。俭败死，钦降吴。师旋病薨，弟昭继专权。", "historicalChoice": 0, "choices": ["令司马师击毌丘俭", "赦毌丘俭以息兵", "令群臣公议两方之罪", "亲征以振军威", "令司马昭代兄击之"], "historicalOutcome": "毌丘俭败死，司马师旋薨昭继"},
            {"year": 257, "month": null, "title": "诸葛诞反", "description": "征东大将军诸葛诞据寿春反，称臣于吴。司马昭挟高贵乡公及太后东征。诞坚守寿春，粮尽败死。司马氏益固。", "historicalChoice": 0, "choices": ["令司马昭击诸葛诞", "赦诸葛诞以息兵", "令群臣公议诞之罪", "招降诸葛诞以用其力", "亲征以振军威"], "historicalOutcome": "诸葛诞败死，司马氏益固"},
            {"year": 260, "month": 5, "title": "讨司马昭", "description": "髦不忍司马昭专权，谓司马昭之心路人所知。率殿中宿卫苍头官僮讨昭。太子舍人成济刺髦于车下，髦死年二十。昭杀成济以掩物议。", "historicalChoice": 0, "choices": ["髦率众讨昭被杀", "髦隐忍待时以图后举", "髦密召忠臣图昭", "髦禅让于昭以避祸", "髦外奔以求免死"], "historicalOutcome": "髦讨昭被杀，昭立元帝奂"},
        ],
    })

    # 20. 魏元帝 曹奂 (B)
    emperors.append({
        "id": "wei_yuandihuan",
        "dynasty": "魏",
        "name": "曹奂",
        "templeName": "魏元帝",
        "reignStart": 260, "reignEnd": 265,
        "evaluation": "末代之主，禅位于晋",
        "background": "曹操之孙，燕王曹宇之子。司马昭杀高贵乡公，迎立之。在位六年，政皆决于昭。司马昭灭蜀后，进晋王。奂终禅位于昭子炎。",
        "initStats": {"treasury": 50, "people": 48, "military": 50, "court": 25, "health": 50, "tech": 35},
        "eraContext": "元帝奂朝司马昭专权。邓艾钟会灭蜀，昭进晋王加九锡。昭薨，子炎嗣，逼奂禅让。魏亡，传四十六年。晋承魏统。",
        "tier": "B",
        "events": [
            {"year": 263, "month": null, "title": "灭蜀汉", "description": "司马昭遣邓艾钟会伐蜀。会攻剑阁，艾偷渡阴平。蜀后主降，蜀亡。魏尽得蜀地。艾会争功，会反被杀，艾亦见害。", "historicalChoice": 0, "choices": ["遣邓艾钟会灭蜀", "令司马昭亲征蜀", "联吴伐蜀以分其地", "守长安以观蜀变", "招降蜀后主以息兵"], "historicalOutcome": "邓艾钟会灭蜀，蜀亡"},
            {"year": 264, "month": null, "title": "昭进晋王", "description": "司马昭灭蜀，进封晋王加九锡，冕十二旒。立子炎为晋世子。昭虽不称帝，仪制同天子。禅代之势已成。", "historicalChoice": 0, "choices": ["进昭晋王加九锡", "拒进爵以正名分", "令群臣公议进爵之事", "厚赐昭而不进爵", "禅让于昭以避祸"], "historicalOutcome": "司马昭进晋王，禅代在即"},
            {"year": 265, "month": 8, "title": "昭薨炎嗣", "description": "司马昭病薨，子炎嗣晋王丞相。群臣劝进，奂禅让于炎。炎即皇帝位，改元泰始，国号晋。废奂为陈留王。魏亡，传四十六年。", "historicalChoice": 0, "choices": ["禅让于司马炎建晋", "拒禅让以守魏祚", "令群臣公议去就", "密召宗室图炎", "外奔以求免死"], "historicalOutcome": "奂禅让于炎，魏亡晋兴"},
        ],
    })

    # ========== 三国蜀 ==========

    # 21. 蜀昭烈帝 刘备 (A)
    emperors.append({
        "id": "shu_zhaoliedi",
        "dynasty": "蜀",
        "name": "刘备",
        "templeName": "蜀昭烈帝",
        "reignStart": 221, "reignEnd": 223,
        "evaluation": "百折不挠，三分天下",
        "background": "涿郡涿县人，汉景帝子中山靖王胜之后。少孤贫，贩履织席为业。起兵讨黄巾，转战半生，依陶谦依曹操依袁绍依刘表。三顾茅庐得诸葛亮，赤壁后据荆益，进位汉中王。曹丕代汉，备称帝续汉统。",
        "initStats": {"treasury": 50, "people": 55, "military": 70, "court": 65, "health": 55, "tech": 30},
        "eraContext": "汉末大乱，刘备转战半生方得荆益。曹操据中原孙权据江东。赤壁之战后三分之势成。刘备称帝续汉统，然关羽失荆州，备伐吴报仇，夷陵大败，忧愤而崩。",
        "tier": "A",
        "events": [
            {"year": 207, "month": null, "title": "三顾茅庐", "description": "刘备屯新野，三顾诸葛亮于隆中。亮为备陈三分天下之计，曰曹操挟天子不可与争锋，孙权据江东可以为援而不可图。备曰孤之有孔明犹鱼之有水也。", "historicalChoice": 0, "choices": ["三顾茅庐，用亮之计", "自力更生不用亮", "投孙权以求存", "投刘表以保荆州", "入蜀图益州以立基"], "historicalOutcome": "备三顾得亮，三分之计定"},
            {"year": 208, "month": null, "title": "赤壁之战", "description": "曹操南征，刘备败于当阳长坂。遣诸葛亮使孙权结盟。孙刘联军拒操于赤壁，火攻大破操。备收荆州江南四郡，始有立足之地。", "historicalChoice": 0, "choices": ["联孙权破操于赤壁", "投孙权以求存", "投苍梧吴巨以避操", "据荆州死战操", "南奔交州以图存"], "historicalOutcome": "备联孙破操，始据荆州"},
            {"year": 211, "month": null, "title": "入蜀", "description": "刘璋邀刘备入蜀拒张鲁。备留诸葛亮关羽守荆州，自率兵入蜀。后与璋反目，围成都。诸葛亮张飞赵云入蜀援备，璋降。备得益州。", "historicalChoice": 0, "choices": ["入蜀取益州立基", "拒刘璋之邀守荆州", "取汉中后再图蜀", "联张鲁以制刘璋", "归孙权以求存"], "historicalOutcome": "备取益州，三分之势成"},
            {"year": 218, "month": null, "title": "取汉中", "description": "刘备率军攻曹操汉中守将夏侯渊。法正为谋，黄忠斩渊于定军山。曹操亲征不能克，备遂有汉中。进位汉中王。", "historicalChoice": 0, "choices": ["攻汉中斩夏侯渊", "守益州不攻汉中", "联孙权共取汉中", "招降夏侯渊以用其勇", "缓图汉中先固益州"], "historicalOutcome": "备取汉中，进位汉中王"},
            {"year": 219, "month": null, "title": "关羽失荆州", "description": "关羽攻曹仁于襄樊，水淹七军威震华夏。孙权遣吕蒙袭荆州，杀关羽。备失荆州，跨有荆益之策破，三国之势大变。", "historicalChoice": 0, "choices": ["令关羽守荆州不北伐", "令关羽北伐以图中原", "增兵荆州以固根本", "令关羽联孙权以保荆州", "亲率大军援关羽"], "historicalOutcome": "关羽失荆州被杀，备失半壁"},
            {"year": 221, "month": 4, "title": "称帝续汉", "description": "曹丕代汉，刘备于成都即帝位，国号汉，史称蜀汉。备以兴复汉室为名，欲伐吴报关羽之仇。诸葛亮等屡谏不能止。", "historicalChoice": 0, "choices": ["称帝续汉统，伐吴报仇", "称帝后先伐魏以兴汉室", "称帝后联吴共伐魏", "不称帝守汉中王之号", "称帝后休兵以固根本"], "historicalOutcome": "备称帝续汉，率军伐吴"},
            {"year": 222, "month": null, "title": "夷陵之败", "description": "刘备率大军伐吴，连营七百里。吴将陆逊坚守不出，待备军疲怠，以火攻大破备于夷陵。备走白帝城，尽丧锐卒。备惭愤发病。", "historicalChoice": 0, "choices": ["率大军伐吴连营七百里", "用诸葛亮之策不伐吴", "小股骚扰吴境以观变", "遣将伐吴不亲征", "联魏伐吴以分其地"], "historicalOutcome": "备败于夷陵，走白帝城"},
            {"year": 223, "month": 4, "title": "白帝托孤", "description": "备病笃，召诸葛亮于白帝城托孤。备谓亮曰君才十倍曹丕，必能安国终定大事。若嗣子可辅则辅之，如其不才君可自取。亮涕泣受命。备崩年六十三。", "historicalChoice": 0, "choices": ["托孤诸葛亮辅太子", "令诸葛亮自取帝位", "令李严共辅以制诸葛亮", "令赵云辅政以固根本", "令群臣共辅以分其权"], "historicalOutcome": "备托孤诸葛亮，太子禅嗣位"},
        ],
    })

    # 22. 蜀后主 刘禅 (A)
    emperors.append({
        "id": "shu_houzhu",
        "dynasty": "蜀",
        "name": "刘禅",
        "templeName": "蜀后主",
        "reignStart": 223, "reignEnd": 263,
        "evaluation": "昏庸之主，乐不思蜀",
        "background": "刘备长子，小名阿斗。十七岁嗣位，诸葛亮辅政。亮卒后蒋琬费祎相继执政。姜维屡北伐。后主宠宦官黄皓，朝政大乱。魏将邓艾灭蜀，禅降。",
        "initStats": {"treasury": 45, "people": 55, "military": 60, "court": 55, "health": 60, "tech": 30},
        "eraContext": "后主朝诸葛亮辅政，南征北伐。亮卒后蒋琬费祎继之，蜀汉得安。姜维北伐耗国力。宦官黄皓用事，朝政乱。邓艾偷渡阴平，后主降，蜀亡。",
        "tier": "A",
        "events": [
            {"year": 225, "month": null, "title": "诸葛亮南征", "description": "南中诸郡叛，诸葛亮率军南征。七擒七纵孟获，南人服。亮收南中金银以充军资，选劲卒为飞军。南中平，蜀汉后方固。", "historicalChoice": 0, "choices": ["令亮南征七擒孟获", "令亮速战平南不留患", "招降南中以省军费", "徙南中民于内地以避祸", "令李严守南中以分亮权"], "historicalOutcome": "亮平南中，蜀汉后方固"},
            {"year": 227, "month": null, "title": "出师北伐", "description": "诸葛亮上出师表，率军北驻汉中图中原。后主诏亮北伐。亮一出祁山，天水南安安定三郡叛魏应亮。马谡失街亭，亮退兵。", "historicalChoice": 0, "choices": ["令亮北伐图中原", "令亮守汉中不北伐", "令亮联吴共伐魏", "令亮南征以固后方", "令亮休兵以息民力"], "historicalOutcome": "亮北伐街亭败，退兵汉中"},
            {"year": 234, "month": null, "title": "亮薨五丈原", "description": "诸葛亮复出斜谷屯五丈原，与司马懿对峙。亮病薨于军中，年五十四。遗命蒋琬费祎继之。蜀军整军而退，懿不敢追。后主以亮故，任蒋琬辅政。", "historicalChoice": 0, "choices": ["任蒋琬继亮辅政", "令亮子瞻继亮之位", "令群臣共辅以分其权", "亲揽万机不假人权", "令魏延代亮统军"], "historicalOutcome": "亮薨五丈原，蒋琬继辅政"},
            {"year": 246, "month": null, "title": "费祎执政", "description": "蒋琬卒，费祎继之辅政。祎宽厚不欲妄动，姜维欲大举北伐，祎常裁制之。蜀汉得安。后祎为魏降人郭循所刺杀。", "historicalChoice": 0, "choices": ["任费祎辅政以安蜀", "任姜维大举北伐以图魏", "令群臣共辅以分其权", "亲揽万机不假人权", "任黄皓以制费祎"], "historicalOutcome": "费祎辅政蜀安，后见刺"},
            {"year": 253, "month": null, "title": "姜维北伐", "description": "费祎见刺，姜维专军政。维屡出陇右北伐魏，互有胜负。维才不及亮，用兵过度，蜀汉国力耗损。后主不能制。", "historicalChoice": 0, "choices": ["任姜维北伐以图魏", "止姜维北伐以息民力", "令姜维守汉中以固边", "联吴共伐魏以分势", "令姜维屯田以省军费"], "historicalOutcome": "姜维北伐耗蜀国力"},
            {"year": 257, "month": null, "title": "黄皓用事", "description": "后主宠宦官黄皓，皓与姜维不和。维请诛皓，后主不许。维惧，屯田沓中以避祸。蜀汉朝政大乱，后主不悟。", "historicalChoice": 0, "choices": ["宠黄皓，致姜维避祸", "诛黄皓以正朝纲", "用黄皓以制姜维", "令群臣公议黄皓之罪", "外放黄皓以远之"], "historicalOutcome": "黄皓用事，姜维避祸沓中"},
            {"year": 262, "month": null, "title": "姜维沓中", "description": "姜维畏黄皓，率军屯沓中麦田不归成都。魏将邓艾钟会谋伐蜀。维上表请增守阴平桥头，后主信黄皓巫鬼之言，不设备。", "historicalChoice": 0, "choices": ["信黄皓不备魏", "从姜维议守阴平", "召姜维还成都以备魏", "遣使求援于吴", "亲征以督诸军"], "historicalOutcome": "后主不备，魏军将至"},
            {"year": 263, "month": null, "title": "蜀亡降魏", "description": "魏遣邓艾钟会伐蜀。姜维拒钟会于剑阁。艾偷渡阴平至成都，后主降。维诈降钟会谋复蜀，事泄被杀。后主迁洛阳，封安乐公。", "historicalChoice": 0, "choices": ["降邓艾以全成都", "守成都待姜维回援", "南奔南中以图后举", "东奔孙权以求存", "死战以殉社稷"], "historicalOutcome": "后主降魏，蜀亡传四十三年"},
            {"year": 264, "month": null, "title": "乐不思蜀", "description": "后主降魏迁洛阳，封安乐公。司马昭宴之，作蜀乐。旧臣皆悲，后主喜笑自若。昭问颇思蜀否，禅曰此间乐不思蜀。郤正教之对，昭识其伪。", "historicalChoice": 0, "choices": ["乐不思蜀以自保", "泣思蜀以表忠心", "密谋复蜀以图后举", "请归蜀以终老", "厚赂司马昭以求安"], "historicalOutcome": "后主乐不思蜀，得保首领"},
        ],
    })

    # ========== 三国吴 ==========

    # 23. 吴大帝 孙权 (A)
    emperors.append({
        "id": "wu_dadi",
        "dynasty": "吴",
        "name": "孙权",
        "templeName": "吴大帝",
        "reignStart": 222, "reignEnd": 252,
        "evaluation": "据江东，三分天下",
        "background": "吴郡富春人，孙坚次子，孙策之弟。建安五年兄策卒，权嗣业年十九。赤壁之战破曹操，跨有荆扬。黄武元年称王，黄龙元年称帝，都建业。在位三十年。",
        "initStats": {"treasury": 55, "people": 55, "military": 70, "court": 60, "health": 60, "tech": 32},
        "eraContext": "孙权据江东，赤壁之战联刘破曹。后袭荆州杀关羽，夷陵之战败刘备。称藩于魏复叛，终称帝。晚年太子和鲁王霸二宫之争，国本动摇。",
        "tier": "A",
        "events": [
            {"year": 208, "month": null, "title": "赤壁之战", "description": "曹操致书孙权会猎于吴。权用周瑜鲁肃议，联刘备拒操。瑜为大都督，黄盖诈降火攻，大破操于赤壁。三分之势成。", "historicalChoice": 0, "choices": ["联刘备破操于赤壁", "降操以保江东", "独抗操不联刘备", "联刘表旧部抗操", "迁都以避操之锋"], "historicalOutcome": "权联刘破操于赤壁，三分之势成"},
            {"year": 219, "month": null, "title": "袭荆州", "description": "关羽北伐襄樊，后方空虚。孙权用吕蒙议，白衣渡江袭荆州。蒙擒杀关羽。权尽得荆州，跨有荆扬。刘备怒，将伐吴。", "historicalChoice": 0, "choices": ["袭荆州杀关羽以全据江东", "守湘水界不袭荆州", "联曹操共图关羽", "招降关羽以用其勇", "守江东以观时变"], "historicalOutcome": "权袭荆州杀关羽，跨有荆扬"},
            {"year": 221, "month": null, "title": "夷陵之战", "description": "刘备伐吴报仇。权用陆逊为大都督拒之。逊坚守不出，待备军疲怠，以火攻大破备于夷陵。备走白帝。权大胜，然亦疲弊。", "historicalChoice": 0, "choices": ["用陆逊破备于夷陵", "亲征以拒刘备", "求和于刘备以息兵", "求援于曹丕以拒备", "守江陵以待备粮尽"], "historicalOutcome": "逊破备于夷陵，吴胜"},
            {"year": 222, "month": null, "title": "称藩于魏", "description": "权破刘备后，恐魏袭其后，遣使称藩于魏。魏封权为吴王加九锡。权虽受封，然自置百官不朝魏。后魏索质子，权绝魏。", "historicalChoice": 0, "choices": ["称藩于魏以稳后方", "不降魏独抗蜀魏", "联蜀抗魏以图中原", "求和于刘备共抗魏", "迁都以避魏之锋"], "historicalOutcome": "权称藩于魏，后绝魏"},
            {"year": 229, "month": 4, "title": "称帝建吴", "description": "孙权称帝于武昌，改元黄龙，国号吴。追尊父坚为武烈皇帝。后迁都建业。三国皆称帝，三分之势定。", "historicalChoice": 0, "choices": ["称帝建吴，都建业", "守吴王之号不称帝", "都武昌以制荆扬", "联蜀共伐魏而后称帝", "缓称帝以观天下"], "historicalOutcome": "权称帝建吴，都建业"},
            {"year": 230, "month": null, "title": "卫温夷洲", "description": "孙权遣将军卫温、诸葛直将甲士万人浮海求夷洲亶洲。至夷洲，得数千人还。亶洲太远不得至。卫温等以违诏无功下狱诛。", "historicalChoice": 0, "choices": ["遣卫温浮海求夷洲", "罢海求以省军费", "令卫温取南海诸岛", "令卫温通商于倭", "亲征夷洲以拓疆"], "historicalOutcome": "卫温至夷洲，吴始通台湾"},
            {"year": 233, "month": null, "title": "公孙渊之叛", "description": "辽东公孙渊遣使称藩于吴。权大喜，封渊为燕王，遣太常张弥等将兵万人金宝甚盛送之。渊斩弥等首送魏，权怒欲亲征。", "historicalChoice": 0, "choices": ["怒欲亲征公孙渊", "忍怒遣使责让公孙渊", "联魏共讨公孙渊", "赦公孙渊以招降", "罢辽东之图以省军费"], "historicalOutcome": "权为公孙渊所卖，忍怒"},
            {"year": 241, "month": null, "title": "二宫之争", "description": "太子和与鲁王霸并宠，群臣分党。陆逊等拥护太子，全寄等附鲁王。权不能决，国本动摇。后废太子和，赐鲁王霸死，立孙亮为太子。", "historicalChoice": 0, "choices": ["废太子和立幼子亮", "固立太子和以正名分", "立鲁王霸以长幼为序", "令群臣议立储", "缓议储位以待时"], "historicalOutcome": "权废太子和立孙亮，国本摇"},
            {"year": 250, "month": null, "title": "废和赐霸", "description": "孙权废太子和为庶人，赐鲁王霸死。立少子亮为太子，以诸葛恪等辅之。权暮年多疑，杀张休顾谭等。吴国自此衰。", "historicalChoice": 0, "choices": ["废和赐霸，立亮为太子", "固立太子和不废", "立鲁王霸为太子", "令群臣公议立储", "立孙和子孙皓以续正统"], "historicalOutcome": "权废和立亮，托孤诸葛恪"},
            {"year": 252, "month": 4, "title": "权崩建业", "description": "孙权崩于建业，年七十一。太子亮嗣位年十岁，诸葛恪辅政。权据江东五十二年，开吴国，三国在位最久之君。", "historicalChoice": 0, "choices": ["太子亮嗣位，诸葛恪辅政", "令太后辅政以固幼主", "择宗室长者摄政", "令群臣共辅以分其权", "独任诸葛恪以专责成"], "historicalOutcome": "会稽王亮嗣位，诸葛恪辅政"},
        ],
    })

    # 24. 吴会稽王 孙亮 (B)
    emperors.append({
        "id": "wu_huikuwangliang",
        "dynasty": "吴",
        "name": "孙亮",
        "templeName": "吴会稽王",
        "reignStart": 252, "reignEnd": 258,
        "evaluation": "幼主聪慧，被废为侯",
        "background": "孙权少子，十岁即位，诸葛恪辅政。恪专权，孙峻杀之。峻从弟綝继专权。亮聪慧，谋诛綝，事泄被废为会稽王。",
        "initStats": {"treasury": 48, "people": 50, "military": 50, "court": 35, "health": 50, "tech": 32},
        "eraContext": "会稽王朝诸葛恪辅政专权，孙峻杀恪专权。峻死弟綝继。亮欲诛綝，事泄被废。吴国权臣专政，国势渐衰。",
        "tier": "B",
        "events": [
            {"year": 253, "month": null, "title": "诸葛恪专权", "description": "诸葛恪辅政，大失众望。恪出兵攻魏合肥新城，大败而归。孙峻与亮谋，伏兵杀恪于宴。峻为大将军，专吴政。", "historicalChoice": 0, "choices": ["用孙峻杀诸葛恪", "任诸葛恪辅政不杀", "令群臣共辅以分其权", "亲揽万机不假人权", "外放诸葛恪以远之"], "historicalOutcome": "孙峻杀恪，专吴政"},
            {"year": 255, "month": null, "title": "孙峻专政", "description": "孙峻辅政专权，杀废太子和。文钦降吴，峻令钦等击魏。峻病薨，从弟綝继辅政。峻虽专权，然能御魏。", "historicalChoice": 0, "choices": ["任孙峻辅政专权", "抑孙峻用儒臣辅政", "令群臣共辅以分其权", "外放孙峻以远之", "亲揽万机不假人权"], "historicalOutcome": "峻辅政专权，后薨綝继"},
            {"year": 258, "month": 9, "title": "亮被废", "description": "亮年长，恶孙綝专权，谋诛之。事泄，綝废亮为会稽王，立琅琊王休为帝。亮后为休贬为候官侯，道中自杀。", "historicalChoice": 0, "choices": ["綝废亮立休", "亮先发诛綝以保位", "令群臣公议废立", "立宗室长者摄政", "令太后临朝称制"], "historicalOutcome": "綝废亮立景帝休"},
        ],
    })

    # 25. 吴景帝 孙休 (B)
    emperors.append({
        "id": "wu_jingdi",
        "dynasty": "吴",
        "name": "孙休",
        "templeName": "吴景帝",
        "reignStart": 258, "reignEnd": 264,
        "evaluation": "诛綝修政，在位六年",
        "background": "孙权第六子。孙綝废会稽王亮，迎立之。休与张布丁奉谋诛綝。在位六年，修政安民。蜀亡后吴益孤。崩，群臣立孙皓。",
        "initStats": {"treasury": 50, "people": 52, "military": 50, "court": 50, "health": 50, "tech": 32},
        "eraContext": "景帝休朝诛孙綝，修政安民。蜀汉亡，吴益孤立。魏司马昭将伐吴。休欲联蜀抗魏，蜀已亡。托孤于濮阳兴张布。",
        "tier": "B",
        "events": [
            {"year": 258, "month": 12, "title": "诛孙綝", "description": "孙休与张布丁奉谋，于腊会伏兵擒孙綝。綝叩头请为奴不得，伏诛。夷三族。休始亲政，以张布为左将军丁奉为大将军。", "historicalChoice": 0, "choices": ["诛孙綝以亲政", "留孙綝辅政以安权臣", "外放孙綝以远之", "令群臣公议綝之罪", "厚赐孙綝而不授权"], "historicalOutcome": "休诛綝亲政，吴政渐安"},
            {"year": 262, "month": null, "title": "蜀求援", "description": "蜀汉为魏所逼，遣使求援于吴。休遣兵攻魏寿春以分其势。次年蜀亡，吴益孤。休忧惧，增兵守西陵。", "historicalChoice": 0, "choices": ["出兵击魏以援蜀", "守境不救蜀以自保", "联魏灭蜀以分其地", "遣使调停以息兵", "徙西陵民于内地以避祸"], "historicalOutcome": "吴出兵援蜀，蜀旋亡"},
            {"year": 264, "month": 7, "title": "休崩", "description": "孙休崩于建业，年三十。太子𩅦年幼，群臣以蜀新亡，宜立长君。濮阳兴张布迎立乌程侯皓。皓即位后荒暴，吴遂亡。", "historicalChoice": 0, "choices": ["太子𩅦嗣位", "迎乌程侯皓入继", "择宗室长者入继", "令群臣议择贤而立", "立孙和子孙皓以续正统"], "historicalOutcome": "群臣迎孙皓，吴遂亡"},
        ],
    })

    # 26. 吴末帝 孙皓 (B)
    emperors.append({
        "id": "wu_modihao",
        "dynasty": "吴",
        "name": "孙皓",
        "templeName": "吴末帝",
        "reignStart": 264, "reignEnd": 280,
        "evaluation": "荒暴之主，吴亡降晋",
        "background": "孙和之子，字元宗。景帝崩，群臣迎立之。初政尚可，后荒暴，杀忠臣，沉湎酒色。晋伐吴，皓降。吴亡，传五十九年。",
        "initStats": {"treasury": 42, "people": 40, "military": 42, "court": 30, "health": 45, "tech": 32},
        "eraContext": "末帝皓朝荒暴杀忠臣。晋已代魏，势强。陆抗守西陵御晋，抗卒后吴无良将。晋伐吴，皓降，三国终归一统于晋。",
        "tier": "B",
        "events": [
            {"year": 266, "month": null, "title": "迁都武昌", "description": "孙皓迁都武昌，扬俗云宁饮建业水不食武昌鱼。民怨。施但等因民怨反于建业，皓还都建业。", "historicalChoice": 0, "choices": ["迁都武昌以避晋", "留都建业以安民", "两都并立以备不虞", "迁都于会稽以近故里", "迁都于交州以避祸"], "historicalOutcome": "皓迁都武昌旋还建业"},
            {"year": 272, "month": null, "title": "陆抗守西陵", "description": "晋将羊祜伐吴，吴将陆抗守西陵拒之。抗大破晋将步阐于西陵。晋不敢犯。抗卒后，吴无良将，晋遂谋伐吴。", "historicalChoice": 0, "choices": ["任陆抗守西陵以拒晋", "令陆抗出击以攻晋", "求和于晋以息兵", "令群臣共议御晋之策", "徙西陵民于内地以避祸"], "historicalOutcome": "陆抗守西陵，晋不敢犯"},
            {"year": 274, "month": null, "title": "抗卒吴衰", "description": "陆抗卒，吴失长城。抗遗言请增守西陵以防晋。皓不纳。晋益图吴，王濬造楼船于蜀，羊祜杜预等谋伐吴。", "historicalChoice": 0, "choices": ["不从抗言增守西陵", "从抗言增守西陵以防晋", "求和于晋以息兵", "令群臣共议御晋之策", "亲征以督诸军"], "historicalOutcome": "皓不纳抗言，晋益图吴"},
            {"year": 279, "month": 11, "title": "晋伐吴", "description": "晋遣杜预王浑王濬等六路伐吴。濬率楼船顺江东下，吴军望风而降。皓遣将拒之皆败。皓议降。", "historicalChoice": 0, "choices": ["遣将拒晋以死战", "降晋以求免死", "南奔交州以图后举", "遣使求和于晋", "亲征以振军威"], "historicalOutcome": "晋六路伐吴，吴军皆败"},
            {"year": 280, "month": 3, "title": "皓降吴亡", "description": "晋将王濬入建业，孙皓面缚舆榇而降。吴亡，传五十九年。三国归一统于晋。皓迁洛阳，封归命侯，后病终。", "historicalChoice": 0, "choices": ["面缚舆榇降晋", "死战以殉社稷", "南奔交州以图后举", "自杀以殉社稷", "请为藩臣以求存"], "historicalOutcome": "皓降晋，吴亡，三国终"},
        ],
    })

    return emperors
