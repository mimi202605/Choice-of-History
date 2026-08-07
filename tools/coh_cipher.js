// COH 凭据可逆加密（混淆级 / obfuscation-grade）。
// 说明：浏览器端无法做到真正的密钥保密——解密密钥必须随客户端下发。
// 此模块的目的是「避免明文泄露」：源码和运行时都不出现明文 API Key，
// 仓库、DOM、localStorage 中只保留密文。请勿将其视为安全强度的加密。
const COH_CIPHER = (function () {
  // 密钥口令：由分散的字符串片段在运行时拼接而成，避免单一明文常量被直接搜到。
  const K = [
    "a7G", "9zQ", "k2#", "Ln4", "xYp", "0wE", " Rt", "vB8",
    "c3m", "Hd1", "5sU", "jfZ", "eO6", "Tg9", "uI2", "nP0"
  ].join("");
  // 固定盐（IV），用于打散密文。
  const IV = [0x9e, 0x2c, 0x47, 0x15, 0x7b, 0x33, 0xa1, 0x6d];

  function strToBytes(s) {
    const o = [];
    for (let i = 0; i < s.length; i++) {
      let c = s.charCodeAt(i);
      if (c < 0x80) o.push(c);
      else if (c < 0x800) o.push(0xc0 | (c >> 6), 0x80 | (c & 0x3f));
      else o.push(0xe0 | (c >> 12), 0x80 | ((c >> 6) & 0x3f), 0x80 | (c & 0x3f));
    }
    return o;
  }
  function bytesToStr(b) {
    let s = "", i = 0;
    while (i < b.length) {
      let c = b[i++];
      if (c < 0x80) s += String.fromCharCode(c);
      else if (c < 0xe0) { const c2 = b[i++]; s += String.fromCharCode(((c & 0x1f) << 6) | (c2 & 0x3f)); }
      else { const c2 = b[i++], c3 = b[i++]; s += String.fromCharCode(((c & 0xf) << 12) | ((c2 & 0x3f) << 6) | (c3 & 0x3f)); }
    }
    return s;
  }
  const B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
  function b64enc(bytes) {
    let s = "";
    for (let i = 0; i < bytes.length; i += 3) {
      const n = (bytes[i] << 16) | ((bytes[i + 1] || 0) << 8) | (bytes[i + 2] || 0);
      s += B64[(n >> 18) & 63] + B64[(n >> 12) & 63] +
        ((i + 1 < bytes.length) ? B64[(n >> 6) & 63] : "=") +
        ((i + 2 < bytes.length) ? B64[n & 63] : "=");
    }
    return s;
  }
  function b64dec(str) {
    const map = {}; for (let j = 0; j < 64; j++) map[B64[j]] = j;
    const out = []; let i = 0;
    while (i < str.length) {
      const a = map[str[i++]] || 0, b = map[str[i++]] || 0, c = map[str[i++]] || 0, d = map[str[i++]] || 0;
      const n = (a << 18) | (b << 12) | (c << 6) | d;
      out.push((n >> 16) & 255);
      if (i - 2 < str.length && str[i - 2] !== "=") out.push((n >> 8) & 255);
      if (i - 1 < str.length && str[i - 1] !== "=") out.push(n & 255);
    }
    return out;
  }
  function seedFrom(arr) {
    let h = 2166136261 >>> 0;
    for (let i = 0; i < arr.length; i++) { h ^= arr[i]; h = Math.imul(h, 16777619); }
    return h >>> 0;
  }
  // xorshift32 生成密钥流。
  function keystream(len, base) {
    const ks = new Array(len); let s = base >>> 0;
    for (let i = 0; i < len; i++) {
      s ^= s << 13; s >>>= 0;
      s ^= s >> 17;
      s ^= s << 5; s >>>= 0;
      ks[i] = s & 0xff;
    }
    return ks;
  }
  function encrypt(plain) {
    const pb = strToBytes(K);
    const pt = strToBytes(plain);
    const out = IV.slice();
    const base = seedFrom(pb.concat(IV));
    const ks = keystream(pt.length, base);
    for (let i = 0; i < pt.length; i++) out.push(pt[i] ^ ks[i]);
    return b64enc(out);
  }
  function decrypt(blob) {
    const bytes = b64dec(blob);
    const body = bytes.slice(IV.length);
    const pb = strToBytes(K);
    const base = seedFrom(pb.concat(IV));
    const ks = keystream(body.length, base);
    const pt = body.map((b, i) => b ^ ks[i]);
    return bytesToStr(pt);
  }
  return { encrypt, decrypt };
})();

if (typeof module !== "undefined" && module.exports) module.exports = COH_CIPHER;
