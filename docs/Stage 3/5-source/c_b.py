# -*- coding: utf-8 -*-
S = []

S.append(dict(t="section", era="classical", part="II", kicker="Part II · 2005 – 2014",
    title="The Classical DIP Foundation",
    lead="Nine years in which the prior was a formula a human wrote down, and the answer to every image was recomputed from scratch.",
    body={"items": ["Spatial filters and the edge problem", "Transform-domain shrinkage", "Total variation",
                    "Non-local self-similarity", "BM3D, in full", "WNNM and the classical ceiling",
                    "Bottleneck 1"]},
    cite="brief §2", notes="Frame this part as the era whose *failure modes* define everything after it. Do not present it as history for its own sake."))

S.append(dict(t="math", era="classical", part="II", kicker="13 · The simplest idea",
    title="Averaging: why it works, and exactly how much",
    lead="The founding intuition of the entire field. If noise is zero-mean and independent, averaging n observations of the same quantity divides the noise standard deviation by √n. Every classical method is a different answer to the question: *which pixels count as observations of the same quantity?*",
    body={"eqs": [
        {"tex": "x̂(i,j)  =  (1/|W|) · Σ_{(p,q) ∈ W}  y(p,q)",
         "where": "the box / arithmetic mean filter over a neighbourhood W centred on (i,j)"},
        {"tex": "Var[ x̂ ]  =  σ² / |W|      ⟹      σ_out  =  σ / √|W|",
         "where": "a 3×3 window divides noise by 3; a 5×5 window divides it by 5"},
        ],
     "bullets": [
        "The derivation only holds if every pixel in W has the *same underlying clean value*. That assumption is true inside a flat region and catastrophically false across an edge.",
        "Across an edge, the mean of the window is not the value of the centre pixel, so the filter introduces a **bias** exactly proportional to the local contrast. You trade variance (noise) for bias (blur), pixel by pixel, and a box filter makes that trade blindly.",
        "This is the bias–variance trade-off in its purest visual form: the quantity you reduce is visible as grain, and the quantity you increase is visible as softness.",
        "**The entire classical era is a search for better definitions of W.** Gaussian weights it by distance. Bilateral weights it by distance *and* intensity. Non-local means abandons locality entirely and weights by patch similarity. BM3D stops weighting and starts *stacking*.",
    ]},
    cite="G&W, Image Restoration chapter · reading",
    notes="This slide earns its place because it makes the rest of Part II inevitable rather than arbitrary. Every subsequent classical method is visibly an answer to 'which pixels belong in W'."))

S.append(dict(t="two", era="classical", part="II", kicker="14 · Linear and order-statistic filters",
    title="Gaussian, median, and the first hard-coded threshold",
    lead="Two filters, two different failure modes, and the first appearance of the problem the brief names explicitly: reliance on hard-coded parameters.",
    body={"left": {"h": "Gaussian filter — linear, isotropic", "bullets": [
        "Weights w(p,q) ∝ exp( −[(p−i)² + (q−j)²] ⁄ 2σ_s² ). Nearer pixels count more.",
        "Separable: an N×N Gaussian is two 1×N passes, so cost is O(N) per pixel, not O(N²). This is why it was the default for decades.",
        "It is the Green's function of the heat equation — Gaussian smoothing *is* isotropic diffusion run for time t = σ_s²⁄2. That equivalence is what TNRD later generalises, in Part III.",
        "**Failure mode:** it diffuses across edges as happily as along them. Structure and noise are treated identically because the weights depend only on geometry.",
    ]},
     "right": {"h": "Median filter — nonlinear, order-statistic", "bullets": [
        "Replace the centre with the *median* of the window. Not a convolution — no kernel exists.",
        "Optimal for impulse (salt-and-pepper) noise, because an outlier cannot move a median the way it moves a mean. This is the same reason Noise2Noise's ℓ₁ loss recovers a median, in Part IV.",
        "Preserves step edges exactly: the median of a half-black, half-white window is black or white, never grey.",
        "**Failure mode:** destroys thin lines and corners, and is poorly matched to Gaussian noise, where the mean is the optimal estimator, not the median.",
    ]},
    },
    foot="Both filters require a window size chosen by a human, in advance, per image. The brief names this directly as a limitation of the classical era: *reliance on hard-coded thresholds*.",
    cite="G&W, Image Restoration chapter · brief §3.2",
    notes="The heat-equation remark is a good one to have loaded. It makes TNRD feel like a continuation rather than a swerve."))

S.append(dict(t="math", era="classical", part="II", kicker="15 · Transform-domain shrinkage",
    title="Sparsity: the idea that a clean image is compressible and noise is not",
    lead="The second great classical strategy. Move to a basis where the signal concentrates into a few large coefficients while the noise stays spread thinly across all of them — then discard the small ones.",
    body={"eqs": [
        {"tex": "hard:   T_h(c)  =  c · 1[ |c| > λ ]                    soft:   T_s(c)  =  sign(c) · max( |c| − λ , 0 )",
         "where": "c — a transform coefficient · λ — the shrinkage threshold, typically λ = σ√(2 log N)"},
        ],
     "bullets": [
        "**Why it works.** An orthonormal transform preserves the noise variance — white noise stays white, spread evenly over all coefficients at amplitude ≈ σ. A natural image, in a wavelet or DCT basis, concentrates its energy into few large coefficients. Thresholding therefore removes far more noise than signal.",
        "**Hard vs soft.** Hard thresholding is unbiased on surviving coefficients but discontinuous, producing ringing artefacts. Soft thresholding is continuous and produces smoother output but biases every surviving coefficient toward zero by λ. BM3D uses hard thresholding in step 1 and a Wiener filter in step 2 precisely to get the benefit of each. `[BM3D07 §III]`",
        "**Where it fails.** A single fixed basis — DCT, or one wavelet family — cannot be sparse for every image structure simultaneously. Edges at arbitrary orientations are notoriously non-sparse in separable wavelets, which is exactly where ringing appears.",
        "**The escape.** If a fixed basis is not sparse enough, learn one. That is K-SVD (Elad & Aharon, IEEE TIP 2006): learn an overcomplete dictionary D from the image's own patches and represent each patch as x ≈ Dα with ‖α‖₀ small. The prior is still hand-designed — sparsity — but the *basis* is now data-driven. This is the first crack in the classical wall.",
    ]},
    cite="BM3D07 §III · Elad & Aharon, IEEE TIP 2006 (cited in DnCNN17)",
    notes="K-SVD is the slide to point at when asked 'when did learning first appear?'. The answer is 2006, and it learned the dictionary, not the prior."))

S.append(dict(t="math", era="classical", part="II", kicker="16 · Total variation",
    title="ROF: the first prior that treats edges as information rather than error",
    lead="Rudin, Osher and Fatemi, 1992. Instead of penalising roughness with a squared gradient — which is quadratic and therefore hates edges — penalise the ℓ₁ norm of the gradient, which is cheap for a few large jumps and expensive for pervasive ripple.",
    body={"eqs": [
        {"tex": "x̂  =  arg min_x   ½‖y − x‖²₂   +   λ · ‖∇x‖₁ ,        ‖∇x‖₁ = Σ_{i,j} √( (∂_h x)²  +  (∂_v x)² )",
         "where": "the isotropic total-variation semi-norm — the ℓ₁ norm of the gradient magnitude field"},
        ],
     "bullets": [
        "**Why ℓ₁ and not ℓ₂.** A Tikhonov prior ‖∇x‖²₂ charges the *square* of a jump, so one edge of height 100 costs 10 000 while a hundred ripples of height 1 cost only 100 — the optimiser removes the edge. TV charges the jump itself, so an edge of height 100 costs 100 and a hundred ripples also cost 100. Edges become affordable.",
        "**Consequence — and the classic artefact.** TV's minimiser is piecewise constant. It preserves edges beautifully and turns smooth gradients into visible flat plateaus. This is *staircasing*, and it is the reason TV is not a general-purpose denoiser.",
        "**Non-differentiability.** ‖·‖₁ has no gradient at zero, so the objective cannot be minimised by plain gradient descent. Chambolle's 2004 dual projection algorithm solves it by iterating on the dual variable to a fixed tolerance.",
        "**The engineering consequence, which matters in Part VI.** The algorithm is a `while` loop with a tolerance and a maximum iteration count, run *per image*. The prior is one line of arithmetic you can read; the price is that nothing is ever reused.",
    ]},
    cite="Rudin, Osher & Fatemi 1992 · Chambolle 2004 · implementation inspected: scikit-image 0.26.0 `denoise_tv_chambolle` [measured]",
    notes="This is the classical method we actually opened the source code of in Stage 2. Have the while-loop screenshot ready — it appears on slide 90."))

S.append(dict(t="two", era="classical", part="II", kicker="17 · The conceptual leap",
    title="Non-local self-similarity — stop looking nearby",
    lead="Buades, Coll and Morel, CVPR 2005. Every method so far assumed the pixels that inform a pixel are the pixels *near* it. Natural images violate that assumption constantly: a brick resembles the other bricks, a stripe resembles the other stripes, and those twins may be two hundred pixels away.",
    body={"left": {"h": "Non-local means", "bullets": [
        "x̂(i) = Σ_j w(i,j) · y(j), summed over the whole image, with w(i,j) ∝ exp( −‖P_i − P_j‖²_a ⁄ h² ).",
        "The weight compares *patches* P centred on i and j, not single pixels. Two pixels are similar if their neighbourhoods are similar.",
        "Averaging many independent observations of the same structure cancels the noise while the shared signal survives — the √n argument from slide 13, now applied to patches rather than a square window.",
        "Cost is quadratic in the number of pixels unless the search is restricted to a window, which every practical implementation does.",
    ]},
     "right": {"h": "Why this matters for the whole deck", "bullets": [
        "NSS is the strongest hand-designed prior ever found for natural images. It powers BM3D and WNNM, and it is the *specific* prior DnCNN lacks.",
        "WNNM's own framing: NSS refers to the fact that there are many repeated local patterns across a natural image, and those non-local similar patches to a given patch can help much the reconstruction of it. `[WNNM14 §3]`",
        "This single idea explains the two most quoted results in this deck — DnCNN's loss on Barbara (Part III) and Restormer's enormous gain on Urban100 (Part VII).",
        "It is also the reason the third bottleneck exists. Convolution is local by construction; recovering non-locality inside a neural network took from 2017 to 2022.",
    ]},
    },
    cite="Buades et al., CVPR 2005 (cited in DnCNN17) · WNNM14 §3",
    notes="If you have time for only one classical concept in the condensed presentation, make it this one — it is load-bearing three more times later in the deck."))

S.append(dict(t="flow", era="classical", part="II", kicker="18 · BM3D, part 1 of 4",
    title="The algorithm that defined the benchmark for a decade",
    lead="Dabov, Foi, Katkovnik and Egiazarian, IEEE TIP 2007. BM3D combines non-local grouping with transform-domain shrinkage, and runs the combination twice. Its two-step structure is stated verbatim in the paper.",
    body={"steps": [
        {"h": "Step 1a-i · Grouping", "p": "For each reference block in the noisy image, find blocks similar to it by block-matching and stack them together in a 3-D array — a *group*."},
        {"h": "Step 1a-ii · Collaborative hard-thresholding", "p": "Apply a 3-D transform to the group, attenuate the noise by hard-thresholding the coefficients, invert the transform, and return the estimates to their original positions."},
        {"h": "Step 1b · Aggregation", "p": "Compute the basic estimate by weighted averaging of all overlapping block-wise estimates."},
        {"h": "Step 2a-i · Re-grouping", "p": "Use block-matching *within the basic estimate* — cleaner, so matching is more accurate. Form two groups: one from the noisy image, one from the basic estimate."},
        {"h": "Step 2a-ii · Collaborative Wiener filtering", "p": "Wiener-filter the noisy group using the energy spectrum of the basic estimate as the pilot spectrum."},
        {"h": "Step 2b · Aggregation", "p": "Aggregate the local estimates by weighted average into the final estimate."},
    ],
     "bullets": [
        "The paper gives two motivations for the second step explicitly: using the basic estimate rather than the noisy image **improves the grouping**, and using it as the Wiener pilot signal is **much more effective and accurate than simple hard-thresholding** of the noisy spectrum. `[BM3D07 §II-C]`",
    ]},
    cite="BM3D07 §II-C, algorithm stated verbatim",
    notes="Do not paraphrase this loosely in the defence — the two-step, two-estimate structure is the single most-asked BM3D question and the paper's own wording is precise."))

S.append(dict(t="math", era="classical", part="II", kicker="19 · BM3D, part 2 of 4",
    title="Why *collaborative* filtering beats filtering each patch alone",
    lead="The word 'collaborative' is doing real work. Stacking similar patches into a 3-D array creates sparsity along a third axis that does not exist in any single patch — and that third axis is where nearly all the denoising happens.",
    body={"eqs": [
        {"tex": "Ŷ_S  =  T₃D⁻¹ (  γ ( T₃D ( Y_S ) )  ) ,        γ(c) = c · 1[ |c| > λ_3D · σ ]",
         "where": "Y_S — the 3-D group of matched blocks · T₃D — a separable 3-D transform · γ — hard thresholding"},
        {"tex": "T₃D  =  T_2D  ⊗  T_1D",
         "where": "a 2-D transform within each block (intra-fragment), composed with a 1-D transform across the stack (inter-fragment)"},
        ],
     "bullets": [
        "**The paper's own ablation is the best evidence.** Varying T_2D and T_1D changes PSNR only modestly — even a transform whose basis elements are *random apart from the DC* loses only 0.1–0.4 dB. The authors conclude that collaborative filtering depends mainly on the third-dimension transform, and that **inter-fragment correlation appears as a much more important feature than intra-fragment correlation**. `[BM3D07 §V]`",
        "**Which is why the DC element matters.** The DST performs measurably worse than every other tested transform, and the paper attributes this to the DST's *lack of a DC basis element* — the DC along the third axis is what captures similarity between stacked blocks. Averaging is recovered as a special case.",
        "**Complexity.** Time complexity is linear in image size, since all parameters are fixed. Cost per pixel is dominated by the exhaustive-search block matching in a local neighbourhood plus the separable transforms. The published profiles are Normal and Fast; the Fast profile uses predictive-search block matching instead of exhaustive search. `[BM3D07 §VI-A, §VI-B]`",
        "**Parameter count.** Block size, search window, matching threshold, λ_3D, the two transforms, and aggregation weights — all set by the authors, with different values above and below σ = 40. This is the 'several manually chosen parameters' that DnCNN names as a drawback of the entire era.",
    ]},
    cite="BM3D07 §V, §VI-A, §VI-B",
    notes="The random-transform ablation is a genuinely surprising result and makes an excellent answer to 'why is BM3D so good?'. It is not the transform — it is the grouping."))

S.append(dict(t="stats", era="classical", part="II", kicker="20 · BM3D, part 3 of 4",
    title="Why BM3D was the benchmark, not merely a benchmark",
    lead="For roughly a decade every denoising paper had to beat BM3D, and almost none did by a meaningful margin. Three numbers explain why that stalemate lasted.",
    body={"stats": [
        {"n": "0.3 dB", "l": "the practical ceiling", "s": "Prior work found that *few methods can outperform BM3D by more than 0.3 dB on average*, a figure DnCNN quotes when calibrating its own result. `[DnCNN17 §IV-B]`"},
        {"n": "0.7 dB", "l": "the estimated theoretical bound", "s": "The estimated PSNR bound over BM3D reported in the literature — Levin & Nadler's work on the inherent limits of natural-image denoising. `[DnCNN17 §IV-B]`"},
        {"n": "2.85 s", "l": "512×512, CPU, σ = 25", "s": "Fast enough to be usable, unlike WNNM's 773 s. BM3D occupied the only viable point on the quality-vs-time curve. `[DnCNN17 Table IV]`"},
    ],
     "bullets": [
        "BM3D's scores on BSD68 — 31.07 / 28.57 / 25.62 dB at σ = 15 / 25 / 50 — are the reference line for every table in Part VII. `[DnCNN17 Table II]`",
        "**And it is still in use.** BM3D appears as a live baseline in Noise2Noise (2018), Noise2Void (2019), ZS-N2N (2023) and Restormer (2022). A seventeen-year-old algorithm is still the thing new zero-shot methods must beat, because it requires no training data at all.",
        "**The honest framing for the defence:** BM3D was not superseded because it was bad. It was superseded because it was *the best a human could do by hand*, and the next gain had to come from somewhere other than a human.",
    ]},
    cite="DnCNN17 §IV-B, Table II, Table IV · baselines in N2N18, N2V19, ZS-N2N23, Restormer22",
    notes="The 'still in use' point is the one that impresses. It reframes BM3D from historical curiosity to live competitor in the zero-shot setting."))

S.append(dict(t="math", era="classical", part="II", kicker="21 · WNNM, part 1 of 2",
    title="The classical peak: low-rank recovery on stacks of similar patches",
    lead="Gu, Zhang, Zuo and Feng, CVPR 2014. WNNM takes the same non-local grouping as BM3D but replaces transform shrinkage with low-rank matrix approximation — and then fixes the standard low-rank estimator so it respects the physics of denoising.",
    body={"eqs": [
        {"tex": "Y_j  =  X_j  +  N_j ,           X_j  low rank",
         "where": "Y_j — a matrix whose columns are the nonlocal similar patches to patch j · X_j — their clean counterpart"},
        {"tex": "X̂_j  =  arg min_{X_j}  (1/σ²_n) ‖Y_j − X_j‖²_F  +  ‖X_j‖_{w,*} ,      ‖X‖_{w,*} = Σ_i w_i σ_i(X)",
         "where": "the weighted nuclear norm — a *differently weighted* sum of singular values, not an equally weighted one"},
        ],
     "bullets": [
        "**The setup.** Stacking similar patches into a matrix makes that matrix low rank, because the columns are near-copies of one another. Recovering a low-rank matrix from a noisy one is a well-studied convex problem.",
        "**The defect WNNM fixes.** Standard nuclear-norm minimisation has a closed form — soft-threshold every singular value by the same λ. But the paper argues this *treats each singular value equally*, ignoring that in denoising the singular values have clear physical meaning: **the larger ones carry the major image components and should be shrunk less**.",
        "**The weighting rule**, stated in the paper: w_i = c·√n ⁄ (σ_i(X_j) + ε), with c a constant, n the number of similar patches, and ε = 10⁻¹⁶ guarding the division. The weight is *inversely proportional* to the singular value, so large components are barely touched and small ones are crushed.",
        "**The circularity, and its resolution.** The weights depend on σ_i(X_j), the singular values of the unknown clean matrix. WNNM estimates them by assuming the noise energy is evenly distributed across subspaces: σ̂_i(X_j) = √( max( σ_i²(Y_j) − n σ_n², 0 ) ).",
    ]},
    cite="WNNM14 §1, §3, Eq. 9–11",
    notes="Expect: 'what is the difference between NNM and WNNM in one sentence?' — NNM soft-thresholds all singular values by the same amount; WNNM thresholds each by an amount inversely proportional to its own size."))

S.append(dict(t="content", era="classical", part="II", kicker="22 · WNNM, part 2 of 2",
    title="The theorem that makes it tractable, and the price it charges",
    lead="Weighting the nuclear norm destroys convexity in general. WNNM's contribution is a theorem identifying exactly when a closed-form solution survives, plus an iterative algorithm for when it does not.",
    body={"bullets": [
        "**Theorem 2 (WNNM).** If the weights satisfy w₁ ≥ w₂ ≥ … ≥ w_n ≥ 0 — that is, *non-ascending* order — the problem has a globally optimal solution obtained by generalised soft-thresholding of the singular values of Y with the weight vector w: X̂ = U S_w(Σ) Vᵀ. The classical singular value thresholding result of Cai et al. is recovered as the special case w₁ = … = w_n = λ.",
        "**The catch for denoising.** The denoising weights are *non-descending* (small singular values get large weights), which is the opposite ordering. The paper therefore proves a separate result: when weights are in non-descending order, an iterative algorithm reaches an analytical **fixed point** in one step, because soft-thresholding preserves the non-ascending order of the singular values, so the auxiliary permutation matrices stay at identity.",
        "**Result.** WNNM leads to *visible PSNR improvements over state-of-the-art methods such as BM3D*, and preserves local structure with fewer visual artefacts. On BSD68 it scores 31.37 / 28.83 / 25.87 dB at σ = 15 / 25 / 50, beating BM3D at every level. `[WNNM14 abstract; DnCNN17 Table II]`",
        "**The price, and it is enormous.** WNNM requires an SVD of every patch group, iterated, per image. Measured in the DnCNN paper's own comparison: **773.2 seconds for a single 512×512 image**, and 2 536 seconds at 1024×1024 — against BM3D's 2.85 s and 11.89 s. `[DnCNN17 Table IV]`",
        "**Effective patch size 361 × 361.** WNNM consults a region more than ten times wider than DnCNN's 35×35 receptive field. Hold on to that number — it reappears on slide 50 and it is the reason WNNM still wins on Barbara.",
    ]},
    cite="WNNM14 Theorem 2, §2.3, abstract · DnCNN17 Table I, Table II, Table IV",
    notes="The 773 seconds is the single most useful classical number you have. It is the entire commercial argument for the deep era, and it comes from the DnCNN paper's own table rather than from us."))

S.append(dict(t="table", era="classical", part="II", kicker="23 · The classical scoreboard",
    title="Where nine years of hand-designed priors finished",
    lead="All figures below are reproduced from Table II and Table IV of the DnCNN paper, which benchmarked every classical competitor under one protocol on one dataset. Reading them across a single row is the fairest available comparison of the era.",
    body={"cols": ["Method", "Year", "Prior Φ", "BSD68 σ=15", "σ=25", "σ=50", "512² runtime"],
          "align": "llllrrr",
          "rows": [
            ["BM3D", "2007", "NSS + 3-D transform sparsity", "31.07", "28.57", "25.62", "2.85 s CPU"],
            ["EPLL", "2011", "Gaussian mixture patch prior", "31.21", "28.68", "25.67", "45.5 s CPU"],
            ["CSF", "2014", "Unrolled field of experts", "31.24", "28.74", "—", "5.67 s / 0.92 s GPU"],
            ["WNNM", "2014", "NSS + weighted low rank", "31.37", "28.83", "25.87", "773.2 s CPU"],
            ["MLP", "2012", "learned (plain network)", "—", "28.96", "26.03", "5.51 s CPU"],
            ["TNRD", "2016", "Unrolled reaction–diffusion", "31.42", "28.92", "25.97", "1.33 s / 0.032 s GPU"],
          ],
          "hl": [3]},
    foot="Two readings. (a) Nine years of work moved BSD68 σ=25 from 28.57 to 28.83 — **0.26 dB**. (b) The best classical method is 271× slower than the second best. The era had hit a wall in both quality and cost simultaneously.",
    cite="DnCNN17 Table II and Table IV — all values as printed",
    notes="Do not add DnCNN to this table. It belongs on slide 53, after the mechanism has been explained. Showing the answer before the argument wastes the reveal."))

S.append(dict(t="cards", era="classical", part="II", kicker="24 · Bottleneck 1",
    title="Why the field had to leave — in the words of the paper that left",
    lead="DnCNN's introduction names the classical era's drawbacks precisely. Quoting the paper that broke a bottleneck, rather than asserting the bottleneck ourselves, is what makes this timeline evidenced rather than imposed.",
    body={"cards": [
        {"tag": "Drawback 1", "h": "Test-time optimisation", "p": "Prior-based methods *involve a complex optimization problem in the testing stage*, making the denoising process time-consuming. Every image restarts from nothing; nothing learned on image 1 helps image 2. `[DnCNN17 §I]`"},
        {"tag": "Drawback 2", "h": "Non-convex, hand-tuned", "p": "The models are *generally non-convex and involve several manually chosen parameters*. Reproducibility and deployment both suffer: the quality you get depends on constants a human picked. `[DnCNN17 §I]`"},
        {"tag": "Drawback 3", "h": "The prior's form limits the result", "p": "Even for the discriminative bridge methods, performance is *inherently restricted to the specified forms of prior*; analysis-model priors are *limited in capturing the full characteristics of image structures*. `[DnCNN17 §I]`"},
        {"tag": "Drawback 4", "h": "One model per noise level", "p": "Bridge methods *train a specific model for a certain noise level* and are *limited in blind image denoising*. In a phone camera, σ is never known. `[DnCNN17 §I]`"},
    ]},
    foot="**Bottleneck 1, stated once:** the prior is written by hand, and paid for once per image. The next era removes both halves of that sentence.",
    cite="DnCNN17 §I — all four drawbacks quoted from the paper's introduction",
    notes="This is a transition slide. Deliver it fast and move. Its function is to make Part III feel forced rather than chosen."))
