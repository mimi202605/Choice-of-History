# 给现有 data/tech_tree.json 的每个节点补上 functionDesc（一句话功能介绍）。
# 直接从 gen_techtree.py 复用 SPECIAL_DESC 映射，保证与生成器一致；
# 采用原地更新，不触碰其它字段、不改写 tech_presets.json。
# 用法：python tools/add_tech_functiondesc.py
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_techtree import SPECIAL_DESC  # noqa: E402

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
TREE_PATH = os.path.join(DATA_DIR, "tech_tree.json")


def main():
    with open(TREE_PATH, "r", encoding="utf-8") as f:
        tree = json.load(f)

    nodes = tree.get("nodes", [])
    missing = set()
    n_added = 0
    for n in nodes:
        special = n.get("special")
        if special not in SPECIAL_DESC:
            missing.add(special)
            continue
        if "functionDesc" not in n:
            n_added += 1
        n["functionDesc"] = SPECIAL_DESC[special]

    if missing:
        print("警告：以下 special 无对应功能介绍，已跳过：", sorted(missing))

    with open(TREE_PATH, "w", encoding="utf-8") as f:
        json.dump(tree, f, ensure_ascii=False, indent=1)

    print(f"✓ 节点总数: {len(nodes)}，本次新增/覆盖 functionDesc: {n_added}")
    print(f"✓ 已写回: {TREE_PATH}")


if __name__ == "__main__":
    main()
