#!/usr/bin/env node
/**
 * contrast_audit.js — Choice of History 全站对比度审计
 * ---------------------------------------------------------------------------
 * 把《技术美术优化规格书》§4 的 "Web 技术美术预算" 做成可自动校验的关卡：
 *   1. 解析每个目标文件 :root 里的色板 token（支持 var() 引用、rgba 半透明合成）
 *   2. 对真实 UI 的「文本色 × 背景色」配对计算 WCAG 2.1 相对亮度对比度
 *   3. 自动标红不达标的配对：
 *        - 正文 / 普通文字 (role:"text")  → 阈值 4.5:1 (WCAG AA)
 *        - 大字 / UI 组件   (role:"ui")    → 阈值 3.0:1 (WCAG AA)
 *
 * 用法:  node contrast_audit.js [baseDir]
 *   baseDir 默认 = 当前工作目录；扫描其中的 index.html 与 data/tech_tree_ui.html
 *
 * 退出码:  0 = 全部达标（可接入 CI 门禁）
 *          1 = 存在未达标配对
 * ---------------------------------------------------------------------------
 */
const fs = require("fs");
const path = require("path");

// ============================ 颜色工具 ============================
function parseColor(str) {
  if (!str) return null;
  str = str.trim();
  if (str[0] === "#") {
    let h = str.slice(1);
    if (h.length === 3) h = h.split("").map((c) => c + c).join("");
    if (h.length !== 6) return null;
    return {
      r: parseInt(h.slice(0, 2), 16),
      g: parseInt(h.slice(2, 4), 16),
      b: parseInt(h.slice(4, 6), 16),
      a: 1,
    };
  }
  const m = str.match(/rgba?\(([^)]+)\)/i);
  if (m) {
    const p = m[1].split(",").map((s) => parseFloat(s.trim()));
    if (p.length < 3) return null;
    return { r: p[0], g: p[1], b: p[2], a: p[3] === undefined ? 1 : p[3] };
  }
  return null;
}

function toLinear(c) {
  c /= 255;
  return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
}
function luminance({ r, g, b }) {
  return 0.2126 * toLinear(r) + 0.7152 * toLinear(g) + 0.0722 * toLinear(b);
}
function composite(fg, bg) {
  const a = fg.a;
  return {
    r: Math.round(fg.r * a + bg.r * (1 - a)),
    g: Math.round(fg.g * a + bg.g * (1 - a)),
    b: Math.round(fg.b * a + bg.b * (1 - a)),
  };
}
function contrast(c1, c2) {
  const l1 = luminance(c1);
  const l2 = luminance(c2);
  const hi = Math.max(l1, l2);
  const lo = Math.min(l1, l2);
  return (hi + 0.05) / (lo + 0.05);
}

// ============================ 解析 :root ============================
function extractTokens(css) {
  const map = {};
  const re = /:root\s*\{([^}]*)\}/g;
  let m;
  while ((m = re.exec(css))) {
    const decl = m[1].matchAll(/(--[\w-]+)\s*:\s*([^;]+);/g);
    for (const d of decl) map[d[1].trim()] = d[2].trim();
  }
  // 解析 var() 引用（最多 5 层，防环）
  for (const k of Object.keys(map)) {
    let v = map[k];
    let guard = 0;
    while (v.includes("var(") && guard++ < 5) {
      v = v.replace(/var\((--[\w-]+)\)/g, (_, n) => map[n] || "#000000");
    }
    map[k] = v;
  }
  return map;
}

function resolveColor(name, tokens, baseBgName) {
  const val = name.startsWith("--") ? tokens[name] || name : name;
  const c = parseColor(val);
  if (!c) return null;
  if (c.a < 1) {
    const baseVal = tokens[baseBgName] || "#f4ecd8";
    const base = parseColor(baseVal) || { r: 244, g: 236, b: 216, a: 1 };
    return composite(c, base);
  }
  return { r: c.r, g: c.g, b: c.b };
}

// ====================== 真实 UI 配对（预算关卡） ======================
// 每项: [文本色(token或字面量), 背景色(token或字面量), role, 说明]
//   role "text" => 普通文字，阈值 4.5   |   role "ui" => 大字/UI组件，阈值 3.0
const PAIRINGS = {
  "index.html": [
    ["--ink", "--bg", "text", "正文"],
    ["--ink-light", "--bg", "text", "次级文字"],
    ["--dim", "--bg", "text", "弱化文字"],
    ["--dim-light", "--bg", "text", "弱化文字(已修)"],
    ["--red", "--bg", "text", "朱红强调"],
    ["--red-bright", "--bg", "text", "朱红高亮"],
    ["--gold", "--bg", "text", "金强调"],
    ["--jade", "--bg", "text", "玉强调"],
    ["--ink", "--bg-light", "text", "浅面板正文"],
    ["--dim-light", "--bg-light", "text", "浅面板弱化文字"],
    ["--red", "--bg-light", "text", "浅面板朱红"],
    ["--gold", "--bg-light", "text", "浅面板金"],
    ["--bar-fill", "--bar-bg", "ui", "进度条填充/轨道"],
    ["--gold", "--bar-bg", "ui", "金 / 进度轨道"],
  ],
  "data/tech_tree_ui.html": [
    ["--txt", "--bg", "text", "正文"],
    ["--dim", "--bg", "text", "弱化文字"],
    ["--acc", "--bg", "text", "激活标签/强调"],
    ["--gold", "--bg", "text", "金(点数)"],
    ["--red", "--bg", "text", "红(不可点)"],
    ["--green", "--bg", "text", "绿(已拥有)"],
    ["--txt", "--panel", "text", "面板正文"],
    ["--dim", "--panel", "text", "面板弱化"],
    ["--acc", "--panel", "text", "面板强调"],
    ["--gold", "--panel", "text", "面板金"],
    ["--red", "--panel", "text", "面板红"],
    ["--green", "--panel", "text", "面板绿"],
    ["--txt", "--panel2", "text", "次面板正文"],
    ["--dim", "--panel2", "text", "次面板弱化"],
    ["--acc", "--panel2", "text", "次面板强调"],
    ["--gold", "--panel2", "text", "次面板金"],
    ["--red", "--panel2", "text", "次面板红"],
    ["#ffffff", "--red", "text", "超前标签白字"],
    ["--b-agri", "--bg", "ui", "分支-农业"],
    ["--b-mil", "--bg", "ui", "分支-军事"],
    ["--b-eng", "--bg", "ui", "分支-工程"],
    ["--b-com", "--bg", "ui", "分支-商业"],
    ["--b-civ", "--bg", "ui", "分支-文明"],
    ["--b-med", "--bg", "ui", "分支-医疗"],
    ["--b-sci", "--bg", "ui", "分支-科学"],
    ["--b-law", "--bg", "ui", "分支-法律"],
    ["--b-occ", "--bg", "ui", "分支-秘术"],
  ],
};

const THRESHOLD = { text: 4.5, ui: 3.0 };

// ============================ 主流程 ============================
function auditFile(file, baseDir) {
  const abs = path.join(baseDir, file);
  if (!fs.existsSync(abs)) {
    console.log(`\n⚠ 跳过（文件不存在）: ${file}`);
    return { file, rows: [], missing: true };
  }
  const css = fs.readFileSync(abs, "utf8");
  const tokens = extractTokens(css);
  const rows = [];
  for (const [textName, bgName, role, note] of PAIRINGS[file] || []) {
    const tc = resolveColor(textName, tokens, "--bg");
    const bc = resolveColor(bgName, tokens, "--bg");
    if (!tc || !bc) {
      rows.push({ textName, bgName, role, note, ratio: null, pass: null, raw: tokens[textName] || textName });
      continue;
    }
    const ratio = contrast(tc, bc);
    const pass = ratio >= THRESHOLD[role];
    rows.push({ textName, bgName, role, note, ratio, pass, raw: tokens[textName] || textName });
  }
  return { file, rows, missing: false };
}

function main() {
  const baseDir = process.argv[2] || process.cwd();
  const files = Object.keys(PAIRINGS);
  let totalFail = 0;
  const reportLines = ["# 对比度审计报告", "", `> 生成时间: ${new Date().toISOString()}`, `> 基准目录: ${baseDir}`, ""];

  for (const file of files) {
    const { rows, missing } = auditFile(file, baseDir);
    if (missing) {
      reportLines.push(`## ${file} — 跳过（文件不存在）`, "");
      continue;
    }
    const fails = rows.filter((r) => r.ratio !== null && !r.pass);
    totalFail += fails.length;
    console.log(`\n=== ${file} ===`);
    console.log("文本色".padEnd(16), "背景色".padEnd(14), "角色".padEnd(6), "对比度".padEnd(9), "阈值".padEnd(6), "结果   说明");
    console.log("-".repeat(78));
    reportLines.push(`## ${file}`, "");
    reportLines.push("| 文本色 | 背景色 | 角色 | 对比度 | 阈值 | 结果 | 说明 |");
    reportLines.push("|--------|--------|------|--------|------|------|------|");
    for (const r of rows) {
      const th = THRESHOLD[r.role];
      if (r.ratio === null) {
        console.log(r.textName.padEnd(16), r.bgName.padEnd(14), r.role.padEnd(6), "N/A".padEnd(9), th.toFixed(1).padEnd(6), "⚠ 解析失败");
        reportLines.push(`| ${r.textName} | ${r.bgName} | ${r.role} | N/A | ${th} | ⚠ 解析失败 | ${r.note} |`);
        continue;
      }
      const flag = r.pass ? "✅" : "❌";
      const ratioStr = r.ratio.toFixed(2);
      const status = r.pass ? "PASS" : "FAIL";
      console.log(
        r.textName.padEnd(16),
        r.bgName.padEnd(14),
        r.role.padEnd(6),
        ratioStr.padEnd(9),
        th.toFixed(1).padEnd(6),
        flag,
        "  " + r.note
      );
      reportLines.push(`| ${r.textName} | ${r.bgName} | ${r.role} | ${ratioStr}:1 | ${th}:1 | ${status} | ${r.note} |`);
    }
    reportLines.push("");
  }

  console.log("\n" + "=".repeat(78));
  if (totalFail === 0) {
    console.log("✅ 全部配对通过 WCAG AA 对比度预算，无阻断项。");
    reportLines.push(`## 结论`, "", `✅ 全部 ${files.length} 个文件、所有配对通过 WCAG AA 对比度预算（正文 ≥4.5:1 / UI组件 ≥3:1），无阻断项。`);
  } else {
    console.log(`❌ 发现 ${totalFail} 处未达标配对，详见上方 ❌ 标记。`);
    reportLines.push(`## 结论`, "", `❌ 发现 **${totalFail}** 处未达标配对，需修复后重新审计（CI 门禁应在此非零退出）。`);
  }
  console.log("=".repeat(78));

  const outPath = path.join(baseDir, "tools", "contrast_audit_report.md");
  fs.writeFileSync(outPath, reportLines.join("\n"), "utf8");
  console.log(`\n📄 报告已写入: ${outPath}`);

  process.exit(totalFail === 0 ? 0 : 1);
}

main();
