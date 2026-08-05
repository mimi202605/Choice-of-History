// 离线生成内置凭据密文（从环境变量读取明文，明文不落文件）。
// 用法：API_URL=... API_KEY=... API_MODEL=... node tools/gen_builtin.js
const { encrypt, decrypt } = require("./coh_cipher.js");

const api = process.env.API_URL;
const key = process.env.API_KEY;
const model = process.env.API_MODEL;

if (!api || !key || !model) {
  console.error("缺少环境变量 API_URL / API_KEY / API_MODEL");
  process.exit(1);
}

const payload = JSON.stringify({ api, key, model });
const blob = encrypt(payload);
const verify = decrypt(blob);

console.log("BLOB:" + blob);
console.log("VERIFY_OK:" + (verify === payload));
if (verify !== payload) {
  console.error("解密校验失败！");
  console.error("expected:", payload);
  console.error("got     :", verify);
  process.exit(2);
}
