# -*- coding: utf-8 -*-
"""
Stage 3 master deck — shared schema.

Slide dict keys
---------------
t      : layout type
         title | section | content | two | cards | table | math | code | stats | flow | quote
era     : classical | bridge | deepcnn | data | arch | meta
part    : roman numeral of the part (string) or ""
title   : slide headline
kicker  : small eyebrow line above the headline
lead    : one short paragraph under the headline (optional)
body    : layout-specific payload (see below)
foot    : small caption / caveat under the body (optional)
cite    : source tag string, e.g. "DnCNN17 Table II"
notes   : speaker notes (string)

Payloads
--------
content : {"bullets":[str,...]}  or {"paras":[str,...]}
two     : {"left":{"h":str,"bullets":[...]},"right":{"h":str,"bullets":[...]}}
cards   : {"cards":[{"h":str,"p":str,"tag":str?},...]}
table   : {"cols":[str,...],"rows":[[str,...],...],"hl":[rowidx,...]?,"align":"lrr..."?}
math    : {"eqs":[{"tex":str,"where":str}],"bullets":[...]}   tex = unicode-typeset
code    : {"lang":str,"file":str,"lines":[str,...],"bullets":[...]}
stats   : {"stats":[{"n":str,"l":str,"s":str}],"bullets":[...]}
flow    : {"steps":[{"h":str,"p":str}],"bullets":[...]}
quote   : {"q":str,"attrib":str}
"""

ERA = {
    "meta":      {"name": "",                    "hex": "1B3A4B"},
    "classical": {"name": "I · Classical DIP",   "hex": "8A6D3B"},
    "bridge":    {"name": "II · The bridge",     "hex": "4C6A92"},
    "deepcnn":   {"name": "III · Deep CNN",      "hex": "2E7D6F"},
    "data":      {"name": "IV · Data branch",    "hex": "9A4A62"},
    "arch":      {"name": "V · Architecture",    "hex": "E4572E"},
}

INK      = "14181D"
BODY     = "343B45"
MUTED    = "6B7684"
RULE     = "D8DEE5"
PAPER    = "FFFFFF"
TINT     = "F4F6F8"
DARK     = "10151B"
DARKTINT = "1B222B"
