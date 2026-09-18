# -*- coding: utf-8 -*-
S = []

S.append(dict(t="section", era="data", part="IV", kicker="Part IV · 2018 – 2025 · branch one",
    title="The Data Branch",
    lead="Seven years spent removing the clean image from the training signal, one requirement at a time — while the network stayed almost exactly where DnCNN left it.",
    body={"items": ["Noise2Noise — clean targets are unnecessary", "Noise2Void — a second noisy copy is unnecessary",
                    "ZS-N2N — a training set is unnecessary", "P2N — discarding information is unnecessary",
                    "The through-line: the network never moved, the target did"]},
    cite="brief §4 (training paradigms)", notes="Open by naming the branch: this is the half of the modern field that answers bottleneck 2. The architecture half is Part V. They are independent."))

S.append(dict(t="math", era="data", part="IV", kicker="39 · Noise2Noise",
    title="The statistical argument that removed the clean image",
    lead="Lehtinen, Munkberg, Hasselgren, Laine, Karras, Aittala and Aila, ICML 2018 (NVIDIA). The paper applies *basic statistical reasoning* and reaches a conclusion that sounds impossible: you can learn to restore images by looking only at corrupted examples.",
    body={"eqs": [
        {"tex": "arg min_z  E_y { L(z, y) }        with  L(z,y) = (z − y)²   ⟹   z = E_y{ y }",
         "where": "the L2 minimiser of a set of observations is their arithmetic mean. The L1 minimiser is the median."},
        {"tex": "arg min_θ  Σ_i  L( f_θ( ŷ_i ) , ŷ_i )        with        E{ ŷ_i | x̂_i } = y_i",
         "where": "Equation (6) — both inputs and targets are drawn from a corrupted distribution, conditioned on the unobserved clean target"},
        ],
     "bullets": [
        "**The argument, in one sentence.** A trivial property of L2 minimisation is that *on expectation, the estimate remains unchanged if we replace the targets with random numbers whose expectations match the targets.* The optimal network parameters are unchanged if the target distribution is swapped for any distribution with the same conditional expectation. Therefore you may corrupt the training targets with zero-mean noise **without changing what the network learns**.",
        "**Given infinite data the solution is identical to clean-target training.** For finite data, the variance is the average variance of the corruptions in the targets divided by the number of training samples — so the penalty shrinks with dataset size rather than persisting.",
        "**What is *not* required.** The paper is emphatic: none of this relies on a likelihood model of the corruption, nor a density model for the clean image manifold. No explicit p(noisy|clean), no p(clean).",
        "**Why this is physically natural.** In many restoration tasks the expectation of the corrupted data *is* the clean target. A long, noise-free exposure is the average of short, independent, noisy exposures — so two short exposures of the same scene are exactly the training pair the theorem asks for.",
        "**The loss chooses the estimator.** L2 recovers the mean. L1 recovers the median, letting networks repair images with up to 50% outlier content. This is the classical mean-versus-median trade-off from slide 14, now operating at the level of the training objective.",
    ]},
    cite="N2N18 §2, Eq. (2)–(6)",
    notes="Guaranteed question: 'how can training on noisy targets possibly work?' Answer with the mean property in one line — L2 regression learns the conditional mean, and the conditional mean of a zero-mean corrupted target is the clean target. Do not start with the network."))

S.append(dict(t="table", era="data", part="IV", kicker="40 · Noise2Noise results",
    title="Noisy targets cost essentially nothing",
    lead="PSNR on three test sets for three noise types, from Table 1. In each pair, *clean* is conventional supervised training and *noisy* is the same network trained on corrupted targets only.",
    body={"cols": ["Test set", "Gaussian σ=25 clean", "noisy", "BM3D", "Poisson λ=30 clean", "noisy", "Bernoulli p=0.5 clean", "noisy"],
          "align": "lrrrrrrr",
          "rows": [
            ["Kodak", "32.50", "32.48", "31.82", "31.52", "31.50", "33.01", "33.17"],
            ["BSD300", "31.07", "31.06", "30.34", "30.18", "30.16", "31.04", "31.16"],
            ["Set14", "31.31", "31.28", "30.50", "30.07", "30.06", "31.51", "31.72"],
            ["**Average**", "**31.63**", "**31.61**", "30.89", "**30.59**", "**30.57**", "**31.85**", "**32.02**"],
          ],
          "hl": [3]},
    foot="**The gap between clean-target and noisy-target training is 0.02 dB on Gaussian noise and 0.02 dB on Poisson.** For Bernoulli noise the noisy-target model is *better*. Setting the deep-learning requirement for clean data aside costs about one fiftieth of the margin DnCNN gained over BM3D. Training used 256×256 crops from the 50 000 ImageNet validation images with σ randomised per example in [0, 50] — i.e. blind denoising.",
    cite="N2N18 Table 1, §3.1 — values as printed",
    notes="The 0.02 dB figure is the number to quote. It converts an abstract theorem into an engineering fact: paired clean data was never actually necessary."))

S.append(dict(t="math", era="data", part="IV", kicker="41 · Noise2Void",
    title="Blind-spot networks — removing the second noisy copy",
    lead="Krull, Buchholz and Jug, CVPR 2019 (MPI-CBG Dresden). Noise2Noise still needs *two independent noisy observations of the same scene*. For a fixed specimen under a microscope that is often two acquisitions; for a moving world, or a single archival image, it is nothing. N2V removes it.",
    body={"eqs": [
        {"tex": "p(s, n)  =  p(s) · p(n | s) ,      p(n | s) = Π_i p(n_i | s_i) ,      E[n_i] = 0   ⟹   E[x_i] = s_i",
         "where": "the two assumptions: (i) the signal is **not** pixel-wise independent, p(s_i|s_j) ≠ p(s_i); (ii) the noise **is** conditionally pixel-wise independent given the signal, and zero-mean"},
        ],
     "bullets": [
        "**The problem to solve.** Train a network with the same noisy image as input *and* target and it degenerates — it learns the identity, which has zero loss and does nothing.",
        "**The fix.** Build a network whose receptive field has a **blind spot** at its centre: the prediction for pixel i is affected by all pixels in a square neighbourhood *except pixel i itself*.",
        "**Why the blind spot cannot learn the identity.** Because the noise is pixel-wise independent given the signal, the neighbouring pixels *carry no information about the value of n_i*. It is impossible for the network to beat its a priori expected value on the noise. The signal, by contrast, is assumed to contain statistical dependencies — so the network can still estimate s_i from the surroundings. It can learn the signal and cannot learn the noise.",
        "**The implementation, which is a trick rather than an architecture.** Implementing a true blind-spot receptive field efficiently is not trivial, so N2V instead *replaces the value in the centre of each input patch with a randomly selected value from the surrounding area*. Any standard CNN then acquires the property. The loss is computed **only** at the masked pixels.",
        "**Efficiency approximation.** Computing gradients for one output pixel per patch is wasteful, so N2V draws 64×64 patches and manipulates **N = 64 pixels per patch simultaneously** — 1.6% of the patch — recovering most of the gradient signal per forward pass.",
    ]},
    cite="N2V19 §3.1, §3.4, §3.5, Fig. 2, Fig. 3",
    notes="Emphasise the two assumptions. They are the entire method, and they are also exactly what breaks when noise is spatially correlated — which is the case for every JPEG, every demosaiced photograph, and anything that has been resized."))

S.append(dict(t="stats", era="data", part="IV", kicker="42 · The price of the blind spot",
    title="What self-supervision costs, measured",
    lead="Four training regimes, one network family, one dataset: BSD68 with σ = 25 Gaussian noise, trained on 400 grayscale images at 180×180 — deliberately the same protocol DnCNN used. The ladder shows exactly what each removed requirement costs.",
    body={"stats": [
        {"n": "29.06", "l": "Traditional · clean targets", "s": "Supervised U-Net, depth 2, 96 initial feature maps. The ceiling."},
        {"n": "28.86", "l": "Noise2Noise · noisy pairs", "s": "−0.20 dB for giving up the clean image."},
        {"n": "28.59", "l": "BM3D · no training at all", "s": "The classical zero-shot baseline, seventeen years old."},
        {"n": "27.71", "l": "Noise2Void · single noisy images", "s": "−1.35 dB from supervised, and 0.88 dB **below** BM3D."},
    ],
     "bullets": [
        "**Read the ladder honestly, and say it before you are asked.** On natural images with plentiful clean data, N2V is *worse than a 2007 algorithm*. The paper does not hide this — it states that its performance *only drops moderately* and notes it still outperforms BM3D on its other benchmarks.",
        "**So why does N2V matter?** Because the comparison above is the one case where the alternatives exist. The paper's real argument is the three biomedical datasets where they do not: cryo-TEM, and two Cell Tracking Challenge sets. For CTC-MSC and CTC-N2DH *only single noisy images exist*, so neither traditional nor N2N training is applicable — and the ground-truth column in the paper's figure is literally captioned *does not exist*.",
        "**The correct framing for the defence.** Self-supervision is not a quality technique. It is an *availability* technique. It trades PSNR for applicability, and in the domains it targets, the alternative is not a lower score — it is no denoiser at all.",
    ]},
    cite="N2V19 §4.1, Fig. 4 — PSNR values as printed",
    notes="Volunteering the 'worse than BM3D' number is a rigour move. It also pre-empts the obvious attack and lets you land the availability argument on your own terms."))

S.append(dict(t="math", era="data", part="IV", kicker="43 · ZS-N2N",
    title="Zero-shot — removing the training set entirely",
    lead="Mansour and Heckel, CVPR 2023 (TU Munich / Rice). N2V still needs a *body of noisy data to train on*. ZS-N2N needs one image: the one you want to denoise. It has no training set, no pretraining, and about 20 000 parameters.",
    body={"eqs": [
        {"tex": "D₁ = y ⊛ k₁ ,   k₁ = [[0, ½],[½, 0]] ;        D₂ = y ⊛ k₂ ,   k₂ = [[½, 0],[0, ½]]        (stride 2)",
         "where": "the **pair downsampler**: split each 2×2 block into its diagonal average and its anti-diagonal average, giving two half-resolution images with similar signal and independent noise"},
        {"tex": "L_res  =  ½ ( ‖ D₁ − f_θ(D₁) − D₂ ‖²  +  ‖ D₂ − f_θ(D₂) − D₁ ‖² )",
         "where": "symmetric **residual** loss — note f_θ predicts the noise, exactly as DnCNN does, six years later"},
        {"tex": "L_cons  =  ½ ( ‖ D₁ − f_θ(D₁) − D₁( y − f_θ(y) ) ‖²  +  ‖ D₂ − f_θ(D₂) − D₂( y − f_θ(y) ) ‖² )",
         "where": "**consistency** — denoise-then-downsample must agree with downsample-then-denoise"},
        ],
     "bullets": [
        "**Minimise L = L_res + L_cons by gradient descent on that one image**, then estimate x̂ = y − f_θ̂(y). Only θ is optimised; D₁ and D₂ are fixed convolutions.",
        "**Why the pair is a valid N2N pair.** Nearby pixels of a clean image are highly correlated and often have similar values, while noise pixels are unstructured and independent — so the downsampled pair has *similar signal but independent noise*, approximating two noisy observations of one scene.",
        "**Why consistency matters.** In the residual loss the network only ever sees half-resolution input. Only the consistency term shows it the image at full spatial resolution, and the paper describes it as a regularising term that *enables better denoising performance and helps to avoid overfitting* — removing the need for the early stopping that Noise2Fast and DIP require.",
        "**The network.** Two 3×3 convolutional operators followed by one 1×1 operator. **≈ 20 K parameters.** No normalisation, no pooling. Convergence needs 1–2 K iterations: *less than half a minute on a GPU and around one minute on a CPU*. The ablation shows that substituting a U-Net causes overfitting and *much worse* performance — the tiny network is load-bearing, not a compromise.",
        "**The comparison that lands.** Self2Self, the strongest zero-shot competitor, takes *1.2 hours to denoise one 256×256 image on a GPU*. ZS-N2N needs 1/200 of the time and 2% of the memory.",
    ]},
    cite="ZS-N2N23 §3, Eq. (2)–(6), §4",
    notes="The reappearance of residual learning here is worth pointing out aloud: DnCNN's 2017 design choice is still the default in a 2023 zero-shot paper with a 20K-parameter network."))

S.append(dict(t="two", era="data", part="IV", kicker="44 · P2N",
    title="Positive2Negative — removing the information loss",
    lead="Li, Wang, Xu, Zhu, Lu and Huang, CVPR 2025. Every self-supervised method so far pays for its training signal by *throwing information away*: N2V blinds a pixel, ZS-N2N halves the resolution. P2N's claim is that neither sacrifice is necessary.",
    body={"left": {"h": "The two mechanisms", "bullets": [
        "**RDC — Renoised Data Construction.** Denoise the image once, estimate the noise, then *add that estimated noise back* with a plus and with a minus, producing y⁺ and y⁻. Both retain the full resolution and every pixel of the original.",
        "**DCS — Denoised Consistency Supervision.** Denoise y⁺ and y⁻ and train the two results to agree. The supervision signal is the disagreement between two renoised views of the same image.",
        "Nothing is masked. Nothing is downsampled. The barrier the title names — *the information-lossy barrier in self-supervised single image denoising* — is the masking-and-downsampling tax that N2V and ZS-N2N both pay.",
    ]},
     "right": {"h": "Why this is a *supervision* change, not a loss change", "bullets": [
        "This distinction matters and it is easy to get wrong. P2N does not merely swap one loss function for another.",
        "**It changes what goes into the network.** The inputs y⁺ and y⁻ are constructed from the model's own output — they do not exist until the model has run once.",
        "**It changes how many forward passes there are.** Three, not one: denoise y, then denoise y⁺, then denoise y⁻.",
        "**It changes which pair is scored.** The comparison is output-against-output, not output-against-target.",
        "A loss function scores a fixed prediction against a fixed target. P2N rewrites the whole training signal — what is shown, how many times, and what is compared.",
    ]},
    },
    foot="**And the architecture?** Unchanged. The network class in the official repository is literally named `UNet_n2n_un` and matches the 2018 Noise2Noise channel widths exactly. P2N+ adds one optional module, Symmetric Prior Injection. Seven years of progress on this branch, and the network is the same one. `[measured — P2N-plus, commit 8a117db]`",
    cite="P2N25 (CVPR 2025, pp. 17924–17934; arXiv:2412.16460) · repository `github.com/Li-Tong-621/P2N-plus` [measured]",
    notes="The supervision-versus-loss distinction was an error we corrected during Stage 2 and it is exactly the kind of precision a TA probes. Be able to state the three differences — inputs, pass count, compared pair — without reading them."))

S.append(dict(t="cards", era="data", part="IV", kicker="45 · The through-line",
    title="The network never moved. The target did.",
    lead="Four papers, seven years, one branch. Read them as a single sequence and each one removes exactly one requirement its predecessor could not drop — while the backbone stays a U-Net of roughly the 2018 shape throughout.",
    body={"cards": [
        {"tag": "2018", "h": "Noise2Noise", "p": "**Target:** a second noisy photograph of the same scene. **Requirement removed:** the clean image. **Cost:** you must capture the scene twice, which rules out anything that moves and every archival image."},
        {"tag": "2019", "h": "Noise2Void", "p": "**Target:** the masked pixel's own original value. **Requirement removed:** the second copy. **Cost:** 1.6% of pixels are blinded per patch, and the noise must be spatially independent — which excludes correlated real noise."},
        {"tag": "2023", "h": "ZS-N2N", "p": "**Target:** the other diagonal of the same 2×2 block. **Requirement removed:** the training set. **Cost:** half the spatial resolution during training, plus a per-image optimisation of 1–2 K steps."},
        {"tag": "2025", "h": "P2N", "p": "**Target:** the model's own output on a renoised copy. **Requirement removed:** the information loss itself. **Cost:** three forward passes per step, and per-image test-time optimisation."},
    ]},
    foot="**The arc in one sentence:** the prior moved out of the algorithm and into the weights in 2017 — and then, on this branch, partly back *out* of the weights and into a per-image optimisation that needs no clean data at all. The classical era's test-time optimisation has returned, but the thing being optimised is now a network, not a pixel grid.",
    cite="N2N18 · N2V19 · ZS-N2N23 · P2N25 — each paper's own stated requirement",
    notes="This is the closing slide of Part IV and the one to deliver from memory. If time is short in the 30-minute version, this single slide can stand in for the entire branch."))
