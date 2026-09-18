# -*- coding: utf-8 -*-
S = []

S.append(dict(t="section", era="arch", part="V", kicker="Part V · 2021 – 2024 · branch two",
    title="The Architecture Branch",
    lead="The other half of the fork. Same supervision as DnCNN, same paired data, same loss family — and a complete replacement of the 3×3 convolution.",
    body={"items": ["Bottleneck 3, stated with evidence", "Attention, and why it does not fit",
                    "Restormer — attention across channels", "NAFNet — is any of this necessary?",
                    "SCUNet — fix the data, not the network", "MambaIR — linear-time global context",
                    "Three competing answers"]},
    cite="brief §4", notes="Name the branch difference immediately: Part IV changed what the network is shown. Part V changed what the network is."))

S.append(dict(t="two", era="arch", part="V", kicker="46 · Bottleneck 3",
    title="Convolution cannot see far enough — and here is the receipt",
    lead="The third bottleneck is the only one visible in DnCNN's own results table, three years before anyone could address it. Two independent pieces of evidence, taken from two papers five years apart, say the same thing.",
    body={"left": {"h": "Evidence 1 — Barbara, 2017", "bullets": [
        "DnCNN-S loses to BM3D by **0.71 dB** and to WNNM by **1.24 dB** on Barbara at σ = 25.",
        "The paper's own explanation: DnCNN fails *on exactly the two images dominated by repetitive structures*, because those images *meet well with the non-local similarity prior*.",
        "DnCNN's receptive field is 35×35. WNNM's effective patch size is **361×361** — ten times wider in each direction.",
        "The scarf's stripes have near-identical twins two hundred pixels away. DnCNN cannot see them. There is no amount of training that fixes a structural blindness.",
    ]},
     "right": {"h": "Evidence 2 — Urban100, 2022", "bullets": [
        "Urban100 is 100 photographs of buildings: windows, balconies and railings repeating identically across the whole frame. It is Barbara's scarf at dataset scale.",
        "Grayscale σ = 50: **DnCNN 26.35 → Restormer 28.33**. A gap of **1.98 dB**.",
        "On BSD68 — ordinary natural images, little repetition — the same two models are 26.23 and 26.62: a gap of **0.39 dB**.",
        "**The gap is five times larger on the dataset made of repetition.** That ratio is the cleanest single measurement of bottleneck 3 in the literature, and it is computed from one table.",
    ]},
    },
    foot="**Restate the bottleneck.** A 3×3 convolution aggregates a 3×3 neighbourhood. Stacking d of them without pooling reaches (2d+1)×(2d+1) — growth is *linear in depth* and therefore ruinously expensive. Reaching 361×361 the DnCNN way needs 180 layers. The architecture branch is the search for an operator whose reach is not bought by depth.",
    cite="DnCNN17 Table III, Table I, §IV-C · Restormer22 Table 4 — Urban100 and BSD68 columns",
    notes="Computing the 1.98-vs-0.39 comparison from Restormer's Table 4 is your own analysis of published numbers, not a claim from either paper. Say 'computed from Table 4' if asked."))

S.append(dict(t="math", era="arch", part="V", kicker="47 · Attention",
    title="Self-attention — the obvious fix, and why it does not fit",
    lead="Attention was invented for sequences and lets any element consult any other in a single operation. That is exactly the property bottleneck 3 needs. Its cost is exactly what makes it unusable on images.",
    body={"eqs": [
        {"tex": "Attention( Q, K, V )  =  softmax( Q Kᵀ / √d_k ) · V",
         "where": "Q, K, V — query, key and value projections of the input · the softmax produces one weight per pair of elements"},
        {"tex": "cost  =  O( W² H² )     for a W × H image",
         "where": "the key–query dot-product interaction grows **quadratically with the spatial resolution**"},
        ],
     "bullets": [
        "**The numbers make the problem concrete.** A 256×256 image has 65 536 spatial positions, so the attention matrix has ≈ 4.3 × 10⁹ entries. At 512×512 it is 6.9 × 10¹⁰. Restoration routinely runs at these resolutions and above; classification, where ViT works, runs at 224×224 on 16×16 patches — 196 tokens.",
        "**Restormer states the constraint directly:** *it is infeasible to apply SA on most image restoration tasks that often involve high-resolution images.*",
        "**Fix 1 — restrict the window.** SwinIR (2021) applies attention only inside fixed local windows, shifting them between layers so information leaks across boundaries. It works, and it is the first Transformer to reach the top of denoising tables. But Restormer's objection is structural: *restricting the spatial extent of SA is contradictory to the goal of capturing the true long-range pixel relationships*. You have bought back the very locality you were trying to escape.",
        "**Fix 2 — change the axis.** If attention over 65 536 spatial positions is unaffordable, attend over the *channels* instead. There are 48. This is Restormer's move, and it is the next slide.",
        "**Fix 3 — abandon attention.** NAFNet argues the gains never came from attention at all. MambaIR replaces it with a recurrence that is linear in sequence length. Both are later in this part.",
    ]},
    cite="Vaswani et al., NeurIPS 2017 (standard formulation) · Restormer22 §1, §3.1 · SCUNet23 §1 on SwinIR",
    notes="Have the token-count arithmetic ready. '65 536 tokens versus 196' explains in five seconds why vision Transformers and restoration Transformers are different problems."))

S.append(dict(t="math", era="arch", part="V", kicker="48 · Restormer, part 1 of 3",
    title="MDTA — self-attention across channels, not pixels",
    lead="Zamir, Arora, Khan, Hayat, Khan and Yang, CVPR 2022. The key design: apply self-attention across the feature dimension rather than the spatial dimension, so the attention map is C×C instead of HW×HW.",
    body={"eqs": [
        {"tex": "Q = W_d^Q W_p^Q Y ,    K = W_d^K W_p^K Y ,    V = W_d^V W_p^V Y",
         "where": "W_p — 1×1 point-wise convolution aggregating cross-channel context · W_d — 3×3 **depth-wise** convolution encoding channel-wise spatial context"},
        {"tex": "Attention( Q̂, K̂, V̂ )  =  V̂ · softmax( K̂ Q̂ᵀ / α )",
         "where": "Q̂, K̂, V̂ reshaped so the dot product yields a **C×C transposed-attention map** — cross-covariance across channels, not pairwise pixel interactions"},
        ],
     "bullets": [
        "**Linear complexity.** The attention matrix is C/k × C/k per head, independent of H and W. Cost grows linearly in the number of pixels rather than quadratically. In the reference configuration C is 48 at level 1, so the matrix is trivially small.",
        "**What the global context actually is.** Instead of explicitly modelling pairwise pixel interactions, MDTA computes *cross-covariance across feature channels* to obtain the attention map. Each channel is a global feature descriptor; weighting channels by their mutual covariance implicitly encodes global relationships.",
        "**The depth-wise convolutions are not decoration.** The paper calls local context mixing before covariance computation *an important feature* of the block, and the ablation proves it: removing depth-wise convolution from MDTA drops Urban100 σ=50 from 29.43 to 29.28.",
        "**Two advantages the authors claim.** It brings *the complimentary strength of convolution operation* into the pipeline, and it ensures contextualised global relationships between pixels are *implicitly modeled* while computing the attention maps.",
    ]},
    cite="Restormer22 §1, §3.1, Table 7",
    notes="The predictable challenge: 'is channel attention really global?' Honest answer — it is global in the sense that every channel is computed from every pixel, so channel statistics carry image-wide information. It is not pairwise pixel attention, and the paper never claims it is."))

S.append(dict(t="math", era="arch", part="V", kicker="49 · Restormer, part 2 of 3",
    title="GDFN and progressive learning",
    lead="The second half of the Transformer block, and a training strategy that is worth as much as an architectural change.",
    body={"eqs": [
        {"tex": "Gate( X )  =  φ( W_d¹ W_p¹ ( LN(X) ) )  ⊙  W_d² W_p² ( LN(X) )",
         "where": "the gated-Dconv feed-forward network: two parallel projections, one passed through GELU, multiplied element-wise · expansion factor γ = 2.66"},
        ],
     "bullets": [
        "**The role of the gate.** A standard feed-forward network is two linear layers with a nonlinearity between them. GDFN replaces the first with a *gating mechanism* — the element-wise product of two projections, one GELU-activated. The gate *controls which complementary features should flow forward*, allowing later layers to focus on more refined attributes.",
        "**Ablation value.** Gating alone gives +0.12 dB over conventional FN; adding depth-wise convolution to it gives **+0.26 dB** at σ = 50 on Urban100.",
        "**Progressive learning.** The network trains on *small patches and large batches in early epochs, and gradually large image patches and small batches in later epochs*. Concretely: begin at 128² with batch 64, then step through (160², 40), (192², 32), (256², 16), (320², 8), (384², 8) at iterations 92 K, 156 K, 204 K, 240 K, 276 K.",
        "**Why it helps.** It is curriculum learning — start with an easier task and move to a harder one where preserving fine structure and texture is required. Because a model trained on mixed-size patches sees more context distributions, it performs better *at test time on images of different resolutions*, which is the normal case in restoration. Batch size falls as patch size rises so the time per optimisation step stays roughly constant.",
        "**Full training recipe.** 4-level encoder–decoder; blocks [4, 6, 6, 8]; heads [1, 2, 4, 8]; channels [48, 96, 192, 384]; 4 refinement blocks; AdamW (β₁ 0.9, β₂ 0.999, weight decay 1e⁻⁴); **L1 loss**; 300 K iterations; LR 3e⁻⁴ → 1e⁻⁶ by cosine annealing; horizontal and vertical flips only.",
    ]},
    cite="Restormer22 §3.2, §3.3, §4 Implementation Details, Table 7, Table 9",
    notes="The progressive-learning schedule is a strong Stage-2-flavoured detail: it is a training-loop property invisible from the abstract, and it is in the YAML in the repository."))

S.append(dict(t="table", era="arch", part="V", kicker="50 · Restormer, part 3 of 3",
    title="The ablation that isolates every claim",
    lead="Colour denoising models trained on 128×128 patches for 100 K iterations, tested on Urban100. FLOPs and inference time at 256×256. This is the table to point at when asked whether the components actually do anything.",
    body={"cols": ["Network component", "FLOPs (B)", "Params (M)", "σ=15", "σ=25", "σ=50"],
          "align": "lrrrrr",
          "rows": [
            ["(a) Baseline — UNet with Resblocks", "83.4", "24.53", "34.42", "32.18", "29.11"],
            ["(b) MTA + FN", "83.7", "24.84", "34.66", "32.39", "29.28"],
            ["(c) MDTA + FN", "85.3", "25.02", "34.72", "32.48", "29.43"],
            ["(e) MTA + DFN", "85.8", "25.08", "34.68", "32.45", "29.42"],
            ["(f) MTA + GDFN", "86.2", "25.12", "34.77", "32.56", "29.54"],
            ["**(g) MDTA + GDFN**", "87.7", "25.31", "**34.82**", "**32.61**", "**29.62**"],
            ["+ Concat (no 1×1)", "110", "25.65", "—", "—", "29.66"],
            ["+ Refinement stage", "141", "26.12", "—", "—", "**29.71**"],
          ],
          "hl": [5]},
    foot="**Total contribution of the Transformer block: +0.51 dB over the baseline at σ = 50**, for a 5% increase in FLOPs. MDTA alone contributes +0.32 dB; GDFN alone contributes +0.26 dB over standard FN. Note also the deeper-versus-wider finding: at matched budget a **deep-narrow** model is more accurate, while a wide-shallow one runs faster through better parallelisation. Restormer ships deep-narrow.",
    cite="Restormer22 Table 7, Table 8, Table 10 — values as printed",
    notes="If a TA asks you to justify any single architectural choice in this deck, this is the table that does it. Every row is a controlled comparison."))

S.append(dict(t="table", era="arch", part="V", kicker="51 · Restormer results",
    title="Gaussian denoising — and the shape of the win",
    lead="Grayscale PSNR from Table 4. The top block is a *single model handling all noise levels*; the bottom block is a *separate model per noise level*. Restormer leads both.",
    body={"cols": ["Method", "Set12 σ=15", "σ=25", "σ=50", "BSD68 σ=15", "σ=25", "σ=50", "Urban100 σ=15", "σ=25", "σ=50"],
          "align": "lrrrrrrrrr",
          "rows": [
            ["DnCNN (2017)", "32.67", "30.35", "27.18", "31.62", "29.16", "26.23", "32.28", "29.80", "26.35"],
            ["FFDNet", "32.75", "30.43", "27.32", "31.63", "29.19", "26.29", "32.40", "29.90", "26.50"],
            ["IRCNN", "32.76", "30.37", "27.12", "31.63", "29.15", "26.19", "32.46", "29.80", "26.22"],
            ["DRUNet", "33.25", "30.94", "27.90", "31.91", "29.48", "26.59", "33.44", "31.11", "27.96"],
            ["**Restormer** (single)", "**33.35**", "**31.04**", "**28.01**", "**31.95**", "**29.51**", "**26.62**", "**33.67**", "**31.39**", "**28.33**"],
            ["NLRN", "33.16", "30.80", "27.64", "31.88", "29.41", "26.47", "33.45", "30.94", "27.49"],
            ["SwinIR", "33.36", "31.01", "27.91", "31.97", "29.50", "26.58", "33.70", "31.30", "27.98"],
            ["**Restormer** (per-σ)", "**33.42**", "**31.08**", "28.00", "31.96", "**29.52**", "**26.62**", "**33.79**", "**31.46**", "**28.29**"],
          ],
          "hl": [4, 7]},
    foot="**Read across the row, not down the column.** From DnCNN to Restormer, BSD68 σ=50 moves 26.23 → 26.62 (**+0.39 dB**) while Urban100 σ=50 moves 26.35 → 28.33 (**+1.98 dB**). The architecture branch did not make denoising uniformly better. It made denoising better *specifically where non-locality matters* — which is exactly what it set out to do. Efficiency note: Restormer has **3.14× fewer FLOPs and runs 13× faster** than SwinIR, and unlike DRUNet it requires no noise-level map as input.",
    cite="Restormer22 Table 4, §4.4 — values as printed",
    notes="The 0.39-versus-1.98 contrast is the single most defensible sentence in Part V. It shows you understand *why* the gain exists rather than just that it does."))

S.append(dict(t="math", era="arch", part="V", kicker="52 · NAFNet, part 1 of 2",
    title="NAFNet — the paper that asked whether any of this is necessary",
    lead="Chen, Chu, Zhang and Sun, ECCV 2022 (MEGVII). While everyone else added mechanisms, this paper removed them, and reached a higher number. Its two derivations are the most elegant reasoning in the modern half of this deck.",
    body={"eqs": [
        {"tex": "GLU( X, f, g, σ )  =  f(X) ⊙ σ( g(X) )                    GELU( x )  =  x · Φ(x)",
         "where": "the gated linear unit, and GELU — Φ is the standard normal CDF"},
        {"tex": "⟹   GELU is a special case of GLU   with f, g = identity and σ = Φ",
         "where": "which suggests GLU is a *generalisation of activation functions* — and that it might replace them"},
        {"tex": "SimpleGate( X, Y )  =  X ⊙ Y",
         "where": "split the feature map in half along the channel axis and multiply the halves. That is the entire activation function."},
        ],
     "bullets": [
        "**The key observation.** GLU *itself contains nonlinearity and does not depend on σ*: even with σ removed, f(X) ⊙ g(X) is nonlinear, because the product of two linear transformations is not linear. So the activation function can be deleted and the gate alone supplies the nonlinearity.",
        "**Compare the implementations.** GELU is approximated as 0.5x(1 + tanh[√(2/π)(x + 0.044715x³)]). SimpleGate is one element-wise multiplication. *That's all*, in the paper's words.",
        "**The same argument, applied again.** Channel attention is CA(X) = X * σ(W₂ max(0, W₁ pool(X))), which the paper rewrites as X * Ψ(X) — structurally identical to the GLU form. Retaining only its two essential roles, aggregating global information and channel interaction, gives **SCA(X) = X * W pool(X)**: one pooling, one 1×1 convolution, no Sigmoid, no ReLU.",
        "**The result.** No Sigmoid, no ReLU, no GELU, no Softmax anywhere in the network. The authors state it is *the first work demonstrating that the nonlinear activation functions may not be necessary for SOTA computer vision methods.*",
    ]},
    cite="NAFNet22 §4, Eq. (1)–(7)",
    notes="Deliver the GELU-as-GLU step slowly. It is a genuinely surprising piece of reasoning and it is the thing a TA is most likely to ask you to reproduce on a whiteboard."))

S.append(dict(t="table", era="arch", part="V", kicker="53 · NAFNet, part 2 of 2",
    title="The ablation ladder — every rung is a controlled experiment",
    lead="Starting from PlainNet — convolution, ReLU, shortcut, in a single-stage U-Net — each row changes exactly one thing. All at a ≈16 GMAC budget, 256×256 patches, batch 32, 200 K iterations, Adam, PSNR loss.",
    body={"cols": ["Step", "Change made", "SIDD (denoising)", "GoPro (deblurring)"],
          "align": "llrr",
          "rows": [
            ["0", "PlainNet — conv + ReLU + shortcut", "39.29", "28.51"],
            ["1", "+ LayerNorm (enables 10× learning rate)", "39.73  (+0.44)", "31.90  (+3.39)"],
            ["2", "ReLU → GELU", "39.71  (−0.02)", "32.11  (+0.21)"],
            ["3", "+ Channel Attention", "39.85  (+0.14)", "32.35  (+0.24)"],
            ["4", "GELU → **SimpleGate**", "39.93  (+0.08)", "32.76  (+0.41)"],
            ["5", "CA → **SCA**", "**39.96  (+0.03)**", "**32.85  (+0.09)**"],
            ["—", "**Final NAFNet at full capacity**", "**40.30**", "**33.69**"],
          ],
          "hl": [1, 5]},
    foot="**Three readings.** (a) The largest single gain is **LayerNorm**, worth +0.44 dB on denoising and +3.39 dB on deblurring — not because normalisation is magic but because it *stabilises training at a ten-times larger learning rate*. The architecture did not improve; the optimisation did. (b) Both simplifications **improved** results — SimpleGate beats GELU, SCA beats CA. (c) The headline: **40.30 dB on SIDD, exceeding the previous state of the art by 0.28 dB with less than half its computational cost**, and 33.69 dB on GoPro, exceeding the previous best by 0.38 dB with **8.4%** of its cost.",
    cite="NAFNet22 §3.3–3.6, §4, abstract — values as printed",
    notes="The LayerNorm row is the honest lesson of the whole architecture branch and worth saying out loud: a large share of reported architectural progress in restoration is optimisation progress wearing a costume."))

S.append(dict(t="two", era="arch", part="V", kicker="54 · SCUNet",
    title="SCUNet — fix the training data, not only the network",
    lead="Zhang, Li, Liang, Cao, Zhang, Tang, Fan, Timofte and Van Gool, *Machine Intelligence Research* 20(6), 2023 (ETH Zürich). Same first author as DnCNN, six years later, attacking the assumption DnCNN made rather than the architecture DnCNN built.",
    body={"left": {"h": "Half one — the swin-conv block", "bullets": [
        "The motivation is stated as complementarity: *different methods for image denoising have complementary image prior modeling ability and can be incorporated to boost the performance*, and DRUNet and SwinIR *exploit very different network architecture designs while achieving very promising denoising performance*.",
        "**The block.** A 1×1 convolution, then split the feature map evenly into two groups. One group goes to a **Swin Transformer block** (non-local modelling); the other to a **residual convolutional block** (local modelling). Concatenate, pass through a 1×1 convolution, add a residual connection.",
        "Plug that block into a standard image-to-image UNet backbone. Local and non-local priors run in parallel rather than one replacing the other.",
        "**9.663 M parameters** in the denoising configuration — a third of Restormer's, a twelfth of NAFNet's. `[measured]`",
    ]},
     "right": {"h": "Half two — the degradation model", "bullets": [
        "**The premise, stated bluntly:** a deep denoising model trained by AWGN *performs poorly for most of real images due to noise assumption mismatch*. Nevertheless AWGN removal *is fair to test the effectiveness of different network architecture designs*.",
        "**So synthesise realistic noise instead.** The training pipeline samples Gaussian (3-D generalised, with a 3×3 covariance matrix modelling R/G/B correlation, σ from {2/255 … 50/255}), **Poisson**, **speckle**, **JPEG compression**, and **processed camera sensor noise**.",
        "**Camera sensor noise is synthesised through a real ISP.** Invert a clean image to raw via a reverse ISP, add read and shot noise there, then run it forward through demosaicing, exposure compensation, white balance, colour-space conversion, tone mapping and gamma correction — with per-camera tone curves rather than one fixed curve.",
        "**Plus resizing** (bilinear and bicubic, scale factor uniform in [0.5, 2]) — because *upscaling would lead AWGN to be spatially correlated while downscaling would change processed camera sensor noise to be less signal-dependent*.",
        "**Plus a random shuffle strategy and a double degradation strategy**, because real images *might be resized or JPEG compressed several times*, in unknown order.",
    ]},
    },
    foot="**The lesson worth stating.** Every other paper in Part V competes on the architecture. SCUNet's four contributions include *a hand-designed noise synthesis model, which can be used to train a general-purpose blind image denoising model*. The distribution you train on is a design surface, and it is the one that most directly attacks the AWGN assumption named on slide 06.",
    cite="SCUNet23 abstract, §1, §3.1, §3.2, Fig. 1 · parameter count [measured], commit 52e440a",
    notes="SCUNet is the bridge between Part V and Part VII. It is the paper that says the benchmark itself is the problem, which is the argument slide 110 then proves with the SIDD numbers."))

S.append(dict(t="math", era="arch", part="V", kicker="55 · MambaIR, part 1 of 2",
    title="State-space models — a third answer to bottleneck 3",
    lead="Guo, Li, Dai, Ouyang, Ren and Xia, ECCV 2024 (Tsinghua Shenzhen / Shenzhen University / ByteDance). If attention is quadratic and windowed attention surrenders globality, borrow a mechanism from control theory that is global *and* linear.",
    body={"eqs": [
        {"tex": "h′(t)  =  A h(t)  +  B x(t) ,          y(t)  =  C h(t)  +  D x(t)",
         "where": "a continuous linear time-invariant system — the S4 formulation. N is the state size; A ∈ ℝ^{N×N}, B ∈ ℝ^{N×1}, C ∈ ℝ^{1×N}, D ∈ ℝ"},
        {"tex": "Ā = exp( ΔA ) ,      B̄ = (ΔA)⁻¹ ( exp(A) − I ) · ΔB          (zero-order hold discretisation)",
         "where": "Δ is the timescale parameter converting the continuous system to a discrete one"},
        {"tex": "h_k = Ā h_{k−1} + B̄ x_k ,   y_k = C h_k + D x_k        ⟺        K̄ = ( CB̄, CĀB̄, …, CĀ^{L−1}B̄ ) ,   y = x ⊛ K̄",
         "where": "the same model in **RNN form** (sequential, O(L) memory of the whole past) and in **CNN form** (a single long convolution, parallelisable)"},
        ],
     "bullets": [
        "**Why the dual form is the whole trick.** The recurrent form gives an unbounded receptive field — h_k depends on every previous input — while the convolutional form allows parallel training. Mamba keeps both: the recursive form *enables the model to memorize ultra-long sequences so that more pixels can be activated to aid restoration*, and the parallel scan algorithm *allows Mamba to enjoy the same advantages of parallel processing*.",
        "**What Mamba adds over S4.** B, C and Δ become **input-dependent**, allowing dynamic, content-adaptive feature representation rather than one fixed linear system. This is the *selective* in Selective Structured State Space Model.",
        "**Complexity.** Linear in sequence length, so linear in pixel count. The paper's own scaling experiment shows the full-attention baseline runs out of memory as input grows from 48×48 to 84×84, while MambaIR scales like windowed attention while retaining a global receptive field.",
    ]},
    cite="MambaIR24 §3.1, Eq. (1)–(4), §4.3, Fig. 5",
    notes="Nobody expects you to derive the ZOH discretisation. Do expect: 'why is an RNN suddenly fast again?' — because the CNN form makes training parallel, and the recurrence is only used at the level of the scan."))

S.append(dict(t="two", era="arch", part="V", kicker="56 · MambaIR, part 2 of 2",
    title="Adapting a sequence model to a 2-D image",
    lead="Mamba was built for text, which is a line. An image is a plane. The paper's contribution is the set of restoration-specific repairs needed to make the transfer work — and it names the two ways it fails without them.",
    body={"left": {"h": "The two failure modes", "bullets": [
        "**Local pixel forgetting.** To run the state-space equation, the feature map must be flattened into a sequence. Two pixels that are vertically adjacent may land hundreds of steps apart in that sequence, so the model forgets its own neighbourhood.",
        "**Channel redundancy.** The *excessive hidden state number* produces highly redundant channels, wasting capacity.",
        "**The fixes, inside the Residual State Space Block (RSSB):** a local convolution to restore neighbourhood awareness, and **channel attention** to suppress redundancy — plus a learnable factor controlling the skip connection.",
        "Ablation: removing the convolution costs Urban100 accuracy (34.15 → 34.04); removing convolution *and* channel attention gives 34.06; replacing the block with an MLP gives 34.22 against the 34.15 baseline configuration.",
    ]},
     "right": {"h": "Scanning, structure, and results", "bullets": [
        "**Four-directional scan.** The feature map is unfolded in four directions and the results summed, so no single raster order dominates. Ablation: one-direction 34.06, two-direction 33.96, four-direction (baseline) 34.15 on Urban100.",
        "**Three stages**, structurally identical to SwinIR: shallow feature extraction (one 3×3 convolution) → deep feature extraction (stacked RSSBs grouped into RSSGs) → high-quality reconstruction aggregating shallow and deep features.",
        "**Colour denoising, Urban100** (σ = 15/25/50): SwinIR 35.13 / 32.90 / 29.82 · Restormer 35.13 / 32.96 / 30.02 · **MambaIR 35.37 / 33.21 / 30.30**.",
        "**Real noise:** SIDD 39.89 dB, DND **40.04 dB** — the best DND figure in the table, 0.01 dB above Restormer.",
        "**Super-resolution**, where the receptive field matters most: MambaIR outperforms SwinIR by **0.41 dB on Manga109 at ×2**.",
    ]},
    },
    foot="**A Stage 2 finding worth knowing.** MambaIR's own repository changelog records that published complexity figures computed with `thop` were wrong and were later corrected. The model also cannot be imported at all without compiled CUDA extensions — `ModuleNotFoundError: mamba_ssm`. That is a deployment fact no paper reports, and it appears again on slide 103. `[measured]`",
    cite="MambaIR24 abstract, §3.2, §4.2, Tables 1, 2, 5, 6 · repository `csguoh/MambaIR`, commit 33d7b34 [measured]",
    notes="The import failure is a real Stage 2 result and a good one to volunteer. It shows you ran the code rather than reading about it."))

S.append(dict(t="cards", era="arch", part="V", kicker="57 · Where the branch stands",
    title="Three live answers, and no winner",
    lead="The honest ending to Part V, and the reason this narrative closes on an open question rather than a conclusion. Each of these is current, each is credible, and they disagree about what the operator should be.",
    body={"cards": [
        {"tag": "Transformer", "h": "Restormer — move the attention axis", "p": "Attend over channels, keep depth-wise convolution for locality. Linear in pixels. **26.1 M parameters.** Best-in-class on Gaussian grayscale, first method past 40 dB on both SIDD and DND. Slowest of the three on CPU by a wide margin. `[measured: 10.44 s at 256²]`"},
        {"tag": "Convolution", "h": "NAFNet — delete the mechanisms", "p": "No attention, no activation functions. Claims the gains were never attention's to begin with. **116.0 M parameters and still 5.5× faster than Restormer on CPU**, because 1×1 and depth-wise convolutions map onto optimised GEMM paths. 40.30 dB on SIDD. `[measured: 1.90 s at 256²]`"},
        {"tag": "State space", "h": "MambaIR — borrow from control theory", "p": "Global receptive field at linear cost via a selective SSM with four-directional scanning. Best DND result at 40.04 dB. Cannot run without compiled CUDA extensions, which is a genuine deployment constraint rather than a footnote. `[measured: import fails]`"},
        {"tag": "Data", "h": "SCUNet — change the training distribution", "p": "The orthogonal answer, and arguably the most practical. **9.7 M parameters**, smallest of the four, with a synthetic degradation pipeline built to survive real photographs rather than benchmarks. `[measured: 1.69 s at 256²]`"},
    ]},
    foot="**Say this in the defence.** A narrative that ends 'and then X won' would be false. The field currently holds three architectural answers and one data-side answer to the same bottleneck, published across three years, none of which has displaced the others. That is what an unresolved research question looks like from the inside.",
    cite="Restormer22 · NAFNet22 · MambaIR24 · SCUNet23 · parameter counts and CPU latencies [measured], see slide 102",
    notes="This is the intellectual high point of the deck. The willingness to end on an open question is what separates a literature review from a synthesis, and the brief grades synthesis."))
