# 随机时局系统（v0.2）落地概览

> 把"无抉择、自动改数值"的随机时局接入《择决千秋》，时期分桶 + 507 类事件 + enterMonth 掷骰全部落进 `index.html`。

## 交付物
| 文件 | 角色 | 状态 |
|------|------|------|
| `index.html` | 游戏主程序，接入随机时局系统 | 已改（主脚本 `node --check` 通过） |
| `data/random_pools.js` | 8 桶共 **507 类**自动生效事件（由生成器写出） | 已生成 |
| `tools/gen_random_pools.py` | 事件池生成器 + 平衡校验 | 已生成 |
| `docs/随机事件系统设计.md` | GDD v0.2 + §13 落地状态 | 已补 |

## 接入要点
1. **时期分桶** `eraTagOf(emperor)`：按 `reignStart` 史料年份映射 8 桶，**零改动 262 帝数据**；立国年（960/1271/1368/1644）归新朝桶。
2. **平衡常量**（复用 B2 单一真相）：`P_RAND=0.18` / `RANDOM_COOLDOWN=1` / `ANTI_CLUSTER=0.6` / `RANDOM_STAT_CAP=±10` / `RANDOM_STAT_CAP_MAJOR=±20`。
3. **状态字段**：`newState` 增加 `_lastRandomId` / `_monthSinceRandom` / `_lastRandomMajorNeg`。
4. **掷骰分支**：`enterMonth` 在非危机月、科技阻力之后、中段加压之前掷骰；命中后早分发 `fireRandomEvent()` 直接结算并渲染结果面板（无选项）。
5. **函数簇**：`eraTagOf` / `reignPhase` / `canFireRandom` / `weightedPick` / `loadRandomEvent` / `scaleByResilience` / `applyRandomChanges` / `fireRandomEvent` / `renderRandomEvent`。

## 设计纪律
- 复用 B1 失败链（`nextMonth` 结算）与 `applyCoupling`（六维耦合）。
- **刻意不含 `applyOutcome` 安全网**（+2 保底）——随机冲击本就该允许纯负面。
- 韧性调制：负面变化按参考维度当前值缩放（满值 ×0.7 / 中位 ×1.0 / 零值 ×1.3），硬上限锁死。
- 数据缺失（脚本未加载）时 `canFireRandom` 优雅降级，不掷骰、零崩溃。

## 冒烟校验（Node 隔离沙箱）
- `scaleByResilience` 公式正确；`applyRandomChanges` 硬上限锁死（非 major ≤±10、major ≤±20）。
- 8 桶 × 600 月长局：命中率 ≈17.3%（≈`P_RAND`）、calamity/boon 均衡、**相邻同 id 重复=0 / NaN=0 / 越界=0 / 连续 major 负面最长=1**（反簇集生效）。

## 待 playtest（[PLACEHOLDER]）
- 真实浏览器 `renderRandomEvent` 的 DOM 表现。
- `P_RAND=0.18` 在完整对局中"意外崩盘占比"目标 < 总崩盘 15%，需 Monte Carlo / 实测回填。
