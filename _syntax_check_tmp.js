const fs = require("fs");
const { execSync } = require("child_process");
const node = "C:/Users/admin/.workbuddy/binaries/node/versions/22.22.2/node.exe";
const html = fs.readFileSync("index.html", "utf8");
const re = /<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g;
let m, i = 0;
while ((m = re.exec(html))) {
  const code = m[1];
  i++;
  if (!code.trim()) continue;
  const f = "_chk_" + i + ".js";
  fs.writeFileSync(f, code);
  try {
    execSync(`"${node}" --check "${f}"`, { stdio: "pipe" });
    console.log("SCRIPT #" + i + ": OK");
  } catch (e) {
    const out = (e.stderr || "").toString();
    console.log("SCRIPT #" + i + ": SYNTAX ERROR\n" + out.split("\n").slice(0, 4).join("\n"));
  }
}
