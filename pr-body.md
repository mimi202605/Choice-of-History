## 概述

本次合并升级了 GitHub Pages 部署工作流的 Actions 版本与 Node 版本，并在游戏核心脚本 `index.html` 中引入三大新机制：**退位/复辟** 旗标系统、**长期记忆注入**（人物存亡）、**越代科技减免**系统，并新增 **时间一致性约束** 防止 AI 叙事出现年代错乱。

## 主要变更

### 工作流升级（.github/workflows/pages.yml）
- actions/checkout: v4 → v6
- actions/setup-node: v4 → v6，Node 版本 20 → 24
- actions/configure-pages: v5 → v6
- actions/upload-pages-artifact: v3 → v4
- actions/deploy-pages: v4 → v5

### 游戏机制（index.html）

**1. 退位/复辟机制**
- FLAG_OMEN 新增 `abdicated`（退位）与 `restored`（复辟）两个 omen 文案
- CANONICAL_FLAGS 词表新增 `abdicated` / `restored`
- 在 `applyChoiceEffects` 与 `applyOutcome` 中加入二者的互斥逻辑

**2. 长期记忆系统（longTermMemory）**
- 向 AI 系统提示注入：退位/复辟状态、人物已故（`*_died`）、人物假死（`*_fakedeath`）等关键记忆
- 在 `applyOutcome` 中允许 `*_died` / `*_fakedeath` 标记绕过规范词表校验

**3. 越代科技减免系统（techMitigate）**
- 根据玩家拥有的越代科技等级，按概率减轻六维属性惩罚
- 自动生成科技减免叙事，并入结果描述
- 新增 `.outcome .mitigate-tech` 样式以视觉区分
- 重构 `renderOutcome` 将减免叙事以独立 span 包裹

**4. 时间一致性约束**
- 在事件生成、后果生成、批量预生成提示中均要求 AI 严格使用与当前时位一致的时间（年号、年份、月份）

**5. setFlags 词表同步**
- 在事件生成、预生成、后果生成提示中均同步更新规范词表为 `unify/reform/long_peace/usurped/scholar_oppose/weak/war_win/war_loss/tax_cut/tax_heavy/scholar_purge/amnesty/flood/famine/rebellion/abdicated/restored`

## 影响
- 提升部署稳定性与性能（Node 24 + Actions v6）
- 增强 AI 叙事的**历史一致性**（时间、人物存亡、政权延续）
- 给予玩家**科技投资**可见的负面后果缓解反馈
- 为后续「中兴/复辟」类剧本线提供机制基础
