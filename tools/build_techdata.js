// 构建脚本：将 data/tech_tree.json + data/tech_presets.json 合并为 data/tech_data.js
// 以全局变量（window.TECH_TREE / window.TECH_PRESETS）形式暴露，
// 规避 file:// 下 fetch 被 CORS 拦截导致科技树数据静默丢失的问题。
// 用法：node tools/build_techdata.js
const fs = require("fs");
const path = require("path");

const dataDir = path.join(__dirname, "..", "data");
const treePath = path.join(dataDir, "tech_tree.json");
const presetsPath = path.join(dataDir, "tech_presets.json");

if (!fs.existsSync(treePath)) { console.error("缺失:", treePath); process.exit(1); }
if (!fs.existsSync(presetsPath)) { console.error("缺失:", presetsPath); process.exit(1); }

const tree = JSON.parse(fs.readFileSync(treePath, "utf8"));
const presets = JSON.parse(fs.readFileSync(presetsPath, "utf8"));

const out =
  "/* 自动生成，请勿手改。源：data/tech_tree.json + data/tech_presets.json —— 以全局变量暴露，使 file:// 双击打开亦可加载。 */\n" +
  "window.TECH_TREE = " + JSON.stringify(tree, null, 0) + ";\n" +
  "window.TECH_PRESETS = " + JSON.stringify(presets, null, 0) + ";\n";

const outPath = path.join(dataDir, "tech_data.js");
fs.writeFileSync(outPath, out, "utf8");

const nodeCount = (tree.nodes || []).length;
const dynCount = Object.keys(presets.dynasties || {}).length;
console.log("科技树节点:", nodeCount, " 朝代预设:", dynCount);
console.log("已写出:", outPath, "(" + (out.length / 1024).toFixed(1) + " KB)");
