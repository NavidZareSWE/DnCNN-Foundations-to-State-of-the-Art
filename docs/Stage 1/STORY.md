# From Foundations to State-of-the-Art: A Cohesive Evolutionary Narrative for Image Denoising

**Stage 1 — Literature Review Pitch**
Digital Image Processing Final Project · Supervisor: Prof. Zohreh Azimifar
Defence date: 11 August 2026

---

## Preface: how this document is grounded

Every factual claim below is traceable to one of two places: the eleven Category A PDFs held in the project repository, or the `Stage_1_Presentation_Guidelines.pdf`. Where a fact required by the guidelines could not be established from those documents, it was verified against publisher or proceedings records and the source is named inline. Citation counts, which no PDF contains, are Google Scholar figures with the date they were checked. Section 7 collects the verification status in one place.

The guidelines define five mandatory sections. This narrative addresses all five in order, and the accompanying deck (`SLIDE.html`) presents the same material in the same sequence.

---

## 1. Topic Definition and the Core Problem

### 1.1 The topic

The topic of this project is **image denoising**: the recovery of a clean image from a noise-corrupted observation of it. Denoising is selected not merely as a representative low-level vision task but because the literature treats it as foundational. SCUNet describes denoising as perhaps the most fundamental image restoration problem, and gives three reasons for that status: it serves as a testbed for evaluating the effectiveness of different image priors and optimisation algorithms, it can be plugged into larger restoration pipelines, and it underpins downstream work more broadly.

The anchor paper for the project is **DnCNN** (Zhang, Zuo, Chen, Meng and Zhang), which states the problem with unusual economy: the goal of image denoising is to recover a clean image $x$ from a noisy observation $y$ following the degradation model

$$y = x + v,$$

where the common assumption is that $v$ is additive white Gaussian noise (AWGN) with standard deviation $\sigma$.

### 1.2 Why this is mathematically hard

Three difficulties follow directly from that one-line model, and each is documented in the selected papers.

**The problem is ill-posed.** The equation $y = x + v$ has one observation and two unknowns per pixel. Infinitely many $(x, v)$ pairs explain any given $y$. Restormer states the point generally for restoration: because of its ill-posed nature it is a highly challenging problem that usually requires strong image priors for effective restoration. Every method in this review is therefore best understood as an answer to a single question — *where does the prior come from?* That question is the spine of the entire narrative.

**A prior must be supplied, and historically it was supplied by hand.** DnCNN frames this from a Bayesian viewpoint: when the likelihood is known, image prior modelling plays a central role, and it lists the families of priors that had been exploited over the preceding decades — non-local self-similarity models, sparse models, gradient models, and Markov random field models. The classical solution shape is a variational objective in which a hand-designed regulariser $\Phi$ encodes the prior,

$$\hat{x} = \arg\min_{x} \tfrac{1}{2}\lVert y - x \rVert_2^2 + \lambda\,\Phi(x),$$

solved anew, per image, at test time.

**Noise removal and detail preservation are in direct tension.** BM3D names this tension precisely. Its stated achievement is that collaborative filtering reveals even the finest details shared by grouped blocks while at the same time preserving the essential unique features of each individual block. That sentence only needs writing because the naive alternative — averaging — destroys exactly the fine structure that makes an image worth denoising.

### 1.3 Why it still matters

Two of the eleven papers establish continued relevance independently of academic benchmarks. ZS-N2N motivates its work by noting that reconstructing fine detail is especially important for medical images, where fine details are necessary for accurate diagnosis. SCUNet frames the open problem in engineering terms: existing methods mostly rely on simple noise assumptions such as AWGN, JPEG compression noise and camera sensor noise, and a general-purpose blind denoising method for real images remains unsolved. Published in 2023, that is the clearest statement in the roster that the problem is live rather than historical.

---

## 2. The Visual Evolutionary Timeline

The guidelines require a timeline that explicitly shows the transitions Classical DIP → Early Deep Learning → Modern SOTA, and that indicates on the timeline *why* the field moved between eras. The narrative below supplies the bottleneck at each hinge. Each bottleneck is stated by the paper that resolved it, so the chain is evidenced rather than asserted.

### Era I — Classical DIP: the prior is written by a human (2007–2014)

The era is represented by **BM3D** (2007) and **WNNM** (2014). Both exploit *non-local self-similarity*: the observation that a natural image repeats itself, so noise, being independent between occurrences, can be cancelled by treating repeated structures jointly.

BM3D operationalises this in three named, sequential steps — 3-D transformation of a group, shrinkage of the transform spectrum, and inverse 3-D transformation — followed by an aggregation step that combines the many overlapping per-pixel estimates, and then a second pass using a collaborative Wiener filter. WNNM reaches the same prior by a different route: it observes that the matrix formed by non-local similar patches in a natural image is of low rank, and that standard nuclear norm minimisation regularises every singular value equally, which restricts its flexibility in problems such as denoising where the singular values have clear physical meanings and should be treated differently. It therefore assigns different weights to different singular values,

$$\lVert X \rVert_{w,*} = \sum_i w_i\,\sigma_i(X),$$

and reports that this outperforms state-of-the-art algorithms such as BM3D on both quantitative measures and visual perception quality.

> **Bottleneck that ended Era I.** Two limitations, both stated by papers in this roster. First, **cost at test time**: TNRD observes that most state-of-the-art techniques of that period concentrated on utmost restoration quality with little consideration of computational efficiency, despite efficiency being critical for real applications. Every image requires solving an optimisation problem from scratch. Second, **manual specification**: the prior, its parameters, and its thresholds are chosen by the designer, so the method cannot improve by being shown data.

### Era II — The bridge: the prior is learned, but the structure is still hand-designed (2016)

**TNRD** is the hinge paper of this review, and it is included precisely because it is neither classical nor fully modern. It keeps the mathematical scaffolding of nonlinear diffusion but learns its contents: in contrast to previous nonlinear diffusion models, *all* the parameters — the linear filters and the influence functions — are simultaneously learned from training data through a loss-based approach. The result preserves the structural simplicity of diffusion models, takes only a small number of diffusion steps, and is well suited to parallel computation on GPUs, which makes inference extremely fast.

TNRD is the moment the field discovers that a fixed, shallow, feed-forward computation trained discriminatively can match an expensive iterative optimiser. That discovery is what makes DnCNN thinkable.

### Era III — Early deep learning: the prior disappears into the weights (2017)

**DnCNN** removes the remaining hand-designed structure. Its contributions, in its own framing, are to bring very deep architecture, modern learning algorithms and modern regularisation into denoising, using residual learning and batch normalisation to speed up training and boost performance. Rather than predicting the clean image, the network predicts the noise, so that

$$\hat{x} = y - \mathcal{R}(y),$$

where $\mathcal{R}$ is the learned residual mapping. DnCNN reports a depth of 17 with a corresponding receptive field of $35 \times 35$.

Two consequences matter for the narrative. First, DnCNN handles **blind** Gaussian denoising — a single model for unknown noise level — where earlier discriminative models trained a specific model per noise level. Second, because residual learning causes the network to implicitly remove the latent clean image in the hidden layers, a single DnCNN can be trained to handle several tasks: Gaussian denoising, single image super-resolution, and JPEG deblocking. Generality arrives as a side effect of the training scheme, not as an architectural feature.

> **Bottleneck that ended Era III (first branch — data).** DnCNN and its contemporaries are supervised: they need matched noisy/clean pairs. Noise2Noise identifies the cost directly — obtaining clean training targets is often difficult or tedious, giving the example that a noise-free photograph requires a long exposure. In medicine and microscopy the clean target may not exist at all.

> **Bottleneck that ended Era III (second branch — architecture).** Restormer names the two structural weaknesses of convolution: convolution provides local connectivity and translation equivariance, which brings efficiency and generalisation, but also causes a limited receptive field and an inability to adapt to input content. MambaIR states the same dilemma as a trade-off: existing restoration backbones face a dilemma between global receptive fields and efficient computation.

### Era IV — Modern SOTA, branch A: escaping the data requirement (2018 → 2023)

This branch is a clean three-step argument, and each step is stated as a strict weakening of the previous step's requirement.

**Noise2Noise** (2018) shows that it is possible to learn to restore images by looking only at corrupted examples, at performance matching and sometimes exceeding training on clean data, without explicit image priors or likelihood models of the corruption. It still requires *pairs* of independent noisy observations of the same scene.

**Noise2Void** (2019) removes the pair. It describes itself as taking the idea one step further: it requires neither noisy image pairs nor clean targets, and can therefore be trained directly on the body of data to be denoised, which makes it applicable where other methods cannot be used — the paper highlights biomedical data, where acquiring training targets, clean or noisy, is frequently impossible. The mechanism is a *blind-spot network*: the receptive field is made to exclude the centre pixel, so the network cannot solve the task by copying the input. The paper is honest about the cost: N2V cannot be expected to outperform methods with more information available during training, and its performance drops, though in moderation.

**Zero-Shot Noise2Noise** (2023) removes the dataset entirely. It demonstrates that a simple 2-layer network, without any training data or knowledge of the noise distribution, enables high-quality denoising at low computational cost. It states the drawbacks it is answering: dataset collection is expensive and time-consuming, and a network trained on a dataset suffers a performance drop when test images come from a different distribution. Its only assumption is pixel-wise independence of the noise, and it explicitly positions itself as motivated by Noise2Noise and Neighbor2Neighbor — an in-roster citation chain that lets the narrative close a loop rather than merely list papers.

### Era IV — Modern SOTA, branch B: escaping the architectural limits of convolution (2022 → 2024)

**Restormer** (2022) brings the Transformer to high-resolution restoration. The problem it solves is that Transformer complexity grows quadratically with spatial resolution, making it infeasible for most restoration tasks. Its answer is to redesign the building blocks rather than shrink the input: a **multi-Dconv head transposed attention (MDTA)** module capable of aggregating local and non-local pixel interactions efficiently enough for high-resolution images, and a **gated-Dconv feed-forward network (GDFN)** that introduces a gating mechanism to perform controlled feature transformation, suppressing less informative features so that only useful information passes further through the hierarchy. Restormer is an encoder–decoder Transformer for multi-scale local–global representation learning that does not disintegrate the image into local windows, thereby exploiting distant image context.

**NAFNet** (2022) is the counter-argument, and including it is what turns the roster from a progress narrative into a critical one. It observes that system complexity of SOTA methods is increasing in a way that may hinder convenient analysis and comparison, decomposes that complexity into inter-block and intra-block components, and then simplifies aggressively — revealing that nonlinear activation functions such as Sigmoid, ReLU, GELU and Softmax are not necessary and can be replaced by multiplication or removed, yielding a Nonlinear Activation Free Network. It reports 40.30 dB PSNR on SIDD for denoising, exceeding the previous SOTA by 0.28 dB with less than half the computational cost, and 33.69 dB on GoPro for deblurring, exceeding the previous SOTA by 0.38 dB with only 8.4% of its computational cost.

**SCUNet** (2023) refuses the choice between convolution and attention and refuses the choice between architecture and data. Architecturally it proposes a swin-conv block that incorporates the local modelling ability of the residual convolutional layer and the non-local modelling ability of the swin transformer block, plugged into a UNet. Equally important is its second contribution — a practical noise degradation model covering Gaussian, Poisson, speckle, JPEG compression and processed camera sensor noises, plus resizing, and involving a random shuffle strategy and a double degradation strategy. Its finding is that the architecture achieves state-of-the-art performance *and* the new degradation model significantly improves practicability. This is the paper that reconnects the whole review to the real world.

**MambaIR** (2024) is the newest source and marks the current frontier. It applies the Selective Structured State Space Model — specifically Mamba — which shows great potential for long-range dependency modelling with **linear** complexity, offering a way to resolve the global-receptive-field-versus-efficiency dilemma. It identifies two problems standard Mamba has in low-level vision, *local pixel forgetting* and *channel redundancy*, and introduces local enhancement and channel attention to address them. It reports outperforming SwinIR by up to 0.45 dB on image super-resolution at similar computational cost but with a global receptive field.

### 2.1 The timeline in one sentence

The prior moves steadily out of human hands: **written by a human** (BM3D, WNNM) → **structured by a human but fitted to data** (TNRD) → **learned entirely from paired data** (DnCNN) → **learned without clean data** (N2N), **without pairs** (N2V), **without any data** (ZS-N2N) → and, in parallel, the *mechanism* that carries the prior changes from convolution to attention (Restormer), to deliberately simplified convolution (NAFNet), to a hybrid (SCUNet), to state-space models (MambaIR).

---

## 3. Source Quota and the 70/30 Distribution

The guidelines require a master list of 10+ distinct sources, with Category A at a minimum of 70% and Category B capped at 30%.

| | Count | Share | Requirement | Status |
|---|---|---|---|---|
| Category A — peer-reviewed papers | 11 | 78.6% | ≥ 70% | Satisfied |
| Category B — auxiliary materials | 3 | 21.4% | ≤ 30% | Satisfied |
| **Total** | **14** | | ≥ 10 | Satisfied |

The guidelines further require that Category A include *both* older milestone papers *and* recent SOTA from 2022–present. The roster contains six pre-2022 milestones (BM3D, WNNM, TNRD, DnCNN, Noise2Noise, Noise2Void) and five 2022-or-later papers (Restormer, NAFNet, ZS-N2N, SCUNet, MambaIR). Both halves of the requirement are met with margin.

## 4. Paper-by-Paper Breakdown (the "Rigor" check)

For each Category A paper the guidelines require metadata and credibility, technical specifications, and evolutionary context. Metadata is reported below with its source of verification. Citation counts are Google Scholar figures checked on 9 August 2026 and are reported inline with each paper.

---

### A1 · Image Denoising by Sparse 3-D Transform-Domain Collaborative Filtering (BM3D)

**Authors** Kostadin Dabov, Alessandro Foi, Vladimir Katkovnik, Karen Egiazarian
**Institution** Institute of Signal Processing, Tampere University of Technology, Finland *(stated in the PDF's author footnote)*
**Venue & year** IEEE Transactions on Image Processing, 16(8), pp. 2080–2095, August 2007 *(printed in the PDF page header; corroborated by dblp)*
**Citations** 11,976 *(Google Scholar, checked 9 August 2026)*

**Sub-problem.** Exploiting non-local self-similarity to sparsify image content enough that a shrinkage in transform domain separates signal from noise.

**Model / architecture.** Not a network. A four-stage algorithm — grouping by block matching, collaborative filtering by 3-D transform and shrinkage, inverse transform, and aggregation of overlapping estimates by weighted averaging — executed twice, the second pass replacing hard thresholding with a collaborative Wiener filter that uses the first pass as an oracle.

**Datasets.** A set of standard grayscale test images, with a separate colour extension (C-BM3D). No training set exists, because nothing is trained.

**Value then vs. now.** In 2007 it defined state of the art. Today it is the reference baseline against which learned methods are measured: SCUNet, published sixteen years later, still lists BM3D-class methods among the comparisons that matter.

**Relation to the roster.** It is the *thing to beat*. WNNM's abstract claims to outperform state-of-the-art algorithms such as BM3D by name; the entire learned-prior line exists because BM3D's hand-designed prior, however good, could not be improved by data.

---

### A2 · Weighted Nuclear Norm Minimization with Application to Image Denoising (WNNM)

**Authors** Shuhang Gu, Lei Zhang, Wangmeng Zuo, Xiangchu Feng
**Institutions** Department of Computing, The Hong Kong Polytechnic University; School of Computer Science and Technology, Harbin Institute of Technology; Department of Applied Mathematics, Xidian University *(all stated on the PDF title page)*
**Venue & year** CVPR 2014, pp. 2862–2869, DOI 10.1109/CVPR.2014.366 *(the PDF does not print its venue; verified against independent proceedings records — this resolves a flag raised during source selection)*
**Citations** 2,960 *(Google Scholar, checked 9 August 2026)*

**Sub-problem.** Standard nuclear norm minimisation regularises every singular value equally in pursuit of convexity, which restricts its flexibility for problems such as denoising where singular values carry distinct physical meaning.

**Model / architecture.** An optimisation method, not a network: weighted nuclear norm minimisation applied to matrices of non-local similar patches, with the solution analysed under different weighting conditions.

**Datasets.** Twenty widely used test images *(stated in the paper)*.

**Value then vs. now.** It is the strongest classical result in the roster and remains a standard classical baseline. It is a stepping stone rather than a live method.

**Relation to the roster.** It shares BM3D's non-local self-similarity prior but reaches it through low-rank matrix approximation rather than transform-domain sparsity — demonstrating that the *prior*, not the machinery, was the classical era's real content. Its cost is what motivates TNRD's efficiency argument.

---

### A3 · Trainable Nonlinear Reaction Diffusion (TNRD)

**Authors** Yunjin Chen, Thomas Pock
**Institution** Institute for Computer Graphics and Vision, Graz University of Technology, Austria; Pock additionally affiliated with Digital Safety *(stated in the PDF footnote)*
**Venue & year** IEEE Transactions on Pattern Analysis and Machine Intelligence. **Note a genuine discrepancy:** the PDF page header reads "VOL. XX, NO. XX, 2016" and the arXiv stamp reads 20 Aug 2016, while citing papers give TPAMI 39(6), pp. 1256–1272, 2017. Both are correct — 2016 acceptance, 2017 issue. Cite as *TPAMI, 39(6):1256–1272, 2017* and be ready to explain the discrepancy if challenged.
**Citations** 1,626 *(Google Scholar, checked 9 August 2026)*

**Sub-problem.** Restoration quality had been pursued with little regard for computational efficiency, despite efficiency being critical for real applications.

**Model / architecture.** A dynamic nonlinear reaction–diffusion model with time-dependent parameters, in which the linear filters and the influence functions are all learned simultaneously from training data by a loss-based approach.

**Datasets.** A training set of 400 images at 180 × 180 for denoising; Set5 and Set14 for super-resolution *(stated in the paper)*.

**Value then vs. now.** Historically pivotal, practically superseded. Its importance is conceptual: it proved a shallow trainable feed-forward model could rival iterative optimisation.

**Relation to the roster.** This is the bridge. It is the first paper in the list where the prior is *learned*, while the computational structure remains hand-designed. DnCNN then discards the diffusion scaffolding and keeps only the learning.

---

### A4 · Beyond a Gaussian Denoiser: Residual Learning of Deep CNN for Image Denoising (DnCNN) — **anchor paper**

**Authors** Kai Zhang, Wangmeng Zuo, Yunjin Chen, Deyu Meng, Lei Zhang
**Institutions** Harbin Institute of Technology; The Hong Kong Polytechnic University; Institute for Computer Graphics and Vision, Graz University of Technology; Xi'an Jiaotong University *(first three stated in the PDF footnote; Deyu Meng's XJTU affiliation corroborated by the university's publication record)*
**Venue & year** IEEE Transactions on Image Processing, 26(7), pp. 3142–3155, 2017, DOI 10.1109/TIP.2017.2662206 *(the arXiv PDF does not print this; verified against publisher and institutional records)*
**Citations** 11,674 *(Google Scholar, checked 9 August 2026)*

**Sub-problem.** Existing discriminative denoisers trained a separate model per noise level. DnCNN targets *blind* Gaussian denoising with a single model.

**Model / architecture.** A deep feed-forward CNN combining residual learning with batch normalisation, predicting the noise rather than the image. Depth 17 with a $35 \times 35$ receptive field *(stated in the paper)*.

**Datasets.** BSD68 for testing, Set12 as the 12 test images, plus Urban100, Set5 and Set14 for super-resolution and Classic5 and LIVE1 for JPEG deblocking *(all named in the paper)*.

**Value then vs. now.** It is the paper that established residual learning plus batch normalisation as the default denoising recipe, and it remains a universal baseline — every modern paper in this roster still reports against DnCNN or its descendants. As a *deployed* method it has been superseded, and it should be presented that way.

**Relation to the roster.** It is the hinge of the whole review. It resolves TNRD's remaining hand-design; it is the supervised method whose data requirement N2N, N2V and ZS-N2N successively dismantle; and it is the convolutional method whose receptive-field limits Restormer and MambaIR are explicitly written against.

---

### A5 · Noise2Noise: Learning Image Restoration without Clean Data

**Authors** Jaakko Lehtinen, Jacob Munkberg, Jon Hasselgren, Samuli Laine, Tero Karras, Miika Aittala, Timo Aila
**Institutions** NVIDIA; Aalto University; MIT CSAIL *(stated on the PDF title page)*
**Venue & year** Proceedings of the 35th International Conference on Machine Learning (ICML), Stockholm, PMLR 80, 2018 *(printed in the PDF's own footer)*
**Citations** 3,064 *(Google Scholar, checked 9 August 2026)*

**Sub-problem.** Clean training targets are difficult or tedious to obtain — a noise-free photograph requires a long exposure.

**Model / architecture.** A training paradigm rather than an architecture. The empirical risk minimised is

$$\arg\min_{\theta} \sum_i L\big(f_\theta(\hat{x}_i),\, y_i\big),$$

with the paper's insight being that $y_i$ may itself be a noisy observation.

**Datasets.** Kodak and Set14 among the image benchmarks, with ImageNet-derived training data; also Monte Carlo rendered images and undersampled MRI scans *(named in the paper)*.

**Value then vs. now.** Conceptually foundational and still actively built upon — ZS-N2N in this same roster states it is motivated by Noise2Noise.

**Relation to the roster.** It is the first break from DnCNN's supervision. It is strictly stronger than DnCNN in data requirements and strictly weaker than Noise2Void.

---

### A6 · Noise2Void — Learning Denoising from Single Noisy Images

**Authors** Alexander Krull, Tim-Oliver Buchholz, Florian Jug
**Institution** MPI-CBG / PKS (CSBD), Dresden, Germany *(stated on the PDF title page)*
**Venue & year** CVPR 2019 *(the PDF does not print its venue; verified against independent proceedings records)*
**Citations** 2,075 *(Google Scholar, checked 9 August 2026)*

**Sub-problem.** Even noisy *pairs* are usually unavailable, particularly in biomedical imaging where acquiring any training target is frequently impossible.

**Model / architecture.** A training scheme built on a **blind-spot network** whose receptive field excludes the centre pixel, preventing the identity solution.

**Datasets.** BSD68 among the evaluation sets *(named in the paper)*.

**Value then vs. now.** Still in active use in microscopy and biomedical imaging, which is precisely the domain it was designed for.

**Relation to the roster.** It removes the one requirement Noise2Noise retained. Its own abstract positions it explicitly as taking the N2N idea one step further, which makes the N2N → N2V → ZS-N2N chain evidenced by the papers rather than imposed by us.

---

### A7 · Restormer: Efficient Transformer for High-Resolution Image Restoration

**Authors** Syed Waqas Zamir, Aditya Arora, Salman Khan, Munawar Hayat, Fahad Shahbaz Khan, Ming-Hsuan Yang
**Institutions** Inception Institute of AI; Mohamed bin Zayed University of AI; Monash University; University of California, Merced; Yonsei University; Google Research *(stated on the PDF title page)*
**Venue & year** CVPR 2022, pp. 5728–5739 *(verified against the CVF Open Access proceedings record)*.
**Citations** 6,181 *(Google Scholar, checked 9 August 2026)*

**Sub-problem.** Transformer computational complexity grows quadratically with spatial resolution, making it infeasible for high-resolution restoration.

**Model / architecture.** An encoder–decoder Transformer built from two redesigned blocks: **MDTA** (multi-Dconv head transposed attention), which aggregates local and non-local pixel interactions efficiently, and **GDFN** (gated-Dconv feed-forward network), which gates feature transformation so only informative features propagate. It avoids splitting the image into local windows, preserving distant context.

**Datasets.** SIDD and DND for real denoising, Urban100, Kodak, Set12, McMaster and BSD68 for Gaussian denoising, GoPro and HIDE for deblurring, Rain100 for deraining *(named in the paper)*. The paper notes training only on SIDD and testing directly on DND — a generalisation result worth citing.

**Value then vs. now.** Current and heavily used; it is the canonical Transformer endpoint of the required narrative arc.

**Relation to the roster.** It answers the receptive-field limitation of DnCNN's convolutions directly and by name. NAFNet is its direct methodological rival, and SCUNet borrows the transformer half of its hybrid from this line of work.

---

### A8 · Simple Baselines for Image Restoration (NAFNet)

**Authors** Liangyu Chen, Xiaojie Chu, Xiangyu Zhang, Jian Sun *(the first two marked as equal contributors)*
**Institution** MEGVII Technology, Beijing, China *(stated on the PDF title page)*
**Venue & year** ECCV 2022, LNCS 13667, pp. 17–33, Springer *(the PDF is the arXiv version; verified against independent proceedings records)*.
**Citations** 2,318 *(Google Scholar, checked 9 August 2026)*

**Sub-problem.** Rising system complexity in SOTA methods hinders convenient analysis and comparison. The paper decomposes complexity into inter-block and intra-block components and attacks both.

**Model / architecture.** A Nonlinear Activation Free Network derived by progressive simplification of a plain UNet baseline, replacing nonlinear activations with multiplication via **SimpleGate**, alongside a simplified channel attention.

**Datasets.** SIDD for denoising and GoPro for deblurring, both used heavily throughout *(named in the paper)*.

**Value then vs. now.** Current, and unusually valuable pedagogically because its ablation-driven derivation is reproducible step by step.

**Relation to the roster.** It is the roster's dissenting voice. Where Restormer argues for more expressive blocks, NAFNet argues that much of the added complexity is unnecessary — and supports that with numbers. Presenting both prevents the narrative from becoming a naive "newer is better" story, which is exactly the failure mode the guidelines warn against.

---

### A9 · Zero-Shot Noise2Noise: Efficient Image Denoising without any Data (ZS-N2N)

**Authors** Youssef Mansour, Reinhard Heckel
**Institutions** School of Computation, Information and Technology, Technical University of Munich; Munich Center for Machine Learning; Department of Electrical and Computer Engineering, Rice University *(stated on the PDF title page)*
**Venue & year** CVPR 2023, pp. 14018–14027, DOI 10.1109/CVPR52729.2023.01347 *(verified against the CVF Open Access proceedings record)*.
**Citations** 266 *(Google Scholar, checked 9 August 2026)*

**Sub-problem.** Existing dataset-free methods are either computationally expensive, require a noise model, or produce inadequate image quality.

**Model / architecture.** A simple two-layer network trained per image, requiring no training data and no knowledge of the noise distribution, assuming only pixel-wise independence of the noise.

**Datasets.** Evaluated on artificial noise, real-world camera noise and microscope noise, using Kodak, SIDD, PolyU and McMaster among the benchmarks *(named in the paper)*.

**Value then vs. now.** Current, and the most immediately reproducible source in the roster — the paper points to a Colab notebook containing its implementation and hyperparameters.

**Relation to the roster.** It is the terminus of the data-requirement branch: DnCNN needs clean pairs, N2N needs noisy pairs, N2V needs a noisy dataset, ZS-N2N needs nothing but the image in front of it. The paper itself names Noise2Noise as motivation, closing the loop inside our own source list.

---

### A10 · Practical Blind Image Denoising via Swin-Conv-UNet and Data Synthesis (SCUNet)

**Authors** Kai Zhang, Yawei Li, Jingyun Liang, Jiezhang Cao, Yulun Zhang, Hao Tang, Deng-Ping Fan, Radu Timofte, Luc Van Gool
**Institutions** Computer Vision Lab, ETH Zürich; Computer Vision Lab, University of Würzburg; KU Leuven *(stated on the PDF title page)*
**Venue & year** Machine Intelligence Research, 20(6), pp. 822–836, 2023, DOI 10.1007/s11633-023-1466-0 *(printed verbatim in the PDF's own citation block)*.
**Citations** 391 *(Google Scholar, checked 9 August 2026)*

**Sub-problem.** Existing methods rely on simple noise assumptions, and a general-purpose blind denoiser for real images remains unsolved.

**Model / architecture.** A **swin-conv block** combining the local modelling of a residual convolutional layer with the non-local modelling of a swin transformer block, used as the main building block of an image-to-image translation UNet. Paired with a designed degradation model covering Gaussian, Poisson, speckle, JPEG and processed camera sensor noise plus resizing, using a random shuffle strategy and a double degradation strategy.

**Datasets.** Urban100, Set12, Kodak, DND, CBSD68, BSD68, McMaster, SIDD, Waterloo and DIV2K appear across its experiments *(named in the paper)*.

**Value then vs. now.** Current, and uniquely relevant to Stage 2 because its data synthesis pipeline is specified in enough detail to be re-implemented.

**Relation to the roster.** It is the synthesis paper. It fuses the convolutional line (DnCNN and successors) with the transformer line (Restormer and SwinIR-style blocks), and it is the only source that treats the *noise model* — the very assumption stated in DnCNN's opening equation — as the thing to fix. It closes the arc that the anchor paper opened.

---

### A11 · MambaIR: A Simple Baseline for Image Restoration with State-Space Model

**Authors** Hang Guo, Jinmin Li, Tao Dai, Zhihao Ouyang, Xudong Ren, Shu-Tao Xia *(Guo and Li marked as equal contributors; Dai as corresponding author)*
**Institutions** Tsinghua Shenzhen International Graduate School, Tsinghua University; College of Computer Science and Software Engineering, Shenzhen University; ByteDance Inc.; Aitist.ai; Peng Cheng Laboratory *(stated on the PDF title page)*
**Venue & year** ECCV 2024, pp. 222–241 *(the PDF is arXiv:2402.15648v3, 15 Oct 2024; venue verified against independent proceedings records)*.
**Citations** 1,208 *(Google Scholar, checked 9 August 2026)*

**Sub-problem.** The dilemma between global receptive fields and efficient computation, plus two failures of standard Mamba in low-level vision: local pixel forgetting and channel redundancy.

**Model / architecture.** A Residual State Space Block (RSSB) adding local enhancement and channel attention to the vanilla Mamba selective state space model, achieving long-range dependency modelling at linear complexity.

**Datasets.** Urban100, Manga109, Set5, Set14, DIV2K, Flickr2K for super-resolution; SIDD for training and SIDD test plus DND for real denoising evaluation *(named in the paper)*.

**Value then vs. now.** The newest source in the roster and the clearest signal that the literature sweep reached genuinely current work. It reports outperforming SwinIR by up to 0.45 dB on super-resolution at comparable cost.

**Relation to the roster.** It resolves the same dilemma Restormer attacked, but by replacing attention altogether rather than making it cheaper. Together with NAFNet it demonstrates that the field has *three* live answers to the receptive-field problem — cheaper attention, simplified convolution, and linear-complexity state spaces — which is a far stronger closing position than naming a single winner.

---

## 5. Category B Source Justification

The guidelines ask, for each auxiliary source, what it is and how it will bridge academic theory to the practical engineering of Stage 2.

**B1 · Stanford CS231n, *Convolutional Neural Networks for Visual Recognition*.** A recognised academic lecture series, named verbatim in the guidelines as an acceptable Category B type. It supplies the mechanics that the Category A papers assume rather than explain — convolution arithmetic, receptive field growth, and batch normalisation. **Bridge to Stage 2:** DnCNN reports a $35 \times 35$ receptive field at depth 17 without deriving it; CS231n provides the derivation, which is what makes the corresponding lines of a real repository legible when we read code.

**B2 · Google Research Blog, *Night Sight: Seeing in the Dark on Pixel Phones*.** A technical blog from an industry leader — Google Research is named verbatim in the guidelines. It separates photon shot noise from read noise, explains that SNR rises with the square root of exposure time, and describes how HDR+ captures a burst of frames, aligns them in software, and merges them. **Bridge to Stage 2:** it is the only source in the roster describing denoising as a shipped consumer product, giving Stage 2's deployment-reality requirement a concrete anchor and supplying the "why does this matter" opening for the pitch.

**B3 · Gonzalez & Woods, *Digital Image Processing* — the Image Restoration chapter.** A textbook chapter, an explicitly permitted Category B type. It supplies the mathematical treatment of noise models (Gaussian, Rayleigh, Poisson, salt-and-pepper) and of mean, order-statistic and adaptive filters. **Bridge to Stage 2:** it is the bottom rung of the timeline, below BM3D, and it is the reference against which SCUNet's synthetic degradation pipeline can be read critically — SCUNet's noise list is essentially the textbook's noise list, industrialised.

---

## 6. The Research Direction Being Proposed for Approval

Stated as one claim, since the guidelines emphasise that the deck must pitch a cohesive story rather than list papers:

> Image denoising is the cleanest available case study in how computer vision replaced hand-designed priors with learned ones. Its history divides into four eras separated by three identifiable bottlenecks — *manual prior design*, *the clean-data requirement*, and *the receptive-field limits of convolution*. Each bottleneck was named by the paper that broke it, so the arc can be evidenced from the primary sources rather than imposed retrospectively. Because the field currently holds three competing answers to the third bottleneck, the story ends in a genuine open question rather than a winner.

---

## 7. Declared Gaps and Unverified Items

Listed openly, because the guidelines grade rigor and because a gap that is stated is a smaller problem than a gap that is discovered.

**7.1 Citation counts — resolved.** The guidelines require a current count per Category A paper. No PDF contains one, so all eleven were taken from Google Scholar on 9 August 2026:

| Paper | Cited by | Paper | Cited by |
|---|---|---|---|
| BM3D | 11,976 | Restormer | 6,181 |
| WNNM | 2,960 | NAFNet | 2,318 |
| TNRD | 1,626 | ZS-N2N | 266 |
| DnCNN | 11,674 | SCUNet | 391 |
| Noise2Noise | 3,064 | MambaIR | 1,208 |
| Noise2Void | 2,075 | | |

Two observations worth making aloud rather than leaving in the table. BM3D and DnCNN sit near twelve thousand each, which is precisely why both remain universal baselines seventeen and nine years after publication — the numbers corroborate the narrative rather than merely decorating it. Conversely, ZS-N2N at 266 and SCUNet at 391 are low because they are recent, not because they are weak; recency and citation count are confounded, and saying so pre-empts the obvious challenge. Counts move continuously, so the date is quoted alongside every figure.

**7.2 TNRD year.** The PDF header says 2016; citing literature says TPAMI 39(6), 2017. Both reflect reality — acceptance versus issue. Cite 2017 and be ready to explain if challenged.

**7.3 Venue verification method.** Venues for BM3D, TNRD, Noise2Noise and SCUNet are printed in the source PDFs themselves. The remaining seven are preprint versions carrying no venue, so those were confirmed against publisher, CVF Open Access or institutional proceedings records rather than copied from another paper's reference list.

**7.4 Not covered here, by design.** Comparative PSNR/SSIM tables, repository analysis, code walkthroughs and deployment discussion are Stage 2 and Stage 3 requirements. They are deliberately excluded from this document and from the Stage 1 deck.
