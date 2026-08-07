// 临时探针：解密内置凭据(JSON)并探测端点连通性/鉴权。用完即删。
const fs = require("fs");
const https = require("https");
const path = require("path");

const root = path.join(__dirname, "..");
const cfgPath = path.join(root, "coh_config.js");
const cipherPath = path.join(root, "tools", "coh_cipher.js");
const { decrypt } = require(cipherPath);

const c = fs.readFileSync(cfgPath, "utf8");
const m = c.match(/builtinCred:\s*"([^"]+)"/);
if (!m) { console.log("NO_BUILTIN_CRED"); process.exit(1); }
const dec = decrypt(m[1]);
let d;
try { d = JSON.parse(dec); } catch (e) { console.log("DECRYPT_NOT_JSON"); console.log(dec.slice(0, 60)); process.exit(1); }
console.log("API=" + (d.api || ""));
console.log("MODEL=" + (d.model || ""));
console.log("KEY_LEN=" + (d.key ? d.key.length : 0));

const base = (d.api || "https://api.agnes-ai.cn/v1").replace(/\/$/, "");
const u = new URL(base + "/v1/models");
const req = https.request({
  hostname: u.hostname,
  path: u.pathname,
  method: "GET",
  timeout: 8000,
  headers: { "Authorization": "Bearer " + (d.key || "") }
}, (r) => {
  console.log("PROBE_STATUS=" + r.statusCode);
  let body = "";
  r.on("data", (dd) => body += dd);
  r.on("end", () => { console.log("PROBE_BODY=" + body.slice(0, 200)); process.exit(0); });
});
req.on("error", (e) => { console.log("PROBE_ERR=" + (e.code || e.message)); process.exit(0); });
req.on("timeout", () => { console.log("PROBE_TIMEOUT"); req.destroy(); process.exit(0); });
req.end();
