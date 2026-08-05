// coh_config.sample.js —— 复制为 coh_config.js 并填入你的部署参数（coh_config.js 已被 git 忽略）。
// 两种形态二选一：
//  A) 官方/共享内置额度：保留 builtinCred（密文），其余默认。
//  B) 自托管：builtinCred 留空，填入自有 api / key（model 可改）。
// 进阶：配置 provisionUrl 启用每用户短期 token 下发（需自建轻量下发服务，详见优化设计文档 7.2）。
window.COH_CONFIG = {
  builtinCred: "",                       // 留空则无需内置密文（走自托管 api/key 或 provisionUrl）
  apiBase: "https://api.agnes-ai.cn/v1", // 自托管时改为你的 API 地址
  model: "agnes-2.5-flash",
  provisionUrl: "",                      // 例：https://your-provision.example.com/token
  selfHosted: false
};
