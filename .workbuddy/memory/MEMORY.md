# 择决千秋 / Choice-of-History — 长期项目记忆

## 架构与构建管线（必读）
- 源码真源：`data/emperors/*.json`（262 帝 / 1866 事件）。
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
- 每月散、缺连贯的根因：`index.html` 的 `PROMPTS.user()` 只喂 5 月标题+六维+anchors+relations，从不回灌 spine/幕/激活 flags/常驻班底。
- 解法：每位皇帝可选填 `reignPremise`(主线索)、`voiceTag`(音色)、`cast`(常驻班底)；`index.html` 经 `FLAG_OMEN`/`reignProgress`/`actNameOf`/`ACT_ATMOSPHERE`/`narrativeContextFor()` 把这些作为「引力源」软注入 AI 提示词。缺字段时返回空串，零回归。
- 已铺 spine/cast 的皇帝：qing_taizu(努尔哈赤)、tang_taizong(唐太宗)、song_gaozong(宋高宗)。其余待扩展。

## 工作流偏好（陛下定）
- 评估(assess)→规划(plan)→冲突检查(conflict-check)→实施(implement)；流程被打断时从中断处继续。
- 结论需基于源码验证，输出结构化 Markdown，建议可执行且勿引入过重代码负担。
- 陛下自称「陛下」；偏好轻松俏皮的互动风格。
