# Stage 3 — From Foundations to State-of-the-Art

**Topic:** Image denoising
**Anchor paper:** Zhang, Zuo, Chen, Meng & Zhang, *Beyond a Gaussian Denoiser: Residual Learning of Deep CNN for Image Denoising*, IEEE Transactions on Image Processing 26(7), 2017
**Course:** Digital Image Processing · **Supervisor:** Prof. Zohreh Azimifar
**Checkpoint:** TA Presentation 3 — Final Project Defence, 31 August 2026

---

## 0. What is in this submission

| File | What it is |
|---|---|
| `1-deliverable/Stage3_Master_Deck.pptx` | **The graded deliverable.** 100 slides, editable PowerPoint. |
| `1-deliverable/Stage3_Master_Deck.pdf` | The same deck as PDF, for submission and printing. |
| `1-deliverable/Stage3_Report.md` | This document. |
| `2-presentation/master-deck.html` | Interactive version of the same 100 slides — keyboard navigation, a contents panel, and a toggle that reveals the speaker notes attached to every slide. |
| `2-presentation/defence.html` | Bilingual English/Persian presenter companion: the condensed spoken script for the 30-minute slot, and a bank of 19 anticipated technical questions with full answers. |
| `2-presentation/companion.html` | Presenter companion scripted for all 100 slides of the master deck. |
| `2-presentation/Presentation_30min.pptx` / `.pdf` / `.html` | The 30-minute condensed talk, 32 slides, two presenters. |
| `2-presentation/presenter-30min.html` | Run sheet for the 30-minute talk — timing, handovers, bilingual block guidance. |
| `3-study/oral-exam.html` | Oral-exam study site — question bank, exam simulator, search. |
| `4-evidence/bench/` | The benchmark script and its raw output. |
| `5-source/` | The generator scripts and the two structured decks (`deck.json`, `presentation.json`) everything above is built from. |

The deck and this report contain the same claims. The deck is organised for delivery; this document is organised for reading, and states the reasoning at greater length in the places where a slide can only state a conclusion.

---

## 1. The organising claim

The brief warns that the final deck *cannot read like 10 disconnected paper summaries* and must *tell the complete evolutionary story of your domain*. Accordingly this work is built around a single claim, and everything in it is evidence for that claim:

> Image denoising is the cleanest available case study in how computer vision replaced hand-designed priors with learned ones. Its history divides into four eras separated by three identifiable bottlenecks — *manual prior design*, *the clean-data requirement*, and *the receptive-field limits of convolution*. Each bottleneck was named by the paper that broke it, so the arc can be evidenced from the primary sources rather than imposed retrospectively. In 2018 the response forked into two branches that have never merged. Because the field currently holds three competing answers to the third bottleneck, the story ends in a genuine open question rather than a winner.

Denoising is unusually well suited to this argument because the prior is written down explicitly in the classical formulation, which means one can point at it and watch it move. The organising question asked of every method in this work — and, in Part VI, of every repository — is therefore:

> **Where is the prior, and who wrote it?**

### 1.1 Mapping onto the brief's required structure

| Brief §3 | Part of this work | Slides |
|---|---|---|
| 1. Introduction & Problem Definition | I — The problem | 06–16 |
| 2. The Classical DIP Foundation | II — Classical DIP | 17–29 |
| 3. The Deep Learning Transition | III — The transition | 30–44 |
| 4. The Modern State-of-the-Art | IV — Data branch · V — Architecture branch | 45–65 |
| 5. Practical Deep-Dive | VI — Engineering reality | 66–80 |
| 6. Comparative Analysis | VII — Comparative analysis | 81–88 |
| 7. Future Directions & Conclusion | VIII — Open problems | 89–93 |

Section 4 is split because the field genuinely forked. Collapsing Noise2Noise, Noise2Void, ZS-N2N and P2N into the same chapter as Restormer, NAFNet, SCUNet and MambaIR would misrepresent what happened: one group changed *what the network is shown*, the other changed *what the network is*, and the two lines of work are largely independent of each other to this day.

---

## 2. Evidence standards

Cross-paper comparison in low-level vision is easy to do badly. The constraints below were imposed on this work and are stated on slide 81 of the deck.

1. **No quality metric in this work was computed by us.** Every PSNR and SSIM figure is reproduced from a published table, with the paper and table named at the point of use.
2. **Rows come from a single table wherever possible.** Where DnCNN is compared with Restormer, both figures are taken from Restormer's Table 4, in which the authors evaluated both under one protocol. Taking each number from its own paper would silently compare two different evaluation scripts, with different crop, border, colour-space and rounding conventions.
3. **Timings and quality are never mixed in one column.** Quality comes from papers; latency and parameter counts come from our own measurements on stated hardware, reported separately and labelled `[measured]`.
4. **Device asymmetries are stated wherever the numbers are.** The DnCNN runtime table compares CPU figures for classical methods against GPU figures for learned ones, and the paper itself notes that the CSF and TNRD GPU times were copied from their original papers.
5. **Unverifiable figures are omitted, not estimated.** One published cell was excluded on these grounds; see §9.2.

---

## 3. Part I — The problem

### 3.1 The degradation model

The field rests on one equation, stated identically across sixteen years:

$$y = x + v$$

where $y$ is the noisy observation, $x$ the latent clean image, and $v$ the noise. DnCNN writes it this way in 2017; SCUNet writes $y = x + n$ in 2023. Noise2Void reformulates it as a joint distribution, $p(s,n) = p(s)\,p(n\mid s)$, which is what makes its assumptions visible enough to exploit.

The standard assumption is that $v$ is additive white Gaussian noise with standard deviation $\sigma$. Each of the four words is load-bearing and each is false of a real camera:

- **Additive** — the clean image is recoverable by subtraction, which is exactly what makes residual learning possible.
- **White** — spatially independent; this is what Noise2Void's blind spot depends on, and the first property that resizing destroys.
- **Gaussian** — zero-mean; this is the whole of the Noise2Noise argument, and it is why residual learning and batch normalisation suit each other.
- **$\sigma$** — benchmarks use $\sigma \in \{15, 25, 50\}$ on 8-bit images; DnCNN-B trains blind over $[0, 55]$.

### 3.2 Ill-posedness and the birth of the prior

Given $y$, infinitely many decompositions into $x + v$ are arithmetically valid. The algorithm must therefore add information that is not present in the measurement. That added information is the **prior**, and there is no prior-free denoiser — a method that appears not to have one has merely hidden it in an architecture, a training set, or a stopping criterion.

The classical era makes the choice explicit through maximum a posteriori estimation. From Bayes' rule,

$$\hat{x} = \arg\max_x p(x \mid y) = \arg\max_x p(y \mid x)\, p(x),$$

and taking negative logarithms turns the product into a sum:

$$\hat{x} = \arg\min_x \Big[ -\log p(y\mid x) - \log p(x) \Big]
= \arg\min_x \tfrac{1}{2}\lVert y - x \rVert_2^2 + \lambda\,\Phi(x).$$

The first term is *forced* by the Gaussian likelihood: $-\log \exp\!\big(-\lVert y-x\rVert^2 / 2\sigma^2\big) = \lVert y-x\rVert^2/2\sigma^2$, with the $1/\sigma^2$ absorbed into $\lambda$. The second term, $\Phi$, is entirely a modelling choice, and the classical era is the history of guesses at it: total variation sets $\Phi(x) = \lVert \nabla x \rVert_1$; sparse coding sets $\Phi(x) = \lVert \alpha \rVert_0$ subject to $x = D\alpha$; WNNM sets $\Phi$ to a weighted nuclear norm on stacks of similar patches.

### 3.3 Metrics

$$\mathrm{PSNR} = 10\log_{10}\!\left(\frac{\mathrm{MAX}^2}{\mathrm{MSE}}\right)\ \mathrm{dB},
\qquad
\mathrm{MSE} = \frac{1}{MN}\sum_{i}\sum_{j}\big[x(i,j)-\hat{x}(i,j)\big]^2 .$$

The logarithm compresses everything: halving the MSE gains exactly $3.01$ dB, so DnCNN's headline $0.6$ dB over BM3D corresponds to roughly a 13% MSE reduction. The calibration that makes that number meaningful is supplied by the DnCNN paper itself — prior work found that *few methods can outperform BM3D by more than 0.3 dB on average*, and the estimated PSNR bound over BM3D is about $0.7$ dB.

SSIM decomposes similarity into luminance, contrast and structure and multiplies them:

$$\mathrm{SSIM}(x,\hat{x}) = \frac{(2\mu_x\mu_{\hat{x}} + C_1)(2\sigma_{x\hat{x}} + C_2)}{(\mu_x^2+\mu_{\hat{x}}^2+C_1)(\sigma_x^2+\sigma_{\hat{x}}^2+C_2)} .$$

The structure term is a local correlation coefficient, so blur — which raises PSNR on a noisy image by lowering MSE — lowers SSIM. Reporting both is the honest minimum.

**On IoU.** The brief lists PSNR, SSIM and IoU as example comparison metrics because it is written generically across many topics. Intersection-over-Union measures region overlap and is undefined for a dense-regression task with continuous-valued output. This work reports PSNR and SSIM and states the reason rather than forcing a meaningless number.

---

## 4. Part II — The classical foundation, and bottleneck 1

### 4.1 The through-line

Every classical method answers one question: *which pixels count as observations of the same quantity?* Averaging $n$ independent observations of a quantity divides the noise standard deviation by $\sqrt{n}$, but only if those observations share the same clean value — which is false across an edge. The resulting bias is proportional to local contrast, and this is the bias–variance trade-off in its most visible form: grain traded against softness.

Gaussian filtering weights by distance; bilateral filtering by distance and intensity; and in 2005 non-local means abandons locality entirely, weighting by patch similarity:

$$\hat{x}(i) = \sum_j w(i,j)\, y(j), \qquad w(i,j) \propto \exp\!\left(-\frac{\lVert P_i - P_j\rVert_{2,a}^2}{h^2}\right).$$

**Non-local self-similarity** is the strongest hand-designed prior ever found for natural images. It powers BM3D and WNNM; it is the specific prior DnCNN lacks; and it is the reason Restormer's gain on Urban100 is five times its gain on BSD68.

### 4.2 BM3D

BM3D combines non-local grouping with transform-domain shrinkage and runs the combination twice: group by block matching, collaboratively hard-threshold in a separable 3-D transform, aggregate by weighted averaging; then re-group *inside the cleaner basic estimate* and Wiener-filter the noisy group using the basic estimate's energy spectrum as the pilot. The paper gives two explicit motivations for the second step — the basic estimate improves the grouping, and it is a far better Wiener pilot than hard-thresholding the noisy spectrum.

The most instructive result is the transform ablation: varying the 2-D and 1-D transforms changes PSNR only modestly, and even a transform whose basis elements are random apart from the DC loses only 0.1–0.4 dB. The authors conclude that *inter-fragment correlation appears as a much more important feature than intra-fragment correlation*. **The grouping is doing the work, not the transform.**

### 4.3 WNNM, and the classical ceiling

Stacking similar patches into a matrix $Y_j = X_j + N_j$ makes $X_j$ low rank, so low-rank recovery applies. Standard nuclear-norm minimisation soft-thresholds every singular value by the same $\lambda$, which the paper objects to on physical grounds: in denoising the larger singular values carry the major image components and should be shrunk *less*. Hence the weighted nuclear norm $\lVert X\rVert_{w,*} = \sum_i w_i \sigma_i(X)$ with

$$w_i = \frac{c\sqrt{n}}{\sigma_i(X_j) + \varepsilon}, \qquad \varepsilon = 10^{-16},$$

and, since $\sigma_i(X_j)$ is unknown, the estimate $\hat{\sigma}_i(X_j) = \sqrt{\max(\sigma_i^2(Y_j) - n\sigma_n^2,\, 0)}$ obtained by assuming the noise energy is evenly distributed across subspaces.

Theorem 2 of that paper establishes that for weights in *non-ascending* order the problem has a globally optimal closed-form solution by generalised soft-thresholding, recovering the classical singular value thresholding result as the special case of equal weights. The denoising weights are non-descending, which is the opposite ordering, so the authors prove separately that an iterative algorithm reaches an analytical fixed point in that regime.

WNNM beats BM3D at every noise level on BSD68 — and takes **773.2 seconds** for one $512\times512$ image against BM3D's 2.85 s.

### 4.4 Bottleneck 1

Stated in the words of the paper that broke it. Prior-based methods *involve a complex optimization problem in the testing stage*, making denoising time-consuming, and the models are *generally non-convex and involve several manually chosen parameters*. The bridge methods that removed the test-time iteration are *inherently restricted to the specified forms of prior*, and they *train a specific model for a certain noise level*, so they are *limited in blind image denoising*.

> **Bottleneck 1: the prior is written by hand, and paid for once per image.**

Nine years of hand-designed priors moved BSD68 at $\sigma=25$ from 28.57 to 28.83 dB — 0.26 dB — while the best method became 271× slower than the second best. The era had hit a wall in quality and cost simultaneously.

---

## 5. Part III — The transition, and bottleneck 2

### 5.1 Unrolling

The conceptual bridge is unrolling: take an iterative optimiser, truncate it to a fixed number of stages, give each stage its own parameters, and train the whole stack end-to-end against a loss measured on the final output. TNRD is the clearest example — simultaneously a nonlinear reaction–diffusion PDE and a convolutional network:

$$\frac{u_t - u_{t-1}}{\Delta t} = -\sum_{i=1}^{N_k} \big(K_i^{t}\big)^{\!\top} \phi_i^{t}\big(K_i^{t} u_{t-1}\big) \;-\; \psi^{t}(u_{t-1}, f),$$

with $\Delta t = 1$ in practice, $K_i$ implemented as 2-D convolution with kernel $k_i$, and the reaction term $\psi^t(u) = \nabla_u D_t(u,f) = \lambda^t A^{\!\top}(Au - f)$, where $A = I$ for denoising and different choices of $A$ give super-resolution and inpainting. What distinguishes TNRD from earlier diffusion models is that both the filters *and* the influence functions are learned, and both vary across stages. The process is truncated to fewer than ten stages and is *well-suited for parallel computation on GPUs*, in explicit contrast to BM3D, which the paper notes is *challenging for parallel computation*.

This is why the classical-to-deep transition is continuous rather than a rupture, and why DnCNN can later derive part of its own justification from a one-stage TNRD.

### 5.2 DnCNN

Three layer types and one global skip. Layer 1 is Conv+ReLU with 64 filters of $3\times3\times c$ and no batch normalisation; layers 2 to $D-1$ are Conv+BN+ReLU with 64 filters of $3\times3\times64$; layer $D$ is convolution alone, producing the output. Zero padding throughout, no pooling, and the paper reports the simple padding strategy produces no boundary artefacts. For DnCNN-S at depth 17 on grayscale the parameter budget is $576 + 15\times(3\cdot3\cdot64\cdot64) + 576 + 15\times2\times64 \approx 556\,$K — essentially one block repeated fifteen times.

**Residual learning.** The network learns $\mathcal{R}(y) \approx v$ and the clean image is recovered as $x = y - \mathcal{R}(y)$. The loss is

$$\ell(\Theta) = \frac{1}{2N}\sum_{i=1}^{N} \big\lVert \mathcal{R}(y_i;\Theta) - (y_i - x_i) \big\rVert_F^2,$$

so the target is the actual noise and the loss never looks at the clean image directly. The justification proceeds in two steps. From ResNet, *when the original mapping is more like an identity mapping, the residual mapping will be much easier to optimize*; and the noisy observation $y$ *is much more like the latent clean image $x$ than it is like the residual image $v$*, especially at low noise. So learning $F(y)=x$ drives the network toward an identity transform, which a stack of convolutions with ReLUs has no natural way to express — seventeen layers would have to conspire into it, a narrow point in parameter space — whereas learning $\mathcal{R}(y)=v$ places the "do nothing" solution at zero, trivially reachable by driving the weights toward zero. DnCNN is *not* ResNet: the paper is explicit that it *employs a single residual unit to predict the residual image* rather than many identity shortcuts.

**The RL/BN synergy.** Direction one is unremarkable: BN alleviates internal covariate shift, and residual learning with BN beats residual learning without it. Direction two is the surprising one — *without residual learning, batch normalization even has a certain adverse effect on convergence*. The mechanism: a mini-batch is only 128 patches, and without residual learning the layer inputs are correlated with their neighbours and depend on the content of those particular images, so the batch statistics are not meaningful. With residual learning, DnCNN *implicitly removes the latent clean image in the hidden layers*, making the inputs of each layer *Gaussian-like distributed, less correlated, and less related to image content*. The paper adds that the residual image and batch normalisation are *both associated with the Gaussian distribution*, and confirms that the win comes from the integration rather than the optimiser — both SGD and Adam give the best results with RL+BN.

**Depth.** With no pooling and $3\times3$ filters, the receptive field of a depth-$d$ network is exactly $(2d+1)\times(2d+1)$. The authors tabulated the effective patch sizes of every competitor at $\sigma = 25$ — EPLL $36^2$, MLP $47^2$, BM3D $49^2$, CSF and TNRD $61^2$, WNNM $361^2$ — and asked whether a DnCNN with a field similar to the *smallest* could compete. Hence $35\times35$, which is depth 17; depth 20 and $41\times41$ for the general tasks, because *high noise level usually requires larger effective patch size*.

### 5.3 Results, honestly read

| Method | Year | BSD68 $\sigma{=}15$ | $\sigma{=}25$ | $\sigma{=}50$ |
|---|---|---:|---:|---:|
| BM3D | 2007 | 31.07 | 28.57 | 25.62 |
| WNNM | 2014 | 31.37 | 28.83 | 25.87 |
| TNRD | 2016 | 31.42 | 28.92 | 25.97 |
| **DnCNN-S** | 2017 | **31.73** | **29.23** | **26.23** |
| **DnCNN-B** (blind) | 2017 | 31.61 | 29.16 | 26.23 |

*Source: DnCNN Table II.*

DnCNN-S beats BM3D by 0.6 dB at all three noise levels, against a literature ceiling of 0.3 dB and an estimated bound of 0.7 dB — roughly 85% of the available headroom. The blind model achieves nearly the same while beating competitors that were trained for the specific noise level.

**Where it loses.** At $\sigma=25$ on the 12-image set, DnCNN-S scores 30.00 on Barbara against BM3D's 30.71 and WNNM's 31.24, and trails WNNM on House. These are exactly the two images dominated by repetitive structure. The paper's explanation is the most valuable passage in its experimental section: *non-local means based methods are usually better on images with regular and repetitive structures, whereas discriminative training based methods generally produce better results on images with irregular textures* — repetitive images *meet well with the non-local similarity prior*.

**Runtime.** At $512^2$, WNNM 773.2 s (CPU), BM3D 2.85 s (CPU), DnCNN-B 0.060 s (GPU). The hardware asymmetry must be stated: the paper itself warns that GPU run time *varies greatly with respect to GPU and GPU-accelerated library*, and that the CSF and TNRD GPU times were copied from the original papers.

**DnCNN-3.** Redefining $v$ as the difference between a high-resolution image and the bicubic upsampling of its low-resolution version turns the same model into single-image super-resolution; redefining it as the difference between an original and its JPEG-compressed version turns it into deblocking. One model beats task-specific baselines on all three. The theoretical permission comes from the connection with one-stage TNRD: the residual estimate remains valid whenever the derivative of the data-fidelity term vanishes at zero, which holds for *many types of noise distributions, e.g. the generalized Gaussian distribution*.

### 5.4 Bottleneck 2

DnCNN closed bottleneck 1 completely: no test-time optimisation, no hand-tuned constants, no per-noise-level model, and real-time inference. The bill it left is in its own loss function, which requires $x$. For fluorescence microscopy, cryo-electron microscopy, MRI and astronomy, a clean ground truth does not exist and cannot be acquired.

> **Bottleneck 2: the training signal requires a clean image.**

And visible in its own results table, three years before anyone could address it:

> **Bottleneck 3: the receptive field is 35×35, and self-similarity is not.**

---

## 6. Part IV — The data branch

### 6.1 Noise2Noise

$L_2$ regression learns the conditional mean of the target. A trivial property of $L_2$ minimisation is that *on expectation, the estimate remains unchanged if we replace the targets with random numbers whose expectations match the targets*. So if $\mathbb{E}\{\hat{y}_i \mid \hat{x}_i\} = y_i$ — which a second noisy photograph of the same scene provides — the optimal parameters are unchanged:

$$\arg\min_\theta \sum_i L\big(f_\theta(\hat{x}_i), \hat{y}_i\big).$$

Given infinite data the solution equals clean-target training; for finite data the extra variance is the target-corruption variance divided by the number of samples. Crucially, none of this relies on a likelihood model of the corruption or a prior on clean images. The loss selects the estimator: $L_2$ recovers the mean, $L_1$ the median — which allows training on data with up to 50% outlier content.

Measured on Kodak, BSD300 and Set14 at $\sigma=25$: clean targets average 31.63 dB, noisy targets 31.61 dB. **The clean-data requirement costs 0.02 dB.**

### 6.2 Noise2Void

Noise2Noise still requires two independent observations of one scene. N2V removes that using a blind-spot receptive field: the prediction for a pixel depends on its square neighbourhood *except the pixel itself*. Because the noise is assumed conditionally pixel-wise independent given the signal, the neighbours carry no information about that pixel's own noise, so the network cannot learn the identity; because the signal is assumed to have spatial dependencies, it can still be estimated from the surroundings.

In practice N2V does not build the architecture — it *replaces the value in the centre of each input patch with a randomly selected value from the surrounding area* and computes the loss only at those masked pixels, manipulating $N = 64$ pixels per $64\times64$ patch for gradient efficiency.

The cost is real and should be stated plainly. On BSD68 at $\sigma=25$: supervised 29.06, Noise2Noise 28.86, BM3D 28.59, **Noise2Void 27.71**. On natural images with plentiful clean data, N2V is worse than a 2007 algorithm. The argument for it is not quality but **availability**: on the two Cell Tracking Challenge datasets the paper's own figure captions the ground-truth column *does not exist*, and neither supervised nor N2N training can be applied at all.

### 6.3 ZS-N2N

ZS-N2N removes the training set. Two fixed stride-2 convolutions with kernels $k_1 = \begin{psmallmatrix}0 & \frac12\\ \frac12 & 0\end{psmallmatrix}$ and $k_2 = \begin{psmallmatrix}\frac12 & 0\\ 0 & \frac12\end{psmallmatrix}$ split the noisy image into two half-resolution images with similar signal and independent noise — an approximation of the Noise2Noise pair, obtained from one image. The loss is symmetric and residual, plus a consistency term:

$$L_{\text{res}} = \tfrac12\Big(\lVert D_1 - f_\theta(D_1) - D_2\rVert^2 + \lVert D_2 - f_\theta(D_2) - D_1\rVert^2\Big),$$

$$L_{\text{cons}} = \tfrac12\Big(\lVert D_1 - f_\theta(D_1) - D_1(y - f_\theta(y))\rVert^2 + \lVert D_2 - f_\theta(D_2) - D_2(y - f_\theta(y))\rVert^2\Big).$$

Only the consistency term ever shows the network the image at full resolution, and the paper describes it as a regulariser that removes the need for the early stopping that DIP and Noise2Fast require. The network is two $3\times3$ convolutional operators followed by a $1\times1$ — about **20 K parameters** — and the ablation shows that substituting a U-Net causes overfitting and much worse performance, so the tiny network is load-bearing rather than a compromise. Convergence takes 1–2 K iterations, under a minute on CPU. The comparison that lands: Self2Self requires *1.2 hours to denoise one 256×256 image on a GPU*.

Note also that the loss is **residual** — DnCNN's 2017 design choice is still the default in a 2023 zero-shot paper.

### 6.4 P2N, and why it is a supervision change

Every self-supervised method above pays for its training signal by discarding information: N2V blinds a pixel, ZS-N2N halves the resolution. P2N's claim is that neither sacrifice is necessary. Renoised Data Construction denoises the image, estimates the noise, and adds it back with a plus and a minus to build $y^{+}$ and $y^{-}$; Denoised Consistency Supervision then trains the two denoised results to agree.

This is **not** merely a new loss function, and the distinction matters:

- it changes **what goes into the network** — $y^{+}$ and $y^{-}$ are constructed from the model's own output and do not exist until the model has run once;
- it changes **how many forward passes** there are — three, not one;
- it changes **which pair is compared** — output against output, not output against target.

A loss function scores a fixed prediction against a fixed target. P2N rewrites the whole training signal.

Meanwhile the architecture is untouched. In the official repository the network class is literally named `UNet_n2n_un` and matches the 2018 Noise2Noise channel widths exactly; P2N+ adds one optional module, Symmetric Prior Injection.

> **The through-line: the network never moved. The target did.**

---

## 7. Part V — The architecture branch

### 7.1 Bottleneck 3, with a receipt

Two independent measurements, eight years apart, of the same phenomenon:

| Measurement | Value | Source |
|---|---|---|
| Barbara, $\sigma{=}25$, DnCNN-S vs BM3D | **−0.71 dB** | DnCNN Table III |
| BSD68 $\sigma{=}50$, DnCNN → Restormer | **+0.39 dB** | Restormer Table 4 |
| Urban100 $\sigma{=}50$, DnCNN → Restormer | **+1.98 dB** | Restormer Table 4 |

Urban100 is 100 photographs of buildings, whose structure repeats identically across hundreds of pixels — Barbara's scarf at dataset scale. **The gain is five times larger on the dataset made of repetition.** A convolution stack reaches $(2d+1)^2$ pixels, so its reach grows *linearly in depth*; reaching WNNM's $361^2$ effective patch size the DnCNN way would need 180 layers. The architecture branch is the search for an operator whose reach is not bought by depth.

### 7.2 Restormer

Vanilla self-attention costs $O(W^2H^2)$, which for a $256^2$ image means an attention matrix with $4.3\times10^9$ entries. SwinIR restricts attention to windows, which Restormer objects to on structural grounds: *restricting the spatial extent of SA is contradictory to the goal of capturing the true long-range pixel relationships*.

MDTA instead moves the axis: attention is computed **across channels**, so the attention map is $C\times C$ and complexity is linear in the number of pixels. $Q$, $K$ and $V$ are formed by $1\times1$ point-wise convolutions followed by $3\times3$ depth-wise convolutions, and

$$\text{Attention}(\hat{Q},\hat{K},\hat{V}) = \hat{V}\cdot\text{softmax}\!\left(\hat{K}\hat{Q}^{\top}/\alpha\right).$$

GDFN replaces the first linear layer of the feed-forward network with a gate — the element-wise product of two projections, one GELU-activated — with expansion factor $\gamma = 2.66$.

Ablation on Urban100 at $\sigma=50$: baseline UNet-with-Resblocks 29.11; MDTA + FN 29.43; MTA + GDFN 29.54; **MDTA + GDFN 29.62**, a gain of 0.51 dB for a 5% FLOP increase. Progressive learning — patch size rising from $128^2$ to $384^2$ with batch size falling from 64 to 8 at fixed iterations — adds further gains at equal training time. Restormer is also reported as having 3.14× fewer FLOPs and running 13× faster than SwinIR.

### 7.3 NAFNet

NAFNet asks whether any of it is necessary. Its two derivations:

$$\text{GLU}(X, f, g, \sigma) = f(X) \odot \sigma(g(X)), \qquad \text{GELU}(x) = x\,\Phi(x),$$

so GELU is the special case of a gated linear unit with $f, g$ the identity and $\sigma = \Phi$. Since the GLU *itself contains nonlinearity and does not depend on $\sigma$* — the product of two linear transformations is not linear — the activation can be deleted entirely:

$$\text{SimpleGate}(X, Y) = X \odot Y,$$

implemented as a channel split and a multiply. The same argument applied to channel attention, $\text{CA}(X) = X \ast \sigma(W_2\max(0, W_1\,\text{pool}(X))) = X \ast \Psi(X)$, yields

$$\text{SCA}(X) = X \ast W\,\text{pool}(X),$$

with no Sigmoid and no ReLU. The result is a network with no nonlinear activation functions anywhere.

The ablation ladder on SIDD: PlainNet 39.29 → +LayerNorm 39.73 → GELU 39.71 → +CA 39.85 → SimpleGate 39.93 → SCA 39.96, and the full-capacity model 40.30 dB, exceeding the previous state of the art by 0.28 dB at less than half its computational cost.

**The largest single gain in that ladder is LayerNorm, worth +0.44 dB — not because normalisation is magic, but because it stabilises training at a ten-times larger learning rate.** A large share of reported architectural progress in restoration is optimisation progress wearing a costume.

### 7.4 SCUNet and MambaIR

SCUNet attacks the same problem from two sides. Architecturally, the swin-conv block splits the feature map in half, sending one half to a Swin Transformer block and the other to a residual convolutional block, running local and non-local priors in parallel rather than replacing one with the other. On the data side, it synthesises Gaussian (3-D generalised, with a $3\times3$ covariance matrix modelling cross-channel correlation), Poisson, speckle, JPEG and processed camera sensor noise — the last by inverting a real ISP to raw, adding read and shot noise there, and running the forward pipeline with per-camera tone curves — plus resizing, a random shuffle strategy, and a double degradation strategy.

MambaIR borrows a selective structured state-space model. The continuous system $h'(t) = Ah(t) + Bx(t),\ y(t) = Ch(t) + Dx(t)$ is discretised by zero-order hold and admits both an RNN form (unbounded memory) and a CNN form (parallel training); Mamba makes $B$, $C$ and $\Delta$ input-dependent. Adapting it to images requires two repairs, both named by the paper: **local pixel forgetting**, because flattening separates vertically adjacent pixels by hundreds of sequence steps, fixed by local convolution; and **channel redundancy** from the excessive hidden-state count, fixed by channel attention. Scanning is four-directional; ablation gives 34.15 on Urban100 against 34.06 for one direction.

### 7.5 Three live answers

| Answer | Mechanism | Strength | Cost |
|---|---|---|---|
| Restormer | Attention across channels | Leads Urban100; first past 40 dB on SIDD *and* DND | 10.44 s CPU at $256^2$ `[measured]` |
| NAFNet | No attention, no activations | 40.30 dB SIDD; 5.5× faster than Restormer on CPU | 116.0 M parameters `[measured]` |
| MambaIR | Selective state-space scan | Best DND at 40.04 dB | Will not import without CUDA `[measured]` |
| SCUNet | Synthetic degradation pipeline | 9.7 M parameters; robust on real photographs | Not the top of any AWGN table |

None has displaced the others. That is what an unresolved research question looks like from the inside.

---

## 8. Part VI — Engineering reality

### 8.1 The organising question, in code

| Era | Open the file, and you find… | What ships | Test-time cost |
|---|---|---|---|
| Classical DIP | A `while` loop and a hand-tuned `weight` | An algorithm | An optimisation, per image |
| Deep CNN, 2017 | A list comprehension of convolution layers | A `.pth` file | One forward pass |
| Data branch, 2018–2025 | The supervision. **The network stops changing.** | A `.pth` plus ~50 gradient steps per image | A short optimisation, per image |
| Architecture branch, 2022–2024 | A new operator replacing the $3\times3$ convolution | A `.pth` and a YAML | One forward pass |

**Classical.** `scikit-image`'s `denoise_tv_chambolle` puts four era-defining facts on one screen: the `weight` argument *is* $\lambda$; `norm.sum()` *is* $\Phi(x) = \lVert\nabla x\rVert_1$; the `while` loop is the test-time optimisation; and the `break` on relative energy change is the stopping criterion. Nothing persists — calling it on a second image reruns every iteration.

**Deep.** In `cszn/KAIR`, `network_dncnn.py` builds the body as `[B.conv(nc, nc, mode='C'+act_mode) for _ in range(nb-2)]` and `forward` returns `x-n`. The three layer types of the paper are literally `m_head`, `m_body`, `m_tail`, and the layer grammar is a three-character string: `'CBR'`, `'CR'`, `'C'`. **The prior is not in the file at all** — it is in the `.pth` checkpoint the class will load. (Note a subtlety: the *paper's* network outputs $\hat{v}$ and the subtraction happens outside; KAIR folds the subtraction into `forward`, so the module returns the clean image. The residual mapping is still what the weights learn — only the module boundary moved.)

**Data branch.** The NVlabs Noise2Noise repository is **TensorFlow** — the last major denoiser released outside PyTorch — and the change from supervised training is structurally one conditional on which tensor is the target. In `P2N-plus`, `noise_estimation_loss` constructs its own inputs and runs three forward passes, and one function implements all the competing self-supervised paradigms behind a `--mode` flag.

> **A caveat found by reading the code against the paper.** Two of those `--mode` branches feed RDC-constructed data to Noise2Void and Noise2Noise. The paper states this data is unsuitable for them because the noise in RDC-constructed images is **correlated**, which collapses their training. Those branches are a documented negative result, not a fair comparison.

**Architecture branch.** Restormer's linear complexity is one `rearrange`: the pattern `'b (head c) h w -> b head c (h w)'` puts pixels on the last axis, so `q @ k.transpose(-2,-1)` is $C\times C$. NAFNet's SimpleGate is `x1, x2 = x.chunk(2, dim=1); return x1 * x2` and its SCA is `nn.Sequential(nn.AdaptiveAvgPool2d(1), nn.Conv2d(...))` with no activation at all — four lines against two pages of derivation. Both blocks also carry `self.beta` and `self.gamma`, learned scalars initialised to zero (`skip-init`), so each block starts as an identity and training decides how much to switch on — a stability device that does not appear in the paper's block diagram.

### 8.2 Frameworks, configuration, weights

| Era | Framework | Configuration |
|---|---|---|
| Classical, ≤2014 | MATLAB / C, or NumPy | Function arguments |
| DnCNN, 2017 | **MatConvNet** (MATLAB) | Hard-coded in a training script |
| Noise2Noise, 2018 | **TensorFlow** | `argparse` flags |
| KAIR, 2018–2024 | PyTorch | A JSON options file |
| Restormer / NAFNet, 2022 | PyTorch + **BasicSR** | **YAML**, resolved by a registry |
| MambaIR, 2024 | PyTorch + compiled CUDA ext. | YAML + registry |
| P2N+, 2025 | PyTorch | `argparse`, with a `--mode` flag |

Two consequences. The BasicSR registry means the architecture is *named by a string in a config file*, so swapping Restormer for NAFNet is a one-line YAML edit — architectures have become interchangeable components. And between 2017 and 2022 the unit of reproducibility moved from *a script you edit* to *a config you version-control*.

On pre-trained weights, the contrast the brief asks for is total. The classical artefact is an algorithm plus constants a human chose, with no reuse: every image restarts from nothing. The modern artefact is a `.pth` file — a serialised `state_dict` — downloaded once and reused indefinitely, loaded with `load_state_dict` (strict by default, so shape mismatches fail loudly), distributed via GitHub Releases and increasingly Hugging Face model cards carrying architecture, training data, metrics and licence as structured metadata. The consequence that is easy to miss: a modern denoiser is **two decoupled artefacts**, so a better checkpoint can ship without touching the code, and the architecture can be swapped without retraining the pipeline. The classical era had no such separation, which is a large part of why it could not compound.

### 8.3 A deployment detail no paper reports

| Model | Required multiple | Padding mode |
|---|---|---|
| Restormer | 8 | `reflect` |
| NAFNet | 16 (`2 ** len(self.encoders)`) | zero (default `F.pad`) |
| P2N+ | 32 | `reflect` |
| SCUNet | 64 (`int(np.ceil(h/64)*64-h)`) | `nn.ReplicationPad2d` |

A factor of eight separates the extremes, and the *modes* differ too — zero padding injects an artificial edge, reflection and replication do not. Feed a $1000\times1000$ image to SCUNet and 24 rows and columns of replicated content are invented, processed, and cropped away. None of this appears in any of the four papers.

### 8.4 What we measured

Each model instantiated from its own repository at a pinned commit, in its denoising configuration. Parameters are `sum(p.numel() for p in model.parameters())`. Latency is the mean of three forward passes at $256\times256$ after one warm-up, under `torch.no_grad()`, **CPU only**, PyTorch 2.13.0, no CUDA.

| Model | Configuration | Parameters | CPU latency, $256^2$ |
|---|---|---:|---:|
| DnCNN-B | `DnCNN(in_nc=1, nc=64, nb=20)` | 0.668 M | 1.015 s |
| P2N+ backbone, SPI off | `UNet_n2n_un(conv_type='plain')` | 0.991 M | 0.286 s |
| P2N+ backbone, SPI on | `UNet_n2n_un(conv_type='SPI')` | 0.925 M | 0.710 s |
| SCUNet | `config=[2]*7, dim=64` | 9.663 M | 1.685 s |
| Restormer | `dim=48, [4,6,6,8]` | 26.127 M | 10.436 s |
| NAFNet | `width=64`, enc `[2,2,4,8]`, mid 12 | 115.983 M | 1.899 s |
| MambaIR | — | *not measurable* | `ModuleNotFoundError: mamba_ssm` |

**Caveats, stated before they are asked.** Absolute CPU latencies are not comparable to published GPU timings — only the ratios are informative. And the forward passes used **random tensors**, so no PSNR or SSIM was measured here.

Four readings follow, none of them visible from a paper:

1. **Parameters do not predict latency.** NAFNet carries 4.4× Restormer's parameters and runs 5.5× faster. NAFNet is $1\times1$ and depth-wise convolutions on fast GEMM paths; Restormer's `rearrange` calls force layout changes. *"More efficient" is meaningless without naming the metric and the device.*
2. **SPI costs latency, not parameters.** Symmetric Prior Injection *reduces* parameters by 6.7% because `Symlayer` routes through a half-width bottleneck, yet raises latency 2.5× because every layer is evaluated twice, on $x$ and on $-x$. The opposite of what a parameter table predicts.
3. **Depth at full resolution is expensive.** DnCNN is the smallest model here and is still slower than the larger P2N+ backbone, because it runs 20 sequential full-resolution $3\times3$ convolutions while a U-Net does most of its work at reduced resolution.
4. **Some models do not run.** MambaIR's import failure is not a gap in the experiment — it *is* the result, and it describes a deployment profile fundamentally different from the others. The repository's changelog also records that published `thop` complexity figures were wrong.

---

## 9. Part VII — Comparative analysis

### 9.1 The three comparisons that carry the argument

**BSD68 has saturated.** At $\sigma=25$: 2007→2014, seven years of hand-designed priors, +0.26 dB; 2014→2017, one architectural idea, +0.40 dB; 2017→2022, five years and an entire Transformer revolution, +0.36 dB.

**Urban100 has not.** The same five years, same models, same table: +1.98 dB at $\sigma=50$ against BSD68's +0.39 dB.

**Real noise is a different problem entirely.** From Restormer's Table 6, evaluated under one protocol:

| Method | SIDD PSNR | SIDD SSIM | DND PSNR |
|---|---:|---:|---:|
| **DnCNN** (AWGN-trained, 2017) | **23.66** | 0.583 | 32.43 |
| BM3D (classical, 2007) | 25.65 | 0.685 | 34.51 |
| Uformer (2022) | 39.77 | 0.959 | 39.96 |
| **Restormer** (2022) | **40.02** | **0.960** | 40.03 |
| NAFNet (2022) | **40.30** | — | — |
| MambaIR (2024) | 39.89 | 0.960 | **40.04** |

DnCNN — which beats BM3D by 0.6 dB on synthetic Gaussian noise — is beaten by BM3D by **1.99 dB** on real sensor noise and trails Restormer by **16.36 dB**. A model trained on the wrong noise distribution does not degrade gracefully; it collapses. This is what SCUNet means by *noise assumption mismatch*.

### 9.2 What supervision costs

| Method | Requires | BSD68 $\sigma{=}25$ |
|---|---|---:|
| Supervised U-Net | Paired clean + noisy | 29.06 |
| DnCNN-S | Paired clean + noisy | 29.23 |
| Noise2Noise | Two noisy copies per scene | 28.86 |
| BM3D | **Nothing** | 28.57 / 28.59 |
| Noise2Void | A body of single noisy images | 27.71 |

Giving up the clean target costs ~0.20 dB; giving up the second copy costs a further 1.15 dB and drops below a 2007 algorithm. But where clean data does not exist, the comparison is not between 27.71 and 29.23 — it is between 27.71 and nothing.

*(The two BM3D figures, 28.57 and 28.59, come from two different papers evaluating the same method on the same dataset at the same noise level. The discrepancy is small and is noted rather than silently averaged.)*

### 9.3 Efficiency has no single axis

The same set of models yields incompatible rankings depending on the metric: by parameters DnCNN is best and NAFNet worst by 174×; by CPU wall-clock the P2N+ backbone is best and Restormer worst by 36×; by quality on real noise NAFNet is best and DnCNN worst by 16 dB. Restormer's own FLOP claim against SwinIR is a fourth axis again.

### 9.4 Synthesis

On BSD68 the field gained **1.00 dB in fifteen years**. On Urban100 it gained **1.98 dB in five**. On real noise it gained **16.64 dB**.

> **Progress in denoising since 2017 is mostly not progress on the 2017 problem.**

---

## 10. Part VIII — Open problems

1. **A general-purpose blind real denoiser remains unsolved** — SCUNet's abstract states this directly. SCUNet's answer is synthetic degradation; Restormer's and NAFNet's is training on SIDD's 320 captured scenes. Neither generalises to an unseen camera with an unseen ISP, and no benchmark currently measures that. The difficulty is structural: real noise is read noise plus shot noise in the raw domain, transformed by demosaicing, white balance, colour conversion, tone mapping and gamma — a pipeline, not a distribution.
2. **Fidelity metrics reward blur.** Every loss in Part VI is $L_1$, $L_2$ or PSNR, and all three recover a conditional mean. Noise2Noise itself names the mechanism: an $L_2$-trained regressor *learns to output the average of all plausible explanations, which results in spatial blurriness*. Perceptual and adversarial losses would fix this and would score *worse* on PSNR, which is why they are common in super-resolution and essentially absent from denoising. As long as leaderboards are PSNR-ranked, the incentive points the wrong way.
3. **Nobody agrees what "efficient" means** (§9.3), and MambaIR's changelog concedes its own published complexity figures were wrong.
4. **The benchmarks have saturated** (§9.1). New capability is arriving faster than the instruments to detect it.
5. **Self-supervision has not met supervision.** N2V trails supervised training by 1.35 dB; P2N removes the information loss rather than closing the gap, and still pays per-image test-time optimisation. Bottleneck 2 is mitigated, not closed — and the domains that need it most are precisely those where no clean reference exists to measure the remaining gap.
6. **The two branches have never merged.** *(Our own observation, and the structural claim of this work.)* P2N ships the 2018 Noise2Noise U-Net verbatim; Restormer, NAFNet and MambaIR all assume paired data. As far as we found, nobody has published a state-space or Transformer backbone trained under RDC/DCS supervision. Whether the branches compose or conflict appears to be open and untested.

### 10.1 What we would deploy

Naming the constraint is the answer; the fork in the timeline predicts which.

| Constraint | Choice | Evidence |
|---|---|---|
| GPU, paired data, real photographs | **NAFNet** | 40.30 dB SIDD; best accuracy-per-ms measured; simplest code |
| CPU- or memory-bound | **SCUNet** | 9.663 M parameters; synthetic-degradation training |
| Maximum quality on repetitive structure | **Restormer** (MambaIR if CUDA guaranteed) | Leads Urban100; only method past 40 dB on both SIDD and DND |
| No clean data at all | **P2N**, or **ZS-N2N** for one image | Accepts per-image test-time optimisation |
| Dependency-free baseline | **BM3D** | No data, no GPU; still beats AWGN-trained DnCNN on real noise by 1.99 dB |

---

## 11. Bibliography

### Category A — 12 peer-reviewed papers (80.0%)

Citation counts are Google Scholar figures checked **9 August 2026**, except A12, which was not verified.

| # | Paper | Venue & year | Cited by |
|---|---|---|---|
| A1 | Dabov, Foi, Katkovnik & Egiazarian — *Image Denoising by Sparse 3-D Transform-Domain Collaborative Filtering* (**BM3D**) | IEEE TIP 16(8), 2007 | 11 976 |
| A2 | Gu, Zhang, Zuo & Feng — *Weighted Nuclear Norm Minimization with Application to Image Denoising* (**WNNM**) | CVPR 2014 | 2 960 |
| A3 | Chen & Pock — *Trainable Nonlinear Reaction Diffusion* (**TNRD**) | IEEE TPAMI 39(6), 2017 | 1 626 |
| A4 | Zhang, Zuo, Chen, Meng & Zhang — *Beyond a Gaussian Denoiser* (**DnCNN**) | IEEE TIP 26(7), 2017 | 11 674 |
| A5 | Lehtinen, Munkberg, Hasselgren, Laine, Karras, Aittala & Aila — *Noise2Noise* | ICML 2018 | 3 064 |
| A6 | Krull, Buchholz & Jug — *Noise2Void* | CVPR 2019 | 2 075 |
| A7 | Zamir, Arora, Khan, Hayat, Khan & Yang — *Restormer* | CVPR 2022 | 6 181 |
| A8 | Chen, Chu, Zhang & Sun — *Simple Baselines for Image Restoration* (**NAFNet**) | ECCV 2022 | 2 318 |
| A9 | Mansour & Heckel — *Zero-Shot Noise2Noise* | CVPR 2023 | 266 |
| A10 | Zhang, Li, Liang, Cao, Zhang, Tang, Fan, Timofte & Van Gool — *Practical Blind Image Denoising via Swin-Conv-UNet* (**SCUNet**) | Machine Intelligence Research 20(6), 2023 | 391 |
| A11 | Guo, Li, Dai, Ouyang, Ren & Xia — *MambaIR* | ECCV 2024 | 1 208 |
| A12 | Li, Wang, Xu, Zhu, Lu & Huang — *Positive2Negative* (**P2N**) | CVPR 2025, pp. 17924–17934 | not verified |

### Category B — 3 auxiliary sources (20.0%)

- **B1 · Stanford CS231n**, *Convolutional Neural Networks for Visual Recognition.* Supplies the backpropagation, convolution-arithmetic and optimisation background that every paper from A4 onward assumes without stating.
- **B2 · Google Research**, *Night Sight* / HDR+ technical blog. Separates photon shot noise from read noise, explains that SNR rises with the square root of exposure time, and describes burst capture, software alignment and merging. The only source describing denoising as a shipped consumer product.
- **B3 · Gonzalez & Woods**, *Digital Image Processing* — the Image Restoration chapter. Supplies the formal treatment of noise models and of mean, order-statistic and adaptive filters. It is also the reference against which SCUNet's degradation pipeline reads critically: SCUNet's noise list is essentially the textbook's noise list, industrialised.

**Quota.** 15 sources · 12 Category A = 80.0% (floor 70%) · 3 Category B = 20.0% (ceiling 30%).

---

## 12. Declared limitations

Stated here rather than discovered in the defence.

1. **No quality metric was computed by us.** Our own measurements cover parameter counts and CPU latency only, and used random tensors, so they carry no image-quality information.
2. **CPU latencies are not comparable to published GPU timings.** Only ratios between our own measurements are meaningful, and only for the CPU backend used.
3. **The DnCNN runtime table mixes devices**, and the paper states the CSF and TNRD GPU times were copied from their original papers. We reproduce the caveat wherever we reproduce the numbers.
4. **One published value is excluded.** MambaIR's CBSD68 $\sigma{=}25$ cell extracted as 32.24, inconsistent with its own row (34.48 at $\sigma{=}15$, 28.66 at $\sigma{=}50$) and with every comparable method. We judged this a probable extraction error and excluded it rather than reproduce it; MambaIR's colour results are quoted from Urban100 instead.
5. **Venue verification.** Venues for BM3D, TNRD, Noise2Noise and SCUNet are printed in the source PDFs. The remaining eight are preprint versions carrying no venue and were confirmed against publisher, CVF Open Access or institutional proceedings records.
6. **TNRD's year is genuinely ambiguous** — the PDF header reads 2016, citing literature gives TPAMI 39(6), 2017. Both reflect reality (acceptance versus issue). We cite 2017.
7. **Reference code availability is uneven.** ZS-N2N has no repository, only a Colab notebook. WNNM has only a third-party mirror with no README or licence. TNRD's available implementation is a same-laboratory re-implementation. The P2N paper's printed repository URL returns HTTP 404; the live code is at `P2N-plus`.
8. **SCUNet's venue is not on the brief's named list.** *Machine Intelligence Research* is a peer-reviewed Springer journal but is not among the venues the brief names. We read that list as illustrative — it is introduced with "e.g." — but if strict adherence is required, moving SCUNet to Category B still leaves 11 of 15 in Category A, or 73.3%, above the floor.
9. **Citation counts move.** All were checked on 9 August 2026 and should be re-checked before the defence.
