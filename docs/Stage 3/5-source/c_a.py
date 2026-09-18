# -*- coding: utf-8 -*-
S = []

# ══════════════════════════ FRONT MATTER ══════════════════════════
S.append(dict(t="title", era="meta", part="", kicker="Digital Image Processing · Final Project · Stage 3",
    title="Image Denoising:\nFrom Foundations to State-of-the-Art",
    lead="Eighteen years in which the image prior moved out of human hands — from a hand-written penalty term, into a file of learned weights, and then into a per-image optimisation that needs no clean data at all.",
    body={"meta": [
        ("Anchor paper", "DnCNN — Zhang, Zuo, Chen, Meng & Zhang\nIEEE TIP 26(7), 2017"),
        ("Sources", "15 total · 12 Category A (80.0%)\n3 Category B (20.0%) · 2007 → 2025"),
        ("Structure", "Four eras · three bottlenecks\nOne fork, in 2018"),
        ("Supervisor", "Prof. Zohreh Azimifar\nFinal defence: 31 August 2026"),
    ]},
    cite="Assignment brief, July 2026",
    notes="Open on the thesis, not on the agenda. One sentence: this deck is not ten paper summaries, it is one argument about where the image prior lives and who writes it. Everything that follows is evidence for that sentence."))

S.append(dict(t="content", era="meta", part="", kicker="How to read this deck",
    title="Every claim carries its source",
    lead="The deck is built to be interrogated. Each slide names where its numbers and its statements come from, so any single claim can be traced back to a primary source in one step.",
    body={"bullets": [
        "**Paper tags** — a bracketed short name and, where relevant, the exact table: `[DnCNN17 · Table II]`, `[Restormer22 · Table 6]`. Numbers reproduced from a paper are never rounded, reshaped, or averaged across papers.",
        "**`[measured]`** — figures produced by us, in a container, from the repositories themselves. Method and hardware are stated on the slide that reports them.",
        "**`[brief]`** — the assignment brief, *From Foundations to State-of-the-Art: A Comprehensive Synthesis*, Prof. Zohreh Azimifar, July 2026.",
        "**`[reading]`** — our interpretation, analogy, or teaching device. Labelled separately because it is *not* a source claim and should not be defended as one.",
        "Where a figure could not be verified, it is absent. No number in this deck was estimated, inferred from a plot, or carried across from a secondary citation."
    ]},
    cite="brief",
    notes="Say this out loud in the defence: the honesty convention is itself a graded artefact. The TA can pick any slide and ask 'where is this from' and the slide answers before you do."))

S.append(dict(t="cards", era="meta", part="", kicker="The argument in four moves",
    title="One thesis, stated before the evidence",
    lead="Image denoising is the cleanest available case study in how computer vision replaced hand-designed priors with learned ones — because in denoising, unusually, the prior is written down explicitly and you can watch it move.",
    body={"cards": [
        {"tag": "ERA I → II", "h": "Bottleneck 1 · Manual prior design",
         "p": "Classical methods solve an optimisation *per image* with a hand-written penalty Φ. WNNM needs 773 s for one 512×512 image. The prior is a human guess, and the guess costs minutes."},
        {"tag": "ERA II → III", "h": "Bottleneck 2 · The clean-data requirement",
         "p": "Discriminative learning removed test-time optimisation, but demanded paired clean/noisy corpora. For microscopy, astronomy, and medical imaging, that pairing does not exist and cannot be manufactured."},
        {"tag": "ERA III → IV/V", "h": "Bottleneck 3 · The receptive field",
         "p": "A 17-layer CNN sees 35×35 pixels. It cannot exploit a repeating pattern 200 pixels away — which is exactly what non-local classical methods were good at, and exactly where DnCNN loses."},
        {"tag": "TODAY", "h": "Three live answers, not one winner",
         "p": "Transformers (Restormer), pure convolution done right (NAFNet), and state-space models (MambaIR) each claim the third bottleneck. The field has not settled. That is the honest ending."},
    ]},
    cite="reading — each bottleneck named by the paper that broke it; see Parts II–V",
    notes="This is the slide to memorise. If you can deliver these four cards from memory with no slide behind you, the condensed 30-minute presentation is already half written."))

S.append(dict(t="table", era="meta", part="", kicker="Map of the deck",
    title="Eight parts, mapped onto the brief's required structure",
    lead="The brief specifies seven sections. This deck follows them in order, splitting the modern era into two parts because the field genuinely forked in 2018 and collapsing that fork would misrepresent it.",
    body={"cols": ["Part", "Contents", "Brief section", "Slides"],
          "align": "lllr",
          "rows": [
            ["I — The problem", "Degradation model, ill-posedness, MAP, PSNR/SSIM, benchmarks", "§1 Introduction & Problem Definition", "05–16"],
            ["II — Classical DIP", "Spatial filters → wavelets → TV → NLM → BM3D → WNNM", "§2 The Classical DIP Foundation", "17–38"],
            ["III — The transition", "MLP, unrolling, CSF, TNRD, and DnCNN in full", "§3 The Deep Learning Transition", "39–57"],
            ["IV — The data branch", "Noise2Noise → Noise2Void → ZS-N2N → P2N", "§4 Modern SOTA (supervision)", "58–68"],
            ["V — The architecture branch", "Attention, Restormer, NAFNet, SCUNet, MambaIR", "§4 Modern SOTA (architecture)", "69–87"],
            ["VI — Engineering reality", "Repositories, code, pipelines, weights, measurements", "§5 Practical Deep-Dive", "88–105"],
            ["VII — Comparative analysis", "PSNR/SSIM across 18 years; efficiency; real noise", "§6 Comparative Analysis", "106–114"],
            ["VIII — Open problems", "What is still unsolved, and what we would build today", "§7 Future Directions & Conclusion", "115–122"],
          ]},
    foot="Back matter — bibliography, verification notes, glossary, defence map: slides 123–127.",
    cite="brief §3, Guidelines for Structuring the Final Slide Deck",
    notes="Point at the third column. The TA wrote that column. Showing that the deck is indexed against their own structure removes an entire class of question."))

# ══════════════════════════ PART I ══════════════════════════
S.append(dict(t="section", era="meta", part="I", kicker="Part I",
    title="The Problem",
    lead="What denoising is, why it is mathematically impossible without an assumption, and how we agree to measure success.",
    body={"items": ["The degradation model", "Why the problem is ill-posed", "MAP and the birth of the prior",
                    "PSNR, SSIM, and what they hide", "The benchmark datasets", "Why denoising is foundational"]},
    cite="brief §1", notes="Thirty seconds. Say only: we cannot discuss eighteen years of solutions until the problem is stated precisely enough that the solutions are comparable."))

S.append(dict(t="math", era="meta", part="I", kicker="05 · The model",
    title="One equation, and it has never changed",
    lead="Every method in this deck — from a 3×3 box filter to a state-space model — is an attempt to invert the same two-term equation. The equation is stated identically in papers sixteen years apart.",
    body={"eqs": [
        {"tex": "y  =  x  +  v",
         "where": "y — the noisy observation the sensor produced · x — the latent clean image we want · v — the noise"},
        ],
     "bullets": [
        "DnCNN, 2017: the degradation model is written `y = x + v`, with v additive white Gaussian noise of standard deviation σ. `[DnCNN17 §I]`",
        "SCUNet, 2023: the same equation is written `y = x + n`, sixteen years after BM3D, in a Transformer paper. `[SCUNet23 Eq. 1]`",
        "Noise2Void, 2019, states it as a *joint distribution* instead: `p(s,n) = p(s)·p(n|s)`, with the signal s and noise n drawn together. That reformulation is what makes self-supervision possible — it is the same model, written so the assumptions are visible. `[N2V19 Eq. 1]`",
        "The constancy is the point. Eighteen years of progress changed nothing about the *problem statement* — only about who supplies the missing information needed to invert it.",
    ]},
    cite="DnCNN17 §I · SCUNet23 Eq. 1 · N2V19 Eq. 1",
    notes="If asked why so many methods are comparable at all: because they all target this exact equation on this exact benchmark. That is unusual in vision and it is why denoising is such a clean case study."))

S.append(dict(t="cards", era="meta", part="I", kicker="06 · Unpacking the assumption",
    title="Additive white Gaussian noise, one word at a time",
    lead="AWGN is the standard assumption, and almost every quantitative claim in this deck is made under it. It is also, as Part VII shows with hard numbers, the single assumption that breaks hardest on real photographs.",
    body={"cards": [
        {"tag": "Additive", "h": "v is added, not blended", "p": "Pixel 200 becomes 200 + ε. Not multiplied (speckle), not applied through a nonlinearity (compression), not signal-dependent (shot noise). The clean image is recoverable by subtraction alone — which is precisely what makes residual learning possible in Part III."},
        {"tag": "White", "h": "Spatially independent", "p": "Each pixel's noise is independent of its neighbours'. No spatial correlation, no structure. This assumption is what Noise2Void depends on for its blind spot to work, and it is the first thing resizing destroys."},
        {"tag": "Gaussian", "h": "Zero-mean bell curve", "p": "Small errors common, large errors rare, mean zero. Zero-mean is load-bearing: it is the whole of the Noise2Noise argument. Gaussianity is what makes batch normalisation and residual learning benefit each other in DnCNN."},
        {"tag": "σ", "h": "The noise level", "p": "The width of the bell. Benchmarks report σ ∈ {15, 25, 50} on 8-bit images. DnCNN-B trains blind across σ ∈ [0, 55]; SCUNet samples σ from {2/255 … 50/255}. σ = 15 is mild grain, σ = 50 is severe."},
    ]},
    cite="DnCNN17 §I, §III-D · SCUNet23 §3.2 · N2N18 §2 · N2V19 §3.1",
    notes="Flag the trap early: every one of these four words is a lie about a real camera. Part VII quantifies exactly how expensive that lie is — DnCNN scores 23.66 dB on real sensor noise."))

S.append(dict(t="two", era="meta", part="I", kicker="07 · Why it is hard",
    title="The problem is ill-posed — and no amount of compute fixes that",
    lead="Given y, infinitely many pairs (x, v) satisfy y = x + v. Arithmetic alone cannot choose between them. Every denoiser ever written is a rule for choosing, and the quality of a denoiser is the quality of its choosing rule.",
    body={"left": {"h": "The impossibility, stated plainly", "bullets": [
        "If I tell you two numbers sum to 10, you cannot recover them. 5+5, 3+7, 9.7+0.3 are all valid.",
        "A denoiser faces exactly that, once per pixel, with the extra constraint that the answers must be jointly plausible as a photograph.",
        "So the algorithm must *add information that is not in the measurement*. That added information is called the **prior**.",
        "There is no such thing as a prior-free denoiser. A method that claims not to have one has merely hidden it — in an architecture, in a training set, or in a stopping criterion.",
    ]},
     "right": {"h": "Why the field is a history of priors", "bullets": [
        "Classical era: the prior is a formula a human wrote. You can read it.",
        "Deep era: the prior is a tensor of weights induced from data. You cannot read it, but you can download it.",
        "Self-supervised era: the prior is partly *the test image itself*, exploited through its own internal statistics.",
        "This deck's organising question, and the question Stage 2 asked of every repository: **open the source file — where is the prior?**",
    ]},
    },
    cite="reading, following DnCNN17 §I on prior-based vs discriminative methods",
    notes="This is the conceptual hinge of the whole presentation. If the TA only remembers one framing from your defence, make it this one."))

S.append(dict(t="math", era="meta", part="I", kicker="08 · The classical formulation",
    title="From Bayes to the objective everyone optimises",
    lead="The classical era's answer to ill-posedness is Maximum a Posteriori estimation. The derivation is three lines, and it produces the exact two-term objective that BM3D, WNNM, TV and TNRD all instantiate differently.",
    body={"eqs": [
        {"tex": "x̂  =  arg max_x  p(x | y)  =  arg max_x  p(y | x) · p(x)",
         "where": "Bayes' rule. The posterior is the likelihood times the prior."},
        {"tex": "x̂  =  arg min_x  [ − log p(y | x)  −  log p(x) ]",
         "where": "Take negative logarithms: maximising a product becomes minimising a sum."},
        {"tex": "x̂  =  arg min_x   ½‖y − x‖²   +   λ · Φ(x)",
         "where": "data fidelity — stay near what the sensor saw     ·     the prior — look like a real image     ·     λ — how far you trust the prior"},
        ],
     "bullets": [
        "The first term follows directly from AWGN: if v ~ N(0, σ²I), then −log p(y|x) = ‖y − x‖²⁄2σ² plus a constant. The squared ℓ₂ penalty is *not* a modelling choice — it is what the Gaussian assumption forces.",
        "The second term, Φ, is entirely a modelling choice, and it is where the whole classical era lives. **Total variation** sets Φ(x) = ‖∇x‖₁. **Sparse coding** sets Φ(x) = ‖α‖₀ subject to x = Dα. **WNNM** sets Φ to a weighted nuclear norm on stacks of similar patches.",
        "λ trades the two off. Large λ → smooth and safe; small λ → sharp and noisy. In the classical era λ is a constant a human tunes; in the deep era it disappears entirely because the two terms are no longer separable.",
        "**Read the whole deck as: what is Φ, and who wrote it?**",
    ]},
    cite="Standard MAP derivation · consistent with DnCNN17 §I framing of prior-based methods",
    notes="Expect to be asked to derive the ½‖y−x‖² term from the Gaussian likelihood on a whiteboard. Practise it: −log of exp(−‖y−x‖²/2σ²) is ‖y−x‖²/2σ². The 1/σ² is absorbed into λ."))

S.append(dict(t="math", era="meta", part="I", kicker="09 · Metric 1",
    title="PSNR — what it measures, and what it cannot",
    lead="PSNR is the field's reporting currency. Every table in this deck is in decibels. Understanding its compression is the difference between reading those tables and being impressed by them.",
    body={"eqs": [
        {"tex": "MSE  =  (1 / MN) · Σ_i Σ_j [ x(i,j) − x̂(i,j) ]²",
         "where": "mean squared error between the estimate and the ground truth, over all MN pixels"},
        {"tex": "PSNR  =  10 · log₁₀ ( MAX² / MSE )    dB       =  20 · log₁₀ ( MAX ) − 10 · log₁₀ ( MSE )",
         "where": "MAX = 255 for 8-bit images. Higher is better. Identical images give MSE = 0 and PSNR = ∞."},
        ],
     "bullets": [
        "**The logarithm compresses everything.** Halving the MSE gains exactly 3.01 dB. A 0.6 dB gain — DnCNN's headline result over BM3D — corresponds to reducing MSE by about 13%. In a field where ten years of work moved the number by two decibels total, 0.6 dB is enormous.",
        "**Calibration you must know cold.** The DnCNN authors cite prior work finding that *few methods can outperform BM3D by more than 0.3 dB on average*, and that the estimated PSNR bound over BM3D is about 0.7 dB. DnCNN-S beat BM3D by 0.6 dB at all three noise levels — roughly 85% of the theoretically available headroom. `[DnCNN17 §IV-B]`",
        "**PSNR can be gamed by blurring.** On a noisy image, a Gaussian blur lowers MSE and therefore raises PSNR while visibly destroying texture. This is why a PSNR-only comparison is not a complete comparison, and why the field reports SSIM alongside.",
        "**PSNR is pixel-wise and has no model of perception.** Two images with identical PSNR can look entirely different if one has its error concentrated on an edge and the other has it spread over flat sky.",
    ]},
    cite="DnCNN17 §IV-B · standard definition",
    notes="Be ready for: 'why is 0.6 dB a big deal?' Answer with the 0.3 dB literature bound and the 0.7 dB estimated ceiling, both of which the DnCNN paper quotes explicitly. Do not answer with 'because the paper says so'."))

S.append(dict(t="math", era="meta", part="I", kicker="10 · Metric 2",
    title="SSIM — structure, not pixels",
    lead="SSIM was designed to punish exactly the failure mode PSNR rewards: the loss of local structure. It decomposes similarity into three comparisons and multiplies them.",
    body={"eqs": [
        {"tex": "SSIM(x, x̂)  =  [ l(x,x̂) ]^α · [ c(x,x̂) ]^β · [ s(x,x̂) ]^γ ,      α = β = γ = 1",
         "where": "luminance × contrast × structure, computed in a sliding local window and averaged"},
        {"tex": "SSIM  =  ( 2μ_x μ_x̂ + C₁ )( 2σ_xx̂ + C₂ )  /  ( μ_x² + μ_x̂² + C₁ )( σ_x² + σ_x̂² + C₂ )",
         "where": "μ — local means · σ² — local variances · σ_xx̂ — local covariance · C₁, C₂ — small stabilising constants"},
        ],
     "bullets": [
        "Range is [0, 1] for non-negative images; 1 means identical. Reported to three decimals in the literature — Restormer's real-noise SSIM on SIDD is 0.960. `[Restormer22 Table 6]`",
        "The structure term s = σ_xx̂ ⁄ (σ_x σ_x̂) is a local correlation coefficient. Blur reduces σ_x̂ and decorrelates the estimate from the reference, so blurring lowers SSIM even where it raises PSNR. That is the entire reason to report both.",
        "SSIM correlates better with human judgement than PSNR does, but it is still a hand-designed perceptual model, not a measurement of perception. Modern work uses LPIPS and no-reference metrics alongside it.",
        "**On IoU.** The brief lists PSNR, SSIM and IoU as example comparison metrics, because it is written generically across many topics. Intersection-over-Union measures region overlap and belongs to segmentation and detection. It is not defined for a dense-regression task with continuous-valued output. We report PSNR and SSIM, which are the standard for low-level vision, and say so rather than forcing a meaningless number. `[brief §3.6]`",
    ]},
    cite="Wang et al., IEEE TIP 2004 (standard SSIM) · brief §3.6 · Restormer22 Table 6",
    notes="The IoU paragraph is deliberate. Raising it before the TA does converts a potential 'you ignored a requirement' into a demonstration of judgement. Deliver it as one calm sentence."))

S.append(dict(t="table", era="meta", part="I", kicker="11 · The benchmarks",
    title="Nine datasets, and what each one is actually testing",
    lead="Benchmark choice is not neutral. Each dataset in this deck was chosen by its authors to expose a specific weakness, and the differences between them carry most of the argument in Part VII.",
    body={"cols": ["Dataset", "Content", "What it stresses", "Used by"],
          "align": "llll",
          "rows": [
            ["BSD68", "68 natural grayscale images, 481×321", "General-purpose average case. The standard denoising benchmark since 2007.", "DnCNN, TNRD, N2V, Restormer"],
            ["Set12", "12 classics — Cameraman, House, Barbara, Lena…", "Per-image behaviour. Barbara and House are dominated by repetitive texture.", "DnCNN Table III, Restormer Table 4"],
            ["Urban100", "100 urban photographs, high resolution", "**Long-range self-similarity.** Building façades repeat identically across hundreds of pixels.", "Restormer, MambaIR, SwinIR"],
            ["CBSD68 / Kodak24 / McMaster", "Colour natural images", "Cross-channel noise correlation and colour artefacts.", "Restormer Table 5, MambaIR Table 5"],
            ["SIDD", "Smartphone images, real sensor noise, 320 training scenes", "**The AWGN assumption itself.** Noise is signal-dependent and processed by an ISP.", "NAFNet, Restormer, MambaIR, P2N"],
            ["DND", "Real photographs, held-out benchmark server", "Generalisation — no training data is released, so you cannot overfit it.", "Restormer, MambaIR"],
            ["Set5 / Set14 / BSD100", "Super-resolution benchmarks", "Whether a denoiser generalises to other inverse problems.", "DnCNN-3, MambaIR"],
            ["Classic5 / LIVE1", "JPEG-compressed images", "Structured, non-Gaussian residual.", "DnCNN-3 Table V"],
          ]},
    foot="Urban100 and SIDD are the two datasets that carry the argument. Urban100 exposes bottleneck 3; SIDD exposes the AWGN assumption. Both appear again in Part VII with numbers.",
    cite="DnCNN17 §IV · Restormer22 §4.4 · MambaIR24 §4.1 · NAFNet22 §5",
    notes="If asked 'why does everyone use BSD68?' — because DnCNN used it, and comparability is worth more than perfection. That path-dependence is itself worth noting."))

S.append(dict(t="cards", era="meta", part="I", kicker="12 · Why it matters",
    title="Denoising is rarely the product — it is the substrate",
    lead="The strongest argument for studying denoising is not that grainy photos are annoying. It is that denoising is the canonical inverse problem, and a good denoiser turns out to be a reusable component in problems that are not denoising at all.",
    body={"cards": [
        {"tag": "Reason 1", "h": "It evaluates priors", "p": "SCUNet's opening argument: denoising *can help to evaluate the effectiveness of different image priors and optimization algorithms*. It is the cleanest possible test bed because the degradation is exactly known. `[SCUNet23 §1]`"},
        {"tag": "Reason 2", "h": "It plugs into other problems", "p": "A denoiser can be inserted into variable-splitting algorithms — half-quadratic splitting, ADMM — to solve deblurring and super-resolution. This is the *plug-and-play prior* result: solve denoising once, get a general-purpose regulariser. `[SCUNet23 §1]`"},
        {"tag": "Reason 3", "h": "It is the first step for vision", "p": "Denoising *could be the very first step for other vision tasks*. Detection, segmentation and classification all degrade on noisy input; the denoiser is the preprocessing that makes the downstream stack work at all. `[SCUNet23 §1]`"},
        {"tag": "Reason 4", "h": "One model, three tasks", "p": "DnCNN proved that super-resolution and JPEG deblocking are *special cases of a general image denoising problem* — redefine v and the same network and loss solve all three. Denoising is not one task; it is a template. `[DnCNN17 §III-D]`"},
    ]},
    cite="SCUNet23 §1 · DnCNN17 §III-D",
    notes="Lead the condensed presentation with reason 2 or 4. They are the ones that make a TA sit up — the claim that denoising is a *template* for inverse problems rather than a task."))
