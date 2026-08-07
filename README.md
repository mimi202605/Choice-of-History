# 择决千秋 · Choice of History

> 皇帝模拟 · 月度抉择 · 历史分支
> Emperor Sim · Monthly Choices · Branching History

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Emperors](https://img.shields.io/badge/emperors-320%2B-brightgreen.svg)]
[![Events](https://img.shields.io/badge/events-1900%2B-orange.svg)]
[![Tech Tree](https://img.shields.io/badge/tech%20tree-1134%20nodes-blue.svg)]
[![Stack](https://img.shields.io/badge/stack-Vanilla%20JS%20%7C%20Zero--dep-lightgrey.svg)]
[![Demo](https://img.shields.io/badge/demo-GitHub%20Pages-red.svg)](https://mimi202605.github.io/Choice-of-History/)
[![Language](https://img.shields.io/badge/language-简体中文-informational.svg)]

**择决千秋** 是一款纯前端的中国历代皇帝模拟游戏。你将从夏至清的 320 余位皇帝中任选一位，以「每月五选一」的抉择推进国运——历史为骨，选择为肉，你的每一个决定都可能改写千秋。

*Choice of History is a zero-dependency, browser-based emperor simulation. Pick any of 300+ emperors from the Xia to Qing dynasties and steer the realm through monthly five-option decisions — where history is the skeleton and your choices are the flesh.*

## ✨ Features

- 📜 **历史为骨，选择为肉** — 320+ 位皇帝（夏→清 18 朝代全覆盖），1900+ 基于《二十四史》《资治通鉴》的史实事件；其中 18 位旗舰帝王拥有手写精修事件库。
- 📊 **六维数值，寿命自决** — 国库 / 民心 / 军事 / 朝政 / 健康 / 科技；健康归零即驾崩，寿命由你的累积抉择决定。
- 🔬 **科技穿越** — 1134 节点宏大科技树（9 分支 × 14 时代），可超越时代但会触发保守派阻力。
- 🤖 **AI 史官** — 通过 OpenAI 兼容 API 实时生成事件与史书体例点评，严谨的中文容错提示词保障稳定性。
- 🎭 **三种模式** — 标准 / 速通（跳过 AI 后果，节奏更快）/ 离线（纯本地规则推演，零网络请求）。
- 🗣 **白话文模式** — 文言↔现代白话一键切换，无需文言基础也能沉浸游玩。
- 🖌 **水墨古籍风 UI** — 100% CSS 渐变 + Canvas 水墨，**零位图、零依赖、无构建**；通过 WCAG AA 对比度审计。
- 🧠 **长期记忆** — 分级记忆系统保持多月份叙事连贯，AI 不再「失忆」。

## 🎮 Live Demo

▶ 在线试玩：**https://mimi202605.github.io/Choice-of-History/**

支持标准 / 速通 / 离线三档模式，默认内置加密演示凭据，打开即玩；亦可填入自有 OpenAI 兼容接口。

## 🚀 Quick Start

**方式 A · 在线试玩**
直接打开上面的 Live Demo 链接，无需安装。

**方式 B · 本地运行（双击即玩）**
```bash
git clone https://github.com/mimi202605/Choice-of-History.git
# 进入目录，双击 index.html 用浏览器打开即可
```
勾选「离线模式」可完全不发起网络请求，最适合本地单机游玩。

**方式 C · 自托管 / 自有接口**
复制配置模板并填入你的参数：
```bash
cp coh_config.sample.js coh_config.js
# 编辑 coh_config.js：清空 builtinCred，填入 apiBase / model（及可选的 provisionUrl）
```
详见下方 [Configuration](#configuration-配置--自托管)。

## 📖 How to Play

1. 选择朝代与皇帝，阅读开局背景与初始六维数值。
2. 每月系统判定事件来源：**历史节点 / 日常政务（AI 生成）/ 数值危机 / 随机时局**。
3. 面对事件做出「五选一」抉择——进取 / 保守 / 革新 / 怀柔 / 铁腕，各有得失，需权衡短期收益与长期风险。
4. 查看史官点评与六维变化动画，自动存档，推进下月。
5. 任一数值 ≤10 触发危机；**健康 = 0 驾崩**，进入结算：在位年数、后世史官总评、关键决策回顾。

## 🛠 Tech Stack

- **原生 JavaScript + CSS + Canvas**，单 `index.html`，**零依赖、无构建、无 npm**。
- 美术：100% CSS 渐变 + Canvas 水墨粒子（仓库零位图资源）。
- 叙事：OpenAI 兼容 Chat Completions API（`response_format: json_object`），完整容错与降级后备事件池。
- 字体：Google Fonts `Ma Shan Zheng`（书法标题）+ `Noto Serif SC`（宋体正文）。
- 部署：GitHub Pages 静态托管；`localStorage` 存档（3 手动 + 1 自动槽）。

## 📂 Project Structure

```
Choice-of-History/
├── index.html              # 游戏主文件（HTML + CSS + JS 全内嵌）
├── coh_config.sample.js    # 自托管配置模板（复制为 coh_config.js）
├── data/                   # 皇帝数据库 / 科技树 / 随机池（JSON + 合并后的 coh_data.js）
├── tools/                  # 构建与注入脚本（build_data.js 等）
├── docs/                   # 设计文档 / 系统设计 / 规格书
└── LICENSE                 # MIT
```

## ⚙️ Configuration / 配置 / 自托管

游戏默认内置一套**加密存储**的演示凭据（模型 `agnes-2.0-flash`，端点 `api.agnes-ai.cn`），明文不落盘、不显示。两种形态二选一：

- **A) 官方/共享内置额度**：保留 `builtinCred`，开箱即玩。
- **B) 自托管**：`builtinCred` 留空，填入自有 `apiBase` / `model`（可加 `provisionUrl` 启用每用户短期 token）。

```js
// coh_config.js
window.COH_CONFIG = {
  builtinCred: "",                       // 留空则走自托管 api/key
  apiBase: "https://your-api.example.com/v1",
  model: "your-model",
  provisionUrl: "",                      // 可选：短期 token 下发服务
  selfHosted: false
};
```

## 🗺 Roadmap

- [x] 320+ 帝王 / 1900+ 史实事件 / 1134 节点科技树
- [x] 退位 / 复辟旗标、长期记忆注入、越代科技减免、时间一致性约束
- [ ] 更多旗舰帝王的精修事件库
- [ ] 移动端布局与触控优化
- [ ] 其他更多文明首领

## 🤝 Contributing

欢迎提 Issue 与 PR！无论是史实纠错、事件补充，还是美术与体验优化，都在欢迎之列。请先阅读 `docs/` 下的设计文档与规格书，以保持风格一致。

## 📄 License

[MIT](LICENSE) © 2026 mimi202605

## 🙏 Acknowledgements

- 字体：[Ma Shan Zheng](https://fonts.google.com/specimen/Ma+Shan+Zheng) · [Noto Serif SC](https://fonts.google.com/specimen/Noto+Serif+SC)（Google Fonts）
- 美术借鉴：《对马岛之魂》墨韵 · 《三国：全面战争》金石质感 · 《大神 / Okami》水墨粒子
- 史实骨架：《二十四史》《资治通鉴》
