// 临时运行器：解密内置凭据(JSON) -> 注入 OPENAI_* 环境变量 -> 调用 tools/gen_baihua.py
// 用法：node tools/_bh_run.js [--limit N] [--files x.json ...]   （参数透传给 gen_baihua.py）
const { spawnSync } = require("child_process");
const fs = require("fs");
const path = require("path");
const { decrypt } = require("./coh_cipher.js");

const root = path.join(__dirname, "..");
const cfgPath = path.join(root, "coh_config.js");
const c = fs.readFileSync(cfgPath, "utf8");
const m = c.match(/builtinCred:\s*"([^"]+)"/);
if (!m) { console.error("NO_BUILTIN_CRED"); process.exit(1); }
const d = JSON.parse(decrypt(m[1]));

process.env.OPENAI_API_KEY = d.key || "";
process.env.OPENAI_BASE_URL = (d.api || "https://api.agnes-ai.cn/v1").replace(/\/$/, "");
process.env.OPENAI_MODEL = d.model || "agnes-2.0-flash";

const PY = "C:\\Users\\admin\\.workbuddy\\binaries\\python\\versions\\3.13.12\\python.exe";
const script = path.join(root, "tools", "gen_baihua.py");
const args = [script, ...process.argv.slice(2)];

console.log("[runner] base=" + process.env.OPENAI_BASE_URL + " model=" + process.env.OPENAI_MODEL + " keyLen=" + process.env.OPENAI_API_KEY.length);
const r = spawnSync(PY, args, { stdio: "inherit", env: process.env });
process.exit(r.status === null ? 1 : r.status);
