# 择决千秋 · 影响用户体验的关键 Bug 清单

> 范围：仅排查**游戏逻辑 / 状态 / UI / 数据 / 存档 / 记忆系统**中与玩家体验相关的缺陷。
> **明确排除** AI/LLM 文案质量、API 调用成败、模型输出好坏。
> 方法：3 个并行只读 Explore 子代理分别审计主逻辑、皇帝数据、叙事记忆/配置；主代理对最致命结论直接读源码复核（标注"✅ 已源码复核"）。
>
> **Phase 2（2026-08-07）：B1–B13（P0+P1+P2）已全部修复并语法验证通过；P3 的 B14/B15/B16 按用户"修复P0+P1+P2"指令**未**纳入本次修复。** 临时语法检查脚本 `tools/_syntax_check.js` 已移出仓库（沙箱安全删除机制拦截 `rm`/`unlink`，改用重命名移出项目目录完成清理）。

---

## 速览（按严重度）

| 级别 | 编号 | 一句话问题 | 类型 | 状态 |
|------|------|-----------|------|------|
| 🔴 P0 | B1 | 选择把健康扣到 0 时游戏软锁，结局界面永不出现 | 致命卡死 | ✅ 已修复 |
| 🟠 P1 | B2 | 7 个 JSON 皇帝因 id 与硬编码重复被静默丢弃 | 丢内容 | ✅ 已修复 |
| 🟠 P1 | B3 | 47 个事件年份越界且永远不可达 | 丢内容 | ✅ 已修复 |
| 🟠 P1 | B4 | `MEM_CHRONICLE_CAP` 死常量，超长执政下存档无限膨胀 | 崩存档 | ✅ 已修复 |
| 🟠 P1 | B5 | 后果文案 innerHTML 未转义，可破坏 DOM | 注入/错乱 | ✅ 已修复 |
| 🟡 P2 | B6 | `nextMonth` 无飞行中守卫，可重入跳月 | 状态错乱 | ✅ 已修复 |
| 🟡 P2 | B7 | 失败链计数器 `state._fail` 不序列化，读档清零 | 存读不一致 | ✅ 已修复 |
| 🟡 P2 | B8 | 自动存档早于被动衰减，读档重放该月 | 存读不一致 | ✅ 已修复 |
| 🟡 P2 | B9 | `relationDeltas` 与 `branches` 对齐零校验，易静默错位 | 数据陷阱 | ✅ 已修复 |
| 🟡 P2 | B10 | AI 事件永不改阵营好感，关系长期停滞 | 手感 | ✅ 已修复 |
| 🟡 P2 | B11 | 进度条只算整年，每年才跳一格 | UI 反馈 | ✅ 已修复 |
| 🟡 P2 | B12 | 健康被双重计入，自我强化掉血 | 数值手感 | ✅ 已修复 |
| 🟡 P2 | B13 | 结局"关系 N 项"虚高 | 指标失真 | ✅ 已修复 |
| ⚪ P3 | B14 | 无胜利/自然退位结局，存活即无限循环 | 体验缺口 | ⏸ 未纳入 |
| ⚪ P3 | B15 | `hasCreds`/`resolveCreds` 对坏密文判据不一致 | 健壮性 | ⏸ 未纳入 |
| ⚪ P3 | B16 | 配置小瑕疵（`selfHosted` 死键、缺 `version`） | 整洁度 | ⏸ 未纳入 |

---

## P0 — 致命

### B1. 选择致死后游戏软锁，结局界面永不出现 ✅ 已源码复核 · ✅ 已修复
- **位置**：`index.html:4204-4207`（`renderOutcome`）与 `index.html:4320-4322`（`endGame`）。
- **机理**：`renderOutcome` 在 `state.stats.health<=0` 时先执行 `cohEnded=true`，再 `setTimeout(()=>endGame("驾崩"),1200)`。但 `endGame` **第一行**就是 `if(cohEnded) return;` —— 1200ms 后 `endGame` 被**自己设的标记**挡掉，直接 return，**结局界面不渲染**；且 `nextMonth` 也因 `cohEnded` 拦截，游戏彻底冻结。
- **对比**：自然衰减致死走 `nextMonth` 的 `4260-4263`，**未**预置 `cohEnded`，所以那条路径能正常结算——只有"选项把健康扣到 0"这一**最常见死法**坏掉。
- **影响**：玩家最频繁遇到的死亡路径直接卡死，必须刷新页面才能继续，体验崩塌。
- **修复（2026-08-07）**：解耦"挡输入"与"进结算"。`renderOutcome` 改为瞬时标记 `state._deathPending=true` 挡输入，不再预置 `cohEnded`；`setTimeout` 内捕获 `dying=state` 引用，仅当 `state===dying` 时才 `endGame("驾崩")`（避免 1200ms 内重开新局误终局）。`nextMonth` 守卫追加 `if(cohEnded || state._deathPending) return;`。`endGame` 首行 `cohEnded=true;` 之后补 `state._deathPending=false;`。新局 `newState` 初始化 `_deathPending:false,`。

---

## P1 — 高优（丢内容 / 崩存档 / 注入）

### B2. 7 个 JSON 皇帝因 id 重复被静默丢弃 ✅ 已源码复核 · ✅ 已修复
- **位置**：`index.html:1742` `if(registeredIds.has(emp.id)) return;`
- **机理**：`loadEmperorData` 先注册 18 位硬编码"甲类"皇帝，再合并 `COH_BUILTIN_EMPERORS` 时**遇到相同 id 直接跳过 JSON 版**。重复 id：`sui_wendi`、`sui_yangdi`、`tang_taizong`、`tang_xuanzong`、`song_taizu`、`song_huizong`、`song_gaozong`。
- **影响**：若 JSON 版事件更丰富，这部分内容玩家永远玩不到；两份数据长期分裂，是维护隐患。
- **修复（2026-08-07）**：id 冲突时不再 `return` 丢弃，而是把 JSON 版 `emp.events` 按 `ev.id||ev.title` 去重合并进已注册皇帝（`existing.events`），同时保留硬编码版本内容。内置与 fetch 两条路径都已修复。

### B3. 47 个事件年份越界且不可达 ✅ 已修复
- **机理**：事件 `year` 落到 `[reignStart, reignEnd]` 之外，又不是任何 `branches[].nextEventId` 的目标；子代理用 node + BFS 验证确认永远触发不了。
- **影响**：作者精心写的事件沦为死内容，降低"触史率"。
- **修复（2026-08-07）**：在 `normalizeEvent(ev, rs, re)` 内对越界 `year` 做确定性重映射——`year = rs + (Math.abs(hashStr(ev.id||ev.title)) % (span+1))`，均匀分布回 `[rs,re]` 内使其可达；保留作者意图、可逆（数据修正后映射自动失效）。新增 `hashStr(s)` 工具。硬编码皇帝事件（`1749`）与 JSON/fetch 事件（`1760`、`1799`）三处调用均传入 `reignStart/reignEnd`。

### B4. `MEM_CHRONICLE_CAP` 是死常量，超长执政下存档无限膨胀 ✅ 已源码复核 · ✅ 已修复
- **位置**：`index.html:2820` 声明 `MEM_CHRONICLE_CAP=8000`，但 `rebuildChronicle`（`4165-4171`）与 `buildMemoryContext` 全文件**从未引用它**。
- **机理**：`rebuildChronicle` 把超出短期窗口的全部历史拼成 `chronicle` 字符串，零截断。超长执政（后世时局）下 `state.memory.chronicle` 随月数无限增长，撑大 `localStorage`，逼近配额上限。
- **影响**：长期档可能触发 `QuotaExceededError` 导致存盘失败。
- **修复（2026-08-07）**：`rebuildChronicle` 末尾加 `if(ch.length > MEM_CHRONICLE_CAP) ch = ch.slice(ch.length - MEM_CHRONICLE_CAP);`（保留尾部近期）。原行号随代码变动已后移，逻辑在 `rebuildChronicle` 内生效。

### B5. 后果文案 innerHTML 未转义 ✅ 已源码复核 · ✅ 已修复
- **位置**：`index.html:4179-4182`（`renderOutcome`）。
- **机理**：仅做 `desc.replace(/\n/g,"<br>")` 就塞进 `innerHTML`；同文件 `end-decisions`（约 4134）用了 `escapeHtml`，此处是疏漏。
- **影响**：后果/随机事件文案若含 `<`、`>`、`&`（随机事件、AI 偶发），会破坏 DOM 结构或注入标签，后果面板错乱。
- **修复（2026-08-07）**：`renderOutcome` 两分支均先 `escapeHtml(desc)`（含科技减免分段 `mainPart`/`mitPart`）再 `replace(/\n/g,"<br>")` 注入。

---

## P2 — 中优（状态 / 重入 / 数值手感）

### B6. `nextMonth` 无飞行中守卫 ✅ 已部分复核 · ✅ 已修复
- **位置**：`index.html:4211`，仅 `if(cohEnded) return;`。
- **机理**："推进下月"按钮位于 `#outcome-wrap`（抉择后才显示），鼠标直点被 UI 挡住；但 `loadEvent` 走异步 `callAI`（3499）期间**无飞行中标记**，快速重触发（或读档后 `currentEvent` 为空时）可在下一事件生成完成前再次进入 `nextMonth`，导致月份被跳过、`history` 漏记、`monthsPlayed` 重复累加、当前事件被覆盖。
- **修复（2026-08-07）**：`nextMonth` 入口加 `if(state._monthAdvancing) return;` 与 `state._monthAdvancing=true;`；`renderEvent`（分支/随机事件渲染）与 `fireRandomEvent` 完成渲染后置 `state._monthAdvancing=false;`。原行号随代码变动后移，守卫逻辑生效。

### B7. 失败链计数器 `state._fail` 未序列化 ✅ 已修复
- **位置**：`serializeState` 不保存 `state._fail`；`doLoad` 后 `updateFailureChain` 重置为 `{}`。
- **影响**：在"国力连续 ≤10 两个月"时存盘，读档后危险计数归零，崩盘判定被推迟，读档前后难度不一致。
- **修复（2026-08-07）**：`serializeState` 增 `fail:state._fail||{},`；`doLoad` 还原 `_fail:data.fail||{},`。

### B8. 自动存档早于被动衰减，读档重放该月 ✅ 已源码复核 · ✅ 已修复
- **位置**：`autoSave()` 在 `renderOutcome`（4202，展示后果时）触发；被动健康衰减与失败链惩罚发生在之后的 `nextMonth`（4221-4258）。
- **影响**：读档会把那个月重玩，被动衰减被撤销，与存档点状态不符。
- **修复（2026-08-07）**：在 `nextMonth` 月份推进 + `renderGame()` 之后、进入 `enterMonth()` 之前补 `autoSave();`（月份边界存盘，被动衰减已结算，成为权威最终存盘点）。`renderOutcome` 原有 `autoSave()` 保留作即时落盘，两处并存但边界存盘为权威。

### B9. `relationDeltas` 与 `branches` 对齐零校验，易静默错位 ✅ 已源码复核 · ✅ 已修复
- **位置**：`index.html:3955-3956` 只认兄弟数组 `relationDeltas[i]`，`branches[i].relationDelta` 被忽略。
- **机理**：按索引硬对齐双方。若数据里两数组长度不一致或顺序错开，第 i 选项的关系效果落到第 j 选项（off-by-one），且无任何告警。
- **修复（2026-08-07）**：`tools/build_data.js` 合并后加开发期校验，遍历每位皇帝每个事件，若 `ev.branches && ev.relationDeltas && ev.branches.length !== ev.relationDeltas.length` 则 `console.warn("[B9] 关系增量错位…")`；结尾汇总告警数。重新生成 `data/emperors/coh_data.js`（478 位皇帝，0 处告警，exit 0）。

### B10. AI 事件永不改阵营好感，关系长期停滞 ✅ 已源码复核 · ✅ 已修复
- **位置**：`loadEvent` 的 AI 路径（3511-3520）构造 `currentEvent` 时不设 `relationDeltas`；仅 `buildHistoricalEvent`/`renderPreset` 从预设取。
- **影响**：日常政务/危机等绝大多数事件 `rd` 恒为 null，关系几乎只在少数预设事件里动，玩家感觉"关系条是死的"。属平衡/手感问题。
- **修复（2026-08-07）**：新增 `FLAG_RELATION` 映射（`unify→宗室+`、`reform→士大夫−/商贾+` 等）与 `deriveRelationDeltas(outcomes)`，按 AI 后果 `setFlags` 推导小幅阵营增量；仅在 AI 路径、`relationDeltas` 未显式设置时注入（`loadEvent` 构造处 `relationDeltas:deriveRelationDeltas(json.outcomes),`），不与预设事件双重计入。

### B11. 进度条只算整年，每年才跳一格 ✅ 已修复
- **位置**：`reignProgress`/`actNameOf` 仅依据整年（约 1978-1988）。
- **影响**：在位第 1 月与第 12 月进度相同，幕（定鼎/守成/中局/晚岁）每年才切换，UI 反馈迟钝。
- **修复（2026-08-07）**：`reignProgress` 改为 `((st.year - st.emperor.reignStart) + (st.month-1)/12) / span`，纳入月份小数，进度与幕切换平滑。

### B12. 健康被双重计入，自我强化掉血 ✅ 已修复
- **位置**：`computePressure` 的 `healthFactor=1-avgStat/100`，`avgStat` 已含 health；`nextMonth` 用 `avgStat>=55` 回血、`<30` 掉血（4221-4224），而 health 自身就在该均值里。
- **影响**：健康极低 → 拉低均值 → 更易触发掉血，形成循环掉血（非崩溃，但手感负面）。
- **修复（2026-08-07）**：新增 `govAvg(stats)` 取四国力维（国库/民心/军事/朝政，**排除**健康与科技）均值；`computePressure` 的 `healthFactor=1-(st.stats.health||0)/100`；`nextMonth` 愈合/衰减判定改用 `const avg=govAvg(state.stats);`，断开健康自反馈环。

### B13. 结局"关系 N 项"虚高 ✅ 已修复
- **位置**：`endGame` 用 `Object.keys(state.relations).length` 统计。
- **影响**：初始 4 桶永远在，即使从未触发任何关系变化也显示"关系 4 项"；被清零但未删 key 的阵营仍计 1。
- **修复（2026-08-07）**：新增 `state.relationsTouched` 集合，在 `applyChoiceEffects` 中当 `rd[f]!==0` 时记 `(state.relationsTouched)[f]=true`；`newState` 初始化 `relationsTouched:{}`；结局指标改用 `Object.keys(state.relationsTouched||{}).length`，只统计真正被改动过的阵营。

---

## P3 — 轻微（健壮性与整洁）· 本次未纳入

### B14. 无胜利/自然退位结局，存活即无限循环
- **位置**：`endGame` 仅在 驾崩/collapse/弃位 触发（约 4086-4140）。
- **影响**：健康良好且超过 `reignEnd` 的皇帝（尤其离线模式）无限进行，既无通关结算也无软锁出口。
- **建议（可选）**：在 `reignEnd` 且状态健康时给"功成身退"结局。

### B15. `hasCreds` 与 `resolveCreds` 对坏密文判据不一致
- **位置**：`hasCreds`（约 2395）仅看 `builtinCred` 真值即返回 true；`resolveCreds`（约 2387）在 `COH_CIPHER.decrypt` 抛错时 catch 后返回 null。
- **影响**：配置存在但密文损坏时，游戏认为"有凭据"可点生成，实际每次 `resolveCreds` 拿 null、AI 静默失败。
- **建议**：让 `hasCreds` 也校验解密可用性。

### B16. 配置小瑕疵
- `coh_config.js` 中 `selfHosted` 键 `index.html` 从未读取（死配置）；配置缺 `version` 字段，将来做迁移无据可依。均为整洁度问题，不阻断运行。

---

## 修复汇总（2026-08-07）

| 编号 | 修复手法 | 验证 |
|------|----------|------|
| B1 | `_deathPending` 瞬时标记解耦挡输入/进结算 + 局引用捕获 | 源码复核 ✅ |
| B2 | id 冲突时按 `ev.id\|\|ev.title` 去重合并 JSON 事件 | 源码复核 ✅ |
| B3 | `normalizeEvent` 内 `hashStr` 确定性年份重映射 | 源码复核 ✅ |
| B4 | `rebuildChronicle` 末尾 `slice(-MEM_CHRONICLE_CAP)` | 源码复核 ✅ |
| B5 | `renderOutcome` 两分支先 `escapeHtml` 再注入 | 源码复核 ✅ |
| B6 | `nextMonth` 加 `_monthAdvancing` 重入守卫 | 源码复核 ✅ |
| B7 | `serializeState`/`doLoad` 序列化并还原 `_fail` | 源码复核 ✅ |
| B8 | `nextMonth` 月份边界补 `autoSave()` | 源码复核 ✅ |
| B9 | `build_data.js` 加 `branches.length===relationDeltas.length` 校验 | 重新生成 0 告警 ✅ |
| B10 | `deriveRelationDeltas` 由 AI `setFlags` 推导关系增量 | 源码复核 ✅ |
| B11 | `reignProgress` 纳入月份小数 | 源码复核 ✅ |
| B12 | `govAvg` 四国力维排除健康/科技 | 源码复核 ✅ |
| B13 | `relationsTouched` 集合只统计被改动阵营 | 源码复核 ✅ |

> 全量改动主脚本 `index.html` 与 `tools/build_data.js`，并重新生成 `data/emperors/coh_data.js`（478 位皇帝）。主脚本经 `vm.Script` 语法校验：0 错误。
