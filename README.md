# Image Denoising — From Foundations to State-of-the-Art

**Course:** Digital Image Processing · **Supervisor:** Prof. Zohreh Azimifar
**Topic:** Image Denoising · **Anchor paper:** DnCNN — Zhang et al., *Beyond a Gaussian Denoiser: Residual Learning of Deep CNN for Image Denoising*, IEEE TIP 2017 ([arXiv:1608.03981](https://arxiv.org/abs/1608.03981))

> **Current stage: Stage 1 — Exhaustive Literature Review & Timeline Construction**

---

## 1. What this project is

The objective is to track the evolution of one image-processing topic from its classical DIP origins to its current state of the art. We act as domain experts on **image denoising**: we trace how the problem was solved with classical mathematics, why those methods hit a wall, how deep learning broke through, and where the field stands today.

The project is graded across three sequential stages, each ending in a live defense session with the Teaching Assistants. The final artifact is a single master slide deck dense enough to serve as a 2–4 hour masterclass — a standalone educational resource, not a set of paper summaries stapled together.

**The narrative spine:**

```
Spatial filtering  →  NLM / BM3D / WNNM  →  CSF / TNRD  →  DnCNN  →  Transformer-era restoration
   (classical)        (non-local priors)      (bridge)      (deep CNN)         (modern SOTA)
```

---

## 2. Deadlines

All three checkpoints fall inside a single month. Dates are given in the Gregorian calendar, the Solar Hijri (Persian) calendar, and the Lunar Hijri calendar.

| # | Checkpoint | Gregorian | Solar Hijri (شمسی) | Lunar Hijri (قمری) |
|---|---|---|---|---|
| 1 | Literature Review Pitch | Tue, 11 Aug 2026 | سه‌شنبه، ۲۰ مرداد ۱۴۰۵ | 28 Ṣafar 1448 |
| 2 | Practical Engineering & Code Analysis | Fri, 21 Aug 2026 | جمعه، ۳۰ مرداد ۱۴۰۵ | 8 Rabīʿ al-Awwal 1448 |
| 3 | Final Project Defense | Mon, 31 Aug 2026 | دوشنبه، ۹ شهریور ۱۴۰۵ | 18 Rabīʿ al-Awwal 1448 |

**Today:** 2 Aug 2026 · ۱۱ مرداد ۱۴۰۵ · 19 Ṣafar 1448 — **9 days to Checkpoint 1.**

> The Lunar Hijri dates above are computed from the tabular/Umm al-Qurā calendar. Locally announced dates may differ by ±1 day depending on moon sighting. Only the Gregorian dates are stated in the assignment brief; the other two columns are conversions provided for convenience.

---

## 3. What we need to do — Stage 1

Stage 1 maps the academic landscape of the topic: how it was solved in the past with classical DIP, the bottlenecks that arose, and how modern researchers solve it today.

### 3.1 Source quota

A minimum of **10 distinct, high-quality sources**, curated, read, and analysed — split by category:

| Category | Share | What counts |
|---|---|---|
| **A** | **minimum 70%** | Peer-reviewed papers from top-tier venues (IEEE TPAMI, CVPR, ICCV, ECCV, NeurIPS, MICCAI). Must mix older milestone papers **and** recent SOTA from 2022–present. |
| **B** | **maximum 30%** | Textbook chapters, recognised academic lectures (Stanford CS231n, MIT OpenCourseWare), or highly technical developer blogs from industry leaders (Google Research, Meta AI). |

Round Category A **up** — 70% is a floor, not a target. At 10 sources that means 7 A / 3 B; at 15 sources, 11 A / 4 B.

### 3.2 The goal

Do **not** merely summarise the papers. Establish a chronological *and* thematic connection between them, explicitly showing the path from classical algorithms to modern SOTA — how the field transitioned from spatial filtering to CNNs and eventually to Vision Transformers. Each source needs a one-line answer to two questions: *why did this exist?* and *why was it superseded?*

### 3.3 Deliverable

A short pitch deck (**not** the master deck) containing:

- [ ] The selected topic, stated explicitly and confirmed with the TA
- [ ] The exact list of 10+ sources, with the A/B split visible so the ratio is verifiable at a glance
- [ ] A visual timeline mapping algorithm evolution (`Classical Math → CNN → Transformer`)
- [ ] The evolutionary narrative stated explicitly, not merely implied by the ordering

The TAs evaluate the rigour of the chosen papers, verify the 70/30 split, and approve the research direction.

---

## 4. Current status



---

## 5. Task board — Stage 1

| # | Task | Owner | Status |
|---|---|---|---|
| 1 | Confirm topic in writing with the TA | | ☐ |
| 2 | Freeze the classical half (BM3D, NLM, WNNM, CSF, TNRD, DnCNN) with per-source notes | | ☐ |
| 3 | Hunt 4–6 papers from 2022+ in CVPR / ICCV / ECCV / NeurIPS / TPAMI proceedings | | ☐ |
| 4 | Verify venue + year + authors for every new entry | | ☐ |
| 5 | Add 2–3 Category B sources | | ☐ |
| 6 | Compute and display the final A/B ratio | | ☐ |
| 7 | Build the visual timeline slide | | ☐ |
| 8 | Assemble and rehearse the pitch deck | | ☐ |



---

## 6. Working rules

1. **Nothing goes on a slide that a group member cannot personally explain.** At Checkpoint 3 the TAs may question us on any slide in the full deck, including ones we never present — so the habit starts now.
2. **No unverified citations.** If a venue or year cannot be confirmed from the proceedings or the authors' page, the source does not go in the list.
3. **Provenance stays visible.** Notes should distinguish what comes from the assignment brief, from a paper, and from our own analysis.

