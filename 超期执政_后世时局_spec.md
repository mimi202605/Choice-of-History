# 超期执政 → 后世时局事件池：事件 `binding` 标注规范 + resolver 函数签名草案

> 状态：**纯 spec，未实现**。本文只定义字段语义、函数签名、集成点、playtest 失败信号与假设。
> 落地实现见后续 build 轮次，不在本文件范围。
> 代码引用基于 `index.html`（核实于 2026-08-07）：`EMPEROR_REGISTRY` L1653、`normalizeEvent` L1656、`E()` L1228、`dynIdByEmperor` L1749、`gateOK` L2984、超期健康处理 L3955、`currentEvent.source` L2275。

---

## 1. 目标与范围

玩家操控的皇帝在位时长超过历史真实 `reignEnd` 后，应能从「对应时间的历史后继皇帝」事件库中借取事件，但**只取合理事件**。

- **已具备的钩子**：`index.html:3955` `if(state.year > state.emperor.reignEnd)` 已经识别超期，目前仅做健康温和递减。本方案复用该信号，不新增"是否超期"判定。
- **不解决**：跨朝代借事件（断代风险）、AI 重写文本的细节、具体数值 tuning。这些单列专项。

**Fun hypothesis**：超期执政的核心乐趣 = 体验「若这位皇帝不死，天下接下来会撞上什么」，用自己积累的派系/国力资本去扛结构性危机。张力来自"我仍是我，但时局已入后朝"。

**Design pillars（不可妥协）**：
1. Plausibility over completeness —— 借来的事件必须过"这事可能发生在当前的我身上吗"测试。
2. Continuity —— 借来的事件必须尊重当前 `state` 的 flags/relations/stats（复用 `gateOK`）。
3. No identity break —— 借来的事件不能指名后继帝、不能暗示玩家换人。

---

## 2. 事件 `binding` 标注规范

### 2.1 字段定义

在事件对象上新增 `binding` 字段。该字段在 `normalizeEvent`（L1656）中读取，透明向下游传递。

| 取值 | 含义 | 是否被超期池借用 | 作者要求 |
|------|------|------------------|----------|
| `"personal"` | 绑定该帝身份：登基/禅位/特定人物生死/专属丑闻（如花石纲、武后称制） | **否** | 默认排除 |
| `"structural"` | 条件驱动的结构性危机：饥荒、水患、边患、党争、继承纠纷、财政破产 | **是**（需 `gateOK` 通过） | 必须用中性第二人称（"陛下"），**不得硬编码皇帝名**，以便跨帝 re-voice |
| `"era"` | 朝代级主题：中兴、衰世、夷狄入寇等可泛化到同朝任意帝的事件 | **是**（需同朝代 + `gateOK`） | 同上，中性表述 |

### 2.2 默认策略（fail-closed 刹车）

- `binding` **缺省时视为 `"personal"`**（排除）。这是防通胀炸弹的硬刹车：未标注的事件一律不借，绝不乐观默认。
- 理由：裸借未审事件会产出"唐太宗撞上宋徽宗花石纲"式荒诞。标注是真实作者成本，不可省。

### 2.3 两处来源的一致处理

- **硬编码甲类（用 `E()` 构造，L1228）**：给 `E()` 增加第 9 个可选参数 `binding`，默认 `"personal"`，向后兼容现有 8 参调用。
  - 签名草案：`function E(year,month,title,description,choices,historicalChoice,historicalOutcome,id,binding)`
  - 返回对象加 `binding: binding || "personal"`。
- **JSON 乙类（`normalizeEvent` 处理，L1656）**：`normalizeEvent` 增加 `binding: ev.binding || "personal"`。JSON 事件直接写 `"binding":"structural"` 即可。
- 两处经 `normalizeEvent` 归一后字段一致，下游无分支。

### 2.4 re-voice 约束（关键，避免 identity break）

`binding:"structural"` / `"era"` 的事件**必须**满足：
- `description` 与 `choices` 文本使用中性第二人称（"陛下""朝廷""边将"），**不得出现具体皇帝庙号/姓名**。
- 凡文本里出现具体皇帝名的事件，即使讲的是饥荒，也只能标 `"personal"`（因为它绑定了那个人的叙事）。
- 运行时借取后，由现有 AI 叙事通道（`narrativeContextFor` / `buildMemoryContext`，已注入当前 `state.emperor`）以当前皇帝身份 re-voice；不在本 spec 详述 re-voice 实现。

---

## 3. resolver / reservoir 函数签名草案

### 3.1 `successorsOf(emperor, opts)` —— 找同朝代后继帝

```js
/**
 * 返回某皇帝之后、同朝代、历史上紧接的若干后继皇帝。
 * @param {object} emperor  皇帝对象（需含 dynasty, reignStart, reignEnd, id）
 * @param {object} [opts]
 * @param {number} [opts.maxDepth=2]  最多取几位后继帝
 *        [PLACEHOLDER · 验证路径] 默认 2，playtest 定 1 还是 2（深度越大越易跳脱当前时局）
 * @returns {Array<object>} 同朝代、reignStart >= emperor.reignEnd、按 reignStart 升序、限前 maxDepth 位
 */
function successorsOf(emperor, opts) { /* 纯 spec，不写实现 */ }
```

**判定规则（明确写死，避免实现走偏）**：
1. **同朝代**：`dynIdByEmperor(e) === dynIdByEmperor(emperor)`（L1749 的 dynasty→id 映射）。
2. **紧接**：`e.reignStart >= emperor.reignEnd`（严格在之后；绝对年坐标，BCE 为负，坐标系一致）。
3. **排序**：按 `e.reignStart` **升序**（不是 DYNASTIES 数组下标序）。
4. **去自身**：排除 `e.id === emperor.id`。
5. **限深**：取前 `opts.maxDepth` 位。
6. **⚠️ 跨朝代红线**：本函数**绝不**用 `DYNASTIES` 数组下标推算"下一朝"。原因：`DYNASTIES`（L1205）顺序非严格编年——辽/金/西夏与宋并行，`nanbei` 是北朝诸朝桶。跨朝代借事件不在本方案范围，函数遇到朝代边界即停止。

**数据可达性**：遍历全局 `EMPEROR_REGISTRY`（L1653，已在 `loadEmperorData` 合并硬编码甲类 + 内置 JSON 乙类，去重后 310 帝），每帝含 `dynasty/reignStart/reignEnd/events`，无需新数据源。

### 3.2 `buildOverflowReservoir(emperor, state, opts)` —— 建可借事件储备池

```js
/**
 * 构建「后世时局」事件储备池：收集后继帝事件中「声明可借」且通过当前状态门控者。
 * @param {object} emperor  当前执政皇帝
 * @param {object} state    游戏状态（提供 flags/relations/stats 给 gateOK）
 * @param {object} [opts]
 * @param {number} [opts.maxDepth=2]          透传给 successorsOf
 * @param {number} [opts.maxYearAhead]        可选：仅借距 emperor.reignEnd 不超过此年数的后继事件；
 *         [PLACEHOLDER · 验证路径] 默认不封顶（取后继帝整段统治期），playtest 决定是否加窗
 * @returns {Array<object>} 候选事件（已 normalizeEvent 形态），每件附元数据：
 *         { ...ev, borrowFrom: successor.id, borrowDepth: number }
 */
function buildOverflowReservoir(emperor, state, opts) { /* 纯 spec，不写实现 */ }
```

**单事件入选条件（逐条 AND）**：
1. `ev.binding === "structural" || ev.binding === "era"`（缺省=`"personal"` → 排除，见 2.2）。
2. `gateOK(ev.gating)` 对当前 `state` 为真（**直接复用现有 `gateOK`，L2984，不重写**）。`gating` 形状：`requiresFlags/forbidFlags/minStats/minRelation/maxRelation`。
3. **忽略 `ev.year` 与 `state.year` 的匹配**：后继帝事件的 `year` 是"该后继帝在位年帧"，不是玩家当前年。借取时事件被 re-voice 为"当下危机"，故不做 `ev.year <= state.year` 这类本帝事件的年份门槛（那是 `pickGatedMajor` L2999 的逻辑，不适用于借用）。
4. 可选 `maxYearAhead` 窗宽：若设，仅留 `successor.reignStart - emperor.reignEnd <= maxYearAhead` 的后继帝事件。
5. 去重：同一 `ev.id` 不重复入池（跨后继帝事件 id 应全局唯一，由现有 schema 保证）。

**附元数据用途**：
- `borrowFrom`：UI/日志溯源（"此事件原属唐高宗"），也供 playtest 信号 A 校验。
- `borrowDepth`：运行时优选 `borrowDepth` 小者（越近的后继帝越优先），避免一上来就跳到 200 年后的无关史。

### 3.3 运行时抽取（在事件选择器末尾）

事件选择器当前顺序（约 L2890–3025 的 `enterMonth` 及其调用的 `pickGatedMajor`/`pickAnchor`/`loadMidCrisis`，加本帝 `events` 按年匹配 L2902，再到 random pool）：**在 random pool 之后追加一层 fallback**——

```
if (state.inOverflow && reservoir 非空) {
  候选 = reservoir.filter(ev => !state.overflowTriggered.includes(ev.id||ev.title))
                  .sort(by borrowDepth asc, then 随机);
  若候选非空 → 取首条，标 currentEvent.source = "overflow"，记入 state.overflowTriggered；
  若候选空 → 退化为现有 random pool（保持不空抽）；
}
```

---

## 4. 集成点清单（实现时对照）

| 位置 | 改动 | 说明 |
|------|------|------|
| `E()` 构造（L1228） | 加第 9 参 `binding`，默认 `"personal"` | 硬编码甲类标注入口，向后兼容 |
| `normalizeEvent`（L1656） | 加 `binding: ev.binding \|\| "personal"` | JSON 乙类标注入口 |
| 超期判定（L3955 附近） | 置 `state.inOverflow = state.year > state.emperor.reignEnd` | 复用现有超期信号，新增布尔标志 |
| 事件选择器（L2890–3025） | random pool 后加 overflow fallback（见 3.3） | 接 reservoir |
| `currentEvent`（L2275） | 借取事件设 `source:"overflow"` | 现有 `source` 字段零成本接 UI 徽标 |
| `state` 初始化 | 新增 `inOverflow:false`、`overflowTriggered:[]` | 运行时字段，序列化需兼容旧档 |
| UI 渲染 | 检测 `source==="overflow"` 显示「后世时局」徽标 | 防体验混淆（失败信号 C） |

---

## 5. Playtest 失败信号（先定义坏长什么样）

- **A（致命 / binding 泄漏）**：超期事件文本指名了后继帝，或暗示"你已不是 X 帝"。触发即 fail → 回查该事件的 `binding` 标错或文本含具体人名。
- **B（内容枯竭）**：超期月里 >30% 抽不到合格 structural/era 事件（reservoir 为空或全被 `gateOK` 挡掉）。→ reservoir 太薄，需补写 structural 事件或放宽 `gating`。
- **C（体验混淆）**：玩家分不清本朝事件与后世时局。→ 确认「后世时局」徽标（UI，`source` 字段）已生效。
- **D（时局跳脱）**：`borrowDepth` 过大导致事件明显属于 100+ 年后的时局。→ 收紧 `maxDepth` 或加 `maxYearAhead` 窗。

---

## 6. 假设与待定（显式标注）

- 假设单局 extended reign 约 60–120 分钟（按月事件推）；若实测 200+ 分钟，整条超期曲线与 reservoir 窗宽需重画。
- `maxDepth` 默认 **2** \[PLACEHOLDER]，靠 playtest 定 1 还是 2。
- `maxYearAhead` 默认**不封顶** \[PLACEHOLDER]，playtest 决定是否加窗。
- 跨朝代借事件**不在范围**（断代风险）；如未来需"改朝换代"另立专项，且必须重写 `successorsOf` 的朝代边界逻辑。
- AI re-voice 文本的实现细节不在本 spec；仅规定 structural/era 事件须中性表述以可被 re-voice。

---

## 7. 不在本方案范围

1. 跨朝代事件借用（断代红线）。
2. AI 重写/neutralize 借取事件文本的具体 prompt 与回退策略。
3. 超期健康递减数值（L3955 现有逻辑）的调整——本方案只复用其超期信号，不动衰减曲线。
4. 对全部 310 帝事件库做 `binding` 标注的实际执行（那是按本规范执行的作者工作，量大，单列实施轮次）。

---

## 8. 实现状态（v1，2026-08-07）

用户指令调整了落地策略：**充分利用 AI 提示词能力生成超期事件，不手写全库**；且**事件描述严禁出现后代皇帝姓名**。故 v1 运行时走「AI 实时生成」而非「借预标注 structural 事件」。

**已落地（`index.html`）**：
- `successorsOf(emperor, {maxDepth=2})`：同朝代 + `reignStart>=reignEnd` + 按 `reignStart` 升序 + 限深；红线不用 `DYNASTIES` 下标。
- `successorReignContext(emperor, state)`：仅透出「年号 + reignPremise 主线 + 事件标题题材」，**刻意不回显后继帝姓名/庙号**，从源头压住"指名"可能。
- `P_OVERFLOW = 0.5` \[PLACEHOLDER]：超期月里「后世时局」事件占比。
- `enterMonth` 顶部置 `state.inOverflow = state.year > state.emperor.reignEnd`（复用 L3955 超期信号）；年份命中事件之后、`tech-resist` 之前插入 `else if(state.inOverflow && aiAvailable() && Math.random()<P_OVERFLOW)` → `eventType="后世时局"`。离线/无 AI 时本分支不触发，自动走常规流（优雅降级）。
- `PROMPTS.user` 增 `后世时局` 分支：注入 `successorReignContext` 题材 + **【铁律·身份中性】**——事件描述/选项/后果严禁出现任何后继君主姓名、庙号、谥号或具体身份称谓，一律中性称谓。
- `E()` 增第 9 参 `binding`（默认 `personal`，向后兼容）；`normalizeEvent` 增 `binding: ev.binding||"personal"`（fail-closed）。`binding` 现作为前向兼容字段 + 离线 fallback 的过滤依据，v1 主路径不依赖它。
- UI：事件面板加 `evt-source` 徽标，`sourceLabel` 映射 `后世时局→"后世时局"`，`paintEventRaw/paintEventBaihua` 调用 `paintSourceBadge()` 显示。
- 校验：主游戏脚本（含全部改动）通过 `node --check`；另一处带 `<!-- -->` 的小内联脚本的报错为浏览器兼容写法误报，非本次引入。

**保留的张力**：AI 生成依赖提示词严守"不指名"铁律；playtest 失败信号 A（事件文本出现后继帝名）仍是最关键的验收项，需在实测中逐条抽检。
