# -*- coding: utf-8 -*-
"""史实审查：提取全量数据面 + 结构化校验"""
import json, os, glob, sys, io, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMP_DIR = os.path.join(BASE, 'data', 'emperors')

def load_all():
    files = sorted(glob.glob(os.path.join(EMP_DIR, '[0-9][0-9]-*.json')))
    out = []
    for f in files:
        d = json.load(open(f, encoding='utf-8'))
        for e in d.get('emperors', []):
            e['_file'] = os.path.basename(f)
            e['_group'] = d.get('group')
            out.append(e)
    return out

def main():
    emps = load_all()
    print('总君主数:', len(emps))
    byfile = {}
    for e in emps:
        byfile.setdefault(e['_file'], []).append(e)
    for f, lst in byfile.items():
        print(f'  {f}: {len(lst)}')

    # id 重复
    ids = {}
    for e in emps:
        ids.setdefault(e['id'], []).append(e['_file'])
    dup = {k: v for k, v in ids.items() if len(v) > 1}
    if dup:
        print('\n[重复ID]', dup)

    # 字段缺失
    print('\n[字段缺失]')
    for e in emps:
        miss = [k for k in ('dynasty', 'name', 'templeName', 'reignStart', 'reignEnd', 'events') if k not in e or e[k] in (None, '')]
        if miss:
            print(' ', e.get('id'), miss)

    # 在位区间异常
    print('\n[在位区间异常 reignStart>reignEnd]')
    for e in emps:
        if isinstance(e.get('reignStart'), int) and isinstance(e.get('reignEnd'), int):
            if e['reignStart'] > e['reignEnd']:
                print(' ', e['id'], e['reignStart'], e['reignEnd'])

    # 事件年份越界
    print('\n[事件年份越出在位区间]')
    cnt = 0
    for e in emps:
        rs, re_ = e.get('reignStart'), e.get('reignEnd')
        if not isinstance(rs, int) or not isinstance(re_, int):
            continue
        for ev in e.get('events', []):
            y = ev.get('year')
            if isinstance(y, int) and not (rs - 1 <= y <= re_ + 1):
                cnt += 1
                if cnt <= 60:
                    print(f"  {e['id']}({rs}~{re_}) 事件{ev.get('id')} year={y} 《{ev.get('title')}》")
    print('  越界事件总数:', cnt)

    # 导出总表
    rows = []
    for e in emps:
        rows.append({
            'id': e['id'], 'file': e['_file'], 'dynasty': e.get('dynasty'),
            'name': e.get('name'), 'templeName': e.get('templeName'),
            'rs': e.get('reignStart'), 're': e.get('reignEnd'),
            'tier': e.get('tier'), 'nev': len(e.get('events', [])),
            'civ': e.get('civilization'), 'period': e.get('period'),
        })
    json.dump(rows, open(os.path.join(BASE, 'tools', '_audit_roster.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('\n名录已导出 tools/_audit_roster.json')

if __name__ == '__main__':
    main()
