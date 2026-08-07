// 临时校验：抽取 index.html 中三段硬编码事件池，校验语法与 baihua 结构。用完即删。
const fs = require("fs");
const path = require("path");
const html = fs.readFileSync(path.join(__dirname, "..", "index.html"), "utf8");
const lines = html.split("\n");

function extractBlock(name){
  const start = lines.findIndex(l => l.includes("const " + name + " = ["));
  if (start < 0) throw new Error("未找到 " + name);
  let i = start;
  while (i < lines.length && lines[i].trim() !== "];") i++;
  if (i >= lines.length) throw new Error(name + " 未找到结束 ];");
  return lines.slice(start, i + 1).join("\n");
}

let total = 0, ok = 0, errs = [];
for (const name of ["DAILY_FALLBACK", "CRISIS_FALLBACK", "TECH_RESIST_EVENTS"]) {
  const block = extractBlock(name);
  let arr;
  try {
    arr = new Function(block + "\nreturn " + name + ";")();
  } catch (e) {
    errs.push(name + " 语法错误: " + e.message);
    continue;
  }
  for (const ev of arr) {
    total++;
    const b = ev.baihua;
    const titleOk = ev.title && ev.description && Array.isArray(ev.choices) && ev.choices.length === 5;
    if (!b || b.title == null || b.description == null || !Array.isArray(b.choices) || b.choices.length !== 5) {
      errs.push((ev.title || "?") + " 的 baihua 不完整");
    } else if (!titleOk) {
      errs.push((ev.title || "?") + " 原文结构异常");
    } else {
      ok++;
    }
  }
}
console.log("硬编码池条目总数:", total, " 结构完整:", ok);
if (errs.length) { console.log("问题:"); errs.forEach(e => console.log("  - " + e)); process.exit(1); }
else console.log("全部通过");
