# -*- coding: utf-8 -*-
"""Builds oral-exam.html — a single-file, dark-mode interactive study site."""
import sys, io, re, html, json
sys.path.insert(0, '/home/claude/work/deck')
import qa_a, qa_b

BANK = qa_a.BANK + qa_b.BANK

CATS = [
    ("A", "Direct assignment", "Questions the brief itself demands answers to."),
    ("B", "Conceptual & theoretical", "Mathematics, algorithms, assumptions, trade-offs."),
    ("C", "Code & implementation", "What the repositories actually contain, and why."),
    ("D", "Experiments & results", "Reading tables, defending measurements, sources of error."),
]

SECTIONS = [
    ("The problem", ["deg-model", "awgn", "illposed", "map", "psnr", "ssim"]),
    ("Classical era", ["averaging", "nss", "bm3d", "wnnm", "tv"]),
    ("DnCNN — the anchor", ["residual", "rlbn", "depth17", "dncnn3"]),
    ("The data branch", ["n2n", "n2v", "zsn2n", "p2n"]),
    ("The architecture branch", ["attention-cost", "mdta", "nafnet", "scunet-mamba"]),
    ("Engineering & code", ["code-prior", "frameworks", "padding"]),
    ("Results & defence", ["bench-table", "bsd68-ladder", "sidd", "urban100"]),
    ("Assignment & meta", ["narrative", "sources", "limitations", "deploy"]),
]

BY = {q["id"]: q for q in BANK}
ORDER = [i for _, ids in SECTIONS for i in ids]
missing = [q["id"] for q in BANK if q["id"] not in ORDER]
assert not missing, "unsectioned: %s" % missing


# ───────────────── markdown → HTML, with math protected ─────────────────
def is_block(lines, i):
    L = lines[i]
    if L.strip().startswith("```"):
        return True
    if L.strip().startswith("> "):
        return True
    if re.match(r'^\s*[-*]\s+', L) or re.match(r'^\s*\d+\.\s+', L):
        return True
    if L.strip().startswith("|") and i + 1 < len(lines) \
       and re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i + 1]):
        return True
    return False


def md(text):
    if not text:
        return ""
    store = []

    def stash(m):
        store.append(m.group(0))
        return "\x00%d\x00" % (len(store) - 1)

    t = re.sub(r'\\\[.*?\\\]|\\\(.*?\\\)', stash, text, flags=re.S)
    t = html.escape(t, quote=False)

    out, i = [], 0
    lines = t.split("\n")
    while i < len(lines):
        L = lines[i]
        if L.strip().startswith("```"):
            body = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i]); i += 1
            i += 1
            out.append("<pre class='code'>%s</pre>" % "\n".join(body))
            continue
        if L.strip().startswith("|") and i + 1 < len(lines) and re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i + 1]):
            hdr = [c.strip() for c in L.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            th = "".join("<th>%s</th>" % inline(c) for c in hdr)
            tb = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r) for r in rows)
            out.append("<div class='tw'><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (th, tb))
            continue
        if L.strip().startswith("> "):
            body = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                body.append(lines[i].strip()[2:]); i += 1
            out.append("<blockquote>%s</blockquote>" % inline(" ".join(body)))
            continue
        if re.match(r'^\s*[-*]\s+', L):
            items = []
            while i < len(lines) and re.match(r'^\s*[-*]\s+', lines[i]):
                items.append(re.sub(r'^\s*[-*]\s+', '', lines[i])); i += 1
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % inline(x) for x in items))
            continue
        if re.match(r'^\s*\d+\.\s+', L):
            items = []
            while i < len(lines) and re.match(r'^\s*\d+\.\s+', lines[i]):
                items.append(re.sub(r'^\s*\d+\.\s+', '', lines[i])); i += 1
            out.append("<ol>%s</ol>" % "".join("<li>%s</li>" % inline(x) for x in items))
            continue
        if not L.strip():
            i += 1
            continue
        para = [L]
        i += 1                      # always consume at least one line
        while i < len(lines) and lines[i].strip() and not is_block(lines, i):
            para.append(lines[i]); i += 1
        out.append("<p>%s</p>" % inline(" ".join(para)))
    res = "".join(out)
    for k, v in enumerate(store):
        res = res.replace("\x00%d\x00" % k, v)
    return res


def inline(s):
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'<em>\1</em>', s)
    return s


def esc(s):
    return html.escape(str(s), quote=True)


# ───────────────── build cards ─────────────────
cards, nav = [], []
n = 0
for sec_name, ids in SECTIONS:
    nav.append("<div class='navsec'>%s</div>" % esc(sec_name))
    cards.append("<h2 class='sechead' id='sec-%s'>%s</h2>" % (esc(sec_name.replace(' ', '-')), esc(sec_name)))
    for qid in ids:
        q = BY[qid]
        n += 1
        cat = q["cat"]
        blob = " ".join([q["q"], q["a"], q["intuition"], " ".join(q["concepts"]),
                         " ".join(f[0] for f in q["follows"]), q["path"]])
        blob = re.sub(r'<[^>]+>|\\[\(\)\[\]]', ' ', blob)
        blob = re.sub(r'[*`|#]+', ' ', blob)
        blob = re.sub(r'\s+', ' ', blob).lower()

        follows = "".join(
            "<details class='fu'><summary>%s</summary><div class='fub'>%s</div></details>"
            % (esc(f[0]), md(f[1])) for f in q["follows"])
        mis = "".join(
            "<div class='mis'><div class='mis-h'>%s</div>"
            "<div class='mis-b'><p><span class='lbl bad'>Why it is wrong</span> %s</p>"
            "<p><span class='lbl good'>Correct</span> %s</p></div></div>"
            % (inline(esc(m[0])), inline(esc(m[1])), inline(esc(m[2]))) for m in q["miscon"])

        cards.append("""
<article class="q" id="q-{qid}" data-cat="{cat}" data-n="{n}" data-hard="{hard}" data-s="{blob}">
 <header class="qh">
  <div class="qmeta"><span class="badge c{cat}">{cat}</span><span class="path">{path}</span>
   {hardtag}<span class="qn">Q{n}</span></div>
  <h3 class="qt">{qt}</h3>
  <div class="qact">
   <button class="reveal">Show answer</button>
   <label class="done"><input type="checkbox" class="ck"> Got it</label>
  </div>
 </header>
 <div class="qbody">
  <section class="blk"><h4>Answer</h4>{a}</section>
  <section class="blk int"><h4>Intuition</h4>{intu}</section>
  <section class="blk"><h4>Key concepts</h4><div class="chips">{chips}</div></section>
  {fublk}
  {misblk}
 </div>
</article>""".format(
            qid=esc(qid), cat=cat, n=n, hard="1" if q["hard"] else "0", blob=esc(blob),
            path=esc(q["path"]),
            hardtag="<span class='badge hot'>often misunderstood</span>" if q["hard"] else "",
            qt=inline(esc(q["q"])), a=md(q["a"]), intu=md(q["intuition"]),
            chips="".join("<span class='chip'>%s</span>" % esc(c) for c in q["concepts"]),
            fublk=("<section class='blk'><h4>Likely follow-ups</h4>"
                   "<p class='hint'>Answers are hidden — try to answer aloud first.</p>%s</section>" % follows) if follows else "",
            misblk=("<section class='blk'><h4>Common misconceptions</h4>%s</section>" % mis) if mis else ""))
        nav.append("<div class='nv' data-go='q-%s'><span>%02d</span>%s</div>" % (esc(qid), n, esc(q["q"])))

TOTAL = n

CSS = """
:root{--bg:#0E1216;--surf:#151B21;--surf2:#1B222A;--line:#252E38;--line2:#2F3A45;
--tx:#E4EAF0;--tx2:#AFBBC7;--tx3:#7E8B98;--acc:#E8734A;--acc2:#5BA6D6;--ok:#4FB286;--bad:#D9636B;
--mono:Consolas,"SF Mono",Menlo,monospace}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--tx);
font:17.5px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
-webkit-font-smoothing:antialiased}
h1,h2,h3,h4{margin:0;line-height:1.25}
code{font-family:var(--mono);font-size:.9em;background:#20272F;color:#9CD0E8;overflow-wrap:anywhere;word-break:break-word;
padding:1px 5px;border-radius:3px}
pre.code{font-family:var(--mono);font-size:13.5px;line-height:1.55;background:#11161B;
border:1px solid var(--line);border-radius:6px;padding:14px 16px;overflow-x:auto;color:#CFDAE4}
a{color:var(--acc2)}

/* top bar */
header#bar{position:fixed;inset:0 0 auto 0;height:60px;z-index:60;background:rgba(14,18,22,.96);
backdrop-filter:blur(8px);border-bottom:1px solid var(--line);display:flex;align-items:center;
gap:12px;padding:0 16px}
#bar .brand{font-weight:700;font-size:15px;white-space:nowrap}
#bar .brand small{display:block;font-weight:400;font-size:11px;color:var(--tx3)}
#search{flex:1;min-width:120px;max-width:440px;background:var(--surf2);border:1px solid var(--line2);
border-radius:7px;color:var(--tx);padding:9px 13px;font:inherit;font-size:14px}
#search:focus{outline:2px solid var(--acc);outline-offset:1px}
.btn{background:var(--surf2);border:1px solid var(--line2);color:var(--tx2);border-radius:7px;
padding:8px 13px;font:inherit;font-size:13.5px;cursor:pointer;white-space:nowrap}
.btn:hover{background:#232C35;color:var(--tx)}
.btn.on{background:var(--acc);border-color:var(--acc);color:#12171C;font-weight:600}
#prog{position:fixed;top:60px;left:0;right:0;height:3px;background:var(--line);z-index:59}
#prog i{display:block;height:100%;width:0;background:var(--acc);transition:width .25s}

/* layout */
#wrap{display:grid;grid-template-columns:296px minmax(0,1fr);gap:0;padding-top:63px}
#side{position:sticky;top:63px;height:calc(100vh - 63px);overflow-y:auto;
border-right:1px solid var(--line);padding:16px 0 60px;background:#101519}
.navsec{padding:14px 18px 6px;font-size:11px;letter-spacing:1.4px;text-transform:uppercase;
color:var(--acc);font-weight:700}
.nv{padding:7px 18px;font-size:13px;color:var(--tx2);cursor:pointer;display:flex;gap:10px;line-height:1.4}
.nv span{color:var(--tx3);min-width:22px;font-variant-numeric:tabular-nums}
.nv:hover{background:var(--surf2);color:var(--tx)}
.nv.done span{color:var(--ok)}
main{padding:26px 34px 120px;max-width:1000px}
.hero{background:var(--surf);border:1px solid var(--line);border-left:4px solid var(--acc);
border-radius:8px;padding:24px 28px;margin-bottom:26px}
.hero h1{font-size:26px;margin-bottom:10px}
.hero p{color:var(--tx2);font-size:15px;margin:0 0 10px}
.hero ul{color:var(--tx2);font-size:14.5px;margin:10px 0 0;padding-left:20px}
.sechead{font-size:13px;letter-spacing:1.6px;text-transform:uppercase;color:var(--acc);
margin:36px 0 16px;padding-bottom:9px;border-bottom:1px solid var(--line)}

/* question card */
.q{background:var(--surf);border:1px solid var(--line);border-radius:9px;margin-bottom:16px;
overflow:hidden}
.q.hide{display:none}
.q[data-hard="1"]{border-left:3px solid var(--acc)}
.qh{padding:18px 22px}
.qmeta{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin-bottom:9px}
.badge{font-size:10.5px;font-weight:700;letter-spacing:.9px;padding:3px 8px;border-radius:4px;
text-transform:uppercase}
.cA{background:#2A3A4A;color:#9CC9EA}.cB{background:#2C3A31;color:#93D3B0}
.cC{background:#3A3350;color:#BDAEE8}.cD{background:#3F3428;color:#E5BE8C}
.badge.hot{background:#4A2A24;color:#F0A88C}
.path{font-size:12px;color:var(--tx3)}
.qn{margin-left:auto;font-size:12px;color:var(--tx3);font-variant-numeric:tabular-nums}
.qt{font-size:21px;font-weight:600;margin-bottom:14px}
.qact{display:flex;align-items:center;gap:14px}
.done{font-size:13px;color:var(--tx3);display:flex;align-items:center;gap:6px;cursor:pointer}
.done input{accent-color:var(--ok);width:15px;height:15px;cursor:pointer}
.q.ok .qt{color:var(--tx2)}
.q.ok{border-color:#27402F}
.qbody{display:none;padding:0 22px 22px;border-top:1px solid var(--line)}
.q.open .qbody{display:block}
.blk{margin-top:20px}
.blk h4{font-size:11.5px;letter-spacing:1.4px;text-transform:uppercase;color:var(--acc);
margin-bottom:9px}
.blk.int{background:var(--surf2);border-radius:7px;padding:15px 18px;border-left:3px solid var(--acc2)}
.blk.int h4{color:var(--acc2)}
.blk p{margin:0 0 11px;color:var(--tx2)}
.blk p:last-child{margin-bottom:0}
.blk strong{color:var(--tx)}
.blk ul,.blk ol{color:var(--tx2);margin:0 0 11px;padding-left:22px}
.blk li{margin-bottom:6px}
blockquote{margin:0 0 12px;padding:12px 18px;background:var(--surf2);border-left:3px solid var(--acc);
border-radius:0 6px 6px 0;color:var(--tx);font-size:17px}
.chips{display:flex;flex-wrap:wrap;gap:7px}
.chip{background:var(--surf2);border:1px solid var(--line2);color:var(--tx2);font-size:12.5px;
padding:4px 10px;border-radius:20px}
.hint{font-size:12.5px;color:var(--tx3);margin:-4px 0 10px}
details.fu{background:var(--surf2);border:1px solid var(--line);border-radius:7px;margin-bottom:9px}
details.fu summary{cursor:pointer;padding:11px 15px;font-size:16px;color:var(--tx);
list-style:none;font-weight:500}
details.fu summary::-webkit-details-marker{display:none}
details.fu summary:before{content:"▸ ";color:var(--acc)}
details.fu[open] summary:before{content:"▾ "}
details.fu[open] summary{border-bottom:1px solid var(--line)}
.fub{padding:13px 15px;font-size:16px;color:var(--tx2)}
.fub p{margin:0}
.mis{background:#1D1618;border:1px solid #3A282C;border-radius:7px;margin-bottom:10px;overflow:hidden}
.mis-h{padding:11px 15px;font-size:16px;color:#F0A8A8;font-weight:600;background:#231A1D}
.mis-b{padding:12px 15px;font-size:16px;color:var(--tx2)}
.mis-b p{margin:0 0 9px}.mis-b p:last-child{margin:0}
.lbl{font-size:10.5px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;
padding:2px 7px;border-radius:3px;margin-right:7px}
.lbl.bad{background:#40262A;color:#F0A8A8}.lbl.good{background:#23402F;color:#8FD9B4}
.tw{overflow-x:auto;margin:0 0 12px}
table{border-collapse:collapse;width:100%;font-size:14px}
th{background:var(--surf2);color:var(--tx);text-align:left;padding:9px 12px;font-weight:600;
border-bottom:1px solid var(--line2);font-size:13px}
td{padding:8px 12px;border-bottom:1px solid var(--line);color:var(--tx2)}
.katex{font-size:1.04em}
.katex-display{margin:.7em 0;overflow-x:auto;overflow-y:hidden;padding:2px 0}
#mathwarn{display:none;background:#2A1E19;border:1px solid #4A3227;border-radius:8px;
padding:12px 16px;margin-bottom:18px;color:#EBC3AE;font-size:13.5px}
body.nomath .blk p,body.nomath .fub p{word-break:break-word}
#empty{display:none;color:var(--tx3);padding:40px 0;text-align:center;font-size:15px}
#examhead{display:none;background:#2A1E19;border:1px solid #4A3227;border-radius:8px;
padding:16px 20px;margin-bottom:20px;color:#EBC3AE;font-size:14.5px}
body.exam #examhead{display:block}
#toTop{position:fixed;right:22px;bottom:22px;z-index:40}
@media(max-width:920px){
 #wrap{grid-template-columns:minmax(0,1fr)}
 #side{position:fixed;left:0;top:63px;width:288px;z-index:55;transform:translateX(-100%);
 transition:.2s;border-right:1px solid var(--line)}
 body.nav #side{transform:none}
 main{padding:20px 16px 100px}
 #bar .brand small{display:none}
}
@media(min-width:921px){#menu{display:none}}
"""

JS = """
const TOTAL=%d;
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const main=$('#list'), cards=()=>$$('.q');

/* progress, persisted locally */
let done=new Set(JSON.parse(localStorage.getItem('oralDone')||'[]'));
function paint(){
  cards().forEach(c=>{
    const id=c.id, ck=c.querySelector('.ck');
    const d=done.has(id); ck.checked=d; c.classList.toggle('ok',d);
    const nv=document.querySelector(`.nv[data-go="${id}"]`); if(nv)nv.classList.toggle('done',d);
  });
  const pct=TOTAL?Math.round(done.size/TOTAL*100):0;
  $('#prog i').style.width=pct+'%%';
  $('#pct').textContent=done.size+' / '+TOTAL+'  ·  '+pct+'%%';
}
main.addEventListener('change',e=>{
  if(!e.target.classList.contains('ck'))return;
  const c=e.target.closest('.q');
  e.target.checked?done.add(c.id):done.delete(c.id);
  localStorage.setItem('oralDone',JSON.stringify([...done])); paint();
});

/* reveal */
main.addEventListener('click',e=>{
  const b=e.target.closest('.reveal'); if(!b)return;
  const c=b.closest('.q'); const open=c.classList.toggle('open');
  b.textContent=open?'Hide answer':'Show answer';
});
$('#expand').onclick=()=>{
  const any=cards().some(c=>!c.classList.contains('open')&&!c.classList.contains('hide'));
  cards().forEach(c=>{ if(c.classList.contains('hide'))return;
    c.classList.toggle('open',any);
    c.querySelector('.reveal').textContent=any?'Hide answer':'Show answer'; });
};

/* search + category filter */
let cat='all';
function filt(){
  const t=$('#search').value.trim().toLowerCase();
  let shown=0;
  cards().forEach(c=>{
    const okCat = cat==='all' || (cat==='hard'? c.dataset.hard==='1' : c.dataset.cat===cat);
    const okTxt = !t || c.dataset.s.includes(t);
    const vis=okCat&&okTxt; c.classList.toggle('hide',!vis); if(vis)shown++;
  });
  $$('.sechead').forEach(h=>{
    let sib=h.nextElementSibling,any=false;
    while(sib&&!sib.classList.contains('sechead')){
      if(sib.classList.contains('q')&&!sib.classList.contains('hide'))any=true;
      sib=sib.nextElementSibling;}
    h.style.display=any?'':'none';
  });
  $('#empty').style.display=shown?'none':'block';
}
$('#search').addEventListener('input',filt);
$$('.fbtn').forEach(b=>b.onclick=()=>{
  cat=b.dataset.f; $$('.fbtn').forEach(x=>x.classList.toggle('on',x===b)); filt();
});

/* exam simulator: shuffle order, collapse everything */
let examOn=false, original=null;
$('#exam').onclick=()=>{
  examOn=!examOn;
  document.body.classList.toggle('exam',examOn);
  $('#exam').classList.toggle('on',examOn);
  $('#exam').textContent=examOn?'Exit exam mode':'Exam simulator';
  if(examOn){
    if(!original) original=[...main.children];
    $$('.sechead').forEach(h=>h.style.display='none');
    const qs=cards().filter(c=>!c.classList.contains('hide'));
    for(let i=qs.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));
      main.insertBefore(qs[i],qs[j]);}
    cards().forEach(c=>{c.classList.remove('open');
      c.querySelector('.reveal').textContent='Show answer';});
    $$('details.fu').forEach(d=>d.open=false);
    window.scrollTo({top:0,behavior:'smooth'});
  } else {
    original.forEach(n=>main.appendChild(n)); filt();
  }
};
$('#reshuffle').onclick=()=>{ if(examOn){$('#exam').click();$('#exam').click();} };

/* nav */
$$('.nv').forEach(e=>e.onclick=()=>{
  const t=document.getElementById(e.dataset.go);
  if(t){t.scrollIntoView({block:'start'});document.body.classList.remove('nav');}
});
$('#menu').onclick=()=>document.body.classList.toggle('nav');
$('#toTop').onclick=()=>window.scrollTo({top:0,behavior:'smooth'});
$('#reset').onclick=()=>{ if(confirm('Clear all progress?')){done=new Set();
  localStorage.setItem('oralDone','[]'); paint();} };

/* keyboard */
document.addEventListener('keydown',e=>{
  if(e.target.tagName==='INPUT')return;
  if(e.key==='/'){e.preventDefault();$('#search').focus();}
  if(e.key==='e')$('#exam').click();
  if(e.key==='a')$('#expand').click();
});
paint(); filt();

/* KaTeX — optional. If the CDN is unreachable the page still works and the
   LaTeX source stays readable, so nothing is lost offline. */
function renderMath(){
  if(window.__katexFailed || !window.katex || !window.renderMathInElement){
    document.body.classList.add('nomath');
    const n=document.getElementById('mathwarn'); if(n)n.style.display='block';
    return;
  }
  try{
    renderMathInElement(document.body,{delimiters:[
      {left:'\\\\[',right:'\\\\]',display:true},
      {left:'\\\\(',right:'\\\\)',display:false}],throwOnError:false});
  }catch(err){
    console.warn('KaTeX render skipped:',err);
    document.body.classList.add('nomath');
    const n=document.getElementById('mathwarn'); if(n)n.style.display='block';
  }
}
/* Chain-load: auto-render is injected only once katex itself is confirmed present,
   because auto-render dereferences katex the moment it evaluates. */
(function loadKatex(){
  const CDN='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/';
  function inject(src,ok,fail){
    const t=document.createElement('script');
    t.src=src; t.onload=ok; t.onerror=fail; document.head.appendChild(t);
  }
  function fail(){ window.__katexFailed=1; renderMath(); }
  inject(CDN+'katex.min.js', function(){
    if(!window.katex) return fail();
    inject(CDN+'contrib/auto-render.min.js', renderMath, fail);
  }, fail);
})();
""" % TOTAL

FILTERS = "".join(
    "<button class='btn fbtn' data-f='%s'>%s</button>" % (c, n)
    for c, n, _ in CATS)

DOC = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Oral Exam Preparation — Image Denoising · Stage 3</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<style>%s</style></head><body>

<header id="bar">
 <button class="btn" id="menu">☰</button>
 <div class="brand">Oral Exam Prep<small>Image denoising · Stage 3 defence</small></div>
 <input id="search" placeholder="Search concept, topic, keyword…   ( / )">
 <button class="btn fbtn on" data-f="all">All</button>
 %s
 <button class="btn fbtn" data-f="hard">Tricky</button>
 <button class="btn" id="expand">Expand all (a)</button>
 <button class="btn" id="exam">Exam simulator (e)</button>
 <span id="pct" style="font-size:12.5px;color:#7E8B98;white-space:nowrap"></span>
</header>
<div id="prog"><i></i></div>

<div id="wrap">
 <nav id="side">%s
  <div style="padding:18px">
   <button class="btn" id="reset" style="width:100%%">Reset progress</button>
  </div>
 </nav>
 <main>
  <div class="hero">
   <h1>%d questions, with model answers</h1>
   <p>Built from the Stage 3 master deck, the assignment brief and the twelve Category&nbsp;A papers.
   Every answer is written to be <em>spoken</em>: state the claim, give the mechanism, then the number.</p>
   <ul>
    <li><strong>Structured mode</strong> (default) runs fundamentals → classical → DnCNN → the two branches → code → results → meta.</li>
    <li><strong>Exam simulator</strong> shuffles everything and collapses every answer, so you answer cold.</li>
    <li><strong>Follow-ups are collapsed on purpose.</strong> Answer them aloud before opening.</li>
    <li>Cards marked <span class="badge hot">often misunderstood</span> are the ones examiners probe hardest.</li>
    <li>Progress is saved in this browser only. Nothing leaves the page.</li>
   </ul>
  </div>
  <div id="mathwarn"><strong>Formulas are showing as LaTeX source.</strong>
   KaTeX could not be loaded, which happens offline or behind a firewall. Everything else on this
   page works normally — the mathematics is still readable, just untypeset.</div>
  <div id="examhead"><strong>Exam mode.</strong> Questions are shuffled and answers hidden.
   Speak your answer out loud in full before revealing — fluency under pressure is what is being tested,
   not recall. <button class="btn" id="reshuffle" style="margin-left:10px">Reshuffle</button></div>
  <div id="list">%s</div>
  <div id="empty">No question matches that search.</div>
 </main>
</div>
<button class="btn" id="toTop">↑ Top</button>
<script>%s</script></body></html>""" % (CSS, FILTERS, "".join(nav), TOTAL, "".join(cards), JS)

io.open('/home/claude/work/out/oral-exam.html', 'w', encoding='utf-8').write(DOC)
print("questions:", TOTAL)
print("follow-ups:", sum(len(q["follows"]) for q in BANK))
print("misconceptions:", sum(len(q["miscon"]) for q in BANK))
print("tricky-flagged:", sum(1 for q in BANK if q["hard"]))
print("bytes:", len(DOC))
