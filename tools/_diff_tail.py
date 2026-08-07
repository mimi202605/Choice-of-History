# -*- coding: utf-8 -*-
"""只看 12-ru / 09-us 两篇的差异（audit_regen_diff 的补充视图）。"""
import runpy, sys, io, os
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
buf = io.StringIO()
old = sys.stdout
sys.stdout = buf
runpy.run_path(os.path.join(HERE, 'audit_regen_diff.py'), run_name='__notmain__')
sys.stdout = old
for line in buf.getvalue().splitlines():
    if '12-ru.json' in line or '09-us.json' in line:
        print(line)
