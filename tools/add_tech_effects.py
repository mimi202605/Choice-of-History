# -*- coding: utf-8 -*-
"""
择决千秋 · 科技具体作用注入器（非破坏式增强，分带多样性版）
======================================================
给 data/tech_tree.json 中每个科技节点补充：
  - node["effect"]   : 结构化效果数组（type/target/perTier/cap），供引擎解析
  - node["effectDesc"]: 一句话具体作用文案（含随时代放大的数值），供科技卡展示
重写 node["functionDesc"] = 原功能介绍 + 具体作用文案。

设计约束（见对话，2026-08-08 第三轮）：
  - 每条线（同 branch×track，14 个 age 节点）按**时代分带**挂不同效果类型：
      early(age 1-4) / mid(age 5-8) / late(age 9-11) / peak(age 12-14)
    旧版把「效果类型」钉死在 special 上 → 同一条线 14 个节点效果种类完全相同，单调。
    新版本带后，玩家顺着一条线往下点，每张卡片看到的效果类型都不一样的（仍随时代放大数值）。
  - **全部当代通道**：passive(每年正月属性) / shield(灾异损失−) / eventLess(灾异触发−)
    / warEdge(战争) / relation(派系) / costLess(研究费−) / unlock(特殊抉择)。
    **移除 score（终评）通道**——用户明确要求「影响当代的」，终评加成整体移出科技实效。
  - 每个带的效果类型由该轨道的史实主题决定（根据科技本身），不纯按 age 机械轮替。
  - 所有 magnitude 有 rationale，但未经 playtest，标 [待playtest校准]。
  - 不重跑 gen_techtree.py（保住已清理的命名/占位修复）；先备份再改，可逆。
"""
import json, os, shutil, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE, "data", "tech_tree.json")

ATTR_CN = {"treasury": "国库", "people": "民心", "military": "军事", "court": "朝政", "health": "健康", "tech": "科技"}
CRISIS_CN = {"flood": "水患", "famine": "饥荒", "epidemic": "疫疠", "wound": "战伤", "dispute": "讼争", "curse": "妖异"}
FACTION_CN = {"宗室": "宗室", "士大夫": "士大夫", "边将": "边将", "商贾": "商贾"}

# 81 个 special → 4 个时代分带 → 效果数组。
# perTier 含义（与引擎一致）：
#   passive/relation : 每档(tier=age分1/2/3)×每级 的绝对增量（passive 为每年正月结算点数）
#   shield/eventLess/costLess/warEdge : 每档×每级的「百分点」
#     - warEdge winBonus : 战争胜算 +% ；lossMitigate : 战败军事损失 −%
# 分带设计原则：early 为轨道核心作用；mid/late/peak 随时代演进叠加/切换不同作用类型，
# 既保证「上下有别」(同线 14 节点效果种类不同)，又「根据科技本身」(类型贴合该轨道史实主题)。
EFFECTS = {
    # ===== 农政 =====
    "yield":     {"early":[{"type":"passive","target":"treasury","perTier":0.09,"cap":2.0}],
                  "mid":  [{"type":"passive","target":"treasury","perTier":0.09,"cap":2.0},{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "late": [{"type":"eventLess","target":"famine","perTier":6,"cap":40}],
                  "peak": [{"type":"shield","target":"famine","perTier":8,"cap":50}]},
    "flood":     {"early":[{"type":"shield","target":"flood","perTier":8,"cap":50}],
                  "mid":  [{"type":"eventLess","target":"flood","perTier":5,"cap":30}],
                  "late": [{"type":"passive","target":"people","perTier":0.06,"cap":1.4}],
                  "peak": [{"type":"relation","target":"士大夫","perTier":1,"cap":6}]},
    "fertility": {"early":[{"type":"passive","target":"people","perTier":0.07,"cap":1.6}],
                  "mid":  [{"type":"passive","target":"people","perTier":0.07,"cap":1.6},{"type":"passive","target":"treasury","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"relation","target":"士大夫","perTier":1,"cap":5}],
                  "peak": [{"type":"eventLess","target":"famine","perTier":5,"cap":30}]},
    "seed":      {"early":[{"type":"eventLess","target":"famine","perTier":6,"cap":40}],
                  "mid":  [{"type":"eventLess","target":"famine","perTier":6,"cap":40},{"type":"shield","target":"famine","perTier":6,"cap":40}],
                  "late": [{"type":"shield","target":"famine","perTier":8,"cap":50}],
                  "peak": [{"type":"passive","target":"people","perTier":0.05,"cap":1.2}]},
    "tool":      {"early":[{"type":"passive","target":"treasury","perTier":0.06,"cap":1.4},{"type":"passive","target":"tech","perTier":0.02,"cap":0.5}],
                  "mid":  [{"type":"passive","target":"tech","perTier":0.06,"cap":1.4}],
                  "late": [{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "storage":   {"early":[{"type":"shield","target":"famine","perTier":8,"cap":50}],
                  "mid":  [{"type":"shield","target":"famine","perTier":8,"cap":50},{"type":"passive","target":"treasury","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"passive","target":"people","perTier":0.05,"cap":1.2}],
                  "peak": [{"type":"relation","target":"商贾","perTier":1,"cap":6}]},
    "landlaw":   {"early":[{"type":"relation","target":"士大夫","perTier":1,"cap":8}],
                  "mid":  [{"type":"relation","target":"士大夫","perTier":1,"cap":8},{"type":"passive","target":"people","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"passive","target":"treasury","perTier":0.05,"cap":1.2}],
                  "peak": [{"type":"passive","target":"court","perTier":0.05,"cap":1.2}]},
    "reclaim":   {"early":[{"type":"passive","target":"treasury","perTier":0.05,"cap":1.2},{"type":"passive","target":"people","perTier":0.03,"cap":0.8}],
                  "mid":  [{"type":"passive","target":"people","perTier":0.06,"cap":1.4}],
                  "late": [{"type":"relation","target":"边将","perTier":1,"cap":6}],
                  "peak": [{"type":"warEdge","target":"lossMitigate","perTier":8,"cap":40}]},
    "pasture":   {"early":[{"type":"passive","target":"treasury","perTier":0.04,"cap":1.0},{"type":"passive","target":"military","perTier":0.03,"cap":0.8}],
                  "mid":  [{"type":"passive","target":"military","perTier":0.05,"cap":1.0}],
                  "late": [{"type":"relation","target":"边将","perTier":1,"cap":6}],
                  "peak": [{"type":"warEdge","target":"winBonus","perTier":1.5,"cap":10}]},
    # ===== 军工（核心 warEdge，按带叠加 派系/属性/减费，避免整线同一句）=====
    "armor":     {"early":[{"type":"warEdge","target":"lossMitigate","perTier":10,"cap":50}],
                  "mid":  [{"type":"warEdge","target":"lossMitigate","perTier":10,"cap":50},{"type":"passive","target":"military","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"relation","target":"边将","perTier":1,"cap":6}],
                  "peak": [{"type":"passive","target":"military","perTier":0.06,"cap":1.4}]},
    "weapon":    {"early":[{"type":"warEdge","target":"winBonus","perTier":2.0,"cap":15}],
                  "mid":  [{"type":"warEdge","target":"winBonus","perTier":2.0,"cap":15},{"type":"passive","target":"military","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"relation","target":"边将","perTier":1,"cap":6}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "formation": {"early":[{"type":"warEdge","target":"winBonus","perTier":1.8,"cap":14}],
                  "mid":  [{"type":"warEdge","target":"winBonus","perTier":1.8,"cap":14},{"type":"relation","target":"边将","perTier":1,"cap":6}],
                  "late": [{"type":"passive","target":"military","perTier":0.05,"cap":1.2}],
                  "peak": [{"type":"warEdge","target":"lossMitigate","perTier":8,"cap":40}]},
    "defense":   {"early":[{"type":"warEdge","target":"lossMitigate","perTier":8,"cap":40}],
                  "mid":  [{"type":"warEdge","target":"lossMitigate","perTier":8,"cap":40},{"type":"passive","target":"military","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"relation","target":"边将","perTier":1,"cap":6}],
                  "peak": [{"type":"shield","target":"wound","perTier":7,"cap":45}]},
    "cavalry":   {"early":[{"type":"warEdge","target":"winBonus","perTier":2.2,"cap":16}],
                  "mid":  [{"type":"warEdge","target":"winBonus","perTier":2.2,"cap":16},{"type":"passive","target":"military","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"relation","target":"边将","perTier":1,"cap":6}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "navy":      {"early":[{"type":"warEdge","target":"winBonus","perTier":1.6,"cap":12}],
                  "mid":  [{"type":"warEdge","target":"winBonus","perTier":1.6,"cap":12},{"type":"relation","target":"边将","perTier":1,"cap":6}],
                  "late": [{"type":"passive","target":"military","perTier":0.05,"cap":1.2}],
                  "peak": [{"type":"warEdge","target":"lossMitigate","perTier":8,"cap":40}]},
    "gunpowder": {"early":[{"type":"warEdge","target":"winBonus","perTier":2.5,"cap":18}],
                  "mid":  [{"type":"warEdge","target":"winBonus","perTier":2.5,"cap":18},{"type":"passive","target":"tech","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"relation","target":"边将","perTier":1,"cap":6}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "intel":     {"early":[{"type":"warEdge","target":"winBonus","perTier":1.4,"cap":10}],
                  "mid":  [{"type":"warEdge","target":"winBonus","perTier":1.4,"cap":10},{"type":"relation","target":"边将","perTier":1,"cap":6}],
                  "late": [{"type":"passive","target":"military","perTier":0.05,"cap":1.2}],
                  "peak": [{"type":"warEdge","target":"lossMitigate","perTier":8,"cap":40}]},
    "logistics": {"early":[{"type":"warEdge","target":"lossMitigate","perTier":9,"cap":45}],
                  "mid":  [{"type":"warEdge","target":"lossMitigate","perTier":9,"cap":45},{"type":"passive","target":"military","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    # ===== 营造（palace/brick 原为 score→朝政/民心，改当代 passive+派系）=====
    "palace":    {"early":[{"type":"passive","target":"court","perTier":0.06,"cap":1.4}],
                  "mid":  [{"type":"relation","target":"宗室","perTier":1,"cap":8}],
                  "late": [{"type":"passive","target":"people","perTier":0.05,"cap":1.2}],
                  "peak": [{"type":"relation","target":"士大夫","perTier":1,"cap":6}]},
    "bridge":    {"early":[{"type":"passive","target":"treasury","perTier":0.05,"cap":1.2},{"type":"passive","target":"people","perTier":0.02,"cap":0.5}],
                  "mid":  [{"type":"passive","target":"people","perTier":0.05,"cap":1.2}],
                  "late": [{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "road":      {"early":[{"type":"passive","target":"court","perTier":0.06,"cap":1.4}],
                  "mid":  [{"type":"passive","target":"court","perTier":0.06,"cap":1.4},{"type":"relation","target":"士大夫","perTier":1,"cap":5}],
                  "late": [{"type":"costLess","target":"research","perTier":3,"cap":20}],
                  "peak": [{"type":"passive","target":"treasury","perTier":0.04,"cap":1.0}]},
    "hydraulics":{"early":[{"type":"shield","target":"flood","perTier":9,"cap":55}],
                  "mid":  [{"type":"shield","target":"flood","perTier":9,"cap":55},{"type":"eventLess","target":"flood","perTier":5,"cap":30}],
                  "late": [{"type":"passive","target":"people","perTier":0.05,"cap":1.2}],
                  "peak": [{"type":"relation","target":"士大夫","perTier":1,"cap":6}]},
    "smelt":     {"early":[{"type":"passive","target":"tech","perTier":0.07,"cap":1.6},{"type":"passive","target":"military","perTier":0.02,"cap":0.5}],
                  "mid":  [{"type":"passive","target":"military","perTier":0.05,"cap":1.0}],
                  "late": [{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "machine":   {"early":[{"type":"passive","target":"treasury","perTier":0.07,"cap":1.6}],
                  "mid":  [{"type":"passive","target":"treasury","perTier":0.07,"cap":1.6},{"type":"passive","target":"tech","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "brick":     {"early":[{"type":"passive","target":"court","perTier":0.05,"cap":1.2}],
                  "mid":  [{"type":"relation","target":"宗室","perTier":1,"cap":6}],
                  "late": [{"type":"passive","target":"people","perTier":0.05,"cap":1.2}],
                  "peak": [{"type":"passive","target":"treasury","perTier":0.04,"cap":1.0}]},
    "city":      {"early":[{"type":"passive","target":"treasury","perTier":0.05,"cap":1.2},{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "mid":  [{"type":"passive","target":"people","perTier":0.05,"cap":1.2}],
                  "late": [{"type":"relation","target":"士大夫","perTier":1,"cap":5}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "ship":      {"early":[{"type":"passive","target":"treasury","perTier":0.06,"cap":1.5},{"type":"passive","target":"military","perTier":0.02,"cap":0.5}],
                  "mid":  [{"type":"passive","target":"military","perTier":0.05,"cap":1.0}],
                  "late": [{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "peak": [{"type":"warEdge","target":"winBonus","perTier":1.6,"cap":12}]},
    # ===== 商工 =====
    "market":    {"early":[{"type":"passive","target":"treasury","perTier":0.08,"cap":1.8}],
                  "mid":  [{"type":"passive","target":"treasury","perTier":0.08,"cap":1.8},{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "late": [{"type":"costLess","target":"research","perTier":3,"cap":20}],
                  "peak": [{"type":"passive","target":"people","perTier":0.04,"cap":1.0}]},
    "coin":      {"early":[{"type":"costLess","target":"research","perTier":4,"cap":25}],
                  "mid":  [{"type":"costLess","target":"research","perTier":4,"cap":25},{"type":"passive","target":"treasury","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "peak": [{"type":"passive","target":"treasury","perTier":0.06,"cap":1.4}]},
    "workshop":  {"early":[{"type":"passive","target":"treasury","perTier":0.07,"cap":1.6},{"type":"passive","target":"tech","perTier":0.02,"cap":0.5}],
                  "mid":  [{"type":"passive","target":"tech","perTier":0.06,"cap":1.4}],
                  "late": [{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "shipping":  {"early":[{"type":"passive","target":"treasury","perTier":0.075,"cap":1.7}],
                  "mid":  [{"type":"passive","target":"treasury","perTier":0.075,"cap":1.7},{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "late": [{"type":"warEdge","target":"winBonus","perTier":1.6,"cap":12}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "saltiron":  {"early":[{"type":"passive","target":"treasury","perTier":0.09,"cap":2.0},{"type":"passive","target":"court","perTier":0.02,"cap":0.5}],
                  "mid":  [{"type":"passive","target":"court","perTier":0.05,"cap":1.2}],
                  "late": [{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "teahorse":  {"early":[{"type":"relation","target":"边将","perTier":1,"cap":8}],
                  "mid":  [{"type":"relation","target":"边将","perTier":1,"cap":8},{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "late": [{"type":"warEdge","target":"winBonus","perTier":1.5,"cap":10}],
                  "peak": [{"type":"passive","target":"treasury","perTier":0.05,"cap":1.2}]},
    "bank":      {"early":[{"type":"costLess","target":"research","perTier":3,"cap":20},{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "mid":  [{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "late": [{"type":"passive","target":"treasury","perTier":0.06,"cap":1.4}],
                  "peak": [{"type":"passive","target":"court","perTier":0.04,"cap":1.0}]},
    "mining":    {"early":[{"type":"passive","target":"tech","perTier":0.06,"cap":1.5}],
                  "mid":  [{"type":"passive","target":"tech","perTier":0.06,"cap":1.5},{"type":"passive","target":"military","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "craft":     {"early":[{"type":"passive","target":"treasury","perTier":0.05,"cap":1.2},{"type":"passive","target":"tech","perTier":0.03,"cap":0.8}],
                  "mid":  [{"type":"passive","target":"tech","perTier":0.06,"cap":1.4}],
                  "late": [{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    # ===== 文教（exam/history/book 原为 score→朝政/民心，改当代 passive/派系）=====
    "school":    {"early":[{"type":"relation","target":"士大夫","perTier":1,"cap":8},{"type":"passive","target":"people","perTier":0.02,"cap":0.5}],
                  "mid":  [{"type":"relation","target":"士大夫","perTier":1,"cap":8}],
                  "late": [{"type":"passive","target":"people","perTier":0.06,"cap":1.4}],
                  "peak": [{"type":"passive","target":"court","perTier":0.04,"cap":1.0}]},
    "exam":      {"early":[{"type":"passive","target":"court","perTier":0.06,"cap":1.4},{"type":"unlock","target":"选才","label":"选才","domain":"court"}],
                  "mid":  [{"type":"relation","target":"士大夫","perTier":1,"cap":6}],
                  "late": [{"type":"passive","target":"people","perTier":0.05,"cap":1.2}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "history":   {"early":[{"type":"passive","target":"court","perTier":0.05,"cap":1.2},{"type":"relation","target":"士大夫","perTier":1,"cap":5}],
                  "mid":  [{"type":"relation","target":"士大夫","perTier":1,"cap":6}],
                  "late": [{"type":"passive","target":"people","perTier":0.04,"cap":1.0}],
                  "peak": [{"type":"passive","target":"court","perTier":0.06,"cap":1.4}]},
    "book":      {"early":[{"type":"passive","target":"people","perTier":0.05,"cap":1.2},{"type":"relation","target":"士大夫","perTier":1,"cap":4}],
                  "mid":  [{"type":"relation","target":"士大夫","perTier":1,"cap":6}],
                  "late": [{"type":"passive","target":"tech","perTier":0.04,"cap":1.0}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "math":      {"early":[{"type":"passive","target":"tech","perTier":0.07,"cap":1.6}],
                  "mid":  [{"type":"passive","target":"tech","perTier":0.07,"cap":1.6},{"type":"passive","target":"court","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"relation","target":"士大夫","perTier":1,"cap":5}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "geo":       {"early":[{"type":"warEdge","target":"winBonus","perTier":2.0,"cap":12},{"type":"passive","target":"tech","perTier":0.02,"cap":0.5}],
                  "mid":  [{"type":"warEdge","target":"winBonus","perTier":2.0,"cap":12}],
                  "late": [{"type":"relation","target":"边将","perTier":1,"cap":6}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "diplomacy": {"early":[{"type":"relation","target":"边将","perTier":1,"cap":8},{"type":"relation","target":"商贾","perTier":1,"cap":4}],
                  "mid":  [{"type":"relation","target":"商贾","perTier":1,"cap":6}],
                  "late": [{"type":"warEdge","target":"winBonus","perTier":1.5,"cap":10}],
                  "peak": [{"type":"passive","target":"court","perTier":0.04,"cap":1.0}]},
    "ritual":    {"early":[{"type":"relation","target":"宗室","perTier":1,"cap":8}],
                  "mid":  [{"type":"relation","target":"宗室","perTier":1,"cap":8},{"type":"relation","target":"士大夫","perTier":1,"cap":4}],
                  "late": [{"type":"passive","target":"court","perTier":0.05,"cap":1.2}],
                  "peak": [{"type":"passive","target":"people","perTier":0.04,"cap":1.0}]},
    "educate":   {"early":[{"type":"passive","target":"people","perTier":0.07,"cap":1.6},{"type":"relation","target":"士大夫","perTier":1,"cap":3}],
                  "mid":  [{"type":"passive","target":"people","perTier":0.07,"cap":1.6}],
                  "late": [{"type":"relation","target":"士大夫","perTier":1,"cap":6}],
                  "peak": [{"type":"passive","target":"court","perTier":0.04,"cap":1.0}]},
    # ===== 医养 =====
    "herb":      {"early":[{"type":"shield","target":"epidemic","perTier":7,"cap":50}],
                  "mid":  [{"type":"shield","target":"epidemic","perTier":7,"cap":50},{"type":"eventLess","target":"epidemic","perTier":4,"cap":25}],
                  "late": [{"type":"passive","target":"health","perTier":0.05,"cap":1.2}],
                  "peak": [{"type":"relation","target":"士大夫","perTier":1,"cap":5}]},
    "acup":      {"early":[{"type":"passive","target":"health","perTier":0.07,"cap":1.6}],
                  "mid":  [{"type":"passive","target":"health","perTier":0.07,"cap":1.6},{"type":"passive","target":"people","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"relation","target":"士大夫","perTier":1,"cap":5}],
                  "peak": [{"type":"eventLess","target":"epidemic","perTier":4,"cap":25}]},
    "formula":   {"early":[{"type":"shield","target":"epidemic","perTier":6,"cap":45}],
                  "mid":  [{"type":"shield","target":"epidemic","perTier":6,"cap":45},{"type":"eventLess","target":"epidemic","perTier":4,"cap":25}],
                  "late": [{"type":"passive","target":"health","perTier":0.05,"cap":1.2}],
                  "peak": [{"type":"relation","target":"商贾","perTier":1,"cap":5}]},
    "surgery":   {"early":[{"type":"shield","target":"wound","perTier":7,"cap":50}],
                  "mid":  [{"type":"shield","target":"wound","perTier":7,"cap":50},{"type":"passive","target":"health","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"relation","target":"士大夫","perTier":1,"cap":5}],
                  "peak": [{"type":"warEdge","target":"lossMitigate","perTier":8,"cap":40}]},
    "epidemic":  {"early":[{"type":"shield","target":"epidemic","perTier":9,"cap":60},{"type":"eventLess","target":"epidemic","perTier":5,"cap":35}],
                  "mid":  [{"type":"shield","target":"epidemic","perTier":9,"cap":60}],
                  "late": [{"type":"eventLess","target":"epidemic","perTier":6,"cap":40}],
                  "peak": [{"type":"passive","target":"health","perTier":0.06,"cap":1.4}]},
    "health":    {"early":[{"type":"passive","target":"health","perTier":0.06,"cap":1.5}],
                  "mid":  [{"type":"passive","target":"health","perTier":0.06,"cap":1.5},{"type":"passive","target":"people","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"relation","target":"士大夫","perTier":1,"cap":5}],
                  "peak": [{"type":"eventLess","target":"epidemic","perTier":4,"cap":25}]},
    "gyne":      {"early":[{"type":"passive","target":"health","perTier":0.05,"cap":1.2},{"type":"passive","target":"people","perTier":0.03,"cap":0.8}],
                  "mid":  [{"type":"passive","target":"people","perTier":0.05,"cap":1.2}],
                  "late": [{"type":"relation","target":"士大夫","perTier":1,"cap":5}],
                  "peak": [{"type":"passive","target":"health","perTier":0.06,"cap":1.4}]},
    "vet":       {"early":[{"type":"passive","target":"people","perTier":0.05,"cap":1.2},{"type":"passive","target":"military","perTier":0.02,"cap":0.6}],
                  "mid":  [{"type":"passive","target":"military","perTier":0.04,"cap":1.0}],
                  "late": [{"type":"relation","target":"边将","perTier":1,"cap":5}],
                  "peak": [{"type":"warEdge","target":"lossMitigate","perTier":6,"cap":30}]},
    "shaman":    {"early":[{"type":"passive","target":"health","perTier":0.04,"cap":1.0},{"type":"shield","target":"curse","perTier":4,"cap":25}],
                  "mid":  [{"type":"shield","target":"curse","perTier":5,"cap":30}],
                  "late": [{"type":"passive","target":"people","perTier":0.04,"cap":1.0}],
                  "peak": [{"type":"relation","target":"士大夫","perTier":1,"cap":4}]},
    # ===== 天文数理（calendar/astro/mathclassic/natural 原为 score→民心/朝政/科技，改当代）=====
    "calendar":  {"early":[{"type":"passive","target":"people","perTier":0.05,"cap":1.2},{"type":"eventLess","target":"famine","perTier":3,"cap":20}],
                  "mid":  [{"type":"eventLess","target":"famine","perTier":5,"cap":30}],
                  "late": [{"type":"passive","target":"tech","perTier":0.04,"cap":1.0}],
                  "peak": [{"type":"relation","target":"士大夫","perTier":1,"cap":5}]},
    "astro":     {"early":[{"type":"passive","target":"court","perTier":0.05,"cap":1.2},{"type":"passive","target":"tech","perTier":0.02,"cap":0.5}],
                  "mid":  [{"type":"passive","target":"tech","perTier":0.06,"cap":1.4}],
                  "late": [{"type":"warEdge","target":"winBonus","perTier":1.5,"cap":10}],
                  "peak": [{"type":"relation","target":"士大夫","perTier":1,"cap":5}]},
    "mathclassic":{"early":[{"type":"passive","target":"tech","perTier":0.07,"cap":1.6},{"type":"passive","target":"court","perTier":0.03,"cap":0.8}],
                  "mid":  [{"type":"passive","target":"tech","perTier":0.07,"cap":1.6}],
                  "late": [{"type":"relation","target":"士大夫","perTier":1,"cap":5}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "survey":    {"early":[{"type":"warEdge","target":"winBonus","perTier":1.8,"cap":12},{"type":"passive","target":"tech","perTier":0.02,"cap":0.5}],
                  "mid":  [{"type":"warEdge","target":"winBonus","perTier":1.8,"cap":12}],
                  "late": [{"type":"relation","target":"边将","perTier":1,"cap":6}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "map":       {"early":[{"type":"warEdge","target":"winBonus","perTier":2.0,"cap":12},{"type":"unlock","target":"料敌","label":"料敌","domain":"war"}],
                  "mid":  [{"type":"warEdge","target":"winBonus","perTier":2.0,"cap":12}],
                  "late": [{"type":"relation","target":"边将","perTier":1,"cap":6}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "weather":   {"early":[{"type":"eventLess","target":"famine","perTier":6,"cap":40},{"type":"eventLess","target":"flood","perTier":4,"cap":25}],
                  "mid":  [{"type":"eventLess","target":"flood","perTier":5,"cap":30}],
                  "late": [{"type":"passive","target":"people","perTier":0.04,"cap":1.0}],
                  "peak": [{"type":"shield","target":"flood","perTier":6,"cap":35}]},
    "physics":   {"early":[{"type":"passive","target":"tech","perTier":0.08,"cap":1.8}],
                  "mid":  [{"type":"passive","target":"tech","perTier":0.08,"cap":1.8},{"type":"passive","target":"court","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"relation","target":"士大夫","perTier":1,"cap":5}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "chem":      {"early":[{"type":"passive","target":"tech","perTier":0.06,"cap":1.5},{"type":"shield","target":"epidemic","perTier":3,"cap":20}],
                  "mid":  [{"type":"shield","target":"epidemic","perTier":4,"cap":25}],
                  "late": [{"type":"relation","target":"商贾","perTier":1,"cap":5}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "natural":   {"early":[{"type":"passive","target":"health","perTier":0.04,"cap":1.0},{"type":"passive","target":"tech","perTier":0.03,"cap":0.8}],
                  "mid":  [{"type":"passive","target":"health","perTier":0.06,"cap":1.4}],
                  "late": [{"type":"relation","target":"士大夫","perTier":1,"cap":5}],
                  "peak": [{"type":"eventLess","target":"epidemic","perTier":4,"cap":25}]},
    # ===== 律礼（census/censor/clan 原为 score→国库/朝政，改当代）=====
    "penal":     {"early":[{"type":"relation","target":"士大夫","perTier":1,"cap":8},{"type":"shield","target":"dispute","perTier":4,"cap":25}],
                  "mid":  [{"type":"shield","target":"dispute","perTier":5,"cap":30}],
                  "late": [{"type":"passive","target":"court","perTier":0.05,"cap":1.2}],
                  "peak": [{"type":"relation","target":"边将","perTier":1,"cap":5}]},
    "rituallaw": {"early":[{"type":"relation","target":"宗室","perTier":1,"cap":6},{"type":"relation","target":"士大夫","perTier":1,"cap":4}],
                  "mid":  [{"type":"relation","target":"士大夫","perTier":1,"cap":6}],
                  "late": [{"type":"passive","target":"court","perTier":0.05,"cap":1.2}],
                  "peak": [{"type":"passive","target":"people","perTier":0.04,"cap":1.0}]},
    "landdeed":  {"early":[{"type":"shield","target":"dispute","perTier":8,"cap":50}],
                  "mid":  [{"type":"shield","target":"dispute","perTier":8,"cap":50},{"type":"passive","target":"treasury","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"relation","target":"士大夫","perTier":1,"cap":5}],
                  "peak": [{"type":"passive","target":"court","perTier":0.04,"cap":1.0}]},
    "census":    {"early":[{"type":"passive","target":"treasury","perTier":0.04,"cap":1.0},{"type":"passive","target":"court","perTier":0.03,"cap":0.8}],
                  "mid":  [{"type":"passive","target":"treasury","perTier":0.06,"cap":1.4}],
                  "late": [{"type":"relation","target":"士大夫","perTier":1,"cap":5}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "censor":    {"early":[{"type":"relation","target":"士大夫","perTier":1,"cap":6},{"type":"eventLess","target":"dispute","perTier":3,"cap":20}],
                  "mid":  [{"type":"relation","target":"士大夫","perTier":1,"cap":6}],
                  "late": [{"type":"passive","target":"court","perTier":0.05,"cap":1.2}],
                  "peak": [{"type":"relation","target":"边将","perTier":1,"cap":5}]},
    "border":    {"early":[{"type":"relation","target":"边将","perTier":1,"cap":8},{"type":"warEdge","target":"winBonus","perTier":1.5,"cap":10}],
                  "mid":  [{"type":"warEdge","target":"winBonus","perTier":1.5,"cap":10}],
                  "late": [{"type":"passive","target":"court","perTier":0.04,"cap":1.0}],
                  "peak": [{"type":"relation","target":"宗室","perTier":1,"cap":5}]},
    "clan":      {"early":[{"type":"relation","target":"宗室","perTier":1,"cap":8},{"type":"passive","target":"court","perTier":0.03,"cap":0.8}],
                  "mid":  [{"type":"relation","target":"宗室","perTier":1,"cap":8}],
                  "late": [{"type":"passive","target":"people","perTier":0.04,"cap":1.0}],
                  "peak": [{"type":"passive","target":"court","perTier":0.05,"cap":1.2}]},
    "militarylaw":{"early":[{"type":"warEdge","target":"lossMitigate","perTier":8,"cap":40},{"type":"relation","target":"边将","perTier":1,"cap":5}],
                  "mid":  [{"type":"warEdge","target":"lossMitigate","perTier":8,"cap":40}],
                  "late": [{"type":"passive","target":"court","perTier":0.04,"cap":1.0}],
                  "peak": [{"type":"relation","target":"士大夫","perTier":1,"cap":5}]},
    "lawsuit":   {"early":[{"type":"shield","target":"dispute","perTier":7,"cap":45}],
                  "mid":  [{"type":"shield","target":"dispute","perTier":7,"cap":45},{"type":"passive","target":"court","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"relation","target":"士大夫","perTier":1,"cap":5}],
                  "peak": [{"type":"passive","target":"people","perTier":0.04,"cap":1.0}]},
    # ===== 方技玄术（fengshui/kanYu 原为 score→民心/军事，改当代）=====
    "alchemy":   {"early":[{"type":"passive","target":"health","perTier":0.05,"cap":1.2},{"type":"passive","target":"tech","perTier":0.03,"cap":0.8}],
                  "mid":  [{"type":"passive","target":"tech","perTier":0.06,"cap":1.4}],
                  "late": [{"type":"relation","target":"士大夫","perTier":1,"cap":4}],
                  "peak": [{"type":"passive","target":"health","perTier":0.06,"cap":1.4}]},
    "divin":     {"early":[{"type":"unlock","target":"占断","label":"占断","domain":"crisis"}],
                  "mid":  [{"type":"unlock","target":"占断","label":"占断","domain":"crisis"},{"type":"relation","target":"士大夫","perTier":1,"cap":4}],
                  "late": [{"type":"passive","target":"court","perTier":0.04,"cap":1.0}],
                  "peak": [{"type":"relation","target":"宗室","perTier":1,"cap":4}]},
    "fengshui":  {"early":[{"type":"passive","target":"court","perTier":0.03,"cap":0.8},{"type":"passive","target":"people","perTier":0.04,"cap":1.0}],
                  "mid":  [{"type":"passive","target":"people","perTier":0.05,"cap":1.2}],
                  "late": [{"type":"relation","target":"士大夫","perTier":1,"cap":4}],
                  "peak": [{"type":"shield","target":"curse","perTier":4,"cap":25}]},
    "fangji":    {"early":[{"type":"passive","target":"health","perTier":0.06,"cap":1.5},{"type":"passive","target":"tech","perTier":0.02,"cap":0.5}],
                  "mid":  [{"type":"passive","target":"health","perTier":0.06,"cap":1.5}],
                  "late": [{"type":"relation","target":"士大夫","perTier":1,"cap":4}],
                  "peak": [{"type":"eventLess","target":"epidemic","perTier":4,"cap":25}]},
    "kanYu":     {"early":[{"type":"warEdge","target":"winBonus","perTier":1.6,"cap":12},{"type":"passive","target":"military","perTier":0.03,"cap":0.8}],
                  "mid":  [{"type":"warEdge","target":"winBonus","perTier":1.6,"cap":12}],
                  "late": [{"type":"relation","target":"边将","perTier":1,"cap":5}],
                  "peak": [{"type":"passive","target":"court","perTier":0.04,"cap":1.0}]},
    "talisman":  {"early":[{"type":"shield","target":"curse","perTier":6,"cap":40}],
                  "mid":  [{"type":"shield","target":"curse","perTier":6,"cap":40},{"type":"passive","target":"health","perTier":0.03,"cap":0.8}],
                  "late": [{"type":"relation","target":"士大夫","perTier":1,"cap":4}],
                  "peak": [{"type":"eventLess","target":"curse","perTier":4,"cap":25}]},
    "fate":      {"early":[{"type":"unlock","target":"占验","label":"占验","domain":"any"}],
                  "mid":  [{"type":"unlock","target":"占验","label":"占验","domain":"any"},{"type":"relation","target":"宗室","perTier":1,"cap":4}],
                  "late": [{"type":"passive","target":"court","perTier":0.04,"cap":1.0}],
                  "peak": [{"type":"relation","target":"士大夫","perTier":1,"cap":4}]},
    "dunjia":    {"early":[{"type":"warEdge","target":"winBonus","perTier":1.8,"cap":12},{"type":"shield","target":"curse","perTier":3,"cap":20}],
                  "mid":  [{"type":"warEdge","target":"winBonus","perTier":1.8,"cap":12}],
                  "late": [{"type":"relation","target":"边将","perTier":1,"cap":5}],
                  "peak": [{"type":"costLess","target":"research","perTier":3,"cap":20}]},
    "witch":     {"early":[{"type":"warEdge","target":"winBonus","perTier":1.5,"cap":10},{"type":"shield","target":"curse","perTier":4,"cap":25}],
                  "mid":  [{"type":"warEdge","target":"winBonus","perTier":1.5,"cap":10}],
                  "late": [{"type":"relation","target":"边将","perTier":1,"cap":5}],
                  "peak": [{"type":"eventLess","target":"curse","perTier":4,"cap":25}]},
}

BANDS = ("early", "mid", "late", "peak")
UNSEEN = set(EFFECTS.keys())


def tier_of(age):
    return 1 if age <= 3 else (2 if age <= 7 else 3)


def band_of(age):
    # early 1-4 / mid 5-8 / late 9-11 / peak 12-14
    if age <= 4:
        return "early"
    if age <= 8:
        return "mid"
    if age <= 11:
        return "late"
    return "peak"


def fmt(sp, age):
    t = sp["type"]
    tg = sp.get("target", "")
    pt = sp.get("perTier", 0)
    cap = sp.get("cap", 0)
    tier = tier_of(age)
    if t == "passive":
        step = pt * tier
        return "每年正月「%s」+%.2f（每级叠加，封顶%.1f/年）" % (ATTR_CN.get(tg, tg), step, cap)
    if t in ("shield", "eventLess"):
        pct = pt * tier
        cn = CRISIS_CN.get(tg, tg)
        if t == "shield":
            return "「%s」类灾异结算损失−%d%%·每级（封顶%d%%）" % (cn, pct, cap)
        return "「%s」类灾异触发率−%d%%·每级（封顶%d%%）" % (cn, pct, cap)
    if t == "warEdge":
        pct = pt * tier
        label = "战争胜算 +" if tg == "winBonus" else "战败军事损失 −"
        return "%s%d%%·每级（封顶%d%%）" % (label, pct, cap)
    if t == "relation":
        step = pt * tier
        return "派系「%s」好感 +%d·每级（封顶%d）" % (FACTION_CN.get(tg, tg), step, cap)
    if t == "costLess":
        pct = pt * tier
        return "研究科技耗费 −%d%%·每级（封顶%d%%）" % (pct, cap)
    if t == "unlock":
        return "相关事件解锁特殊抉择：「%s」" % sp.get("label", tg)
    if t == "ability":
        return "可发动「%s」（冷却%d月）" % (sp.get("label", tg), sp.get("cooldown", 3))
    return ""


def main():
    if not os.path.exists(JSON_PATH):
        print("FATAL: 未找到", JSON_PATH)
        return
    # 备份
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = JSON_PATH + ".bak_effects_" + ts
    shutil.copy2(JSON_PATH, bak)
    print("已备份 ->", os.path.basename(bak))

    data = json.load(open(JSON_PATH, encoding="utf-8"))
    nodes = data.get("nodes", [])
    n_total = len(nodes)
    n_eff = 0
    n_desc = 0
    missing = []
    specials_seen = set()
    bandless = []  # 缺少某分带的 special（结构上必须四带齐全）

    for n in nodes:
        sp_def = EFFECTS.get(n.get("special"))
        if sp_def is None:
            missing.append(n.get("id"))
            continue
        for b in BANDS:
            if b not in sp_def:
                bandless.append(n["special"])
        specials_seen.add(n["special"])
        UNSEEN.discard(n["special"])
        sp_list = sp_def[band_of(n["age"])]
        # 写结构化 effect（深拷贝，避免脚本间共享引用）
        n["effect"] = [dict(s) for s in sp_list]
        eff = "; ".join(fmt(s, n["age"]) for s in sp_list)
        n["effectDesc"] = eff
        base = (n.get("functionDesc") or "").strip()
        # 去掉旧版可能已追加的 effectDesc 残留（以「｜」分隔标记）
        if "｜" in base:
            base = base.split("｜", 1)[0].strip()
        # 幂等保护：若节点原本就没有「一句话作用」，上一轮会把 functionDesc 直接写成 eff，
        # 再跑一次时 base 就等于 eff，拼出「eff ｜ eff」重复文案（曾波及 196 个节点）。
        if base == eff:
            base = ""
        n["functionDesc"] = (base + " ｜ " + eff) if base else eff
        n_eff += 1
        n_desc += 1

    json.dump(data, open(JSON_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("节点总数:", n_total, " | 写入 effect:", n_eff, " | 写入 effectDesc:", n_desc)
    print("EFFECTS 覆盖 special 数:", len(specials_seen), "/", len(EFFECTS))

    # 多样性自检：每条线（special）跨 4 分带应当出现 ≥2 种不同效果类型，否则仍单调。
    mono = []
    variety_dist = {}
    for sp, bands in EFFECTS.items():
        types = set()
        for b in BANDS:
            for s in bands.get(b, []):
                types.add(s["type"])
        variety_dist[len(types)] = variety_dist.get(len(types), 0) + 1
        if len(types) < 2:
            mono.append(sp)
    print("每条线「跨带不同效果类型数」分布:", dict(sorted(variety_dist.items())))
    if mono:
        print("⚠ 仍单调（<2 种类型）的线:", mono)
    else:
        print("✅ 全部 81 条线跨带类型 ≥2，单调问题已消除")
    # score 残留检查（绝不允许再出现终评通道）
    left_score = [sp for sp, bands in EFFECTS.items()
                  for b in BANDS for s in bands.get(b, []) if s.get("type") == "score"]
    if left_score:
        print("⚠ 仍含 score 通道的 special:", sorted(set(left_score)))
    else:
        print("✅ 无 score（终评）通道残留")
    if bandless:
        print("⚠ 缺少分带的 special:", sorted(set(bandless)))
    if UNSEEN:
        print("⚠ 未使用的 EFFECTS key（数据里无对应 special）:", sorted(UNSEEN))
    if missing:
        print("⚠ 数据中无 effect 映射的节点 special:", missing[:20], "...共", len(missing))


if __name__ == "__main__":
    main()
