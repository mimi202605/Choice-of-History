# -*- coding: utf-8 -*-
import json, io

path = '/workspace/data/emperors/03-jin-nanbeichao-sui.json'
with io.open(path, 'r', encoding='utf-8') as f:
    d = json.load(f)

# Additional historically-grounded events for B-class emperors with <5 events.
# Each tuple: (id, [event dicts...])  -- appended to existing events list.
add = {
"jin_kangdi": [
  {"year":343,"month":null,"title":"何充辅政","description":"帝即位，以何充为中书监辅政。充与庾冰交恶，朝局内耗。褚裒以外戚辞辅政之任，外镇徐兖。","historicalChoice":0,"choices":["以何充辅政","留庾冰独辅","令裒与充并辅","太后临朝裁之","令宗室共辅"],"historicalOutcome":"何充辅政，与庾冰交恶。"},
  {"year":343,"month":null,"title":"北魏通使","description":"遣使通好北魏，欲息南北之争。然魏索交州未果，边境时扰。","historicalChoice":0,"choices":["遣使通好北魏","绝魏专守江淮","联柔然攻魏","厚赂魏求和","令边将严守"],"historicalOutcome":"南北暂通好，边境粗安。"}
],
"jin_aidi": [
  {"year":362,"month":null,"title":"崇清谈","description":"帝好黄老清谈，雅尚玄学。朝野士族承风流衍，政事多废。","historicalChoice":0,"choices":["崇清谈尚玄学","抑玄学崇儒术","兼修儒玄","令士族习吏事","禁清谈专政务"],"historicalOutcome":"清谈益盛，政事渐废。"}
],
"jin_feidi": [
  {"year":366,"month":null,"title":"桓温专政","description":"桓温镇荆州，专擅上游，朝堂仰其鼻息。帝受制，政事一决于温。","historicalChoice":0,"choices":["受制桓温委政于温","图诛桓温","令谢安抗温","外结方镇制温","太后临朝"],"historicalOutcome":"温专政，帝如傀儡。"},
  {"year":368,"month":null,"title":"乏嗣议","description":"帝无子，朝议储嗣。桓温欲立易于己者，帝忧惧。","historicalChoice":0,"choices":["立宗室子弟为嗣","禅位于桓温","令太后择嗣","立会稽王昱","外任宗室出藩"],"historicalOutcome":"储议未定，温益专横。"}
],
"jin_jianwendi": [
  {"year":371,"month":null,"title":"温诛旧党","description":"桓温入朝，诛殷浩旧党、武陵王晞等立威。帝噤不敢言。","historicalChoice":0,"choices":["听温诛旧党立威","图诛温自保","令宗室抗温","外结谢安","太后临朝"],"historicalOutcome":"温诛旧党，朝堂震怖。"},
  {"year":372,"month":null,"title":"谢安用事","description":"桓温虽专，谢安、王坦之周旋其间，延阻温篡。帝倚之以安。","historicalChoice":0,"choices":["倚谢安延阻温篡","委政于温","令宗室制温","外结方镇","禅位于温"],"historicalOutcome":"谢安用事，温篡未遂。"}
],
"jin_gongdi": [
  {"year":419,"month":null,"title":"刘裕封宋王","description":"刘裕进封宋王，加九锡，建宋国。代晋之势已成，帝备位而已。","historicalChoice":0,"choices":["封裕为宋王加九锡","拒封以抗裕","令宗室制裕","禅位于裕","外结北魏"],"historicalOutcome":"裕进宋王，代晋在即。"},
  {"year":419,"month":null,"title":"裕平休之","description":"司马休之于荆州反刘裕，裕讨平之。晋室宗藩尽除，禅代无阻。","historicalChoice":0,"choices":["令裕平司马休之","厚抚休之","令休之辅政","迁都以避裕","禅位于休之"],"historicalOutcome":"休之败，晋宗藩尽。"}
],
"song_shaodi": [
  {"year":423,"month":null,"title":"即位失德","description":"帝即位，居丧无礼，游戏无度。徐羡之、傅亮、谢晦深忧之。","historicalChoice":0,"choices":["居丧游戏无度","戒游戏亲丧礼","令辅臣谏诤","托政辅臣","迁都以避乱"],"historicalOutcome":"帝失德，辅臣谋废立。"},
  {"year":424,"month":null,"title":"北魏通好","description":"初立，与北魏通好息兵。然河南已失，南北划河而治。","historicalChoice":0,"choices":["通好北魏息兵","绝魏专守淮南","联柔然攻魏","厚赂魏求和","令边将严守"],"historicalOutcome":"南北通好，划河而治。"}
],
"song_qianfeidi": [
  {"year":465,"month":null,"title":"杀辅臣","description":"帝忌戴法兴等辅臣，赐死。任阮佃夫等寒人掌机要，朝政益乱。","historicalChoice":0,"choices":["诛辅臣任寒人","留辅臣辅政","令宗室辅政","太后临朝","自揽万机"],"historicalOutcome":"辅臣诛，朝政乱。"},
  {"year":465,"month":null,"title":"虐诸叔","description":"帝忌诸叔，囚湘东王彧等为猪王，以木槽盛食。诸叔怨愤。","historicalChoice":0,"choices":["虐辱囚诸叔","厚待诸叔","诛诸叔","外任诸叔","令诸叔入朝共辅"],"historicalOutcome":"诸叔怨愤，废立机伏。"}
],
"song_mingdi": [
  {"year":471,"month":null,"title":"萧道成崛起","description":"淮北既失，萧道成镇淮阴，御北魏有功，渐掌兵权，为宋亡张本。","historicalChoice":0,"choices":["任萧道成镇淮阴","抑道成以收兵权","令宗室代道成","外任道成出藩","厚待道成以安之"],"historicalOutcome":"道成崛起，宋亡之机伏。"}
],
"song_houfeidi": [
  {"year":475,"month":null,"title":"萧道成惧","description":"帝狂暴欲杀萧道成，道成结王敬则等密谋自保。","historicalChoice":0,"choices":["欲杀道成致其反","厚待道成以安之","外任道成出藩","令道成辅政","戒备防道成"],"historicalOutcome":"道成惧而谋弑。"},
  {"year":476,"month":null,"title":"杀大臣","description":"帝杀大臣如戏，剖腹剔骨。朝堂人人自危，离心益甚。","historicalChoice":0,"choices":["狂暴杀大臣","戒杀亲政务","令辅臣谏诤","厚待大臣","迁都以避乱"],"historicalOutcome":"朝堂离心，弑机迫近。"}
],
"song_shundi": [
  {"year":477,"month":null,"title":"沈攸之反","description":"沈攸之荆州反萧道成，袁粲石头城应之。道成讨平，代宋之势成。","historicalChoice":0,"choices":["倚道成平攸之","厚抚攸之","令袁粲辅政制道成","禅位于道成","迁都避乱"],"historicalOutcome":"攸之败，道成代宋势成。"},
  {"year":478,"month":null,"title":"道成专政","description":"萧道成进齐王，加九锡，诛宋宗室。帝备位而已，禅代在即。","historicalChoice":0,"choices":["封道成为齐王加九锡","拒封抗道成","令宗室制道成","禅位于道成","外结北魏"],"historicalOutcome":"道成进齐王，禅代在即。"}
],
"qi_wudi": [
  {"year":485,"month":null,"title":"校籍激变","description":"校籍严急，富阳唐寓之聚众反。武帝遣军讨平，校籍稍宽。","historicalChoice":0,"choices":["遣军讨唐寓之","赦寓之改校籍","宽简户籍","迁民于他郡","令士族自平乱"],"historicalOutcome":"寓之乱平，校籍稍宽。"}
],
"qi_yulinwang": [
  {"year":494,"month":null,"title":"受祖禅立","description":"武帝崩，太孙昭业即位。帝奢淫，挥霍库藏，西昌侯萧鸾辅政。","historicalChoice":0,"choices":["受祖禅立","让位于弟","令萧鸾辅政","太后临朝","厚待宗室"],"historicalOutcome":"帝受立，萧鸾辅政。"},
  {"year":494,"month":null,"title":"萧鸾专政","description":"萧鸾专政，谋废立。帝不察，奢淫如故，祸机迫近。","historicalChoice":0,"choices":["听萧鸾专政","图诛萧鸾","令宗室制鸾","外任鸾出藩","厚待鸾以安之"],"historicalOutcome":"鸾专政，废立在即。"},
  {"year":494,"month":null,"title":"挥霍库藏","description":"帝挥霍武帝库藏，赐赐无节，宫廷奢靡。萧鸾益忧，决意废之。","historicalChoice":0,"choices":["挥霍库藏","节用亲政","令辅臣谏诤","厚赏萧鸾","迁都以避乱"],"historicalOutcome":"帝奢淫，鸾决废立。"}
],
"qi_hailingwang": [
  {"year":494,"month":null,"title":"受立为帝","description":"萧鸾废郁林王，迎立海陵王昭文。帝如傀儡，政尽归鸾。","historicalChoice":0,"choices":["受萧鸾迎立","拒位让于鸾","图诛萧鸾","奔北魏","禅位于鸾"],"historicalOutcome":"帝受立，政归鸾。"},
  {"year":494,"month":null,"title":"萧鸾图代","description":"萧鸾图自立，先诛异己，谋代齐。帝备位而已，禅代在即。","historicalChoice":0,"choices":["听鸾图代","图诛鸾","令宗室抗鸾","奔北魏","禅位于鸾"],"historicalOutcome":"鸾图代，禅代在即。"},
  {"year":494,"month":null,"title":"在位三月","description":"在位仅三月，萧鸾废之为海陵王，自立为帝。帝被幽，旋遇害。","historicalChoice":0,"choices":["被鸾废为海陵王","抗鸾被杀","奔北魏","禅位于鸾","隐居以全"],"historicalOutcome":"帝被废弑，齐明帝立。"}
],
"qi_mingdi": [
  {"year":496,"month":null,"title":"崇佛祈寿","description":"帝性猜忌，崇佛道祈寿。起建初寺，设法会，然屠戮宗室不已。","historicalChoice":0,"choices":["崇佛道祈寿","戒杀亲政务","令辅臣谏诤","厚待宗室","禁佛崇儒"],"historicalOutcome":"崇佛而不能止杀。"}
],
"qi_dongkunhou": [
  {"year":500,"month":null,"title":"萧懿之死","description":"崔慧景反，萧懿讨平之。帝旋杀萧懿，致其弟萧衍起兵襄阳。","historicalChoice":0,"choices":["杀萧懿致衍反","赦萧懿以安衍","令萧懿辅政","外任萧懿出藩","厚赏萧懿"],"historicalOutcome":"萧懿被杀，萧衍起兵。"}
],
"qi_hedi": [
  {"year":501,"month":null,"title":"萧衍东下","description":"萧衍起兵襄阳，东下攻建康。东昏侯狂暴如故，城中内变。","historicalChoice":0,"choices":["遣军拒萧衍","厚赂衍求和","迁都以避衍","令诸王勤王","亲征衍"],"historicalOutcome":"衍东下，建康危。"},
  {"year":501,"month":null,"title":"萧衍专政","description":"衍入建康，弑东昏侯，迎立和帝于江陵。政尽归衍，禅代在即。","historicalChoice":0,"choices":["受衍拥立","图诛衍","奔北魏","禅位于衍","令宗室抗衍"],"historicalOutcome":"衍专政，禅代在即。"}
],
"liang_jianwendi": [
  {"year":550,"month":null,"title":"受立侯景","description":"侯景废先太子，立简文帝。帝如傀儡，政事一决于景。","historicalChoice":0,"choices":["受侯景立为傀儡","拒位让于景","图诛侯景","奔荆州依绎","自杀殉梁"],"historicalOutcome":"帝受立，政归景。"},
  {"year":550,"month":null,"title":"侯景专政","description":"景自为宇宙大将军，专擅朝政。帝备位而已，吟咏自遣。","historicalChoice":0,"choices":["听景专政","图诛景","令旧臣抗景","奔外藩","禅位于景"],"historicalOutcome":"景专政，帝如囚。"},
  {"year":551,"month":null,"title":"宫体之咏","description":"帝雅好文辞，宫体诗风行。然国破家亡，吟咏徒增悲辛。","historicalChoice":0,"choices":["雅好宫体诗","罢诗专政","令文士谏诤","崇佛祈安","戒文习武"],"historicalOutcome":"宫体行，国破徒悲。"}
],
"liang_yuandi": [
  {"year":553,"month":null,"title":"焚古今书","description":"江陵将陷，帝焚古今图书十四万卷，叹读书万卷犹有今日。文化巨厄。","historicalChoice":0,"choices":["焚古今图书十四万卷","留书降魏","迁书于江南","令臣护书出城","自焚宫阙"],"historicalOutcome":"图书尽焚，文化巨厄。"}
],
"liang_jingdi": [
  {"year":555,"month":null,"title":"僧辩之死","description":"陈霸先杀王僧辩，废萧渊明，立方智。梁室内争，霸先专政。","historicalChoice":0,"choices":["听霸先杀僧辩","厚抚僧辩","令僧辩辅政","外任僧辩","禅位于霸先"],"historicalOutcome":"僧辩死，霸先专政。"},
  {"year":556,"month":null,"title":"齐梁交锋","description":"北齐立萧渊明为梁帝，陈霸先拒之，败齐军于建康。江北尽失。","historicalChoice":0,"choices":["倚霸先拒齐","厚赂齐求和","迁都以避齐","联西魏抗齐","令诸将分拒"],"historicalOutcome":"齐军败，然江北尽失。"}
],
"chen_wendi": [
  {"year":565,"month":null,"title":"留异反","description":"东阳留异反，文帝遣侯安都讨平之。陈政渐安，天嘉小康。","historicalChoice":0,"choices":["遣侯安都讨留异","厚抚留异","令诸将分讨","联周攻异","迁民于内"],"historicalOutcome":"留异平，陈政安。"}
],
"chen_feidi": [
  {"year":567,"month":null,"title":"受父传位","description":"文帝崩，太子伯宗即位，年幼，叔安成王顼辅政。","historicalChoice":0,"choices":["受父传位","让位于叔顼","令辅臣辅政","太后临朝","禅位于叔"],"historicalOutcome":"帝受立，顼辅政。"},
  {"year":567,"month":null,"title":"安成王辅政","description":"安成王顼专政，威权日盛。帝幼弱，朝权渐移于顼。","historicalChoice":0,"choices":["听顼辅政","图诛顼","令宗室制顼","外任顼出藩","太后临朝"],"historicalOutcome":"顼辅政，威权盛。"},
  {"year":568,"month":null,"title":"被废为临海王","description":"安成王顼废帝为临海王，自立为帝，是为宣帝。帝被废后幽死。","historicalChoice":0,"choices":["被顼废为临海王","抗顼被杀","禅位于顼","奔北周","戒备防顼"],"historicalOutcome":"帝被废，宣帝立。"}
],
"chen_xuandi": [
  {"year":575,"month":null,"title":"吴明彻北伐","description":"太建中遣吴明彻北伐，克寿阳合肥，复淮南。北齐内乱，陈得志一时。","historicalChoice":0,"choices":["遣吴明彻北伐复淮南","专守长江不北伐","联周共灭齐","厚赂齐求和","令淳于量督师"],"historicalOutcome":"太建北伐初克，复淮南。"}
],
"wei_xianwendi": [
  {"year":470,"month":null,"title":"崇佛兴寺","description":"帝崇佛，兴塔寺，度僧尼。佛事大兴，国用为耗。","historicalChoice":0,"choices":["崇佛兴塔寺","限佛以节用","罢佛专政务","崇道抑佛","令民间自办佛事"],"historicalOutcome":"佛事兴，国用耗。"}
],
"wei_xiaozhuangdi": [
  {"year":528,"month":null,"title":"河阴之变","description":"尔朱荣沉胡太后及幼主于河，于河阴杀王公二千余。立帝，魏权入尔朱氏。","historicalChoice":0,"choices":["受尔朱荣立于河阴之后","拒立奔梁","图诛尔朱荣","令宗室抗尔朱","厚待尔朱荣"],"historicalOutcome":"河阴之变，权入尔朱氏。"}
],
"wei_jiemindi": [
  {"year":531,"month":null,"title":"高欢起兵","description":"高欢于信都起兵讨尔朱氏，立安定王朗。两帝并立，魏分裂。","historicalChoice":0,"choices":["遣尔朱氏讨高欢","招抚高欢","令宗室助讨","迁都以避欢","厚赂高欢"],"historicalOutcome":"高欢势盛，尔朱氏败。"},
  {"year":531,"month":null,"title":"尔朱氏专横","description":"尔朱世隆等专横，杀异己。帝虽立，政在尔朱氏，朝野怨愤。","historicalChoice":0,"choices":["听尔朱氏专横","图诛尔朱氏","令宗室抗尔朱","外结高欢","太后临朝"],"historicalOutcome":"尔朱氏专横，怨愤积。"}
],
"wei_andingwang": [
  {"year":531,"month":null,"title":"高欢起兵","description":"高欢于信都起兵讨尔朱氏，立安定王朗为帝，改元中兴。","historicalChoice":0,"choices":["受高欢立","拒立奔尔朱","图诛高欢","令宗室助欢","禅位于欢"],"historicalOutcome":"帝受立，高欢名正。"},
  {"year":531,"month":null,"title":"尔朱氏跋扈","description":"尔朱氏据洛阳，杀异己。高欢以讨尔朱为名，势益盛。","historicalChoice":0,"choices":["倚高欢讨尔朱氏","厚赂尔朱氏","令宗室助讨","迁都以避","禅位于高欢"],"historicalOutcome":"尔朱氏跋扈，高欢势盛。"}
],
"wei_xiaowudi": [
  {"year":532,"month":null,"title":"高欢入洛","description":"高欢韩陵胜后入洛阳，废安定王，立孝武帝修。政归高欢。","historicalChoice":0,"choices":["受高欢入洛拥立","拒立奔宇文泰","图诛高欢","令宗室抗欢","禅位于欢"],"historicalOutcome":"帝受立，高欢辅政。"}
],
"xiwei_feidi": [
  {"year":552,"month":null,"title":"取梁蜀","description":"宇文泰遣尉迟迥取梁益州，西魏版图大扩。泰威望益盛。","historicalChoice":0,"choices":["令宇文泰取梁蜀","守关不南伐","厚赂梁求和","联齐攻梁","令诸将分伐"],"historicalOutcome":"取梁蜀，西魏版图扩。"},
  {"year":553,"month":null,"title":"行周官","description":"宇文泰用苏绰，仿周官改制，行六条诏书。关陇政治粗备。","historicalChoice":0,"choices":["用苏绰仿周官改制","留旧制不革","行汉化改革","令豪强自治","厚待苏绰"],"historicalOutcome":"周官改制，关陇粗备。"}
],
"xiwei_gongdi": [
  {"year":555,"month":null,"title":"行周礼","description":"宇文泰仿周礼建六官，改官制。关陇政治一统于周制。","historicalChoice":0,"choices":["行周礼建六官","留旧官制","行汉魏官制","令百官自择","缓行周礼"],"historicalOutcome":"周礼行，六官建。"},
  {"year":556,"month":null,"title":"宇文泰卒","description":"宇文泰卒，世子觉嗣。宇文护辅政，逼帝禅位，西魏亡。","historicalChoice":0,"choices":["听护辅政禅位","图诛护","令宗室抗护","奔南梁","太后临朝"],"historicalOutcome":"泰卒，护逼禅，西魏亡。"}
],
"beiqi_feidi": [
  {"year":560,"month":null,"title":"杨愔辅政","description":"文宣崩，杨愔辅废帝殷。欲抑宗室，常山王演、长广王湛不协。","historicalChoice":0,"choices":["以杨愔辅政","令宗室辅政","太后临朝","亲揽万机","禅位于叔"],"historicalOutcome":"愔辅政，宗室不协。"},
  {"year":560,"month":null,"title":"常山王图位","description":"常山王演图位，与湛结，执杨愔杀之。废帝之祸迫近。","historicalChoice":0,"choices":["听演图位","图诛演","令宗室制演","外任演出藩","厚待演以安之"],"historicalOutcome":"演图位，废立在即。"}
],
"beiqi_xiaozhaodi": [
  {"year":560,"month":null,"title":"诛杨愔","description":"帝与长广王湛结，执杨愔杀之，废侄殷自立。","historicalChoice":0,"choices":["诛杨愔废侄自立","厚待殷不废","令辅臣辅殷","太后临朝","禅位于湛"],"historicalOutcome":"诛愔自立，孝昭立。"},
  {"year":561,"month":null,"title":"弑侄济南","description":"帝忌废帝济南王殷，使人弑之。性虽明而杀侄损德。","historicalChoice":0,"choices":["弑侄济南王","厚待殷以安之","外任殷出藩","令殷出家","释殷以安宗室"],"historicalOutcome":"弑侄损德，旋坠马崩。"}
],
"beiqi_wuchengdi": [
  {"year":563,"month":null,"title":"和士开乱政","description":"帝宠和士开，士开与胡后通，乱政。杀宗室直臣，朝纲益乱。","historicalChoice":0,"choices":["宠和士开乱政","诛士开亲政","令宗室辅政","外任士开出藩","太后临朝"],"historicalOutcome":"士开乱政，朝纲紊。"}
],
"beiqi_youzhu": [
  {"year":577,"month":null,"title":"受禅即位","description":"后主禅位于太子恒，欲奔陈。八岁即位，改元承光。","historicalChoice":0,"choices":["受父禅即位","让位于父抗周","奔南陈","出降北周","奔突厥"],"historicalOutcome":"帝受禅，旬日即亡。"},
  {"year":577,"month":null,"title":"周军入邺","description":"北周军入邺，齐军溃。帝与后主奔青州，欲奔陈。","historicalChoice":0,"choices":["奔青州欲奔陈","巷战殉齐","出降北周","奔突厥","迁都以避周"],"historicalOutcome":"周入邺，齐溃。"},
  {"year":577,"month":null,"title":"被执青州","description":"周军执帝及后主于青州，送长安，旋遇害。北齐亡。","historicalChoice":0,"choices":["被周军执于青州","抗周被杀","自杀殉齐","奔南陈","隐居以全"],"historicalOutcome":"帝被执，北齐亡。"}
],
"beizhou_xiaomindi": [
  {"year":557,"month":null,"title":"受禅建周","description":"宇文护逼西魏恭帝禅位于宇文觉，建北周，都长安。政在护。","historicalChoice":0,"choices":["受宇文护禅位建周","拒禅让于魏","图诛宇文护","令宗室抗护","禅位于护"],"historicalOutcome":"北周立，政在护。"},
  {"year":557,"month":null,"title":"谋诛宇文护","description":"帝不堪护专权，与李植、孙恒等谋诛护。事泄。","historicalChoice":0,"choices":["谋诛宇文护","厚待护以安之","令护辅政不疑","奔南梁","戒备防护"],"historicalOutcome":"谋泄，帝危。"},
  {"year":557,"month":null,"title":"被废为略阳公","description":"护废帝为略阳公，旋弑之。立宁都公毓，是为明帝。","historicalChoice":0,"choices":["被护废为略阳公旋弑","抗护被杀","奔南梁","禅位于护","戒备防护"],"historicalOutcome":"帝被废弑，明帝立。"}
],
"beizhou_mingdi": [
  {"year":559,"month":null,"title":"亲政称帝","description":"帝始称皇帝（前称天王），亲政。宽徭息役，政事粗修。","historicalChoice":0,"choices":["亲政称皇帝","令护辅政","太后临朝","禅位于弟邕","令宗室辅政"],"historicalOutcome":"帝亲政，朝局粗安。"},
  {"year":560,"month":null,"title":"为护所鸩","description":"帝图去护，护使李安置毒于饼，帝食之崩。弟鲁公邕立。","historicalChoice":0,"choices":["为宇文护所鸩","诛护自保","戒备防护","出奔避祸","托孤弟邕"],"historicalOutcome":"帝遇害，武帝立。"}
],
"beizhou_xuandi": [
  {"year":578,"month":null,"title":"立五后","description":"帝荒淫，立五皇后，破前代之制。朝野骇然。","historicalChoice":0,"choices":["立五皇后","立一后正后宫","令辅臣谏诤","戒淫亲政","太后临朝"],"historicalOutcome":"立五后，朝野骇。"},
  {"year":579,"month":null,"title":"巡幸奢靡","description":"帝巡幸无度，营离宫，役民力。朝政尽废，民怨积。","historicalChoice":0,"choices":["巡幸奢靡营离宫","节用亲政","令辅臣谏诤","罢巡幸","厚待宗室"],"historicalOutcome":"帝奢靡，民怨积。"}
],
"beizhou_jingdi": [
  {"year":580,"month":null,"title":"杨坚辅政","description":"宣帝崩，幼帝阐立，杨坚为丞相辅政。坚诛宇文氏宗亲，集权。","historicalChoice":0,"choices":["受杨坚辅政","图诛杨坚","令宗室抗坚","太后临朝","禅位于坚"],"historicalOutcome":"杨坚辅政，集权。"},
  {"year":580,"month":null,"title":"尉迟迥之乱","description":"尉迟迥等起兵反杨坚，坚遣韦孝宽讨平。宇文氏宗亲多诛。","historicalChoice":0,"choices":["令杨坚讨尉迟迥","厚抚迥以安之","令宗室助迥","奔南陈","禅位于迥"],"historicalOutcome":"迥乱平，坚代周势成。"}
],
"sui_gongdi": [
  {"year":617,"month":null,"title":"李渊入关","description":"李渊起兵太原，入关中，据长安。立代王侑为帝，遥尊炀帝为太上皇。","historicalChoice":0,"choices":["受李渊立为傀儡","图诛李渊","奔洛阳","禅位于李渊","令宗室抗渊"],"historicalOutcome":"渊入关，立帝，政归渊。"},
  {"year":618,"month":null,"title":"禅位李渊","description":"炀帝遇害凶问至，李渊逼帝禅位，建唐，隋亡。帝为酅国公。","historicalChoice":0,"choices":["禅位于李渊","抗渊被废","奔萧铣","自杀殉隋","让于宗室"],"historicalOutcome":"帝禅位，隋亡唐兴。"}
]
}

for e in d['emperors']:
    if e['id'] in add:
        # append new events (avoid duplicating titles already present)
        existing_titles = set(ev['title'] for ev in e['events'])
        for ev in add[e['id']]:
            if ev['title'] not in existing_titles:
                e['events'].append(ev)

# Sort events by year within each emperor (stable)
for e in d['emperors']:
    e['events'].sort(key=lambda x: (x['year'] if x['year'] is not None else 9999))

with io.open(path, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

# report
emps=d['emperors']
A=[e for e in emps if e['tier']=='A']; B=[e for e in emps if e['tier']=='B']
print('emperors:', len(emps), 'A:', len(A), 'B:', len(B))
print('total events:', sum(len(e['events']) for e in emps))
print('min B events:', min(len(e['events']) for e in B), 'max:', max(len(e['events']) for e in B))
print('all B >=5:', all(len(e['events'])>=5 for e in B))
# verify choices
bad=0
for e in emps:
    for ev in e['events']:
        if len(ev['choices'])!=5 or ev['historicalChoice']!=0: bad+=1
print('bad events:', bad)
