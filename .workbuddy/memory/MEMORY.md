# 择决千秋 / Choice-of-History — 长期项目记忆

## 架构与构建管线（必读）
- **皇帝数据有两处来源，审计完整性时必须两处都查**（2026-08-07 教训：曾只查 JSON 漏掉 index.html 硬编码，误报汉/隋/唐/宋/元/明/清顶级帝「缺失」）：**
  1. `data/emperors/*.json` —— 乙类（5-8 事件），经 `build_data.js` 合并为 `data/emperors/coh_data.js`（`window.COH_BUILTIN_EMPERORS`）。
  2. `index.html` 硬编码「甲类」18 位详事件库（`E_QIN_SHIHUANG` 等，约 220 行起），含秦始皇/汉高祖/汉武帝/汉光武帝/隋文帝/隋炀帝/唐太宗/唐玄宗/宋太祖/宋徽宗/宋高宗/元世祖/明太祖/明成祖/明思宗/清康熙/清雍正/清乾隆。
- **运行时合并去重（`loadEmperorData`）：先注册硬编码甲类 → 再合并 `COH_BUILTIN_EMPERORS`，重复 id 跳过 JSON 版（硬编码优先）。** `dynIdByEmperor(e)` 把 `e.dynasty` 映射到 `DYNASTIES[].id`（如 周→zhou、秦→qin、三国→three、南北朝诸朝→nanbei、五代→wudai）。新皇帝加 JSON 时 `dynasty` 字段必须匹配该 map 的 key，否则注册不到朝代。
- JSON 真源当前：310 帝中国 + 177 帝外国 = **488 帝**（2026-08-07 史实审查后补入武则天 +1）。
- 游戏实际加载文件：`data/emperors/coh_data.js`（`window.COH_BUILTIN_EMPERORS`，全局变量暴露以便 file:// 双击打开）。
- **改了 `*.json` 必须重跑 `node tools/build_data.js` 重建 `coh_data.js`**，否则运行时看不到改动。
- 文案/配置也经 `coh_config.js`（有 `coh_config.sample.js` 样本）。

## 关键数据 Schema（避免踩坑）
- 事件 `branches[i]` 仅携带 `setFlags` / `clearFlags` / `nextEventId`。
- **派系关系由兄弟数组 `relationDeltas[i]` 驱动**（与 branches 下标对齐）。在 `branches` 里写 `relationDelta` 无效、被 `applyChoiceEffects` 忽略。
- `state.flags`：叙事布尔旗；`state.relations`：派系关系 −100~100，默认桶 宗室/士大夫/边将/商贾。
- `CANONICAL_FLAGS` 词表：unify, reform, long_peace, usurped, scholar_oppose, weak, war_win, war_loss, tax_cut, tax_heavy, scholar_purge, amnesty, flood, famine, rebellion。
- mid-crisis：`midCrisisAnchors:[{atProgress, event:{...}}]`；`computePressure = 0.35*bell + 0.4*healthFactor`，bell 在进度 0.5（中局大考）处峰值。

## 统一剧情（叙事软注入，保留 AI 随机性）
- 每月连贯性根因（已修复）：原 `PROMPTS.user()` 只喂近 5 月截断摘要，第 5 月前叙事对 AI 不可见（失忆）。2026-08-07 改为分级记忆（见下「AI 记忆」）：`buildMemoryContext()` 注入近事详情(全 reign 逐字)+前事压缩纪要+玩家重大抉择语义记忆。
- 解法：每位皇帝可选填 `reignPremise`(主线索)、`voiceTag`(音色)、`cast`(常驻班底)；`index.html` 经 `FLAG_OMEN`/`reignProgress`/`actNameOf`/`ACT_ATMOSPHERE`/`narrativeContextFor()` 把这些作为「引力源」软注入 AI 提示词。缺字段时返回空串，零回归。
- **已铺 spine 的皇帝：全 262 帝（P3 完成）**。3 帝手写精修（qing_taizu/tang_taizong/song_gaozong）+ 69 帝脚本注入精修（Tier A）+ 190 帝模板化（Tier B/C，按朝代生成主线索+音色）。114 帝配 cast 班底。注入脚本 `tools/_inject_spine.js`，备份 `data/emperors/_backup_20260807/`。
- 史官音色 pillars（P1 已落地，index.html）：`HISTORIAN_VOICE`（通用拟史官体·记指悬三段式）+ `VOICE_TAG_VARIANT`（质朴/华赡/冷峻）+ `historianVoiceFor(emp)` 注入 `PROMPTS.system` 的【本朝叙事主线索】；`historianComment` 提示词强化为记指悬（仍 AI 生成，保留随机性）；`historianPrologueFor(emp)` 登基定场白注入 `selectEmperor`→`#intro-verdict`；`historianEpilogueFor(emp,ending)` 结局判词追加 `endGame`→`#end-review`（white-space:pre-line）。无 reignPremise 时全部跳过，零回归。

## 工作流偏好（陛下定）
- 评估(assess)→规划(plan)→冲突检查(conflict-check)→实施(implement)；流程被打断时从中断处继续。
- 结论需基于源码验证，输出结构化 Markdown，建议可执行且勿引入过重代码负担。
- 陛下自称「陛下」；偏好轻松俏皮的互动风格。

## AI 记忆（分级记忆 · 2026-08-07）
- 纯前端无后端；借鉴 Mem0(提取-压缩)/Letta(三级记忆)/claude-mem(Reflector)/OpenViking(分层按需) 理念，做浏览器内落地。
- `state.memory={v:1,chronicle:"",decisions:[]}`；`recordHistory` 现额外存 `outcomeDescription`(全文后果)/`historianComment`(史官评)/`setFlags`，并触发 `updateMemory()`→抽取语义抉择(CANONICAL_FLAGS去重)+`rebuildChronicle()`(滚出窗口事件压标题行)。
- `buildMemoryContext(st)`：注入【近事详情】+【前事纪要·压缩】+【玩家重大抉择】；有界 `MEM_BUDGET`。
- 常量：`MEM_RECENT_BUDGET=500`(逐字月数≈40年)、`MEM_BUDGET=160000`(字硬上限)、`MEM_CHRONICLE_CAP=8000`。按 300k 上下文设计。
- `pregenerateMonths` 现注入 `narrativeContextFor`+`buildMemoryContext`，未来月锚定主线索/派系。
- 旧档兼容：`doLoad` 缺 `memory` 时 `defaultChronicle(history)` 兜底生成。零额外 API 调用。

## 终评与科技树（2026-08-07 约定）
- **后世史官总评（`buildHistorianFinalReview`，index.html）刻意排除「科技」属性**：科技是科技树加点资源、数值通常偏低，列入会误导「最弱项」判定。终评所陈五维 = `REVIEW_DIMS=["treasury","people","military","court","health"]`，用在 govAvg、「综其五事」列举、最长/最短排名；科技仅在「越代科技」段落（具体科技）专述。改此函数若再加维度，须同步改 REVIEW_DIMS 与 `_rank[_rank.length-1]` 索引。
- **科技节点一句话作用（`functionDesc`）**：每个科技树节点新增 `functionDesc` 字段（一句中文功能介绍）。映射表 `SPECIAL_DESC` 在 `tools/gen_techtree.py`（81 个 special 键 = 9 分支×9 轨道，与各分支 `specials` 列表对应），`build_tree()` 输出 `functionDesc`。已用 `tools/add_tech_functiondesc.py` 给现有 `data/tech_tree.json` 全量补完（1134 节点），并重跑 `node tools/build_techdata.js` 重建 `data/tech_data.js`。改映射后跑这两个脚本即可刷新。UI 展示：游戏内 `renderTechTree` 卡片加 `.tn-func` 行；`data/tech_tree_ui.html` 卡片加 `.fn` 行。
- **按文明改名层（2026-08-07 落地）**：科技树显示名按文明解析，外国首领看到非中文名、中国首领零回归。
  - 覆盖清单 `data/tech_names_overlay.json`：三级（branches/tracks/nodes），值可为字符串或 `{foreign, rome}`；生成期展开 `foreign→{us,uk,ru}`、`rome→{rome}`；**cn 永不覆盖**，保留 tree 原中文名。节点级键用 `branch_age_track` id（如 `civ_05_01`）。
  - 生成：`gen_techtree.py` 给每个节点烤入 `names`{foreign,rome}/`civBranch`{foreign,rome}/`trackNames`{foreign,rome}，`main()` 给 `meta.branches[i]` 加 `civBranch`。改完覆盖 JSON 须重跑 `gen_techtree.py` + `build_techdata.js`。
  - 解析：`tech_engine.js` 的 `compute()` 经 `_civName/_civBranchName/_civTrackName`（civ = `emperor.civilization`，缺省 "cn"）；`index.html` 经 `tnName/tnBranch/tnTrack/techCiv` 渲染分支标签/节点名/轨道名/研究提示。
  - 外国 period 时代映射与标志科技：13 个外国 period 在 `gen_techtree.py` 与 `tech_engine.js` 的 `DYNASTY_ERA` 同步（如「开国立宪」=8、「王政」=3），`SIGNATURE` 各加时代名片坐标 → 外国首领拿到非空初始科技树、越代机制正常。
  - 改名原则（用户确认）：结构+标志科技优先；真正跨文明通用的节点（水利/冶金/历法/医养等）保留共享名，不强行替换。

## 史实基准（2026-08-07 全量审查后确立，改数据前必读）
- 报告：`docs/史实审查与修正报告.md`；修正前全量备份：`data/emperors/_backup_audit_20260807/`。
- **审查工具箱**（`tools/`，只读可复现）：`audit_extract.py` / `audit_reign_ref.py` / `audit_overlap.py` / `audit_cn_evyear.py` / **`audit_nianhao.py`（年号↔公元交叉校验，挖硬伤最有效）** / `audit_anachronism.py` / `audit_foreign*.py` / `audit_diff_summary.py`。改完数据跑一遍即可回归。
- **已知非错误，勿再"修"**：① 30 处即位前事件（叙事前置，刻意）；② 复辟型君主在位重叠；③ 6 处事件晚于在位终年——晋恭帝/梁敬帝/北齐废帝/北周宣帝/隋恭帝/北魏献文帝，皆禅位或被废后遇害，史实正确；④ `*_fb` 余波事件 `historicalChoice=-1` 是设计约定；⑤ 夏商纪年本就示意性；⑥ 甲类 18 帝在位年全部核对无误。
- **`tools/gen_foreign.py` 已根治同步（2026-08-07 收尾）**：分层模板池 `LAYERS` + 年份钳制 `_clamp_year` + outcome 派生 `derive_outcome` + 精修覆盖 `EVENT_OVERRIDES` + 回归自检 `selfcheck/postprocess` 已全部回灌进生成器，重跑不再冲掉产物层修正（自检全绿、与修正后产物对比零倒退）。可作为外国篇重生成的唯一可信来源。
- 事件按 `year` 字段匹配触发（`pickGatedMajor` 中 `ev.year <= state.year`），**不是按数组顺序**，故重排事件安全。
- **`historicalOutcome` 已在 UI 接上（2026-08-07 收尾）**：数据层 91.2% 的 JSON 事件(2638/2891)带非空 `historicalOutcome`；`index.html` 终局复盘 `end-decisions` 新增「史册所载 · <historicalOutcome>」对照行（`recordHistory` 捕获 → `buildHistoricalEvent`/`renderPreset` 接 `currentEvent` → 渲染处 `ho ? ... : ""` 守卫，空字段整行不渲染，零回归）。
