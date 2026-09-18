# -*- coding: utf-8 -*-
"""
Oral-exam question bank, part 1.

Q(id, cat, path, q, a, intuition, concepts, follows, miscon, hard)
  cat    : A direct | B conceptual | C code | D results | E misconception
  path   : "Assignment → Section → Task" breadcrumb
  follows: [(question, answer), ...]   rendered collapsed
  miscon : [(statement, why_wrong, correct), ...]
  hard   : flag for "commonly misunderstood"
LaTeX is written with \\( \\) inline and \\[ \\] display, rendered by KaTeX.
"""

def Q(id, cat, path, q, a, intuition, concepts, follows=(), miscon=(), hard=False):
    return dict(id=id, cat=cat, path=path, q=q, a=a, intuition=intuition,
                concepts=list(concepts), follows=[list(f) for f in follows],
                miscon=[list(m) for m in miscon], hard=hard)

BANK = []
A = BANK.append

# ═══════════════ 1. THE PROBLEM ═══════════════
A(Q("deg-model", "B", "Stage 3 → Part I → The degradation model",
"Write down the image denoising problem formally, and explain every symbol.",
r"""The observation model is
\[ y = x + v \]
where \(y\) is the noisy image the sensor actually produced, \(x\) is the latent clean image we want to recover, and \(v\) is the noise.

Three things are worth stressing. First, this is an **observation model**, not an algorithm — it says what happened to the image, not how to undo it. Second, it has stayed literally unchanged across the whole period this project covers: DnCNN writes \(y = x + v\) in 2017 and SCUNet writes \(y = x + n\) in 2023. Third, denoising is the problem of estimating \(x\) given only \(y\), which means recovering two unknowns from one measurement.

Noise2Void restates the same thing as a joint distribution, \( p(s,n) = p(s)\,p(n \mid s) \), with signal \(s\) and noise \(n\). That is not a different model — it is the same model written so that the independence assumptions become visible, which is exactly what makes self-supervised training possible.""",
"""If I tell you two numbers add up to 10, you cannot tell me what they are. That is the entire difficulty of denoising, repeated once per pixel, with the extra constraint that your answers have to look like a photograph when assembled.""",
["degradation model", "latent clean image", "observation vs algorithm", "joint distribution form"],
[("Why is the model additive rather than multiplicative?",
  "Because the standard benchmark assumption is AWGN, where noise is added to the pixel value. Real sensor noise is not purely additive — shot noise is signal-dependent and speckle is multiplicative — which is precisely why AWGN-trained models collapse on real photographs. SCUNet's degradation pipeline models Poisson and speckle explicitly for that reason."),
 ("What changes if the noise is not zero-mean?",
  "Then a bias survives averaging. Every method that relies on averaging observations — from the box filter to Noise2Noise — assumes \\(\\mathbb{E}[v]=0\\). With a non-zero mean you would first have to estimate and subtract the offset; otherwise the estimator converges to \\(x + \\mathbb{E}[v]\\), not \\(x\\)."),
 ("Is this model ever exactly true?",
  "For a synthetic benchmark, yes — the noise was added by the evaluation script, so the model is exact by construction. For a real photograph, no. The noise has already passed through demosaicing, white balance, tone mapping and gamma, which correlate it spatially and across channels.")],
[("The degradation model is something a denoising method chooses.",
  "It is not a design choice; it is a statement about how the data were produced. Methods differ in the prior they add, not in the observation model.",
  "Every method in this project targets the same \\(y = x + v\\). What differs is the extra information each supplies to make the inversion well-posed.")],
hard=False))

A(Q("awgn", "B", "Stage 3 → Part I → Slide 7 · AWGN",
"What does 'additive white Gaussian noise' mean, word by word, and which of those words is the dangerous one?",
r"""**Additive** — the noise is added to the pixel value, so pixel 200 becomes \(200 + \varepsilon\). It is not multiplied in (speckle) and not applied through a nonlinearity (compression). This is what makes \(x\) recoverable by subtraction, and therefore what makes residual learning possible at all.

**White** — the noise at each pixel is statistically independent of its neighbours. No spatial correlation, no structure. Noise2Void's blind spot depends entirely on this: if neighbours carried information about a pixel's own noise, the blind-spot trick would fail.

**Gaussian** — the noise follows \( v \sim \mathcal{N}(0, \sigma^2 I) \): small errors common, large errors rare, and crucially **zero mean**. Zero-mean is the whole of the Noise2Noise argument. Gaussianity is also why residual learning and batch normalisation reinforce each other in DnCNN.

**\(\sigma\)** — the standard deviation, the width of the bell, reported on 8-bit images. Benchmarks use \(\sigma \in \{15, 25, 50\}\); DnCNN-B trains blind over \([0, 55]\); SCUNet samples \(\sigma\) from \(\{2/255 \ldots 50/255\}\).

Every one of those four words is false of a real camera, and Part VII puts a number on how expensive that is: DnCNN scores 23.66 dB on real sensor noise while reaching 31.73 dB on synthetic Gaussian noise at \(\sigma=15\).""",
"""AWGN is the physicist's spherical cow. It is simple enough to reason about mathematically and to generate on demand, which is why the whole field standardised on it — and simple in exactly the ways real cameras are not.""",
["additive", "white / spatial independence", "zero-mean Gaussian", "noise level sigma", "assumption mismatch"],
[("Why does the field keep using an assumption it knows is wrong?",
  "Because it is reproducible and it isolates the variable under test. SCUNet states this explicitly: AWGN removal *is fair to test the effectiveness of different network architecture designs*, even while a general blind real denoiser remains unsolved. It is a controlled comparison, not a claim about photographs."),
 ("Which word breaks first on a real photograph?",
  "'White'. Demosaicing interpolates missing colour samples from neighbours, which correlates the noise spatially and across channels before anything else happens. Resizing and JPEG then correlate it further."),
 ("How would you verify that an image really has AWGN?",
  "Look at a flat region: estimate the residual after a strong smoother, then check (a) the histogram against a Gaussian, (b) the autocorrelation for spatial structure, and (c) whether the variance is constant across brightness levels. Shot noise fails the third test because its variance scales with signal.")],
[("Because AWGN is white, the noise has no visible structure, so any structure in the residual must be signal.",
  "That is a good diagnostic heuristic but not a theorem, and it is exactly the reasoning that fails on real noise, where the noise itself is structured.",
  "The residual-has-structure test is valid *under the AWGN assumption*. Once noise is spatially correlated, structured residual no longer implies lost signal.")],
hard=True))

A(Q("illposed", "B", "Stage 3 → Part I → Slide 8 · Ill-posedness",
"Why is denoising described as ill-posed, and what follows from that?",
r"""Given a single observation \(y\), infinitely many pairs \((x, v)\) satisfy \(y = x + v\). Arithmetic alone cannot choose among them: one measurement, two unknowns. In Hadamard's terms the solution is not unique, so the problem is ill-posed.

The consequence is the central idea of this whole project. Because the answer is not determined by the data, the algorithm must **add information that is not in the measurement**. That added information is called the **prior**.

From this, three things follow that are worth saying out loud in a defence:

1. **There is no prior-free denoiser.** A method that appears not to have one has hidden it — in an architecture, in a training set, or in a stopping criterion.
2. **The quality of a denoiser is the quality of its prior.** Everything else is optimisation detail.
3. **The history of the field is the history of where the prior lives** — hand-written formula, then learned weights, then the test image's own statistics.""",
"""Ill-posed does not mean "hard". It means "underdetermined". No amount of compute fixes underdetermination; only an assumption does.""",
["ill-posed problem", "underdetermined system", "the prior", "regularisation"],
[("Where is the prior in a neural network, concretely?",
  "In the weights, and partly in the architecture. The training set teaches the network what natural images look like; the convolutional structure encodes translation equivariance and locality as a built-in prior before any training happens."),
 ("Does more training data remove the need for a prior?",
  "No — it changes where the prior comes from. More data gives a better *estimate* of the image distribution, but the network still has to impose that distribution on an underdetermined problem at test time."),
 ("Is super-resolution ill-posed in the same way?",
  "Yes, and more severely: each low-resolution pixel corresponds to several high-resolution ones. That is why DnCNN-3 can treat super-resolution as a special case — redefine \\(v\\) as the difference between the ground truth and the bicubic upsampling, and the same residual network applies.")],
[("With a large enough network the problem stops being ill-posed.",
  "Network capacity does not add information to the measurement. It only changes how flexibly the prior can be expressed.",
  "A bigger network can represent a better prior. It cannot make one measurement determine two unknowns.")],
hard=True))

A(Q("map", "B", "Stage 3 → Part I → Slide 9 · MAP",
"Derive the classical denoising objective from Bayes' rule, and say which term is forced and which is chosen.",
r"""Start from maximum a posteriori estimation:
\[ \hat{x} = \arg\max_x p(x \mid y) = \arg\max_x p(y \mid x)\, p(x) \]
by Bayes' rule, discarding \(p(y)\) because it does not depend on \(x\).

Take negative logarithms — monotone, so the arg max becomes an arg min, and the product becomes a sum:
\[ \hat{x} = \arg\min_x \big[ -\log p(y \mid x) - \log p(x) \big] \]

Now substitute the AWGN likelihood. If \(v \sim \mathcal{N}(0, \sigma^2 I)\) then
\[ p(y \mid x) \propto \exp\!\left(-\frac{\lVert y - x\rVert^2}{2\sigma^2}\right)
\;\Longrightarrow\; -\log p(y\mid x) = \frac{\lVert y-x\rVert^2}{2\sigma^2} + \text{const} \]
which gives the standard two-term objective
\[ \hat{x} = \arg\min_x \tfrac{1}{2}\lVert y - x \rVert_2^2 + \lambda\,\Phi(x) \]

**The first term is forced.** The squared \(\ell_2\) data-fidelity penalty is not a modelling preference — it is what the Gaussian assumption produces. The \(1/\sigma^2\) is absorbed into \(\lambda\). Change the noise model and this term changes: Laplacian noise would give an \(\ell_1\) fidelity term.

**The second term is chosen.** \(\Phi\) is the prior, and the entire classical era is a sequence of guesses at it: total variation sets \(\Phi(x) = \lVert \nabla x\rVert_1\); sparse coding sets \(\Phi(x) = \lVert\alpha\rVert_0\) subject to \(x = D\alpha\); WNNM sets \(\Phi\) to a weighted nuclear norm on stacks of similar patches.

\(\lambda\) trades them off: large \(\lambda\) gives smooth and safe, small \(\lambda\) gives sharp and noisy.""",
r"""Fidelity says "stay near what the camera saw". The prior says "look like a real image". \(\lambda\) says how much you trust the camera versus your own taste.""",
["Bayes' rule", "MAP estimation", "data fidelity", "regularisation term", "lambda trade-off"],
[("Where does \\(\\lambda\\) go in the deep learning era?",
  "It disappears, because the two terms stop being separable. A discriminative network learns a direct mapping \\(y \\mapsto \\hat{x}\\); there is no explicit fidelity term and no explicit prior to weigh against it. The trade-off is baked into the weights by the training distribution."),
 ("What would the fidelity term be for Poisson noise?",
  "Not squared error. The Poisson negative log-likelihood gives a term of the form \\(\\sum_i (x_i - y_i \\log x_i)\\) — the generalised Kullback–Leibler divergence. This is why methods derived under a Gaussian likelihood are not automatically correct for photon-limited imaging."),
 ("Is MAP the same as MMSE?",
  "No. MAP returns the mode of the posterior; the minimum mean squared error estimator returns its mean. They coincide for a Gaussian posterior but not in general — and the MMSE estimate, being an average over plausible images, is the blurrier of the two.")],
[("The \\(\\ell_2\\) data term is chosen because it is mathematically convenient.",
  "It is convenient, but that is not why it is there. It follows directly from the Gaussian log-likelihood.",
  "Under AWGN the squared \\(\\ell_2\\) term is derived, not chosen. Convenience is a happy consequence of the assumption, not the justification for the term.")],
hard=True))

A(Q("psnr", "B", "Stage 3 → Part I → Slide 10 · PSNR",
"Define PSNR, and explain why a 0.6 dB improvement is considered a large result.",
r"""\[ \mathrm{MSE} = \frac{1}{MN}\sum_{i}\sum_{j}\big[x(i,j) - \hat{x}(i,j)\big]^2,
\qquad \mathrm{PSNR} = 10\log_{10}\!\left(\frac{\mathrm{MAX}^2}{\mathrm{MSE}}\right)\ \text{dB} \]
with \(\mathrm{MAX} = 255\) for 8-bit images. Higher is better; identical images give \(\mathrm{MSE}=0\) and infinite PSNR.

The logarithm is what makes small numbers meaningful. Halving the MSE gains exactly \(10\log_{10}2 = 3.01\) dB, so a 0.6 dB gain corresponds to roughly a 13% MSE reduction:
\[ 10^{-0.6/10} \approx 0.871 \]

The reason 0.6 dB counts as large is not intuition but the calibration DnCNN supplies itself. Prior work found that *few methods can outperform BM3D by more than 0.3 dB on average*, and the estimated PSNR bound over BM3D is about 0.7 dB. MLP and TNRD achieved roughly 0.35 dB. DnCNN-S beat BM3D by **0.6 dB at all three noise levels** — about 85% of the theoretically available headroom — and DnCNN-B achieved nearly the same **without being told \(\sigma\)**.

The honest caveat: PSNR is pixel-wise and has no model of perception. Two images with identical PSNR can look completely different depending on whether the error sits on an edge or in flat sky. And blurring a noisy image lowers MSE while visibly destroying texture, so PSNR can be raised by making an image worse to look at.""",
"""Decibels compress. Going from 28 to 29 dB is not "one better out of thirty" — it is a 21% reduction in squared error, on a benchmark where a decade of work moved the number by about one decibel in total.""",
["mean squared error", "logarithmic scale", "3 dB = halved MSE", "practical vs theoretical ceiling", "blur gaming the metric"],
[("What PSNR would you get from doing nothing?",
  "PSNR between the noisy input and the clean reference. For \\(\\sigma = 25\\) on 8-bit data, \\(10\\log_{10}(255^2/25^2) \\approx 20.2\\) dB. Any denoiser reporting below about 20 dB at that noise level is doing worse than the identity function."),
 ("Why not just report MSE?",
  "Three reasons: the log scale makes differences across noise levels comparable; decibels are the convention so results are comparable across twenty years of papers; and MSE values are tiny and awkward to read. Nothing is lost — the transform is monotone and invertible."),
 ("Can PSNR be misleading between two methods?",
  "Yes, and slide 38 is the example. DnCNN beats BM3D by 0.47 dB on the 12-image average but loses by 0.71 dB on Barbara. The average hides a systematic failure on repetitive texture, which is why per-image and per-dataset breakdowns matter.")],
[("A 0.6 dB improvement is small because 0.6 is a small number.",
  "It ignores the logarithm and the empirical ceiling. 0.6 dB is ~13% of the squared error, against a literature ceiling of 0.3 dB and a theoretical bound of 0.7 dB.",
  "Judge a dB figure against the headroom available on that benchmark, not against the absolute magnitude of the number."),
 ("Higher PSNR always means a better-looking image.",
  "PSNR rewards the conditional mean, and the mean of all plausible clean images is smoother than any of them.",
  "A Gaussian blur can raise PSNR while visibly destroying texture. This is why SSIM is reported alongside it, and why Noise2Noise names the resulting *spatial blurriness* explicitly.")],
hard=True))

A(Q("ssim", "B", "Stage 3 → Part I → Slide 11 · SSIM",
"What does SSIM measure that PSNR cannot, and why is IoU not reported in this project?",
r"""SSIM decomposes similarity into three local comparisons and multiplies them:
\[ \mathrm{SSIM}(x,\hat{x}) = [l(x,\hat{x})]^{\alpha}\,[c(x,\hat{x})]^{\beta}\,[s(x,\hat{x})]^{\gamma}, \qquad \alpha=\beta=\gamma=1 \]
which expands to
\[ \mathrm{SSIM} = \frac{(2\mu_x\mu_{\hat{x}} + C_1)(2\sigma_{x\hat{x}} + C_2)}{(\mu_x^2 + \mu_{\hat{x}}^2 + C_1)(\sigma_x^2 + \sigma_{\hat{x}}^2 + C_2)} \]
computed in a sliding local window and averaged. \(\mu\) are local means, \(\sigma^2\) local variances, \(\sigma_{x\hat{x}}\) the local covariance, and \(C_1, C_2\) small constants that stop the ratio exploding when the denominator approaches zero.

The structure term \(s = \sigma_{x\hat{x}} / (\sigma_x \sigma_{\hat{x}})\) is a **local correlation coefficient**. This is the part PSNR has no analogue for. Blur reduces \(\sigma_{\hat{x}}\) and decorrelates the estimate from the reference, so blurring lowers SSIM even where it raises PSNR. That is the entire reason to report both.

Range is \([0,1]\) for non-negative images, reported to three decimals — Restormer's real-noise SSIM on SIDD is 0.960.

**On IoU.** The assignment brief lists PSNR, SSIM and IoU as example comparison metrics because the brief is written generically across many project topics. Intersection-over-Union measures the overlap of two regions and belongs to segmentation and detection. Denoising is dense regression with continuous-valued output — there are no regions to intersect, so IoU is undefined here. Raising this explicitly, rather than forcing a meaningless number, is the defensible position.""",
"""PSNR asks "how wrong is each pixel?". SSIM asks "does the local pattern still look like the original pattern?". Blur keeps pixels roughly right while destroying the pattern, which is why the two metrics disagree exactly where it matters.""",
["luminance / contrast / structure", "local correlation coefficient", "stabilising constants", "perception–distortion", "IoU is undefined for regression"],
[("Is SSIM a measurement of human perception?",
  "No. It is a hand-designed model of perception that correlates better with human judgement than PSNR does. It is still an engineered formula, which is why modern work adds LPIPS and no-reference metrics rather than treating SSIM as ground truth."),
 ("Why are \\(C_1\\) and \\(C_2\\) needed?",
  "Numerical stability. In a perfectly flat region \\(\\mu\\) and \\(\\sigma\\) both approach zero and the ratio becomes \\(0/0\\). The constants — conventionally \\((K_1 L)^2\\) and \\((K_2 L)^2\\) with \\(K_1 = 0.01\\), \\(K_2 = 0.03\\) — keep it finite and well-behaved."),
 ("Could you train directly on SSIM?",
  "Yes, it is differentiable and it is used in some restoration work. In this project's papers it is not: Restormer optimises plain L1 and NAFNet optimises a PSNR loss. That is itself a finding — the field optimises the distortion metric it is ranked on.")],
[("SSIM and PSNR measure the same thing on a different scale.",
  "They can move in opposite directions. Blurring raises PSNR and lowers SSIM.",
  "PSNR is a pixel-wise error measure; SSIM is a local structural correlation. Disagreement between them is informative, not noise."),
 ("The project should have reported IoU because the brief lists it.",
  "The brief's metric list is illustrative and written to cover many project topics, not all of which are regression.",
  "IoU has no definition for continuous dense output. Stating why a listed metric does not apply demonstrates judgement; reporting a fabricated number would not.")],
hard=True))

# ═══════════════ 2. CLASSICAL ═══════════════
A(Q("averaging", "B", "Stage 3 → Part II → Averaging",
"Why does averaging reduce noise, and exactly how much?",
r"""If a pixel's clean value is \(x\) and we have \(n\) independent noisy observations \(y_k = x + v_k\) with \(\mathbb{E}[v_k]=0\) and \(\mathrm{Var}[v_k]=\sigma^2\), then the sample mean has
\[ \mathrm{Var}\!\left[\frac{1}{n}\sum_k y_k\right] = \frac{\sigma^2}{n}
\quad\Longrightarrow\quad \sigma_{\text{out}} = \frac{\sigma}{\sqrt{n}} \]
A \(3\times3\) box filter averages 9 samples and divides the noise standard deviation by 3; a \(5\times5\) window divides it by 5.

The derivation depends on one assumption that is easy to miss: **every pixel in the window must share the same underlying clean value**. That is true inside a flat region and catastrophically false across an edge. Across an edge the window mean is not the centre pixel's value, so the filter introduces a **bias** proportional to the local contrast.

This is the bias–variance trade-off in its most visual form: the quantity you reduce is visible as grain, and the quantity you increase is visible as softness. A box filter makes that trade blindly.

Everything in the classical era is a better answer to the question *which pixels count as observations of the same quantity?* Gaussian weights by distance; bilateral by distance and intensity; non-local means abandons locality entirely and weights by patch similarity; BM3D stops weighting and starts stacking.""",
"""Averaging works because noise cancels and signal does not. It fails at edges because the "signal" is not one value there — you are averaging two different things and getting neither.""",
["law of large numbers", "variance reduction", "bias–variance trade-off", "edge blurring", "window selection"],
[("Why \\(\\sqrt{n}\\) rather than \\(n\\)?",
  "Because variance adds linearly for independent variables and the mean divides by \\(n^2\\): \\(\\mathrm{Var}[\\frac{1}{n}\\sum v_k] = \\frac{1}{n^2}\\cdot n\\sigma^2 = \\sigma^2/n\\). Standard deviation is the square root of that, so it falls as \\(1/\\sqrt{n}\\)."),
 ("What breaks if the observations are correlated?",
  "The variance no longer falls as \\(\\sigma^2/n\\); cross-covariance terms survive. In the limit of perfectly correlated noise, averaging removes nothing at all. This is why spatially correlated real noise is so much harder than AWGN."),
 ("How does Google's Night Sight use this?",
  "It captures a burst of short exposures, aligns them in software, and merges them. That is exactly the \\(\\sqrt{n}\\) argument applied across time rather than space — and it avoids the edge-blurring problem, because aligned frames really are observations of the same scene point.")],
[("A bigger filter window is always better for noise.",
  "Bigger windows reduce variance but increase bias wherever the window spans more than one structure.",
  "There is an optimal window size per region, which is why adaptive and non-local methods outperform fixed windows.")],
hard=False))

A(Q("nss", "B", "Stage 3 → Part II → Non-local self-similarity",
"What is non-local self-similarity, and why does it matter three separate times in this project?",
r"""Non-local self-similarity (NSS) is the observation that natural images contain many repeated local patterns, and that patches far apart in the image can be near-copies of each other. Non-local means (Buades et al., CVPR 2005) exploits it directly:
\[ \hat{x}(i) = \sum_j w(i,j)\, y(j), \qquad
   w(i,j) \propto \exp\!\left(-\frac{\lVert P_i - P_j \rVert_{2,a}^2}{h^2}\right) \]
The weight compares **patches** \(P\) centred on \(i\) and \(j\), not single pixels: two pixels are similar if their neighbourhoods are similar. Averaging many independent observations of the same structure cancels noise while the shared signal survives — the \(\sqrt{n}\) argument again, now over patches rather than a square window.

WNNM states the idea plainly: there are many repeated local patterns across a natural image, and non-local similar patches to a given patch can help much in reconstructing it.

It matters three times:

1. **It powers the classical peak.** BM3D groups similar patches before filtering; WNNM stacks them into a low-rank matrix. Both get their strength from NSS.
2. **It is the prior DnCNN lacks.** DnCNN's receptive field is \(35\times35\). It loses 0.71 dB to BM3D on Barbara, the one Set12 image dominated by repetitive texture.
3. **It is what the architecture branch had to recover.** Restormer's gain over DnCNN on Urban100 — photographs of buildings, where structure repeats across hundreds of pixels — is 1.98 dB at \(\sigma=50\), against 0.39 dB on ordinary natural images. Five times larger on the dataset made of repetition.""",
r"""A brick wall gives you a hundred photographs of the same brick. If you only look at a \(35\times35\) window you can see one brick; if you can look anywhere in the image you can average a hundred and the noise all but disappears.""",
["non-local self-similarity", "patch similarity weighting", "block matching", "receptive field limits", "Urban100"],
[("Why is NSS a *prior* rather than an algorithm?",
  "Because it is an assumption about what natural images are like — that they contain repetition. It is not derivable from the measurement; it is extra information imposed on an underdetermined problem, which is the definition of a prior."),
 ("Does NSS hold for all images?",
  "No. It holds strongly for textures, façades and regular patterns, and weakly for irregular natural texture. DnCNN's paper makes exactly this point: discriminative training does better on irregular textures, where the non-local similarity prior is weakened."),
 ("How does a Transformer recover NSS?",
  "By letting any position influence any other in one operation. Restormer does it indirectly — it attends over channels rather than pixels, so the attention map is \\(C\\times C\\) and every channel is computed from every pixel, encoding image-wide statistics at linear cost.")],
[("DnCNN loses on Barbara because it was under-trained.",
  "It is a structural limitation, not a training one. A \\(35\\times35\\) receptive field physically cannot see a matching patch 200 pixels away.",
  "No amount of training fixes a receptive field that is too small. The fix required a different operator, which is what Part V is about.")],
hard=True))

A(Q("bm3d", "B", "Stage 3 → Part II → BM3D",
"Walk through BM3D, and say which part actually does the work.",
r"""BM3D (Dabov et al., IEEE TIP 2007) runs a grouping-and-shrinkage pipeline **twice**.

**Step 1 — basic estimate.** (a) For each reference block, find similar blocks by block-matching and stack them into a 3-D array, a *group*. (b) Apply a separable 3-D transform to the group, hard-threshold the coefficients, invert the transform, and return the estimates to their original positions. (c) Aggregate all overlapping block-wise estimates by weighted averaging.

**Step 2 — final estimate.** (a) Re-run block matching **inside the basic estimate**, which is cleaner, so the matching is more accurate. Form two groups: one from the noisy image, one from the basic estimate. (b) Wiener-filter the noisy group using the basic estimate's energy spectrum as the pilot. (c) Aggregate again.

The paper gives both motivations for the second pass explicitly: the basic estimate **improves the grouping**, and using it as the Wiener pilot is **much more effective and accurate than simple hard-thresholding** of the noisy spectrum.

The collaborative filtering step is
\[ \hat{Y}_S = T_{3D}^{-1}\big(\gamma(T_{3D}(Y_S))\big), \qquad
   \gamma(c) = c\cdot\mathbb{1}[\,|c| > \lambda_{3D}\sigma\,], \qquad T_{3D} = T_{2D}\otimes T_{1D} \]

**Which part does the work?** The grouping, not the transform. The paper's own ablation shows that varying \(T_{2D}\) and \(T_{1D}\) changes PSNR only modestly — even a transform whose basis elements are random apart from the DC loses just 0.1–0.4 dB — and concludes that *inter-fragment correlation appears as a much more important feature than intra-fragment correlation*. Consistently, the DST performs worst, which the authors attribute to its **lack of a DC basis element**: the DC along the stacking axis is what captures similarity between stacked blocks, recovering plain averaging as a special case.""",
"""Stacking a hundred near-identical patches creates a third axis along which the signal is almost constant and the noise is not. Almost all the denoising happens along that new axis — the clever transform is nearly incidental.""",
["block matching", "collaborative filtering", "hard thresholding", "Wiener pilot", "aggregation", "third-dimension sparsity"],
[("Why does BM3D need two steps at all?",
  "Because block matching on a noisy image is unreliable — you match noise as well as structure. The first pass produces a cleaner image to match on, and a cleaner spectrum to use as a Wiener pilot. Both improvements come from having *any* estimate, however imperfect."),
 ("What is the computational cost?",
  "Linear in image size, since all parameters are fixed. Cost per pixel is dominated by exhaustive-search block matching in a local neighbourhood plus the separable transforms. The Fast profile swaps exhaustive for predictive search. Measured in DnCNN's Table IV: 2.85 s for a \\(512\\times512\\) image on CPU."),
 ("How many parameters does BM3D have?",
  "Block size, search window, matching threshold, \\(\\lambda_{3D}\\), two transforms, and aggregation weights — all set by the authors, with different values above and below \\(\\sigma = 40\\). This is precisely the *several manually chosen parameters* DnCNN names as a drawback of the era.")],
[("BM3D works because the 3-D transform is especially good at representing image patches.",
  "The paper's ablation contradicts this: a near-random transform loses only a few tenths of a decibel.",
  "BM3D works because grouping creates sparsity along the stacking axis. The transform is a way to exploit that sparsity, not the source of it.")],
hard=True))

A(Q("wnnm", "B", "Stage 3 → Part II → WNNM",
"Explain WNNM: what is being minimised, why the weights are needed, and what it costs.",
r"""Stack the non-local similar patches to patch \(j\) as the columns of a matrix. Then
\[ Y_j = X_j + N_j, \qquad X_j \text{ low rank} \]
because near-copies make near-dependent columns. WNNM recovers \(X_j\) by
\[ \hat{X}_j = \arg\min_{X_j} \frac{1}{\sigma_n^2}\lVert Y_j - X_j\rVert_F^2 + \lVert X_j \rVert_{w,*},
\qquad \lVert X \rVert_{w,*} = \sum_i w_i\,\sigma_i(X) \]

**Why weights.** Standard nuclear-norm minimisation has a closed form — soft-threshold every singular value by the same \(\lambda\). The paper objects that this *treats each singular value equally*, ignoring that in denoising the singular values have physical meaning: **the larger ones carry the major image components and should be shrunk less**. So
\[ w_i = \frac{c\sqrt{n}}{\sigma_i(X_j) + \varepsilon}, \qquad \varepsilon = 10^{-16} \]
inversely proportional to the singular value: big components barely touched, small ones crushed.

**The circularity.** The weights depend on the unknown clean singular values. WNNM estimates them by assuming the noise energy is spread evenly across subspaces:
\[ \hat{\sigma}_i(X_j) = \sqrt{\max\!\big(\sigma_i^2(Y_j) - n\sigma_n^2,\ 0\big)} \]

**The theory.** Theorem 2 shows that when the weights are in *non-ascending* order the problem has a globally optimal solution by generalised soft-thresholding of the singular values, with classical singular value thresholding as the equal-weight special case. Denoising weights are *non-descending* — the opposite order — so a separate result shows an iterative algorithm reaches an analytical fixed point there.

**The cost.** An SVD per patch group, iterated, per image: **773.2 seconds** for one \(512\times512\) image, against BM3D's 2.85 s, and 2 536 s at \(1024\times1024\). Its effective patch size is \(361\times361\).""",
"""A stack of similar patches is nearly a rank-one matrix — one pattern repeated. The big singular values are the pattern; the small ones are noise. WNNM keeps the pattern and deletes the rest, weighting the decision by how big each component is.""",
["low-rank approximation", "nuclear norm", "singular value thresholding", "weighted norm", "non-convexity", "test-time cost"],
[("Why is the weighted nuclear norm not convex?",
  "The nuclear norm is convex because it is a sum of singular values with equal non-negative weights. Once weights differ and are chosen inversely to the singular values, the penalty depends on the matrix in a way that breaks convexity in general — hence the need for Theorem 2 to identify when a closed form survives."),
 ("What makes WNNM the classical peak?",
  "It combines the two strongest classical ideas — non-local grouping and a data-adaptive low-rank prior — and it beats BM3D at every noise level on BSD68 (31.37 / 28.83 / 25.87 vs 31.07 / 28.57 / 25.62). Nothing hand-designed did better afterwards."),
 ("Why does 773 seconds matter to the argument?",
  "It is the entire commercial case for the deep era, and it comes from DnCNN's own comparison table rather than from us. DnCNN-B does the same job in 0.060 s on GPU — about 12 900× faster, with the device difference stated.")],
[("WNNM is slow because SVD is slow.",
  "SVD on a small patch-group matrix is cheap. The cost is that it must be done for every group, and the whole thing iterated, for every image.",
  "The cost is architectural, not algorithmic: test-time optimisation means nothing is reused between images. That is bottleneck 1.")],
hard=False))

A(Q("tv", "B", "Stage 3 → Part II → Total variation",
"Why does total variation preserve edges when squared-gradient regularisation does not?",
r"""The ROF model (Rudin, Osher, Fatemi, 1992) is
\[ \hat{x} = \arg\min_x \tfrac{1}{2}\lVert y - x\rVert_2^2 + \lambda\lVert \nabla x\rVert_1,
\qquad \lVert\nabla x\rVert_1 = \sum_{i,j}\sqrt{(\partial_h x)^2 + (\partial_v x)^2} \]

Compare the costs. A Tikhonov prior \(\lVert\nabla x\rVert_2^2\) charges the **square** of a jump, so one edge of height 100 costs 10 000 while a hundred ripples of height 1 cost only 100 — the optimiser removes the edge and keeps the ripple. TV charges the jump itself, so an edge of height 100 costs 100 and a hundred ripples of height 1 also cost 100. **Edges become affordable**, and the penalty stops preferring to destroy them.

Two consequences follow:

- **Staircasing.** The minimiser of a TV-regularised objective is piecewise constant. Edges are preserved beautifully and smooth gradients turn into visible flat plateaus. That is why TV is not a general-purpose photographic denoiser.
- **Non-differentiability.** \(\lVert\cdot\rVert_1\) has no gradient at zero, so plain gradient descent does not apply. Chambolle's 2004 dual projection algorithm solves it by iterating on a dual variable to a fixed tolerance — which, in code, is a `while` loop with a tolerance and an iteration cap, run once per image.""",
r"""The \(\ell_2\) penalty is like a fine that grows with the square of the offence, so one big jump is unaffordable. The \(\ell_1\) penalty charges per unit, so one big jump costs the same as the same total amount of small wobbles — and the optimiser has no reason to prefer wobbles.""",
["total variation", "L1 vs L2 penalties", "sparsity of gradients", "staircasing artefact", "Chambolle projection"],
[("Why does \\(\\ell_1\\) promote sparsity in general?",
  "Its level sets have corners on the coordinate axes. When you intersect a data-fidelity ball with an \\(\\ell_1\\) ball, the contact point tends to land on a corner, where some coordinates are exactly zero. The \\(\\ell_2\\) ball is round and has no corners, so it shrinks everything without zeroing anything."),
 ("Where is TV in the project's code analysis?",
  "`scikit-image 0.26.0`, `denoise_tv_chambolle`. It is the classical exhibit precisely because it is small: the `weight` argument is \\(\\lambda\\), one line of arithmetic is \\(\\Phi\\), the `while` loop is the test-time optimisation, and the `break` on relative energy change is the stopping criterion."),
 ("What would you use TV for today?",
  "Not photographic denoising. It remains useful where the piecewise-constant assumption is actually correct — some medical and scientific imaging — and as a regulariser inside larger inverse-problem solvers.")],
[("TV preserves edges because it detects them.",
  "There is no edge detection anywhere in TV. It has no notion of where edges are.",
  "TV preserves edges because of how it *prices* them. An \\(\\ell_1\\) penalty on the gradient is indifferent between one large jump and many small ones, so the optimiser is not pushed to flatten the jump.")],
hard=False))

# ═══════════════ 3. DnCNN ═══════════════
A(Q("residual", "B", "Stage 3 → Part III → DnCNN residual learning",
"Why does DnCNN predict the noise instead of the clean image?",
r"""DnCNN learns \(\mathcal{R}(y) \approx v\) and recovers \(x = y - \mathcal{R}(y)\). The loss is
\[ \ell(\Theta) = \frac{1}{2N}\sum_{i=1}^{N}\big\lVert \mathcal{R}(y_i;\Theta) - (y_i - x_i)\big\rVert_F^2 \]
so the target is \((y_i - x_i)\), the actual noise. The loss never looks at the clean image directly.

The justification is two steps, both from the paper:

1. **From ResNet:** *when the original mapping is more like an identity mapping, the residual mapping will be much easier to optimize.*
2. **The observation that closes it:** the noisy observation \(y\) *is much more like the latent clean image \(x\) than it is like the residual image \(v\)*, especially at low noise.

Put together: learning \(F(y)=x\) would force the network toward an identity transform. A stack of convolutions with ReLUs has no natural way to express "copy the input unchanged" — seventeen layers would all have to conspire into an identity, which is a narrow and awkward point in parameter space. Learning \(\mathcal{R}(y)=v\) instead places the "do nothing" solution at **zero**, which is trivially reachable by driving the weights toward zero. Residual learning relocates the easy solution from the hard point to the easy point.

Two precision points for a defence. **DnCNN is not ResNet**: the paper states it *employs a single residual unit to predict the residual image*, one global skip rather than many identity shortcuts. And the paper hedges its own priority — residual prediction had been used in super-resolution and demosaicking, but *to the best of our knowledge there is no work which directly predicts the residual image for denoising*.""",
"""It is easier to learn "what is wrong with this photo" than "what this photo should look like". The first is small and mostly zero; the second is the whole image.""",
["residual learning", "identity mapping difficulty", "single global skip", "loss target", "optimisation landscape"],
[("Does residual learning change what the network *can* represent?",
  "No — the function classes are equivalent, since \\(x = y - v\\) is an invertible reparameterisation. It changes how easy the target is to *reach* by gradient descent. This is an optimisation argument, not an expressivity one."),
 ("What does the identity-is-hard explanation rest on?",
  "The ResNet argument is from the paper; the specific explanation of *why* identity is awkward for a ReLU-convolution stack is an interpretation, not a quoted claim. Say so if pressed — it is the explanation that satisfies the question, but it should be labelled as reasoning rather than citation."),
 ("Where does residual learning show up later in the project?",
  "In ZS-N2N, 2023, six years later: the network predicts noise and the estimate is \\(\\hat{x} = y - f_{\\hat\\theta}(y)\\), in a 20 000-parameter zero-shot method. The design choice outlived the architecture completely.")],
[("Residual learning is the same thing as a ResNet skip connection.",
  "ResNet uses many identity shortcuts inside the network; DnCNN uses one skip across the entire network, applied to the input and output.",
  "DnCNN has a single global residual unit. The paper says so explicitly, and confusing the two is a common slip."),
 ("The network outputs the clean image and the subtraction is internal detail.",
  "The paper's network outputs \\(\\hat v\\) and the subtraction happens outside. The KAIR reference implementation folds it into `forward`, which is where the confusion comes from.",
  "The residual mapping is what the weights learn either way — only the module boundary moves. Be able to state which convention a given codebase uses.")],
hard=True))

A(Q("rlbn", "B", "Stage 3 → Part III → RL/BN synergy",
"Explain the residual-learning / batch-normalisation synergy in both directions.",
r"""The paper's claim is two-way: *the integration of residual learning and batch normalization can result in fast and stable training and better denoising performance*, and the two *benefit from each other*.

**Direction 1 — residual learning benefits from BN.** The easy half. Batch normalisation alleviates internal covariate shift: as training updates early layers, the distribution arriving at later layers keeps moving, so those layers chase a target that will not hold still. BN normalises activations across the mini-batch before the nonlinearity, then applies a learned scale and shift — two parameters per activation. Fig. 2 of the paper shows residual learning *without* BN converging quickly but settling below residual learning *with* BN.

**Direction 2 — BN benefits from residual learning.** The surprising half, and the one examiners ask about. *Without residual learning, batch normalization even has a certain adverse effect on convergence.* BN alone is worse than nothing.

The mechanism the paper gives: a mini-batch is only 128 patches. Without residual learning, the input intensity and convolutional features are correlated with their neighbours, so the distribution of each layer's inputs depends on **the content of the images in that particular batch** — the batch statistics are not estimating anything stable. With residual learning, DnCNN *implicitly removes the latent clean image in the hidden layers*, which makes layer inputs **Gaussian-like distributed, less correlated, and less related to image content**. That is exactly the regime BN's batch statistics assume.

The paper adds a deeper reason specific to this task: *the residual image and batch normalization are both associated with the Gaussian distribution*, so it is very likely they benefit from each other.

Finally, the paper rules out the obvious confound: both SGD and Adam give the best results with RL+BN, so it is *the integration of residual learning and batch normalization, rather than the optimization algorithm*, that produces the win.""",
"""Batch norm needs the things it is normalising to look like samples from one stable distribution. Subtracting the image out of the hidden layers is what makes them look that way.""",
["internal covariate shift", "batch statistics", "mini-batch content dependence", "Gaussian-like activations", "controlled ablation"],
[("Would this hold for a task where the residual is not Gaussian?",
  "The paper guards its own claim in a footnote, noting this does not mean DnCNN cannot handle other tasks well. DnCNN-3 is the evidence: it works on super-resolution and JPEG deblocking, where the residual is clearly not AWGN."),
 ("Why does batch size matter here?",
  "BN estimates mean and variance from the batch. With 128 patches, those estimates are noisy and content-dependent unless the activations are already roughly content-independent. That is precisely what residual learning supplies."),
 ("Would LayerNorm avoid the problem?",
  "It would avoid the batch-content dependence, since it normalises per sample rather than across the batch. Interestingly NAFNet finds LayerNorm to be the single largest gain in its whole ablation — +0.44 dB on SIDD — because it stabilises training at a ten-times larger learning rate.")],
[("Batch normalisation always helps deep networks.",
  "DnCNN's own ablation shows BN alone hurting convergence on this task.",
  "BN helps when its distributional assumptions hold. Residual learning is what makes them hold here, which is why the paper frames it as a synergy rather than as two independent improvements.")],
hard=True))

A(Q("depth17", "B", "Stage 3 → Part III → Depth and receptive field",
"Why is DnCNN 17 layers deep? Derive the number.",
r"""Because there is no pooling and all filters are \(3\times3\), each layer extends the receptive field by one pixel in every direction. For depth \(d\) the receptive field is exactly
\[ (2d+1)\times(2d+1) \]
so \(d = 17\) gives \(35\times35\).

The number 35 was not guessed. The authors tabulated the **effective patch size** of every competitor at \(\sigma = 25\):

| Method | Effective patch size |
|---|---|
| EPLL | \(36\times36\) |
| **DnCNN-S** | \(\mathbf{35\times35}\) |
| MLP | \(47\times47\) |
| BM3D | \(49\times49\) |
| CSF / TNRD | \(61\times61\) |
| WNNM | \(361\times361\) |

and posed the design question: *it is interesting to verify whether DnCNN with a receptive field size similar to EPLL can compete against the leading denoising methods.* So they matched the **smallest** effective patch size in the field. For other general denoising tasks they used depth 20, giving \(41\times41\), because *high noise level usually requires larger effective patch size*.

The point worth making in a defence is the comparison: DnCNN wins with a receptive field one tenth the linear extent of WNNM's. **It is not seeing more; it is understanding better.** And that same fact is why it loses on Barbara, and why Part V exists.""",
r"""Each \(3\times3\) layer lets a pixel peek one step further out. Seventeen layers gets you seventeen steps in every direction, which is 35 pixels across — deliberately chosen to be the smallest window any competitor used.""",
["receptive field arithmetic", "effective patch size", "no pooling", "design justification", "depth vs reach"],
[("Why not just use a much deeper network?",
  "Receptive field grows only *linearly* with depth, so reaching WNNM's \\(361\\times361\\) would need about 180 layers — with the parameter count, memory and optimisation difficulty that implies. That inefficiency is bottleneck 3, and it is why the fix had to be a different operator rather than more layers."),
 ("How would pooling change the arithmetic?",
  "Pooling multiplies the receptive field rather than adding to it, so a U-Net reaches far more cheaply. DnCNN avoids it because denoising must emit one clean pixel per input pixel and pooling discards spatial resolution. Later architectures reintroduce it with skip connections to restore detail."),
 ("What is 'effective patch size' for a non-network method?",
  "The spatial extent of the region that can influence one output pixel. For BM3D it is the \\(25\\times25\\) non-local search window applied twice, giving \\(49\\times49\\); for MLP it is a \\(39\\times39\\) patch followed by a \\(9\\times9\\) averaging filter, giving \\(47\\times47\\).")],
[("Deeper is always better for denoising.",
  "Depth buys receptive field linearly and at real cost. DnCNN deliberately chose the *smallest* competitive receptive field and won anyway.",
  "What matters is whether the receptive field matches the spatial extent of the structure you need to exploit. Beyond that, depth adds cost without adding reach.")],
hard=False))

A(Q("dncnn3", "A", "Stage 3 → Part III → DnCNN-3",
"The paper is titled 'Beyond a Gaussian Denoiser'. What is beyond, and what justifies it?",
r"""Reinterpret \(v\), and the same network, loss and training procedure solve two problems that are not denoising:

- **Denoising:** \(v\) is AWGN, \(\sigma \in [0,55]\).
- **Super-resolution:** let \(v\) be *the difference between a ground-truth high-resolution image and the bicubic upsampling of its low-resolution version*. Scales \(\times2, \times3, \times4\).
- **JPEG deblocking:** let \(v\) be *the difference between the original image and its compressed version*. Quality factors 5–99.

The paper's conclusion is that super-resolution and JPEG deblocking *are special cases of a 'general' image denoising problem*.

**The justification is derived, not asserted.** From the connection with one-stage TNRD, the residual estimate remains valid whenever *the derivative of the data-fidelity term vanishes at zero* — a condition that holds for *many types of noise distributions, e.g. the generalized Gaussian distribution*. The authors then state it is natural to assume it also holds for SISR and JPEG noise.

**Results.** BSD68 \(\sigma{=}25\): BM3D 28.57, TNRD 28.92, **DnCNN-3 29.02**. Set5 \(\times3\): TNRD 33.18, VDSR 33.67, **DnCNN-3 33.75**. Classic5 QF10: AR-CNN 29.03, TNRD 29.28, **DnCNN-3 29.40**.

Reproduce the paper's hedge: *to the best of our knowledge* no existing method had been reported for handling these three tasks with a single model. Overstating priority is exactly what a defence punishes.""",
"""If you define "noise" as "whatever went wrong", then downsampling and JPEG compression are both kinds of noise, and a network that learns to predict what went wrong can undo all three.""",
["task generalisation", "residual reinterpretation", "generalized Gaussian condition", "single model, three tasks"],
[("Is the residual really zero-mean for JPEG artefacts?",
  "Not obviously, and the paper does not claim it is. The stated condition is that the derivative of the data-fidelity term vanishes at zero, which is weaker. The empirical results are the real evidence."),
 ("Why does this matter for the project's narrative?",
  "It reframes denoising from a task into a *template* for inverse problems. That is one of the strongest arguments for why studying denoising is worthwhile — and it anticipates the plug-and-play prior result SCUNet cites."),
 ("What is the cost of one model for three tasks?",
  "A slightly larger training set (91 images plus 200 BSD, 128×8 000 patches), depth 20 rather than 17, and three days of training rather than six hours. Accuracy per task is not sacrificed — it beats specialist baselines on all three.")],
[],
hard=False))
