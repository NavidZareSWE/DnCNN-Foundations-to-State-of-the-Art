# -*- coding: utf-8 -*-
S = []

S.append(dict(t="section", era="bridge", part="III", kicker="Part III · 2012 – 2017",
    title="The Deep Learning Transition",
    lead="Five years in which the optimisation loop was unrolled into a fixed architecture, and then abandoned entirely.",
    body={"items": ["MLP — the first plain network to matter", "Unrolling as the conceptual bridge",
                    "CSF and TNRD", "DnCNN: architecture, residual learning, BN synergy",
                    "Depth, receptive field, data, results", "One model, three tasks", "Bottleneck 2"]},
    cite="brief §3", notes="This is the centre of the deck and the part you are anchored on. Budget the most rehearsal time here."))

S.append(dict(t="content", era="bridge", part="III", kicker="25 · The first crack",
    title="MLP, 2012 — a plain neural network reaches BM3D",
    lead="Burger, Schuler and Harmeling, CVPR 2012. Before any architectural insight, before residual learning, before batch normalisation: a multi-layer perceptron trained on enough patches matched the best hand-designed algorithm in the field.",
    body={"bullets": [
        "**The method is deliberately unsophisticated.** Take a noisy patch, flatten it to a vector, push it through several fully connected layers, and read a clean patch out. No convolution, no weight sharing, no prior of any kind written down.",
        "**The result.** On BSD68 at σ = 25 it scores **28.96 dB**, ahead of BM3D's 28.57 and ahead of WNNM's 28.83 — the strongest result in the whole classical table at that noise level. At σ = 50 it scores 26.03, again the best pre-DnCNN figure. `[DnCNN17 Table II]`",
        "**Effective patch size 47 × 47**, arising from a 39×39 input patch followed by a 9×9 averaging filter. Comparable to BM3D's 49×49 — the network was not seeing more than its competitors. `[DnCNN17 Table I]`",
        "**What it proved, and what it did not.** It proved that a learned mapping could match a decade of hand-designed mathematics. It did not explain *why*, did not generalise across noise levels — a separate model per σ — and its fully connected structure scaled badly with patch size.",
        "**The reading.** MLP is the existence proof, not the solution. It told the field that the answer was learning, and left the question of *what to learn and how* wide open for the next five years.",
    ]},
    cite="Burger et al., CVPR 2012 (cited in DnCNN17) · DnCNN17 Table I, Table II",
    notes="Useful framing: MLP is the moment the field learned the destination without learning the route. Everything from 2012 to 2017 is route-finding."))

S.append(dict(t="two", era="bridge", part="III", kicker="26 · The bridge concept",
    title="Unrolling — turn the iterations into layers",
    lead="The elegant idea that connects the two eras. A classical denoiser is an iterative optimiser: repeat some update rule K times. Unrolling fixes K, gives every iteration its own parameters, and trains the whole stack end-to-end by back-propagation.",
    body={"left": {"h": "Before — an optimiser", "bullets": [
        "Run until convergence, or until a tolerance is met. K is unbounded and data-dependent.",
        "Every stage applies the *same* hand-written rule with the *same* hand-tuned constants.",
        "Quality is whatever the fixed objective's minimiser happens to be. You cannot ask for better without redesigning Φ.",
        "Cost is unpredictable: a hard image takes longer than an easy one.",
    ]},
     "right": {"h": "After — an architecture", "bullets": [
        "Truncate to a fixed K — TNRD uses *usually less than 10* stages. Now the runtime is a constant.",
        "Give each stage its *own* filters and nonlinearities, and let them differ across stages.",
        "Train all of them against a loss measured on the final output. The objective being minimised is no longer the objective being optimised at test time — it is the training loss.",
        "The result is, structurally, a neural network — but one whose layers are inherited from a PDE rather than invented.",
    ]},
    },
    foot="**Why this matters for the narrative.** Unrolling is the bridge that makes the classical→deep transition continuous rather than a rupture. TNRD is a diffusion equation and a CNN simultaneously, which is exactly why DnCNN can later derive itself from a one-stage TNRD.",
    cite="TNRD16 §1.2, §2 · reading",
    notes="If the TA asks 'was the move to deep learning a clean break?' — no, and this slide is the evidence. CSF and TNRD are both."))

S.append(dict(t="math", era="bridge", part="III", kicker="27 · TNRD",
    title="Trainable Nonlinear Reaction Diffusion — a PDE with learned parameters",
    lead="Chen and Pock, IEEE TPAMI 2016/2017. DnCNN's direct theoretical ancestor. The model is a classical nonlinear diffusion process in which every component — the filters *and* the influence functions — is learned from data rather than chosen.",
    body={"eqs": [
        {"tex": "( u_t − u_{t−1} ) / Δt   =   − Σ_{i=1}^{N_k} (K_i^t)ᵀ · φ_i^t ( K_i^t u_{t−1} )   −   ψ^t ( u_{t−1}, f )",
         "where": "left group = diffusion term  ·  right group = reaction term  ·  K_i — sparse matrices implementing 2-D convolution with kernel k_i  ·  φ_i — influence functions  ·  f — the degraded input"},
        {"tex": "ψ^t(u)  =  ∇_u D_t(u, f)  =  λ^t Aᵀ ( A u − f ) ,        A = I  for denoising",
         "where": "the reaction term is the gradient of a data-fidelity term — which is what makes one framework serve denoising, super-resolution and JPEG deblocking"},
        ],
     "bullets": [
        "**Δt = 1 in practice**, because φ and ψ can be freely rescaled. The paper states this directly.",
        "**What is learned:** in previous nonlinear diffusion models the filters were fixed (derivative operators) and the diffusivity was a chosen function. TNRD learns both *simultaneously* through a loss-based approach, and lets them **vary across stages**.",
        "**Configurations reported:** 24 filters of 5×5, 48 filters of 7×7, 80 filters of 9×9 — the filter count is m²−1 for an m×m kernel. Influence functions are parameterised as weighted sums of Gaussian radial basis functions.",
        "**The engineering payoff the paper emphasises:** the process is truncated to a few stages, preserves the structural simplicity of diffusion models, and is *well-suited for parallel computation on GPUs*, in explicit contrast to BM3D, which the paper notes is *challenging for parallel computation*.",
        "**Result and limit.** TNRD reaches 31.42 / 28.92 / 25.97 dB on BSD68 at 0.032 s per 512×512 image on GPU — the best quality-per-second in the classical table. But it trains one model per noise level, and its effective patch size is 61×61 from ten 7×7 convolution layers. `[DnCNN17 Tables I, II, IV]`",
    ]},
    cite="TNRD16 abstract, §1, §2, §3 · DnCNN17 Tables I, II, IV",
    notes="Expect 'what exactly is an influence function?' — it is the derivative of the penalty applied to each filter response; classical diffusion calls it the flux function. TNRD learns its shape instead of assuming one."))

S.append(dict(t="content", era="deepcnn", part="III", kicker="28 · The anchor paper",
    title="DnCNN — the four questions it set out to answer",
    lead="*Beyond a Gaussian Denoiser: Residual Learning of Deep CNN for Image Denoising.* Kai Zhang, Wangmeng Zuo, Yunjin Chen, Deyu Meng, Lei Zhang. IEEE Transactions on Image Processing 26(7), 2017. arXiv:1608.03981.",
    body={"bullets": [
        "**Q1 — Can a deep CNN with residual learning and batch normalisation beat the state of the art on Gaussian denoising?** Answer: yes, by 0.6 dB over BM3D at all three noise levels.",
        "**Q2 — Can a *single* model handle unknown noise levels?** Answer: yes. DnCNN-B trains across σ ∈ [0, 55] and beats noise-level-specific competitors without being told σ.",
        "**Q3 — Can one network handle denoising, super-resolution and JPEG deblocking together?** Answer: yes. DnCNN-3 beats a specialist baseline on all three.",
        "**Q4 — Do residual learning and batch normalisation benefit *each other*?** Answer: yes, and this is the paper's most-cited empirical finding. Neither works nearly as well alone.",
        "**The three contributions, in the authors' framing.** (1) An end-to-end trainable deep CNN that, *unlike existing deep methods which directly estimate the latent clean image*, adopts residual learning to remove the latent clean image from the noisy observation. (2) The finding that residual learning and batch normalisation *greatly benefit CNN learning*, speeding up training and boosting performance. (3) That DnCNN extends easily to general image denoising — one model for blind Gaussian denoising, one model for three tasks.",
        "**Institutions.** Harbin Institute of Technology, The Hong Kong Polytechnic University, Xi'an Jiaotong University. **Citations: 11 674** (Google Scholar, checked 9 August 2026).",
    ]},
    cite="DnCNN17 abstract, §I · citation count: Google Scholar, 9 Aug 2026",
    notes="Recheck the citation count the morning of the defence and say the date you checked. A stale number is a small error that reads as carelessness."))

S.append(dict(t="flow", era="deepcnn", part="III", kicker="29 · Architecture",
    title="Three layer types, one global skip, and nothing else",
    lead="The paper describes the design origin plainly: they *modify the VGG network to make it suitable for image denoising*, and set the depth from the effective patch sizes used by state-of-the-art denoising methods. Given depth D there are exactly three kinds of layer.",
    body={"steps": [
        {"h": "Layer 1 · Conv + ReLU", "p": "64 filters of size 3×3×c generate 64 feature maps; ReLU = max(0,·) follows. c = 1 grayscale, c = 3 colour. **No batch normalisation on the first layer.**"},
        {"h": "Layers 2 … D−1 · Conv + BN + ReLU", "p": "64 filters of size 3×3×64. Batch normalisation is inserted *between* the convolution and the ReLU. Repeated D−2 times — fifteen times in DnCNN-S."},
        {"h": "Layer D · Conv only", "p": "c filters of size 3×3×64 reconstruct the output. **No BN, no ReLU** — the output must be able to take negative values, because it is a noise map."},
        {"h": "Global skip · x̂ = y − v̂", "p": "The network outputs v̂, the predicted *noise*. The clean image is recovered outside the network by subtraction. One skip connection across the entire network."},
    ],
     "bullets": [
        "**Zero padding throughout**, keeping every middle feature map the same size as the input. The paper reports this simple strategy produces **no boundary artefacts**.",
        "**No pooling anywhere.** Pooling discards spatial resolution, and denoising must emit one clean pixel per input pixel. Removing it is what makes the receptive-field arithmetic on slide 32 exact.",
        "**Parameter budget, DnCNN-S, depth 17, grayscale:** layer 1 = 576; layers 2–16 = 15 × (3·3·64·64) = 552 960; layer 17 = 576; BN parameters = 15 × 2 × 64 = 1 920. **Total ≈ 556 K.** The network is one block repeated fifteen times.",
    ]},
    cite="DnCNN17 §III-B, Fig. 1 · parameter breakdown computed from the stated shapes",
    notes="The 'one block repeated fifteen times' observation is the bridge to Part V: DnCNN's power came from depth and training strategy, not architectural cleverness, which is precisely why successors attacked the block."))

S.append(dict(t="math", era="deepcnn", part="III", kicker="30 · The central idea",
    title="Residual learning — predict the dirt, not the photograph",
    lead="The single design choice that defines the paper. Existing discriminative models learn F(y) = x, the clean image. DnCNN learns R(y) ≈ v, the noise, and recovers x = y − R(y).",
    body={"eqs": [
        {"tex": "ℓ(Θ)  =  (1 / 2N) · Σ_{i=1}^{N}  ‖  ℛ( y_i ; Θ )  −  ( y_i − x_i )  ‖²_F",
         "where": "Equation (1) of the paper — averaged MSE between the desired residual images and the estimated ones, over N noisy–clean training patch pairs"},
        ],
     "bullets": [
        "**The target is (y_i − x_i), which is the actual noise.** The loss never looks at the clean image directly. This is the one line to check when opening any denoising repository: does `forward()` return the image or the noise?",
        "**The formal justification, in two steps.** (a) From ResNet: *when the original mapping is more like an identity mapping, the residual mapping will be much easier to optimize.* (b) The observation that closes it: the noisy observation y *is much more like the latent clean image x than it is like the residual image v* — especially at low noise. So F(y) would be closer to an identity mapping than R(y) is, and the residual formulation is more suitable.",
        "**Why learning the identity is genuinely hard.** A stack of convolutions with ReLUs has no built-in way to express 'copy the input unchanged'; seventeen layers would have to conspire into an identity transform, which is a narrow and awkward point in parameter space. A network that outputs *zero*, by contrast, is trivially reachable — drive the weights toward zero. Residual learning relocates the 'do nothing' solution from the hard point to the easy one.",
        "**DnCNN is not ResNet.** The paper is explicit: *unlike the residual network, which uses many residual units (identity shortcuts), DnCNN employs a single residual unit to predict the residual image.* One global skip, not dozens of local ones.",
        "**Priority, stated with a hedge — reproduce the hedge.** Residual prediction had already been used in super-resolution and colour demosaicking, but *to the best of our knowledge there is no work which directly predicts the residual image for denoising.*",
    ]},
    cite="DnCNN17 §II-A, §III-A, Eq. (1)",
    notes="The 'why identity is hard' explanation is not in the paper — it is labelled reading. Say so if pressed. It is the answer that satisfies a TA who asks why the ResNet argument applies here."))

S.append(dict(t="two", era="deepcnn", part="III", kicker="31 · The synergy",
    title="Residual learning and batch normalisation need each other",
    lead="The paper's most cited empirical finding, and a favourite defence question. The claim is a two-way street: *the integration of residual learning and batch normalization can result in fast and stable training and better denoising performance*, and the two *benefit from each other*.",
    body={"left": {"h": "Direction 1 — RL benefits from BN", "bullets": [
        "The straightforward half. BN alleviates internal covariate shift: as training updates early layers, the distribution arriving at later layers keeps moving, and those layers chase a target that will not hold still.",
        "BN normalises activations across the mini-batch before the nonlinearity, then applies a learned scale and shift — only two parameters per activation, trained by back-propagation.",
        "The paper's Fig. 2 shows residual learning *without* BN converges fast but lands below residual learning *with* BN.",
        "Benefits the paper lists: fast training, better performance, low sensitivity to initialisation.",
    ]},
     "right": {"h": "Direction 2 — BN benefits from RL (the surprising half)", "bullets": [
        "Without residual learning, batch normalisation *even has a certain adverse effect on convergence*. BN alone is worse than nothing.",
        "**The mechanism the paper gives.** A mini-batch is a small set — 128 patches. Without residual learning, the input intensity and convolutional features are correlated with their neighbours, so the distribution of layer inputs depends on the *content of the images in that particular batch*.",
        "With residual learning, DnCNN *implicitly removes the latent clean image in the hidden layers*, which makes the inputs of each layer **Gaussian-like distributed, less correlated, and less related to image content**. Residual learning therefore helps BN reduce covariate shift.",
        "**The deeper reason for denoising specifically:** *the residual image and batch normalization are both associated with the Gaussian distribution*, so it is very likely they benefit from each other.",
    ]},
    },
    foot="**Not the optimiser.** The paper checks this: both SGD and Adam give the best results with RL+BN. It is *the integration of residual learning and batch normalization, rather than the optimization algorithm*, that produces the win.",
    cite="DnCNN17 §III-C, Fig. 2",
    notes="Likely question: 'would this hold where the residual is not Gaussian?' The paper guards its own claim in a footnote — this does not mean DnCNN cannot handle other tasks well — and DnCNN-3 proves it on SR and JPEG, where the residual is clearly not AWGN."))

S.append(dict(t="table", era="deepcnn", part="III", kicker="32 · Depth",
    title="Why 17 layers — a hyperparameter with a documented derivation",
    lead="Because pooling is removed and all filters are 3×3, the receptive field of a depth-d DnCNN is exactly (2d+1)×(2d+1). The authors chose d by anchoring that number to the *effective patch size* of competing methods at σ = 25.",
    body={"cols": ["Method", "Effective patch size", "How it arises"],
          "align": "lll",
          "rows": [
            ["EPLL", "36 × 36", "Smallest of the group"],
            ["**DnCNN-S**", "**35 × 35**", "**Depth 17, chosen to sit near the smallest**"],
            ["MLP", "47 × 47", "39×39 patch followed by a 9×9 averaging filter"],
            ["BM3D", "49 × 49", "Non-local search in a 25×25 window, performed twice"],
            ["CSF", "61 × 61", "Ten conv layers with 7×7 filters over five stages"],
            ["TNRD", "61 × 61", "Same construction as CSF"],
            ["WNNM", "361 × 361", "Large window, iterated non-local search"],
          ],
          "hl": [1]},
    foot="**The design question, and it is elegant:** *it is interesting to verify whether DnCNN with a receptive field size similar to EPLL can compete against the leading denoising methods.* For a known σ they set RF = 35×35, depth 17; for other general denoising tasks they adopt a larger field with depth 20 (41×41) — because *high noise level usually requires larger effective patch size*.",
    cite="DnCNN17 Table I, §III-B — table values as printed",
    notes="The killer line: DnCNN wins with a receptive field one tenth the linear extent of WNNM's. It is not seeing more; it is understanding better. That sets up the Barbara slide two slides later."))

S.append(dict(t="table", era="deepcnn", part="III", kicker="33 · Data and training",
    title="The pipeline that made it work",
    lead="This is the slide that answers the brief's Stage 2 question — *how do their data pipelines work* — for the anchor paper itself, and the baseline against which the modern pipelines in Part VI are contrasted.",
    body={"cols": ["Model", "Source images", "Patches", "Patch size", "Noise / task", "Depth"],
          "align": "llllll",
          "rows": [
            ["DnCNN-S", "400 images at 180×180", "128 × 1 600", "40 × 40", "σ fixed at 15, 25 or 50", "17"],
            ["DnCNN-B", "400 images at 180×180", "128 × 3 000", "50 × 50", "σ sampled from [0, 55]", "20"],
            ["CDnCNN-B", "432 BSD colour images", "128 × 3 000", "50 × 50", "σ sampled from [0, 55]", "20"],
            ["DnCNN-3", "91 images + 200 BSD", "128 × 8 000", "50 × 50", "Denoising + SISR + JPEG", "20"],
          ]},
    foot="**Hyperparameters.** MSE on the residual · SGD with momentum 0.9 and weight decay 1e⁻⁴ · learning rate decayed exponentially from 1e⁻¹ to 1e⁻⁴ over 50 epochs · mini-batch 128 · He initialisation · **MatConvNet**, a MATLAB library. Trained on an Intel i7-5820K @ 3.30 GHz with an Nvidia Titan X: **≈ 6 hours** for DnCNN-S, **one day** for DnCNN-B/CDnCNN-B, **three days** for DnCNN-3.",
    cite="DnCNN17 §IV-A · training-time figures from §IV-A",
    notes="Flag MatConvNet out loud. Essentially nothing in modern denoising is MATLAB, and tracing that migration is a direct answer to the brief's question about how pre-trained weights are used today versus before. It returns on slide 96."))

S.append(dict(t="table", era="deepcnn", part="III", kicker="34 · Results, part 1",
    title="BSD68 — the headline benchmark",
    lead="Average PSNR in dB, reproduced from Table II of the paper. The classical block is the same one shown on slide 23; DnCNN's two rows are now added beneath it.",
    body={"cols": ["Method", "σ = 15", "σ = 25", "σ = 50"],
          "align": "lrrr",
          "rows": [
            ["BM3D (2007)", "31.07", "28.57", "25.62"],
            ["EPLL (2011)", "31.21", "28.68", "25.67"],
            ["MLP (2012)", "—", "28.96", "26.03"],
            ["CSF (2014)", "31.24", "28.74", "—"],
            ["WNNM (2014)", "31.37", "28.83", "25.87"],
            ["TNRD (2016)", "31.42", "28.92", "25.97"],
            ["**DnCNN-S** (known σ)", "**31.73**", "**29.23**", "**26.23**"],
            ["**DnCNN-B** (blind)", "**31.61**", "**29.16**", "**26.23**"],
          ],
          "hl": [6, 7]},
    foot="**How to read 0.6 dB without sounding naive.** Prior work found *few methods can outperform BM3D by more than 0.3 dB on average*; MLP and TNRD achieved about 0.35 dB. DnCNN-S outperforms BM3D by **0.6 dB at all three noise levels**, and at σ = 50 both variants exceed BM3D by about 0.6 dB — very close to the estimated PSNR bound over BM3D of 0.7 dB. **DnCNN captured roughly 85% of the theoretically available headroom — and DnCNN-B did it without being told σ.**",
    cite="DnCNN17 Table II, §IV-B",
    notes="The blind row is the more impressive one and presenters usually skip it. DnCNN-B beats every noise-level-specific competitor while not knowing the noise level. Say that explicitly."))

S.append(dict(t="table", era="deepcnn", part="III", kicker="35 · Results, part 2",
    title="Where it loses — and why losing is the interesting result",
    lead="Per-image PSNR at σ = 25, from Table III. DnCNN-S wins on ten of twelve images. The two it loses are not random, and the paper's explanation of them is the most intellectually valuable passage in its experimental section.",
    body={"cols": ["Image", "BM3D", "WNNM", "TNRD", "DnCNN-S", "Δ vs BM3D"],
          "align": "lrrrrr",
          "rows": [
            ["Cameraman", "29.45", "29.64", "29.72", "**30.18**", "+0.73"],
            ["House", "32.85", "**33.22**", "32.53", "33.06", "+0.21"],
            ["Peppers", "30.16", "30.42", "30.57", "**30.87**", "+0.71"],
            ["Monarch", "29.25", "29.84", "29.85", "**30.28**", "+1.03"],
            ["Parrot", "28.93", "29.15", "29.18", "**29.43**", "+0.50"],
            ["**Barbara**", "30.71", "**31.24**", "29.41", "30.00", "**−0.71**"],
            ["Boat", "29.90", "30.03", "29.91", "**30.21**", "+0.31"],
            ["Average (12)", "29.97", "30.26", "30.06", "**30.44**", "+0.47"],
          ],
          "hl": [5]},
    foot="**The paper's own explanation.** DnCNN-S fails to achieve the best result on exactly the two images *dominated by repetitive structures*, consistent with a known finding: *non-local means based methods are usually better on images with regular and repetitive structures, whereas discriminative training based methods generally produce better results on images with irregular textures.* Images with regular repetitive structures *meet well with the non-local similarity prior*; irregular textures *weaken the advantage of that specific prior*.",
    cite="DnCNN17 Table III, §IV-C — values as printed",
    notes="This is the most important slide in Part III for the narrative. Barbara's scarf is bottleneck 3, visible in 2017, three years before anyone could fix it. Point at −0.71 and say: this number is why Part V exists."))

S.append(dict(t="table", era="deepcnn", part="III", kicker="36 · Results, part 3",
    title="Runtime — the commercial argument, stated honestly",
    lead="Seconds per image at noise level 25, from Table IV. This table is the reason denoising moved into products, and it is also the table on which a careless presenter gets caught.",
    body={"cols": ["Method", "256×256", "512×512", "1024×1024", "Device"],
          "align": "lrrrl",
          "rows": [
            ["BM3D", "0.65", "2.85", "11.89", "CPU"],
            ["WNNM", "203.1", "773.2", "2 536.4", "CPU"],
            ["EPLL", "25.4", "45.5", "422.1", "CPU"],
            ["MLP", "1.42", "5.51", "19.4", "CPU"],
            ["CSF", "2.11 / —", "5.67 / 0.92", "40.8 / 1.72", "CPU / GPU"],
            ["TNRD", "0.45 / 0.010", "1.33 / 0.032", "4.61 / 0.116", "CPU / GPU"],
            ["**DnCNN-S**", "0.74 / **0.014**", "3.41 / **0.051**", "12.1 / **0.200**", "CPU / GPU"],
            ["**DnCNN-B**", "0.90 / **0.016**", "4.11 / **0.060**", "14.1 / **0.235**", "CPU / GPU"],
          ],
          "hl": [6, 7]},
    foot="**State the asymmetry before you are asked.** The paper itself warns that *since GPU run time varies greatly with respect to GPU and GPU-accelerated library, it is hard to make a fair comparison* between CSF, TNRD and DnCNN — the authors simply **copied the CSF and TNRD GPU times from the original papers**. And BM3D's 2.85 s is a CPU figure being set beside a GPU figure. The honest headline is: **DnCNN-B is 12 900× faster than WNNM at 512×512 (773.2 s CPU → 0.060 s GPU)**, with the hardware difference named.",
    cite="DnCNN17 Table IV and its caption",
    notes="Reproducing the paper's own caveat is what separates a rigorous presentation from a marketing one. A sharp TA will check exactly this."))

S.append(dict(t="two", era="deepcnn", part="III", kicker="37 · The title's claim",
    title="One model, three tasks — 'beyond a Gaussian denoiser'",
    lead="The conceptual leap that gives the paper its name. Reinterpret v, and the identical network, identical loss and identical training procedure solve two problems that are not denoising.",
    body={"left": {"h": "The reinterpretation", "bullets": [
        "**Denoising:** v is AWGN, σ ∈ [0, 55].",
        "**Super-resolution:** if v is *the difference between a ground-truth high-resolution image and the bicubic upsampling of its low-resolution version*, the same degradation model becomes single-image SR. Scales ×2, ×3, ×4.",
        "**JPEG deblocking:** if v is *the difference between the original image and its compressed version*, the model becomes JPEG deblocking. Quality factors 5–99.",
        "The paper's conclusion: SISR and JPEG deblocking *are special cases of a 'general' image denoising problem* — even though their v is very different from AWGN.",
    ]},
     "right": {"h": "The theoretical permission, and the results", "bullets": [
        "It is not asserted but derived: from the connection with one-stage TNRD, the residual estimate remains valid whenever *the derivative of the data-fidelity term vanishes at zero*, a condition holding for *many types of noise distributions, e.g. the generalized Gaussian distribution*. The authors state it is natural to assume it also holds for SISR and JPEG noise.",
        "**Denoising, BSD68 σ=25:** BM3D 28.57, TNRD 28.92 → **DnCNN-3 29.02**.",
        "**SR, Set5 ×3:** TNRD 33.18, VDSR 33.67 → **DnCNN-3 33.75**. Set14 ×3: TNRD 29.43, VDSR 29.77 → **29.81**.",
        "**JPEG, Classic5 QF10:** AR-CNN 29.03, TNRD 29.28 → **DnCNN-3 29.40**. LIVE1 QF20: AR-CNN 31.29, TNRD 31.46 → **31.59**.",
        "**Reproduce the hedge.** The paper says *to the best of our knowledge* none of the existing methods had been reported for handling these three tasks with only a single model. Overstating priority is exactly what a defence punishes.",
    ]},
    },
    cite="DnCNN17 §III-D, Table V — values as printed",
    notes="Fig. 12 of the paper shows one input image with six differently-degraded regions restored by one model, described as looking natural without obvious artefacts. Mention it; it is the visual proof."))

S.append(dict(t="cards", era="deepcnn", part="III", kicker="38 · Bottleneck 2",
    title="What DnCNN settled, and the bill it left behind",
    lead="DnCNN closed bottleneck 1 completely. It removed test-time optimisation, removed hand-tuned constants, removed the per-noise-level model, and made denoising real-time. In doing so it created a new dependency that the next era spent seven years attacking.",
    body={"cards": [
        {"tag": "Settled", "h": "Test-time cost", "p": "One forward pass. 0.060 s for a 512×512 image. WNNM's 773 s is gone and never comes back — every method after 2017 is a feed-forward network."},
        {"tag": "Settled", "h": "Blind operation", "p": "DnCNN-B needs no σ estimate. The workaround of estimating noise first and loading a matching model — which made the result hostage to the estimate — is obsolete."},
        {"tag": "**The bill**", "h": "Paired clean data", "p": "The loss is ‖ℛ(y) − (y − x)‖². It requires **x**. DnCNN's 400 clean images plus synthetic noise are cheap for natural photographs and **impossible** for fluorescence microscopy, cryo-electron microscopy, MRI, or astronomy, where a clean ground truth does not exist and cannot be acquired."},
        {"tag": "**The bill**", "h": "The local receptive field", "p": "35×35 pixels. Barbara's scarf, −0.71 dB against BM3D. The non-local self-similarity prior that BM3D and WNNM exploited for free is simply unavailable to a stack of 3×3 convolutions."},
    ]},
    foot="**The 2018 fork.** These two debts were attacked independently and almost simultaneously, by different communities, with different methods — and they never merged. Parts IV and V follow one branch each.",
    cite="reading, grounded in DnCNN17 §III-A Eq. (1), Table I and Table III · N2V19 §1 on the unavailability of ground truth",
    notes="This is the hinge of the whole deck. Slow down here. The fork is the structural claim that distinguishes your narrative from a chronological list, and the TA will notice it."))
