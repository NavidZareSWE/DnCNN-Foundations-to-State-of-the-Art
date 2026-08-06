I'll start by pulling the exact Stage 1 requirements from your project materials.Let me pull the exact wording of the Stage 1 rules from the official brief, plus anything TA-specific.The requirements are now clear. Let me verify each candidate paper's venue, year, and availability rather than relying on memory.Now let me verify which of these have YouTube explainers — that's your Bonus #1.## Before the list: two honesty flags

**No TA document exists in the project.** I searched the project knowledge thoroughly. The only authoritative rule source is the assignment brief, *From Foundations to State-of-the-Art: A Comprehensive Synthesis* (Prof. Zohreh Azimifar). Your project guide states explicitly that no TA clarifications were ever supplied. I am therefore ranking against the **PDF brief only**. If your TA issued verbal amendments, re-check my selections against them.

**"p2-part" is undefined.** That term appears nowhere in the assignment brief, the DnCNN paper, your deck, or the study guide. I have interpreted your High Bonus as "papers containing a numbered algorithm box, pseudocode, or an explicitly enumerated modelling pipeline." Correct me if it means something specific.

## The mandatory criteria I am filtering against

From the brief, Stage 1:

| Rule | Requirement |
|---|---|
| Volume | ≥ 10 distinct, high-quality sources |
| Category A | ≥ 70% peer-reviewed papers from top-tier venues (IEEE TPAMI, CVPR, ICCV, ECCV, NeurIPS, MICCAI given as examples) |
| Category B | ≤ 30% textbooks, recognised lectures, industry-leader technical blogs |
| Recency | Must include a mix of older milestones **and** recent SOTA from **2022–present** |
| Narrative | Must trace spatial filtering → CNN → Vision Transformer, not summarise papers in isolation |

My proposed roster: **14 sources = 11 Category A + 3 Category B → A = 78.6%**, clearing the 70% floor with margin. This matches the "14 sources" row of Table 1 in your study guide.

---

# CATEGORY A — Peer-reviewed papers (11)

## Era 1 — Classical DIP

### A1. Image Denoising by Sparse 3-D Transform-Domain Collaborative Filtering (BM3D)
- **Authors:** Kostadin Dabov, Alessandro Foi, Vladimir Katkovnik, Karen Egiazarian
- **Year:** 2007 — *IEEE Transactions on Image Processing*, 16(8), 2080–2095
- **Scholar:** `https://scholar.google.com/scholar?q=Image+denoising+by+sparse+3-D+transform-domain+collaborative+filtering`
- **PDF:** Not verified as freely hosted by the publisher; IEEE Xplore is paywalled. Check your university's IEEE subscription.
- **YouTube:** I searched but found no authoritative explainer I can verify.
- **Summary:** BM3D groups similar 2-D patches into 3-D stacks, applies a shrinkage in a 3-D transform domain, and aggregates the filtered patches back with weighted averaging. It runs this as a two-stage cascade — a hard-threshold pass, then a Wiener-filtered pass using the first estimate as an oracle. It was the classical benchmark that DnCNN was explicitly built to beat.
- **Mandatory fit:** IEEE TIP, peer-reviewed, top-tier; anchors the "classical DIP origins" half of the evolutionary path. Your DnCNN paper reports its 512×512 runtime as 2.85 s, giving you the runtime contrast the brief wants.
- **Bonuses:** **High Bonus — strongest in the set.** The method is written as three named, sequential stages, then repeated as a second stage. This is the cleanest "explicit algorithm" paper you have. No YouTube. Dense but rigorous.
- **Confidence: 95%** — venue and pagination cross-confirmed across multiple independent reference lists.

### A2. Weighted Nuclear Norm Minimization with Application to Image Denoising (WNNM)
- **Authors:** Shuhang Gu, Lei Zhang, Wangmeng Zuo, Xiangchu Feng
- **Year:** 2014 — CVPR
- **Scholar:** `https://scholar.google.com/scholar?q=Weighted+Nuclear+Norm+Minimization+with+Application+to+Image+Denoising`
- **PDF:** CVF Open Access hosts CVPR 2014 papers; locate via `openaccess.thecvf.com`.
- **YouTube:** None verified.
- **Summary:** WNNM treats a stack of similar patches as a low-rank matrix corrupted by noise and recovers it by minimising a *weighted* nuclear norm, assigning smaller penalties to larger singular values. It represents the peak of classical non-local performance — and its computational cost.
- **Mandatory fit:** CVPR, explicitly named in the brief's venue list. Represents the "bottleneck" the brief asks you to identify: your DnCNN paper reports 773 s for a 512×512 image, versus DnCNN-B at 0.060 s.
- **Bonuses:** High Bonus — the paper presents its solver as a numbered algorithm with an iterative regularisation loop. No YouTube.
- **Confidence: 80%.** Venue and year are taken from the reference lists inside your project files; I did not independently verify them via the CVF proceedings in this session. **Verify before citing.**

### A3. Trainable Nonlinear Reaction Diffusion (TNRD)
- **Authors:** Yunjin Chen, Thomas Pock
- **Year:** 2016 — *IEEE TPAMI*
- **Scholar:** `https://scholar.google.com/scholar?q=Trainable+Nonlinear+Reaction+Diffusion+fast+effective+image+restoration`
- **PDF:** Paywalled on IEEE Xplore; an arXiv preprint exists.
- **YouTube:** None verified.
- **Summary:** TNRD unrolls a fixed number of nonlinear diffusion steps into a trainable feed-forward architecture, learning the filters and influence functions end-to-end. It eliminates test-time optimisation while retaining a diffusion-process interpretation.
- **Mandatory fit:** IEEE TPAMI — named explicitly in the brief. It is DnCNN's direct theoretical ancestor and is the single best paper for narrating the classical→deep *bridge*, which the brief's Section 3 requires.
- **Bonuses:** High Bonus — the diffusion-step unrolling is presented as an explicit stage-by-stage pipeline. No YouTube.
- **Confidence: 80%.** Same provenance caveat as A2 — venue and year come from your project files, not my own verification.

## Era 2 — The deep CNN turn

### A4. Beyond a Gaussian Denoiser: Residual Learning of Deep CNN for Image Denoising (DnCNN)
- **Authors:** Kai Zhang, Wangmeng Zuo, Yunjin Chen, Deyu Meng, Lei Zhang
- **Year:** 2017 — *IEEE Transactions on Image Processing*, 26(7), 3142–3155 (arXiv:1608.03981)
- **Scholar:** `https://scholar.google.com/scholar?q=Beyond+a+Gaussian+Denoiser+Residual+Learning+of+Deep+CNN+for+Image+Denoising`
- **PDF:** In your project folder; arXiv preprint at `https://arxiv.org/abs/1608.03981`
- **YouTube:** None verified.
- **Summary:** DnCNN learns the *residual* (the noise) rather than the clean image, combining residual learning with batch normalisation in a plain 17–20 layer CNN with no pooling and no skip connections. A single blind model, DnCNN-B, handles an unknown noise range, and DnCNN-3 handles denoising, super-resolution, and JPEG deblocking simultaneously.
- **Mandatory fit:** Your anchor paper, and the pivot of the entire narrative. IEEE TIP.
- **Bonuses:** High Bonus — the architecture is specified layer-by-layer with exact training hyperparameters (128-patch mini-batches, 50 epochs, LR decayed 1e⁻¹→1e⁻⁴, momentum 0.9, weight decay 1e⁻⁴), which is fully reproducible.
- **Confidence: 100%** — verified directly against the PDF in your project.

### A5. Noise2Noise: Learning Image Restoration without Clean Data
- **Authors:** Jaakko Lehtinen, Jacob Munkberg, Jon Hasselgren, Samuli Laine, Tero Karras, Miika Aittala, Timo Aila
- **Year:** 2018 — ICML (PMLR vol. 80, pp. 2965–2974 / 4620–4631 depending on edition)
- **Scholar:** `https://scholar.google.com/scholar?q=Noise2Noise+Learning+Image+Restoration+without+Clean+Data`
- **PDF:** `https://proceedings.mlr.press/v80/lehtinen18a/lehtinen18a.pdf` (open access, verified)
- **YouTube:** No authoritative explainer verified. A recorded FCAI talk by Lehtinen exists but I could not confirm a YouTube URL.
- **Summary:** The paper's argument is a statistical one: because an L2-trained regressor converges to the conditional mean of its targets, training on *noisy* targets converges to the same solution as training on clean ones, provided noise is zero-mean. It shows the L1 loss recovers the median of the targets, so networks can be trained to repair images with up to 50% outlier content using only pairs of corrupted images.
- **Mandatory fit:** ICML — peer-reviewed and top-tier, though not on the brief's named list. It is the conceptual hinge between supervised CNN denoising and the self-supervised era, which is essential to your narrative.
- **Bonuses:** **Bonus #2 — exceptionally clearly written.** The core result is a two-line expectation argument. High Bonus partially: the loss-function-to-statistic mapping (L2→mean, L1→median, L0→mode) is laid out explicitly and is trivially reproducible.
- **Confidence: 95%** — venue verified via Aalto's research portal and the PMLR proceedings.

### A6. Noise2Void — Learning Denoising From Single Noisy Images
- **Authors:** Alexander Krull, Tim-Oliver Buchholz, Florian Jug
- **Year:** 2019 — CVPR, pp. 2129–2137
- **Scholar:** `https://scholar.google.com/scholar?q=Noise2Void+Learning+Denoising+From+Single+Noisy+Images`
- **PDF:** `https://openaccess.thecvf.com/content_CVPR_2019/papers/Krull_Noise2Void_-_Learning_Denoising_From_Single_Noisy_Images_CVPR_2019_paper.pdf` (verified open access)
- **YouTube:** ✅ `https://www.youtube.com/watch?v=uaa6GzmVLQo` — a practical N2V walkthrough (DigitalSreeni, #294). This is an implementation tutorial, not a paper reading. An author video also exists on Vimeo at `https://vimeo.com/305045007`.
- **Summary:** N2V removes even the paired-noisy-image requirement by using a blind-spot receptive field: the network predicts each pixel from its neighbourhood while being architecturally forbidden from seeing the pixel itself. It is trained by masking N pixels per patch and supervising only on those.
- **Mandatory fit:** CVPR — named in the brief. Completes the supervised → N2N → N2V self-supervision arc.
- **Bonuses:** **Bonus #1 partially satisfied** (tutorial video, not a paper explainer). **High Bonus** — the masking scheme is stated as an explicit procedure, with concrete numbers: a depth-2 U-Net with kernel size 5, batch norm, 32 initial feature maps, batch size 128, and N = 64 pixels manipulated per input patch. That is directly reproducible.
- **Confidence: 95%** — CVPR 2019 and pagination confirmed via dblp and CVF.

## Era 3 — Transformers and modern SOTA (2022–present)

### A7. Restormer: Efficient Transformer for High-Resolution Image Restoration ⭐ **top pick**
- **Authors:** Syed Waqas Zamir, Aditya Arora, Salman Khan, Munawar Hayat, Fahad Shahbaz Khan, Ming-Hsuan Yang
- **Year:** 2022 — **CVPR 2022 (Oral)**, pp. 5718–5729
- **Scholar:** `https://scholar.google.com/scholar?q=Restormer+Efficient+Transformer+for+High-Resolution+Image+Restoration`
- **PDF:** `https://openaccess.thecvf.com/content/CVPR2022/html/Zamir_Restormer_Efficient_Transformer_for_High-Resolution_Image_Restoration_CVPR_2022_paper.html` (verified); arXiv `https://arxiv.org/abs/2111.09881`
- **YouTube:** ✅ **Official CVPR 2022 conference video:** `https://www.youtube.com/watch?v=3mqu6N4_0pY`. A second independent review: `https://www.youtube.com/watch?v=wL7IRllbcC0`
- **Summary:** Restormer redesigns the two core Transformer building blocks — multi-head attention and the feed-forward network — so the model captures long-range pixel interactions while remaining applicable to large images, avoiding the quadratic cost of standard self-attention. The two mechanisms are MDTA (attention computed across channels rather than spatial positions) and GDFN (a gated depthwise feed-forward network). It reports SOTA on Gaussian and real-image denoising among other tasks.
- **Mandatory fit:** **Satisfies every mandatory criterion simultaneously** — CVPR (named venue), 2022 (recency window), and it is the canonical "Transformer" endpoint of the brief's required `Classical Math → CNN → Transformer` timeline.
- **Bonuses:** **Bonus #1 — official conference video, the strongest YouTube evidence in the set. High Bonus** — the paper walks through the overall pipeline in Fig. 2, then MDTA and GDFN in turn, and closes with the details of a progressive training scheme. That progressive schedule (increasing patch size, decreasing batch size) is an explicit, reproducible training pipeline.
- **Confidence: 98%.** This is the single highest-scoring paper against your combined criteria.

### A8. Simple Baselines for Image Restoration (NAFNet)
- **Authors:** Liangyu Chen, Xiaojie Chu, Xiangyu Zhang, Jian Sun
- **Year:** 2022 — **ECCV 2022**, LNCS 13667, pp. 17–33
- **Scholar:** `https://scholar.google.com/scholar?q=Simple+Baselines+for+Image+Restoration+NAFNet`
- **PDF:** arXiv `https://arxiv.org/abs/2204.04676`
- **YouTube:** None verified.
- **Summary:** The authors argue that the system complexity of SOTA restoration methods has been rising in ways that hinder analysis and comparison, and propose a simple baseline that exceeds SOTA while remaining computationally efficient. They then show the nonlinear activations — Sigmoid, ReLU, GELU, Softmax — are unnecessary and can be replaced by multiplication or removed, yielding the Nonlinear Activation Free Network. It reports 40.30 dB PSNR on SIDD for denoising, exceeding the prior SOTA by 0.28 dB at under half the computational cost.
- **Mandatory fit:** ECCV — named in the brief. 2022, inside the recency window.
- **Bonuses:** **High Bonus — arguably the best "step-by-step methodology" paper in the whole set.** The method is literally constructed as an incremental derivation: starting from a plain UNet-backbone CNN block, the authors add common enhancements (normalisation, advanced activation, attention) one at a time and measure each increment. Every design decision is an ablation you can reproduce and present as a slide sequence. **Bonus #2 — extremely readable**, by design. No YouTube.
- **Confidence: 95%** — ECCV 2022 proceedings entry confirmed via ACM DL and Springer.

### A9. Zero-Shot Noise2Noise: Efficient Image Denoising Without Any Data ⭐ **best readability + reproducibility**
- **Authors:** Youssef Mansour, Reinhard Heckel
- **Year:** 2023 — **CVPR 2023**, pp. 14018–14027
- **Scholar:** `https://scholar.google.com/scholar?q=Zero-Shot+Noise2Noise+Efficient+Image+Denoising+Without+Any+Data`
- **PDF:** `https://openaccess.thecvf.com/content/CVPR2023/html/Mansour_Zero-Shot_Noise2Noise_Efficient_Image_Denoising_Without_Any_Data_CVPR_2023_paper.html` (verified); arXiv `https://arxiv.org/abs/2303.11253`
- **CVPR poster/slides page:** `https://cvpr.thecvf.com/virtual/2023/poster/21064`
- **YouTube:** None verified — but the CVPR virtual page hosts slides and a poster.
- **Summary:** The paper shows that a simple 2-layer network, with no training data and no knowledge of the noise distribution, can achieve high-quality denoising at low computational cost. The approach is motivated by Noise2Noise and Neighbor2Neighbor and works for pixel-wise independent noise. The authors provide a Colab notebook containing their implementation and hyperparameters.
- **Mandatory fit:** CVPR 2023 — named venue, well inside the 2022+ window.
- **Bonuses:** **Bonus #2 — the clearest and shortest modern paper on this list. High Bonus — the strongest reproducibility case of any paper here:** a 2-layer network, published hyperparameters, and an executable Colab notebook. If any group member needs to demonstrate a working denoiser live at the TA defence, this is the one they can actually run.
- **Confidence: 95%.**

### A10. Practical Blind Image Denoising via Swin-Conv-UNet and Data Synthesis (SCUNet)
- **Authors:** Kai Zhang, Yawei Li, Jingyun Liang, Jiezhang Cao, Yulun Zhang, Hao Tang, Deng-Ping Fan, Radu Timofte, Luc Van Gool
- **Year:** 2023 — *Machine Intelligence Research*, 20(6), 822–836
- **Scholar:** `https://scholar.google.com/scholar?q=Practical+Blind+Image+Denoising+via+Swin-Conv-UNet+and+Data+Synthesis`
- **PDF:** `https://link.springer.com/content/pdf/10.1007/s11633-023-1466-0.pdf` (verified open); arXiv `https://arxiv.org/abs/2203.13278`
- **YouTube:** None verified.
- **Summary:** SCUNet attacks blind real-image denoising from two directions at once: a swin-conv block that fuses the local modelling of a residual convolutional layer with the non-local modelling of a Swin Transformer block, plugged into a UNet; and a practical noise degradation model for training-data synthesis covering Gaussian, Poisson, speckle, JPEG compression and further degradations.
- **Mandatory fit:** 2023, peer-reviewed. ⚠️ **Caveat:** *Machine Intelligence Research* (Springer) is **not** on the brief's named venue list, though the list is prefaced with "e.g." The author roster — Kai Zhang (DnCNN's first author), Van Gool, Timofte — makes a strong quality defence. Flag this one to your TA rather than being surprised by the question.
- **Bonuses:** **High Bonus — the best explicit data/modelling pipeline in the set.** The degradation-synthesis model is a sequential, randomised pipeline you can diagram as one slide, and it directly answers the brief's Stage 2 question about how modern data pipelines work. It is also narratively perfect: the *same author* who wrote your anchor paper returns six years later with the Transformer answer.
- **Confidence: 92%** (deducted for the venue caveat, not the paper).

### A11. MambaIR: A Simple Baseline for Image Restoration with State-Space Model
- **Authors:** Hang Guo, Jinmin Li, Tao Dai, Zhihao Ouyang, Xudong Ren, Shu-Tao Xia
- **Year:** 2024 — **ECCV 2024**, LNCS 15076, pp. 222–241
- **Scholar:** `https://scholar.google.com/scholar?q=MambaIR+Simple+Baseline+for+Image+Restoration+with+State-Space+Model`
- **PDF:** arXiv `https://arxiv.org/abs/2402.15648`
- **YouTube:** None verified.
- **Summary:** MambaIR observes that existing restoration backbones face a dilemma between global receptive fields and efficient computation, and applies the Selective Structured State Space Model (Mamba) to model long-range dependencies at linear complexity. It addresses two problems the standard Mamba has in low-level vision: local pixel forgetting and channel redundancy.
- **Mandatory fit:** ECCV — named venue. 2024 — this is your *newest* source, and it demonstrates to the TAs that your literature sweep reached genuinely current work rather than stopping at 2022.
- **Bonuses:** No YouTube verified. High Bonus partially — the block design is specified explicitly, though the state-space mathematics makes it the hardest read on this list. Include it for recency and for the "future directions" section; do not make it the centrepiece unless a group member is confident defending SSMs.
- **Confidence: 88%.**

### Optional 12th — SwinIR
Liang, Cao, Sun, Zhang, Van Gool, Timofte, **ICCV *Workshops* 2021**, pp. 1833–1844. PDF verified at CVF. Two caveats disqualify it from my core list: it is a **workshop** paper, and **2021**, so it satisfies neither the "top-tier conference" nor the "2022–present" reading strictly. Include it only as a *bridge* citation in your narrative — SCUNet (A10) explicitly positions itself as integrating SwinIR's and DRUNet's complementary designs — not as one of your recency papers.

---

# CATEGORY B — Auxiliary materials (3)

### B1. Stanford CS231n — Convolutional Neural Networks for Visual Recognition
- **Type:** Recognised academic lecture series — **named verbatim in the brief**, so it is unimpeachable.
- **Use:** Cite the convolution/receptive-field and batch-normalisation material to underpin your DnCNN architecture section, including the RF = (2d+1)² derivation.
- **Confidence: 100%** on category eligibility.

### B2. Google Research Blog — "Night Sight: Seeing in the Dark on Pixel Phones"
- **URL:** `https://research.google/blog/night-sight-seeing-in-the-dark-on-pixel-phones/` (verified live)
- **Type:** Technical blog from an industry leader — **Google Research is named verbatim in the brief**.
- **Summary:** The post separates photon shot noise from read noise, explains that SNR rises with the square root of exposure time, and describes how HDR+ — introduced in 2014 — captures a burst of frames, aligns them in software, and merges them.
- **Why it earns its slot:** It is the only source in your roster that shows denoising as a *shipped consumer product*. That gives your "why does this matter" opening slide something concrete, and it feeds Stage 2's deployment-reality requirement.
- **Confidence: 98%.**

### B3. Gonzalez & Woods, *Digital Image Processing* — the Image Restoration chapter
- **Type:** Textbook chapter — an explicitly permitted Category B type.
- **Use:** The mathematical treatment of noise models (Gaussian, Rayleigh, Poisson, salt-and-pepper) and mean/order-statistic/adaptive filters. This is your bottom rung on the timeline, below BM3D.
- **⚠️ Verify yourself:** chapter number and page range vary between the 3rd and 4th editions. Cite the exact edition on your shelf.
- **Confidence: 85%** — high on category eligibility and topical fit; I have not verified edition-specific pagination.

---

## Roster arithmetic

| | Count | Share |
|---|---|---|
| Category A | 11 | **78.6%** ✅ (floor is 70%) |
| Category B | 3 | 21.4% ✅ (ceiling is 30%) |
| **Total** | **14** | ✅ (floor is 10) |
| Pre-2018 milestones | 4 | ✅ "older milestone papers" |
| 2022–present | 5 (A7–A11) | ✅ "recent SOTA publications" |

## Ranked against your criteria

1. **Restormer (A7)** — the only paper satisfying every mandatory criterion *and* Bonus #1 with an official conference video *and* the High Bonus. Lead with it.
2. **NAFNet (A8)** and **ZS-N2N (A9)** — no video, but they win the High Bonus and Bonus #2 outright. NAFNet's incremental derivation and ZS-N2N's runnable Colab are your two best "we can explain and reproduce this" defences.
3. **SCUNet (A10)** — best explicit pipeline, best narrative closure with your anchor paper, minor venue caveat.
4. **BM3D (A1)** — best classical algorithm exposition.

## Where I could not deliver

- **YouTube coverage is thin.** I verified real explainer videos for only two entries: Restormer (official CVPR video, plus an independent review) and Noise2Void (an implementation tutorial). For BM3D, WNNM, TNRD, DnCNN, Noise2Noise, NAFNet, SCUNet, ZS-N2N and MambaIR, **I searched but found nothing I can verify.** I have not invented links. ECVA and CVF host presentation videos for ECCV/CVPR papers — check those directly for A8, A9 and A11.
- **A2 (WNNM) and A3 (TNRD)** rest on venue/year data taken from the reference lists inside your project files, not from my own check of the proceedings. Verify both before they go on a slide.
- **A1 and A3** are behind IEEE paywalls; I found no legitimate free PDF.