# 对比度审计报告

> 生成时间: 2026-08-06T09:16:22.128Z
> 基准目录: D:\工作\2026\开发的软件\Choice-of-History

## index.html

| 文本色 | 背景色 | 角色 | 对比度 | 阈值 | 结果 | 说明 |
|--------|--------|------|--------|------|------|------|
| --ink | --bg | text | 13.01:1 | 4.5:1 | PASS | 正文 |
| --ink-light | --bg | text | 8.73:1 | 4.5:1 | PASS | 次级文字 |
| --dim | --bg | text | 5.40:1 | 4.5:1 | PASS | 弱化文字 |
| --dim-light | --bg | text | 5.09:1 | 4.5:1 | PASS | 弱化文字(已修) |
| --red | --bg | text | 6.45:1 | 4.5:1 | PASS | 朱红强调 |
| --red-bright | --bg | text | 4.95:1 | 4.5:1 | PASS | 朱红高亮 |
| --gold | --bg | text | 5.09:1 | 4.5:1 | PASS | 金强调 |
| --jade | --bg | text | 5.20:1 | 4.5:1 | PASS | 玉强调 |
| --ink | --bg-light | text | 14.65:1 | 4.5:1 | PASS | 浅面板正文 |
| --dim-light | --bg-light | text | 5.73:1 | 4.5:1 | PASS | 浅面板弱化文字 |
| --red | --bg-light | text | 7.27:1 | 4.5:1 | PASS | 浅面板朱红 |
| --gold | --bg-light | text | 5.73:1 | 4.5:1 | PASS | 浅面板金 |
| --bar-fill | --bar-bg | ui | 6.23:1 | 3:1 | PASS | 进度条填充/轨道 |
| --gold | --bar-bg | ui | 4.40:1 | 3:1 | PASS | 金 / 进度轨道 |

## data/tech_tree_ui.html

| 文本色 | 背景色 | 角色 | 对比度 | 阈值 | 结果 | 说明 |
|--------|--------|------|--------|------|------|------|
| --txt | --bg | text | 13.01:1 | 4.5:1 | PASS | 正文 |
| --dim | --bg | text | 5.40:1 | 4.5:1 | PASS | 弱化文字 |
| --acc | --bg | text | 5.38:1 | 4.5:1 | PASS | 激活标签/强调 |
| --gold | --bg | text | 5.09:1 | 4.5:1 | PASS | 金(点数) |
| --red | --bg | text | 6.45:1 | 4.5:1 | PASS | 红(不可点) |
| --green | --bg | text | 5.20:1 | 4.5:1 | PASS | 绿(已拥有) |
| --txt | --panel | text | 14.19:1 | 4.5:1 | PASS | 面板正文 |
| --dim | --panel | text | 5.89:1 | 4.5:1 | PASS | 面板弱化 |
| --acc | --panel | text | 5.87:1 | 4.5:1 | PASS | 面板强调 |
| --gold | --panel | text | 5.55:1 | 4.5:1 | PASS | 面板金 |
| --red | --panel | text | 7.04:1 | 4.5:1 | PASS | 面板红 |
| --green | --panel | text | 5.67:1 | 4.5:1 | PASS | 面板绿 |
| --txt | --panel2 | text | 12.33:1 | 4.5:1 | PASS | 次面板正文 |
| --dim | --panel2 | text | 5.12:1 | 4.5:1 | PASS | 次面板弱化 |
| --acc | --panel2 | text | 5.10:1 | 4.5:1 | PASS | 次面板强调 |
| --gold | --panel2 | text | 4.82:1 | 4.5:1 | PASS | 次面板金 |
| --red | --panel2 | text | 6.11:1 | 4.5:1 | PASS | 次面板红 |
| #ffffff | --red | text | 7.60:1 | 4.5:1 | PASS | 超前标签白字 |
| --b-agri | --bg | ui | 3.38:1 | 3:1 | PASS | 分支-农业 |
| --b-mil | --bg | ui | 4.95:1 | 3:1 | PASS | 分支-军事 |
| --b-eng | --bg | ui | 4.87:1 | 3:1 | PASS | 分支-工程 |
| --b-com | --bg | ui | 3.38:1 | 3:1 | PASS | 分支-商业 |
| --b-civ | --bg | ui | 4.88:1 | 3:1 | PASS | 分支-文明 |
| --b-med | --bg | ui | 5.20:1 | 3:1 | PASS | 分支-医疗 |
| --b-sci | --bg | ui | 3.93:1 | 3:1 | PASS | 分支-科学 |
| --b-law | --bg | ui | 3.11:1 | 3:1 | PASS | 分支-法律 |
| --b-occ | --bg | ui | 3.87:1 | 3:1 | PASS | 分支-秘术 |

## 结论

✅ 全部 2 个文件、所有配对通过 WCAG AA 对比度预算（正文 ≥4.5:1 / UI组件 ≥3:1），无阻断项。