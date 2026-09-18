# -*- coding: utf-8 -*-
"""Builds presenter-30min.html — run sheet, per-slide script, handover, bilingual Q&A."""
import json, io, re, html

S = json.load(open('/home/claude/work/stage3/Stage3_ImageDenoising/5-source/presentation.json', encoding='utf-8'))
HAND = next(i for i, s in enumerate(S, 1) if 'Handover' in (s['kicker'] or ''))

def e(t): return html.escape(str(t), quote=False)
def clean(t):
    t = re.sub(r'`\[[^\]]+\]`', '', str(t)).replace('**','').replace('`','')
    t = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'\1', t)
    return re.sub(r'\s+', ' ', t).strip()
def md(t):
    t = e(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    return re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'<i>\1</i>', t)
def mmss(x): return "%d:%02d" % (x // 60, x % 60)

# spoken script, composed from each slide's own content
def script(s):
    b, t, out = s['body'], s['t'], []
    if s['lead']: out.append(clean(s['lead']))
    if t == 'title':
        return ("Good morning. Our topic is image denoising. This is not ten papers in chronological "
                "order — it is one technical story: what each method could not do, what the next one "
                "changed, and which line of code changed to do it. " + clean(s['lead']))
    if t == 'section':
        return "%s. %s We will cover %s." % (clean(s['title']), clean(s['lead']),
                                             ", then ".join(clean(i) for i in b['items']))
    if t == 'quote':
        return clean(b['q'].replace('\n\n', ' '))
    if t == 'table':
        out.append("The table compares " + ", ".join(clean(c) for c in b['cols'] if clean(c)) + ".")
        for i in (b.get('hl') or [])[:2]:
            if i < len(b['rows']):
                r = b['rows'][i]
                out.append("The row that matters is %s: %s." %
                           (clean(r[0]), "; ".join(clean(c) for c in r[1:] if clean(c))))
    elif t == 'cards':
        for c in b['cards']: out.append("%s. %s" % (clean(c['h']), clean(c['p'])))
    elif t == 'two':
        for side in ('left', 'right'):
            out.append("%s. %s" % (clean(b[side]['h']),
                                   " ".join(clean(x) for x in b[side]['bullets'])))
    elif t == 'stats':
        for v in b['stats']: out.append("%s, %s. %s" % (clean(v['n']), clean(v['l']), clean(v['s'])))
        out += [clean(x) for x in b.get('bullets', [])]
    elif t == 'flow':
        for p in b['steps']: out.append("%s. %s" % (clean(p['h']), clean(p['p'])))
    elif t == 'code':
        out.append("On screen is the actual change, before and after.")
        out += [clean(x) for x in b['bullets']]
    elif t == 'math':
        for q in b['eqs']: out.append("The equation on screen — " + clean(q.get('where','')) + ".")
        out += [clean(x) for x in b.get('bullets', [])]
    if s['foot']: out.append(clean(s['foot']))
    txt = " ".join(out)
    return re.sub(r'\s+([,.;:])', r'\1', re.sub(r'\.\s*\.', '.', txt))

# ── bilingual block-level guidance ──
BLOCKS = [
(1, 4, "Opening — frame the talk as evolution", "شروع — قاب‌بندی روایت تکاملی",
 "Do not open with an agenda. Open with the claim: this is one story about where the image prior lives and who writes it. Slide 2 is a contract with the audience — it tells the TA exactly what to listen for, which is worth the forty seconds. Slide 4 defines what SOTA means with three qualifiers; that definition is what makes the comparison at slide 26 land as a payoff rather than a hedge.",
 "با فهرست مطالب شروع نکنید. با ادعا شروع کنید: این یک روایت واحد است دربارهٔ اینکه پیشین تصویر کجا زندگی می‌کند و چه کسی آن را می‌نویسد. اسلاید ۲ یک قرارداد با مخاطب است — دقیقاً به استاد و دستیار می‌گوید به چه چیزی گوش بدهند و ارزش آن چهل ثانیه را دارد. اسلاید ۴ معنای SOTA را با سه قید تعریف می‌کند؛ همین تعریف است که باعث می‌شود مقایسهٔ اسلاید ۲۶ نتیجه‌بخش باشد نه یک طفره."),
(5, 8, "Era 1 — the hand-written prior", "دورهٔ اول — پیشین دست‌نویس",
 "BM3D's memorable fact is the ablation: a transform that is random apart from the DC loses only a few tenths of a decibel, so the grouping does the work. On slide 7 point at the highlighted Performance row and say the footnote out loud — plus 0.26 dB for a 271-times slowdown is the sentence that motivates the entire deep era. Slide 8 is fast; it is four quotes from the paper that ended the era.",
 "نکتهٔ ماندگار BM3D همان مطالعهٔ حذفی است: تبدیلی که جز مؤلفهٔ DC تصادفی باشد تنها چند دهم دسی‌بل از دست می‌دهد، پس کار اصلی را گروه‌بندی انجام می‌دهد. در اسلاید ۷ به ردیف پررنگ Performance اشاره کنید و پانویس را بلند بخوانید — «۰٫۲۶ دسی‌بل بیشتر به قیمت ۲۷۱ برابر کندتر» همان جمله‌ای است که کل دورهٔ یادگیری عمیق را توجیه می‌کند. اسلاید ۸ را سریع رد کنید؛ چهار نقل‌قول از مقاله‌ای است که آن دوره را تمام کرد."),
(9, 14, "Era 2 — the prior becomes a file", "دورهٔ دوم — پیشین به فایل تبدیل می‌شود",
 "This is the core of presenter one's material. Slide 12 is the most important implementation slide in the talk: point at return x-n, then at the BEFORE/AFTER comment block, and say that the same function class became far easier to optimise. On slide 13 use the phrase eighty-five per cent of the available headroom — it turns 0.6 dB into what it actually is. Slide 14 is the hinge; slow down, then hand over cleanly.",
 "این هستهٔ بخش ارائه‌دهندهٔ اول است. اسلاید ۱۲ مهم‌ترین اسلاید پیاده‌سازی کل ارائه است: به return x-n اشاره کنید، بعد به بلوک BEFORE/AFTER، و بگویید همان کلاس تابعی است اما بهینه‌سازی‌اش به‌مراتب ساده‌تر شده. در اسلاید ۱۳ از عبارت «۸۵ درصد فضای موجود» استفاده کنید — همین عبارت ۰٫۶ دسی‌بل را به آنچه واقعاً هست تبدیل می‌کند. اسلاید ۱۴ لولای روایت است؛ سرعت را کم کنید و بعد تحویل را تمیز انجام دهید."),
(15, 19, "Branch A — removing the clean image", "شاخهٔ الف — حذف تصویر تمیز",
 "Presenter two opens on the fork — deliver it with energy, it re-engages the room after the handover. On slide 17 the punchline is the 0.02 dB figure; say it last and let it sit. On slide 18 volunteer the row where Noise2Void scores below BM3D before anyone asks, then land the availability argument as your own point: where clean data does not exist, the comparison is against nothing at all.",
 "ارائه‌دهندهٔ دوم با انشعاب شروع می‌کند — آن را با انرژی بگویید، چون بعد از تعویض ارائه‌دهنده باید دوباره توجه جمع را بگیرید. در اسلاید ۱۷ ضربهٔ نهایی عدد ۰٫۰۲ دسی‌بل است؛ آن را آخر بگویید و یک مکث بدهید. در اسلاید ۱۸ خودتان ردیفی را که Noise2Void پایین‌تر از BM3D است مطرح کنید پیش از آنکه کسی بپرسد، و بعد استدلال «در دسترس بودن» را به‌عنوان نکتهٔ خودتان بگویید: جایی که دادهٔ تمیز وجود ندارد، مقایسه با هیچ است."),
(20, 24, "Branch B — replacing the convolution", "شاخهٔ ب — جایگزینی کانولوشن",
 "Slide 21 is the strongest analytical moment in the talk: identical models, identical table, and the gain changes by a factor of five when the dataset changes. Say computed from Table 4 so the provenance is unambiguous. Slides 22 and 23 are the two code slides — point at the rearrange pattern and at x1 * x2. Do not skip NAFNet's LayerNorm finding; it is the most intellectually honest line in the presentation.",
 "اسلاید ۲۱ قوی‌ترین لحظهٔ تحلیلی کل ارائه است: مدل‌های یکسان، جدول یکسان، و دستاورد با تغییر مجموعه‌داده پنج برابر می‌شود. بگویید «محاسبه‌شده از جدول ۴» تا منشأ عدد روشن باشد. اسلایدهای ۲۲ و ۲۳ دو اسلاید کد هستند — به الگوی rearrange و به x1 * x2 اشاره کنید. یافتهٔ LayerNorm در NAFNet را رد نکنید؛ صادقانه‌ترین جملهٔ کل ارائه است."),
(25, 31, "Synthesis — why several SOTAs", "جمع‌بندی — چرا چند SOTA داریم",
 "Slide 26 is the centrepiece: walk the Leads on column, not the figures, then deliver the footnote. Slide 27 answers the question the professor is most likely to ask, so give it its full time. On slide 30 commit to one proposal — the first row, crossing the fork — and have a reason ready for why that one. Deliver the conclusion from memory with the slide behind you, then stop and invite questions.",
 "اسلاید ۲۶ نقطهٔ اوج است: ستون «Leads on» را مرور کنید نه اعداد را، و بعد پانویس را بگویید. اسلاید ۲۷ به محتمل‌ترین پرسش استاد پاسخ می‌دهد، پس زمان کاملش را بدهید. در اسلاید ۳۰ روی یک پیشنهاد متعهد شوید — ردیف اول، یعنی عبور از انشعاب — و دلیل انتخابش را آماده داشته باشید. جمع‌بندی را از حفظ و با اسلاید پشت سرتان بگویید، بعد بایستید و پرسش‌ها را دعوت کنید."),
]

QA = [
("Why are there several state-of-the-art methods rather than one best?",
 "Because the benchmarks measure different capabilities and the cost axes disagree. BSD68 measures average-case Gaussian removal and has saturated — 0.36 dB across five years. Urban100 measures long-range self-similarity. SIDD and DND measure real sensor noise. NAFNet leads SIDD at 40.30 dB, Restormer leads Urban100 and is the only method past 40 dB on both real-noise sets, MambaIR leads DND by a hundredth of a decibel, and SCUNet competes on the training distribution instead of the architecture. A method can lead one table and trail another with no contradiction. On top of that our own measurements give three incompatible efficiency rankings of the same models.",
 "چون محک‌ها توانایی‌های متفاوتی را می‌سنجند و محورهای هزینه با هم نمی‌خوانند. BSD68 حذف نویز گاوسی در حالت میانگین را می‌سنجد و اشباع شده — ۰٫۳۶ دسی‌بل در پنج سال. Urban100 خودتشابهی دوربرد را می‌سنجد. SIDD و DND نویز واقعی حسگر را. NAFNet در SIDD با ۴۰٫۳۰ پیشتاز است، Restormer در Urban100 و تنها روشی است که در هر دو محک نویز واقعی از ۴۰ دسی‌بل گذشته، MambaIR در DND با اختلاف یک‌صدم دسی‌بل جلوست، و SCUNet به‌جای معماری روی توزیع آموزشی رقابت می‌کند. یک روش می‌تواند در یک جدول اول باشد و در جدول دیگر عقب، بدون هیچ تناقضی. افزون بر این، اندازه‌گیری‌های خودمان سه رتبه‌بندی کارایی ناسازگار از همان مدل‌ها می‌دهد."),
("What exactly changed between DnCNN and the previous approach?",
 "Three things, and the paper is explicit about each. First, the architecture stops resembling an optimiser — TNRD unrolled a PDE into stages; DnCNN is a plain Conv-BN-ReLU stack with no pooling. Second, the network outputs the noise rather than the image, so the clean result is y minus the prediction. Third, residual learning and batch normalisation are used together, and the paper shows neither works nearly as well alone. In code the contribution is the return statement: return x minus n instead of return the model output.",
 "سه چیز، و مقاله دربارهٔ هر سه صریح است. اول، معماری دیگر شبیه یک بهینه‌ساز نیست — TNRD یک معادلهٔ دیفرانسیل را به مراحل باز کرده بود؛ DnCNN یک پشتهٔ سادهٔ Conv-BN-ReLU بدون ادغام است. دوم، شبکه به‌جای تصویر، نویز را خروجی می‌دهد، پس نتیجهٔ تمیز برابر است با y منهای پیش‌بینی. سوم، یادگیری پسماند و نرمال‌سازی دسته‌ای با هم به کار می‌روند و مقاله نشان می‌دهد هیچ‌کدام به‌تنهایی نزدیک به این نتیجه نمی‌رسند. در کد، مشارکت اصلی همان دستور return است: به‌جای بازگرداندن خروجی مدل، x منهای n برگردانده می‌شود."),
("Why was predicting the noise important rather than just a stylistic choice?",
 "Because it changes the optimisation landscape without changing the function class. From ResNet, a mapping close to the identity is hard to optimise. The noisy image is much more like the clean image than it is like the noise, so learning the image forces the network toward an identity transform, which a stack of seventeen ReLU convolutions has no natural way to express. Learning the noise instead moves the do-nothing solution to zero, which is trivially reachable by driving weights toward zero.",
 "چون چشم‌انداز بهینه‌سازی را عوض می‌کند بدون آنکه کلاس تابعی عوض شود. از ResNet می‌دانیم نگاشتی که به همانی نزدیک است سخت بهینه می‌شود. تصویر نویزی بسیار بیشتر به تصویر تمیز شبیه است تا به نویز، پس یادگیری تصویر شبکه را به‌سمت یک نگاشت همانی می‌راند که پشته‌ای از هفده کانولوشن با ReLU راه طبیعی برای بیانش ندارد. در مقابل، یادگیری نویز راه‌حل «کاری نکن» را روی صفر می‌گذارد که با میل‌دادن وزن‌ها به صفر به‌سادگی قابل دستیابی است."),
("What makes Restormer state of the art, and since when?",
 "Concretely: it is the first method past 40 dB on both SIDD and DND, it leads Urban100 at every noise level, and it reports 3.14 times fewer FLOPs and 13 times faster runtime than SwinIR. It was published at CVPR 2022. I would not claim a period over which it held that position — no paper here reports one, and I am not going to estimate it. What distinguishes it from NAFNet is where the advantage sits — Restormer's gain is concentrated on long-range repetitive structure, which is exactly what its channel attention was designed to recover, while NAFNet leads on real sensor noise with far simpler code.",
 "مشخصاً: نخستین روشی است که در هر دو محک SIDD و DND از ۴۰ دسی‌بل عبور کرده، در Urban100 در همهٔ سطوح نویز پیشتاز است، و ۳٫۱۴ برابر FLOP کمتر و ۱۳ برابر سریع‌تر از SwinIR گزارش می‌دهد. در CVPR سال ۲۰۲۲ منتشر شده است. دربارهٔ اینکه چه مدت این جایگاه را نگه داشته ادعایی نمی‌کنم — هیچ‌کدام از مقالات چنین چیزی گزارش نکرده‌اند و ما هم تخمین نمی‌زنیم. آنچه آن را از NAFNet جدا می‌کند جای مزیت است — دستاورد Restormer روی ساختار تکرارشوندهٔ دوربرد متمرکز است که دقیقاً همان چیزی است که توجه کانالی‌اش برای بازیابی‌اش طراحی شده، در حالی که NAFNet روی نویز واقعی حسگر با کدی به‌مراتب ساده‌تر پیشتاز است."),
("Can you propose a concrete improvement based on these limitations?",
 "Yes, and it falls straight out of the structural finding of this project: the two branches have never merged. P2N still ships the 2018 Noise2Noise U-Net, while Restormer, NAFNet and MambaIR all assume paired supervised data. As far as we found, nobody has trained a Transformer or state-space backbone under P2N's renoised-data supervision. It is cheap to test because both halves already exist as working code, and it is measurable: run Noise2Void's own protocol on BSD68 at sigma 25 and on the cryo-TEM sets, and see whether the 1.35 dB self-supervision gap shrinks.",
 "بله، و مستقیماً از یافتهٔ ساختاری این پروژه می‌آید: دو شاخه هرگز به هم نپیوسته‌اند. P2N هنوز همان U-Net سال ۲۰۱۸ را عرضه می‌کند، در حالی که Restormer و NAFNet و MambaIR همگی دادهٔ زوجِ بانظارت را فرض می‌گیرند. تا جایی که ما یافتیم، کسی ستون فقرات ترنسفورمری یا فضای‌حالت را تحت نظارت دادهٔ دوباره‌نویزی‌شدهٔ P2N آموزش نداده است. آزمودنش کم‌هزینه است چون هر دو نیمه از قبل به‌صورت کد کارا وجود دارند، و قابل اندازه‌گیری است: پروتکل خودِ Noise2Void را روی BSD68 در سیگما ۲۵ و روی مجموعه‌های cryo-TEM اجرا کنید و ببینید آیا شکاف ۱٫۳۵ دسی‌بلی خودنظارتی کم می‌شود."),
("Why does the field still use BM3D as a baseline in 2023?",
 "Because it needs no training data and no GPU, which makes it the only fair comparison for zero-shot methods. Noise2Noise, Noise2Void and ZS-N2N all benchmark against it for exactly that reason. And on real sensor noise it still beats an AWGN-trained DnCNN by 1.99 dB, because it never committed to a learned noise distribution in the first place — it only assumes local self-similarity, which stays true.",
 "چون نه دادهٔ آموزشی می‌خواهد نه GPU، و همین آن را تنها مقایسهٔ منصفانه برای روش‌های zero-shot می‌کند. Noise2Noise و Noise2Void و ZS-N2N دقیقاً به همین دلیل با آن مقایسه می‌شوند. ضمناً روی نویز واقعی حسگر هنوز ۱٫۹۹ دسی‌بل از DnCNNِ آموزش‌دیده با AWGN بهتر است، چون از ابتدا به هیچ توزیع نویزِ آموخته‌شده‌ای متعهد نشده — فقط خودتشابهی محلی را فرض می‌گیرد که همچنان درست است."),
("What limitations remain in the current SOTA?",
 "Four. A general blind denoiser for real cameras remains unsolved — SCUNet's abstract says so, and nothing generalises to an unseen camera with an unseen ISP. Fidelity metrics reward blur, because L1, L2 and PSNR all recover a conditional mean and Noise2Noise itself names the resulting spatial blurriness. Nobody agrees what efficient means. And the benchmarks have saturated: BSD68 moved 0.36 dB in five years while real noise moved sixteen.",
 "چهار مورد. نویززدای کورِ همه‌منظوره برای دوربین‌های واقعی هنوز حل نشده — چکیدهٔ SCUNet همین را می‌گوید و هیچ روشی به دوربین دیده‌نشده با ISP دیده‌نشده تعمیم نمی‌یابد. معیارهای وفاداری به تاری پاداش می‌دهند، چون L1 و L2 و PSNR همگی میانگین شرطی را بازیابی می‌کنند و خودِ Noise2Noise تاری مکانی حاصل را نام می‌برد. کسی بر سر معنای «کارآمد» توافق ندارد. و محک‌ها اشباع شده‌اند: BSD68 در پنج سال ۰٫۳۶ دسی‌بل جابه‌جا شد در حالی که نویز واقعی شانزده دسی‌بل."),
]

# ── render ──
rows, blocks, t = [], [], 0
for s in S:
    sec = s.get('sec', 0)
    who = 1 if s['num'] < HAND else 2
    start = t; t += sec
    rows.append("<tr class='%s'><td>%02d</td><td>P%d</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                % ('hand' if s['num'] == HAND else '', s['num'], who,
                   mmss(start) if sec else '—', mmss(sec) if sec else 'backup',
                   e(clean(s['kicker'] or s['title']))))
    blocks.append("""<article class="sl p%d" id="s%d">
 <div class="h"><span class="n">%02d</span><div><h3>%s</h3>
  <div class="m"><span class="p">Presenter %d</span><span>%s</span><span class="k">%s</span></div></div></div>
 <div class="b">
  <section class="say"><h4>What to say</h4><p>%s</p></section>
  <section><h4>Delivery</h4><p>%s</p></section>
 </div></article>""" % (who, s['num'], s['num'], md(s['title']), who,
                        mmss(sec) if sec else 'not presented',
                        e(clean(s['kicker'])), e(script(s)),
                        md(re.sub(r'^\d+s\.\s*|^Not presented\.\s*', '', s['notes']))))

p1 = sum(s.get('sec',0) for s in S if s['num'] < HAND)
p2 = sum(s.get('sec',0) for s in S if s['num'] >= HAND)

blk = "".join("""<details class="blk" open><summary><b>Slides %d–%d</b> · %s
 <span class="fa">%s</span></summary><div class="cols"><div>%s</div>
 <div class="fa" dir="rtl">%s</div></div></details>"""
 % (a, b, e(en), e(fa), e(g1), e(g2)) for a, b, en, fa, g1, g2 in BLOCKS)

qa = "".join("""<details class="qa"><summary>%s</summary><div class="cols">
 <div><h5>English</h5><p>%s</p></div><div class="fa" dir="rtl"><h5>پاسخ فارسی</h5><p>%s</p></div>
 </div></details>""" % (e(q), e(en), e(fa)) for q, en, fa in QA)

CSS = """
:root{--bg:#0E1216;--surf:#151B21;--surf2:#1B222A;--line:#252E38;--tx:#E4EAF0;--tx2:#AFBBC7;
--tx3:#7E8B98;--a1:#5BA6D6;--a2:#E8734A;--ok:#4FB286}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);
font:17.5px/1.65 -apple-system,"Segoe UI",Roboto,Arial,sans-serif}
h1,h2,h3,h4,h5{margin:0;line-height:1.25}code{font-family:Consolas,monospace;font-size:.88em;
background:#20272F;color:#9CD0E8;padding:1px 5px;border-radius:3px;overflow-wrap:anywhere;word-break:break-word}
.fa{font-family:Vazirmatn,"Noto Naskh Arabic",Tahoma,sans-serif;line-height:2.0}
main{max-width:1120px;margin:0 auto;padding:28px 20px 100px}
.hero{background:var(--surf);border-left:4px solid var(--a2);padding:24px 28px;margin-bottom:24px}
.hero h1{font-size:26px;margin-bottom:10px}.hero p{color:var(--tx2);margin:0 0 10px}
.stat{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:18px}
.stat div{background:var(--surf2);border-left:3px solid var(--a1);padding:11px 14px}
.stat b{display:block;font-size:20px;color:var(--a1)}.stat span{font-size:11.5px;color:var(--tx3)}
h2.sec{font-size:14px;letter-spacing:1.6px;text-transform:uppercase;color:var(--a2);
margin:38px 0 14px;padding-bottom:8px;border-bottom:1px solid var(--line)}
table.run{border-collapse:collapse;width:100%;font-size:15px;background:var(--surf)}
table.run th{text-align:left;padding:9px 12px;color:var(--tx);border-bottom:1px solid var(--line);
font-size:11px;letter-spacing:1.2px;text-transform:uppercase}
table.run td{padding:7px 12px;border-bottom:1px solid var(--line);color:var(--tx2)}
tr.hand td{background:#2A1E19;color:#EBC3AE;font-weight:600}
.blk,.qa{background:var(--surf);border:1px solid var(--line);border-radius:8px;margin-bottom:10px;
overflow:hidden}
.blk summary,.qa summary{cursor:pointer;padding:13px 18px;font-size:15px;list-style:none}
.blk summary::-webkit-details-marker,.qa summary::-webkit-details-marker{display:none}
.blk summary:before,.qa summary:before{content:"▸ ";color:var(--a2)}
.blk[open] summary:before,.qa[open] summary:before{content:"▾ "}
.blk summary .fa{display:block;color:var(--tx3);font-size:13px;margin-top:3px}
.cols{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:26px;padding:16px 18px;font-size:16px;
color:var(--tx2)}
.cols h5{font-size:10.5px;letter-spacing:1.3px;text-transform:uppercase;color:var(--a1);
margin-bottom:6px}.cols p{margin:0}
.sl{background:var(--surf);border:1px solid var(--line);border-radius:8px;margin-bottom:10px}
.sl.p1{border-left:3px solid var(--a1)}.sl.p2{border-left:3px solid var(--a2)}
.sl .h{display:flex;gap:14px;padding:14px 18px;align-items:flex-start}
.sl .n{width:34px;height:34px;flex:none;border-radius:7px;background:var(--surf2);
display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;color:var(--tx3)}
.sl h3{font-size:18.5px}
.sl .m{display:flex;gap:9px;margin-top:6px;font-size:11.5px;color:var(--tx3);flex-wrap:wrap}
.sl .m span{background:var(--surf2);padding:2px 8px;border-radius:4px}
.sl .m .p{color:var(--ok)}.sl .m .k{color:var(--a2)}
.sl .b{padding:0 18px 18px}
.sl section{margin-top:14px;border-top:1px solid var(--line);padding-top:12px}
.sl h4{font-size:10.5px;letter-spacing:1.3px;text-transform:uppercase;color:var(--a2);margin-bottom:7px}
.sl p{margin:0;color:var(--tx2);font-size:16.2px}
.say{background:var(--surf2);border-radius:7px;padding:14px 16px!important;border-top:none!important}
.say h4{color:var(--ok)}.say p{color:var(--tx);font-size:17.5px;line-height:1.66}
@media(max-width:860px){.cols{grid-template-columns:minmax(0,1fr)}.stat{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media print{body{background:#fff;color:#000}.sl,.blk,.qa{border:1px solid #ccc}}
"""

DOC = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Presenter Run Sheet — 30-minute talk, two presenters</title>
<link href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css" rel="stylesheet">
<style>%s</style></head><body><main>
<div class="hero">
 <h1>Run sheet — 32 slides, two presenters, 26:06 core</h1>
 <p>Timings are per slide and cumulative. The handover is <b>slide %d</b>, chosen because slide 14
 sets up both bottlenecks and slide 15 answers them — the split falls on a natural seam in the
 argument rather than an arbitrary midpoint.</p>
 <p><b>If you are running late</b>, cut in this order: slide 10 (TNRD) to 30 s, slide 24
 (SCUNet/MambaIR) to 35 s, slide 29 (open problems) to 30 s. Never cut slides 12, 21, 26 or 27 —
 they are the implementation change, the bottleneck-3 evidence, the SOTA comparison and the
 multiple-SOTA answer. Those four are what the evaluation is actually about.</p>
 <div class="stat">
  <div><b>%s</b><span>presenter 1 · slides 1–%d</span></div>
  <div><b>%s</b><span>presenter 2 · slides %d–32</span></div>
  <div><b>26:06</b><span>core content</span></div>
  <div><b>3:54</b><span>buffer inside 30:00</span></div>
 </div>
</div>
<h2 class="sec">Run sheet</h2>
<table class="run"><thead><tr><th>#</th><th>Who</th><th>Start</th><th>Length</th><th>Slide</th></tr></thead>
<tbody>%s</tbody></table>
<h2 class="sec">Block guidance — English and Persian</h2>%s
<h2 class="sec">Slide-by-slide script</h2>%s
<h2 class="sec">Anticipated questions</h2>%s
</main></body></html>""" % (CSS, HAND, mmss(p1), HAND - 1, mmss(p2), HAND,
                            "".join(rows), blk, "".join(blocks), qa)

OUTF = '/home/claude/work/stage3/Stage3_ImageDenoising/2-presentation/presenter-30min.html'
io.open(OUTF, 'w', encoding='utf-8').write(DOC)
print("wrote", OUTF)
print("slides:", len(S), "| P1", mmss(p1), "| P2", mmss(p2), "| core", mmss(p1 + p2))
print("blocks:", len(BLOCKS), "| bilingual Q&A:", len(QA), "| bytes:", len(DOC))
