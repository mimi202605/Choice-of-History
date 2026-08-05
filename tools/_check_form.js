// 临时验证：内置模式下设置界面应显示真实默认 api/model，key 仍掩码
const fs=require("fs"), vm=require("vm");
const html=fs.readFileSync("index.html","utf8");
const m=html.match(/"use strict";([\s\S]*?)\n<\/script>/);
let body=m[1];
const data=fs.readFileSync("data/emperors/coh_data.js","utf8");
const cfg=fs.readFileSync("coh_config.js","utf8");
const store={};
function stubEl(id){ if(!store[id]) store[id]={id,value:"",textContent:"",checked:false,classList:{add(){},remove(){},contains(){return false;}},style:{},addEventListener(){},click(){},focus(){}}; return store[id]; }
const sandbox={ console, setTimeout, clearTimeout, setInterval, clearInterval, Math, JSON, Date, Array, Object, Set, Map, Promise, AbortController:function(){this.abort=()=>{};this.signal={};}, fetch:async()=>({ok:false,status:0,json:async()=>({}),text:async()=>""}),
  localStorage:{store:{},getItem(k){return this.store[k]??null;},setItem(k,v){this.store[k]=v;}},
  document:{ getElementById:(id)=>stubEl(id), querySelectorAll:()=>[], querySelector:()=>null, addEventListener(){} },
};
sandbox.window=sandbox; sandbox.globalThis=sandbox;
const driver=`
  loadSettings();
  settings.builtin=true;
  loadSettingsToForm();
  globalThis.__R={
    api: document.getElementById("set-api").value,
    model: document.getElementById("set-model").value,
    key: document.getElementById("set-key").value,
    defModel: BUILTIN_DEFAULT_MODEL,
    cfgApi: (window.COH_CONFIG&&window.COH_CONFIG.apiBase)
  };
  globalThis.__DONE=true;
`;
try{
  const ctx=vm.createContext(sandbox);
  new vm.Script(data+"\n"+cfg+"\n"+body+"\n"+driver,{filename:"t.js"}).runInContext(ctx);
}catch(e){ console.log("ERR",e.message, e.stack&&e.stack.split("\n")[1]); }
setTimeout(()=>{
  const r=sandbox.__R;
  const okApi = r.api===r.cfgApi;
  const okModel = r.model===r.defModel;
  const okKeyMask = r.key.indexOf("已配置")>=0;
  console.log("set-api  =", r.api);
  console.log("set-model=", r.model);
  console.log("set-key  =", r.key);
  console.log("CHECK api==COH_CONFIG.apiBase:", okApi);
  console.log("CHECK model==BUILTIN_DEFAULT_MODEL:", okModel);
  console.log("CHECK key 仍为掩码:", okKeyMask);
  console.log("RESULT:", (okApi&&okModel&&okKeyMask)?"PASS":"FAIL");
  process.exit((okApi&&okModel&&okKeyMask)?0:1);
}, 300);
