# 择决千秋 / Choice-of-History — 长期项目记忆

## 架构与构建管线（必读）
- 皇帝数据两来源，审计须两处都查：① data/emperors/*.json（build_data.js → coh_data.js 的 window.COH_BUILTIN_EMPERORS）；② index.html 硬编码「甲类」18 帝详事件库。运行时先注册硬编码→再合并 JSON，重复 id 跳 JSON。
- JSON 真源：310 中国 + 177 外国 = 488 帝。改 json 须重跑 `node tools/build_data.js`。
- `dynIdByEmperor(e)` 把 `e.dynasty` 映射 `DYNASTIES[].id`；新帝 `dynasty` 须匹配该 map key。

## 关键 Schema
- 事件 `branches[i]` 仅带 `setFlags`/`clearFlags`/`nextEventId`；派系关系由兄弟数组 `relationDeltas[i]` 驱动（与 branches 下标对齐），在 branches 写 `relationDelta` 无效。
- `state.flags`=叙事布尔旗；`state.relations`=派系 −100~100（宗室/士大夫/边将/商贾）。
- `CANONICAL_FLAGS`：unify,reform,long_peace,usurped,scholar_oppose,weak,war_win,war_loss,tax_cut,tax_heavy,scholar_purge,amnesty,flood,famine,rebellion。
- 终评 `buildHistorianFinalReview` 排除「科技」维度；五维 `REVIEW_DIMS=["treasury","people","military","court","health"]`。

## 科技树
- 数据流：`tools/gen_techtree.py`（81 specials=9分支×9轨道）→ `data/tech_tree.json`（1134 节点，结构 `{schemaVersion,meta,nodes[]}`）→ `data/tech_data.js`（`node tools/build_techdata.js`）→ `window.TECH_TREE`。
- 引擎 `tools/tech_engine.js`：`TechEngine.compute(emperor, ownedTechs)`→`techProfile`（specials/perBranch/eraLevel）。
- 节点 id=`{branch}_{age:02d}_{trackIdx:02d}`；命名真源=gen_techtree.py 分支矩阵，改名须矩阵+json 双修再 `build_techdata.js`。
- `functionDesc`（一句话作用）由 `SPECIAL_DESC` 映射 + `tools/add_tech_functiondesc.py` 补；按文明改名层 `data/tech_names_overlay.json`（cn 永不覆盖）。
- 科技「具体作用」层（属性外）：`tools/add_tech_effects.py` 按 81 special 注入 `effect`+`effectDesc`（跑完须 `build_techdata.js`）。**7 通道** passive/shield/eventLess/warEdge/relation/costLess/unlock（**score 终评通道已于 2026-08-08 移除**——陛下要求科技只影响当代，终评不再含科技加成）；**粒度=(special,age)**：每轨道 14 段短码演进序列（脚本内 `EFFECTS[special]` 为 14 空格分隔短码串，短码→`SHORTCODE` 映射；复合用 '+' 如 `T+Sm`），按 (age-1) 取段，**强制相邻 age 效果类型不同**（彻底差异化；旧版「分带」让同带相邻 age 雷同，如曲辕犁age5==占城稻age6 曾完全同效，2026-08-08 末轮已修）。量级=`perTier×时代档(age≤3→1/≤7→2/≥8→3)×等级`，逐 special 有 cap。
- index.html `computeTechEffects`(≈4063) 聚合 + 钩子落地；封顶常量 `PASSIVE_YEAR_CAP=3`/`REL_TOTAL_CAP=25`（≈4040；**SCORE_TOTAL_CAP 已删**），改引擎须同步 `tools/_sim_tech_effects.js` 顶部常量。
- ⚠️ 坑：`initTechAtStart` 把朝代预设灌进 `state.ownedTechs`（清最多 543 项）→ 读 ownedTechs 的「玩家回报」类机制会开局即封顶。玩家自研增量在 `state.playerTechs`；`computeTechEffects` 只计 playerTechs。
- `warWinChance()` 是战争胜算**唯一真源**：`edgeBreadth=min(0.15, wlvl*0.01)`（时代底子）+ `edgeElite=min(0.20, warEdgeWinBonus()/100)`（自研尖端）。`paintWarStatus` 与科技树战争行都须调它。

## 史实基准（改数据前必读）
- 报告 `docs/史实审查与修正报告.md`；备份 `data/emperors/_backup_audit_20260807/`。审查工具 `tools/audit_*.py`，改完跑回归。
- 已知非错误：即位前事件/复辟重叠/被废遇害晚于终年/`*_fb` 余波 `historicalChoice=-1`/夏商纪年示意性。
- 外国篇重生成唯一源 `tools/gen_foreign.py`；`historicalOutcome` 已接 UI `end-decisions`。

## Git/沙箱（排查必读）
- 沙箱删空目录→`.git/refs/heads` 与 `.git/refs/remotes/origin` 被删使 git 报 not a repo。`mkdir -p` 复活+写 `packed-refs`；git 加 `-c gc.auto=0 -c gc.autodetach=0`。
- 勿用 `git stash`（曾触发对象库损坏）；勿依赖 `git pull`（本地与 origin 无公共祖先）。
- GitHub push 仍 blocked（401 无凭据）。
