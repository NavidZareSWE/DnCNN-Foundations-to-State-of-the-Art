# -*- coding: utf-8 -*-
"""
Builds companion.html — a per-slide presenter companion for all 100 slides.

Every slide gets: what it communicates · what to say · what the visuals mean ·
presentation cues · transition · timing. Slides 7–11 additionally carry a
hand-written deep-dive. Source attribution (deck HTML vs assignment PDF) is
tracked per slide and shown as a tag.
"""
import json, io, re, html, sys

S = json.load(open('/home/claude/work/stage3/Stage3_ImageDenoising/5-source/deck.json', encoding='utf-8'))
IDX = {s['num']: s for s in S}
WPM = 125.0

ERA = {
 "meta":      ("",                   "#1D3D50"),
 "classical": ("I · Classical DIP",  "#7A5E2E"),
 "bridge":    ("II · The bridge",    "#3D5A85"),
 "deepcnn":   ("III · Deep CNN",     "#1F6B5D"),
 "data":      ("IV · Data branch",   "#8A3A52"),
 "arch":      ("V · Architecture",   "#BF4419"),
}

def e(t): return html.escape(str(t), quote=False)

def clean(t):
    """Strip deck markup and citation brackets for spoken prose."""
    t = re.sub(r'`\[([^\]]+)\]`', r'', t)
    t = t.replace('**', '').replace('`', '')
    t = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'\1', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def md(t):
    t = e(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'<i>\1</i>', t)
    return t

def words(t): return len(clean(t).split())

def mmss(n):
    sec = max(15, int(round(n / WPM * 60 / 5) * 5))
    return "%d:%02d" % (sec // 60, sec % 60), sec

# ─────────────── visuals description, per layout ───────────────
def visuals(s):
    b, t = s['body'], s['t']
    if t == 'title':
        return ("A title slide. The four panels along the bottom are the project's identity card: "
                "anchor paper, source count and split, the structural claim, and the defence date. "
                "They exist so that nobody has to ask those four questions later.")
    if t == 'section':
        return ("A part divider. The large faded numeral on the right is the part number; the list "
                "underneath is what this part will cover, in order. Nothing here needs explaining — "
                "it is a breath between sections.")
    if t == 'quote':
        return ("A full-slide statement with an accent rule down the left. There is nothing to point "
                "at; the slide is the sentence.")
    if t == 'table':
        cols = b['cols']; nr = len(b['rows'])
        hl = b.get('hl', [])
        out = ("A %d-row table with columns for %s." % (nr, ", ".join(clean(c) for c in cols)))
        if hl:
            names = [clean(str(b['rows'][i][0])) for i in hl if i < nr]
            out += " The shaded row%s — %s — %s the row%s the argument rests on." % (
                "s" if len(names) > 1 else "", ", ".join(names),
                "are" if len(names) > 1 else "is", "s" if len(names) > 1 else "")
        if s['foot']:
            out += " The tinted panel under the table is the reading, not more data — that is the sentence to deliver."
        return out
    if t == 'cards':
        n = len(b['cards'])
        tags = [clean(c.get('tag', '')) for c in b['cards'] if c.get('tag')]
        out = "%d panels, read left to right then down." % n
        if tags:
            out += " The small coloured labels — %s — are the spine: they say what each panel is *for*." % ", ".join(tags)
        return out
    if t == 'two':
        return ("Two columns, deliberately opposed: “%s” on the left against “%s” on the right. "
                "The contrast between them is the content; do not read one column and then the other "
                "as if they were separate lists." % (clean(b['left']['h']), clean(b['right']['h'])))
    if t == 'math':
        n = len(b['eqs'])
        return ("%d boxed equation%s, each with a smaller italic line underneath naming every symbol. "
                "The bullets below unpack them. Point at the specific term you are discussing — the "
                "symbol line exists so nobody has to guess what a letter means."
                % (n, "s" if n > 1 else ""))
    if t == 'code':
        return ("A verbatim source listing on the left, taken from %s, with commentary on the right. "
                "The highlighted lines are the ones that carry the claim. Point at the line, not the panel."
                % clean(b['file']))
    if t == 'stats':
        ns = [clean(v['n']) for v in b['stats']]
        return ("%d large figures — %s — each with a label and a one-line source underneath. "
                "These are the numbers to say out loud; everything else on the slide is support."
                % (len(ns), ", ".join(ns)))
    if t == 'flow':
        return ("%d numbered steps stacked vertically, each with a short name on the left and the "
                "explanation on the right. It is a sequence: walk down it, do not jump around."
                % len(b['steps']))
    return "A headline, a lead paragraph and a bulleted argument. The bold openers are the claim of each bullet."

# ─────────────── spoken script ───────────────
def script(s):
    b, t, out = s['body'], s['t'], []
    lead = clean(s['lead']) if s['lead'] else ""
    title = clean(s['title'])

    if t == 'title':
        return ("Good morning. Our topic is image denoising, and our anchor paper is DnCNN — Zhang and "
                "colleagues, IEEE Transactions on Image Processing, 2017. " + lead +
                " Before the contents, I want to state the claim this deck is arguing for, because "
                "everything after it is evidence: four eras, three bottlenecks, and one fork in 2018 "
                "that has never closed.")
    if t == 'section':
        return ("Part %s. %s. %s We will cover %s." % (
            s['part'], title, lead,
            ", then ".join(clean(i) for i in b['items'][:4]) +
            (", and finally " + clean(b['items'][-1]) if len(b['items']) > 4 else "")))
    if t == 'quote':
        return clean(b['q'].replace('\n\n', ' '))

    if lead:
        out.append(lead)

    if t == 'math':
        ORD = ["The first equation", "The second equation", "The third equation",
               "The fourth equation", "The fifth equation"]
        PROPER = {"Bayes'", "Bayes", "Gaussian", "Frobenius", "Equation", "Poisson",
                  "Wiener", "Mamba", "Swin", "GELU", "L2", "L1"}
        one = len(b['eqs']) == 1
        for k, eq in enumerate(b['eqs']):
            w = clean(eq.get('where', '')).rstrip('.').replace(' · ', '; ')
            if w:
                first = w.split()[0]
                if first[:1].isupper() and first.isalpha() and first not in PROPER:
                    w = w[:1].lower() + w[1:]
            head = "The equation on screen" if one else ORD[min(k, 4)]
            tail = " — point at it as you say this — " if k == 0 else " — "
            out.append("%s%s%s." % (head, tail, w) if w
                       else "%s is the one on screen; give them a beat to read it." % head)
        for x in b.get('bullets', []):
            out.append(clean(x))
    elif t == 'table':
        out.append("Read the table with me. " + ", ".join(clean(c) for c in b['cols']) + ".")
        hl = b.get('hl', [])
        for i in hl[:3]:
            if i < len(b['rows']):
                r = b['rows'][i]
                out.append("The row that matters is %s: %s." % (clean(str(r[0])),
                           ", ".join(clean(str(c)) for c in r[1:] if clean(str(c)))))
    elif t == 'cards':
        for c in b['cards']:
            out.append("%s. %s" % (clean(c['h']), clean(c['p'])))
    elif t == 'two':
        out.append("On the left, %s. %s" % (clean(b['left']['h']),
                   " ".join(clean(x) for x in b['left']['bullets'])))
        out.append("On the right, %s. %s" % (clean(b['right']['h']),
                   " ".join(clean(x) for x in b['right']['bullets'])))
    elif t == 'stats':
        for v in b['stats']:
            out.append("%s — %s. %s" % (clean(v['n']), clean(v['l']), clean(v['s'])))
        for x in b.get('bullets', []):
            out.append(clean(x))
    elif t == 'flow':
        for i, p in enumerate(b['steps'], 1):
            out.append("Step %d, %s. %s" % (i, clean(p['h']), clean(p['p'])))
        for x in b.get('bullets', []):
            out.append(clean(x))
    elif t == 'code':
        out.append("What is on screen is the actual source, from %s, unedited." % clean(b['file']))
        for x in b['bullets']:
            out.append(clean(x))
    else:
        for x in (b.get('bullets') or b.get('paras') or []):
            out.append(clean(x))

    if s['foot']:
        out.append(clean(s['foot']))
    txt = " ".join(out)
    txt = re.sub(r'\.\s*\.', '.', txt)
    txt = re.sub(r'\s+([,.;:])', r'\1', txt)
    return re.sub(r'\s+', ' ', txt).strip()

def transition(s):
    nxt = IDX.get(s['num'] + 1)
    if not nxt:
        return "End of the deck — stop, thank them, and invite questions."
    if nxt['t'] == 'section':
        return "That closes this part. Next: Part %s, %s." % (nxt['part'], clean(nxt['title']))
    if s['t'] == 'section':
        return "Straight into the first slide of the part: %s." % clean(nxt['title'])
    return "Which leads to the next slide: %s." % clean(nxt['title'])

def source_tag(s):
    c = (s['cite'] or '').lower()
    has_pdf = 'brief' in c
    has_paper = any(k in c for k in ['dncnn', 'bm3d', 'wnnm', 'tnrd', 'n2n', 'n2v', 'restormer',
                                     'nafnet', 'scunet', 'mambair', 'p2n', 'zs-n2n', 'wang'])
    if has_pdf and (has_paper or 'measured' in c):
        return ("Both", "Slide content from the deck; requirement framing from the assignment PDF.")
    if has_pdf:
        return ("Assignment PDF", "This slide exists because the brief asks for it.")
    if 'measured' in c:
        return ("Deck + our own measurement", "Figures produced by us; method stated on the slide.")
    if has_paper:
        return ("Deck (sourced from papers)", "Every figure is reproduced from the cited table.")
    return ("Deck", "Our own framing or reading, labelled as such on the slide.")

# ─────────────── hand-written depth for slides 7–11 ───────────────
DEEP = {
7: ("""This is the first slide where you can lose the room or win it. The four words of AWGN are not vocabulary — each one is a load-bearing assumption that a later slide breaks.

Deliver it as four claims with a consequence attached to each. **Additive** is what makes residual learning possible at all, because if noise were multiplied in you could not recover the image by subtraction — connect it forward to slide 33. **White** is what Noise2Void's blind spot depends on, so connect it forward to slide 45. **Gaussian**, and specifically *zero-mean*, is the entire Noise2Noise argument, which is slide 43. **Sigma** is the one the benchmarks vary.

Then land the punch: every one of those four words is false of a real camera, and slide 82 puts a number on it — DnCNN scores 23.66 dB on real sensor noise. Say that number here, once, as a forward reference. It buys you attention for the next seventy slides.""",
 "The forward references are the point. This slide is a promissory note that Parts III, IV, V and VII all redeem."),
8: ("""The conceptual hinge of the presentation. If the examiners remember one framing, make it this one.

Open with the arithmetic, not the terminology: if I tell you two numbers sum to ten, you cannot recover them. Then say that a denoiser faces exactly that, once per pixel, with the extra constraint that the answers must be jointly plausible as a photograph.

Only then introduce the word *prior*, and define it as "information the algorithm adds that is not in the measurement". Do not define it first — the definition lands much harder after the impossibility.

Close with the three consequences, and be firm about the first: there is no prior-free denoiser. A method that claims not to have one has hidden it in an architecture, a training set, or a stopping criterion. That sentence is what makes Part VI's organising question — *open the file, where is the prior?* — feel inevitable rather than clever.""",
 "Pause after 'there is no prior-free denoiser'. It is the sentence the rest of the deck hangs from."),
9: ("""The only real derivation in the condensed presentation, so do it properly and slowly — three lines, and name every symbol as it appears.

Line one is Bayes' rule with p(y) dropped because it does not depend on x. Line two is negative logarithms, turning a product into a sum and arg max into arg min. Line three substitutes the Gaussian likelihood.

The sentence that matters most is about the split: **the first term is forced, the second is chosen.** The squared L2 data-fidelity term is not a modelling preference — it is what the Gaussian assumption produces, because minus the log of exp of minus squared error over two sigma squared *is* squared error over two sigma squared. Phi, by contrast, is entirely a modelling choice, and the whole classical era is a sequence of guesses at it.

Expect to be asked to derive the fidelity term on a whiteboard. Practise it until it takes fifteen seconds.

Finish with the reading instruction: *read the whole deck as — what is Phi, and who wrote it?*""",
 "If you are running short, cut a bullet but never cut the forced-versus-chosen sentence."),
10: ("""The examiners will not challenge the formula. They will challenge whether 0.6 dB means anything, so pre-empt that.

Give the compression first: 3.01 dB is exactly a halving of MSE, so 0.6 dB is about a 13% reduction. Then give the calibration, and be explicit that it comes from the DnCNN paper itself rather than from us — prior work put the practical ceiling over BM3D at 0.3 dB and the estimated theoretical bound at 0.7 dB. DnCNN took 0.6, which is roughly 85% of the available headroom, and the blind model did it without being told sigma.

Then volunteer the weakness before it is used against you: PSNR can be raised by blurring, because blur lowers MSE while destroying texture. That is why SSIM is on the next slide, and it is why Noise2Noise names the resulting spatial blurriness as a known failure of L2 training.""",
 "'Eighty-five per cent of the available headroom' is the phrase to memorise. It converts a small number into a large result."),
11: ("""Two jobs on this slide, and the second one is a judgement call you should make on your own terms.

First, SSIM. Do not read the formula aloud — name the three components, then explain only the structure term, because that is the one PSNR has no analogue for. It is a local correlation coefficient, so blur decorrelates the estimate from the reference and lowers SSIM even where it raises PSNR. That single sentence is the whole reason the field reports both.

Second, IoU. The brief lists PSNR, SSIM and IoU as example metrics because it is written generically across many project topics. IoU measures region overlap and is undefined for dense regression with continuous output. Say so in one calm sentence, state that you report PSNR and SSIM because they are the standard for low-level vision, and move on.

Raising it yourself converts a potential 'you ignored a requirement' into a demonstration of judgement. Waiting for them to raise it does the opposite.""",
 "Six seconds on IoU, said matter-of-factly. Do not sound defensive and do not elaborate."),
}

# ─────────────── build ───────────────
blocks, nav, total = [], [], 0
for s in S:
    n = s['num']
    era_name, hexv = ERA.get(s['era'], ERA['meta'])
    sc = script(s)
    w = words(sc)
    tm, sec = mmss(w)
    total += sec
    src, srcnote = source_tag(s)
    deep = DEEP.get(n)

    nav.append("<div class='nv%s' data-go='sl%d'><span>%02d</span>%s</div>"
               % (' key' if n in DEEP else '', n, n, e(clean(s['title']))[:58]))

    blocks.append("""
<article class="sl{focus}" id="sl{n}" style="--era:{hex}" data-s="{blob}" data-part="{part}">
 <div class="slh">
  <div class="sn">{n}</div>
  <div class="st"><h3>{title}</h3>
   <div class="meta"><span class="era">{era}</span><span class="typ">{typ}</span>
    <span class="src">{src}</span><span class="tm">{tm} · {w} words</span>{focusbadge}</div></div>
 </div>
 <div class="slb">
  <section><h4>What this slide communicates</h4><p>{comm}</p></section>
  <section class="say"><h4>What to say</h4><p>{say}</p></section>
  <section><h4>What the visuals mean</h4><p>{vis}</p></section>
  <section><h4>Presentation cues</h4><p>{cue}</p></section>
  {deepblk}
  <section class="tr"><h4>Transition</h4><p>{trn}</p></section>
  <section class="src2"><h4>Source</h4><p><b>{src}.</b> {srcnote} Slide citation: <i>{cite}</i></p></section>
 </div>
</article>""".format(
        n=n, hex=hexv, era=e(era_name or "Front / back matter"), typ=s['t'],
        title=md(s['title']), src=e(src), srcnote=e(srcnote), tm=tm, w=w,
        focus=' focus' if deep else '',
        focusbadge="<span class='fb'>deep-dive</span>" if deep else "",
        part=e(s['part'] or '—'),
        blob=e(re.sub(r'\s+', ' ', (clean(s['title']) + ' ' + sc)).lower()[:2600]),
        comm=md(s['lead']) if s['lead'] else md(clean(s['title'])),
        say=e(sc), vis=md(visuals(s)), cue=md(s['notes']),
        deepblk=("<section class='deep'><h4>Deep-dive — slide %d</h4>%s<p class='pin'>%s</p></section>"
                 % (n, "".join("<p>%s</p>" % md(p) for p in deep[0].split("\n\n")), md(deep[1]))) if deep else "",
        trn=e(transition(s)), cite=e(s['cite'])))

TOT = "%d:%02d" % (total // 60, total % 60)

# ─────────────── bilingual Q&A ───────────────
QA = [
("What exactly are slides 7 to 11 doing in the argument?",
 "They set up the problem precisely enough that every later comparison means something. Slide 7 names the AWGN assumption and flags that all four of its words are false of a real camera. Slide 8 establishes that denoising is ill-posed, so a prior is mandatory. Slide 9 derives the two-term MAP objective and separates the forced data term from the chosen prior. Slides 10 and 11 define the metrics and their failure modes. Without those five slides, the 0.6 dB result on slide 37 and the 23.66 dB collapse on slide 82 would both be unreadable.",
 "این پنج اسلاید مسئله را آن‌قدر دقیق تعریف می‌کنند که همهٔ مقایسه‌های بعدی معنا پیدا کنند. اسلاید ۷ فرض نویز گاوسی سفید جمع‌شونده را نام می‌برد و هشدار می‌دهد که هر چهار واژهٔ آن دربارهٔ دوربین واقعی نادرست است. اسلاید ۸ نشان می‌دهد نویززدایی بدوضع است، پس پیشین اجباری است. اسلاید ۹ هدف دوجمله‌ای MAP را استخراج می‌کند و جملهٔ تحمیلی داده را از پیشینِ انتخابی جدا می‌کند. اسلایدهای ۱۰ و ۱۱ معیارها و حالت‌های شکستشان را تعریف می‌کنند. بدون این پنج اسلاید، نتیجهٔ ۰٫۶ دسی‌بل در اسلاید ۳۷ و فروریزش ۲۳٫۶۶ دسی‌بلی در اسلاید ۸۲ هر دو بی‌معنا می‌شدند.",
 "They are the setup that makes every later number legible."),
("On slide 9, why is the data-fidelity term squared error rather than something else?",
 "Because it is derived, not chosen. If the noise is Gaussian with variance sigma squared, the likelihood is proportional to exp of minus the squared norm of y minus x, over two sigma squared. Taking the negative logarithm gives exactly that squared norm over two sigma squared, plus a constant, and the one-over-sigma-squared is absorbed into lambda. Change the noise model and the term changes — Laplacian noise would give an L1 fidelity term, and Poisson noise would give a generalised Kullback–Leibler term.",
 "چون استخراج شده است، نه انتخاب. اگر نویز گاوسی با واریانس سیگما دو باشد، درست‌نمایی متناسب است با نمایی منفیِ نرم مربعی y منهای x تقسیم بر دو سیگما دو. با گرفتن لگاریتم منفی، دقیقاً همان نرم مربعی تقسیم بر دو سیگما دو به‌علاوهٔ یک ثابت به دست می‌آید و ضریب یک بر سیگما دو در لاندا جذب می‌شود. اگر مدل نویز عوض شود این جمله هم عوض می‌شود — نویز لاپلاسی جملهٔ وفاداری L1 می‌دهد و نویز پواسون جملهٔ واگرایی کولبک–لایبلر تعمیم‌یافته.",
 "Forced by the Gaussian likelihood; not a convenience choice."),
("On slide 10, is 0.6 dB actually a large improvement?",
 "Yes, and the calibration comes from the DnCNN paper itself rather than from us. The logarithm compresses everything: 3.01 dB is exactly a halving of mean squared error, so 0.6 dB is about a 13 per cent MSE reduction. More importantly, prior work put the practical ceiling over BM3D at 0.3 dB on average and the estimated theoretical bound at about 0.7 dB. DnCNN-S beat BM3D by 0.6 dB at all three noise levels — roughly 85 per cent of the available headroom — and DnCNN-B achieved nearly the same without being told sigma.",
 "بله، و این کالیبراسیون از خودِ مقالهٔ DnCNN می‌آید نه از ما. لگاریتم همه چیز را فشرده می‌کند: ۳٫۰۱ دسی‌بل دقیقاً یعنی نصف شدن خطای مربعی میانگین، پس ۰٫۶ دسی‌بل حدود ۱۳ درصد کاهش MSE است. مهم‌تر آنکه کارهای پیشین سقف عملی نسبت به BM3D را به‌طور میانگین ۰٫۳ دسی‌بل و کران نظری تخمینی را حدود ۰٫۷ دسی‌بل گزارش کرده‌اند. DnCNN-S در هر سه سطح نویز ۰٫۶ دسی‌بل بهتر بود — یعنی حدود ۸۵ درصد فضای موجود — و DnCNN-B تقریباً همان را بدون دانستن سیگما به دست آورد.",
 "85% of the theoretically available headroom."),
("On slide 11, why is IoU not reported?",
 "Because Intersection-over-Union measures the overlap of two regions and belongs to segmentation and detection. Denoising is dense regression with continuous-valued output — there are no regions to intersect, so IoU has no definition here. The brief lists it because the brief is written generically across many project topics. We report PSNR and SSIM, which are the standard for low-level vision, and we state the reason rather than forcing a meaningless number.",
 "چون معیار اشتراک بر اجتماع، هم‌پوشانی دو ناحیه را می‌سنجد و به بخش‌بندی و تشخیص تعلق دارد. نویززدایی یک رگرسیون چگال با خروجی پیوسته است — ناحیه‌ای برای اشتراک‌گیری وجود ندارد، پس IoU اینجا تعریف نشده است. شرح پروژه آن را ذکر کرده چون متنی عمومی برای موضوعات متعدد است. ما PSNR و SSIM را گزارش می‌کنیم که استاندارد بینایی سطح‌پایین‌اند، و دلیلش را می‌گوییم به‌جای آنکه عددی بی‌معنا را به‌زور وارد کنیم.",
 "Undefined for continuous dense output — say it in one calm sentence."),
("On slide 7, if AWGN is wrong, why use it at all?",
 "Because it is reproducible and it isolates the variable under test. SCUNet states this directly: AWGN removal is fair for testing the effectiveness of different network architecture designs, even while a general blind real denoiser remains unsolved. It is a controlled comparison, not a claim about photographs. And the project does not stop there — slide 82 shows the cost of the assumption in decibels.",
 "چون تکرارپذیر است و متغیر تحت آزمون را جدا می‌کند. SCUNet این را صریح می‌گوید: حذف نویز گاوسی سفید جمع‌شونده برای سنجش اثربخشی طراحی‌های مختلف معماری منصفانه است، حتی در حالی که نویززدای کورِ همه‌منظوره برای تصاویر واقعی هنوز حل نشده است. این یک مقایسهٔ کنترل‌شده است، نه ادعایی دربارهٔ عکس‌های واقعی. و پروژه همین‌جا متوقف نمی‌شود — اسلاید ۸۲ هزینهٔ این فرض را برحسب دسی‌بل نشان می‌دهد.",
 "Controlled comparison, not a claim about real photographs."),
("On slide 8, what do you mean by 'there is no prior-free denoiser'?",
 "Given one observation y, infinitely many splits into x plus v satisfy the equation. Arithmetic cannot choose among them, so every algorithm must add information that is not in the measurement — that added information is the prior. A method that appears not to have one has merely hidden it: in an architecture, in a training set, or in a stopping criterion. That claim is what makes Part Six's organising question meaningful.",
 "با داشتن یک مشاهدهٔ y، بی‌نهایت تجزیه به x به‌علاوهٔ v معادله را ارضا می‌کند. حساب نمی‌تواند میان آن‌ها انتخاب کند، پس هر الگوریتمی باید اطلاعاتی اضافه کند که در اندازه‌گیری نیست — همان اطلاعات اضافه، پیشین است. روشی که به نظر می‌رسد پیشین ندارد، صرفاً آن را پنهان کرده: در یک معماری، در یک مجموعهٔ آموزشی، یا در یک معیار توقف. همین ادعا است که پرسش سازمان‌دهندهٔ بخش ششم را معنادار می‌کند.",
 "Every denoiser has a prior; the question is only where it lives."),
("Why is the deck 100 slides if the presentation is 30 minutes?",
 "Because the brief asks for two different things. It requires depth and coverage equivalent to a two-to-four-hour course, usable as a complete self-study reference including theory, mathematics and implementation — that is the 100 slides. It separately says the presentation day is a condensed summary, with technical questions drawn from anywhere in the deck. So the deck is the reference and the 30 minutes is an executive summary of it.",
 "چون شرح پروژه دو چیز متفاوت می‌خواهد. عمق و پوشش در حد یک دورهٔ دو تا چهار ساعته را لازم می‌داند که به‌عنوان مرجع خودآموز کامل شامل تئوری، ریاضیات و پیاده‌سازی قابل استفاده باشد — که همان ۹۴ اسلاید است. جداگانه می‌گوید روز ارائه خلاصه‌ای فشرده است و پرسش‌های فنی از هر جای مجموعه پرسیده می‌شود. پس مجموعه، مرجع است و آن ۳۰ دقیقه خلاصهٔ اجرایی آن.",
 "The deck is the reference; the 30 minutes is a summary of it."),
("Which slide would you lead with if you only had five minutes?",
 "Slide 82 — real sensor noise. DnCNN, which beats BM3D by 0.6 dB on synthetic Gaussian noise, scores 23.66 dB on SIDD while Restormer reaches 40.02. BM3D, a 2007 algorithm, beats DnCNN there by 1.99 dB. That single row makes the whole evolutionary argument land in one breath: a model trained on the wrong noise distribution does not degrade gracefully, it collapses.",
 "اسلاید ۸۲ — نویز حسگر واقعی. DnCNN که روی نویز گاوسی مصنوعی ۰٫۶ دسی‌بل از BM3D بهتر است، روی SIDD امتیاز ۲۳٫۶۶ می‌گیرد در حالی که Restormer به ۴۰٫۰۲ می‌رسد. BM3D، الگوریتمی از سال ۲۰۰۷، همان‌جا ۱٫۹۹ دسی‌بل از DnCNN بهتر است. همین یک ردیف، کل استدلال تکاملی را در یک نفس منتقل می‌کند: مدلی که روی توزیع نویز اشتباه آموزش دیده به‌تدریج افت نمی‌کند، فرو می‌ریزد.",
 "23.66 against 40.02 is the strongest single number in the deck."),
("Do the presentation and the assignment brief ever conflict?",
 "One place, and we flag it ourselves rather than leaving it to be found. The brief lists PSNR, SSIM and IoU as example comparison metrics; the deck reports PSNR and SSIM and explains on slide 11 why IoU is undefined for dense regression. That is a deliberate, stated departure, not an omission. Separately, SCUNet's venue — Machine Intelligence Research — is not among the venues the brief names, which we flag on slide 93; we read the brief's list as illustrative since it is introduced with 'e.g.'. Beyond those two, no significant conflicts were identified.",
 "یک مورد، و خودمان آن را علامت می‌زنیم به‌جای آنکه بگذاریم کشف شود. شرح پروژه، PSNR و SSIM و IoU را به‌عنوان معیارهای نمونه فهرست می‌کند؛ مجموعه اسلایدها PSNR و SSIM را گزارش می‌کند و در اسلاید ۱۱ توضیح می‌دهد چرا IoU برای رگرسیون چگال تعریف نشده است. این یک انحراف عمدی و اعلام‌شده است، نه یک حذف. جداگانه، محل انتشار SCUNet — نشریهٔ Machine Intelligence Research — در میان محل‌هایی که شرح پروژه نام می‌برد نیست، که در اسلاید ۹۳ علامت زده‌ایم؛ ما فهرست شرح پروژه را نمونه‌وار می‌خوانیم چون با «مثلاً» معرفی شده است. جز این دو مورد، تعارض معناداری شناسایی نشد.",
 "Two stated departures, both raised by us first."),
("How do you know every number on a slide is correct?",
 "Because no quality metric in the deck was computed by us. Every PSNR and SSIM is reproduced from a published table with the paper and the table named at the point of use, and where a row compares two methods, both figures come from the same table so we are not comparing two evaluation scripts. Our own measurements cover parameter counts and CPU latency only, they used random tensors, and they are reported in separate tables labelled 'measured'. Where a figure could not be verified, it is absent — one MambaIR cell is excluded on exactly those grounds.",
 "چون هیچ معیار کیفیتی در این مجموعه توسط ما محاسبه نشده است. هر PSNR و SSIM از جدولی منتشرشده بازتولید شده، با ذکر نام مقاله و جدول در همان محل، و جایی که یک ردیف دو روش را مقایسه می‌کند هر دو عدد از یک جدول آمده‌اند تا دو اسکریپت ارزیابی متفاوت مقایسه نشوند. اندازه‌گیری‌های خودمان فقط شمار پارامترها و تأخیر CPU را پوشش می‌دهند، از تنسورهای تصادفی استفاده کرده‌اند، و در جدول‌های جداگانه با برچسب «اندازه‌گیری‌شده» گزارش شده‌اند. جایی که عددی قابل راستی‌آزمایی نبود، اصلاً نیامده است — یک سلول از MambaIR دقیقاً به همین دلیل حذف شده.",
 "Citation and measurement are never mixed in one column."),
]

qa_html = "".join("""<details class="qa">
<summary>{q}</summary>
<div class="qab">
 <div class="ans"><h5>English</h5><p>{en}</p></div>
 <div class="ans fa" dir="rtl"><h5>پاسخ فارسی</h5><p>{fa}</p></div>
 {kp}
</div></details>""".format(q=e(q), en=e(en), fa=e(fa),
    kp="<div class='kp'><b>Key point.</b> %s</div>" % e(kp) if kp else "")
    for q, en, fa, kp in QA)

CSS = """
:root{--bg:#0E1216;--surf:#151B21;--surf2:#1B222A;--line:#252E38;--line2:#303A45;
--tx:#E4EAF0;--tx2:#AFBBC7;--tx3:#7E8B98;--acc:#E8734A;--acc2:#5BA6D6;--ok:#4FB286}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);
font:17.5px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
h1,h2,h3,h4,h5{margin:0;line-height:1.25}
code{font-family:Consolas,monospace;font-size:.88em;background:#20272F;color:#9CD0E8;
padding:1px 5px;border-radius:3px;overflow-wrap:anywhere;word-break:break-word}
header#bar{position:fixed;inset:0 0 auto 0;height:58px;z-index:60;background:rgba(14,18,22,.96);
border-bottom:1px solid var(--line);display:flex;align-items:center;gap:12px;padding:0 16px}
.brand{font-weight:700;font-size:15px;white-space:nowrap}
.brand small{display:block;font-weight:400;font-size:11px;color:var(--tx3)}
#search{flex:1;max-width:420px;background:var(--surf2);border:1px solid var(--line2);border-radius:7px;
color:var(--tx);padding:9px 13px;font:inherit;font-size:14px}
.btn{background:var(--surf2);border:1px solid var(--line2);color:var(--tx2);border-radius:7px;
padding:8px 13px;font:inherit;font-size:13.5px;cursor:pointer;white-space:nowrap}
.btn:hover{background:#232C35;color:var(--tx)}.btn.on{background:var(--acc);border-color:var(--acc);
color:#12171C;font-weight:600}
#wrap{display:grid;grid-template-columns:300px 1fr;padding-top:58px}
#side{position:sticky;top:58px;height:calc(100vh - 58px);overflow-y:auto;
border-right:1px solid var(--line);padding:14px 0 60px;background:#101519}
.nv{padding:6px 16px;font-size:12.5px;color:var(--tx2);cursor:pointer;display:flex;gap:9px;line-height:1.4}
.nv span{color:var(--tx3);min-width:22px;font-variant-numeric:tabular-nums}
.nv:hover{background:var(--surf2);color:var(--tx)}
.nv.key{color:#F0A88C}.nv.key span{color:#F0A88C}
main{padding:26px 34px 120px;max-width:1020px}
.hero{background:var(--surf);border:1px solid var(--line);border-left:4px solid var(--acc);
border-radius:8px;padding:24px 28px;margin-bottom:24px}
.hero h1{font-size:27px;margin-bottom:10px}
.hero p{color:var(--tx2);font-size:16.5px;margin:0 0 10px}
.stat{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:18px}
.stat div{background:var(--surf2);border-left:3px solid var(--acc);padding:11px 14px}
.stat b{display:block;font-size:21px;color:var(--acc)}
.stat span{font-size:11.5px;color:var(--tx3)}
.sl{background:var(--surf);border:1px solid var(--line);border-left:4px solid var(--era);
border-radius:8px;margin-bottom:14px;overflow:hidden}
.sl.hide{display:none}
.sl.focus{border-color:var(--acc);border-left-color:var(--acc);box-shadow:0 0 0 1px rgba(232,115,74,.22)}
.slh{display:flex;gap:15px;padding:16px 20px;cursor:pointer;align-items:flex-start}
.sn{width:40px;height:40px;flex:none;border-radius:8px;background:var(--era);color:#fff;
display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px}
.st h3{font-size:19px;font-weight:600}
.meta{display:flex;gap:9px;flex-wrap:wrap;margin-top:7px;font-size:11.5px;color:var(--tx3)}
.meta span{background:var(--surf2);padding:2px 8px;border-radius:4px}
.meta .era{color:var(--tx2)}.meta .tm{color:var(--acc2)}
.fb{background:#4A2A24 !important;color:#F0A88C}
.slb{display:none;padding:0 20px 20px}
.sl.open .slb{display:block}
.slb section{margin-top:18px;border-top:1px solid var(--line);padding-top:14px}
.slb section:first-child{border-top:none;padding-top:0}
.slb h4{font-size:11px;letter-spacing:1.4px;text-transform:uppercase;color:var(--acc);margin-bottom:8px}
.slb p{margin:0 0 9px;color:var(--tx2);font-size:16.2px}
.slb p:last-child{margin-bottom:0}
.slb b{color:var(--tx)}
.say{background:var(--surf2);border-radius:8px;padding:16px 18px !important;border-top:none !important}
.say h4{color:var(--ok)}
.say p{color:var(--tx);font-size:17.5px;line-height:1.68}
.deep{background:#1E1712;border:1px solid #3E2C22;border-radius:8px;padding:16px 18px !important;
border-top:none !important}
.deep h4{color:#F0A88C}
.pin{border-top:1px solid #3E2C22;padding-top:10px;margin-top:12px !important;
color:#EBC3AE !important;font-size:13.8px !important}
.tr h4{color:var(--acc2)}.src2 h4{color:var(--tx3)}.src2 p{font-size:13px}
h2.sec{font-size:14px;letter-spacing:1.6px;text-transform:uppercase;color:var(--acc);
margin:40px 0 16px;padding-bottom:9px;border-bottom:1px solid var(--line)}
details.qa{background:var(--surf);border:1px solid var(--line);border-radius:8px;margin-bottom:10px;
overflow:hidden}
details.qa summary{cursor:pointer;padding:14px 18px;font-size:15.5px;font-weight:500;list-style:none}
details.qa summary::-webkit-details-marker{display:none}
details.qa summary:before{content:"▸ ";color:var(--acc)}
details.qa[open] summary:before{content:"▾ "}
details.qa[open] summary{border-bottom:1px solid var(--line);background:var(--surf2)}
.qab{padding:16px 18px}
.ans{margin-bottom:14px}
.ans h5{font-size:11px;letter-spacing:1.3px;text-transform:uppercase;color:var(--acc2);margin-bottom:7px}
.ans p{margin:0;color:var(--tx2);font-size:16.2px}
.ans.fa{font-family:Vazirmatn,"Noto Naskh Arabic",Tahoma,sans-serif;line-height:2.0}
.ans.fa h5{color:var(--ok)}
.kp{background:var(--surf2);border-left:3px solid var(--acc);padding:10px 14px;font-size:13.8px;
color:var(--tx2)}
#empty{display:none;color:var(--tx3);text-align:center;padding:40px}
@media(max-width:920px){#wrap{grid-template-columns:1fr}
 #side{position:fixed;top:58px;left:0;width:288px;z-index:55;transform:translateX(-100%);transition:.2s}
 body.nav #side{transform:none}main{padding:20px 16px 100px}.stat{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(min-width:921px){#menu{display:none}}
"""

JS = """
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const slides=()=>$$('.sl');
document.addEventListener('click',e=>{
  const h=e.target.closest('.slh'); if(!h)return; h.parentElement.classList.toggle('open');
});
$('#expand').onclick=()=>{
  const any=slides().some(s=>!s.classList.contains('open')&&!s.classList.contains('hide'));
  slides().forEach(s=>{if(!s.classList.contains('hide'))s.classList.toggle('open',any);});
};
let only=false;
$('#focus').onclick=()=>{ only=!only; $('#focus').classList.toggle('on',only); filt(); };
function filt(){
  const t=$('#search').value.trim().toLowerCase(); let n=0;
  slides().forEach(s=>{
    const okF=!only||s.classList.contains('focus');
    const okT=!t||s.dataset.s.includes(t);
    const v=okF&&okT; s.classList.toggle('hide',!v); if(v)n++;
  });
  $('#empty').style.display=n?'none':'block';
  $('#count').textContent=n+' of '+slides().length+' slides';
}
$('#search').addEventListener('input',filt);
$$('.nv').forEach(x=>x.onclick=()=>{
  const t=document.getElementById(x.dataset.go);
  if(t){t.classList.add('open');t.scrollIntoView({block:'start',behavior:'smooth'});
  document.body.classList.remove('nav');}
});
$('#menu').onclick=()=>document.body.classList.toggle('nav');
document.addEventListener('keydown',e=>{
  if(e.target.tagName==='INPUT')return;
  if(e.key==='/'){e.preventDefault();$('#search').focus();}
  if(e.key==='a')$('#expand').click();
  if(e.key==='f')$('#focus').click();
});
filt();
"""

DOC = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Presenter Companion — all 100 slides · Stage 3</title>
<link href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css" rel="stylesheet">
<style>%s</style></head><body>
<header id="bar">
 <button class="btn" id="menu">☰</button>
 <div class="brand">Presenter Companion<small>All 100 slides · script, visuals, cues, timing</small></div>
 <input id="search" placeholder="Search any slide…   ( / )">
 <button class="btn" id="focus">Slides 7–11 only (f)</button>
 <button class="btn" id="expand">Expand all (a)</button>
 <span id="count" style="font-size:12.5px;color:#7E8B98;white-space:nowrap"></span>
</header>
<div id="wrap">
 <nav id="side">%s</nav>
 <main>
  <div class="hero">
   <h1>Every slide, with a script you can read aloud</h1>
   <p>Built from the master deck itself, so nothing here is invented: each script is composed from
   that slide's own headline, lead, body and footnote, with the citation brackets stripped for speech.
   Where a slide's claim comes from the assignment brief rather than the deck, the <b>Source</b> row
   says so.</p>
   <p>Timings assume <b>125 words per minute</b> — technical delivery with pauses, not a news reader.
   The full read-through is far longer than the 30-minute slot, which is the point: the deck is the
   reference, the presentation is a summary of it. Use the condensed script in <code>defence.html</code>
   for the actual 30 minutes, and this file to answer anything from any slide.</p>
   <div class="stat">
    <div><b>100</b><span>slides scripted</span></div>
    <div><b>%s</b><span>full read-through</span></div>
    <div><b>5</b><span>deep-dive slides (7–11)</span></div>
    <div><b>%d</b><span>bilingual Q&amp;A</span></div>
   </div>
  </div>
  <h2 class="sec">Complete slide-by-slide script</h2>
  <div id="list">%s</div>
  <div id="empty">No slide matches that search.</div>
  <h2 class="sec">Questions &amp; answers — English and Persian</h2>
  <div>%s</div>
  <h2 class="sec">Source discrepancies</h2>
  <div class="hero" style="border-left-color:#5BA6D6">
   <p><b>Two stated departures, both raised by us rather than left to be found.</b></p>
   <p><b>1 · Metrics.</b> The assignment brief lists PSNR, SSIM and IoU as example comparison metrics.
   The deck reports PSNR and SSIM only, and slide 11 explains why: IoU measures region overlap and is
   undefined for dense regression with continuous-valued output. The brief supports including IoU;
   the deck supports excluding it. We treat the brief's list as illustrative, since it is introduced
   with &ldquo;e.g.&rdquo;, and we state the reasoning on the slide.</p>
   <p><b>2 · Venue.</b> SCUNet appeared in <i>Machine Intelligence Research</i> 20(6), 2023 — a
   peer-reviewed Springer journal, but not among the venues the brief names. Flagged on slide 93.
   If strict adherence to the named list were required, moving SCUNet to Category B still leaves
   11 of 15 sources in Category A, or 73.3%%, above the 70%% floor.</p>
   <p><b>Beyond these two, no significant conflicts were identified</b> between the deck and the
   assignment brief. Where the deck goes beyond the brief — the 2018 fork, the bottleneck framing,
   the measured benchmark — it is labelled as our own reading or measurement on the slide itself.</p>
  </div>
 </main>
</div>
<script>%s</script></body></html>""" % (CSS, "".join(nav), TOT, len(QA), "".join(blocks), qa_html, JS)

io.open('/home/claude/work/out/companion.html', 'w', encoding='utf-8').write(DOC)
print("slides scripted:", len(S))
print("full read-through:", TOT)
print("deep-dives:", len(DEEP))
print("bilingual Q&A:", len(QA))
print("bytes:", len(DOC))
