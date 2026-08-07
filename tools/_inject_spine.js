// P3 铺陈合并脚本：把 spine 安全注入 data/emperors/*.json
// 仅新增 reignPremise/voiceTag/cast 三字段；已有 reignPremise 者跳过（保留手写精修版）
const fs = require('fs');
const path = require('path');

const SPINE_A = require('./_spine_a.js');
const SPINE_SONG_MING = require('./_spine_song_ming.js');
const ALL_SPINE = Object.assign({}, SPINE_A, SPINE_SONG_MING);

const dataDir = path.join(__dirname, '..', 'data', 'emperors');
const files = fs.readdirSync(dataDir).filter(f => f.endsWith('.json'));

// 朝代 -> 主线索模板生成器（用于 Tier B/C 无精修表的帝）
// 返回 { premise, voice, cast? }
function dynastyTemplate(dyn, e) {
  const name = e.name || e.templeName || e.id;
  const tmpl = {
    '夏': { p: `${name}继夏后之绪，值诸侯渐畔、德衰之世，能否以一人之威、挽将倾之鼎？`, v: '冷峻' },
    '商': { p: `${name}承商室之运，处宗祀兴衰之际，能否以祭与兵、安动摇之社稷？`, v: '质朴' },
    '周': { p: `${name}当东迁之后、王室式微，能否以名义之尊、制方伯之横？`, v: '华赡' },
    '秦': { p: `${name}承暴秦之辙，能否以法术之密、守二世之短祚？`, v: '冷峻' },
    '汉': { p: `${name}处炎汉之世，值外戚宦官更迭之局，能否以权宜安宗庙、苏疲民？`, v: '华赡' },
    '三国': { p: `${name}鼎足之余、生于乱离，能否以强弱之势、存一方之祀？`, v: '质朴' },
    '晋': { p: `${name}处江左或中原之乱，能否于胡汉交侵中、存晋室一线之脉？`, v: '冷峻' },
    '宋': { p: `${name}守赵宋之局，值强邻压境、党争未息，能否以文治之醇、御边患之亟？`, v: '华赡' },
    '齐': { p: `${name}代宋而立、亦出武人，能否于篡弑相仍中、稍安江左之民？`, v: '质朴' },
    '梁': { p: `${name}继梁室之绪，处侯景余波，能否以文雅之政、补征伐之伤？`, v: '华赡' },
    '陈': { p: `${name}守江南残局，国小力弱，能否以孤忠、延陈祚最后一息？`, v: '质朴' },
    '北魏': { p: `${name}处拓跋之朝，值胡汉交融之痛，能否以政制之变、安代迁之怨？`, v: '冷峻' },
    '北齐': { p: `${name}承高氏之乱政，能否于淫暴之朝、保一身之节、苏民之困？`, v: '冷峻' },
    '北周': { p: `${name}处关陇之基，能否以府兵之制、为混一者铺路？`, v: '冷峻' },
    '西魏': { p: `${name}守关中孤弱，能否依宇文之规、抗东魏之强？`, v: '冷峻' },
    '东魏': { p: `${name}处高欢之挟，虚拥魏号，能否于权臣之下、存魏室之形？`, v: '冷峻' },
    '隋': { p: `${name}值隋室之末，能否于炀帝之弊、保一隅之安？`, v: '冷峻' },
    '唐': { p: `${name}处李唐之世，值藩镇宦官相蚀，能否以中枢之政、挽将坠之纲？`, v: '华赡' },
    '后梁': { p: `${name}处五代之初，能否以篡立之身、服中原之望？`, v: '质朴' },
    '后唐': { p: `${name}处沙陀之朝，能否以兵变得国、守创业之难？`, v: '质朴' },
    '后晋': { p: `${name}处儿皇帝之辱，能否于契丹之胁、保石晋之位？`, v: '冷峻' },
    '后汉': { p: `${name}处五代之促，能否于刘氏短祚、苏乱离之民？`, v: '质朴' },
    '后周': { p: `${name}处周世宗之余，能否以粗安之政、为混一铺路？`, v: '质朴' },
    '辽': { p: `${name}守契丹之业，能否于番汉之间、保两院之制、和宋以安？`, v: '质朴' },
    '金': { p: `${name}处女真之朝，值蒙宋交逼，能否以武备之实、存完颜之祚？`, v: '冷峻' },
    '西夏': { p: `${name}守党项之隅，能否于宋辽金之间、以小国周旋而不亡？`, v: '质朴' },
    '元': { p: `${name}处蒙元之末，能否于衅端四起、红巾鼎沸中、保大都之灯？`, v: '冷峻' },
    '明': { p: `${name}守朱明之局，值内阉外患之逼，能否以祖训之严、苏疲敝之政？`, v: '华赡' },
    '清': { p: `${name}承满洲之业，能否以入关之后、抚汉地之民、定鼎之局？`, v: '质朴' },
    '新': { p: `${name}以符命代汉，能否以托古之制、安海内之疑？`, v: '华赡' }
  };
  const t = tmpl[dyn] || { p: `${name}处其世、当其任，能否以一身之政、安宗庙、苏疲民？`, v: '华赡' };
  return { p: t.p, v: t.v };
}

// 朝代 -> 班底池（仅 Tier B 有精修表外的帝时备选；此处只对 Tier B 有代表性的配 1-2 人）
const CAST_POOL = {
  '汉': [{ id: 'han_chen', name: '朝中公卿', role: '辅政之臣', voiceTag: '华赡' }],
  '唐': [{ id: 'tang_chen', name: '宰执近臣', role: '中枢之臣', voiceTag: '华赡' }],
  '宋': [{ id: 'song_chen', name: '两制儒臣', role: '论政之臣', voiceTag: '华赡' }],
  '明': [{ id: 'ming_chen', name: '翰林阁臣', role: '票拟之臣', voiceTag: '华赡' }],
  '元': [{ id: 'yuan_chen', name: '怯薛权臣', role: '近侍之臣', voiceTag: '冷峻' }],
  '清': [{ id: 'qing_chen', name: '八旗谋臣', role: '佐命之臣', voiceTag: '质朴' }]
};

let stats = { total: 0, already: 0, refined: 0, templated: 0, skippedNoDyn: 0, castAdded: 0 };

files.forEach(file => {
  const fp = path.join(dataDir, file);
  const json = JSON.parse(fs.readFileSync(fp, 'utf8'));
  (json.emperors || []).forEach(e => {
    stats.total++;
    if (e.reignPremise) { stats.already++; return; } // 保留手写精修版
    const refined = ALL_SPINE[e.id];
    if (refined) {
      e.reignPremise = refined.reignPremise;
      e.voiceTag = refined.voiceTag;
      if (refined.cast) { e.cast = refined.cast; stats.castAdded++; }
      stats.refined++;
    } else {
      const t = dynastyTemplate(e.dynasty, e);
      e.reignPremise = t.p;
      e.voiceTag = t.v;
      // Tier B 配一个朝代典型班底（轻量），Tier C 不配
      if (e.tier === 'B' && CAST_POOL[e.dynasty]) {
        e.cast = CAST_POOL[e.dynasty];
        stats.castAdded++;
      }
      stats.templated++;
    }
  });
  fs.writeFileSync(fp, JSON.stringify(json, null, 2) + '\n', 'utf8');
});

console.log('=== P3 铺陈统计 ===');
console.log(JSON.stringify(stats, null, 2));
console.log('已铺 spine 总数预计:', stats.already + stats.refined + stats.templated, '(应=262)');
