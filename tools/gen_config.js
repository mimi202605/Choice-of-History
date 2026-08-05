// gen_config.js —— 从环境变量生成 coh_config.js（部署期注入，避免共享密钥入库）。
// 用法（环境变量可选）：
//   COH_BUILTIN_CRED=<密文>  COH_API_BASE=https://...  COH_MODEL=agnes-2.0-flash \
//   COH_PROVISION_URL=https://.../token  node tools/gen_config.js
// 不传则回退到占位（游戏仍可离线/自填 Key 运行）。
const fs = require("fs");
const path = require("path");

const cfg = {
  builtinCred: process.env.COH_BUILTIN_CRED || "",
  apiBase: process.env.COH_API_BASE || "https://api.agnes-ai.cn/v1",
  model: process.env.COH_MODEL || "agnes-2.0-flash",
  provisionUrl: process.env.COH_PROVISION_URL || "",
  selfHosted: !!process.env.COH_SELF_HOSTED
};

const out =
  "// 自动生成（tools/gen_config.js），git 忽略。请勿手改。\n" +
  "window.COH_CONFIG = " + JSON.stringify(cfg, null, 2) + ";\n";

const outPath = path.join(__dirname, "..", "coh_config.js");
fs.writeFileSync(outPath, out, "utf8");
console.log("已写出:", outPath);
console.log("builtinCred:", cfg.builtinCred ? "(已注入)" : "(空)",
            "| provisionUrl:", cfg.provisionUrl || "(无)",
            "| selfHosted:", cfg.selfHosted);
