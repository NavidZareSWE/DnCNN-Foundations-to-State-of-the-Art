# -*- coding: utf-8 -*-
import json, html, re, io, os, base64

S = json.load(open('/home/claude/work/stage3/Stage3_ImageDenoising/5-source/deck.json', encoding='utf-8'))

ERA = {
 "meta":      ("",              "#14343F", 2007, 2025),
 "classical": ("CLASSICAL DIP", "#7C5E2A", 2007, 2014),
 "bridge":    ("THE BRIDGE",    "#2F5470", 2012, 2017),
 "deepcnn":   ("DEEP CNN",      "#1C6151", 2016, 2018),
 "data":      ("DATA BRANCH",   "#7E3247", 2018, 2025),
 "arch":      ("ARCHITECTURE",  "#C0451A", 2021, 2024),
}
SPAN = 2025 - 2007

EQWEB = '/home/claude/work/out/eq_web'
_eqcache = {}

def eq_data_uri(name):
    """Inline the pdflatex-rendered equation so the deck needs no network at all."""
    if name not in _eqcache:
        with open(os.path.join(EQWEB, name), 'rb') as f:
            _eqcache[name] = 'data:image/png;base64,' + base64.b64encode(f.read()).decode()
    return _eqcache[name]

# ── embedded paper figures (the 12 figband images) ─────────────────────────
FIGDIR = '/home/claude/work/stage3/Stage3_ImageDenoising/5-source/figband_imgs'
try:
    FIGMAP = json.load(open(os.path.join(FIGDIR, 'manifest.json'), encoding='utf-8'))
except FileNotFoundError:
    FIGMAP = {}
_figcache = {}
_figmime = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg'}

def fig_data_uri(fname):
    if fname not in _figcache:
        ext = os.path.splitext(fname)[1].lower()
        with open(os.path.join(FIGDIR, fname), 'rb') as f:
            _figcache[fname] = 'data:%s;base64,%s' % (_figmime.get(ext, 'image/png'),
                                                        base64.b64encode(f.read()).decode())
    return _figcache[fname]


def esc(t):
    return html.escape(str(t), quote=False)

def md(t):
    """**bold**, *italic*, `code`, ^n^ (inline citation marker) -> HTML."""
    t = esc(t)
    t = re.sub(r'\*\*(.+?)\*\*', lambda m: '<b>' + m.group(1).replace('`', '') + '</b>', t, flags=re.S)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*([^*\n]+)\*', r'<i>\1</i>', t)
    t = re.sub(r'\^(\d+)\^', r'<span class="cref">[\1]</span>', t)
    return t

def ul(items, cls="b"):
    return '<ul class="%s">%s</ul>' % (cls, ''.join('<li>%s</li>' % md(i) for i in items))

def cite_line(s):
    """Numbered reference legend for multi-source slides (citeN), else plain cite."""
    cl = s.get('citeN')
    if cl:
        return '&emsp;'.join('<span class="cref">[%d]</span> %s' % (i + 1, esc(part))
                              for i, part in enumerate(cl))
    return md(s['cite'])

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
    fig = FIGMAP.get(str(s['num']))
    if fig:
        A('<div class="figband"><img src="%s" alt="%s"><div class="figcap">%s</div></div>'
          % (fig_data_uri(fig['file']), esc(fig['alt']), md(fig['cap'])))

def footblock(s):
    if s['foot']: A('<div class="foot">%s</div>' % md(s['foot']))

for s in S:
    t = s['t']; b = s['body']
    slide_open(s)

    if t == 'title':
        A('<div class="kick accent">%s</div>' % esc(s['kicker']).upper())
        A('<h1>%s</h1>' % esc(s['title']).replace('\n', '<br>'))
        A('<p class="lede">%s</p>' % md(s['lead']))
        A('<div class="metagrid%s">' % (' metagrid5' if len(b['meta']) == 5 else ''))
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
        headblock(s)
        A(ul(b.get('bullets') or b.get('paras') or []))
        footblock(s)

    elif t == 'two':
        headblock(s)
        A('<div class="g2">')
        for side in ('left', 'right'):
            c = b[side]
            A('<div class="card"><h4>%s</h4>%s</div>' % (md(c['h']), ul(c['bullets'])))
        A('</div>')
        footblock(s)

    elif t == 'cards':
        headblock(s)
        cols = 2 if len(b['cards']) > 2 else len(b['cards'])
        A('<div class="cards c%d">' % cols)
        for c in b['cards']:
            A('<div class="card">')
            if c.get('tag'): A('<div class="tag">%s</div>' % re.sub(r'[*`]','',esc(c['tag'])).upper())
            A('<h4>%s</h4><p>%s</p></div>' % (md(c['h']), md(c['p'])))
        A('</div>')
        footblock(s)

    elif t == 'table':
        headblock(s)
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
        headblock(s)
        for eq in b['eqs']:
            if eq.get('img'):
                # width in em so the equation scales with the surrounding type
                wem = eq['imgw'] / 200.0 * 72.0 / 19.0
                A('<div class="eq"><div class="tex"><img alt="%s" title="%s" src="%s" '
                  'style="width:%.2fem;max-width:100%%"></div>'
                  % (esc(eq.get('latex', eq['tex'])), esc(eq.get('latex', eq['tex'])),
                     eq_data_uri(eq['img']), wem))
            else:
                A('<div class="eq"><div class="tex">%s</div>' % esc(eq['tex']))
            if eq.get('where'): A('<div class="where">%s</div>' % md(eq['where']))
            A('</div>')
        if b.get('bullets'): A(ul(b['bullets']))
        footblock(s)

    elif t == 'code':
        headblock(s)
        A('<div class="g-code"><div class="codebox"><div class="fname">%s</div><pre>' % esc(b['file']))
        for L in b['lines']:
            cls = ' class="cm"' if (L.strip().startswith('#') or '←' in L) else ''
            A('<span%s>%s</span>' % (cls, esc(L) if L else '&nbsp;'))
        A('</pre></div><div class="codenotes">%s</div></div>' % ul(b['bullets']))
        footblock(s)

    elif t == 'stats':
        headblock(s)
        A('<div class="stats c%d">' % len(b['stats']))
        for v in b['stats']:
            A('<div class="card"><div class="big">%s</div><div class="lab">%s</div><p>%s</p></div>'
              % (esc(v['n']), md(v['l']), md(v['s'])))
        A('</div>')
        A(ul(b['bullets']))
        footblock(s)

    elif t == 'flow':
        headblock(s)
        A('<div class="flow">')
        for i, p in enumerate(b['steps'], 1):
            A('<div class="step"><div class="n">%d</div><div class="h">%s</div><div class="p">%s</div></div>'
              % (i, md(p['h']), md(p['p'])))
        A('</div>')
        if b.get('bullets'): A(ul(b['bullets']))
        footblock(s)

    chrome(s)

BODY = '\n'.join(P)

# --- navigation index ---
NAV = []
for s in S:
    if s['t'] in ('title', 'section'):
        NAV.append('<div class="nv part" data-go="%d">%s</div>' % (s['num'], esc(s['title'].replace('\n', ' '))))
    else:
        NAV.append('<div class="nv" data-go="%d"><span>%02d</span>%s</div>'
                   % (s['num'], s['num'], esc(re.sub(r'\*\*|`|\*', '', s['title']))))
NAVHTML = ''.join(NAV)

CSS = open('/home/claude/work/figs/fixed_style.css', encoding='utf-8').read()

JS = """
const N=%d;
const bar=document.getElementById('bar');
function go(n){const el=document.getElementById('s'+n);if(el)el.scrollIntoView({behavior:'smooth',block:'start'});}
document.querySelectorAll('.nv').forEach(e=>e.onclick=()=>{go(+e.dataset.go);document.body.classList.remove('nav');});
document.getElementById('bNav').onclick=()=>document.body.classList.toggle('nav');
document.getElementById('bNotes').onclick=()=>{document.body.classList.toggle('shownotes');
 localStorage.setItem('s3notes',document.body.classList.contains('shownotes')?'1':'0');};
if(localStorage.getItem('s3notes')==='1')document.body.classList.add('shownotes');
document.getElementById('bPrint').onclick=()=>window.print();
let cur=1;
const obs=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){
 cur=+e.target.id.slice(1);document.getElementById('pos').textContent=cur+' / '+N;
 document.getElementById('prog').style.width=(cur/N*100)+'%%';}});},{rootMargin:'-45%% 0px -50%% 0px'});
document.querySelectorAll('.sl').forEach(s=>obs.observe(s));
document.addEventListener('keydown',e=>{
 if(e.target.tagName==='INPUT')return;
 if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){e.preventDefault();go(Math.min(N,cur+1));}
 if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();go(Math.max(1,cur-1));}
 if(e.key==='Home')go(1); if(e.key==='End')go(N);
 if(e.key==='n')document.getElementById('bNotes').click();
 if(e.key==='m')document.getElementById('bNav').click();
});
""" % len(S)

DOC = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Image Denoising — From Foundations to State-of-the-Art · Stage 3 Master Deck</title>
<style>%s</style></head><body>
<div id="bar"><b>Stage 3 · Master Deck</b>
<button id="bNav">Contents (m)</button>
<button id="bNotes">Speaker notes (n)</button>
<button id="bPrint">Print / PDF</button>
<span style="flex:1"></span><span id="pos">1 / %d</span></div>
<div id="nav">%s</div>
<div id="prog"></div>
<div id="deck">%s</div>
<script>%s</script></body></html>""" % (CSS, len(S), NAVHTML, BODY, JS)

io.open('/home/claude/work/out/master-deck.html', 'w', encoding='utf-8').write(DOC)
print("html written:", len(DOC), "bytes,", len(S), "slides")
