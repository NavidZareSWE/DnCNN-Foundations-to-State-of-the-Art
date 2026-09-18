# -*- coding: utf-8 -*-
"""Builds defence.html — bilingual (EN/FA) presenter companion for the Stage 3 defence."""
import io, json, html

def e(t): return html.escape(str(t), quote=False)

# ═══════════════ 30-MINUTE CONDENSED SCRIPT ═══════════════
# b = block; slides = deck slides to show; t/tf = title; s/sf = spoken script; c/cf = cue
SCRIPT = [
dict(n=1, min="0:00", dur="1:30", slides="1–4",
 t="Open on the thesis, not the agenda",
 tf="با تز شروع کنید، نه با فهرست مطالب",
 s="""Good morning. Our topic is image denoising, and our anchor paper is DnCNN, Zhang and colleagues, IEEE Transactions on Image Processing, 2017.

Before the contents, the claim. This deck is not ten paper summaries. It is one argument: image denoising is the cleanest available case study in how computer vision replaced hand-designed priors with learned ones — because in denoising, unusually, the prior is written down explicitly and you can watch it move.

Four eras, three bottlenecks. Manual prior design. The clean-data requirement. The receptive-field limit of convolution. Each bottleneck is named by the paper that broke it, so the arc is evidenced rather than imposed. And in 2018 the field forked into two branches that have never merged.

Ninety-four slides, fifteen sources, twelve of them Category A.""",
 sf="""صبح بخیر. موضوع ما نویززدایی تصویر است و مقالهٔ لنگر ما DnCNN است، ژانگ و همکاران، IEEE TIP، سال ۲۰۱۷.

پیش از فهرست مطالب، ادعا. این مجموعه اسلاید، خلاصهٔ ده مقاله نیست. یک استدلال واحد است: نویززدایی تصویر تمیزترین مطالعهٔ موردی موجود است از اینکه بینایی ماشین چگونه پیشین‌های دست‌ساز را با پیشین‌های آموخته‌شده جایگزین کرد — چون در نویززدایی، برخلاف بیشتر مسائل، پیشین صریحاً نوشته می‌شود و می‌توان حرکتش را دید.

چهار دوره، سه گلوگاه. طراحی دستی پیشین. نیاز به دادهٔ تمیز. و محدودیت میدان گیرندگی در کانولوشن. هر گلوگاه توسط همان مقاله‌ای نام برده شده که آن را شکسته است، پس این مسیر مستند است نه تحمیلی. و در سال ۲۰۱۸ این حوزه به دو شاخه تقسیم شد که هرگز به هم نپیوستند.

نود و چهار اسلاید، پانزده منبع، دوازده مورد در دستهٔ A.""",
 c="Do not read the agenda slide aloud. Point at it for three seconds and move.",
 cf="اسلاید فهرست مطالب را با صدای بلند نخوانید. سه ثانیه به آن اشاره کنید و رد شوید."),

dict(n=2, min="1:30", dur="3:00", slides="6–11",
 t="The problem, and why it is impossible without an assumption",
 tf="مسئله، و چرا بدون یک فرض حل‌نشدنی است",
 s="""One equation, and it has never changed: y equals x plus v. DnCNN writes it that way in 2017; SCUNet writes it identically in 2023.

The problem is ill-posed. Given y, infinitely many splits into x plus v are arithmetically valid. So the algorithm must add information that is not in the measurement — a prior. There is no prior-free denoiser; a method that claims not to have one has merely hidden it.

The classical era makes the choice explicit through MAP: minimise one-half the squared error to what the sensor saw, plus lambda times Phi of x. The first term is forced by the Gaussian assumption; the second is entirely a modelling choice. **Read the whole deck as: what is Phi, and who wrote it?**

On metrics — we report PSNR and SSIM. IoU appears in the brief because the brief is generic; it measures region overlap and is not defined for dense regression. We say so rather than force it.""",
 sf="""یک معادله، که هرگز تغییر نکرده است: y برابر است با x به‌علاوهٔ v. DnCNN آن را در ۲۰۱۷ به همین شکل می‌نویسد؛ SCUNet در ۲۰۲۳ دقیقاً همان را می‌نویسد.

مسئله بدوضع است. با داشتن y، بی‌نهایت تجزیه به x به‌علاوهٔ v از نظر حسابی معتبر است. پس الگوریتم باید اطلاعاتی اضافه کند که در اندازه‌گیری نیست — یعنی یک پیشین. نویززدایی بدون پیشین وجود ندارد؛ روشی که ادعا می‌کند پیشین ندارد، صرفاً آن را پنهان کرده است.

دورهٔ کلاسیک این انتخاب را از طریق MAP صریح می‌کند: کمینه‌سازی نصف خطای مربعی نسبت به آنچه حسگر دیده، به‌علاوهٔ لاندا ضرب‌در Φ از x. جملهٔ اول را فرض گاوسی تحمیل می‌کند؛ جملهٔ دوم کاملاً یک انتخاب مدل‌سازی است. **کل این مجموعه را این‌گونه بخوانید: Φ چیست، و چه کسی آن را نوشته است؟**

دربارهٔ معیارها — ما PSNR و SSIM گزارش می‌کنیم. IoU در شرح پروژه آمده چون آن متن عمومی است؛ IoU هم‌پوشانی ناحیه را می‌سنجد و برای رگرسیون چگال تعریف نشده است. ما این را می‌گوییم به‌جای آنکه به‌زور واردش کنیم.""",
 c="The IoU sentence is deliberate and takes six seconds. Saying it first converts a possible criticism into evidence of judgement.",
 cf="جملهٔ مربوط به IoU عمدی است و شش ثانیه وقت می‌گیرد. گفتن آن پیش از پرسیده‌شدن، یک ایراد احتمالی را به نشانهٔ قضاوت درست تبدیل می‌کند."),

dict(n=3, min="4:30", dur="4:30", slides="15–26",
 t="Era I — the prior is a formula a human wrote",
 tf="دورهٔ اول — پیشین فرمولی است که انسان نوشته",
 s="""Everything classical is one question: which pixels count as observations of the same quantity? Averaging n independent observations divides noise by root n — but only if they share the same clean value, which is false across an edge. That is the bias–variance trade, visible as grain against softness.

Gaussian weights by distance. Bilateral by distance and intensity. Then in 2005 non-local means abandons locality entirely and weights by patch similarity. That idea — non-local self-similarity — is the strongest hand-designed prior ever found for natural images, and it is load-bearing three more times in this deck.

BM3D, 2007, runs it twice: group by block matching, collaboratively hard-threshold in a 3-D transform, aggregate; then re-group inside the cleaner basic estimate and Wiener-filter. The paper's own ablation shows the transform barely matters — even a random basis loses only a few tenths — so the grouping is doing the work.

WNNM, 2014, is the classical peak: stack similar patches, recover the low-rank matrix, and weight each singular value inversely to its own size so large components survive. It beats BM3D. It also takes 773 seconds for one 512-by-512 image.

Nine years of hand-designed priors moved BSD68 at sigma 25 by 0.26 decibels, and the best method was 271 times slower than the second best. **Bottleneck one: the prior is written by hand and paid for once per image.**""",
 sf="""همهٔ روش‌های کلاسیک یک پرسش‌اند: کدام پیکسل‌ها مشاهدهٔ یک کمیت واحد به شمار می‌روند؟ میانگین‌گیری از n مشاهدهٔ مستقل، نویز را بر جذر n تقسیم می‌کند — اما فقط اگر مقدار تمیز مشترکی داشته باشند، که در عبور از لبه نادرست است. این همان بده‌بستان اریبی–واریانس است که به‌صورت دانه‌دانگی در برابر نرمی دیده می‌شود.

گاوسی بر اساس فاصله وزن می‌دهد. دوطرفه بر اساس فاصله و شدت. سپس در ۲۰۰۵ میانگین غیرمحلی، محلی‌بودن را کاملاً رها می‌کند و بر اساس شباهت وصله وزن می‌دهد. این ایده — خودتشابهی غیرمحلی — قوی‌ترین پیشین دست‌ساز برای تصاویر طبیعی است و سه بار دیگر در این مجموعه نقش کلیدی دارد.

BM3D در ۲۰۰۷ آن را دو بار اجرا می‌کند: گروه‌بندی با تطبیق بلوک، آستانه‌گذاری سخت مشارکتی در یک تبدیل سه‌بعدی، و تجمیع؛ سپس گروه‌بندی مجدد درون تخمین پایهٔ تمیزتر و فیلتر وینر. مطالعهٔ حذفی خودِ مقاله نشان می‌دهد نوع تبدیل تقریباً اهمیتی ندارد — حتی یک پایهٔ تصادفی فقط چند دهم دسی‌بل از دست می‌دهد — پس کار اصلی را گروه‌بندی انجام می‌دهد.

WNNM در ۲۰۱۴ اوج دورهٔ کلاسیک است: وصله‌های مشابه را روی هم می‌چیند، ماتریس کم‌رتبه را بازیابی می‌کند، و هر مقدار تکین را به‌طور وارون با اندازهٔ خودش وزن می‌دهد تا مؤلفه‌های بزرگ باقی بمانند. از BM3D بهتر است. اما برای یک تصویر ۵۱۲ در ۵۱۲ هفتصد و هفتاد و سه ثانیه وقت می‌گیرد.

نه سال پیشین دست‌ساز، BSD68 در سیگما ۲۵ را تنها ۰٫۲۶ دسی‌بل جابه‌جا کرد، و بهترین روش ۲۷۱ برابر کندتر از دومین روش بود. **گلوگاه یک: پیشین با دست نوشته می‌شود و برای هر تصویر یک‌بار هزینه دارد.**""",
 c="773 seconds is your most useful classical number. It comes from the DnCNN paper's own table, not from us.",
 cf="عدد ۷۷۳ ثانیه مفیدترین عدد کلاسیک شماست. از جدول خودِ مقالهٔ DnCNN آمده، نه از ما."),

dict(n=4, min="9:00", dur="6:00", slides="29–44",
 t="Era II — the prior becomes a file",
 tf="دورهٔ دوم — پیشین به یک فایل تبدیل می‌شود",
 s="""The bridge is unrolling: take an iterative optimiser, truncate it to a fixed number of stages, give each stage its own parameters, and train end-to-end. TNRD is simultaneously a reaction–diffusion PDE and a convolutional network, which is why the transition is continuous rather than a rupture.

Then DnCNN. Three layer types, one global skip, and nothing else — 556 thousand parameters, essentially one block repeated fifteen times.

The central idea is residual learning. The network predicts the noise, not the image; the loss target is y minus x. The justification is precise: from ResNet, a mapping close to the identity is hard to optimise — and y is much more like x than it is like v, especially at low noise. So learning the image would force the network toward an identity, which is a narrow, awkward point in parameter space, whereas learning the noise puts the do-nothing solution at zero, which is trivially reachable.

Residual learning and batch normalisation then benefit each other, and the second direction is the surprising one: without residual learning, batch norm actively hurts convergence, because layer statistics depend on which images are in the mini-batch. Residual learning strips the image out of the hidden layers, making activations Gaussian-like and content-independent — exactly the conditions batch norm needs.

Depth 17 is derived, not guessed: receptive field two-d-plus-one squared, set to 35 by 35 to match EPLL, the smallest effective patch size in the field.

The result: 0.6 decibels over BM3D at all three noise levels, against a literature ceiling of 0.3 and a theoretical bound of 0.7 — about 85 percent of the available headroom — and the blind model does it without being told sigma. Runtime falls from 773 seconds to 60 milliseconds, though I should say that comparison is CPU against GPU and the paper flags it itself.

And it loses. On Barbara, minus 0.71 decibels against BM3D, on exactly the image dominated by repetitive structure. **That number is bottleneck three, visible in 2017, three years before anyone could fix it.**

**Bottleneck two is the bill DnCNN leaves: the loss requires x.** For microscopy and medical imaging, x does not exist.""",
 sf="""پل ارتباطی، «باز کردن حلقه» است: یک بهینه‌ساز تکراری را بردارید، به تعداد ثابتی مرحله کوتاهش کنید، به هر مرحله پارامترهای خودش را بدهید، و کل آن را سرتاسری آموزش دهید. TNRD هم‌زمان یک معادلهٔ دیفرانسیل واکنش–انتشار است و هم یک شبکهٔ کانولوشنی، و برای همین این گذار پیوسته است نه گسست.

سپس DnCNN. سه نوع لایه، یک اتصال پرشی سراسری، و هیچ چیز دیگر — ۵۵۶ هزار پارامتر، که عملاً یک بلوک است که پانزده بار تکرار شده.

ایدهٔ مرکزی، یادگیری پسماند است. شبکه نویز را پیش‌بینی می‌کند، نه تصویر را؛ هدفِ تابع زیان، y منهای x است. توجیه دقیق است: از ResNet می‌دانیم نگاشتی که به همانی نزدیک باشد سخت بهینه می‌شود — و y بسیار بیشتر به x شبیه است تا به v، به‌ویژه در نویز کم. پس یادگیری تصویر، شبکه را به‌سمت یک نگاشت همانی می‌راند که نقطه‌ای تنگ و دشوار در فضای پارامتر است، در حالی که یادگیری نویز، راه‌حلِ «کاری نکن» را روی صفر می‌گذارد که به‌سادگی قابل دستیابی است.

آنگاه یادگیری پسماند و نرمال‌سازی دسته‌ای به هم سود می‌رسانند، و جهت دوم همان جهت غافلگیرکننده است: بدون یادگیری پسماند، نرمال‌سازی دسته‌ای عملاً به همگرایی آسیب می‌زند، چون آمار لایه‌ها به این وابسته است که کدام تصاویر در آن دستهٔ کوچک هستند. یادگیری پسماند تصویر را از لایه‌های پنهان بیرون می‌کشد و فعال‌سازی‌ها را گاوسی‌مانند و مستقل از محتوا می‌کند — دقیقاً همان شرایطی که نرمال‌سازی دسته‌ای لازم دارد.

عمق ۱۷ استنتاج شده است، نه حدس: میدان گیرندگی برابر است با دو‌d به‌علاوهٔ یک، به توان دو، که روی ۳۵ در ۳۵ تنظیم شده تا با EPLL برابر شود، یعنی کوچک‌ترین اندازهٔ وصلهٔ مؤثر در این حوزه.

نتیجه: ۰٫۶ دسی‌بل بهتر از BM3D در هر سه سطح نویز، در برابر سقف عملی ۰٫۳ و کران نظری ۰٫۷ — یعنی حدود ۸۵ درصد فضای موجود — و مدل کور این کار را بدون دانستن سیگما انجام می‌دهد. زمان اجرا از ۷۷۳ ثانیه به ۶۰ میلی‌ثانیه می‌رسد، هرچند باید بگویم این مقایسه CPU در برابر GPU است و خودِ مقاله هم به آن اشاره می‌کند.

و شکست هم می‌خورد. روی تصویر Barbara، منفی ۰٫۷۱ دسی‌بل نسبت به BM3D، دقیقاً روی تصویری که ساختار تکرارشونده بر آن غالب است. **این عدد همان گلوگاه سوم است، که در ۲۰۱۷ دیده شد، سه سال پیش از آنکه کسی بتواند حلش کند.**

**گلوگاه دو، صورت‌حسابی است که DnCNN باقی می‌گذارد: تابع زیان به x نیاز دارد.** برای میکروسکوپی و تصویربرداری پزشکی، x اصلاً وجود ندارد.""",
 c="This is the longest block and the one you are anchored on. If you overrun anywhere, overrun here — but state the CPU/GPU caveat, it is cheap and it protects you.",
 cf="این بلندترین بخش است و شما بر آن تمرکز دارید. اگر جایی از زمان عقب افتادید، همین‌جا باشد — اما حتماً نکتهٔ CPU در برابر GPU را بگویید؛ کم‌هزینه است و از شما محافظت می‌کند."),

dict(n=5, min="15:00", dur="4:00", slides="42–49",
 t="Branch one — the network never moved, the target did",
 tf="شاخهٔ یک — شبکه جابه‌جا نشد، هدف جابه‌جا شد",
 s="""Noise2Noise, 2018. L2 regression learns the conditional mean, and the conditional mean of a zero-mean corrupted target is the clean target. Therefore you may replace clean targets with a second noisy photograph without changing what the network learns. Measured cost: 0.02 decibels. The clean-data requirement was never actually necessary.

Noise2Void, 2019, removes the second copy with a blind spot. Because noise is pixel-wise independent given the signal, the neighbours carry no information about a pixel's own noise — so the network cannot learn the identity, but it can still learn the signal. The cost is real: 27.71 on BSD68, which is 1.35 below supervised and below BM3D. I want to say that plainly, because the argument is not quality — it is availability. On the Cell Tracking Challenge datasets the paper's ground-truth column is literally captioned "does not exist."

ZS-N2N, 2023, removes the training set: two fixed diagonal filters split one image into a noisy pair, a twenty-thousand-parameter two-layer network is fitted to it, done in under a minute on a CPU.

P2N, 2025, removes the information loss itself — renoise the model's own output with a plus and a minus, and train the two denoised versions to agree. Nothing masked, nothing downsampled.

**And the backbone across all seven years is the same U-Net.** In the P2N repository the class is literally named UNet-n2n-un, with the 2018 channel widths.""",
 sf="""‏Noise2Noise، سال ۲۰۱۸. رگرسیون L2 میانگین شرطی را یاد می‌گیرد، و میانگین شرطیِ یک هدفِ مخدوشِ میانگین‌صفر، همان هدف تمیز است. بنابراین می‌توانید هدف تمیز را با عکس نویزی دومی از همان صحنه جایگزین کنید بدون آنکه آنچه شبکه می‌آموزد تغییر کند. هزینهٔ اندازه‌گیری‌شده: ۰٫۰۲ دسی‌بل. نیاز به دادهٔ تمیز در واقع هرگز ضروری نبود.

‏Noise2Void، سال ۲۰۱۹، نسخهٔ دوم را با «نقطهٔ کور» حذف می‌کند. چون نویز به‌شرط سیگنال پیکسل‌به‌پیکسل مستقل است، همسایه‌ها هیچ اطلاعاتی دربارهٔ نویزِ خودِ آن پیکسل ندارند — پس شبکه نمی‌تواند نگاشت همانی را بیاموزد، اما همچنان می‌تواند سیگنال را بیاموزد. هزینه‌اش واقعی است: ۲۷٫۷۱ روی BSD68، یعنی ۱٫۳۵ پایین‌تر از حالت بانظارت و حتی پایین‌تر از BM3D. می‌خواهم این را صریح بگویم، چون استدلال، کیفیت نیست — در دسترس بودن است. در مجموعه‌داده‌های Cell Tracking Challenge، ستون حقیقت مبنا در خودِ مقاله عیناً «وجود ندارد» عنوان‌گذاری شده است.

‏ZS-N2N، سال ۲۰۲۳، مجموعهٔ آموزشی را حذف می‌کند: دو فیلتر قطری ثابت یک تصویر را به یک زوج نویزی تقسیم می‌کنند، و یک شبکهٔ دولایه با بیست هزار پارامتر روی همان تصویر برازش می‌شود — کمتر از یک دقیقه روی CPU.

‏P2N، سال ۲۰۲۵، خودِ اتلاف اطلاعات را حذف می‌کند — خروجی خودِ مدل را با علامت مثبت و منفی دوباره نویزی کنید و دو نسخهٔ نویززدایی‌شده را وادار کنید با هم توافق کنند. نه چیزی ماسک می‌شود، نه چیزی کوچک.

**و ستون فقرات در تمام این هفت سال، همان U-Net است.** در مخزن P2N نام کلاس عیناً UNet-n2n-un است، با همان عرض کانال‌های ۲۰۱۸.""",
 c="Volunteering the 27.71 number — worse than a 2007 algorithm — is a rigour move. It also lets you land the availability argument on your own terms.",
 cf="خودتان عدد ۲۷٫۷۱ را بگویید — بدتر از یک الگوریتم سال ۲۰۰۷. این نشانهٔ دقت است و اجازه می‌دهد استدلال «در دسترس بودن» را با شرایط خودتان مطرح کنید."),

dict(n=6, min="19:00", dur="4:00", slides="51–65",
 t="Branch two — three competing answers",
 tf="شاخهٔ دو — سه پاسخ رقیب",
 s="""Bottleneck three has a receipt. Restormer's Table 4 evaluates DnCNN and Restormer under one protocol. On BSD68 at sigma 50 the five-year gain is 0.39 decibels. On Urban100 — photographs of buildings, where structure repeats across hundreds of pixels — it is 1.98. **Five times larger on the dataset made of repetition.** That is Barbara's scarf, measured at dataset scale.

Attention is the obvious fix and its cost is the obvious problem: quadratic in resolution, which for a 256-square image means a four-billion-entry attention matrix. SwinIR restricts to windows, which buys back the locality you were escaping.

Restormer moves the axis instead: attend across channels, so the matrix is C by C, independent of resolution. In the code it is one einops rearrange that puts pixels on the last axis. Ablation: MDTA plus GDFN is worth 0.51 decibels over a UNet-with-Resblocks baseline.

NAFNet asks whether any of it is necessary. GELU is a special case of a gated linear unit; the gate alone supplies the nonlinearity; so replace the activation with a channel split and a multiply. Apply the same argument to channel attention and both nonlinearities disappear. Every simplification improved the result. And the largest single gain in their whole ablation is LayerNorm, worth 0.44 decibels — not because normalisation is magic, but because it stabilises training at a ten-times larger learning rate. **A large share of reported architectural progress in restoration is optimisation progress wearing a costume.**

MambaIR borrows a selective state-space model — global receptive field at linear cost — and SCUNet attacks the problem from the data side instead, synthesising Gaussian, Poisson, speckle, JPEG and ISP-simulated sensor noise with random shuffling.

**Three architectural answers and one data answer, published across three years, none of which has displaced the others.**""",
 sf="""گلوگاه سه سند دارد. جدول ۴ مقالهٔ Restormer، هم DnCNN و هم Restormer را تحت یک پروتکل ارزیابی می‌کند. روی BSD68 در سیگما ۵۰، دستاورد پنج‌ساله ۰٫۳۹ دسی‌بل است. روی Urban100 — عکس‌هایی از ساختمان‌ها، جایی که ساختار در طول صدها پیکسل تکرار می‌شود — این عدد ۱٫۹۸ است. **پنج برابر بزرگ‌تر، روی مجموعه‌داده‌ای که از تکرار ساخته شده.** این همان شال Barbara است، اما در مقیاس یک مجموعه‌داده.

توجه، راه‌حل بدیهی است و هزینه‌اش مشکل بدیهی: مرتبهٔ دو نسبت به تفکیک‌پذیری، که برای یک تصویر ۲۵۶ در ۲۵۶ یعنی ماتریس توجهی با چهار میلیارد درایه. SwinIR آن را به پنجره‌ها محدود می‌کند، که همان محلی‌بودنی را برمی‌گرداند که می‌خواستید از آن بگریزید.

‏Restormer به‌جای آن محور را عوض می‌کند: توجه در راستای کانال‌ها، پس ماتریس C در C است و مستقل از تفکیک‌پذیری. در کد، این یک فراخوانی rearrange است که پیکسل‌ها را روی آخرین محور می‌گذارد. مطالعهٔ حذفی: MDTA به‌علاوهٔ GDFN معادل ۰٫۵۱ دسی‌بل نسبت به پایهٔ UNet با بلوک‌های پسماند ارزش دارد.

‏NAFNet می‌پرسد آیا اصلاً هیچ‌کدام از این‌ها لازم است. GELU حالت خاصی از واحد خطی دروازه‌دار است؛ خودِ دروازه غیرخطی بودن را تأمین می‌کند؛ پس تابع فعال‌سازی را با تقسیم کانال و یک ضرب جایگزین کنید. همین استدلال را دربارهٔ توجه کانالی به کار ببرید و هر دو غیرخطی‌ها ناپدید می‌شوند. هر ساده‌سازی نتیجه را بهتر کرد. و بزرگ‌ترین دستاورد منفرد در کل مطالعهٔ حذفی آن‌ها، LayerNorm است با ۰٫۴۴ دسی‌بل — نه چون نرمال‌سازی جادو است، بلکه چون آموزش را با نرخ یادگیری ده برابر پایدار می‌کند. **بخش بزرگی از پیشرفت معماری گزارش‌شده در بازیابی تصویر، در واقع پیشرفت بهینه‌سازی است که لباس مبدل پوشیده.**

‏MambaIR یک مدل فضای‌حالت انتخابی قرض می‌گیرد — میدان گیرندگی سراسری با هزینهٔ خطی — و SCUNet به‌جای این‌ها از سمت داده حمله می‌کند و نویز گاوسی، پواسون، اسپکل، JPEG و نویز حسگر شبیه‌سازی‌شده با ISP را با ترتیب تصادفی سنتز می‌کند.

**سه پاسخ معماری و یک پاسخ داده‌ای، منتشرشده در سه سال، که هیچ‌کدام دیگری را کنار نزده است.**""",
 c="The 0.39-versus-1.98 contrast is your own analysis of published numbers. Say 'computed from Table 4' so the provenance is unambiguous.",
 cf="تقابل ۰٫۳۹ در برابر ۱٫۹۸ تحلیل خودتان از اعداد منتشرشده است. بگویید «محاسبه‌شده از جدول ۴» تا منشأ آن ابهام نداشته باشد."),

dict(n=7, min="23:00", dur="3:30", slides="66–77",
 t="Engineering reality — open the file, where is the prior?",
 tf="واقعیت مهندسی — فایل را باز کن، پیشین کجاست؟",
 s="""We asked one question of one codebase per era: open the source file, where is the prior?

Classical: scikit-image's TV-Chambolle is a while loop. The weight argument is lambda. One line of arithmetic is Phi. The loop is the test-time optimisation. Nothing persists — call it on a second image and every iteration runs again.

DnCNN in KAIR is a list comprehension of convolution layers, and forward returns x minus n. The prior is not in the file at all; it is in the .pth checkpoint the class will load. That is the moment the prior stops being readable.

Restormer's linear complexity is one rearrange. NAFNet's SimpleGate is chunk-and-multiply — four lines against two pages of derivation.

We then ran them. Seven architectures instantiated from their own repositories at pinned commits, parameters counted, CPU latency timed. Three findings no paper reports. NAFNet has 4.4 times Restormer's parameters and runs 5.5 times faster — so "more efficient" is meaningless without naming the metric and the device. Turning on P2N's Symmetric Prior Injection *reduces* parameters by 6.7 percent and *raises* latency 2.5 times, because every layer is evaluated twice. And MambaIR will not import without compiled CUDA extensions — which is not a gap in our experiment, it is the result.

Two caveats before you ask. Those runs used random tensors, so we measured no PSNR. And CPU latencies are not comparable to published GPU timings; only the ratios are informative.""",
 sf="""ما از هر دوره، از یک مخزن کد، یک پرسش پرسیدیم: فایل منبع را باز کن، پیشین کجاست؟

کلاسیک: پیاده‌سازی TV-Chambolle در scikit-image یک حلقهٔ while است. آرگومان weight همان لاندا است. یک خط حساب همان Φ است. خودِ حلقه، بهینه‌سازی زمان آزمون است. هیچ چیز باقی نمی‌ماند — آن را روی تصویر دوم صدا بزنید و همهٔ تکرارها از نو اجرا می‌شوند.

‏DnCNN در KAIR یک list comprehension از لایه‌های کانولوشن است، و forward مقدار x منهای n را برمی‌گرداند. پیشین اصلاً در این فایل نیست؛ در فایل ‎.pth است که این کلاس بارگذاری خواهد کرد. این همان لحظه‌ای است که پیشین دیگر خواندنی نیست.

پیچیدگی خطی Restormer یک فراخوانی rearrange است. SimpleGate در NAFNet یعنی تقسیم و ضرب — چهار خط در برابر دو صفحه استدلال.

سپس آن‌ها را اجرا کردیم. هفت معماری از مخازن خودشان روی کامیت‌های مشخص ساخته شدند، پارامترها شمرده و تأخیر روی CPU اندازه‌گیری شد. سه یافته که هیچ مقاله‌ای گزارش نمی‌کند. NAFNet ۴٫۴ برابر پارامترهای Restormer را دارد و ۵٫۵ برابر سریع‌تر است — پس «کارآمدتر» بدون نام‌بردن معیار و سخت‌افزار بی‌معناست. روشن‌کردن Symmetric Prior Injection در P2N پارامترها را ۶٫۷ درصد **کم** و تأخیر را ۲٫۵ برابر **زیاد** می‌کند، چون هر لایه دو بار ارزیابی می‌شود. و MambaIR بدون افزونه‌های کامپایل‌شدهٔ CUDA اصلاً import نمی‌شود — که نقص آزمایش ما نیست، خودِ نتیجه است.

دو نکتهٔ احتیاطی پیش از آنکه بپرسید. آن اجراها از تنسورهای تصادفی استفاده کردند، پس ما هیچ PSNR اندازه نگرفتیم. و تأخیرهای CPU با زمان‌های GPU منتشرشده قابل مقایسه نیستند؛ فقط نسبت‌ها آموزنده‌اند.""",
 c="Declaring the random-tensor caveat unprompted is much stronger than conceding it under questioning.",
 cf="اعلام خودجوش نکتهٔ «تنسور تصادفی» بسیار قوی‌تر از پذیرفتن آن زیر فشار پرسش است."),

dict(n=8, min="26:30", dur="3:30", slides="82–93",
 t="The number that carries the argument, and the close",
 tf="عددی که استدلال را حمل می‌کند، و جمع‌بندی",
 s="""One slide carries the comparative analysis. SIDD and DND are photographs taken with real smartphone cameras. DnCNN — which beats BM3D by 0.6 decibels on synthetic Gaussian noise — scores **23.66 decibels**. BM3D beats it by 1.99. Restormer reaches 40.02, and NAFNet 40.30.

A model trained on the wrong noise distribution does not degrade gracefully. It collapses by sixteen decibels. That is what SCUNet means by noise assumption mismatch, and it is why the field moved from AWGN benchmarks to real-noise benchmarks between 2019 and 2022.

So: on BSD68 the field gained one decibel in fifteen years and has saturated. On Urban100 it gained two decibels in five. On real noise it gained sixteen. **Progress in denoising since 2017 is mostly not progress on the 2017 problem.**

What is still unsolved: a general-purpose blind real denoiser — SCUNet's own abstract says so; the perception–distortion trade-off, because every loss in the field recovers a conditional mean and the conditional mean is blurry; and a cost metric anyone agrees on.

If you ask which model to deploy, the honest answer names the constraint first. Paired data and a GPU: NAFNet. Memory-bound: SCUNet. Maximum quality on repetitive structure: Restormer. No clean data at all: P2N or ZS-N2N. A dependency-free baseline: BM3D, still.

To close. Four eras, three bottlenecks, one fork in 2018 that has never merged, and three live answers to the third bottleneck. Which is why this ends in a genuine open question rather than a winner. Thank you — I am happy to take questions on any slide.""",
 sf="""یک اسلاید، کل تحلیل مقایسه‌ای را حمل می‌کند. SIDD و DND عکس‌هایی هستند که با دوربین‌های واقعی گوشی گرفته شده‌اند. DnCNN — که روی نویز گاوسی مصنوعی ۰٫۶ دسی‌بل از BM3D بهتر است — امتیاز **۲۳٫۶۶ دسی‌بل** می‌گیرد. BM3D با ۱٫۹۹ دسی‌بل از آن جلو می‌زند. Restormer به ۴۰٫۰۲ می‌رسد و NAFNet به ۴۰٫۳۰.

مدلی که روی توزیع نویز اشتباه آموزش دیده، به‌تدریج افت نمی‌کند. شانزده دسی‌بل فرو می‌ریزد. این همان چیزی است که SCUNet آن را «ناهمخوانی فرض نویز» می‌نامد، و دلیل آن است که این حوزه بین ۲۰۱۹ و ۲۰۲۲ از محک‌های AWGN به محک‌های نویز واقعی کوچ کرد.

پس: روی BSD68 این حوزه در پانزده سال یک دسی‌بل به دست آورد و اشباع شده است. روی Urban100 در پنج سال دو دسی‌بل. روی نویز واقعی شانزده دسی‌بل. **پیشرفت نویززدایی از سال ۲۰۱۷ به بعد، عمدتاً پیشرفت روی مسئلهٔ ۲۰۱۷ نیست.**

آنچه هنوز حل نشده: یک نویززدای کورِ همه‌منظوره برای تصاویر واقعی — چکیدهٔ خودِ SCUNet همین را می‌گوید؛ بده‌بستان ادراک–اعوجاج، چون هر تابع زیانی در این حوزه میانگین شرطی را بازیابی می‌کند و میانگین شرطی تار است؛ و یک معیار هزینه که همه بر سرش توافق داشته باشند.

اگر بپرسید کدام مدل را مستقر کنیم، پاسخ صادقانه ابتدا محدودیت را نام می‌برد. دادهٔ زوج و GPU: NAFNet. محدودیت حافظه: SCUNet. بیشترین کیفیت روی ساختار تکرارشونده: Restormer. نبودِ کامل دادهٔ تمیز: P2N یا ZS-N2N. یک خط پایهٔ بدون وابستگی: همچنان BM3D.

برای جمع‌بندی. چهار دوره، سه گلوگاه، یک انشعاب در ۲۰۱۸ که هرگز به هم نپیوست، و سه پاسخ زنده به گلوگاه سوم. و برای همین این روایت به یک پرسش باز واقعی ختم می‌شود، نه به یک برنده. متشکرم — با کمال میل به پرسش‌ها دربارهٔ هر اسلایدی پاسخ می‌دهم.""",
 c="Deliver the final paragraph from memory with the slide behind you. It is the last thing they hear before questions.",
 cf="پاراگراف پایانی را از حفظ و با اسلاید پشت سرتان ارائه دهید. این آخرین چیزی است که پیش از پرسش‌ها می‌شنوند."),
]

EXPANSION = {1: ('If running short: name the four competencies the brief grades — scholarship, synthesis, engineering, defence — and say which part of the deck answers each.', 'اگر وقت کم آوردید: چهار توانمندی\u200cای را که شرح پروژه نمره می\u200cدهد نام ببرید — پژوهش، سنتز، مهندسی، دفاع — و بگویید کدام بخش مجموعه به هرکدام پاسخ می\u200cدهد.'), 2: ('Expansion: derive the ½‖y−x‖² term aloud from the Gaussian likelihood — minus log of exp(−‖y−x‖²/2σ²) is ‖y−x‖²/2σ², and the 1/σ² is absorbed into λ. Thirty seconds, and it pre-empts a likely question.', 'گسترش: جملهٔ ½‖y−x‖² را با صدای بلند از درست\u200cنمایی گاوسی استخراج کنید — منفی لگاریتم exp(−‖y−x‖²/2σ²) برابر است با ‖y−x‖²/2σ²، و ضریب ۱/σ² در λ جذب می\u200cشود. سی ثانیه، و یک پرسش محتمل را پیش\u200cدستی می\u200cکند.'), 3: ("Expansion: BM3D's transform ablation — even a basis that is random apart from the DC loses only 0.1–0.4 dB, so the grouping does the work, not the transform. It is the most surprising classical result you have.", 'گسترش: مطالعهٔ حذفی تبدیل در BM3D — حتی پایه\u200cای که جز مؤلفهٔ DC تصادفی است تنها ۰٫۱ تا ۰٫۴ دسی\u200cبل از دست می\u200cدهد، پس کار اصلی را گروه\u200cبندی انجام می\u200cدهد نه تبدیل. غافلگیرکننده\u200cترین نتیجهٔ کلاسیکی است که دارید.'), 4: ("Expansion: DnCNN-3 — redefine v as HR minus bicubic upsampling and the same network does super-resolution; as original minus JPEG-compressed and it does deblocking. One model beats a specialist baseline on all three. Reproduce the paper's 'to the best of our knowledge' hedge.", 'گسترش: DnCNN-3 — اگر v را تفاوت تصویر باکیفیت و درون\u200cیابی دومکعبی تعریف کنید، همان شبکه فراتفکیک\u200cپذیری انجام می\u200cدهد؛ اگر تفاوت اصل و نسخهٔ فشردهٔ JPEG باشد، رفع بلوک انجام می\u200cدهد. یک مدل در هر سه از خط پایهٔ تخصصی بهتر است. قید «تا جایی که می\u200cدانیم» مقاله را عیناً بازگو کنید.'), 5: ("Expansion: walk the four targets explicitly — a second photograph, the masked pixel's own value, the other diagonal of a 2×2 block, the model's own renoised output. Each removes one requirement and adds one cost.", 'گسترش: چهار هدف را صریحاً مرور کنید — عکس دوم، مقدار خودِ پیکسل ماسک\u200cشده، قطر دیگرِ یک بلوک ۲×۲، و خروجی دوباره\u200cنویزی\u200cشدهٔ خودِ مدل. هرکدام یک نیاز را حذف و یک هزینه اضافه می\u200cکند.'), 6: ('Expansion: the attention token arithmetic — a 256² image has 65 536 positions, so the attention matrix has 4.3 billion entries, against 196 tokens for a ViT at 224² with 16×16 patches. That contrast explains in five seconds why restoration Transformers are a different problem.', 'گسترش: حساب توکن\u200cهای توجه — یک تصویر ۲۵۶×۲۵۶ شامل ۶۵٬۵۳۶ موقعیت است، پس ماتریس توجه ۴٫۳ میلیارد درایه دارد، در برابر ۱۹۶ توکن برای یک ViT در ۲۲۴×۲۲۴ با وصله\u200cهای ۱۶×۱۶. این تقابل در پنج ثانیه توضیح می\u200cدهد چرا ترنسفورمرهای بازیابی مسئلهٔ دیگری\u200cاند.'), 7: ('Expansion: the padding table — Restormer needs multiples of 8, NAFNet 16, P2N+ 32, SCUNet 64, and the padding modes differ too. A factor of eight, invisible from every paper, and it matters the moment two are chained.', 'گسترش: جدول لایه\u200cگذاری — Restormer مضارب ۸، NAFNet مضارب ۱۶، P2N+ مضارب ۳۲، و SCUNet مضارب ۶۴ می\u200cخواهد، و حالت لایه\u200cگذاری هم فرق دارد. ضریبی هشت\u200cبرابری که از هیچ مقاله\u200cای پیدا نیست و لحظه\u200cای که دو مدل پشت سر هم بیایند اهمیت پیدا می\u200cکند.'), 8: ('Expansion: the three unsolved problems, one sentence each — a blind real denoiser, the perception–distortion trade-off, and a cost metric anyone agrees on. Then close on the open question.', 'گسترش: سه مسئلهٔ حل\u200cنشده، هرکدام یک جمله — نویززدای کور برای تصاویر واقعی، بده\u200cبستان ادراک–اعوجاج، و معیار هزینه\u200cای که همه بر سرش توافق کنند. سپس با پرسش باز جمع\u200cبندی کنید.')}
for _b in SCRIPT:
    _b['x'], _b['xf'] = EXPANSION[_b['n']]

# recompute timings from actual word counts (125 wpm = technical delivery with pauses)
_t = 0
for _b in SCRIPT:
    _w = len(_b['s'].split())
    _d = max(60, round(_w / 125 * 60 / 15) * 15)
    _b['min'] = "%d:%02d" % (_t // 60, _t % 60)
    _b['dur'] = "%d:%02d" % (_d // 60, _d % 60)
    _t += _d
SPOKEN = _t

# ═══════════════ Q&A BANK ═══════════════
QA = [
("core", "Why is 0.6 dB a big deal? It sounds like nothing.",
 "چرا ۰٫۶ دسی‌بل مهم است؟ به نظر ناچیز می‌آید.",
 "Because the logarithm compresses everything: 3.01 dB is exactly a halving of MSE, so 0.6 dB is about a 13% MSE reduction. More importantly, the DnCNN paper supplies its own calibration — prior work found few methods can outperform BM3D by more than 0.3 dB on average, and the estimated PSNR bound over BM3D is about 0.7 dB. DnCNN-S beat BM3D by 0.6 dB at all three noise levels, so it captured roughly 85% of the theoretically available headroom. And DnCNN-B did it blind. [DnCNN17 §IV-B, Table II]",
 "چون لگاریتم همه چیز را فشرده می‌کند: ۳٫۰۱ دسی‌بل دقیقاً یعنی نصف شدن MSE، پس ۰٫۶ دسی‌بل حدود ۱۳٪ کاهش MSE است. مهم‌تر آنکه خودِ مقالهٔ DnCNN کالیبراسیون ارائه می‌دهد — کارهای پیشین نشان داده‌اند کمتر روشی به‌طور میانگین بیش از ۰٫۳ دسی‌بل از BM3D بهتر عمل می‌کند، و کران تخمینی PSNR نسبت به BM3D حدود ۰٫۷ دسی‌بل است. DnCNN-S در هر سه سطح نویز ۰٫۶ دسی‌بل بهتر بود، یعنی حدود ۸۵٪ فضای نظری موجود. و DnCNN-B این کار را به‌صورت کور انجام داد."),

("core", "Why predict the noise rather than the clean image?",
 "چرا نویز را پیش‌بینی کنیم و نه تصویر تمیز را؟",
 "Two steps. From ResNet: when the original mapping is close to an identity, the residual mapping is much easier to optimise. And y is much more like x than it is like v, especially at low noise. So learning F(y)=x forces the network toward an identity transform, which a stack of convolutions with ReLUs has no natural way to express — seventeen layers would have to conspire into it, a narrow and awkward point in parameter space. Learning R(y)=v puts the 'do nothing' solution at zero, which is trivially reachable by driving weights toward zero. Note DnCNN is not ResNet: it uses a single global residual unit, not many identity shortcuts. [DnCNN17 §II-A, §III-A]",
 "دو گام. از ResNet: وقتی نگاشت اصلی به همانی نزدیک باشد، نگاشت پسماند بسیار ساده‌تر بهینه می‌شود. و y بسیار بیشتر به x شبیه است تا به v، به‌ویژه در نویز کم. پس یادگیری F(y)=x شبکه را به‌سمت یک تبدیل همانی می‌راند، که پشتهٔ کانولوشن‌ها با ReLU هیچ راه طبیعی برای بیانش ندارد — هفده لایه باید با هم آن را بسازند، که نقطه‌ای تنگ در فضای پارامتر است. یادگیری R(y)=v راه‌حل «کاری نکن» را روی صفر می‌گذارد که با میل‌دادن وزن‌ها به صفر به‌سادگی قابل دستیابی است. توجه کنید DnCNN همان ResNet نیست: یک واحد پسماند سراسری دارد، نه شمار زیادی میان‌بر همانی."),

("core", "Explain the residual-learning / batch-norm synergy in both directions.",
 "هم‌افزایی یادگیری پسماند و نرمال‌سازی دسته‌ای را در هر دو جهت توضیح دهید.",
 "Direction one is easy: BN alleviates internal covariate shift, so residual learning with BN beats residual learning without it. Direction two is the surprising one — without residual learning, BN even has an adverse effect on convergence. The mechanism: a mini-batch is only 128 patches, and without residual learning the layer inputs are correlated with their neighbours and depend on the content of those particular images, so the batch statistics are meaningless. With residual learning DnCNN implicitly removes the latent clean image in the hidden layers, making layer inputs Gaussian-like, less correlated, and less related to image content. The paper also notes both the residual image and BN are associated with the Gaussian distribution, which is why they suit each other in Gaussian denoising specifically. And it is the integration, not the optimiser — both SGD and Adam give the best result with RL+BN. [DnCNN17 §III-C]",
 "جهت اول ساده است: BN جابه‌جایی هم‌متغیر درونی را کاهش می‌دهد، پس یادگیری پسماند با BN بهتر از بدون آن است. جهت دوم غافلگیرکننده است — بدون یادگیری پسماند، BN حتی اثر نامطلوبی بر همگرایی دارد. سازوکار: یک دستهٔ کوچک فقط ۱۲۸ وصله است، و بدون یادگیری پسماند ورودی‌های لایه با همسایه‌هایشان همبسته‌اند و به محتوای همان تصاویر خاص وابسته‌اند، پس آمار دسته بی‌معنا می‌شود. با یادگیری پسماند، DnCNN تصویر تمیز نهفته را به‌طور ضمنی در لایه‌های پنهان حذف می‌کند و ورودی لایه‌ها گاوسی‌مانند، کم‌همبسته و مستقل از محتوا می‌شوند. مقاله همچنین می‌گوید هم تصویر پسماند و هم BN با توزیع گاوسی مرتبط‌اند، و برای همین به‌طور خاص در نویززدایی گاوسی به هم می‌آیند. و این ترکیب است نه بهینه‌ساز — هم SGD و هم Adam با RL+BN بهترین نتیجه را می‌دهند."),

("core", "Why depth 17? Is that not arbitrary?",
 "چرا عمق ۱۷؟ آیا دلبخواهی نیست؟",
 "It is derived. With no pooling and 3×3 filters, the receptive field of a depth-d DnCNN is exactly (2d+1)×(2d+1). The authors tabulated the effective patch size of every competitor at σ=25 — EPLL 36×36, MLP 47×47, BM3D 49×49, CSF and TNRD 61×61, WNNM 361×361 — and posed the question of whether a DnCNN with a receptive field similar to the *smallest* of them could compete. So 35×35, which is depth 17. For general denoising tasks they used depth 20, 41×41, because high noise levels require a larger effective patch size. The point worth making: DnCNN wins with a field one tenth the linear extent of WNNM's. [DnCNN17 Table I, §III-B]",
 "استنتاج شده است. بدون ادغام و با فیلترهای ۳×۳، میدان گیرندگی یک DnCNN با عمق d دقیقاً (2d+1)×(2d+1) است. نویسندگان اندازهٔ وصلهٔ مؤثر همهٔ رقبا را در سیگما ۲۵ جدول کردند — EPLL ‏۳۶×۳۶، MLP ‏۴۷×۴۷، BM3D ‏۴۹×۴۹، CSF و TNRD ‏۶۱×۶۱، WNNM ‏۳۶۱×۳۶۱ — و این پرسش را مطرح کردند که آیا DnCNN با میدانی شبیه **کوچک‌ترین** آن‌ها می‌تواند رقابت کند. پس ۳۵×۳۵، یعنی عمق ۱۷. برای وظایف عمومی‌تر از عمق ۲۰ و میدان ۴۱×۴۱ استفاده کردند، چون سطوح نویز بالا وصلهٔ مؤثر بزرگ‌تری می‌خواهند. نکتهٔ گفتنی: DnCNN با میدانی یک‌دهمِ گسترهٔ خطی WNNM برنده می‌شود."),

("core", "Where does DnCNN lose, and why does that matter?",
 "‏DnCNN کجا شکست می‌خورد و چرا مهم است؟",
 "On Barbara at σ=25 it scores 30.00 against BM3D's 30.71 and WNNM's 31.24 — minus 0.71 and minus 1.24. It also trails WNNM on House. Those are exactly the two images in the set dominated by repetitive structure. The paper's explanation: non-local means based methods are usually better on images with regular and repetitive structures, whereas discriminative training based methods do better on irregular textures — repetitive images meet well with the non-local similarity prior. This matters because it is bottleneck three, visible in 2017, three years before anyone could fix it, and it is why Restormer's gain on Urban100 is five times its gain on BSD68. [DnCNN17 Table III, §IV-C]",
 "روی تصویر Barbara در سیگما ۲۵ امتیاز ۳۰٫۰۰ می‌گیرد در برابر ۳۰٫۷۱ برای BM3D و ۳۱٫۲۴ برای WNNM — یعنی منفی ۰٫۷۱ و منفی ۱٫۲۴. روی House هم از WNNM عقب است. این دقیقاً همان دو تصویری است که ساختار تکرارشونده بر آن‌ها غالب است. توضیح مقاله: روش‌های مبتنی بر میانگین غیرمحلی معمولاً روی تصاویر با ساختار منظم و تکرارشونده بهترند، در حالی که روش‌های مبتنی بر آموزش تمایزی روی بافت‌های نامنظم بهتر عمل می‌کنند — تصاویر تکرارشونده با پیشین شباهت غیرمحلی خوب جور در می‌آیند. این مهم است چون همان گلوگاه سوم است که در ۲۰۱۷ دیده شد، و دلیل آن است که دستاورد Restormer روی Urban100 پنج برابر دستاوردش روی BSD68 است."),

("branch", "How can training on noisy targets possibly work?",
 "آموزش با هدف‌های نویزی چطور ممکن است کار کند؟",
 "L2 regression learns the conditional mean of the target. A trivial property of L2 minimisation is that on expectation the estimate is unchanged if you replace the targets with random numbers whose expectations match them. So if E{ŷ|x̂} = y — which is exactly what a second noisy photograph of the same scene gives you — the optimal parameters are unchanged. Given infinite data the solution equals clean-target training; for finite data the extra variance is the target-corruption variance divided by the number of samples. It relies on no likelihood model of the corruption and no prior on clean images. Measured on Kodak/BSD300/Set14 at σ=25, clean targets average 31.63 and noisy targets 31.61 — a gap of 0.02 dB. [N2N18 §2, Table 1]",
 "رگرسیون L2 میانگین شرطی هدف را می‌آموزد. یک ویژگی ساده از کمینه‌سازی L2 این است که در امید ریاضی، تخمین تغییر نمی‌کند اگر هدف‌ها را با اعداد تصادفی‌ای جایگزین کنید که امیدشان با هدف‌ها یکی است. پس اگر E{ŷ|x̂} = y باشد — که دقیقاً همان چیزی است که عکس نویزی دوم از همان صحنه به شما می‌دهد — پارامترهای بهینه تغییر نمی‌کنند. با دادهٔ بی‌نهایت، جواب با آموزش هدف‌تمیز یکی است؛ با دادهٔ متناهی، واریانس اضافی برابر است با واریانس مخدوش‌سازی هدف تقسیم بر تعداد نمونه‌ها. این استدلال به هیچ مدل درست‌نمایی از مخدوش‌سازی و هیچ پیشینی روی تصاویر تمیز متکی نیست. اندازه‌گیری‌شده روی Kodak/BSD300/Set14 در سیگما ۲۵: هدف تمیز میانگین ۳۱٫۶۳ و هدف نویزی ۳۱٫۶۱ — اختلاف ۰٫۰۲ دسی‌بل."),

("branch", "Why can a blind-spot network not just learn the identity?",
 "چرا شبکهٔ نقطه‌کور نمی‌تواند صرفاً نگاشت همانی را بیاموزد؟",
 "Because the noise is assumed conditionally pixel-wise independent given the signal, so the neighbouring pixels carry no information about the value of that pixel's own noise — it is impossible to beat the a priori expected value. The signal, by contrast, is assumed to have statistical dependencies between nearby pixels, so it *can* be estimated from the surroundings. The network can therefore learn the signal and cannot learn the noise. In practice N2V does not build a true blind-spot architecture: it replaces the centre value of each input patch with a randomly selected value from the surrounding area, and computes the loss only at those masked pixels — 64 of them per 64×64 patch. The obvious failure case is spatially correlated noise, which is exactly what resizing, demosaicing and JPEG all produce. [N2V19 §3.1, §3.4, §3.5]",
 "چون فرض شده نویز به‌شرط سیگنال پیکسل‌به‌پیکسل مستقل است، پس پیکسل‌های همسایه هیچ اطلاعاتی دربارهٔ مقدار نویزِ خودِ آن پیکسل ندارند — شکست‌دادن مقدار مورد انتظار پیشین ناممکن است. در مقابل، فرض شده سیگنال میان پیکسل‌های نزدیک وابستگی آماری دارد، پس **می‌توان** آن را از اطراف تخمین زد. بنابراین شبکه می‌تواند سیگنال را بیاموزد و نمی‌تواند نویز را بیاموزد. در عمل N2V معماری نقطه‌کور واقعی نمی‌سازد: مقدار مرکز هر وصلهٔ ورودی را با مقداری تصادفی از ناحیهٔ اطراف جایگزین می‌کند و زیان را فقط روی همان پیکسل‌های ماسک‌شده حساب می‌کند — ۶۴ پیکسل در هر وصلهٔ ۶۴×۶۴. حالت شکست بدیهی، نویز همبستهٔ مکانی است، که دقیقاً همان چیزی است که تغییر اندازه، دی‌موزاییک و JPEG تولید می‌کنند."),

("branch", "Is P2N just a new loss function?",
 "آیا P2N فقط یک تابع زیان جدید است؟",
 "No, and the distinction matters. A loss function scores a fixed prediction against a fixed target. P2N changes the whole supervision signal in three ways. It changes what goes into the network — y⁺ and y⁻ are constructed from the model's own output and do not exist until the model has run once. It changes how many forward passes there are — three, not one. And it changes which pair is compared — output against output, not output against target. The architecture, meanwhile, is untouched: the class in the repository is literally named UNet_n2n_un and matches the 2018 Noise2Noise channel widths. [P2N25; repository Li-Tong-621/P2N-plus, measured]",
 "خیر، و این تمایز مهم است. تابع زیان یک پیش‌بینی ثابت را در برابر یک هدف ثابت امتیاز می‌دهد. P2N کل سیگنال نظارت را از سه جهت تغییر می‌دهد. آنچه وارد شبکه می‌شود عوض می‌شود — y⁺ و y⁻ از خروجی خودِ مدل ساخته می‌شوند و تا پیش از یک‌بار اجرای مدل اصلاً وجود ندارند. تعداد عبورهای رو به جلو عوض می‌شود — سه بار، نه یک بار. و اینکه کدام زوج مقایسه می‌شود عوض می‌شود — خروجی در برابر خروجی، نه خروجی در برابر هدف. در همین حال معماری دست‌نخورده است: نام کلاس در مخزن عیناً UNet_n2n_un است و با عرض کانال‌های Noise2Noise سال ۲۰۱۸ مطابقت دارد."),

("arch", "Show me where Restormer's attention is actually linear.",
 "نشان دهید توجه Restormer دقیقاً کجا خطی است.",
 "restormer_arch.py, class Attention, forward. After the 1×1 and 3×3 depth-wise projections, three einops calls rearrange q, k and v with the pattern 'b (head c) h w -> b head c (h w)'. That puts pixels on the last axis and channels second-to-last — the opposite of standard spatial attention. So q @ k.transpose(-2,-1) has shape (C/head) × (C/head), not (HW) × (HW). At level 1 with dim=48 and one head that is a 48×48 matrix regardless of image size. F.normalize along the pixel axis makes the product a cosine similarity between channels, which is the cross-covariance the paper describes, and self.temperature is a learned per-head scale replacing 1/√d_k. [measured — Restormer commit 68dc6ac]",
 "در فایل restormer_arch.py، کلاس Attention، متد forward. پس از تصویرسازی‌های ۱×۱ و ۳×۳ عمق‌جدا، سه فراخوانی einops مقادیر q، k و v را با الگوی 'b (head c) h w -> b head c (h w)' بازچینش می‌کنند. این کار پیکسل‌ها را روی آخرین محور و کانال‌ها را روی یکی‌مانده‌به‌آخر می‌گذارد — برعکس توجه مکانی متعارف. پس q @ k.transpose(-2,-1) ابعاد (C/head) × (C/head) دارد، نه (HW) × (HW). در سطح یک با dim=48 و یک سر، این ماتریسی ۴۸×۴۸ است، صرف‌نظر از اندازهٔ تصویر. F.normalize در راستای محور پیکسل، حاصل‌ضرب را به شباهت کسینوسی میان کانال‌ها تبدیل می‌کند که همان کوواریانس متقابل مورد اشارهٔ مقاله است، و self.temperature یک مقیاس آموخته‌شده به‌ازای هر سر است که جای ۱ بر جذر d_k را می‌گیرد."),

("arch", "Why is NAFNet faster than Restormer with 4.4× the parameters?",
 "چرا NAFNet با ۴٫۴ برابر پارامتر از Restormer سریع‌تر است؟",
 "Because parameters do not determine latency; arithmetic intensity and memory layout do. NAFNet is 1×1 and depth-wise convolutions, which map onto highly optimised GEMM kernels. Restormer's three rearrange calls force tensor-layout changes, and its attention matmuls are poorly served by a CPU backend. Measured in our container at 256×256: Restormer 10.436 s at 26.127 M parameters, NAFNet 1.899 s at 115.983 M. The practical conclusion is that any claim of the form 'model X is more efficient' is meaningless without naming the metric — parameters, MACs, or wall-clock — and the device. Note also that NAFNet's size is nearly all bottleneck: the 12 middle blocks run at 1024 channels, and 12 × 7 × 1024² ≈ 88 M of the 116 M sits there. [measured]",
 "چون پارامترها تأخیر را تعیین نمی‌کنند؛ شدت محاسباتی و چیدمان حافظه تعیین می‌کنند. NAFNet از کانولوشن‌های ۱×۱ و عمق‌جدا ساخته شده که روی هسته‌های بهینهٔ GEMM می‌نشینند. سه فراخوانی rearrange در Restormer چیدمان تنسور را تغییر می‌دهند و ضرب‌های ماتریسی توجه روی پشتیبان CPU به‌خوبی اجرا نمی‌شوند. اندازه‌گیری ما در ۲۵۶×۲۵۶: Restormer ‏۱۰٫۴۳۶ ثانیه با ۲۶٫۱۲۷ میلیون پارامتر، NAFNet ‏۱٫۸۹۹ ثانیه با ۱۱۵٫۹۸۳ میلیون. نتیجهٔ عملی این است که هر ادعایی به شکل «مدل X کارآمدتر است» بدون نام‌بردن معیار — پارامتر، MAC یا زمان دیواری — و سخت‌افزار، بی‌معناست. ضمناً حجم NAFNet تقریباً تماماً در گلوگاه است: ۱۲ بلوک میانی روی ۱۰۲۴ کانال کار می‌کنند و ۱۲ × ۷ × ۱۰۲۴² ≈ ۸۸ میلیون از ۱۱۶ میلیون همان‌جاست."),

("arch", "Is channel attention really 'global'? It sounds like a weaker claim.",
 "آیا توجه کانالی واقعاً «سراسری» است؟ ادعای ضعیف‌تری به نظر می‌رسد.",
 "It is global in the sense that every channel is computed from every pixel, so channel statistics carry image-wide information, and weighting channels by their mutual covariance implicitly encodes global relationships. It is not pairwise pixel attention, and Restormer never claims it is — the paper says the contextualised global relationships are *implicitly* modelled. The empirical case is the ablation: MDTA gives +0.32 dB over a UNet-with-Resblocks baseline on Urban100 at σ=50, and the depth-wise convolution inside it is worth another 0.15. Whether that is 'really global' is a fair philosophical objection; what is not in doubt is that it recovers most of the non-locality gap, since Restormer's Urban100 gain over DnCNN is 1.98 dB. [Restormer22 §3.1, Tables 4 and 7]",
 "به این معنا سراسری است که هر کانال از همهٔ پیکسل‌ها محاسبه می‌شود، پس آمار کانال اطلاعات کل تصویر را حمل می‌کند و وزن‌دهی کانال‌ها بر اساس کوواریانس متقابلشان، روابط سراسری را به‌طور ضمنی رمزگذاری می‌کند. این توجه پیکسل‌به‌پیکسل نیست و Restormer هم چنین ادعایی نمی‌کند — مقاله می‌گوید روابط سراسری زمینه‌مند به‌طور **ضمنی** مدل می‌شوند. شاهد تجربی همان مطالعهٔ حذفی است: MDTA روی Urban100 در سیگما ۵۰ مقدار ۰٫۳۲ دسی‌بل نسبت به پایهٔ UNet با بلوک پسماند می‌افزاید، و کانولوشن عمق‌جدای درون آن ۰٫۱۵ دسی‌بل دیگر ارزش دارد. اینکه آیا این «واقعاً سراسری» است ایراد فلسفی منصفانه‌ای است؛ آنچه تردیدی در آن نیست این است که بیشترِ شکاف غیرمحلی را جبران می‌کند، چون دستاورد Restormer روی Urban100 نسبت به DnCNN ‏۱٫۹۸ دسی‌بل است."),

("code", "What did the code tell you that the papers did not?",
 "کد چه چیزی به شما گفت که مقالات نگفتند؟",
 "Four things. First, padding constants differ by a factor of eight — Restormer requires multiples of 8 with reflect padding, NAFNet 16 with zero padding, P2N+ 32 with reflect, SCUNet 64 with ReplicationPad2d — which matters the moment two are chained, and zero padding injects an artificial edge the others do not. Second, P2N's Symmetric Prior Injection *reduces* parameters 6.7% while *raising* latency 2.5×, because every layer is evaluated twice, on x and on −x — the opposite of what a parameter table predicts. Third, MambaIR cannot be imported at all without compiled CUDA extensions. Fourth, MambaIR's own changelog records that published complexity figures computed with thop were wrong. None of this is visible from any abstract. [measured]",
 "چهار چیز. اول، ثابت‌های لایه‌گذاری هشت برابر با هم فرق دارند — Restormer مضارب ۸ با لایه‌گذاری بازتابی، NAFNet مضارب ۱۶ با لایه‌گذاری صفر، P2N+ مضارب ۳۲ بازتابی، و SCUNet مضارب ۶۴ با ReplicationPad2d — و این لحظه‌ای اهمیت پیدا می‌کند که دو مدل پشت سر هم قرار گیرند، ضمن اینکه لایه‌گذاری صفر لبه‌ای مصنوعی می‌سازد که بقیه نمی‌سازند. دوم، Symmetric Prior Injection در P2N پارامترها را ۶٫۷٪ **کم** و تأخیر را ۲٫۵ برابر **زیاد** می‌کند، چون هر لایه دو بار روی x و ‎−x ارزیابی می‌شود — برعکس چیزی که جدول پارامتر پیش‌بینی می‌کند. سوم، MambaIR بدون افزونه‌های کامپایل‌شدهٔ CUDA اصلاً import نمی‌شود. چهارم، تغییرنامهٔ خودِ MambaIR ثبت کرده که ارقام پیچیدگی منتشرشده که با thop حساب شده بودند نادرست بوده‌اند. هیچ‌کدام از این‌ها از چکیدهٔ هیچ مقاله‌ای پیدا نیست."),

("code", "Did you verify any of the PSNR numbers yourself?",
 "آیا هیچ‌یک از اعداد PSNR را خودتان راستی‌آزمایی کردید؟",
 "No, and we say so explicitly on the methodology slide. Every quality metric in this deck is reproduced from a published table, with the paper and table named. Our own measurements cover parameter counts and CPU forward-pass latency only, and they used random tensors, so they carry no image-quality information whatsoever. We kept the two in separate tables deliberately. Doing our own PSNR evaluation correctly would require matching each paper's crop, border, colour-space and rounding conventions, and a table mixing our numbers with theirs would be worse than useless. Where rows compare two methods, we take both from the same table — for example both DnCNN and Restormer from Restormer's Table 4 — so we are not comparing two different evaluation scripts.",
 "خیر، و این را صریحاً در اسلاید روش‌شناسی می‌گوییم. هر معیار کیفیتی در این مجموعه از جدولی منتشرشده بازتولید شده، با ذکر نام مقاله و جدول. اندازه‌گیری‌های خودِ ما فقط شمار پارامترها و تأخیر عبور رو به جلو روی CPU را پوشش می‌دهند و از تنسورهای تصادفی استفاده کرده‌اند، پس هیچ اطلاعاتی دربارهٔ کیفیت تصویر ندارند. ما عمداً این دو را در جدول‌های جداگانه نگه داشتیم. انجام درست ارزیابی PSNR توسط خودمان نیازمند تطبیق قراردادهای برش، حاشیه، فضای رنگ و گردکردنِ هر مقاله است، و جدولی که اعداد ما را با اعداد آن‌ها مخلوط کند بدتر از بی‌فایده است. جایی که یک ردیف دو روش را مقایسه می‌کند، هر دو را از یک جدول برداشته‌ایم — مثلاً هم DnCNN و هم Restormer از جدول ۴ مقالهٔ Restormer — تا دو اسکریپت ارزیابی متفاوت را با هم مقایسه نکنیم."),

("code", "Why did you not use DnCNN's own repository as the main code exhibit?",
 "چرا مخزن خودِ DnCNN را نمایشگاه اصلی کد قرار ندادید؟",
 "Two reasons. The original is MatConvNet, a MATLAB library, and the brief scopes the code deep-dive to *modern* approaches — so DnCNN appears as the measured baseline the modern repositories are contrasted against, which is the role Stage 1 assigned it. But the MATLAB fact is itself an exhibit: essentially nothing in modern denoising is MATLAB, and tracing that migration — MATLAB to TensorFlow in 2018, then PyTorch from 2019 onward, hard-coded scripts to argparse to YAML resolved by a BasicSR registry — is a direct answer to the brief's question about how pre-trained weights are used today compared with older methods. For the code itself we used KAIR, which is by DnCNN's own first author and is the PyTorch reference the field actually uses.",
 "دو دلیل. نسخهٔ اصلی با MatConvNet نوشته شده که کتابخانه‌ای متلبی است، و شرح پروژه، غواصی در کد را به رویکردهای **مدرن** محدود می‌کند — پس DnCNN به‌عنوان خط پایهٔ اندازه‌گیری‌شده‌ای ظاهر می‌شود که مخازن مدرن با آن مقایسه می‌شوند، همان نقشی که مرحلهٔ یک به آن داد. اما خودِ متلبی‌بودن یک نمایشگاه است: عملاً هیچ چیز در نویززدایی مدرن متلبی نیست، و ردیابی این کوچ — از متلب به TensorFlow در ۲۰۱۸ و سپس PyTorch از ۲۰۱۹ به بعد، از اسکریپت‌های سخت‌کدشده به argparse و سپس YAML که رجیستری BasicSR آن را حل می‌کند — پاسخی مستقیم به پرسش شرح پروژه دربارهٔ نحوهٔ استفادهٔ امروزی از وزن‌های از پیش‌آموزش‌دیده در مقایسه با روش‌های قدیمی است. برای خودِ کد از KAIR استفاده کردیم که کار نویسندهٔ اول همان DnCNN است و مرجع پای‌تورچی است که این حوزه واقعاً از آن استفاده می‌کند."),

("compare", "Which model would you deploy?",
 "کدام مدل را مستقر می‌کنید؟",
 "Name the constraint first — that is the honest answer and it is what the fork in our timeline predicts. Real photographs with a GPU and paired data: NAFNet, 40.30 dB on SIDD and the best accuracy-per-millisecond we measured, with by far the simplest code. CPU- or memory-bound: SCUNet at 9.663 M parameters, whose synthetic-degradation training makes the blind weights robust on photographs that were resized or JPEG-compressed before you ever saw them. Maximum quality on repetitive structure: Restormer, or MambaIR if CUDA is guaranteed. No clean data at all: P2N, or ZS-N2N for a single image, accepting per-image test-time optimisation as the price. A dependency-free baseline: BM3D, still — it needs no data and no GPU and it still beats an AWGN-trained DnCNN on real sensor noise by 1.99 dB. Five constraints, five answers, all current.",
 "اول محدودیت را نام ببرید — این پاسخ صادقانه است و همان چیزی است که انشعاب خط زمانی ما پیش‌بینی می‌کند. عکس‌های واقعی با GPU و دادهٔ زوج: NAFNet، با ۴۰٫۳۰ دسی‌بل روی SIDD و بهترین دقت به‌ازای میلی‌ثانیه‌ای که اندازه گرفتیم، و به‌مراتب ساده‌ترین کد. محدودیت CPU یا حافظه: SCUNet با ۹٫۶۶۳ میلیون پارامتر، که آموزش با تخریب مصنوعی، وزن‌های کورش را روی عکس‌هایی که پیش از دیدن شما تغییر اندازه یا فشرده‌سازی JPEG شده‌اند مقاوم می‌کند. بیشترین کیفیت روی ساختار تکرارشونده: Restormer، یا MambaIR اگر CUDA تضمین‌شده باشد. نبودِ کامل دادهٔ تمیز: P2N، یا ZS-N2N برای یک تصویر واحد، با پذیرش بهینه‌سازی زمان آزمون برای هر تصویر به‌عنوان بها. یک خط پایهٔ بدون وابستگی: همچنان BM3D — که نه داده می‌خواهد نه GPU و هنوز روی نویز حسگر واقعی ۱٫۹۹ دسی‌بل از DnCNNِ آموزش‌دیده با AWGN بهتر است. پنج محدودیت، پنج پاسخ، همه به‌روز."),

("compare", "Has the field actually progressed since DnCNN?",
 "آیا این حوزه واقعاً از زمان DnCNN پیشرفت کرده است؟",
 "It depends entirely on which benchmark you ask. On BSD68 at σ=50, DnCNN to Restormer is 26.23 to 26.62 — 0.39 dB in five years, which is saturation. On Urban100 at the same noise level it is 26.35 to 28.33 — 1.98 dB. On real sensor noise it is 23.66 to 40.02 — more than sixteen decibels. So the honest summary is that progress in denoising since 2017 is mostly not progress on the 2017 problem. The field changed which question it was answering: from 'remove additive white Gaussian noise from a natural image' to 'handle long-range self-similarity' and then to 'handle the noise a real camera actually produces'. A benchmark that cannot distinguish 2017 from 2022 is no longer measuring what the field is working on.",
 "کاملاً بستگی دارد از کدام محک بپرسید. روی BSD68 در سیگما ۵۰، از DnCNN تا Restormer یعنی ۲۶٫۲۳ تا ۲۶٫۶۲ — ۰٫۳۹ دسی‌بل در پنج سال، که یعنی اشباع. روی Urban100 در همان سطح نویز، ۲۶٫۳۵ تا ۲۸٫۳۳ — ۱٫۹۸ دسی‌بل. روی نویز حسگر واقعی، ۲۳٫۶۶ تا ۴۰٫۰۲ — بیش از شانزده دسی‌بل. پس خلاصهٔ صادقانه این است که پیشرفت نویززدایی از ۲۰۱۷ به بعد عمدتاً پیشرفت روی مسئلهٔ ۲۰۱۷ نیست. این حوزه پرسشی را که پاسخ می‌داد عوض کرد: از «نویز گاوسی سفید جمع‌شونده را از یک تصویر طبیعی حذف کن» به «خودتشابهی دوربرد را مدیریت کن» و سپس به «نویزی را که یک دوربین واقعی واقعاً تولید می‌کند مدیریت کن». محکی که نتواند ۲۰۱۷ را از ۲۰۲۲ تشخیص دهد، دیگر چیزی را که این حوزه روی آن کار می‌کند نمی‌سنجد."),

("meta", "What is still unsolved, and what would you research?",
 "چه چیزی هنوز حل نشده، و شما چه چیزی را پژوهش می‌کردید؟",
 "Unsolved: a general-purpose blind real denoiser — SCUNet's own abstract states it remains unsolved, and neither synthetic degradation nor SIDD-trained models generalise to an unseen camera with an unseen ISP. The perception–distortion trade-off, because L1, L2 and PSNR losses all recover a conditional mean and Noise2Noise itself names the resulting spatial blurriness. And no agreed cost metric — we produced three incompatible efficiency rankings of the same models. What I would research is our own observation: the two branches have never merged. P2N ships the 2018 Noise2Noise U-Net verbatim; Restormer, NAFNet and MambaIR all assume paired data. As far as we found, nobody has published a state-space or Transformer backbone trained under RDC/DCS supervision, so whether the branches compose or conflict is an open and apparently untested question.",
 "حل‌نشده‌ها: یک نویززدای کورِ همه‌منظوره برای تصاویر واقعی — چکیدهٔ خودِ SCUNet می‌گوید این مسئله حل‌نشده باقی مانده، و نه تخریب مصنوعی و نه مدل‌های آموزش‌دیده روی SIDD به دوربینی دیده‌نشده با ISP دیده‌نشده تعمیم نمی‌یابند. بده‌بستان ادراک–اعوجاج، چون توابع زیان L1 و L2 و PSNR همگی میانگین شرطی را بازیابی می‌کنند و خودِ Noise2Noise تاریِ مکانی حاصل را نام می‌برد. و نبود معیار هزینهٔ مورد توافق — ما سه رتبه‌بندی کارایی ناسازگار از همان مدل‌ها تولید کردیم. آنچه من پژوهش می‌کردم مشاهدهٔ خودمان است: این دو شاخه هرگز به هم نپیوسته‌اند. P2N همان U-Net سال ۲۰۱۸ را عیناً عرضه می‌کند؛ Restormer و NAFNet و MambaIR همگی دادهٔ زوج را فرض می‌گیرند. تا جایی که ما یافتیم، کسی ستون فقرات فضای‌حالت یا ترنسفورمری را تحت نظارت RDC/DCS منتشر نکرده است، پس اینکه این دو شاخه با هم ترکیب می‌شوند یا تعارض دارند، پرسشی باز و ظاهراً آزموده‌نشده است."),

("meta", "Your source list includes a venue not on the brief's named list.",
 "فهرست منابع شما شامل محل انتشاری است که در فهرست نام‌برده‌شدهٔ شرح پروژه نیست.",
 "Correct, and we flag it ourselves on the limitations slide rather than leaving it to be found. SCUNet appeared in *Machine Intelligence Research*, volume 20 issue 6, 2023 — a peer-reviewed Springer journal, but not among the venues the brief names. We read the brief's list as illustrative rather than exhaustive, since it is introduced with 'e.g.'. If the assessment requires strict adherence to the named list, SCUNet can be moved to Category B without breaking the quota: we would still have 11 Category A of 15, which is 73.3%, above the 70% floor. We would rather raise that arithmetic than have it raised for us.",
 "درست است، و ما خودمان آن را در اسلاید محدودیت‌ها علامت می‌زنیم به‌جای آنکه بگذاریم کشف شود. SCUNet در نشریهٔ Machine Intelligence Research، جلد ۲۰ شمارهٔ ۶، سال ۲۰۲۳ منتشر شده — یک نشریهٔ داوری‌شدهٔ اشپرینگر، اما نه در میان محل‌هایی که شرح پروژه نام می‌برد. ما فهرست شرح پروژه را نمونه‌وار می‌خوانیم نه جامع، چون با «مثلاً» معرفی شده است. اگر ارزیابی پایبندی سخت‌گیرانه به آن فهرست را لازم بداند، SCUNet می‌تواند بدون شکستن سهمیه به دستهٔ B منتقل شود: آنگاه همچنان ۱۱ منبع دستهٔ A از ۱۵ داریم، یعنی ۷۳٫۳٪، بالاتر از کف ۷۰٪. ترجیح می‌دهیم خودمان این حساب را مطرح کنیم تا اینکه برایمان مطرح شود."),

("meta", "Why does your narrative end without a winner?",
 "چرا روایت شما بدون برنده تمام می‌شود؟",
 "Because a narrative that ended 'and then X won' would be false. Three architectural answers to the third bottleneck were published across three years — Restormer in 2022, NAFNet in 2022, MambaIR in 2024 — and none has displaced the others: Restormer leads Urban100, NAFNet leads SIDD, MambaIR leads DND by a hundredth of a decibel. SCUNet answers the same problem from the data side entirely. Meanwhile bottleneck two is mitigated, not closed: self-supervision still trails supervision. Ending on an open question is what distinguishes a synthesis from a literature review, and the brief grades synthesis. It also happens to be true, which is the better reason.",
 "چون روایتی که با «و سپس X برنده شد» تمام شود نادرست است. سه پاسخ معماری به گلوگاه سوم در طول سه سال منتشر شدند — Restormer در ۲۰۲۲، NAFNet در ۲۰۲۲، MambaIR در ۲۰۲۴ — و هیچ‌کدام دیگری را کنار نزده است: Restormer در Urban100 پیشتاز است، NAFNet در SIDD، و MambaIR در DND با اختلاف یک‌صدم دسی‌بل. SCUNet هم همان مسئله را کاملاً از سمت داده پاسخ می‌دهد. در همین حال گلوگاه دو تخفیف یافته، نه بسته شده: خودنظارتی هنوز از بانظارت عقب است. پایان‌دادن به یک پرسش باز همان چیزی است که سنتز را از مرور ادبیات جدا می‌کند، و شرح پروژه سنتز را نمره می‌دهد. ضمناً اتفاقاً درست هم هست، که دلیل بهتری است."),
]

GROUPS = [("core","The anchor paper","مقالهٔ لنگر"),
          ("branch","The data branch","شاخهٔ داده"),
          ("arch","The architecture branch","شاخهٔ معماری"),
          ("code","Engineering & code","مهندسی و کد"),
          ("compare","Comparison & deployment","مقایسه و استقرار"),
          ("meta","Method & scope","روش و دامنه")]

# ═══════════════ RENDER ═══════════════
blocks = []
for b in SCRIPT:
    def paras(t): return ''.join('<p>%s</p>' % e(p).replace('**','') for p in t.split('\n\n'))
    def parasb(t):
        import re as _re
        out=[]
        for p in t.split('\n\n'):
            p=e(p)
            p=_re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', p)
            out.append('<p>%s</p>'%p)
        return ''.join(out)
    blocks.append("""
<article class="blk">
 <div class="bh">
  <div class="bn">%d</div>
  <div class="bt"><h3 class="en">%s</h3><h3 class="fa">%s</h3>
   <div class="bmeta"><span>%s</span><span>%s</span><span class="sl">Slides %s</span></div></div>
 </div>
 <div class="cols">
  <div class="en script">%s</div>
  <div class="fa script" dir="rtl">%s</div>
 </div>
 <div class="cue"><div class="en"><b>Cue.</b> %s</div><div class="fa" dir="rtl"><b>یادآوری.</b> %s</div></div>
 <div class="cue exp"><div class="en"><b>Slack.</b> %s</div><div class="fa" dir="rtl"><b>وقت اضافه.</b> %s</div></div>
</article>""" % (b['n'], e(b['t']), e(b['tf']), e(b['min']), e(b['dur']), e(b['slides']),
                 parasb(b['s']), parasb(b['sf']), e(b['c']), e(b['cf']), e(b['x']), e(b['xf'])))

qa_html = []
for gid, gname, gfa in GROUPS:
    items = [q for q in QA if q[0] == gid]
    if not items: continue
    qa_html.append('<h4 class="qg"><span class="en">%s</span><span class="fa" dir="rtl">%s</span></h4>' % (e(gname), e(gfa)))
    for _, qen, qfa, aen, afa in items:
        qa_html.append("""<details class="qa">
<summary><span class="en">%s</span><span class="fa" dir="rtl">%s</span></summary>
<div class="cols"><div class="en">%s</div><div class="fa" dir="rtl">%s</div></div></details>"""
        % (e(qen), e(qfa), e(aen), e(afa)))

CSS = """
:root{--ink:#0F1418;--body:#2E353D;--soft:#525C67;--muted:#717C89;--rule:#E2E7EC;--tint:#F5F7F9;--accent:#BF4419;--dark:#0F1418}
*{box-sizing:border-box}
body{margin:0;background:#E7EBEF;color:var(--ink);font-family:Calibri,Carlito,"Segoe UI",system-ui,sans-serif;font-size:17px}
.fa{font-family:Vazirmatn,"Noto Naskh Arabic","IRANSans",Tahoma,sans-serif;line-height:2.0;font-size:15.5px}
h1,h2,h3,h4{font-family:Cambria,Caladea,Georgia,serif;margin:0}
#bar{position:sticky;top:0;background:rgba(15,20,25,.97);color:#C7D2DC;display:flex;
align-items:center;gap:12px;padding:10px 20px;font-size:12.5px;z-index:20;flex-wrap:wrap}
#bar b{color:#fff}
#bar button{background:#1E2731;color:#C7D2DC;border:1px solid #2E3A46;border-radius:4px;
padding:5px 12px;font-size:12px;cursor:pointer;font-family:inherit}
#bar button.on{background:var(--accent);color:#fff;border-color:var(--accent)}
main{max-width:1180px;margin:0 auto;padding:24px 20px 90px}
.hero{background:var(--dark);color:#E7EDF3;border-radius:6px;padding:30px 34px;margin-bottom:22px}
.hero h1{font-size:34px;color:#fff;margin-bottom:10px}
.hero p{font-size:15px;color:#B9C4CF;line-height:1.6;max-width:80ch;margin:0 0 6px}
.hero .tag{font-size:11px;letter-spacing:1.6px;color:var(--accent);font-weight:700;margin-bottom:10px}
.blk{background:#fff;border-radius:6px;padding:22px 26px;margin-bottom:16px;
box-shadow:0 1px 3px rgba(16,24,32,.08)}
.bh{display:flex;gap:16px;align-items:flex-start;border-bottom:1px solid var(--rule);
padding-bottom:14px;margin-bottom:16px}
.bn{width:38px;height:38px;border-radius:50%;background:var(--accent);color:#fff;flex:none;
display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px}
.bt h3{font-size:21px;line-height:1.24}
.bt h3.fa{color:var(--muted);font-size:16px;font-weight:400;margin-top:3px}
.bmeta{margin-top:7px;display:flex;gap:14px;font-size:11.5px;color:var(--muted)}
.bmeta .sl{color:var(--accent);font-weight:600}
.cols{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:26px}
.script p{font-size:17px;line-height:1.64;color:var(--body);margin:0 0 13px}
.script.fa p{line-height:2.0;font-size:17px}
.script b,.cue b{color:var(--ink)}
.cue{margin-top:15px;background:var(--tint);border-left:4px solid var(--rule);border-radius:0;
padding:12px 16px;font-size:13.6px;color:var(--body)}
.cue .cols{gap:22px}
body.en-only .fa,body.fa-only .en{display:none}
body.en-only .cols,body.fa-only .cols{grid-template-columns:minmax(0,1fr)}
h2.sec{font-size:28px;margin:34px 0 14px}
.qg{font-size:17px;color:var(--accent);margin:22px 0 8px;display:flex;gap:12px;align-items:baseline}
.qg .fa{font-size:13px;color:var(--muted)}
details.qa{background:#fff;border-radius:5px;margin-bottom:8px;
box-shadow:0 1px 2px rgba(16,24,32,.07);overflow:hidden}
details.qa summary{cursor:pointer;padding:15px 20px;font-weight:600;font-size:15.5px;
display:flex;flex-direction:column;gap:3px;list-style:none}
details.qa summary::-webkit-details-marker{display:none}
details.qa summary .fa{font-weight:400;color:var(--muted);font-size:14px}
details.qa[open] summary{border-bottom:1px solid var(--rule);background:var(--tint)}
details.qa .cols{padding:17px 20px 20px;font-size:16px;line-height:1.62;color:var(--body)}
details.qa .cols .fa{line-height:1.95}
.budget{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:18px 0}
.budget div{background:#18202A;border:1px solid #2C3947;border-radius:5px;padding:11px 13px}
.budget b{display:block;font-family:Cambria,Georgia,serif;font-size:24px;color:var(--accent)}
.budget span{display:block;font-size:11px;color:#9FB0BE;margin-top:4px;line-height:1.35}
.cue.exp{background:#FCF3EE;border-left-color:var(--accent)}
@media print{#bar{display:none}body{background:#fff}.blk,details.qa{box-shadow:none;border:1px solid var(--rule)}
details.qa .cols{display:grid !important}}
@media(max-width:900px){.cols{grid-template-columns:minmax(0,1fr)}.budget{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:520px){#bar{flex-wrap:wrap;height:auto;padding:8px 14px;row-gap:6px}
 #bar span{flex-basis:100%}}
"""

JS = """
const B=document.body;
function mode(m){B.classList.remove('en-only','fa-only');
 if(m!=='both')B.classList.add(m+'-only');
 document.querySelectorAll('#bar .lang').forEach(x=>x.classList.toggle('on',x.dataset.m===m));
 localStorage.setItem('s3lang',m);}
document.querySelectorAll('#bar .lang').forEach(x=>x.onclick=()=>mode(x.dataset.m));
mode(localStorage.getItem('s3lang')||'both');
document.getElementById('bOpen').onclick=()=>{
 const d=document.querySelectorAll('details.qa');
 const any=[...d].some(x=>!x.open); d.forEach(x=>x.open=any);};
document.getElementById('bPrint').onclick=()=>window.print();
"""

DOC = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Stage 3 Defence — Presenter Companion · همراه ارائه‌دهنده</title>
<link href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css" rel="stylesheet">
<style>%s</style></head><body>
<div id="bar"><b>Stage 3 · Presenter Companion</b>
<button class="lang" data-m="both">EN + FA</button>
<button class="lang" data-m="en">English</button>
<button class="lang" data-m="fa">فارسی</button>
<button id="bOpen">Expand Q&amp;A</button>
<button id="bPrint">Print</button>
<span style="flex:1"></span><span>%s scripted · 8 blocks · %d questions</span></div>
<main>
<div class="hero">
 <div class="tag">IMAGE DENOISING · FINAL DEFENCE · 31 AUGUST 2026</div>
 <h1>Condensed 30-minute script, and the question bank</h1>
 <p>The master deck is 100 slides. This is the executive summary you actually deliver. Every block names the slides to show.</p>
 <div class="budget">
  <div><b>%s</b><span>scripted core, at 125 wpm</span></div>
  <div><b>30:00</b><span>slot</span></div>
  <div><b>~8:00</b><span>slide navigation, pointing at tables, pauses</span></div>
  <div><b>rest</b><span>use the <i>Slack</i> line in each block, in order</span></div>
 </div>
 <p><b>How to use the slack.</b> Deliver the script first. It is written to be spoken, not read, and it is deliberately short of the slot so a slow start cannot cost you the conclusion. If you reach block 8 with time left, go back and deploy the <i>Slack</i> expansions in order — each is thirty to sixty seconds and each pre-empts a question that is likely to be asked anyway.</p>
 <p>Rule for the defence: <b>do not say anything you cannot defend from a primary source.</b> Where a claim is our own reading, the deck labels it, and so should you.</p>
</div>
%s
<h2 class="sec">Anticipated technical questions</h2>
%s
</main>
<script>%s</script></body></html>""" % (CSS, "%d:%02d" % (SPOKEN//60, SPOKEN%60), len(QA),
    "%d:%02d" % (SPOKEN//60, SPOKEN%60), ''.join(blocks), ''.join(qa_html), JS)

io.open('/home/claude/work/out/defence.html','w',encoding='utf-8').write(DOC)

# timing check
tot = 0
for b in SCRIPT:
    m, s = b['dur'].split(':'); tot += int(m)*60 + int(s)
print("blocks:", len(SCRIPT), "| questions:", len(QA), "| scripted:", "%d:%02d" % (tot//60, tot % 60))
words = sum(len(b['s'].split()) for b in SCRIPT)
print("English words:", words, "→ at 135 wpm ≈ %d:%02d" % (words//135, (words*60//135) % 60))
