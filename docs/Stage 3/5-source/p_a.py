# -*- coding: utf-8 -*-
"""Presentation deck content, part A — Presenter 1."""
S = []

S.append(dict(t="title", era="meta", part="", kicker="Digital Image Processing · Final Project · Stage 3",
    title="Image Denoising:\nHow the Field Actually Evolved",
    lead="Not ten papers in order. One technical story: what each method could not do, what the next one changed, and which line of code changed to do it.",
    body={"meta": [
        ("The question", "Why did each innovation\nhave to be invented?"),
        ("Anchor paper", "DnCNN — Zhang et al.\nIEEE TIP 26(7), 2017"),
        ("Presenters", "Navid Zare · Ali Ahmadi\nKomeil Khodayar"),
        ("Reference", "100-slide master deck\nsubmitted separately"),
    ]},
    cite="brief §3 · full evidence in the master deck",
    notes="30s. Say the framing sentence and move. Do not read the meta cards — they answer questions before they are asked."))

S.append(dict(t="cards", era="meta", part="", kicker="The shape of this talk",
    title="Four questions we will answer about every method",
    lead="Each algorithm gets the same four-part treatment, so the comparison between them is structural rather than anecdotal. The methods that were state of the art get a fifth question.",
    body={"cards": [
        {"tag": "1", "h": "What could the previous method not do?",
         "p": "Every innovation in this field was a response to a *named, measured* failure — usually named by the paper that fixed it, which is what makes this timeline evidenced rather than imposed."},
        {"tag": "2", "h": "What changed technically?",
         "p": "The algorithmic change: a different prior, a different training target, a different operator. Stated precisely enough that you could implement it."},
        {"tag": "3", "h": "Which line of code changed?",
         "p": "A Before → After from the reference implementations. Contribution → algorithmic change → **implementation change** → measured improvement, as one chain."},
        {"tag": "4", "h": "What did it buy, and what did it cost?",
         "p": "The measured improvement, the applications it opened, and the new limitation it created — because every step in this story created the next problem."},
    ]},
    foot="**And for the SOTA methods, a fifth:** what made it state of the art, *on which benchmark and in which years*, and why it did not make the others obsolete.",
    cite="reading — the structure of this presentation",
    notes="40s. This slide is a contract with the audience. It also tells the TA exactly what to listen for, which is worth the time."))

S.append(dict(t="math", era="meta", part="", kicker="The problem",
    title="One equation, three unknowns, eighteen years",
    lead="Given only y, infinitely many splits into x + v are arithmetically valid. Every method in this talk supplies the missing information in a different way — that supplied information is called the prior, and the whole story is about where it lives.",
    body={"eqs": [{"tex": "y = x + v", "where": "y — what the sensor produced · x — the clean image we want · v — the noise"}],
     "bullets": [
        "**The classical answer** writes the prior down as a formula: minimise ½‖y − x‖² + λ·Φ(x). You can read Φ, differentiate it, and argue about it.",
        "**The deep answer** replaces Φ with a tensor of learned weights. You cannot read it, but you can download it and it runs in 60 ms.",
        "**The self-supervised answer** takes the prior partly from the test image itself, so no clean data is needed at all.",
        "**Where the prior lives, and who writes it, is the single axis this whole talk runs along.**",
    ]},
    cite="DnCNN17 §I · standard MAP formulation",
    notes="60s. This is the only theory slide. Everything else is evolution. Do not derive MAP here — the master deck has it and the audience does not need it to follow the story."))

S.append(dict(t="two", era="meta", part="", kicker="Ground rules",
    title="What 'state of the art' means in this talk",
    lead="The phrase is used loosely in most presentations. We use it with three qualifiers attached, because that is what makes the SOTA comparison later in the talk meaningful rather than rhetorical.",
    body={"left": {"h": "A SOTA claim needs three things", "bullets": [
        "**A benchmark and a metric.** 'Best denoiser' is meaningless. 'Highest PSNR on BSD68 at σ=25' is a claim you can check.",
        "**A time window.** Every method here was SOTA for a bounded period on a bounded benchmark, then was overtaken — usually on that benchmark only.",
        "**A comparison protocol.** Two papers reporting on the same dataset can still disagree; we take both numbers from one table wherever possible.",
    ]},
     "right": {"h": "Which is why there is no single winner", "bullets": [
        "Different benchmarks measure different capabilities: BSD68 measures average-case Gaussian removal, Urban100 measures **long-range self-similarity**, SIDD measures **real sensor noise**.",
        "A method can lead one and trail another. Restormer, NAFNet and MambaIR each lead a different table *today*.",
        "**We return to this on slide 36** with the numbers, because 'why are there several SOTAs' is the question this talk is built to answer.",
    ]},
    },
    cite="reading, grounded in the benchmark definitions used by DnCNN17, Restormer22, NAFNet22",
    notes="50s. Setting this up now means the SOTA comparison later lands as a payoff rather than a hedge."))

# ─────────────── ERA 1: CLASSICAL ───────────────
S.append(dict(t="section", era="classical", part="1", kicker="Baseline · 2007 – 2014",
    title="The Hand-Written Prior",
    lead="Where the field started: a formula a human wrote, re-solved from scratch for every image.",
    body={"items": ["BM3D — the baseline everything is measured against",
                    "WNNM — the classical ceiling",
                    "Bottleneck 1 — why the era ended"]},
    cite="brief §2", notes="10s. Just say 'Era one' and move."))

S.append(dict(t="flow", era="classical", part="1", kicker="BM3D · 2007 · the baseline",
    title="The innovation: filter patches together, not alone",
    lead="Dabov et al., IEEE TIP 2007. Previous transform-domain methods shrank each patch independently. BM3D's innovation is to *group* similar patches first, creating a third axis along which the signal is nearly constant and the noise is not.",
    body={"steps": [
        {"h": "What changed", "p": "Block-match similar patches into a 3-D stack, transform the **stack**, hard-threshold, invert, aggregate — then repeat using the cleaner estimate as a Wiener pilot."},
        {"h": "Why it works", "p": "The paper's own ablation: even a transform that is *random apart from the DC* loses only 0.1–0.4 dB. **The grouping does the work, not the transform.** `[BM3D07 §V]`"},
        {"h": "Impact", "p": "BSD68 σ=25: **28.57 dB** at 2.85 s per 512×512. Became the reference line every paper for a decade had to beat."},
        {"h": "SOTA window", "p": "Roughly **2007 → 2014**, on BSD68/Set12 Gaussian denoising. Still a live baseline in papers from 2023, because it needs no training data."},
        {"h": "Applications", "p": "Still deployed where no training data exists or no GPU is available; used as the zero-shot comparison in Noise2Noise, Noise2Void and ZS-N2N."},
    ]},
    cite="BM3D07 §II-C, §V · DnCNN17 Table II, Table IV · baselines in N2N18, N2V19, ZS-N2N23",
    notes="90s. The random-transform ablation is the memorable fact — lead with it if pressed for time."))

S.append(dict(t="table", era="classical", part="1", kicker="WNNM · 2014 · before → after",
    title="WNNM vs BM3D — the same grouping, a better estimator",
    lead="Gu et al., CVPR 2014. WNNM keeps BM3D's non-local grouping and replaces what happens to the group. This is the first clean Before → After in the story, and it is entirely inside one step.",
    body={"cols": ["Aspect", "BM3D (2007)", "WNNM (2014)", "Why it matters"],
          "align": "llll",
          "rows": [
            ["Core algorithm", "Group patches, shrink in a 3-D transform", "Group patches, recover a **low-rank matrix**", "Stacked near-copies are low rank by construction — a stronger structural assumption"],
            ["Key innovation", "Collaborative hard-thresholding", "**Weighted** nuclear norm: wᵢ ∝ 1⁄σᵢ", "Large singular values carry the image and are shrunk *less*; standard NNM shrinks all equally"],
            ["Implementation change", "3-D DCT + threshold", "SVD per patch group + per-value shrinkage, iterated", "One transform call becomes an iterated SVD — the entire cost difference"],
            ["Performance", "28.57 dB · 2.85 s", "**28.83 dB** · **773.2 s**", "+0.26 dB for a **271× slowdown**"],
            ["Limitation", "Fixed hand-set parameters", "Non-convex; still per-image optimisation", "Neither can reuse anything learned from one image on the next"],
            ["Applications", "General-purpose, real-time-ish", "Offline / quality-critical restoration", "The cost makes WNNM impractical for interactive or batch use"],
          ],
          "hl": [3]},
    foot="**This row is the whole argument for what comes next.** Seven years of hand-designed priors bought 0.26 dB on BSD68 at σ=25, and the best method became 271× slower than the second best. The era had hit a wall in quality *and* cost simultaneously.",
    cite="DnCNN17 Table II, Table IV · WNNM14 §3, Theorem 2",
    notes="90s. Point at the highlighted row and say the sentence in the footnote. This is the slide that motivates the entire deep era."))

S.append(dict(t="cards", era="classical", part="1", kicker="Bottleneck 1",
    title="Why the era ended — stated by the paper that ended it",
    lead="DnCNN's introduction names the classical era's drawbacks in its own words. Quoting the paper that broke the bottleneck, rather than asserting it ourselves, is what makes this an evidenced timeline.",
    body={"cards": [
        {"tag": "Drawback 1", "h": "The prior is paid for once per image",
         "p": "Prior-based methods *involve a complex optimization problem in the testing stage*. Nothing learned on image 1 helps image 2. WNNM: 773 s, every time. `[DnCNN17 §I]`"},
        {"tag": "Drawback 2", "h": "The prior is written by hand",
         "p": "The models are *generally non-convex and involve several manually chosen parameters* — block size, thresholds, λ, different values above and below σ=40. `[DnCNN17 §I]`"},
        {"tag": "Drawback 3", "h": "Its form limits the ceiling",
         "p": "Performance is *inherently restricted to the specified forms of prior*. You cannot exceed what your formula can express, however well you tune it. `[DnCNN17 §I]`"},
        {"tag": "Drawback 4", "h": "One model per noise level",
         "p": "Bridge methods *train a specific model for a certain noise level* and are *limited in blind image denoising*. In a real camera, σ is never known. `[DnCNN17 §I]`"},
    ]},
    cite="DnCNN17 §I — all four quoted from the paper's introduction",
    notes="45s. Fast. These four cards are the setup for DnCNN answering all four at once."))

# ─────────────── ERA 2: DnCNN ───────────────
S.append(dict(t="section", era="deepcnn", part="2", kicker="The break · 2016 – 2017",
    title="The Prior Becomes a File",
    lead="One architecture answers all four drawbacks at once — and creates the two problems the rest of the talk is about.",
    body={"items": ["TNRD — the bridge nobody skips",
                    "DnCNN — innovation, implementation, impact",
                    "Bottlenecks 2 and 3"]},
    cite="brief §3", notes="10s."))

S.append(dict(t="table", era="bridge", part="2", kicker="TNRD · 2016 · before → after",
    title="Unrolling — the step that made the transition continuous",
    lead="Chen & Pock, TPAMI. Worth ninety seconds because it is the conceptual bridge: it shows that a classical optimiser and a neural network are the same object viewed differently, which is why the move to deep learning was not a rupture.",
    body={"cols": ["Aspect", "Classical optimiser", "TNRD (unrolled)", "Why it matters"],
          "align": "llll",
          "rows": [
            ["Iteration count", "Run to convergence, unbounded", "**Truncated to a fixed K** (usually < 10)", "Runtime becomes a constant — the first half of bottleneck 1 is gone"],
            ["Parameters", "Same hand-set rule every iteration", "**Every stage has its own learned filters and nonlinearities**", "The prior is no longer one formula; it is K different learned ones"],
            ["What is learned", "Nothing", "Filters *and* influence functions, jointly, from data", "Earlier diffusion models fixed the filters and chose the diffusivity"],
            ["Implementation", "`while` loop to a tolerance", "A fixed stack trained by back-propagation", "Structurally a CNN — and *well-suited for parallel computation on GPUs*"],
            ["Performance", "WNNM 28.83 dB · 773 s", "**28.92 dB · 0.032 s** (GPU)", "Best quality-per-second of the era"],
            ["Limitation", "—", "Still one model per noise level", "Blind denoising remains unsolved"],
          ]},
    foot="**Keep this in mind for the next slide.** DnCNN derives part of its own justification from a one-stage TNRD — the two are directly connected, not merely adjacent in time.",
    cite="TNRD16 §1.2, §2, §3 · DnCNN17 Tables II, IV",
    notes="75s. If you are running late, this is the first slide to compress — but do not cut it entirely, the TA may ask how the transition happened."))

S.append(dict(t="table", era="deepcnn", part="2", kicker="DnCNN · 2017 · before → after",
    title="DnCNN vs TNRD — remove the optimiser entirely",
    lead="Zhang et al., IEEE TIP. TNRD unrolled the optimiser; DnCNN throws away the optimisation heritage and keeps only the network. The technical change is small, the consequence is the largest single step in this story.",
    body={"cols": ["Aspect", "TNRD (2016)", "DnCNN (2017)", "Why it matters"],
          "align": "llll",
          "rows": [
            ["Core algorithm", "K diffusion stages, PDE-derived", "**Plain deep CNN**: Conv-BN-ReLU ×17, no pooling", "The architecture no longer has to resemble an optimiser at all"],
            ["What the net outputs", "The restored image", "**The noise** — x = y − R(y)", "Residual learning: the 'do nothing' solution moves to zero, which is trivially reachable"],
            ["Key enabler", "Learned influence functions", "**Residual learning + batch normalisation, together**", "Neither works nearly as well alone — the paper's most-cited empirical finding"],
            ["Noise levels", "One model per σ", "**DnCNN-B: one blind model, σ ∈ [0, 55]**", "Drawback 4 solved; no noise estimate needed at test time"],
            ["Performance", "28.92 dB · 0.032 s", "**29.23 dB · 0.060 s** (blind: 29.16)", "+0.6 dB over BM3D at *all three* noise levels"],
            ["Applications", "Gaussian denoising", "**One model for denoising + super-resolution + JPEG deblocking**", "Redefine v and the same network solves three tasks"],
          ],
          "hl": [1, 4]},
    cite="DnCNN17 §II-A, §III-A, §III-C, §III-D, Table II, Table IV · TNRD16",
    notes="90s. The two highlighted rows are the innovation and the payoff. Say both out loud."))

S.append(dict(t="code", era="deepcnn", part="2", kicker="DnCNN · the implementation change",
    title="The innovation is eight characters",
    lead="`cszn/KAIR`, `models/network_dncnn.py`, by DnCNN's own first author. The architecture is a list comprehension; the contribution is the return statement.",
    body={"lang": "python", "file": "KAIR/models/network_dncnn.py — the whole network",
     "lines": [
        "m_head = B.conv(in_nc, nc, mode='C'+act_mode[-1])",
        "m_body = [B.conv(nc, nc, mode='C'+act_mode)",
        "          for _ in range(nb-2)]          # ← the entire network",
        "m_tail = B.conv(nc, out_nc, mode='C')",
        "",
        "def forward(self, x):",
        "    n = self.model(x)",
        "    return x-n                           # ← the contribution",
        "",
        "# BEFORE (discriminative CNNs, ~2012-2016):",
        "#     return self.model(x)      -> learn F(y) = x",
        "# AFTER (DnCNN, 2017):",
        "#     return x - self.model(x)  -> learn R(y) = v",
     ],
     "bullets": [
        "**Why that one change matters.** From ResNet: a mapping close to the identity is hard to optimise. And y is much more like x than it is like v — so learning the *image* forces the network toward an identity transform, which seventeen ReLU layers have no natural way to express.",
        "**Learning the noise moves the trivial solution to zero**, reachable by driving weights toward zero. Same function class, far easier optimisation landscape.",
        "**The synergy, in one sentence.** Residual learning strips the image out of the hidden layers, making activations Gaussian-like and content-independent — which is exactly the regime batch-norm's batch statistics assume. *Without* residual learning, BN *has a certain adverse effect on convergence*.",
        "**Where the prior went.** Nowhere in this file. It is in the `.pth` checkpoint this class will load. That is the moment the prior stopped being readable — and started being downloadable.",
     ]},
    cite="measured — cszn/KAIR, verbatim · DnCNN17 §II-A, §III-C",
    notes="100s. The most important implementation slide in the talk. Point at `return x-n`, then at the BEFORE/AFTER comment block."))

S.append(dict(t="stats", era="deepcnn", part="2", kicker="DnCNN · why it was SOTA",
    title="What made it state of the art, and for how long",
    lead="A SOTA claim with all three qualifiers attached: the benchmark, the margin against the known ceiling, and the window before it was overtaken.",
    body={"stats": [
        {"n": "+0.6 dB", "l": "over BM3D, all three σ", "s": "On BSD68. Prior work put the practical ceiling over BM3D at **0.3 dB** and the estimated theoretical bound at **0.7 dB** — so DnCNN took about **85% of the available headroom**. `[DnCNN17 §IV-B]`"},
        {"n": "12 900×", "l": "faster than WNNM at 512²", "s": "773.2 s CPU → 0.060 s GPU. The device differs and the paper says so; the order of magnitude is the point. `[DnCNN17 Table IV]`"},
        {"n": "2017–2021", "l": "its SOTA window", "s": "Held the Gaussian-denoising reference position until DRUNet and SwinIR in 2021. On *real* noise it was never SOTA at all — slide 34."},
    ],
     "bullets": [
        "**And it did it blind.** DnCNN-B reaches 29.16 dB without being told σ, beating every noise-level-specific competitor in the table. That is drawback 4 closed.",
        "**Applications it opened:** real-time denoising in imaging pipelines; the `.pth` checkpoint as a shippable artefact; and denoising as a *reusable component* — a trained denoiser can be dropped into variable-splitting solvers as a general-purpose prior. `[SCUNet23 §1]`",
    ]},
    cite="DnCNN17 §IV-B, Table II, Table IV · SCUNet23 §1",
    notes="70s. '85% of the available headroom' is the phrase that makes 0.6 dB sound like what it is."))

S.append(dict(t="two", era="deepcnn", part="2", kicker="Bottlenecks 2 and 3",
    title="What DnCNN broke, and the two bills it left",
    lead="This slide is the hinge of the whole talk. Everything after it is the field paying off these two debts — and they were paid off by two different communities, independently, and never merged.",
    body={"left": {"h": "Bottleneck 2 — it needs clean data", "bullets": [
        "The loss is ‖R(y) − (y − x)‖². **It requires x.**",
        "For fluorescence microscopy, cryo-EM, MRI and astronomy a clean ground truth **does not exist and cannot be acquired** — you cannot photograph the same cell noiselessly.",
        "So the most valuable applications of denoising were the ones DnCNN could not serve.",
        "**→ Answered by the data branch. Presenter 2, slide 19.**",
    ]},
     "right": {"h": "Bottleneck 3 — it cannot see far enough", "bullets": [
        "Receptive field is **35×35 pixels**, chosen deliberately to match EPLL, the *smallest* effective patch size in the field. WNNM's is 361×361.",
        "Visible in DnCNN's own Table III: on **Barbara** it *loses* to BM3D by **0.71 dB** — the one Set12 image dominated by repetitive texture.",
        "The paper explains it: repetitive images *meet well with the non-local similarity prior* that a 35×35 convolution stack cannot reach.",
        "**→ Answered by the architecture branch. Presenter 2, slide 24.**",
    ]},
    },
    foot="**A limitation visible in 2017, in the winning paper's own results table, that took until 2022 to fix.** That is what an honest evolution story looks like.",
    cite="DnCNN17 §III-A Eq. (1), Table I, Table III · N2V19 §1",
    notes="80s. Slow down. Then hand over. Rehearse the handover sentence so it is not awkward."))
