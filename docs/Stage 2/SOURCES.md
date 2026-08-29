# Master Source Register — Publication Metadata and Reference Implementations

**Project:** *From Foundations to State-of-the-Art* — Image Denoising
**Anchor paper:** DnCNN (Zhang et al., IEEE TIP, 2017)
**Register compiled:** 29 August 2026
**Composition:** 15 sources — 12 Category A (80.0 %), 3 Category B (20.0 %). The Category A share exceeds the 70 % floor stipulated by the assignment brief.

This register consolidates, for every source in the bibliography, the bibliographic identity of the work and the location of its reference implementation. All repository URLs were re-resolved over HTTPS on 29 August 2026 and the returned status code is recorded in Table 3. Where a work has no author-maintained repository, the table states this explicitly rather than substituting a third-party re-implementation without labelling it as such.

---

## 1. Category A — Peer-Reviewed Publications

Table 1 records the bibliographic identity of the twelve peer-reviewed sources. The identifier column (`A1`–`A12`) is the citation key used throughout the Stage 1 and Stage 2 deliverables. Publication dates are given at the granularity at which they are printed in the published record: journal articles carry a volume, issue and page range, whereas conference papers carry proceedings pagination and the month of the conference.

**Table 1 — Category A sources: identity, venue and publication date.**

| ID | Method | Full title (abbreviated) | Authors | Venue | Publication date | Pages | Preprint |
|---|---|---|---|---|---|---|---|
| A1 | **BM3D** | Image Denoising by Sparse 3-D Transform-Domain Collaborative Filtering | K. Dabov, A. Foi, V. Katkovnik, K. Egiazarian | IEEE Trans. Image Processing, vol. 16, no. 8 | August 2007 | 2080–2095 | — |
| A2 | **WNNM** | Weighted Nuclear Norm Minimization with Application to Image Denoising | S. Gu, L. Zhang, W. Zuo, X. Feng | CVPR | 2014 | 2862–2869 | — |
| A3 | **TNRD** | Trainable Nonlinear Reaction Diffusion: A Flexible Framework for Fast and Effective Image Restoration | Y. Chen, T. Pock | IEEE TPAMI, vol. 39, no. 6 | 2017 (issue date; IEEE early access 2016) | 1256–1272 | arXiv:1508.02848 (12 Aug 2015) |
| A4 | **DnCNN** *(anchor)* | Beyond a Gaussian Denoiser: Residual Learning of Deep CNN for Image Denoising | K. Zhang, W. Zuo, Y. Chen, D. Meng, L. Zhang | IEEE Trans. Image Processing, vol. 26, no. 7 | July 2017 | 3142–3155 | arXiv:1608.03981 |
| A5 | **Noise2Noise** | Noise2Noise: Learning Image Restoration without Clean Data | J. Lehtinen, J. Munkberg, J. Hasselgren, S. Laine, T. Karras, M. Aittala, T. Aila | ICML, PMLR vol. 80 | July 2018 | — | arXiv:1803.04189 |
| A6 | **Noise2Void** | Noise2Void — Learning Denoising from Single Noisy Images | A. Krull, T.-O. Buchholz, F. Jug | CVPR | June 2019 | — | arXiv:1811.10980 |
| A7 | **Restormer** | Restormer: Efficient Transformer for High-Resolution Image Restoration | S. W. Zamir, A. Arora, S. Khan, M. Hayat, F. S. Khan, M.-H. Yang | CVPR | June 2022 | 5728–5739 | arXiv:2111.09881 |
| A8 | **NAFNet** | Simple Baselines for Image Restoration | L. Chen, X. Chu, X. Zhang, J. Sun | ECCV, LNCS vol. 13667 | 2022 | 17–33 | arXiv:2204.04676 (10 Apr 2022) |
| A9 | **ZS-N2N** | Zero-Shot Noise2Noise: Efficient Image Denoising without any Data | Y. Mansour, R. Heckel | CVPR | June 2023 | 14018–14027 | arXiv:2303.11253 |
| A10 | **SCUNet** | Practical Blind Image Denoising via Swin-Conv-UNet and Data Synthesis | K. Zhang, Y. Li, J. Liang, J. Cao, Y. Zhang, H. Tang, D.-P. Fan, R. Timofte, L. Van Gool | Machine Intelligence Research, vol. 20, no. 6 | 2023 | 822–836 | arXiv:2203.13278 |
| A11 | **MambaIR** | MambaIR: A Simple Baseline for Image Restoration with State-Space Model | H. Guo, J. Li, T. Dai, Z. Ouyang, X. Ren, S.-T. Xia | ECCV | 2024 | 222–241 | arXiv:2402.15648 |
| A12 | **P2N** | Positive2Negative: Breaking the Information-Lossy Barrier in Self-Supervised Single Image Denoising | T. Li, L. Wang, Z. Xu, L. Zhu, W. Lu, H. Huang | CVPR | June 2025 | 17924–17934 | arXiv:2412.16460 (21 Dec 2024) |

---

## 2. Reference Implementations

Table 2 pairs each Category A source with the implementation that its authors released, together with the framework in which that implementation is written. The distinction between an *author-released* artefact and a *third-party* artefact is preserved in the final column, because the two do not carry equivalent evidential weight when a claim about a method is grounded in its code.

**Table 2 — Reference implementations by source.**

| ID | Method | Implementation URL | Framework / language | Provenance |
|---|---|---|---|---|
| A1 | BM3D | `https://webpages.tuni.fi/foi/GCF-BM3D` | MATLAB with MEX binaries | Author-released. The 2007 paper prints the address `http://www.cs.tut.fi/~foi/GCF-BM3D`; Tampere University has since migrated the page to the `webpages.tuni.fi` host. |
| A2 | WNNM | `https://github.com/csjunxu/WNNM_CVPR2014` | MATLAB | **Third-party mirror.** No author-maintained repository was located. The repository contains the MATLAB demo set (`Demo.m`, `Demo_AWGN.m`, `Block_matching.m`, `NoiseEstimation/`) but no README or licence file. |
| A3 | TNRD | `https://github.com/VLOGroup/denoising-variationalnetwork` | TensorFlow (requires the `tensorflow-icg` fork) | **Same-laboratory re-implementation, not the original release.** VLOGroup is the Institute for Computer Graphics and Vision at TU Graz, where co-author T. Pock is based; the repository states that it implements the TNRD model and was used for Kobler et al., GCPR 2017. The original MATLAB release was distributed from the first author's `escience.cn` page, which is no longer reachable. |
| A4 | DnCNN | `https://github.com/cszn/DnCNN` | MATLAB / MatConvNet at the repository root, plus a `TrainingCodes/` directory | Author-released; the URL is printed in the paper. |
| A4 | DnCNN (PyTorch) | `https://github.com/cszn/KAIR` | PyTorch | Author-released. KAIR is the same author's unified training and testing toolbox; it is the artefact actually inspected in Stage 2, and it also supplies the SCUNet weights. |
| A5 | Noise2Noise | `https://github.com/NVlabs/noise2noise` | TensorFlow | Author-released. The README identifies it as the official TensorFlow implementation of the ICML 2018 paper; licensed CC BY-NC 4.0. |
| A6 | Noise2Void | `https://github.com/juglab/n2v` | TensorFlow / Keras, built on CSBDeep | Author-released (Jug laboratory). The README now carries a maintenance warning and directs new users to the CAREamics PyTorch library. |
| A7 | Restormer | `https://github.com/swz30/Restormer` | PyTorch (BasicSR; requires `einops`) | Author-released. An official Hugging Face Space is also maintained at `https://huggingface.co/spaces/swzamir/Restormer`. |
| A8 | NAFNet | `https://github.com/megvii-research/NAFNet` | PyTorch (BasicSR) | Author-released (MEGVII Technology). |
| A9 | ZS-N2N | `https://colab.research.google.com/drive/1i82nyizTdszyHkaHBuKPbWnTzao8HF9b` | PyTorch, distributed as a Colab notebook | Author-released. **No GitHub repository exists.** The notebook URL is printed verbatim in the arXiv abstract; the implementation and its hyperparameters are contained entirely within the notebook. |
| A10 | SCUNet | `https://github.com/cszn/SCUNet` | PyTorch | Author-released. |
| A11 | MambaIR | `https://github.com/csguoh/MambaIR` | PyTorch (requires compiled CUDA extensions for the selective-scan operator) | Author-released. |
| A12 | P2N | `https://github.com/Li-Tong-621/P2N-plus` | PyTorch | Author-released, **but not at the address printed in the paper.** See Section 4. |
| A12 | P2N (baselines) | `https://github.com/Li-Tong-621/Tool-for-SSSID` | PyTorch | Author-released companion repository containing reproduced self-supervised baselines. |

---

## 3. Repository Resolution Status

Table 3 records the HTTP status returned for each repository when the register was compiled, together with the commit at which the repository was inspected during Stage 2. Pinning the commit is what makes every code-derived claim in the Stage 2 deliverables independently re-checkable: a reader can check out the identical tree and reproduce the reading.

**Table 3 — Resolution status (29 August 2026) and Stage 2 inspection commits (22 August 2026).**

| Repository | HTTP status, 29 Aug 2026 | Commit inspected (full SHA) | Last commit at inspection |
|---|---|---|---|
| `cszn/DnCNN` | 200 | `e93b27812d3ff523a3a79d19e5e50d233d7a8d0a` | 2021-10-10 |
| `cszn/KAIR` | 200 | `fc1732f4a4514e42ce15e5b3a1e18c828af47a1e` | 2024-10-02 |
| `swz30/Restormer` | 200 | `68dc6ac472db26f16361150cb7a96a1bc87da93f` | 2025-10-23 |
| `megvii-research/NAFNet` | 200 | `2b4af71ebe098a92a75910c233a3965a3e93ede4` | 2024-03-29 |
| `cszn/SCUNet` | 200 | `52e440a80a655b01e0b41e9dd9bfe599bc11625e` | 2023-12-15 |
| `csguoh/MambaIR` | 200 | `33d7b3460c4665229334cc8de38c7f4c766ed3be` | 2026-06-03 |
| `Li-Tong-621/P2N-plus` | 200 | `8a117dbde427f73d618cfd2675cc2eaa34746ef3` | 2025-11-01 |
| `Li-Tong-621/P2N` | **404** | Not clonable | — |
| `Li-Tong-621/Tool-for-SSSID` | 200 | Not inspected | — |
| `NVlabs/noise2noise` | 200 | Not inspected in Stage 2 | — |
| `juglab/n2v` | 200 | Not inspected in Stage 2 | — |
| `csjunxu/WNNM_CVPR2014` | 200 | Not inspected in Stage 2 | — |
| `VLOGroup/denoising-variationalnetwork` | 200 | Not inspected in Stage 2 | — |

The seven repositories carrying a commit SHA are those cloned for the Stage 2 code deep-dive. The remaining entries were resolved for this register only; no claim in any deliverable currently rests on their contents.

---

## 4. Category B — Auxiliary Sources

**Table 4 — Category B sources.**

| ID | Source | Type | Author / publisher | Date | URL |
|---|---|---|---|---|---|
| B1 | CS231n: Convolutional Neural Networks for Visual Recognition | Recognised academic lecture series | Stanford University | Ongoing | `https://cs231n.stanford.edu/` |
| B2 | Night Sight: Seeing in the Dark on Pixel Phones | Industry research blog | M. Levoy and Y. Pritch, Google Research | November 2018 | `https://research.google/blog/night-sight-seeing-in-the-dark-on-pixel-phones/` (originally published at `https://ai.googleblog.com/2018/11/night-sight-seeing-in-dark-on-pixel.html`) |
| B3 | *Digital Image Processing* — Image Restoration chapter | Textbook chapter | R. C. Gonzalez and R. E. Woods | Edition to be confirmed | — |

None of the Category B sources ships a reference implementation, and none is cited in support of a code-derived claim.

---

## 5. Verification Caveats

The following items are recorded so that no statement in this register is mistaken for a stronger claim than the evidence supports.

1. **The P2N code URL printed in the published paper is dead.** The CVPR 2025 paper states that its code is released at `https://github.com/Li-Tong-621/P2N`. That address returned HTTP 404 on 22 August 2026 and again on 29 August 2026, and `git clone` against it fails authentication, which is GitHub's standard response for a non-existent or private repository. The code that exists is `Li-Tong-621/P2N-plus`, corresponding to the journal extension; its released checkpoint is named `results/P2N_TPAMI.pt`. This discrepancy is itself a Stage 2 finding about reproducibility, not merely a bibliographic inconvenience.

2. **ZS-N2N has no repository.** Its entire released implementation is a Colab notebook. Any statement about "the ZS-N2N repository" would be incorrect.

3. **A2 and A3 are not served by author-maintained repositories.** The WNNM entry is a third-party mirror and the TNRD entry is a re-implementation produced by the co-author's own laboratory for a different publication. Neither should be cited as the authors' released artefact.

4. **A3 carries two plausible years.** The TPAMI issue in which TNRD appears is dated 2017, while the IEEE early-access record and several reference lists give 2016. The Stage 1 deliverables use 2017. This should be confirmed against the IEEE Xplore record before the defence and cited consistently.

5. **A10 is published in a venue outside the brief's named list.** *Machine Intelligence Research* does not appear among IEEE TPAMI, CVPR, ICCV, ECCV, NeurIPS or MICCAI. Instructor confirmation that the venue is acceptable remains outstanding.

6. **No citation counts are recorded in this register.** None were re-verified on the compilation date. When citation counts are required, they must be taken from Google Scholar rather than Semantic Scholar — the two are not interchangeable and the latter reports materially lower figures — and the source and retrieval date must be stated alongside the number.

7. **Framework attributions describe the released code, not the paper.** For example, DnCNN is listed as MATLAB/MatConvNet because that is what `cszn/DnCNN` contains; the PyTorch implementation used in Stage 2 came from the same author's KAIR toolbox, which is listed separately for that reason.
