# -*- coding: utf-8 -*-
import json, importlib, sys
sys.path.insert(0, '/home/claude/work/deck')

slides = []
for mod in ['c_a', 'c_b', 'c_c', 'c_d', 'c_e', 'c_f', 'c_g']:
    m = importlib.import_module(mod)
    slides.extend(m.S)

for i, s in enumerate(slides, start=1):
    s['num'] = i
    s.setdefault('part', '')
    s.setdefault('kicker', '')
    s.setdefault('lead', '')
    s.setdefault('foot', '')
    s.setdefault('cite', '')
    s.setdefault('notes', '')

json.dump(slides, open('/home/claude/work/deck/deck.json', 'w'), ensure_ascii=False, indent=1)

from collections import Counter
print("TOTAL SLIDES:", len(slides))
print("by type:", dict(Counter(s['t'] for s in slides)))
print("by era :", dict(Counter(s['era'] for s in slides)))
print("by part:", dict(Counter(s['part'] for s in slides)))
missing = [s['num'] for s in slides if not s['notes']]
print("slides without notes:", missing)
