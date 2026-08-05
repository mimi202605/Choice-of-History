import json, glob, os

files = sorted(glob.glob("data/emperors/*.json"))
for f in files:
    with open(f, encoding="utf-8") as fh:
        data = json.load(fh)
    emps = data.get("emperors", [])
    print(f"\n=== {os.path.basename(f)} ===")
    print(f"  group: {data.get('group')}")
    print(f"  dynasties: {data.get('dynasties')}")
    print(f"  emperor count: {len(emps)}")
    short_bg = [e['name'] for e in emps if len(e.get('background','')) < 40]
    empty_bg = [e['name'] for e in emps if not e.get('background','').strip()]
    no_ev = [e['name'] for e in emps if not e.get('events')]
    few_ev = [e['name'] for e in emps if len(e.get('events',[])) < 3]
    no_era = [e['name'] for e in emps if not e.get('eraContext','').strip()]
    print(f"  empty background: {empty_bg}")
    print(f"  short background(<40): {short_bg}")
    print(f"  empty events: {no_ev}")
    print(f"  events<3: {few_ev}")
    print(f"  empty eraContext: {no_era}")
