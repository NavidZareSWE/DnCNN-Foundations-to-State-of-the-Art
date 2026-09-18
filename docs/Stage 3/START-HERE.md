# Stage 3 — Image Denoising: From Foundations to State-of-the-Art

Final deliverable set for the Digital Image Processing final project.
**Presenters:** Navid Zare · Ali Ahmadi · Komeil Khodayar
**Supervisor:** Prof. Zohreh Azimifar · **Defence:** 31 August 2026

## Folder structure

| Folder | Contents |
|---|---|
| `1-deliverable/` | **The graded submission.** `Stage3_Master_Deck.pptx` + `.pdf`, and `Stage3_Report.md`. |
| `2-presentation/` | The 30-minute talk (`Presentation_30min.pptx` / `.pdf` / `.html`) and everything used to prepare and deliver it: `presenter-30min.html`, `master-deck.html`, `companion.html`, `defence.html`. |
| `3-study/` | `oral-exam.html` — the personal study/exam-simulator site. |
| `4-evidence/bench/` | The benchmark script and its raw, recorded output. |
| `5-source/` | The structured decks (`deck.json`, `presentation.json`) and the generator scripts everything above is built from. Not part of the graded submission; kept for reproducibility. |

## Files

| File | What it is | Open it with |
|---|---|---|
| **`1-deliverable/Stage3_Master_Deck.pptx`** | **The graded deliverable** — 100 slides, fully editable | PowerPoint / Keynote / LibreOffice |
| `1-deliverable/Stage3_Master_Deck.pdf` | The same deck as PDF, for submission and printing | any PDF reader |
| `1-deliverable/Stage3_Report.md` | Written master report | any Markdown reader |
| `2-presentation/master-deck.html` | Interactive version of the same 100 slides | any browser |
| `2-presentation/defence.html` | Bilingual EN/FA presenter companion — spoken script + 19-question bank | any browser |
| **`2-presentation/Presentation_30min.pptx`** | **The 30-minute talk.** 32 slides, two presenters, evolution and SOTA focused | PowerPoint / Keynote |
| `2-presentation/Presentation_30min.html` / `.pdf` | The same 32-slide talk, as an interactive page and as PDF | any browser / PDF reader |
| **`2-presentation/presenter-30min.html`** | **Run sheet for the talk** — per-slide timing, cumulative clock, the handover, what to cut if late, bilingual block guidance, 7 anticipated questions | any browser |
| **`2-presentation/companion.html`** | **Presenter companion for all 100 slides** — what each slide communicates, a script to read aloud, what the visuals mean, cues, transitions, timing, a quick-reference bullet list per slide; bilingual EN/FA | any browser |
| **`3-study/oral-exam.html`** | **Oral-exam study site** — question bank with model answers and collapsed follow-ups and misconceptions; structured mode, exam simulator, search, progress tracking | any browser |
| `4-evidence/bench/bench.py` | The benchmark script | Python 3 + PyTorch |
| `4-evidence/bench/RESULTS.txt` | Its recorded output, with caveats and pinned commits | text |
| `5-source/deck.json`, `5-source/presentation.json` | The structured content both decks are generated from | any text editor |
| `5-source/*.py`, `5-source/gen_pptx.js` | The generator scripts (HTML, PPTX, companion, oral-exam study site) | Python 3 / Node.js |

## The deck

100 slides in eight parts plus front and back matter, indexed against the brief's required §3 structure:

| Part | Contents | Brief § | Slides |
|---|---|---|---|
| — | Front matter — title, how to read the deck, the argument in four moves, map of the deck | — | 01–04 |
| I | The problem — degradation model, ill-posedness, MAP, PSNR/SSIM, the nine benchmarks | §1 | 05–13 |
| II | Classical DIP (2005–2014) — filters → transform-domain shrinkage → TV → non-local self-similarity → BM3D → WNNM | §2 | 14–26 |
| III | The deep learning transition (2012–2017) — the first MLP crack, unrolling, TNRD, and DnCNN in full | §3 | 27–41 |
| IV | The data branch (2018–2025) — Noise2Noise → Noise2Void → ZS-N2N → P2N | §4 | 42–49 |
| V | The architecture branch (2021–2024) — Restormer, NAFNet, SCUNet, MambaIR | §4 | 50–62 |
| VI | Engineering reality — repositories, code, data pipelines, loss functions, pre-trained weights, measurements | §5 | 63–77 |
| VII | Comparative analysis — 18 years of results, efficiency, real noise, **SOTA qualified**, synthesis | §6 | 78–85 |
| VIII | Open problems, the practical answer, **SOTA qualified table**, **Before → After**, **proposal directions**, presentation strategy, conclusion | §7 | 86–96 |
| — | Back matter — bibliography (Category A, Category B), declared limitations, **defence map** | — | 97–100 |

**Every slide carries speaker notes.** In `master-deck.html` press `n` to reveal them,
`m` for the contents panel, and arrow keys to navigate. In PowerPoint they are in the
notes pane as usual.

## Evolution and SOTA coverage in the master deck

Slides 90–95 (inside Part VIII) carry the evolution and SOTA analysis explicitly, so the
master deck itself makes this case rather than leaving it only in the condensed talk:

- **Slide 90 — SOTA, qualified.** Four current methods, each naming the benchmark, the figure, the
  publication venue and year, and what distinguishes it from the others leading elsewhere. It
  deliberately does **not** state how long any method held its position: no source in this project
  reports that, so the deck declines to estimate it.
- **Slide 91 — why several SOTAs.** Four structural reasons, each measurable.
- **Slides 92–93 — Before → After, as implementation changes.** Every step, each naming the smallest
  code change that carries the innovation, from the iterated SVD through `return x - n` and the
  target-tensor swap to the einops `rearrange` and `x1 * x2`.
- **Slide 94 — four proposal directions**, each tied to a documented limitation, stating what would
  change and how it would be measured. The deck commits to one.
- **Slide 95 — how to present this deck**, stating what the condensed summary covers and what it
  deliberately leaves to the deck, so the cut is visibly deliberate — including how the two
  presenters split the talk.

## What the condensed 30-minute deck does

Structured around how the talk will be evaluated, and timed to the brief's format. Two presenters,
one handover: **12:00** (presenter 1, slides 1–14, the classical era and the break to DnCNN) and
**14:06** (presenter 2, slides 15–32, both 2018 branches, the synthesis, conclusion and backup
index) — 26:06 core against a 30:00 slot. The handover falls at slide 15, the seam where the field
itself forks in 2018.

- **Every method gets the same four questions:** what could the previous one not do, what changed
  technically, which line of code changed, what did it buy and cost. The comparison between methods
  is therefore structural rather than anecdotal.
- **Before → After tables** for WNNM vs BM3D, TNRD vs classical, DnCNN vs TNRD, N2V vs N2N, and
  ZS-N2N vs P2N — each with an *implementation change* row, not just a performance row.
- **Four Before → After code slides** showing the smallest snippet that carries the innovation:
  `return x-n`, the target-tensor swap, the einops `rearrange`, and `x1 * x2`.
- **Every SOTA claim names its benchmark and metric**, and the comparison table reports publication
  year rather than an invented SOTA window. Slide 26's second column is *which table each method
  leads* — the checkable claim.
- **Slide 27 answers "why several SOTAs"** with four reasons, because that is the question most
  likely to be asked and it deserves more than a sentence.
- **Slide 30 proposes four research directions**, each tied to a documented limitation, stating what
  would change and how it would be measured. The deck commits to one.

## Art direction — "Signal / Noise"

The visual language is derived from the subject rather than applied to it.

**The grain field.** The title, the eight part dividers and the closing statement carry a
procedurally generated field of dots that dissolves from dense noise into clean paper. It is
deterministic (seeded per slide), drawn at shape level, and it is the only ornament in the deck —
because it is the thing the deck is about.

**The 18-year spine.** Every content slide carries a hairline along the foot running 2007 → 2025,
with the current era's span picked out in its own colour. You can always see where in the arc you
are standing.

**An asymmetric grid.** The left rail is deliberately empty except for a large faint folio and a
rotated era label. Tables break the rail to gain width; everything else respects it. That tension
between held and broken margin is what stops 100 slides reading as one template.

**Rules, not boxes.** No rounded cards, no fills behind body copy, no shadows. Structure is carried
by hairlines, heavy era rules and whitespace. Warm off-white paper (`#FAF9F6`), near-black ink
(`#14120F`). Part dividers invert to a full-height ink block with a 108 pt reversed numeral.

**Typography.** Cambria for display and figures, set large with negative tracking; Calibri for body;
Consolas for code, with a line-number gutter. Scale contrast is deliberately wide — 44–50 pt display
against 8.5 pt letterspaced micro-caps. Lists use hanging figures instead of bullets.

**Eleven distinct layouts.** Title, part divider, numbered argument, opposed columns, broadsheet
grid, data table, equation band, statistic row, process spine, annotated listing, and full-slide
statement — each used where its shape fits the content, so consecutive slides rarely repeat.

**A rendering note.** This deck was proofed in a container that substitutes Caladea and Carlito for
Cambria and Calibri. Caladea carries no Greek, so Greek in the proof renders came from a fallback
face. On a machine with real Cambria the equations render better than the proofs, not worse.

## Which file to use when

| Situation | File |
|---|---|
| Submitting the deliverable | `1-deliverable/Stage3_Master_Deck.pptx` |
| Presenting | `2-presentation/Presentation_30min.pptx` + `2-presentation/presenter-30min.html` |
| Rehearsing against the master deck | `2-presentation/defence.html` — alternative condensed script over the 100 slides |
| Preparing for questions on any slide | `2-presentation/companion.html` — all 100 slides scripted |
| Studying to genuinely understand it | `3-study/oral-exam.html` — dark mode, LaTeX, exam simulator |
| Reading the argument as prose | `1-deliverable/Stage3_Report.md` |

**Offline behaviour.** `master-deck.html` is fully self-contained: its equations and its 12 embedded
paper figures are inlined as base64, so it needs no network at all. `oral-exam.html` is the only
file that reaches out, loading KaTeX from a CDN to typeset the inline mathematics in its answers. It
degrades cleanly: if the CDN is blocked or you are offline, a banner says so and the LaTeX source
stays readable. Nothing else on that page is affected.

## Before the defence

1. **Re-check the citation counts** on slide 91 (Category A bibliography, slide 97) — they are
   Google Scholar figures from 9 August 2026 and the date is printed alongside them.
2. **Read `defence.html` end to end.** The spoken core is 14:45 against a 30:00 slot;
   each block carries a *Slack* expansion to deploy if you finish early.
3. **Slide 100 is the defence map** — print it and keep it in front of you during questions.
4. **Do not put anything on a slide you cannot personally explain.** Every slide was
   built to be answered from, and its notes field carries the answer it expects.
5. **Run `oral-exam.html` in exam-simulator mode at least twice.** It shuffles the question bank
   and hides every answer, so you answer cold — which is the actual test.
6. **Rehearse the handover** (slide 15) out loud at least once — a clean handover reads as a
   prepared team, not two separate talks stitched together.

## Design system

Light theme throughout. Near-black text (`#0F1418`) on white; white text appears only on
solid accent fills, all of which clear 4.5:1 contrast. Cambria for display, Calibri for
body, Consolas for code. Each of the five eras carries its own accent colour, applied
consistently to the top rule, the title bar, bullet marks, table headers and footnote
panels, so the era a slide belongs to is readable at a glance.

Type scale: slide titles 26–34 pt (single-line where possible), leads 12–14.5 pt,
body 10–13.6 pt, equations 11.5–17 pt, key figures 42 pt. Sizes are fitted per slide by
the generator so that nothing is clipped and nothing falls below a readable minimum.

## Evidence conventions

- Paper tags name the exact table or figure: `[DnCNN17 · Table II]`, `[Restormer22 · Table 6]`,
  `[WNNM14 · Fig. 1]`.
- `[measured]` — figures we produced ourselves; method and hardware stated on the slide.
- `[brief]` — the assignment brief.
- `[reading]` — our interpretation, labelled because it is not a source claim.

No quality metric in this work was computed by us; all PSNR/SSIM figures are reproduced
from published tables. Our own measurements cover parameter counts and CPU latency only,
and used random tensors. See `Stage3_Report.md` §2 and §12.
