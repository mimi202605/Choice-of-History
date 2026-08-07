#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_baihua.py —— 《抉择千秋 / Choice of History》白话文模式 · 批量翻译脚本

功能：
  读取 data/emperors/0*.json 中全部皇帝的文言文设定（历史评价 / 背景 / 时代背景 /
  每个历史事件的 标题·描述·五选项·史实结局），调用 OpenAI 兼容接口，将其译为
  通俗易懂的现代白话文，写回各皇帝的 `baihua` 字段。

  翻译结果以「预置白话层」形式随数据打包，游戏开启「白话文模式」时即逐字替换原文，
  离线、即时、零运行时开销。脚本可断点续译（已完整翻译的皇帝自动跳过），也可配合
  index.html 的「运行时缺译补译」机制：即便此处未译，游戏在联网时也会按需补译并缓存。

用法：
  # 默认走内置端点（需自备 Key）
  export OPENAI_API_KEY="sk-..."
  python tools/gen_baihua.py

  # 自托管 / 其他 OpenAI 兼容端点
  OPENAI_API_KEY="sk-..." OPENAI_BASE_URL="https://your.endpoint/v1" \
  OPENAI_MODEL="gpt-4o-mini" python tools/gen_baihua.py

  # 仅试译前 3 位皇帝（验证效果）
  python tools/gen_baihua.py --limit 3

  # 指定模型 / 仅处理某几份文件
  python tools/gen_baihua.py --model agnes-2.0-flash --files 01-xia-shang-zhou-qin.json

完成后务必运行： node tools/build_data.js
以便将带 baihua 的数据重新打包进 data/emperors/coh_data.js（游戏实际加载的文件）。
"""
import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(HERE), "data", "emperors")
DEFAULT_FILES = [
    "01-xia-shang-zhou-qin.json",
    "02-han-xin-sanguo.json",
    "03-jin-nanbeichao-sui.json",
    "04-tang-wudai.json",
    "05-song-liao-jin-xixia.json",
    "06-yuan.json",
    "07-ming.json",
    "08-qing.json",
]
CHUNK = 15          # 每位皇帝按事件数分块翻译，避免单次输出过长
MAX_RETRY = 3
SLEEP_BETWEEN = 0.25


def get_cfg():
    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.agnes-ai.cn/v1").rstrip("/")
    model = os.environ.get("OPENAI_MODEL", "agnes-2.0-flash")
    return api_key, base_url, model


def call_chat(base_url, api_key, model, system, user):
    url = base_url + "/chat/completions"
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.3,
        "response_format": {"type": "json_object"},
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
    })
    last_err = None
    for attempt in range(MAX_RETRY):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            return json.loads(content)
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code == 429:
                time.sleep(2 * (attempt + 1))
                continue
            try:
                detail = e.read().decode("utf-8", "ignore")[:200]
            except Exception:
                detail = ""
            raise RuntimeError(f"HTTP {e.code} {detail}")
        except Exception as e:  # 网络/解析/超时
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"调用失败: {last_err}")


def translate_chunk(emp, events, include_top, cfg):
    api_key, base_url, model = cfg
    system = ("你是严谨的古文今译专家。请将游戏中的文言文文案逐条译为通俗易懂的现代白话文，"
              "保持原意、史实、人物与地名不变，语气贴合原文（庄重史书体），不得增删情节，"
              "不得改写为现代改编或续写。只输出一个 JSON 对象，不要任何解释或 Markdown。")

    lines = []
    if include_top:
        if emp.get("evaluation"):
            lines.append("【历史评价】" + emp["evaluation"])
        if emp.get("background"):
            lines.append("【背景】" + emp["background"])
        if emp.get("eraContext"):
            lines.append("【时代背景】" + emp["eraContext"])
    for ev in events:
        eid = ev.get("id") or ""
        title = ev.get("title") or ""
        desc = ev.get("description") or ""
        choices = ev.get("choices") or []
        outcome = ev.get("historicalOutcome") or ""
        cline = "；".join(f"{i+1}.{c}" for i, c in enumerate(choices))
        lines.append(f"[事件 {eid}]\n标题：{title}\n描述：{desc}\n选项：{cline}\n史实结局：{outcome}")

    spec = []
    if include_top:
        spec.append('"evaluation":"<历史评价白话>","background":"<背景白话>","eraContext":"<时代背景白话>"')
    spec.append('"events":{ "<事件id>": {"title":"","description":"","choices":["","","","",""],"historicalOutcome":""} }')
    user = ("下面是一位游戏君主的文言文设定，请逐条翻译。\n"
            "输出 JSON 结构：{ " + ", ".join(spec) + " }\n"
            "注意：events 的键必须是给出的<事件id>；choices 必须正好 5 条且与原文顺序一致；"
            "未给出的字段不要出现。\n\n" + "\n\n".join(lines))

    return call_chat(base_url, api_key, model, system, user)


def is_complete(emp):
    bh = emp.get("baihua")
    if not bh:
        return False
    if not (bh.get("evaluation") and bh.get("background") and bh.get("eraContext")):
        return False
    events = emp.get("events") or []
    ev_map = bh.get("events") or {}
    for ev in events:
        eid = ev.get("id")
        if not eid:
            continue
        m = ev_map.get(eid)
        if not m:
            return False
        if not (m.get("title") and m.get("description") and isinstance(m.get("choices"), list)
                and len(m["choices"]) == 5 and m.get("choices") and m.get("historicalOutcome") is not None):
            return False
    return True


def translate_emperor(emp, cfg):
    events = emp.get("events") or []
    chunks = [events[i:i + CHUNK] for i in range(0, len(events), CHUNK)]
    result = {"evaluation": "", "background": "", "eraContext": "", "events": {}}
    for ci, chunk in enumerate(chunks):
        include_top = (ci == 0)
        data = translate_chunk(emp, chunk, include_top, cfg)
        if include_top:
            result["evaluation"] = data.get("evaluation", "") or result["evaluation"]
            result["background"] = data.get("background", "") or result["background"]
            result["eraContext"] = data.get("eraContext", "") or result["eraContext"]
        evs = data.get("events") or {}
        for k, v in evs.items():
            if isinstance(v, dict):
                result["events"][k] = v
    # 兜底：若模型漏翻顶层字段，保留已有（若有）
    old = emp.get("baihua") or {}
    for k in ("evaluation", "background", "eraContext"):
        if not result.get(k) and old.get(k):
            result[k] = old[k]
    return result


def process_file(fname, cfg, limit):
    path = os.path.join(DATA_DIR, fname)
    if not os.path.exists(path):
        print(f"  · 跳过（文件不存在）：{fname}")
        return 0, 0
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    emps = data if isinstance(data, list) else data.get("emperors", [])
    done = 0
    translated = 0
    for emp in emps:
        if limit is not None and (done + translated) >= limit:
            break
        name = emp.get("name", "?")
        if is_complete(emp):
            done += 1
            continue
        try:
            bh = translate_emperor(emp, cfg)
            emp["baihua"] = bh
            translated += 1
            print(f"  ✓ 已译：{name}（{len(bh['events'])} 则事件）")
        except Exception as e:
            print(f"  ✗ 翻译失败：{name} — {e}")
            continue
        time.sleep(SLEEP_BETWEEN)
    # 无论是否全译完，写回（含已跳过但原本就完整的）
    if isinstance(data, list):
        out = data
    else:
        out = data
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    return done, translated


def main():
    ap = argparse.ArgumentParser(description="批量生成白话文翻译（写入 baihua 字段）")
    ap.add_argument("--files", nargs="*", default=DEFAULT_FILES, help="要处理的源 JSON 文件")
    ap.add_argument("--limit", type=int, default=None, help="最多翻译多少位皇帝（用于试译）")
    ap.add_argument("--model", default=None, help="覆盖模型名")
    ap.add_argument("--base-url", default=None, help="覆盖 API Base URL")
    ap.add_argument("--api-key", default=None, help="覆盖 API Key")
    args = ap.parse_args()

    if args.model:
        os.environ["OPENAI_MODEL"] = args.model
    if args.base_url:
        os.environ["OPENAI_BASE_URL"] = args.base_url
    if args.api_key:
        os.environ["OPENAI_API_KEY"] = args.api_key

    api_key, base_url, model = get_cfg()
    if not api_key:
        print("✗ 未检测到 OPENAI_API_KEY。请先设置环境变量，或在 coh_config.js 中配置后导出。")
        print("  示例：export OPENAI_API_KEY=\"sk-...\" && python tools/gen_baihua.py")
        sys.exit(1)

    cfg = (api_key, base_url, model)
    print(f"端点：{base_url}  模型：{model}")
    total_done = total_tr = 0
    for fname in args.files:
        print(f"\n== 处理 {fname} ==")
        d, t = process_file(fname, cfg, args.limit)
        total_done += d
        total_tr += t
    print(f"\n完成。已完整跳过 {total_done} 位，新翻译 {total_tr} 位。")
    print("记得运行： node tools/build_data.js")


if __name__ == "__main__":
    main()
