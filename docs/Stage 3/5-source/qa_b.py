# -*- coding: utf-8 -*-
from qa_a import Q

BANK = []
A = BANK.append

# ═══════════════ 4. DATA BRANCH ═══════════════
A(Q("n2n", "B", "Stage 3 → Part IV → Noise2Noise",
"How can training on noisy targets possibly work?",
r"""The argument is about what \(L_2\) regression actually learns. For a set of observations,
\[ \arg\min_z \mathbb{E}_y\{(z-y)^2\} = \mathbb{E}_y\{y\} \]
— the \(L_2\) minimiser is the **conditional mean** of the target. The paper states the consequence as a triviality: *on expectation, the estimate remains unchanged if we replace the targets with random numbers whose expectations match the targets.*

So if we train
\[ \arg\min_\theta \sum_i L\big(f_\theta(\hat{x}_i), \hat{y}_i\big)
\quad\text{subject to}\quad \mathbb{E}\{\hat{y}_i \mid \hat{x}_i\} = y_i \]
the optimal parameters are unchanged from clean-target training. A second noisy photograph of the same scene satisfies exactly that condition, because the noise is zero-mean.

Given infinite data the solution is identical to clean-target training. For finite data the extra variance is the average corruption variance divided by the number of training samples — so the penalty **shrinks with dataset size** rather than persisting.

Two things are notably *not* required: no likelihood model of the corruption, and no density model of the clean image manifold.

**Measured cost**, Kodak/BSD300/Set14 averages at \(\sigma=25\): clean targets 31.63 dB, noisy targets 31.61 dB. A gap of **0.02 dB** — about one fiftieth of the margin DnCNN gained over BM3D. The clean-data requirement was never actually necessary.

The loss also selects the estimator: \(L_2\) recovers the mean, \(L_1\) the median (allowing up to 50% outlier content), \(L_0\) the mode.""",
"""If you ask someone to guess a number and score them on squared error, their best strategy is to guess the average. It does not matter whether you show them the true value or a noisy version of it — as long as the noise averages out, the average is the same.""",
["conditional mean", "L2 minimiser", "zero-mean corruption", "finite-sample variance", "loss selects estimator"],
[("Why does \\(L_1\\) give the median?",
  "Minimising \\(\\mathbb{E}|z-y|\\) puts the optimum where half the probability mass lies on each side, which is the median by definition. That is why \\(L_1\\)-trained networks tolerate heavy outlier corruption — a median ignores extreme values that would drag a mean."),
 ("Does Noise2Noise need the two noisy images to have the same noise level?",
  "No. The condition is on the conditional expectation, not on the variance. Different noise levels change the finite-sample variance penalty but not the optimum."),
 ("What is the practical limitation?",
  "You must capture the same scene twice, independently. That rules out anything that moves, and every archival or single-shot image. Noise2Void exists specifically to remove that requirement.")],
[("Noise2Noise learns to reproduce noise, so its output must be noisy.",
  "It learns the conditional mean of a noisy target, and that mean is the clean image.",
  "The network cannot predict the specific noise realisation in the target because it is independent of the input. The best it can do — and what the loss drives it to — is predict the mean, which is clean.")],
hard=True))

A(Q("n2v", "B", "Stage 3 → Part IV → Noise2Void",
"Why can a blind-spot network not simply learn the identity?",
r"""Noise2Void trains with the same noisy image as input and target. Naively that degenerates instantly: the identity function has zero loss and does nothing useful.

The fix is a **blind spot**: the prediction for pixel \(i\) is allowed to depend on every pixel in a square neighbourhood **except pixel \(i\) itself**.

The reason this works rests on two stated assumptions:
\[ p(s,n) = p(s)\,p(n\mid s), \qquad p(n\mid s) = \prod_i p(n_i \mid s_i), \qquad \mathbb{E}[n_i]=0 \]
1. the signal \(s\) is **not** pixel-wise independent — \(p(s_i \mid s_j) \neq p(s_i)\);
2. the noise **is** conditionally pixel-wise independent given the signal, and zero-mean.

Given assumption 2, the neighbouring pixels *carry no information whatsoever about the value of \(n_i\)*. It is impossible for the network to beat the a priori expected value of the noise. Given assumption 1, the signal *can* still be estimated from the surroundings. So the network can learn the signal and cannot learn the noise. The degenerate solution is unreachable by construction.

**The implementation is a trick, not an architecture.** Building a true blind-spot receptive field efficiently is awkward, so N2V instead *replaces the value in the centre of each input patch with a randomly selected value from the surrounding area* and computes the loss **only** at those masked pixels. Any standard CNN then acquires the property. For gradient efficiency it masks \(N = 64\) pixels per \(64\times64\) patch — 1.6% — rather than one.""",
"""You are asked to guess a pixel without being allowed to look at it. You can use the pattern around it, so you can guess the picture. You cannot guess the random speck that landed on it, because nothing around it knows about that speck.""",
["blind-spot receptive field", "conditional pixel-wise independence", "masking scheme", "degenerate identity solution"],
[("What breaks the method?",
  "Spatially correlated noise. If neighbours carry information about a pixel's own noise, the blind spot no longer prevents learning the noise. Resizing, demosaicing and JPEG all produce correlated noise — which is why P2N notes that RDC-constructed data is unsuitable for N2V training."),
 ("What does the blind spot cost?",
  "On BSD68 at \\(\\sigma = 25\\): supervised 29.06, Noise2Noise 28.86, BM3D 28.59, **Noise2Void 27.71**. So it is 1.35 dB below supervised and 0.88 dB below a 2007 algorithm. The paper does not hide this."),
 ("Then why does N2V matter?",
  "Because that comparison only exists where the alternatives exist. On cryo-TEM and the Cell Tracking Challenge datasets the paper's own figure captions the ground-truth column *does not exist*. Self-supervision is an availability technique, not a quality technique.")],
[("Self-supervised denoising is a better method than supervised denoising.",
  "It measurably is not, where clean data is available.",
  "It trades PSNR for applicability. Where clean data exists, supervision wins by 1.35 dB. Where it does not, the comparison is between 27.71 and nothing at all.")],
hard=True))

A(Q("zsn2n", "B", "Stage 3 → Part IV → ZS-N2N",
"How does ZS-N2N denoise an image with no training set at all?",
r"""It manufactures a Noise2Noise pair from the single image using two fixed stride-2 convolutions:
\[ k_1 = \begin{pmatrix} 0 & \tfrac12 \\ \tfrac12 & 0\end{pmatrix}, \qquad
   k_2 = \begin{pmatrix} \tfrac12 & 0 \\ 0 & \tfrac12\end{pmatrix} \]
Each \(2\times2\) block is split into its diagonal average \(D_1\) and anti-diagonal average \(D_2\), giving two half-resolution images. Because nearby clean pixels are highly correlated while noise is unstructured and independent, the pair has *similar signal but independent noise* — an approximation of two observations of one scene.

Then fit a network to that one image with two losses:
\[ L_{\text{res}} = \tfrac12\left(\lVert D_1 - f_\theta(D_1) - D_2\rVert^2 + \lVert D_2 - f_\theta(D_2) - D_1\rVert^2\right) \]
\[ L_{\text{cons}} = \tfrac12\left(\lVert D_1 - f_\theta(D_1) - D_1(y - f_\theta(y))\rVert^2 + \lVert D_2 - f_\theta(D_2) - D_2(y - f_\theta(y))\rVert^2\right) \]
Minimise \(L = L_{\text{res}} + L_{\text{cons}}\) by gradient descent on \(\theta\) alone — \(D_1, D_2\) are fixed — then estimate \(\hat{x} = y - f_{\hat\theta}(y)\).

**Why consistency matters:** the residual loss only ever shows the network half-resolution input. The consistency term is the only one that sees the image at full resolution, and it requires denoise-then-downsample to agree with downsample-then-denoise. The paper describes it as a regulariser that *enables better denoising performance and helps to avoid overfitting*, removing the early stopping that DIP and Noise2Fast require.

**The network is two \(3\times3\) operators and one \(1\times1\) — about 20 000 parameters**, converging in 1–2 K iterations, under a minute on CPU. The ablation shows a U-Net substitution *overfits* and performs much worse, so the tiny network is load-bearing rather than a compromise. For comparison, Self2Self needs *1.2 hours to denoise one \(256\times256\) image on a GPU*.

Note that \(f_\theta\) predicts the **noise** — DnCNN's 2017 design choice, still the default in 2023.""",
r"""Take the two diagonals of every \(2\times2\) square. They show almost the same picture but carry different noise, so each can act as the other's training target. It is Noise2Noise with the second photograph carved out of the first.""",
["pair downsampler", "residual loss", "consistency loss", "per-image optimisation", "overfitting and capacity"],
[("Why does a *smaller* network work better here?",
  "Because there is only one image. A high-capacity network can memorise the noise realisation, which is exactly the failure mode; 20 K parameters cannot. Capacity limitation is doing the job that a training set would otherwise do."),
 ("Is this the same as Deep Image Prior?",
  "Related but not the same. DIP relies on the untrained network's structural bias and needs careful early stopping. ZS-N2N constructs an explicit self-supervised target from the pair downsampler and uses the consistency term as a regulariser, which is what removes the early-stopping requirement."),
 ("What is the cost of the zero-shot setting?",
  "Test-time optimisation returns. You pay 1–2 K gradient steps per image, which is the classical era's per-image cost reappearing — except that what is optimised is now a network rather than a pixel grid.")],
[],
hard=False))

A(Q("p2n", "B", "Stage 3 → Part IV → P2N",
"Is P2N just a new loss function? Justify your answer precisely.",
r"""No, and the distinction is exactly the kind a defence probes.

P2N has two mechanisms. **Renoised Data Construction (RDC)** denoises the image once, estimates the noise, then adds that estimated noise back with a plus and with a minus, producing \(y^{+}\) and \(y^{-}\) — both at full resolution, with every pixel retained. **Denoised Consistency Supervision (DCS)** then denoises \(y^{+}\) and \(y^{-}\) and trains the two results to agree.

A loss function scores a **fixed prediction** against a **fixed target**. P2N changes three things a loss function cannot:

1. **What goes into the network.** \(y^{+}\) and \(y^{-}\) are constructed from the model's own output and do not exist until the model has run once.
2. **How many forward passes there are.** Three, not one: denoise \(y\), then \(y^{+}\), then \(y^{-}\).
3. **Which pair is scored.** Output against output, not output against target.

The contribution the title names — breaking *the information-lossy barrier* — is that neither masking nor downsampling is required. N2V blinds 1.6% of pixels; ZS-N2N halves the resolution. P2N pays neither tax.

Meanwhile the **architecture is untouched**: the network class in the official repository is literally named `UNet_n2n_un` and matches the 2018 Noise2Noise channel widths. P2N+ adds one optional module, Symmetric Prior Injection. Seven years of progress on this branch, and the backbone is the same one.""",
"""Changing the loss is changing how you grade the exam. P2N changes what questions are on the exam, how many exams there are, and whose answers get compared.""",
["RDC", "DCS", "supervision vs loss", "information-lossy barrier", "unchanged backbone"],
[("Why can RDC data not be used to train Noise2Void?",
  "Because the noise in RDC-constructed images is **correlated**, which violates N2V's conditional pixel-wise independence assumption and collapses its training. The paper states this, and the repository contains those `--mode` branches as a documented negative result — reading the flag table without the paper would lead to the opposite conclusion."),
 ("What does Symmetric Prior Injection cost?",
  "Measured: it *reduces* parameters by 6.7% (0.991 M → 0.925 M) because `Symlayer` routes through a half-width bottleneck, yet raises CPU latency 2.5× (0.286 s → 0.710 s) because every layer is evaluated twice, on \\(x\\) and on \\(-x\\). The opposite of what a parameter table predicts."),
 ("Does P2N close the gap to supervised training?",
  "No. Its contribution is removing the information loss, not closing the quality gap, and it still pays per-image test-time optimisation. Bottleneck 2 is mitigated, not closed.")],
[("P2N is an incremental variant of ZS-N2N.",
  "They solve different sub-problems. ZS-N2N removes the training set; P2N removes the information sacrifice that all prior self-supervised methods paid.",
  "Read the data branch as a sequence of requirement removals: clean target (N2N) → second copy (N2V) → training set (ZS-N2N) → information loss (P2N).")],
hard=True))

# ═══════════════ 5. ARCHITECTURE BRANCH ═══════════════
A(Q("attention-cost", "B", "Stage 3 → Part V → Attention complexity",
"Why can standard self-attention not be applied to image restoration?",
r"""Standard self-attention is
\[ \mathrm{Attention}(Q,K,V) = \mathrm{softmax}\!\left(\frac{QK^{\top}}{\sqrt{d_k}}\right)V \]
The \(QK^{\top}\) term produces one weight for **every pair of elements**, so for a \(W\times H\) image the cost is
\[ O(W^2H^2) \]
quadratic in the number of pixels.

The arithmetic makes it concrete. A \(256\times256\) image has 65 536 spatial positions, so the attention matrix has about \(4.3\times10^9\) entries. At \(512\times512\) it is \(6.9\times10^{10}\). Restoration routinely runs at those resolutions and above. For contrast, a ViT at \(224\times224\) with \(16\times16\) patches has **196 tokens** — classification and restoration are simply not the same computational problem. Restormer states the constraint directly: *it is infeasible to apply SA on most image restoration tasks that often involve high-resolution images.*

Three responses exist in this project:

- **Restrict the window.** SwinIR attends inside fixed local windows, shifting them between layers. It works, but Restormer's objection is structural: *restricting the spatial extent of SA is contradictory to the goal of capturing the true long-range pixel relationships* — you have bought back the locality you were trying to escape.
- **Change the axis.** If 65 536 spatial positions are unaffordable, attend over the **channels** instead. There are 48. This is Restormer's MDTA.
- **Abandon attention.** NAFNet argues the gains were never attention's to begin with; MambaIR replaces it with a state-space recurrence that is linear in sequence length.""",
"""Attention lets everything talk to everything. With 65 000 pixels that is 4 billion conversations per layer. Either you shrink the room, change who is talking, or find a different way to pass messages.""",
["quadratic complexity", "token count", "windowed attention", "locality trade-off"],
[("Why is quadratic cost acceptable in NLP but not vision?",
  "Sequence lengths. A language model might handle a few thousand tokens; an image at \\(512^2\\) has 262 144 positions, two orders of magnitude more, and restoration cannot downsample them away because the output must be full resolution."),
 ("Why can't you just patch the image like ViT does?",
  "Patching discards spatial resolution within each patch. Classification only needs a label, so that loss is acceptable; denoising needs one clean pixel per input pixel, so it is not."),
 ("Is windowed attention actually bad?",
  "No — SwinIR is competitive and reaches the top of denoising tables. Restormer's objection is about the *principle*, and its evidence is efficiency rather than accuracy: Restormer reports 3.14× fewer FLOPs and 13× faster runtime than SwinIR at comparable quality.")],
[],
hard=False))

A(Q("mdta", "B", "Stage 3 → Part V → Restormer MDTA",
"How does Restormer make attention linear in the number of pixels?",
r"""By transposing which axis the attention is computed over. Multi-Dconv Head Transposed Attention forms
\[ Q = W_d^{Q}W_p^{Q}Y, \quad K = W_d^{K}W_p^{K}Y, \quad V = W_d^{V}W_p^{V}Y \]
where \(W_p\) is a \(1\times1\) point-wise convolution aggregating cross-channel context and \(W_d\) is a \(3\times3\) **depth-wise** convolution encoding channel-wise spatial context. Then
\[ \mathrm{Attention}(\hat{Q},\hat{K},\hat{V}) = \hat{V}\cdot\mathrm{softmax}\!\left(\frac{\hat{K}\hat{Q}^{\top}}{\alpha}\right) \]
with the tensors reshaped so that the dot product yields a \(C \times C\) **transposed-attention map** — a cross-covariance across feature channels — rather than an \(HW \times HW\) map over pixels.

**Why that is linear.** The attention matrix is \((C/k)\times(C/k)\) per head, independent of \(H\) and \(W\). At level 1 with \(C = 48\) and one head, that is a \(48\times48\) matrix whether the image is \(256\times256\) or \(4000\times3000\). Cost therefore grows *linearly* in pixel count.

**In what sense is it global?** Every channel is computed from every pixel, so channel statistics carry image-wide information, and weighting channels by their mutual covariance implicitly encodes global relationships. The paper is careful: contextualised global relationships are *implicitly* modelled. It never claims pairwise pixel attention.

**The depth-wise convolutions are load-bearing.** The paper calls local context mixing before covariance computation *an important feature* of the block, and the ablation proves it: removing depth-wise convolution from MDTA drops Urban100 \(\sigma{=}50\) from 29.43 to 29.28.

In code this is one `einops` pattern: `'b (head c) h w -> b head c (h w)'` puts pixels on the last axis and channels second-to-last, which is what makes `q @ k.transpose(-2,-1)` come out \(C\times C\).""",
"""Instead of asking "which pixels matter to this pixel?", ask "which feature maps matter to this feature map?". There are 48 feature maps and 65 000 pixels, so the second question is four billion times cheaper — and because every feature map was computed from the whole image, the answer still carries global information.""",
["transposed attention", "cross-covariance", "depth-wise convolution", "linear complexity", "einops layout"],
[("Is channel attention genuinely a substitute for spatial attention?",
  "Partially, and the evidence is empirical rather than theoretical. Restormer's Urban100 gain over DnCNN is 1.98 dB at \\(\\sigma=50\\), so it recovers most of the non-locality gap. Whether it is 'really global' is a fair philosophical objection the paper sidesteps by saying *implicitly*."),
 ("What does the full ablation say?",
  "On Urban100 at \\(\\sigma=50\\): baseline UNet-with-Resblocks 29.11 → MDTA+FN 29.43 → MTA+GDFN 29.54 → **MDTA+GDFN 29.62**. Total 0.51 dB for a 5% FLOP increase; MDTA contributes 0.32 dB and GDFN 0.26 dB over standard FN."),
 ("What is `self.temperature` in the code?",
  "A learned per-head scale replacing the fixed \\(1/\\sqrt{d_k}\\). Combined with `F.normalize` along the pixel axis, it turns the product into a scaled cosine similarity between channels.")],
[("Restormer is fast because attention is linear, so it must be fast everywhere.",
  "Linear complexity is an asymptotic statement about FLOPs, not about wall-clock on a given backend.",
  "Measured on CPU at \\(256^2\\), Restormer took 10.436 s — the slowest model we ran — because three `rearrange` calls force tensor-layout changes and attention matmuls are poorly served by a CPU backend.")],
hard=True))

A(Q("nafnet", "B", "Stage 3 → Part V → NAFNet",
"Derive SimpleGate from GELU, and explain what NAFNet's ablation actually proves.",
r"""**The derivation.** A gated linear unit is
\[ \mathrm{GLU}(X, f, g, \sigma) = f(X)\odot\sigma(g(X)) \]
and GELU is \(\mathrm{GELU}(x) = x\,\Phi(x)\) with \(\Phi\) the standard normal CDF. Setting \(f\) and \(g\) to the identity and \(\sigma = \Phi\) recovers GELU exactly — **GELU is a special case of a GLU**. That suggests a GLU is a generalisation of activation functions rather than a separate component.

The key observation is that the GLU *itself contains nonlinearity and does not depend on \(\sigma\)*: even with \(\sigma\) removed, \(f(X)\odot g(X)\) is still nonlinear, because the product of two linear transformations is not linear. So the activation function can be deleted and the gate alone supplies the nonlinearity:
\[ \mathrm{SimpleGate}(X, Y) = X \odot Y \]
implemented as a channel split and an element-wise multiply. Compare implementations: GELU is approximated as \(0.5x\left(1+\tanh\left[\sqrt{2/\pi}\,(x + 0.044715x^3)\right]\right)\); SimpleGate is `x1, x2 = x.chunk(2, dim=1); return x1 * x2`.

Applying the same argument to channel attention, \(\mathrm{CA}(X) = X * \sigma(W_2\max(0, W_1\,\mathrm{pool}(X)))\) has the form \(X * \Psi(X)\). Keeping only its two essential roles — aggregating global information and channel interaction — gives
\[ \mathrm{SCA}(X) = X * W\,\mathrm{pool}(X) \]
one pooling and one \(1\times1\), with no Sigmoid and no ReLU.

**What the ablation proves.** On SIDD, at a fixed ≈16 GMAC budget: PlainNet 39.29 → **+LayerNorm 39.73** → GELU 39.71 → +CA 39.85 → SimpleGate 39.93 → SCA 39.96, with the full-capacity model at 40.30 dB.

Three readings. (a) **The largest single gain is LayerNorm, +0.44 dB** — and the reason is that it stabilises training at a ten-times larger learning rate. The architecture did not improve; the optimisation did. (b) Both simplifications **improved** the result. (c) The claim that follows is the paper's own: this is *the first work demonstrating that the nonlinear activation functions may not be necessary for SOTA computer vision methods*.""",
"""If multiplying two things together is already nonlinear, you do not need a separate nonlinearity. NAFNet noticed that the gate everyone was putting *after* the activation could replace the activation entirely.""",
["gated linear unit", "SimpleGate", "simplified channel attention", "ablation ladder", "LayerNorm and learning rate"],
[("Why is \\(X \\odot Y\\) nonlinear?",
  "Because it is a product of two functions of the same input. Write \\(X = Ax\\), \\(Y = Bx\\); then \\(X \\odot Y\\) contains terms quadratic in \\(x\\), so it is not a linear map. Linearity would require \\(f(ax_1 + bx_2) = af(x_1)+bf(x_2)\\), which a product violates."),
 ("What is the honest lesson of the LayerNorm row?",
  "That a substantial share of reported architectural progress in restoration is optimisation progress in disguise. It is the most intellectually useful line in Part V and worth volunteering."),
 ("Why is NAFNet 116 M parameters yet fast?",
  "Width doubles per level, so the 12 middle blocks run at 1024 channels and roughly 88 M of the 116 M sits in the bottleneck. But \\(1\\times1\\) and depth-wise convolutions map onto highly optimised GEMM kernels, so measured CPU latency at \\(256^2\\) is 1.899 s — 5.5× faster than Restormer with 4.4× the parameters.")],
[("Removing nonlinearities must reduce a network's expressive power.",
  "It would, if the network became linear. It does not.",
  "SimpleGate replaces one nonlinearity with another. The network is still nonlinear; it is just nonlinear through multiplication rather than through a transcendental function.")],
hard=True))

A(Q("scunet-mamba", "B", "Stage 3 → Part V → SCUNet and MambaIR",
"SCUNet and MambaIR attack the same bottleneck from different directions. Contrast them.",
r"""**MambaIR — a new operator.** It borrows a selective structured state-space model. The continuous system
\[ h'(t) = Ah(t) + Bx(t), \qquad y(t) = Ch(t) + Dx(t) \]
is discretised by zero-order hold, \(\bar{A} = \exp(\Delta A)\), and then admits two equivalent forms: a **recurrent** form \(h_k = \bar{A}h_{k-1} + \bar{B}x_k\), which gives an unbounded receptive field, and a **convolutional** form \(y = x \circledast \bar{K}\), which is parallelisable. Mamba keeps both, and makes \(B, C, \Delta\) **input-dependent** — the *selective* part — giving content-adaptive behaviour rather than one fixed linear system. Complexity is linear in sequence length, so linear in pixel count.

Adapting a sequence model to a plane needs two repairs the paper names: **local pixel forgetting**, because flattening puts vertically adjacent pixels hundreds of steps apart, fixed by a local convolution; and **channel redundancy** from the excessive hidden-state count, fixed by channel attention. Scanning is four-directional (ablation: 34.15 on Urban100 versus 34.06 for one direction).

**SCUNet — a new training distribution.** Architecturally it runs local and non-local priors *in parallel*: a \(1\times1\) convolution, split the feature map in two, send one half to a Swin Transformer block and the other to a residual convolutional block, concatenate. But its distinctive contribution is on the data side — synthesising Gaussian (3-D generalised, with a \(3\times3\) covariance matrix for cross-channel correlation), Poisson, speckle, JPEG, and **camera sensor noise generated through a real ISP** (invert to raw, add read and shot noise there, run demosaicing/white-balance/tone-mapping/gamma forward), plus resizing, random shuffling and double degradation.

**The contrast that matters.** Every other paper in Part V competes on the architecture. SCUNet's premise is that the benchmark itself is the problem: a model trained by AWGN *performs poorly for most of real images due to noise assumption mismatch*. **The distribution you train on is a design surface**, and it is the one that attacks the AWGN assumption most directly.""",
"""MambaIR builds a better telescope. SCUNet argues you have been pointing the telescope at the wrong sky.""",
["state-space model", "selective scan", "dual RNN/CNN form", "degradation synthesis", "ISP simulation", "noise assumption mismatch"],
[("Why is an RNN suddenly fast again?",
  "Because training uses the convolutional form, which is parallel, and inference uses a hardware-aware parallel scan. The recurrence is never run as a naive sequential loop over 65 000 pixels."),
 ("What did the code tell you about MambaIR?",
  "That it cannot be imported at all without compiled CUDA extensions — `ModuleNotFoundError: mamba_ssm`. That is not a gap in the experiment; it is a deployment result no paper reports. Its own changelog also records that published `thop` complexity figures were wrong."),
 ("Does SCUNet win on the AWGN benchmarks?",
  "It is not the top of any AWGN table, and it does not need to be. Its 9.663 M parameters make it the smallest of the four, and its argument is robustness on real photographs that have been resized or JPEG-compressed before you ever see them.")],
[("MambaIR replaced Transformers in image restoration.",
  "Nothing has replaced anything. Restormer leads Urban100, NAFNet leads SIDD at 40.30 dB, MambaIR leads DND by 0.01 dB.",
  "The field currently holds three architectural answers and one data-side answer to bottleneck 3, published across three years, none of which has displaced the others.")],
hard=False))

# ═══════════════ 6. CODE ═══════════════
A(Q("code-prior", "C", "Stage 3 → Part VI → The organising question",
"You claim the deck asks one question of every codebase. What is it, and what does each era answer?",
r"""The question is: **open the source file — where is the prior?**

**Classical.** `scikit-image 0.26.0`, `denoise_tv_chambolle`. Four era-defining facts sit on one screen: the `weight` argument *is* \(\lambda\); `norm.sum()` *is* \(\Phi(x) = \lVert\nabla x\rVert_1\), one line of arithmetic you can read and differentiate by hand; the `while` loop *is* the test-time optimisation; and the `break` on relative energy change is the stopping criterion. Nothing persists — call it on a second image and every iteration runs again. That is bottleneck 1 expressed as control flow.

**Deep CNN.** `cszn/KAIR`, `network_dncnn.py`. The architecture is a list comprehension:
```python
m_body = [B.conv(nc, nc, mode='C'+act_mode, bias=bias) for _ in range(nb-2)]
```
and `forward` returns `x-n`. The layer grammar is a three-character string — `'CBR'`, `'CR'`, `'C'`. **The prior is not in the file at all.** It is in the `.pth` checkpoint the class will load. This is the moment the prior stops being readable.

**Data branch.** In `P2N-plus`, `noise_estimation_loss` does not merely score an output — it *constructs the inputs* and runs three forward passes. And one function implements all the competing self-supervised paradigms behind a `--mode` flag. The network class is `UNet_n2n_un`, matching 2018 channel widths.

**Architecture branch.** Restormer's linear complexity is one `rearrange`. NAFNet's SimpleGate is `chunk` and multiply.

**The arc in one sentence:** the prior moved out of the algorithm and into the weights — and then, on the data branch, partly back *out* of the weights and into a per-image optimisation that needs no clean data.""",
"""In 2007 you could read the assumption. In 2017 you could only download it. That single change is what the whole engineering section documents.""",
["test-time optimisation", "state_dict checkpoints", "supervision in code", "architecture as config"],
[("Why use KAIR rather than DnCNN's own repository?",
  "The original is MatConvNet, a MATLAB library, and the brief scopes the code deep-dive to modern approaches. But the MATLAB fact is itself an exhibit — essentially nothing in modern denoising is MATLAB, and tracing that migration answers the brief's question about pre-trained weights directly. KAIR is by DnCNN's own first author and is the PyTorch reference the field uses."),
 ("What is the subtlety in `return x-n`?",
  "The *paper's* network outputs \\(\\hat{v}\\) and the subtraction happens outside; KAIR folds the subtraction into `forward`, so the module returns the clean image. The residual mapping is still what the weights learn — only the module boundary moved."),
 ("Why does pinning commits matter?",
  "Because `main` moves, and a claim about a moving branch is not reproducible. Every code claim in the project is tied to a specific commit — Restormer `68dc6ac`, NAFNet `2b4af71`, SCUNet `52e440a`, MambaIR `33d7b34`, P2N+ `8a117db`.")],
[],
hard=False))

A(Q("frameworks", "C", "Stage 3 → Part VI → Frameworks and weights",
"How are pre-trained weights used today compared with older manual methods?",
r"""**Then — the classical artefact.** What ships is an algorithm plus constants a human chose. There is no reuse: every image restarts from nothing, and nothing computed on image 1 helps image 2. Adapting to a new domain means re-deriving the prior or re-tuning constants by hand. Reproducibility depends on matching a parameter table that is often in prose rather than code. **The knowledge lives in the paper.**

**Now — the modern artefact.** What ships is a `.pth` file: a serialised `state_dict`, a dictionary mapping layer names to tensors, downloaded once and reused indefinitely. Loading is `model.load_state_dict(torch.load(path))`, with `strict=True` by default so a shape mismatch fails loudly rather than silently. Distribution is via GitHub Releases, Google Drive links, and increasingly Hugging Face model cards carrying architecture, training data, metrics and licence as structured metadata. Adaptation means fine-tuning, or using the weights as an initialisation — which is exactly what P2N does before its per-image optimisation. **The knowledge lives in the tensors.**

The migration is datable from the repositories themselves: MATLAB/MatConvNet in 2017, TensorFlow for Noise2Noise in 2018, PyTorch from 2019 onward; hard-coded scripts → `argparse` → a JSON options file → **YAML resolved by a BasicSR registry**.

**The consequence that is easy to miss.** Because the weights are a file and the architecture is a string in a YAML, a modern denoiser is **two decoupled artefacts**. You can ship a better checkpoint without touching the code, and swap the architecture without retraining the pipeline — swapping Restormer for NAFNet is a one-line YAML edit. The classical era had no such separation, and that is a large part of why it could not compound.""",
"""The classical era shipped a recipe. The modern era ships the cake and the recipe separately, so either can be improved without the other.""",
["state_dict", "strict loading", "BasicSR registry", "model cards", "decoupled artefacts"],
[("What happens if `strict=True` and the shapes mismatch?",
  "It raises immediately, listing missing and unexpected keys. That is desirable — silent partial loading would give a model that runs and produces quietly wrong output, which is far harder to debug than a crash."),
 ("What does the registry pattern change conceptually?",
  "It makes architectures interchangeable components named by strings. That is a strong statement about maturity: the architecture has become configuration rather than code."),
 ("Between 2017 and 2022, what changed about reproducibility?",
  "The unit of reproducibility moved from *a script you edit* to *a config you version-control*. That is why modern papers can honestly claim exact reproduction in a way 2017 papers could not.")],
[],
hard=False))

A(Q("padding", "C", "Stage 3 → Part VI → Deployment details",
"What did reading the code tell you that the papers did not?",
r"""Four things, none of which appears in any abstract.

**1. Every model pads, and they all pad differently.** A U-Net that downsamples \(k\) times needs input dimensions divisible by \(2^k\), and each repository solves it with the same pad-then-crop idiom and a different constant:

| Model | Required multiple | Padding mode |
|---|---|---|
| Restormer | 8 | `reflect` |
| NAFNet | 16 (`2 ** len(self.encoders)`) | zero (default `F.pad`) |
| P2N+ | 32 | `reflect` |
| SCUNet | 64 (`int(np.ceil(h/64)*64-h)`) | `nn.ReplicationPad2d` |

A factor of eight separates the extremes, and the *modes* differ too — zero padding injects a hard artificial edge, reflection and replication do not. Feed a \(1000\times1000\) image to SCUNet and 24 rows and columns of replicated content are silently invented, processed, and cropped away. This becomes a real problem the moment two models are chained in one pipeline.

**2. SPI costs latency, not parameters.** Turning on Symmetric Prior Injection *reduces* P2N+'s parameters by 6.7% yet raises CPU latency 2.5×, because every layer is evaluated twice, on \(x\) and on \(-x\). Exactly the opposite of what a parameter table predicts.

**3. MambaIR cannot be imported without compiled CUDA extensions.** That is not a gap in the experiment — it *is* the result, and it describes a deployment profile fundamentally different from the others.

**4. MambaIR's own changelog records that published `thop` complexity figures were wrong** and were later corrected.""",
"""Papers report what the model achieves. Code reports what it requires. The gap between those two is where deployment lives.""",
["padding constants", "reflect vs zero padding", "hidden preprocessing", "dependency constraints", "reported vs actual complexity"],
[("Why does padding mode matter for denoising specifically?",
  "Because the network is being asked to distinguish structure from noise. Zero padding creates a hard artificial edge at the boundary, which looks like structure and can produce visible border artefacts. Reflection and replication extend the image plausibly instead."),
 ("Did DnCNN have this problem?",
  "No, and that is a point in its favour. It uses zero padding throughout with no downsampling, so every feature map stays the same size as the input, and the paper reports the strategy produces **no boundary artefacts**. The problem arrives with U-Net-style downsampling."),
 ("How would you handle this in a real pipeline?",
  "Normalise it: wrap each model in an adapter that pads to its own required multiple with a consistent mode and crops afterwards, so the pipeline's behaviour does not depend on which model is in the slot.")],
[],
hard=False))

# ═══════════════ 7. RESULTS ═══════════════
A(Q("bench-table", "D", "Stage 3 → Part VI → Measured benchmark",
"Explain your benchmark table: what it shows, how it was produced, and what it does not show.",
r"""**Method.** Each model was instantiated from its own repository at a pinned commit, in the configuration that repository uses for denoising. Parameters are `sum(p.numel() for p in model.parameters())`. Latency is the mean of three forward passes at \(256\times256\) after one warm-up, under `torch.no_grad()`, **CPU only**, PyTorch 2.13.0, no CUDA.

| Model | Parameters | CPU latency, \(256^2\) |
|---|---|---|
| DnCNN-B | 0.668 M | 1.015 s |
| P2N+ backbone, SPI off | 0.991 M | 0.286 s |
| P2N+ backbone, SPI on | 0.925 M | 0.710 s |
| SCUNet | 9.663 M | 1.685 s |
| Restormer | 26.127 M | 10.436 s |
| NAFNet | 115.983 M | 1.899 s |
| MambaIR | *not measurable* | import fails |

**What it shows — four readings.** (a) **Parameters do not predict latency**: NAFNet has 4.4× Restormer's parameters and runs 5.5× faster, because it is \(1\times1\) and depth-wise convolutions on fast GEMM paths while Restormer's `rearrange` calls force layout changes. (b) **SPI costs latency, not parameters.** (c) **Depth at full resolution is expensive**: DnCNN is the smallest model and still slower than the larger P2N+ backbone, because it runs 20 sequential full-resolution \(3\times3\) convolutions at 64 channels while a U-Net does most of its work at reduced resolution. (d) **Some models simply do not run.**

**What it does not show, stated before being asked.** The forward passes used **random tensors**, so **no PSNR or SSIM was measured here** — every quality figure in the project comes from a published table. And absolute CPU latencies are **not comparable** to published GPU timings; only the ratios between rows are informative, and only for this backend.""",
"""The table answers "what does this cost to run?", not "how good is it?". Keeping those two questions in separate tables is the whole of the honesty policy.""",
["parameter counting", "wall-clock measurement", "warm-up passes", "random-tensor caveat", "CPU vs GPU comparability"],
[("Why three runs and a warm-up?",
  "The first pass includes lazy allocation, kernel selection and cache population, so it is systematically slower and unrepresentative. Three runs afterwards give a mean that is stable enough for ratio comparisons without pretending to be a rigorous statistical estimate — and I would report the spread if asked for more rigour."),
 ("Why not measure PSNR yourself?",
  "Doing it correctly would mean matching each paper's crop, border, colour-space and rounding conventions. A table mixing our numbers with theirs would be worse than useless, so we kept measurement and citation strictly separated."),
 ("How would the ranking change on a GPU?",
  "Probably substantially. Attention matmuls are well served by GPU tensor cores, so Restormer's disadvantage would shrink. That is precisely why the claim is stated as a ratio on a named backend rather than as a general efficiency ordering.")],
[("A model with more parameters is slower.",
  "Latency depends on arithmetic intensity and memory layout, not parameter count.",
  "NAFNet is the counterexample in our own data: 4.4× the parameters and 5.5× faster. Any claim that model X is 'more efficient' is meaningless without naming the metric — parameters, MACs, or wall-clock — and the device.")],
hard=True))

A(Q("bsd68-ladder", "D", "Stage 3 → Part VII → BSD68",
"Read the BSD68 table across eighteen years. What is the honest conclusion?",
r"""Average PSNR at \(\sigma = 25\), with each row's source named:

| Method | Year | \(\sigma{=}15\) | \(\sigma{=}25\) | \(\sigma{=}50\) | Source |
|---|---|---|---|---|---|
| BM3D | 2007 | 31.07 | 28.57 | 25.62 | DnCNN T2 |
| WNNM | 2014 | 31.37 | 28.83 | 25.87 | DnCNN T2 |
| TNRD | 2016 | 31.42 | 28.92 | 25.97 | DnCNN T2 |
| **DnCNN-S** | 2017 | **31.73** | **29.23** | **26.23** | DnCNN T2 |
| DRUNet | 2021 | 31.91 | 29.48 | 26.59 | Restormer T4 |
| SwinIR | 2021 | 31.97 | 29.50 | 26.58 | Restormer T4 |
| **Restormer** | 2022 | **31.96** | **29.52** | **26.62** | Restormer T4 |

Read the \(\sigma=25\) column as three eras:

- 2007 → 2014, seven years of hand-designed priors: **+0.26 dB**
- 2014 → 2017, one architectural idea: **+0.40 dB**
- 2017 → 2022, five years and an entire Transformer revolution: **+0.36 dB**

**The honest conclusion is that BSD68 has saturated**, and has been saturating since roughly 2018. A benchmark that cannot distinguish 2017 from 2022 is no longer measuring what the field is working on.

That is why the project does not stop here. The same five years and the same two models give **+1.98 dB on Urban100**, and **+16.36 dB on SIDD real noise**. Progress did not stop; the question changed.

Note also the methodological point: DnCNN appears twice with slightly different numbers (31.73 from its own paper, 31.62 re-evaluated in Restormer's Table 4). That is why rows compare methods **from a single table** wherever possible — otherwise you are silently comparing two evaluation scripts.""",
"""Everyone kept running the same race faster and faster until the stopwatch stopped being able to tell them apart. The interesting results moved to a different race.""",
["benchmark saturation", "cross-paper comparability", "per-dataset reading", "evaluation protocol differences"],
[("Why does BSD68 saturate?",
  "It contains relatively little long-range repetition, so it measures a capability the field largely solved by 2018 while being blind to the one it moved on to. It is also close to whatever noise-level-specific ceiling exists for these 68 images."),
 ("Is the comparison across two source tables legitimate?",
  "Only with the caveat shown. The top block is internally consistent and the bottom block is internally consistent; the DnCNN row appears in both precisely so the reader can see the size of the protocol difference — about 0.1 dB."),
 ("What would a better benchmark look like?",
  "One that separates the capabilities being claimed: long-range self-similarity (Urban100 does this), real sensor noise (SIDD and DND), and generalisation to an unseen camera and ISP — which, as far as we found, nothing currently measures.")],
[],
hard=True))

A(Q("sidd", "D", "Stage 3 → Part VII → Real noise",
"Interpret the SIDD result. Why does DnCNN score 23.66 dB?",
r"""From Restormer's Table 6, all evaluated under one protocol:

| Method | SIDD PSNR | SIDD SSIM | DND PSNR |
|---|---|---|---|
| **DnCNN** (AWGN-trained, 2017) | **23.66** | 0.583 | 32.43 |
| BM3D (classical, 2007) | 25.65 | 0.685 | 34.51 |
| **Restormer** (2022) | **40.02** | **0.960** | 40.03 |
| NAFNet (2022) | **40.30** | — | — |

**What it shows.** DnCNN — which beats BM3D by 0.6 dB on synthetic Gaussian noise — is beaten by BM3D by **1.99 dB** on real sensor noise, and trails Restormer by **16.36 dB**.

**Why it happens.** DnCNN was trained on a noise distribution that does not occur in the test data. Real sensor noise is read noise plus shot noise in the raw domain, then transformed by demosaicing, white balance, colour-space conversion, tone mapping and gamma — each of which correlates it spatially and across channels and makes its variance signal-dependent. Every one of the four words in "additive white Gaussian noise" is violated. The network has learned a mapping from one distribution and is being evaluated on another.

**Is it expected?** Yes, qualitatively — a discriminative model trained on the wrong distribution should degrade. What is *not* obvious in advance is the magnitude: it does not degrade gracefully, it **collapses by sixteen decibels** and falls below a seventeen-year-old algorithm. BM3D survives better precisely because it makes no learned commitment to a training distribution; it only assumes local self-similarity, which remains true.

**Why BM3D still loses to Restormer by 14 dB.** Because BM3D's own noise model is also Gaussian; it is simply less overfitted to it. Restormer and NAFNet were trained on SIDD's 320 captured noisy/clean scene pairs — real data, no noise model at all.

**Limitations.** Neither approach generalises to an unseen camera with an unseen ISP, and no benchmark currently measures that. SCUNet's answer is to synthesise realistic degradations instead; its abstract still concedes that a general-purpose blind real denoiser *remains unsolved*.""",
"""Train a model to remove one kind of grain and show it a different kind, and it does not partially succeed — it fails, because it is confidently subtracting the wrong thing.""",
["distribution shift", "signal-dependent noise", "ISP pipeline", "noise assumption mismatch", "graceful degradation"],
[("Could DnCNN be fixed by retraining on SIDD?",
  "Largely, yes — the architecture is not the limiting factor here, the training distribution is. That is exactly SCUNet's argument, and it is why its contribution is a *noise synthesis model* rather than a new block."),
 ("Why is SSIM 0.583 so much worse proportionally than the PSNR?",
  "Because SSIM's structure term is a local correlation, and a denoiser removing the wrong signal destroys local structure rather than just shifting pixel values. The two metrics agree here that the failure is structural, not a small offset."),
 ("Which single slide would you lead with in a short presentation?",
  "This one. 23.66 against 40.02 makes the whole evolutionary argument land in one breath, and it is more informative than any BSD68 table.")],
[("DnCNN is a bad model.",
  "It is an excellent model for the problem it was trained on, where it captured ~85% of the available headroom over BM3D.",
  "The failure is a distribution mismatch, not a capability deficit. Stating it that way is both more accurate and more useful.")],
hard=True))

A(Q("urban100", "D", "Stage 3 → Part VII → Urban100",
"You claim Urban100 is the key evidence for bottleneck 3. Show the reasoning.",
r"""Three measurements of the same phenomenon, eight years apart:

| Measurement | Value | Source |
|---|---|---|
| Barbara, \(\sigma{=}25\), DnCNN-S vs BM3D | **−0.71 dB** | DnCNN Table III |
| BSD68 \(\sigma{=}50\), DnCNN → Restormer | **+0.39 dB** | Restormer Table 4 |
| Urban100 \(\sigma{=}50\), DnCNN → Restormer | **+1.98 dB** | Restormer Table 4 |

**The reasoning.** The second and third rows use identical models, the identical table and the identical noise level. The only thing that changes is the dataset — from ordinary natural images to 100 photographs of buildings, where windows, balconies and railings repeat identically across the whole frame. **The gain is five times larger on the dataset made of repetition.**

That ratio is the cleanest single measurement of bottleneck 3 in the literature, and it is computed from one table. A convolutional network with a \(35\times35\) receptive field cannot exploit self-similarity beyond 35 pixels; non-local classical methods could; attention gave it back.

The first row is the same fact visible five years earlier, in DnCNN's own results. The paper's explanation: DnCNN fails on exactly the two Set12 images *dominated by repetitive structures*, because those images *meet well with the non-local similarity prior*, whereas discriminative training does better on irregular textures.

**The corollary is the useful claim.** The architecture branch did not make denoising uniformly better. It made denoising better **specifically where non-locality matters** — which is exactly what it set out to do. Aggregate benchmark numbers conceal this completely.

**Provenance caveat:** the 1.98-versus-0.39 comparison is our own analysis of published values, not a claim either paper makes. Say "computed from Table 4" if challenged.""",
"""Barbara's scarf was a warning in 2017. Urban100 is a hundred images of that scarf, and it is where the last five years of architecture work actually shows up.""",
["receptive field limits", "long-range self-similarity", "per-dataset analysis", "own-analysis provenance"],
[("Why does Urban100 have such strong self-similarity?",
  "Architecture is modular by construction. A façade is the same window repeated dozens of times at regular intervals, often across hundreds of pixels — which is the ideal case for a non-local prior and the worst case for a small receptive field."),
 ("Could you test this hypothesis more directly?",
  "Yes — measure a self-similarity statistic per image (for example, the average distance to the best-matching non-local patch) and correlate it with the per-image gain from DnCNN to Restormer. We did not run that experiment, and it would be a reasonable thing to propose."),
 ("Does this mean Restormer is worse on non-repetitive images?",
  "No. It is still better, by 0.39 dB. The point is that most of its advantage is concentrated where non-locality helps, not that it trades one for the other.")],
[],
hard=True))

# ═══════════════ 8. ASSIGNMENT / META ═══════════════
A(Q("narrative", "A", "Stage 3 → Assignment → §3 structure",
"The brief warns the deck must not read like ten disconnected paper summaries. How does yours avoid that?",
r"""By committing to a single claim before any evidence appears, and treating every paper as evidence for it:

> Image denoising is the cleanest available case study in how computer vision replaced hand-designed priors with learned ones. Its history divides into **four eras separated by three bottlenecks** — manual prior design, the clean-data requirement, and the receptive-field limits of convolution. In 2018 the response **forked** into two branches that have never merged.

Three structural devices enforce it:

1. **Each bottleneck is named by the paper that broke it.** DnCNN's introduction supplies the four drawbacks of the classical era in its own words. The receptive-field limit is visible in DnCNN's own Table III. So the arc is evidenced from primary sources rather than imposed retrospectively.
2. **The fork is structural, not decorative.** The brief's §4 is split into two parts because Noise2Noise/Noise2Void/ZS-N2N/P2N changed *what the network is shown*, while Restormer/NAFNet/SCUNet/MambaIR changed *what the network is*. Collapsing them into one chapter would misrepresent what happened.
3. **One organising question runs through the engineering section:** open the file, where is the prior? That converts Part VI from a tour of repositories into a continuation of the same argument.

The deck is also indexed against the brief's own seven-section structure on slide 4, so the mapping is explicit rather than implied.""",
"""A summary lists what each paper did. A synthesis explains why each paper had to exist. The difference is whether removing one paper would break the argument.""",
["evolutionary narrative", "bottleneck framing", "the 2018 fork", "structural mapping to the brief"],
[("Why end without naming a winner?",
  "Because that would be false. Restormer leads Urban100, NAFNet leads SIDD, MambaIR leads DND by 0.01 dB, and SCUNet answers the same problem from the data side entirely. Three architectural answers and one data answer, none of which has displaced the others — that is what an unresolved question looks like from the inside."),
 ("What is the weakest point in the narrative?",
  "That the two branches are presented as independent, which is an observation rather than a proven claim. Nobody has published a state-space or Transformer backbone trained under RDC/DCS supervision as far as we found — so whether they compose or conflict is genuinely untested, and I present it as an open question rather than a finding."),
 ("How would you defend the choice of anchor paper?",
  "DnCNN sits exactly at the hinge. It closes bottleneck 1 completely and creates both bottleneck 2 and the visible evidence for bottleneck 3 in its own results table. No other paper in the roster is simultaneously the resolution of one era and the cause of the next two.")],
[],
hard=False))

A(Q("sources", "A", "Stage 3 → Assignment → §2 source rules",
"Defend your source selection against the brief's quota and quality rules.",
r"""**The arithmetic.** 15 sources total: 12 Category A peer-reviewed (**80.0%**, against a 70% floor) and 3 Category B auxiliary (**20.0%**, against a 30% ceiling). Compliant with margin on both sides.

**Category A** spans 2007–2025 and is chosen to instantiate the narrative rather than to fill a quota: BM3D and WNNM for the classical peak; TNRD for the unrolling bridge; DnCNN as the anchor; Noise2Noise, Noise2Void, ZS-N2N and P2N for the data branch; Restormer, NAFNet, SCUNet and MambaIR for the architecture branch. Removing any one of them breaks a link in the argument.

**Category B** is justified by role, not by availability:
- **CS231n** supplies the backpropagation and convolution-arithmetic background every paper from DnCNN onward assumes without stating.
- **Google Research's Night Sight / HDR+ writing** is the only source describing denoising as a *shipped consumer product*, and it supplies the physical grounding — photon shot noise versus read noise, SNR rising with the square root of exposure time — for the real-noise argument.
- **Gonzalez & Woods**, Image Restoration chapter, supplies the formal treatment of noise models and of mean, order-statistic and adaptive filters. It is also the reference against which SCUNet's pipeline reads critically: SCUNet's noise list is essentially the textbook's noise list, industrialised.

**The flag I raise myself.** SCUNet appeared in *Machine Intelligence Research* 20(6), 2023 — a peer-reviewed Springer journal, but not among the venues the brief names. I read that list as illustrative, since it is introduced with "e.g.". If strict adherence were required, moving SCUNet to Category B still leaves 11 of 15 in Category A, or 73.3%, above the floor. I would rather raise that arithmetic than have it raised for me.""",
"""A bibliography that satisfies a quota is a list. A bibliography where each entry has a job is an argument.""",
["source quotas", "Category A vs B", "role-based justification", "self-flagged edge cases"],
[("Why are the citation counts included?",
  "Because they corroborate the narrative rather than decorate it. BM3D and DnCNN both sit near twelve thousand citations, which is precisely why both remain universal baselines nineteen and nine years later. Conversely ZS-N2N at 266 and SCUNet at 391 are low because they are *recent*, not weak — recency and citation count are confounded, and saying so pre-empts the obvious challenge."),
 ("Why is one citation count marked 'not verified'?",
  "P2N's count was not confirmed at the time of checking, and the project's rule is that unverified figures are omitted rather than estimated. All other counts are Google Scholar figures checked on 9 August 2026, with the date quoted alongside."),
 ("What other provenance problems did you find?",
  "Reference code availability is uneven: ZS-N2N has no repository, only a Colab notebook; WNNM has only a third-party mirror with no README or licence; TNRD's available implementation is a same-laboratory re-implementation; and the P2N paper's printed repository URL returns HTTP 404, with the live code at `P2N-plus`.")],
[],
hard=False))

A(Q("limitations", "A", "Stage 3 → Assignment → Honesty",
"What are the weaknesses of your own work?",
r"""Stated here rather than discovered under questioning:

1. **No quality metric was computed by us.** Every PSNR and SSIM is reproduced from a published table with the paper and table named. Our measurements cover parameter counts and CPU latency only, and used random tensors, so they carry no image-quality information.
2. **CPU latencies are not comparable to published GPU timings.** Only ratios between our own measurements are meaningful, and only for the backend used.
3. **The DnCNN runtime table mixes devices** — CPU for classical methods, GPU for learned ones — and the paper itself states the CSF and TNRD GPU times were copied from their original papers. We reproduce the caveat wherever we reproduce the numbers.
4. **One published value is excluded.** MambaIR's CBSD68 \(\sigma{=}25\) cell extracted as 32.24, inconsistent with its own row (34.48 at \(\sigma{=}15\), 28.66 at \(\sigma{=}50\)) and with every comparable method. We judged it a probable extraction error and excluded it rather than reproduce it; MambaIR's colour results are quoted from Urban100 instead.
5. **TNRD's year is genuinely ambiguous** — the PDF header reads 2016, the citing literature gives TPAMI 39(6), 2017. Both reflect reality, acceptance versus issue. We cite 2017.
6. **Venue verification is uneven.** Four venues are printed in the source PDFs; the other eight are preprints carrying no venue and were confirmed against publisher or CVF records rather than copied from another paper's reference list.
7. **The two-branch independence claim is an observation, not a proven result.**
8. **Citation counts move** and should be re-checked before the defence.""",
"""A gap you declare is a smaller problem than a gap someone finds. Declaring them also signals that you read the primary material rather than aggregating it.""",
["declared limitations", "measurement scope", "excluded data", "provenance verification"],
[("Why exclude the MambaIR cell rather than footnote it?",
  "Because a footnoted number still ends up quoted. If I cannot verify it and it contradicts its own row, reporting it would violate the project's own rule that unverifiable figures are omitted rather than estimated."),
 ("Is not measuring PSNR yourself a serious weakness?",
  "It is a real scope limitation, and I would say so plainly. It would have required matching each paper's crop, border, colour-space and rounding conventions to be meaningful. Given the time available, a rigorous citation policy was the better use of effort than a half-correct reproduction."),
 ("What would you do differently with more time?",
  "Run a proper PSNR reproduction on BSD68 for two or three models under one protocol, and run the benchmark on a GPU so the efficiency ratios reflect the deployment target rather than a CPU backend.")],
[],
hard=False))

A(Q("deploy", "A", "Stage 3 → Part VIII → Deployment",
"Which model would you deploy?",
r"""Name the constraint first — that is the honest answer, and the fork in the timeline predicts which:

| Constraint | Choice | Evidence |
|---|---|---|
| GPU, paired data, real photographs | **NAFNet** | 40.30 dB SIDD; best accuracy-per-ms measured; simplest code |
| CPU- or memory-bound | **SCUNet** | 9.663 M parameters; synthetic-degradation training |
| Maximum quality on repetitive structure | **Restormer** (MambaIR if CUDA guaranteed) | Leads Urban100; only method past 40 dB on both SIDD and DND |
| No clean data at all | **P2N**, or **ZS-N2N** for one image | Accepts per-image test-time optimisation as the price |
| Dependency-free baseline | **BM3D** | No data, no GPU; still beats AWGN-trained DnCNN on real noise by 1.99 dB |

Notice what the list does not contain: a winner. Five constraints, five different answers, all current. That is not indecision — it is what an unresolved research question looks like when you have to ship something on Monday.""",
"""The question "which is best?" has no answer. The question "best under which constraint?" has five, and knowing all five is the actual competence being tested.""",
["constraint-driven selection", "accuracy per millisecond", "dependency risk", "zero-shot fallback"],
[("What if I force you to pick one?",
  "NAFNet, for real photographs with a GPU and paired data — highest measured quality on SIDD, best accuracy per millisecond in our own measurements, and by a wide margin the simplest code to maintain. But I would want to say what I am giving up: 116 M parameters, and no answer at all when clean data does not exist."),
 ("Why is BM3D still on the list in 2026?",
  "Because it needs no training data and no GPU, it appears as a live baseline in papers as recent as 2023, and on real sensor noise it beats an AWGN-trained DnCNN by 1.99 dB. For a zero-shot, dependency-free fallback nothing has displaced it."),
 ("What would change your answer in two years?",
  "A model that generalises to an unseen camera and ISP without retraining. That is the open problem SCUNet names, and solving it would collapse most of this table into a single recommendation.")],
[],
hard=False))
