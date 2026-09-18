# -*- coding: utf-8 -*-
S = []

# ══════════════════════════ PART VII ══════════════════════════
S.append(dict(t="section", era="meta", part="VII", kicker="Part VII",
    title="Comparative Analysis",
    lead="Eighteen years of numbers, assembled under rules strict enough that the comparison means something.",
    body={"items": ["The rules we followed", "BSD68 — the long ladder", "Urban100 — where the gap is",
                    "Real noise — where the assumption breaks", "Efficiency", "Supervision cost",
                    "The whole arc in one view"]},
    cite="brief §6", notes="Open with the rules slide, not with a table. Numbers assembled without a stated methodology are the easiest thing in a deck to attack."))

S.append(dict(t="content", era="meta", part="VII", kicker="72 · Methodology",
    title="Five rules, so that the comparison survives scrutiny",
    lead="Cross-paper PSNR tables are the most commonly abused artefact in this field. These are the constraints we imposed on ourselves, and they are worth stating before any number appears.",
    body={"bullets": [
        "**1 · No number was computed by us.** Every PSNR and SSIM in Part VII is reproduced from a published table, with the paper and table named. We ran no denoising evaluation of our own, because doing it correctly would require matching each paper's crop, border, colour-space and rounding conventions — and a table that mixes our numbers with theirs would be worse than useless.",
        "**2 · Rows come from one table wherever possible.** When comparing DnCNN to Restormer, both figures are taken from Restormer's Table 4, where the authors evaluated both under one protocol. Taking DnCNN's number from its own paper and Restormer's from its own would silently compare two different evaluation scripts.",
        "**3 · Timings and quality are never mixed in one column.** Every quality number is from a paper; every latency and parameter count is from our own measurements on stated hardware. The two are reported in separate tables and labelled.",
        "**4 · Device asymmetries are stated.** The DnCNN runtime table compares CPU figures for classical methods against GPU figures for learned ones, and the paper itself flags that GPU times were copied from other papers. We reproduce the caveat every time we reproduce the numbers.",
        "**5 · Where a figure could not be verified, it is absent.** We found one probable extraction error in a published table we could not confirm (MambaIR's CBSD68 σ=25 cell, which breaks the pattern of its own row). That cell is excluded from every chart in this deck rather than reproduced with a footnote.",
    ]},
    cite="reading — methodology adopted for this deck",
    notes="Rule 2 is the one a careful TA will care about most, and rule 5 is the one that demonstrates you actually read the tables rather than copied them."))

S.append(dict(t="table", era="meta", part="VII", kicker="73 · The long ladder",
    title="BSD68 grayscale — eighteen years, one benchmark",
    lead="Average PSNR in dB. The 2007–2017 block is from DnCNN Table II; the 2017–2022 block is from Restormer Table 4, which re-evaluated DnCNN under its own protocol. The two DnCNN rows differ slightly for exactly that reason, and that difference is itself worth knowing.",
    body={"cols": ["Method", "Year", "Era", "σ = 15", "σ = 25", "σ = 50", "Source"],
          "align": "lllrrrl",
          "rows": [
            ["BM3D", "2007", "Classical", "31.07", "28.57", "25.62", "DnCNN T2"],
            ["EPLL", "2011", "Classical", "31.21", "28.68", "25.67", "DnCNN T2"],
            ["MLP", "2012", "Early learning", "—", "28.96", "26.03", "DnCNN T2"],
            ["WNNM", "2014", "Classical peak", "31.37", "28.83", "25.87", "DnCNN T2"],
            ["TNRD", "2016", "Bridge", "31.42", "28.92", "25.97", "DnCNN T2"],
            ["**DnCNN**", "2017", "Deep CNN", "**31.73**", "**29.23**", "**26.23**", "DnCNN T2"],
            ["DnCNN (re-evaluated)", "2017", "Deep CNN", "31.62", "29.16", "26.23", "Restormer T4"],
            ["FFDNet", "2018", "Deep CNN", "31.63", "29.19", "26.29", "Restormer T4"],
            ["DRUNet", "2021", "Deep CNN", "31.91", "29.48", "26.59", "Restormer T4"],
            ["SwinIR", "2021", "Transformer", "31.97", "29.50", "26.58", "Restormer T4"],
            ["**Restormer**", "2022", "Transformer", "**31.96**", "**29.52**", "**26.62**", "Restormer T4"],
          ],
          "hl": [5, 10]},
    foot="**Read the σ = 25 column as a single story.** 2007 → 2014, seven years of hand-designed priors: **+0.26 dB**. 2014 → 2017, one architectural idea: **+0.40 dB**. 2017 → 2022, five years and an entire Transformer revolution: **+0.36 dB**. On ordinary natural images the field is deep into diminishing returns, and has been since roughly 2018. **This table is the argument that BSD68 has stopped being informative** — which is why the next two slides exist.",
    cite="DnCNN17 Table II · Restormer22 Table 4 — source column names the origin of every row",
    notes="The saturation reading is the intellectually honest one and it sets up slides 74 and 75. Do not present this table as 'and progress continued'. Present it as 'and here is where the benchmark died'."))

S.append(dict(t="stats", era="arch", part="VII", kicker="74 · Where the gap actually is",
    title="Urban100 — the same five years, five times the gain",
    lead="Identical models, identical table, identical noise level. The only thing that changes is the dataset — from ordinary natural images to photographs of buildings, where structure repeats across hundreds of pixels.",
    body={"stats": [
        {"n": "+0.39 dB", "l": "BSD68, σ = 50 · DnCNN → Restormer", "s": "26.23 → 26.62. Ordinary natural images, little long-range repetition. Five years of architectural work buys almost nothing."},
        {"n": "+1.98 dB", "l": "Urban100, σ = 50 · DnCNN → Restormer", "s": "26.35 → 28.33. Highly repetitive urban structure. The same five years buy **five times as much**."},
        {"n": "−0.71 dB", "l": "Barbara, σ = 25 · DnCNN vs BM3D, 2017", "s": "30.00 vs 30.71. The identical phenomenon, visible in the anchor paper's own table five years earlier — on the one image in Set12 whose texture repeats."},
    ],
     "bullets": [
        "**These three numbers are the same fact, measured three times across eight years.** A convolutional network with a 35×35 receptive field cannot exploit self-similarity beyond 35 pixels. Non-local classical methods could. Attention gave it back.",
        "**The corollary, which is the more useful claim.** The modern architecture branch did not make denoising uniformly better. It made denoising better **specifically where non-locality matters**. Aggregate benchmark numbers conceal this completely, which is why a per-dataset reading is not pedantry — it is the only way to see what actually changed.",
        "**And it explains why BSD68 saturated.** BSD68 contains relatively little long-range repetition, so it measures a capability the field stopped competing on around 2018 while being blind to the one it moved to.",
    ]},
    cite="Restormer22 Table 4 (BSD68 and Urban100 columns) · DnCNN17 Table III (Barbara) — ratio computed by us from published values",
    notes="This is the analytical high point of Part VII. It is your own analysis of published numbers, which is exactly what 'synthesis' means in the grading criteria. Say 'computed from Table 4' so the provenance is unambiguous."))

S.append(dict(t="table", era="meta", part="VII", kicker="75 · The assumption breaks",
    title="Real sensor noise — and a 16 dB collapse",
    lead="SIDD and DND contain photographs of real scenes taken with real smartphone cameras, where noise is signal-dependent, spatially correlated, and processed by an imaging pipeline. Both tables below are from Restormer's Table 6, evaluated under one protocol.",
    body={"cols": ["Method", "Type", "SIDD PSNR", "SIDD SSIM", "DND PSNR", "DND SSIM"],
          "align": "llrrrr",
          "rows": [
            ["**DnCNN**", "AWGN-trained CNN, 2017", "**23.66**", "0.583", "**32.43**", "0.790"],
            ["BM3D", "Classical, 2007", "25.65", "0.685", "34.51", "0.851"],
            ["CBDNet*", "Real-noise CNN, 2019", "30.78", "0.801", "38.06", "0.942"],
            ["MPRNet", "Multi-stage CNN, 2021", "39.71", "0.958", "39.80", "0.954"],
            ["Uformer", "Transformer, 2022", "39.77", "0.959", "39.96", "0.956"],
            ["**Restormer**", "Transformer, 2022", "**40.02**", "**0.960**", "40.03", "0.956"],
            ["NAFNet", "Convolutional, 2022", "**40.30**", "—", "—", "—"],
            ["MambaIR", "State-space, 2024", "39.89", "0.960", "**40.04**", "0.956"],
          ],
          "hl": [0, 5, 6]},
    foot="**The single most important number in this deck: 23.66 dB.** DnCNN — which beats BM3D by 0.6 dB on synthetic Gaussian noise — is beaten by BM3D by **1.99 dB** on real sensor noise, and trails Restormer by **16.36 dB**. A model trained on the wrong noise distribution does not degrade gracefully; it collapses. This is exactly what SCUNet means by *noise assumption mismatch*, and it is why the field's centre of gravity moved from AWGN benchmarks to real-noise benchmarks between 2019 and 2022. *NAFNet's 40.30 dB is from its own abstract, evaluated on SIDD under the same benchmark but not in Restormer's table; the asterisk marks methods using additional training data.",
    cite="Restormer22 Table 6 · NAFNet22 abstract · MambaIR24 Table 6 · SCUNet23 §1",
    notes="Lead the condensed 30-minute presentation's comparative section with this slide, not with BSD68. 23.66 against 40.02 is the number that makes the whole evolutionary argument land in one breath."))

S.append(dict(t="table", era="meta", part="VII", kicker="76 · Efficiency",
    title="Cost, measured three different ways — with three different answers",
    lead="Quality is only half of a comparison. The left block is reproduced from the DnCNN paper; the right block is our own measurement. They are kept separate deliberately, per rule 3.",
    body={"cols": ["Method", "Era", "Published 512² runtime", "Device", "Parameters [measured]", "CPU 256² [measured]"],
          "align": "lllllr",
          "rows": [
            ["WNNM", "Classical peak", "773.2 s", "CPU", "— (no network)", "—"],
            ["EPLL", "Classical", "45.5 s", "CPU", "— (no network)", "—"],
            ["BM3D", "Classical", "2.85 s", "CPU", "— (no network)", "—"],
            ["TNRD", "Bridge", "1.33 s / 0.032 s", "CPU / GPU", "— (not run)", "—"],
            ["DnCNN-B", "Deep CNN", "4.11 s / 0.060 s", "CPU / GPU", "0.668 M", "1.015 s"],
            ["P2N+ backbone", "Data branch", "— (not published)", "—", "0.991 M", "0.286 s"],
            ["SCUNet", "Architecture", "— (not published)", "—", "9.663 M", "1.685 s"],
            ["Restormer", "Architecture", "— (not published)", "—", "26.127 M", "10.436 s"],
            ["NAFNet", "Architecture", "— (not published)", "—", "115.983 M", "1.899 s"],
          ]},
    foot="**Three incompatible rankings from one set of models.** By **parameters**, DnCNN is best and NAFNet is worst by 174×. By **CPU wall-clock**, P2N+'s backbone is best and Restormer is worst by 36×. By **quality on real noise**, NAFNet is best and DnCNN is worst by 16 dB. There is no single efficiency axis, and a paper that reports only one has chosen the one that flatters it. Restormer's own claim — **3.14× fewer FLOPs and 13× faster than SwinIR** — is a fourth axis again.",
    cite="DnCNN17 Table IV · measured, Stage 2 · Restormer22 §4.4",
    notes="The three-incompatible-rankings observation is a good closing line for the efficiency discussion and a genuinely useful thing for the TA to hear."))

S.append(dict(t="table", era="data", part="VII", kicker="77 · The other axis",
    title="What supervision costs, in decibels",
    lead="Parts IV and V are usually compared on quality alone, which misses the point of Part IV entirely. The right comparison sets quality against *what the method demands of you before it will run at all*.",
    body={"cols": ["Method", "What it requires", "BSD68 σ=25", "Source"],
          "align": "llrl",
          "rows": [
            ["Supervised U-Net (traditional)", "Paired clean + noisy images", "29.06", "N2V19 Fig. 4"],
            ["DnCNN-S", "Paired clean + noisy images", "29.23", "DnCNN17 T2"],
            ["Noise2Noise", "Two independent noisy copies per scene", "28.86", "N2V19 Fig. 4"],
            ["BM3D", "**Nothing** — no training at all", "28.57 / 28.59", "DnCNN17 T2 / N2V19"],
            ["Noise2Void", "A body of single noisy images", "27.71", "N2V19 Fig. 4"],
          ],
          "hl": [3]},
    foot="**Read the whole ladder in one sentence.** Giving up the clean target costs about **0.20 dB** (29.06 → 28.86). Giving up the second noisy copy costs a further **1.15 dB** (28.86 → 27.71) and drops below a 2007 algorithm. **But on cryo-TEM and the Cell Tracking Challenge datasets, the three rows above Noise2Void simply do not exist** — the paper's own figure captions the ground-truth column *does not exist*. Where clean data is available, supervision wins. Where it is not, the comparison is not between 27.71 and 29.23; it is between 27.71 and nothing.",
    cite="N2V19 §4.1 and Fig. 4 · DnCNN17 Table II — all values as printed",
    notes="Note the two BM3D figures, 28.57 and 28.59, from two different papers on the same dataset and noise level. Mentioning that discrepancy unprompted is a small, cheap demonstration of care."))

S.append(dict(t="table", era="meta", part="VII", kicker="78 · Synthesis",
    title="Eighteen years, seven methods, one table",
    lead="The comparative analysis compressed to the rows that carry the argument. Read down the last two columns: the story is not that the numbers went up, but that *what they are measuring* changed.",
    body={"cols": ["Method", "Year", "Where the prior lives", "BSD68 σ=50", "Urban100 σ=50", "SIDD (real)"],
          "align": "lllrrr",
          "rows": [
            ["BM3D", "2007", "Hand-written: NSS + 3-D sparsity", "25.62", "—", "25.65"],
            ["WNNM", "2014", "Hand-written: NSS + low rank", "25.87", "—", "—"],
            ["TNRD", "2016", "Learned, inside a fixed PDE", "25.97", "—", "—"],
            ["**DnCNN**", "2017", "Learned, in 0.67 M weights", "**26.23**", "26.35", "**23.66**"],
            ["DRUNet", "2021", "Learned, multi-scale CNN", "26.59", "27.96", "—"],
            ["**Restormer**", "2022", "Learned, channel attention", "**26.62**", "**28.33**", "**40.02**"],
            ["NAFNet", "2022", "Learned, no attention at all", "—", "—", "**40.30**"],
            ["MambaIR", "2024", "Learned, state-space scan", "—", "—", "39.89"],
          ],
          "hl": [3, 5]},
    foot="**Three readings, and they are the conclusion of Part VII.** (1) On BSD68 the field gained **1.00 dB in fifteen years** and has plainly saturated. (2) On Urban100 it gained **1.98 dB in five years**, because that benchmark measures the capability the field actually moved to. (3) On real noise it gained **16.64 dB**, because the first four rows were answering a question — remove AWGN — that real photographs never asked. **Progress in denoising since 2017 is mostly not progress on the 2017 problem.**",
    cite="DnCNN17 Table II · Restormer22 Tables 4 and 6 · NAFNet22 abstract · MambaIR24 Table 6 · dashes mark values not reported in the cited tables",
    notes="The closing sentence is the single strongest line in the deck. Deliver it, pause, and move on. Do not elaborate."))

# ══════════════════════════ PART VIII ══════════════════════════
S.append(dict(t="section", era="meta", part="VIII", kicker="Part VIII",
    title="Open Problems & Conclusion",
    lead="What eighteen years did not solve, and what we would build tomorrow morning.",
    body={"items": ["Real noise modelling", "The perception–distortion trade-off", "Efficiency and deployment",
                    "Evaluation itself", "Self-supervision's remaining gap", "What we would build today",
                    "The thesis, restated"]},
    cite="brief §7", notes="Keep this part fast. Its function is to prove the field is alive, not to survey it."))

S.append(dict(t="cards", era="meta", part="VIII", kicker="79 · Unsolved, 1 and 2",
    title="Real noise, and the perception–distortion trade-off",
    lead="The two open problems for which this deck already contains hard evidence, rather than speculation.",
    body={"cards": [
        {"tag": "Open problem 1", "h": "A general-purpose blind real denoiser", "p": "SCUNet's abstract states the position as of 2023: *a general-purpose blind denoising method for real images remains unsolved.* The evidence on slide 75 is stark — DnCNN scores 23.66 dB on SIDD. SCUNet's answer is to synthesise realistic degradations; Restormer and NAFNet's answer is to train directly on SIDD's 320 captured scenes. **Neither generalises to an unseen camera with an unseen ISP**, and no benchmark currently measures that."},
        {"tag": "Why it is hard", "h": "Noise is a pipeline, not a distribution", "p": "Real noise is read noise plus shot noise in the raw domain, then transformed by demosaicing, white balance, colour conversion, tone mapping and gamma — each of which correlates it spatially and across channels. SCUNet models this by *inverting* the ISP, adding noise in raw, and running it forward again. That is an engineering simulation of a physical device, not a probability model, and it is as good as the device model it assumes."},
        {"tag": "Open problem 2", "h": "Fidelity metrics reward blur", "p": "Every loss in Part VI is L1, L2 or PSNR. All three recover a conditional mean, and the conditional mean of the plausible clean images is smoother than any of them. **Noise2Noise names this mechanism explicitly:** an L2-trained regressor *learns to output the average of all plausible explanations, which results in spatial blurriness*. The field's default objective is structurally biased toward the very over-smoothing that BM3D was criticised for."},
        {"tag": "Why it persists", "h": "The metric constrains the loss", "p": "Perceptual and adversarial losses would fix the blur and would score *worse* on PSNR, because they hallucinate plausible texture that does not match the ground truth pixel for pixel. As long as leaderboards are PSNR-ranked, the incentive points the wrong way. This is why, as slide 67 observes, perceptual losses are common in super-resolution and essentially absent from denoising."},
    ]},
    cite="SCUNet23 abstract, §3.2 · N2N18 §2 · Restormer22 Table 6 · reading",
    notes="The observation that Noise2Noise names the blur mechanism while proposing an L2 method is a nice piece of close reading. It is in §2 of the paper, in the super-resolution example."))

S.append(dict(t="cards", era="meta", part="VIII", kicker="80 · Unsolved, 3 to 5",
    title="Efficiency, evaluation, and the self-supervision gap",
    lead="Three further open problems, each of which this deck has produced direct evidence for rather than inherited from a survey.",
    body={"cards": [
        {"tag": "Open problem 3", "h": "Nobody agrees what efficient means", "p": "Slide 76 produced three incompatible rankings of the same models from parameters, wall-clock and quality — and Restormer's FLOP claim is a fourth. MambaIR's own changelog concedes its published `thop` complexity figures were wrong. **The field has no agreed cost metric**, which makes efficiency claims across papers close to meaningless and is why our benchmark reports the counting method alongside every number."},
        {"tag": "Open problem 4", "h": "The benchmarks have saturated", "p": "BSD68 σ=25 moved 0.36 dB in the five years from DnCNN to Restormer, while Urban100 moved five times as much and SIDD moved sixteen decibels. A benchmark that cannot distinguish 2017 from 2022 is no longer measuring the thing the field is working on. **New capability is arriving faster than the instruments to detect it.**"},
        {"tag": "Open problem 5", "h": "Self-supervision has not met supervision", "p": "N2V trails supervised training by 1.35 dB on BSD68 and sits below BM3D. P2N's contribution is removing the *information loss*, not closing the quality gap, and it still pays per-image test-time optimisation. **Bottleneck 2 is mitigated, not closed** — and the domains that need it most, microscopy and medical imaging, are precisely those where no clean reference exists to measure the remaining gap."},
        {"tag": "Open problem 6", "h": "The two branches have never merged", "p": "This is our own observation and the structural claim of the deck. P2N ships the 2018 Noise2Noise U-Net verbatim; Restormer, NAFNet and MambaIR all assume paired data. **Nobody has published a state-space or Transformer backbone trained by RDC/DCS supervision.** Whether the branches compose or conflict is, as far as we found, an open and apparently untested question."},
    ]},
    cite="measured, Stage 2 · N2V19 §4.1 · P2N25 · Restormer22 Table 4 · reading",
    notes="Open problem 6 is the one to offer if asked 'what would you research?'. It falls directly out of your own two-branch framing and is a genuine, specific, testable gap."))

S.append(dict(t="flow", era="meta", part="VIII", kicker="81 · The practical answer",
    title="What we would deploy, and on what evidence",
    lead="The brief asks what the current industry and academic standard is. The honest answer is that it depends on one constraint, and the fork in this deck's timeline predicts which.",
    body={"steps": [
        {"h": "Real photographs, GPU available, paired data exists", "p": "**NAFNet.** 40.30 dB on SIDD, best accuracy-per-millisecond measured, and by a wide margin the simplest code in Part VI — no attention, no activation functions. `[NAFNet22 abstract; measured 1.90 s CPU at 256²]`"},
        {"h": "CPU-bound or memory-bound deployment", "p": "**SCUNet.** 9.663 M parameters, smallest of the architecture branch, and its synthetic-degradation training makes the blind weights unusually robust on photographs that were resized or JPEG-compressed before you ever saw them. `[measured; SCUNet23 §3.2]`"},
        {"h": "Maximum quality on repetitive structure", "p": "**Restormer**, or MambaIR if CUDA is guaranteed. Restormer leads Urban100 at every noise level and is the only model past 40 dB on both SIDD and DND; MambaIR takes DND by 0.01 dB. Accept 10.4 s per 256² image on CPU. `[Restormer22 T4, T6; MambaIR24 T6; measured]`"},
        {"h": "No clean data exists at all", "p": "**P2N**, or ZS-N2N for a single image with no training corpus and a minute of CPU. Accept per-image test-time optimisation as the price, and accept a quality gap to supervised training that is real and measured. `[P2N25; ZS-N2N23 §3]`"},
        {"h": "A fast, dependency-free baseline", "p": "**BM3D.** Seventeen years old, needs no data and no GPU, still appears as a live baseline in 2023 papers, and still beats an AWGN-trained DnCNN on real sensor noise by 1.99 dB. `[Restormer22 T6]`"},
    ],
     "bullets": [
        "**Notice what this list does not contain: a winner.** Five constraints, five different answers, all current. That is not indecision — it is what an unresolved research question looks like when you have to ship something on Monday.",
    ]},
    cite="NAFNet22 · SCUNet23 · Restormer22 · MambaIR24 · P2N25 · ZS-N2N23 · measured",
    notes="Strongest possible answer to 'which one would you use?'. Never answer that question with a single model name — answer it with the constraint that decides."))

S.append(dict(t="quote", era="meta", part="VIII", kicker="82 · Conclusion",
    title="The thesis, restated",
    lead="",
    body={"q": "Image denoising is the cleanest available case study in how computer vision replaced hand-designed priors with learned ones.\n\nIts history divides into four eras separated by three identifiable bottlenecks — manual prior design, the clean-data requirement, and the receptive-field limits of convolution. Each bottleneck was named by the paper that broke it, so the arc is evidenced from the primary sources rather than imposed in hindsight.\n\nIn 2018 the response forked. One branch changed what the network is shown; the other changed what the network is. They have never merged.\n\nAnd because the field currently holds three competing answers to the third bottleneck and none to the first open problem, the story ends in a genuine open question rather than a winner.",
     "attrib": "The claim this deck has spent 122 slides evidencing."},
    cite="reading — the organising claim, carried since Stage 1",
    notes="Deliver this from memory with the slide behind you. Roughly fifty seconds. It is the last substantive thing the TAs hear before questions begin, which makes it the part most worth rehearsing word for word."))

# ══════════════════════════ BACK MATTER ══════════════════════════
S.append(dict(t="table", era="meta", part="", kicker="83 · Bibliography",
    title="Category A — twelve peer-reviewed papers",
    lead="Citation counts are Google Scholar figures checked on 9 August 2026, except P2N, which was not verified and is marked accordingly. Counts move continuously; the date is quoted alongside every figure.",
    body={"cols": ["#", "Paper", "Authors", "Venue & year", "Cited by"],
          "align": "lllll",
          "rows": [
            ["A1", "Image Denoising by Sparse 3-D Transform-Domain Collaborative Filtering (**BM3D**)", "Dabov, Foi, Katkovnik, Egiazarian", "IEEE TIP 16(8), 2007", "11 976"],
            ["A2", "Weighted Nuclear Norm Minimization with Application to Image Denoising (**WNNM**)", "Gu, Zhang, Zuo, Feng", "CVPR 2014", "2 960"],
            ["A3", "Trainable Nonlinear Reaction Diffusion (**TNRD**)", "Chen, Pock", "IEEE TPAMI 39(6), 2017", "1 626"],
            ["A4", "Beyond a Gaussian Denoiser: Residual Learning of Deep CNN (**DnCNN**)", "Zhang, Zuo, Chen, Meng, Zhang", "IEEE TIP 26(7), 2017", "11 674"],
            ["A5", "Noise2Noise: Learning Image Restoration without Clean Data", "Lehtinen, Munkberg, Hasselgren, Laine, Karras, Aittala, Aila", "ICML 2018", "3 064"],
            ["A6", "Noise2Void — Learning Denoising from Single Noisy Images", "Krull, Buchholz, Jug", "CVPR 2019", "2 075"],
            ["A7", "Restormer: Efficient Transformer for High-Resolution Image Restoration", "Zamir, Arora, Khan, Hayat, Khan, Yang", "CVPR 2022", "6 181"],
            ["A8", "Simple Baselines for Image Restoration (**NAFNet**)", "Chen, Chu, Zhang, Sun", "ECCV 2022", "2 318"],
            ["A9", "Zero-Shot Noise2Noise: Efficient Image Denoising without any Data", "Mansour, Heckel", "CVPR 2023", "266"],
            ["A10", "Practical Blind Image Denoising via Swin-Conv-UNet and Data Synthesis (**SCUNet**)", "Zhang, Li, Liang, Cao, Zhang, Tang, Fan, Timofte, Van Gool", "Machine Intelligence Research 20(6), 2023", "391"],
            ["A11", "MambaIR: A Simple Baseline for Image Restoration with State-Space Model", "Guo, Li, Dai, Ouyang, Ren, Xia", "ECCV 2024", "1 208"],
            ["A12", "Positive2Negative: Breaking the Information-Lossy Barrier in Self-Supervised Single Image Denoising (**P2N**)", "Li, Wang, Xu, Zhu, Lu, Huang", "CVPR 2025, pp. 17924–17934", "not verified"],
          ]},
    foot="**Two observations worth making aloud rather than leaving in the table.** BM3D and DnCNN sit near twelve thousand citations each, which is precisely why both remain universal baselines nineteen and nine years after publication — the counts corroborate the narrative rather than decorating it. Conversely ZS-N2N at 266 and SCUNet at 391 are low because they are recent, not because they are weak; recency and citation count are confounded, and saying so pre-empts the obvious challenge.",
    cite="Google Scholar, checked 9 August 2026 · venues verified per slide 85",
    notes="Recheck the counts the morning of the defence, and update the date. If a TA asks why P2N has no count, say it was not verified and you do not report unverified numbers."))

S.append(dict(t="content", era="meta", part="", kicker="84 · Bibliography",
    title="Category B — three auxiliary sources, and why each is here",
    lead="Three of fifteen sources, or 20.0%, against the brief's 30% ceiling. Category A is 80.0%, against a 70% floor. Each Category B item is included because it does something no paper in the roster does.",
    body={"bullets": [
        "**B1 · Stanford CS231n**, *Convolutional Neural Networks for Visual Recognition*. A recognised academic lecture series, explicitly permitted by the brief. It supplies the backpropagation, convolution-arithmetic and optimisation background that every Category A paper from A4 onward assumes without stating. **Role in the narrative:** it is the reason slides 29–31 can discuss receptive fields and batch normalisation as shared vocabulary rather than deriving them.",
        "**B2 · Google Research**, *Night Sight* / HDR+ technical blog. A highly technical developer publication from an industry leader, explicitly permitted by the brief. It separates photon shot noise from read noise, explains that SNR rises with the square root of exposure time, and describes how a burst of frames is captured, aligned in software and merged. **Role in the narrative:** it is the only source in the roster describing denoising as a *shipped consumer product*, and it supplies the physical grounding for the real-noise argument on slides 75 and 79.",
        "**B3 · Gonzalez & Woods**, *Digital Image Processing* — the Image Restoration chapter. A textbook chapter, explicitly permitted. It supplies the formal treatment of noise models (Gaussian, Rayleigh, Poisson, salt-and-pepper) and of mean, order-statistic and adaptive filters that Part II's first three slides rest on. **Role in the narrative:** it is the bottom rung of the timeline, below BM3D, and it is the reference against which SCUNet's synthetic degradation pipeline reads critically — SCUNet's noise list is essentially the textbook's noise list, industrialised.",
        "**Verification note.** Chapter number and page range differ between the 3rd and 4th editions of Gonzalez & Woods. Cite the exact edition physically in use.",
        "**The arithmetic.** 15 sources total. 12 Category A = 80.0% (floor 70%). 3 Category B = 20.0% (ceiling 30%). Compliant with margin on both sides.",
    ]},
    cite="brief §2, Source Distribution Rules",
    notes="Each Category B item has a 'role in the narrative' clause. That is what converts a compliance list into evidence of curation, which is what the Rigor of Research criterion actually grades."))

S.append(dict(t="content", era="meta", part="", kicker="85 · Honesty",
    title="Declared limitations — stated, not discovered",
    lead="A gap that is stated is a smaller problem than a gap that is found. These are every known weakness in this deck.",
    body={"bullets": [
        "**No quality metric in this deck was computed by us.** Every PSNR and SSIM is reproduced from a published table. Our own measurements cover parameter counts and CPU forward-pass latency only, and used **random tensors**, so they carry no image-quality information whatsoever.",
        "**CPU latencies are not comparable to published GPU timings.** Only the ratios between our own measurements are meaningful, and they are meaningful only for the CPU backend we used.",
        "**The DnCNN runtime table mixes devices.** Classical methods are timed on CPU, learned methods on GPU, and the paper states that GPU times for CSF and TNRD were copied from their original papers. We reproduce this caveat wherever we reproduce the numbers.",
        "**One published value is excluded.** MambaIR's CBSD68 σ=25 figure extracted as 32.24, which is inconsistent with its own row (34.48 at σ=15, 28.66 at σ=50) and with every comparable method. We judged this a probable extraction error and excluded the cell rather than reproduce it. MambaIR's colour results are quoted from Urban100 instead, which is internally consistent.",
        "**Venue verification.** Venues for BM3D, TNRD, Noise2Noise and SCUNet are printed in the source PDFs themselves. The remaining eight are preprint versions carrying no venue, and were confirmed against publisher, CVF Open Access or institutional proceedings records rather than copied from another paper's reference list.",
        "**TNRD's year is genuinely ambiguous.** The PDF header reads 2016; the citing literature gives TPAMI 39(6), 2017. Both reflect reality — acceptance versus issue. We cite 2017.",
        "**Reference code availability is uneven.** ZS-N2N has no repository, only a Colab notebook. WNNM has only a third-party mirror with no README or licence. TNRD's available implementation is a same-laboratory re-implementation, not the authors' original release. The P2N paper's printed repository URL returns HTTP 404; the live code is at `P2N-plus`.",
        "**SCUNet's venue is not on the brief's named list.** *Machine Intelligence Research* is a peer-reviewed Springer journal but is not among the venues the brief names. The brief's list is illustrative rather than exhaustive; we flag this rather than conceal it.",
    ]},
    cite="reading — self-assessment",
    notes="Volunteer the MambaIR exclusion and the P2N 404 if the conversation allows. Both are small, specific, and demonstrate that you read the primary material rather than aggregated it."))

S.append(dict(t="table", era="meta", part="", kicker="86 · Defence map",
    title="Where to find the answer to the question you are about to be asked",
    lead="The deck is indexed by likely question rather than by topic, because that is how it will be interrogated.",
    body={"cols": ["If they ask…", "Go to", "The one-line answer"],
          "align": "lll",
          "rows": [
            ["Why is 0.6 dB a big deal?", "09, 34", "Prior work put the practical ceiling over BM3D at 0.3 dB and the theoretical bound at 0.7 dB."],
            ["Why residual learning?", "30", "y is closer to x than to v, so F(y) would have to approximate an identity, which is the hard point in parameter space."],
            ["Why do RL and BN need each other?", "31", "RL makes layer inputs Gaussian-like and content-independent, which is what BN's batch statistics require."],
            ["Why depth 17?", "32", "Receptive field (2d+1)² set to 35×35 to match EPLL, the smallest effective patch size in the field."],
            ["Where does DnCNN lose, and why?", "35, 46", "Barbara, −0.71 dB. Repetitive structure meets the non-local prior that a 35×35 field cannot reach."],
            ["How can noisy targets work?", "39", "L2 regression learns the conditional mean, and the conditional mean of a zero-mean corrupted target is the clean target."],
            ["Why does the blind spot not learn identity?", "41", "Neighbours carry no information about a pixel's own noise, given conditional pixel-wise independence."],
            ["Where is Restormer's attention linear?", "63", "`restormer_arch.py`, `Attention.forward` — the `rearrange` puts pixels last, so q@kᵀ is C×C."],
            ["Why is NAFNet faster with more parameters?", "71", "1×1 and depth-wise convolutions hit optimised GEMM paths; `rearrange` forces layout changes."],
            ["What did the code tell you that the papers did not?", "69, 71", "Padding constants differ by 8×; SPI cuts parameters and triples latency; MambaIR will not import without CUDA."],
            ["Which model would you deploy?", "81", "Name the constraint first. Five constraints, five different answers, all current."],
            ["What is still unsolved?", "79, 80", "General blind real denoising, the perception–distortion trade-off, and a cost metric anyone agrees on."],
          ]},
    foot="**The rule for the defence.** Do not put anything on a slide you cannot personally explain. Every slide in this deck was built to be answered from, and the notes field of every slide carries the answer it expects.",
    cite="reading",
    notes="Print this slide. It is the single most useful page to have in front of you while the TAs are asking questions."))
