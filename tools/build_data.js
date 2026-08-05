// 构建脚本：将 data/emperors/*.json 合并为 data/emperors/coh_data.js
// 以全局变量形式暴露，规避 file:// 下 fetch 被 CORS 拦截导致乙类皇帝静默丢失的问题。
// 用法：node tools/build_data.js
const fs = require("fs");
const path = require("path");

const dir = path.join(__dirname, "..", "data", "emperors");
const files = [
  "01-xia-shang-zhou-qin.json",
  "02-han-xin-sanguo.json",
  "03-jin-nanbeichao-sui.json",
  "04-tang-wudai.json",
  "05-song-liao-jin-xixia.json",
  "06-yuan.json",
  "07-ming.json",
  "08-qing.json",
];

let all = [];
let counts = {};
for (const f of files) {
  const p = path.join(dir, f);
  if (!fs.existsSync(p)) {
    console.warn("跳过缺失文件:", f);
    continue;
  }
  const data = JSON.parse(fs.readFileSync(p, "utf8"));
  const emps = Array.isArray(data) ? data : (data.emperors || []);
  counts[f] = emps.length;
  all = all.concat(emps);
}

// 去重（按 id；无 id 按 name+dynasty）
const seen = new Set();
const dedup = [];
for (const e of all) {
  const key = e.id || (e.dynasty + "|" + e.name);
  if (seen.has(key)) continue;
  seen.add(key);
  dedup.push(e);
}

const out =
  "/* 自动生成，请勿手改。源：data/emperors/*.json —— 以全局变量暴露，使 file:// 双击打开亦可加载。 */\n" +
  "window.COH_BUILTIN_EMPERORS = " + JSON.stringify(dedup, null, 0) + ";\n";

const outPath = path.join(dir, "coh_data.js");
fs.writeFileSync(outPath, out, "utf8");

console.log("合并皇帝:", dedup.length, "位");
console.log("各文件:", JSON.stringify(counts));
console.log("已写出:", outPath, "(" + (out.length / 1024).toFixed(1) + " KB)");
