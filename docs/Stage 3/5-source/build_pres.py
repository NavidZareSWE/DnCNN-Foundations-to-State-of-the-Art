# -*- coding: utf-8 -*-
"""Assemble the 30-minute presentation deck and attach its equation image."""
import json, sys
sys.path.insert(0, '/home/claude/work/deck')
import p_a, p_b

S = p_a.S + p_b.S
master = {s['num']: s for s in json.load(open('deck.json', encoding='utf-8'))}

for i, s in enumerate(S, 1):
    s['num'] = i
    for k in ('part', 'kicker', 'lead', 'foot', 'cite', 'notes'):
        s.setdefault(k, '')
    # reuse the already-typeset y = x + v equation from the master deck
    if s['t'] == 'math':
        src = master[6]['body']['eqs'][0]
        for q in s['body']['eqs']:
            q['latex'] = src['latex']; q['img'] = src['img']
            q['imgw'] = src['imgw']; q['imgh'] = src['imgh']

json.dump(S, open('presentation.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

from collections import Counter
print('slides:', len(S))
print('types :', dict(Counter(s['t'] for s in S)))
hand = next(i for i, s in enumerate(S, 1) if 'Handover' in (s['kicker'] or ''))
print('handover at slide', hand, '→ presenter 1:', hand - 1, 'slides · presenter 2:', len(S) - hand + 1)
missing = [s['num'] for s in S if not s['notes']]
print('slides without notes:', missing or 'none')
