// 凭据配置（7.2 去共享化）——部署期由 tools/gen_config.js 生成，git 忽略，不入库。
// 此文件含内置凭据密文（解密算法见 tools/coh_cipher.js），用于官方内置额度体验；
// 自托管者请将 builtinCred 留空、填入自有 api/key，或配置 provisionUrl 启用每用户额度。
// 注意：本文件出现在工作副本中仅为本地运行/演示；正式发布前应改为 per-deploy 注入，避免共享同一密文。
window.COH_CONFIG = {
  builtinCred: "nixHFXszoW0pMGijaZX2TTYBgly+RWHpTbBWvBw1KbLIHI+ZVN8Ix21EEGvj3XzlNH7Uq1OQrslFvKXHQpDDBjBiwug0ZivSfv3dJoBXHjfeu1DOSh8Ldo9peNQOjbblqc0sIEm3o8YeNFZIuzmvwF1NHA7kGM5s90wQ6AMuj6VMIQ==",
  apiBase: "https://api.agnes-ai.cn/v1",
  model: "agnes-2.5-flash",
  provisionUrl: "",      // 留空=使用内置密文；填入=每用户短期 token 下发（需自建下发服务）
  selfHosted: false
};
