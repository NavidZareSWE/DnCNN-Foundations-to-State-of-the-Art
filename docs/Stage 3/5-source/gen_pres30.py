# -*- coding: utf-8 -*-
"""Build Presentation_30min.html (the 32-slide condensed talk) from presentation.json,
reusing the master deck's fixed CSS/JS shell so both decks share one visual system."""
import json, html, re, os, base64

BASE = "/home/claude/work"
SRC = os.path.join(BASE, "stage3/Stage3_ImageDenoising/5-source/presentation.json")
STYLE = open(os.path.join(BASE, "figs/fixed_style.css"), encoding="utf-8").read()
SCRIPT_TMPL = open(os.path.join(BASE, "figs/fixed_script.js"), encoding="utf-8").read()
EQ_DATAURI = open(os.path.join(BASE, "figs/eq_6_0_datauri.txt"), encoding="utf-8").read().strip()
OUT = os.path.join(BASE, "stage3/Stage3_ImageDenoising/2-presentation/Presentation_30min.html")

S = json.load(open(SRC, encoding="utf-8"))

ERA = {
 "meta":      ("",              "#14343F", 2007, 2025),
 "classical": ("CLASSICAL DIP", "#7C5E2A", 2007, 2014),
 "bridge":    ("THE BRIDGE",    "#2F5470", 2012, 2017),
 "deepcnn":   ("DEEP CNN",      "#1C6151", 2016, 2018),
 "data":      ("DATA BRANCH",   "#7E3247", 2018, 2025),
 "arch":      ("ARCHITECTURE",  "#C0451A", 2021, 2024),
}
SPAN = 2025 - 2007

def esc(t):
    return html.escape(str(t), quote=False)

def md(t):
    t = esc(t)
    t = re.sub(r'\*\*(.+?)\*\*', lambda m: '<b>' + m.group(1).replace('`', '') + '</b>', t, flags=re.S)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*([^*\n]+)\*', r'<i>\1</i>', t)
    t = re.sub(r'\^(\d+)\^', r'<span class="cref">[\1]</span>', t)
    return t

def ul(items, cls="b"):
    return '<ul class="%s">%s</ul>' % (cls, ''.join('<li>%s</li>' % md(i) for i in items))

def cite_line(s):
    cl = s.get('citeN')
    if cl:
        return '&emsp;'.join('<span class="cref">[%d]</span> %s' % (i + 1, esc(part))
                              for i, part in enumerate(cl))
    return md(s['cite'])

FIGDIR = os.path.join(BASE, "figs/final")
_mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}
def b64img(fname):
    ext = os.path.splitext(fname)[1].lower()
    data = open(os.path.join(FIGDIR, fname), "rb").read()
    return "data:%s;base64,%s" % (_mime[ext], base64.b64encode(data).decode())

FIGS = {
 6:  ("BM3D.jpg", "Block matching in practice: the reference patch R and the similar patches BM3D groups with it before collaborative 3-D filtering. [BM3D07 · Fig. 2]"),
 10: ("TNRD.png", "The diffusion network unrolled as a feed-forward graph: learned filters, trainable nonlinearity and reaction force applied at every stage. [TNRD16/17 · Fig. 1]"),
 11: ("DnCNN.png", "The DnCNN architecture: Conv(+BN)+ReLU layers predict the residual noise, not the clean image. [DnCNN17 · Fig. 1]"),
 17: ("N2N.png", "Noise2Noise's own result: training on noisy targets (orange) tracks clean-target training (blue) almost exactly. [N2N18 · Fig. 1]"),
 18: ("N2V.png", "Traditional, Noise2Noise and Noise2Void training schemes side by side, with N2V's single-image blind-spot result on the right. [N2V19 · Fig. 1]"),
 19: ("P2N.png", "The information-lossy barrier made visible: ZS-N2N, MASH and ATBSN all lose fine structure that P2N's renoise-and-agree supervision keeps. [P2N25 · Fig. 2]"),
 21: ("MambaIR.png", "Effective receptive field: CNNs stay tightly local, Transformers spread further, the Mamba-based backbone activates the widest field. [MambaIR24 · Fig. 1]"),
 23: ("NAFNet.png", "The lineage NAFNet derives in one figure: the transformer block simplified step by step down to SimpleGate and SCA. [NAFNet22 · Fig. 3]"),
 24: ("SCUNet.png", "The Swin-Conv-UNet pipeline: swin-conv blocks combine local and non-local modelling on the way down and back up a UNet backbone. [SCUNet23 · Fig. 1]"),
}

P = []
A = P.append

def slide_open(s):
    era, hexv, fr, to = ERA.get(s['era'], ERA['meta'])
    A('<section class="sl %s" id="s%d" style="--era:%s">' % (s['t'], s['num'], hexv))
    if s['t'] not in ('title', 'section'):
        A('<div class="rail"><div class="folio">%02d</div>%s</div>'
          % (s['num'], ('<div class="eralbl">%s</div>' % esc(era)) if era else ''))

def chrome(s):
    era, hexv, fr, to = ERA.get(s['era'], ERA['meta'])
    if s['t'] not in ('title', 'section', 'quote'):
        left = (fr - 2007) / SPAN * 100.0
        wdt = (to - fr) / SPAN * 100.0
        seg = ('<i style="left:%.2f%%;width:%.2f%%"></i>' % (left, wdt)) if era else ''
        ticks = "".join('<u style="left:%.2f%%"><b>%d</b></u>' % ((y - 2007) / SPAN * 100.0, y)
                        for y in (2007, 2014, 2017, 2022, 2025))
        A('<div class="cite">%s</div><div class="spine">%s%s</div>' % (cite_line(s), seg, ticks))
    else:
        A('<div class="cite">%s</div>' % cite_line(s))
    if s['notes']:
        A('<div class="notes"><b>Speaker notes.</b> %s</div>' % md(s['notes']))
    A('</section>')

def headblock(s):
    if s['kicker']: A('<div class="kick">%s</div>' % esc(s['kicker']).upper())
    A('<h2>%s</h2>' % md(s['title']))
    if s['lead']: A('<p class="lead">%s</p>' % md(s['lead']))

def footblock(s):
    if s['foot']: A('<div class="foot">%s</div>' % md(s['foot']))

def maybe_fig(s):
    fig = FIGS.get(s['num'])
    if not fig:
        return
    fname, cap = fig
    uri = b64img(fname)
    alt = cap.split(" [")[0]
    A('<div class="figband"><img src="%s" alt="%s"><div class="figcap">%s</div></div>' % (uri, esc(alt), cap))

for s in S:
    t = s['t']; b = s['body']
    slide_open(s)

    if t == 'title':
        A('<div class="kick accent">%s</div>' % esc(s['kicker']).upper())
        A('<h1>%s</h1>' % esc(s['title']).replace('\n', '<br>'))
        A('<p class="lede">%s</p>' % md(s['lead']))
        A('<div class="metagrid metagrid5">')
        for k, v in b['meta']:
            A('<div><b>%s</b>%s</div>' % (esc(k).upper(), esc(v).replace('\n', '<br>')))
        A('</div>')

    elif t == 'section':
        A('<div class="secL"><div class="ghost">%s</div><div class="rule"></div>'
          '<h1 class="sec">%s</h1><div class="kick">%s</div></div>'
          % (esc(s['part']), md(s['title']), esc(s['kicker']).upper()))
        A('<div class="secR"><div class="kick">In this part</div><div class="seclist">%s</div>'
          '<p class="lede">%s</p></div>'
          % ("".join('<div><s>%02d</s><span>%s</span></div>' % (i + 1, md(x))
                     for i, x in enumerate(b['items'])), md(s['lead'])))

    elif t == 'quote':
        A('<div class="kick accent">%s</div>' % esc(s['kicker']).upper())
        A('<h1>%s</h1>' % md(s['title']))
        A('<blockquote>%s</blockquote>' %
          ''.join('<p>%s</p>' % md(p) for p in b['q'].split('\n\n')))
        A('<div class="attrib">— %s</div>' % md(b['attrib']))

    elif t == 'content':
        headblock(s); maybe_fig(s)
        A(ul(b.get('bullets') or b.get('paras') or []))
        footblock(s)

    elif t == 'two':
        headblock(s); maybe_fig(s)
        A('<div class="g2">')
        for side in ('left', 'right'):
            c = b[side]
            A('<div class="card"><h4>%s</h4>%s</div>' % (md(c['h']), ul(c['bullets'])))
        A('</div>')
        footblock(s)

    elif t == 'cards':
        headblock(s); maybe_fig(s)
        cols = 2 if len(b['cards']) > 2 else len(b['cards'])
        A('<div class="cards c%d">' % cols)
        for c in b['cards']:
            A('<div class="card">')
            if c.get('tag'): A('<div class="tag">%s</div>' % re.sub(r'[*`]', '', esc(c['tag'])).upper())
            A('<h4>%s</h4><p>%s</p></div>' % (md(c['h']), md(c['p'])))
        A('</div>')
        footblock(s)

    elif t == 'table':
        headblock(s); maybe_fig(s)
        align = b.get('align', 'l' * len(b['cols']))
        hl = set(b.get('hl', []))
        A('<div class="tw"><table><thead><tr>')
        for j, c in enumerate(b['cols']):
            A('<th class="%s">%s</th>' % ('r' if align[j] == 'r' else 'l', md(c)))
        A('</tr></thead><tbody>')
        for i, r in enumerate(b['rows']):
            A('<tr class="%s">' % ('hl' if i in hl else ''))
            for j, cell in enumerate(r):
                A('<td class="%s">%s</td>' % ('r' if align[j] == 'r' else 'l', md(cell)))
            A('</tr>')
        A('</tbody></table></div>')
        footblock(s)

    elif t == 'math':
        headblock(s); maybe_fig(s)
        for eq in b['eqs']:
            if eq.get('img'):
                wem = eq['imgw'] / 200.0 * 72.0 / 19.0
                A('<div class="eq"><div class="tex"><img alt="%s" title="%s" src="%s" '
                  'style="width:%.2fem;max-width:100%%"></div>'
                  % (esc(eq.get('latex', eq['tex'])), esc(eq.get('latex', eq['tex'])),
                     EQ_DATAURI, wem))
            else:
                A('<div class="eq"><div class="tex">%s</div>' % esc(eq['tex']))
            if eq.get('where'): A('<div class="where">%s</div>' % md(eq['where']))
            A('</div>')
        if b.get('bullets'): A(ul(b['bullets']))
        footblock(s)

    elif t == 'code':
        headblock(s); maybe_fig(s)
        A('<div class="g-code"><div class="codebox"><div class="fname">%s</div><pre>' % esc(b['file']))
        for L in b['lines']:
            cls = ' class="cm"' if (L.strip().startswith('#') or '←' in L) else ''
            A('<span%s>%s</span>' % (cls, esc(L) if L else '&nbsp;'))
        A('</pre></div><div class="codenotes">%s</div></div>' % ul(b['bullets']))
        footblock(s)

    elif t == 'stats':
        headblock(s); maybe_fig(s)
        A('<div class="stats c%d">' % len(b['stats']))
        for v in b['stats']:
            A('<div class="card"><div class="big">%s</div><div class="lab">%s</div><p>%s</p></div>'
              % (esc(v['n']), md(v['l']), md(v['s'])))
        A('</div>')
        A(ul(b['bullets']))
        footblock(s)

    elif t == 'flow':
        headblock(s); maybe_fig(s)
        A('<div class="flow">')
        for i, p in enumerate(b['steps'], 1):
            A('<div class="step"><div class="n">%d</div><div class="h">%s</div><div class="p">%s</div></div>'
              % (i, md(p['h']), md(p['p'])))
        A('</div>')
        if b.get('bullets'): A(ul(b['bullets']))
        footblock(s)

    chrome(s)

BODY = '\n'.join(P)

NAV = []
for s in S:
    if s['t'] in ('title', 'section'):
        NAV.append('<div class="nv part" data-go="%d">%s</div>' % (s['num'], esc(s['title'].replace('\n', ' '))))
    else:
        NAV.append('<div class="nv" data-go="%d"><span>%02d</span>%s</div>'
                   % (s['num'], s['num'], esc(re.sub(r'\*\*|`|\*', '', s['title']))))
NAVHTML = ''.join(NAV)

SCRIPT = SCRIPT_TMPL.replace('const N=100;', 'const N=%d;' % len(S))
assert 'const N=%d;' % len(S) in SCRIPT, "N substitution failed — check fixed_script.js literal"

DOC = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Image Denoising — The 30-Minute Talk · Stage 3</title>
<style>%s</style></head><body>
<div id="bar"><b>Stage 3 · 30-Minute Talk</b>
<button id="bNav">Contents (m)</button>
<button id="bNotes">Speaker notes (n)</button>
<button id="bPrint">Print / PDF</button>
<span style="flex:1"></span><span id="pos">1 / %d</span></div>
<div id="nav">%s</div>
<div id="prog"></div>
<div id="deck">%s</div>
<script>%s</script></body></html>""" % (STYLE, len(S), NAVHTML, BODY, SCRIPT)

open(OUT, "w", encoding="utf-8").write(DOC)
print("wrote", OUT, len(DOC), "bytes;", len(S), "slides")
