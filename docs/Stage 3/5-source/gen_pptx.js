// ───────────────────────────────────────────────────────────────────────────
//  "Signal / Noise" — art direction for the Stage 3 master deck.
//
//  Grounded in the subject rather than decorating it:
//    · a procedural GRAIN FIELD that thins from noise into clean paper
//    · an 18-YEAR SPINE along the foot, so the slide's place in the arc is
//      always visible
//    · an asymmetric editorial grid with an empty left rail carrying the
//      folio and a rotated era label
//    · rules, not boxes. Whitespace, not fills.
// ───────────────────────────────────────────────────────────────────────────
const pptxgen = require('pptxgenjs');
const fs = require('fs');

const SRC = process.env.DECK_IN  || '/home/claude/work/stage3/Stage3_ImageDenoising/5-source/deck.json';
const DST = process.env.DECK_OUT || '/home/claude/work/out/Stage3_Master_Deck.pptx';
const S = JSON.parse(fs.readFileSync(SRC, 'utf8'));

// NOTE on figures: the 12 source-paper figures that are embedded inline in
// master-deck.html (and the condensed set in Presentation_30min.html) are
// NOT reproduced inline in this PPTX — those layouts are hand-fit to their
// text/table/equation content with the print already at or near its floor
// font size on several slides (see `warn[]` below), and a figure band big
// enough to be legible does not fit there without either shrinking that
// content's floor further or removing prose. Instead, each of those 12
// figures is appended as its own full slide at the end of this deck (see
// "figure appendix" below), at full legible size, captioned with the exact
// caption and citation used inline in master-deck.html, and cross-referenced
// back to the slide number where it is discussed — additive only, so it
// cannot regress the fitted layouts of slides 1-100.
const APXDIR = '/home/claude/work/stage3/Stage3_ImageDenoising/5-source/appendix_figs';
const APXMANIFEST = (() => {
  try { return JSON.parse(fs.readFileSync(APXDIR + '/manifest.json', 'utf8')); }
  catch (e) { return {}; }
})();

// ── palette ───────────────────────────────────────────────────────────────
const PAPER = 'FAF9F6';   // warm off-white, not clinical white
const PANEL = 'F2F0E9';   // warm tint for equation / code fields
const INK   = '14120F';
const BODY  = '33302B';
const SOFT  = '5A554D';
const MUTED = '8A847A';
const FAINT = 'B5AFA4';
const RULE  = 'DFDBD2';
const RULE2 = 'C9C4B9';
const REV   = 'F7F5F0';   // reversed text on ink

const ERA = {
  meta:      { name: 'FOUNDATION',    hex: '14343F', tint: 'E8EEF0', from: 2007, to: 2025 },
  classical: { name: 'CLASSICAL DIP', hex: '7C5E2A', tint: 'F2EDE3', from: 2007, to: 2014 },
  bridge:    { name: 'THE BRIDGE',    hex: '2F5470', tint: 'E9EEF3', from: 2012, to: 2017 },
  deepcnn:   { name: 'DEEP CNN',      hex: '1C6151', tint: 'E6F0ED', from: 2016, to: 2018 },
  data:      { name: 'DATA BRANCH',   hex: '7E3247', tint: 'F4EAED', from: 2018, to: 2025 },
  arch:      { name: 'ARCHITECTURE',  hex: 'C0451A', tint: 'FAEBE4', from: 2021, to: 2024 },
};
const ACC = 'C0451A';     // house accent

const SER = 'Cambria';    // display, figures
const SAN = 'Calibri';    // body, labels
const MON = 'Consolas';

// ── grid ──────────────────────────────────────────────────────────────────
const W = 13.333, H = 7.5;
const RAIL = 0.66;        // left rail — holds folio + rotated era label
const M    = 1.98;        // main column starts here
const R    = 12.70;       // main column ends here
const CW   = R - M;       // 10.72
const MEASURE = 9.30;     // narrow measure for lead paragraphs
const SPINE_Y = 6.98;     // the 18-year timeline
const BODY_TOP = 0.60;

const warn = [];
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.author = 'DIP Final Project — Stage 3';
pres.title  = process.env.DECK_TITLE || 'Image Denoising: From Foundations to State-of-the-Art';

// ── text utilities ────────────────────────────────────────────────────────
function plain(s) { return String(s).replace(/\^(\d+)\^/g, '[$1]').replace(/\*+/g, '').replace(/`/g, ''); }

function rich(str, base) {
  base = base || {};
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*\n]+\*|`[^`]+`|\^\d+\^)/g;
  let last = 0, m;
  const push = (t, x) => { if (t !== '') out.push({ text: t, options: Object.assign({}, base, x || {}) }); };
  while ((m = re.exec(str)) !== null) {
    if (m.index > last) push(str.slice(last, m.index));
    const tok = m[0];
    if (tok.startsWith('**')) {
      const inner = tok.slice(2, -2), allCode = /^`[^`]+`$/.test(inner);
      push(inner.replace(/`/g, ''), Object.assign({ bold: true, color: base.strong || INK },
        allCode ? { fontFace: MON, color: base.codeColor || '145A66' } : {}));
    } else if (tok.startsWith('`')) {
      push(tok.slice(1, -1), { fontFace: MON, color: base.codeColor || '145A66' });
    } else if (tok.startsWith('^')) {
      // inline citation marker ^n^ -> small bold accent "[n]", maps to the numbered
      // legend rendered by citeLine() in the slide's own reference line.
      const n = tok.slice(1, -1);
      push('[' + n + ']', { bold: true, italic: false, color: ACC,
        fontSize: Math.max(7, Math.round((base.fontSize || 12) * 0.78)) });
    } else {
      push(tok.slice(1, -1).replace(/`/g, ''), { italic: true });
    }
    last = re.lastIndex;
  }
  if (last < str.length) push(str.slice(last));
  if (!out.length) push(str);
  return out;
}

// Numbered reference legend for multi-source slides (s.citeN), else the plain cite string.
function citeLine(s) {
  if (s.citeN && s.citeN.length) {
    return s.citeN.map((part, i) => '[' + (i + 1) + '] ' + plain(part)).join('   ');
  }
  return plain(s.cite);
}

function cpl(w, fs, serif) { return Math.max(10, Math.floor(w * (serif ? 134 : 165) / fs)); }
// Bold runs render visibly wider per character than plain(); a paragraph that
// is mostly **bold** wraps sooner than a flat char-count model predicts. Used
// where a text box has no autoPage and a bad estimate means silent overflow.
function boldFrac(t) {
  const total = plain(String(t)).length || 1;
  let bold = 0;
  String(t).replace(/\*\*([^*]+)\*\*/g, (m, inner) => { bold += inner.replace(/`/g, '').length; return ''; });
  return Math.min(1, bold / total);
}
function nlinesRich(t, w, fs, serif) {
  return nlines(t, w / (1 + 0.16 * boldFrac(t)), fs, serif);
}
function nlines(t, w, fs, serif) {
  let n = 0;
  plain(String(t)).split('\n').forEach(s => { n += Math.max(1, Math.ceil(s.length / cpl(w, fs, serif))); });
  return n;
}
function lh(fs) { return fs * 0.0163; }
// Equations set in bold serif with symbols and wide spacing measure far wider than
// prose. LibreOffice reorders symbol-heavy runs when they wrap, so they must not wrap.
function eqLines(t, w, fs) {
  return Math.max(1, Math.ceil(plain(String(t)).length / Math.max(6, Math.floor(w * 100 / fs))));
}

// ── primitives ────────────────────────────────────────────────────────────
function hair(sl, x, y, w, color, pt) {
  sl.addShape(pres.ShapeType.line, { x, y, w, h: 0,
    line: { color: color || RULE, width: pt || 0.75 } });
}
function vhair(sl, x, y, h, color, pt) {
  sl.addShape(pres.ShapeType.line, { x, y, w: 0, h,
    line: { color: color || RULE, width: pt || 0.75 } });
}
function block(sl, x, y, w, h, color) {
  sl.addShape(pres.ShapeType.rect, { x, y, w, h, fill: { color }, line: { width: 0 } });
}
function label(sl, txt, x, y, w, color, fs, align) {
  sl.addText(plain(txt).toUpperCase(), { x, y, w, h: 0.24, fontSize: fs || 8.5, bold: true,
    color: color || MUTED, charSpacing: 2.2, fontFace: SAN, align: align || 'left',
    isTextBox: true, margin: 0 });
}

// Deterministic grain. Density falls off toward the text, so the field reads
// as noise dissolving into clean paper — the subject of the deck, not decoration.
function grain(sl, o) {
  const { x, y, w, h, seed, count } = o;
  const dir = o.dir || 'right';          // which edge is dense
  const c = o.color || INK;
  const dMin = o.dMin || 0.016, dMax = o.dMax || 0.036;
  const peak = o.peak === undefined ? 0.62 : o.peak;   // max keep probability
  let r = (seed >>> 0) || 1;
  const rnd = () => { r = (r * 1103515245 + 12345) & 0x7fffffff; return r / 0x7fffffff; };
  for (let i = 0; i < count; i++) {
    const u = rnd(), v = rnd();
    const t = dir === 'right' ? u : 1 - u;
    if (rnd() > Math.pow(t, 2.6) * peak) continue;      // keep, biased to the dense edge
    const d = dMin + rnd() * (dMax - dMin) * (0.45 + 0.55 * t);
    sl.addShape(pres.ShapeType.rect, { x: x + u * (w - d), y: y + v * (h - d), w: d, h: d,
      fill: { color: c }, line: { width: 0 } });
  }
}

// ── chrome: rail + 18-year spine ──────────────────────────────────────────
function chrome(sl, s, opts) {
  opts = opts || {};
  const e = ERA[s.era] || ERA.meta;

  // folio, set large and faint like a book page number
  sl.addText(String(s.num).padStart(2, '0'), { x: RAIL - 0.28, y: BODY_TOP - 0.10, w: 1.15, h: 0.62,
    fontSize: 30, bold: true, color: 'E3DFD6', fontFace: SER, align: 'left',
    charSpacing: -1, isTextBox: true, margin: 0 });

  // era name, rotated up the rail
  if (e.name && s.era !== 'meta') {
    sl.addText(e.name, { x: RAIL - 1.30, y: 3.05, w: 2.70, h: 0.30, fontSize: 8.5, bold: true,
      color: e.hex, charSpacing: 2.6, fontFace: SAN, align: 'center', rotate: 270,
      isTextBox: true, margin: 0 });
  }

  if (opts.noSpine) return;

  // the 18-year spine
  const x0 = M, x1 = R, span = x1 - x0, Y0 = 2007, Y1 = 2025;
  hair(sl, x0, SPINE_Y, span, RULE2, 0.75);
  if (s.era !== 'meta') {
    const a = x0 + (e.from - Y0) / (Y1 - Y0) * span;
    const b = x0 + (e.to - Y0) / (Y1 - Y0) * span;
    sl.addShape(pres.ShapeType.line, { x: a, y: SPINE_Y, w: b - a, h: 0,
      line: { color: e.hex, width: 2.6 } });
  }
  [2007, 2014, 2017, 2022, 2025].forEach(yr => {
    const x = x0 + (yr - Y0) / (Y1 - Y0) * span;
    vhair(sl, x, SPINE_Y - 0.055, 0.055, RULE2, 0.75);
    sl.addText(String(yr), { x: x - 0.35, y: SPINE_Y + 0.05, w: 0.7, h: 0.2, fontSize: 7,
      color: FAINT, align: 'center', fontFace: SAN, isTextBox: true, margin: 0 });
  });

  if (s.cite) {
    sl.addText(citeLine(s), { x: M, y: SPINE_Y - 0.40, w: CW, h: 0.24, fontSize: 8.2,
      color: MUTED, italic: true, align: 'right', fontFace: SAN, isTextBox: true, margin: 0 });
  }
  if (s.notes) sl.addNotes(plain(s.notes));
}

// ── header: mark, kicker, display title, lead ─────────────────────────────
function head(sl, s, opt) {
  opt = opt || {};
  const e = ERA[s.era] || ERA.meta;
  let y = BODY_TOP;

  if (s.kicker) {
    // short heavy mark, then the kicker — an editorial signature
    sl.addShape(pres.ShapeType.line, { x: M, y: y + 0.10, w: 0.34, h: 0,
      line: { color: e.hex, width: 2.6 } });
    label(sl, s.kicker, M + 0.46, y, CW - 0.46, e.hex, 8.8);
    y += 0.34;
  }

  const tw = opt.titleW || CW;
  let tfs = opt.big ? 40 : 34;
  let tl = nlines(s.title, tw, tfs, true);
  while (tl > 1 && tfs > 25) { tfs = +(tfs - 1.5).toFixed(1); tl = nlines(s.title, tw, tfs, true); }
  while (tl > 2 && tfs > 21) { tfs = +(tfs - 1.5).toFixed(1); tl = nlines(s.title, tw, tfs, true); }
  const th = tl * lh(tfs) * 1.04 + 0.06;
  sl.addText(rich(s.title, { fontSize: tfs, bold: true, color: INK, fontFace: SER,
      charSpacing: tfs > 30 ? -0.9 : -0.5 }),
    { x: M, y, w: tw, h: th, valign: 'top', isTextBox: true, margin: 0, lineSpacingMultiple: 0.92 });
  y += th + 0.13;

  if (s.lead) {
    const lw = opt.leadW || MEASURE;
    let lfs = 13.6, ll = nlines(s.lead, lw, lfs, false);
    if (ll > 3) { lfs = 12.6; ll = nlines(s.lead, lw, lfs, false); }
    if (ll > 4) { lfs = 11.8; ll = nlines(s.lead, lw, lfs, false); }
    const lhh = ll * lh(lfs) * 1.24 + 0.05;
    sl.addText(rich(s.lead, { fontSize: lfs, color: SOFT, fontFace: SAN, strong: INK }),
      { x: M, y, w: lw, h: lhh, valign: 'top', isTextBox: true, margin: 0, lineSpacingMultiple: 1.10 });
    y += lhh + 0.06;
  }
  return y + 0.22;
}

// ── foot: a rule and a statement, not a box ───────────────────────────────
function footM(s) {
  if (!s.foot) return { h: 0, fs: 0 };
  let fs = 11.4, n = nlines(s.foot, CW, fs, false);
  if (n > 2) { fs = 10.8; n = nlines(s.foot, CW, fs, false); }
  if (n > 4) { fs = 10.2; n = nlines(s.foot, CW, fs, false); }
  return { h: n * lh(fs) * 1.26 + 0.26, fs };
}
function foot(sl, s) {
  if (!s.foot) return;
  const e = ERA[s.era] || ERA.meta, fm = footM(s);
  const y = SPINE_Y - 0.52 - fm.h;
  sl.addShape(pres.ShapeType.line, { x: M, y, w: CW, h: 0, line: { color: e.hex, width: 2.2 } });
  sl.addText(rich(s.foot, { fontSize: fm.fs, color: BODY, fontFace: SAN, strong: INK }),
    { x: M, y: y + 0.15, w: CW, h: fm.h - 0.15, valign: 'top', isTextBox: true, margin: 0,
      lineSpacingMultiple: 1.08 });
}
function bottom(s) {
  const fm = footM(s);
  return s.foot ? SPINE_Y - 0.52 - fm.h - 0.22 : SPINE_Y - 0.52;
}

// ── editorial numbered list: hanging figures, no bullets ──────────────────
function list(sl, arr, x, y, w, maxH, o) {
  o = o || {};
  const num = o.numbered !== false;
  const ind = num ? 0.40 : (o.dot === false ? 0 : 0.22);
  const tw = w - ind;
  const floor = o.floor || 10.2;
  let fs = o.fs || 13, gap0 = o.gap === undefined ? 0.15 : o.gap;
  let rows, tot, gap = gap0;
  for (let i = 0; i < 26; i++) {
    rows = arr.map(t => nlines(t, tw, fs, false));
    tot = rows.reduce((a, n) => a + n * lh(fs) * 1.22, 0) + gap * (arr.length - 1);
    if (tot <= maxH || fs <= floor) break;
    fs = +(fs - 0.3).toFixed(2);
  }
  if (tot > maxH && arr.length > 1) {
    gap = Math.max(0.04, gap0 - (tot - maxH) / (arr.length - 1));
    tot = rows.reduce((a, n) => a + n * lh(fs) * 1.22, 0) + gap * (arr.length - 1);
  }
  if (tot > maxH + 0.02) warn.push(`${o.tag || '?'} +${(tot - maxH).toFixed(2)}" @${fs}pt`);
  let yy = y;
  arr.forEach((t, i) => {
    const hh = rows[i] * lh(fs) * 1.22;
    if (num) {
      sl.addText(String(i + 1).padStart(2, '0'), { x: x, y: yy - 0.015, w: 0.34, h: 0.26,
        fontSize: fs * 0.80, bold: true, color: o.dotc || MUTED, fontFace: SER,
        isTextBox: true, margin: 0 });
    } else if (ind) {
      block(sl, x + 0.02, yy + lh(fs) * 0.42, 0.09, 0.055, o.dotc || MUTED);
    }
    sl.addText(rich(t, { fontSize: fs, color: o.color || BODY, fontFace: SAN }),
      { x: x + ind, y: yy - 0.03, w: tw, h: hh + 0.10, valign: 'top', isTextBox: true,
        margin: 0, lineSpacingMultiple: 1.08 });
    yy += hh + gap;
  });
  return yy;
}

// ═══════════════════════════ LAYOUTS ══════════════════════════════════════

function lTitle(sl, s) {
  sl.background = { color: PAPER };
  grain(sl, { x: 9.95, y: 0.26, w: 3.38, h: 4.72, seed: 9137, count: 2100,
              dir: 'right', peak: 0.55, dMin: 0.015, dMax: 0.040 });
  block(sl, 0, 0, W, 0.115, INK);

  label(sl, s.kicker, M, 1.05, 9, ACC, 9.5);
  sl.addText(s.title, { x: M, y: 1.42, w: 7.5, h: 2.2, fontSize: 44, bold: true, color: INK,
    fontFace: SER, charSpacing: -1.4, isTextBox: true, margin: 0, lineSpacingMultiple: 0.90 });
  sl.addShape(pres.ShapeType.line, { x: M, y: 3.66, w: 1.30, h: 0, line: { color: ACC, width: 3 } });
  sl.addText(s.lead, { x: M, y: 3.90, w: 7.3, h: 1.1, fontSize: 13.2, color: SOFT, fontFace: SAN,
    isTextBox: true, margin: 0, lineSpacingMultiple: 1.16 });

  const meta = s.body.meta;
  const gap = meta.length > 4 ? 0.28 : 0.30;
  const cw = (CW - (meta.length - 1) * gap) / meta.length;
  hair(sl, M, 5.30, CW, INK, 1.6);
  let mfs = 11.6;
  const fits = fs => meta.every(kv => nlines(kv[1], cw, fs, false) <= 3);
  while (mfs > 9.0 && !fits(mfs)) mfs = +(mfs - 0.3).toFixed(2);
  meta.forEach((kv, i) => {
    const x = M + i * (cw + gap);
    if (i) vhair(sl, x - gap / 2, 5.46, 1.10, RULE2, 0.75);
    label(sl, kv[0], x, 5.48, cw, ACC, 8);
    sl.addText(kv[1], { x, y: 5.76, w: cw, h: 0.86, fontSize: mfs, color: INK, fontFace: SAN,
      isTextBox: true, margin: 0, lineSpacingMultiple: 1.10 });
  });
  sl.addText(citeLine(s), { x: M, y: SPINE_Y - 0.02, w: 9, h: 0.24, fontSize: 8.2, color: MUTED,
    italic: true, fontFace: SAN, isTextBox: true, margin: 0 });
  if (s.notes) sl.addNotes(plain(s.notes));
}

function lSection(sl, s) {
  sl.background = { color: PAPER };
  const e = ERA[s.era] || ERA.meta;
  const acc = s.era === 'meta' ? ACC : e.hex;
  const BW = 5.55;
  block(sl, 0, 0, BW, H, INK);
  grain(sl, { x: BW - 2.10, y: 0, w: 2.10, h: H, seed: 4211 + s.num, count: 1500,
              dir: 'right', peak: 0.42, color: '474036', dMin: 0.014, dMax: 0.034 });

  sl.addText(s.part || '', { x: 0.62, y: 0.78, w: 3.6, h: 2.4, fontSize: 108, bold: true,
    color: acc, fontFace: SER, charSpacing: -3, isTextBox: true, margin: 0 });
  sl.addShape(pres.ShapeType.line, { x: 0.70, y: 3.28, w: 1.15, h: 0, line: { color: acc, width: 3 } });
  sl.addText(s.title, { x: 0.70, y: 3.44, w: 4.2, h: 2.0, fontSize: 34, bold: true, color: REV,
    fontFace: SER, charSpacing: -0.8, isTextBox: true, margin: 0, lineSpacingMultiple: 0.94 });
  label(sl, s.kicker, 0.70, 6.44, 4.2, '8E877B', 8.5);

  label(sl, 'in this part', BW + 0.95, 1.30, 5, acc, 8.8);
  const items = s.body.items;
  let y = 1.72;
  hair(sl, BW + 0.95, y - 0.12, 6.30, RULE2, 0.75);
  items.forEach((it, i) => {
    const n = nlines(it, 5.55, 13, false), hh = n * lh(13) * 1.22;
    sl.addText(String(i + 1).padStart(2, '0'), { x: BW + 0.95, y: y - 0.01, w: 0.45, h: 0.26,
      fontSize: 10.5, bold: true, color: acc, fontFace: SER, isTextBox: true, margin: 0 });
    sl.addText(rich(it, { fontSize: 13, color: BODY, fontFace: SAN }),
      { x: BW + 1.48, y: y - 0.04, w: 5.75, h: hh + 0.1, valign: 'top', isTextBox: true,
        margin: 0, lineSpacingMultiple: 1.08 });
    y += hh + 0.30;
    hair(sl, BW + 0.95, y - 0.15, 6.30, RULE, 0.75);
  });
  sl.addText(s.lead, { x: BW + 0.95, y: Math.max(y + 0.20, 5.55), w: 6.10, h: 1.0, fontSize: 12.4,
    color: SOFT, italic: true, fontFace: SAN, isTextBox: true, margin: 0, lineSpacingMultiple: 1.14 });
  sl.addText(citeLine(s), { x: BW + 0.95, y: SPINE_Y - 0.02, w: 6.1, h: 0.24, fontSize: 8.2,
    color: MUTED, italic: true, fontFace: SAN, isTextBox: true, margin: 0 });
  sl.addText(String(s.num).padStart(2, '0'), { x: 11.6, y: SPINE_Y - 0.08, w: 1.1, h: 0.32,
    fontSize: 15, bold: true, color: 'E3DFD6', fontFace: SER, align: 'right', isTextBox: true, margin: 0 });
  if (s.notes) sl.addNotes(plain(s.notes));
}

function lQuote(sl, s) {
  sl.background = { color: PAPER };
  grain(sl, { x: 10.1, y: 2.6, w: 3.23, h: 4.4, seed: 7717, count: 1200,
              dir: 'right', peak: 0.45, dMin: 0.014, dMax: 0.034 });
  block(sl, 0, 0, W, 0.115, INK);
  label(sl, s.kicker, M, 0.92, 8, ACC, 9.5);
  sl.addText(s.title, { x: M, y: 1.26, w: 9.6, h: 0.8, fontSize: 38, bold: true, color: INK,
    fontFace: SER, charSpacing: -1.1, isTextBox: true, margin: 0 });
  hair(sl, M, 2.24, 9.6, INK, 2.2);
  const paras = s.body.q.split('\n\n');
  const QW = 8.50, QTOP = 2.48, QBOT = 6.18;
  let qf = 18, gapP = 0.20;
  const qh = f => paras.reduce((a, p) => a + nlines(p, QW, f, true) * lh(f) * 1.24, 0)
                  + gapP * (paras.length - 1);
  while (qf > 12 && qh(qf) > QBOT - QTOP) qf = +(qf - 0.5).toFixed(1);
  sl.addText(paras.map((p, i) => ({ text: p,
    options: { breakLine: i < paras.length - 1, paraSpaceAfter: Math.round(gapP * 72) } })),
    { x: M, y: QTOP, w: QW, h: QBOT - QTOP, fontSize: qf, color: INK, fontFace: SER, italic: true,
      valign: 'top', isTextBox: true, margin: 0, lineSpacingMultiple: 1.24 });
  hair(sl, M, QBOT + 0.14, 2.2, RULE2, 0.75);
  sl.addText('— ' + s.body.attrib, { x: M, y: QBOT + 0.28, w: 8.5, h: 0.3, fontSize: 11.5,
    color: MUTED, fontFace: SAN, isTextBox: true, margin: 0 });
  chrome(sl, s, { noSpine: true });
  sl.addText(citeLine(s), { x: M, y: SPINE_Y - 0.02, w: 8, h: 0.24, fontSize: 8.2, color: MUTED,
    italic: true, fontFace: SAN, isTextBox: true, margin: 0 });
}

function lContent(sl, s) {
  sl.background = { color: PAPER };
  const e = ERA[s.era] || ERA.meta;
  const y = head(sl, s);
  const arr = s.body.bullets || s.body.paras || [];
  hair(sl, M, y - 0.13, CW, RULE, 0.75);
  list(sl, arr, M, y, CW, bottom(s) - y,
    { fs: arr.length > 6 ? 12.6 : 13.4, numbered: !!s.body.bullets, dotc: e.hex,
      gap: 0.17, floor: 10.4, tag: 's' + s.num });
  foot(sl, s); chrome(sl, s);
}

function lTwo(sl, s) {
  sl.background = { color: PAPER };
  const e = ERA[s.era] || ERA.meta;
  const y = head(sl, s);
  const gapx = 0.62, cw = (CW - gapx) / 2, hgt = bottom(s) - y;
  vhair(sl, M + cw + gapx / 2, y - 0.05, hgt + 0.05, RULE, 0.75);
  [['left', M], ['right', M + cw + gapx]].forEach(g => {
    const col = s.body[g[0]], x = g[1];
    sl.addShape(pres.ShapeType.line, { x, y: y - 0.13, w: cw, h: 0, line: { color: e.hex, width: 2.2 } });
    sl.addText(rich(col.h, { fontSize: 16, bold: true, color: INK, fontFace: SER, charSpacing: -0.4 }),
      { x, y: y + 0.04, w: cw, h: 0.54, valign: 'top', isTextBox: true, margin: 0,
        lineSpacingMultiple: 0.94 });
    list(sl, col.bullets, x, y + 0.66, cw, hgt - 0.72,
      { fs: 12.4, dotc: e.hex, gap: 0.15, floor: 10.0, numbered: false, tag: 's' + s.num + g[0] });
  });
  foot(sl, s); chrome(sl, s);
}

function lCards(sl, s) {
  sl.background = { color: PAPER };
  const e = ERA[s.era] || ERA.meta;
  const y = head(sl, s);
  const cards = s.body.cards;
  const cols = cards.length <= 2 ? cards.length : 2;
  const rows = Math.ceil(cards.length / cols);
  const gx = 0.62, gy = 0.26;
  const cw = (CW - (cols - 1) * gx) / cols;
  const hgt = bottom(s) - y;

  // Rows were previously given equal height regardless of how much text each
  // holds, and the paragraph box was fixed at 12.1pt with no shrink/warn — so a
  // text-heavy row silently overflowed into the row below (or past the foot
  // rule) with nothing in warn[] to catch it. Give each row only what its
  // longest card needs at the base sizes, then scale all rows down together
  // if the total still does not fit; a per-card font floor below is the last
  // resort once that reallocation is exhausted.
  const HFS = 16.5, PFS0 = 12.1;
  const need = cards.map(c => {
    const hl = nlinesRich(c.h, cw, HFS, true) * lh(HFS) * 1.06 + 0.08;
    const pl = nlinesRich(c.p, cw, PFS0, false) * lh(PFS0) * 1.10;
    return 0.20 + (c.tag ? 0.28 : 0) + hl + 0.09 + pl + 0.06;
  });
  const rowNeed = [];
  for (let r = 0; r < rows; r++) {
    let m = 0;
    for (let ci = 0; ci < cols; ci++) {
      const idx = r * cols + ci;
      if (idx < cards.length) m = Math.max(m, need[idx]);
    }
    rowNeed.push(m);
  }
  const totalNeed = rowNeed.reduce((a, b) => a + b, 0) + gy * (rows - 1);
  const scale = totalNeed > hgt ? hgt / totalNeed : 1;
  const rowH = rowNeed.map(v => v * scale);
  const rowY = [];
  { let acc = y; for (let r = 0; r < rows; r++) { rowY.push(acc); acc += rowH[r] + gy; } }

  cards.forEach((c, i) => {
    const cx = i % cols, ry = Math.floor(i / cols);
    const x = M + cx * (cw + gx), yy = rowY[ry], ch = rowH[ry];
    sl.addShape(pres.ShapeType.line, { x, y: yy, w: cw, h: 0, line: { color: e.hex, width: 2.2 } });
    if (cx) vhair(sl, x - gx / 2, yy + 0.06, ch - 0.10, RULE, 0.75);
    let ty = yy + 0.20;
    if (c.tag) { label(sl, c.tag, x, ty, cw, e.hex, 8.2); ty += 0.28; }
    const hl = nlinesRich(c.h, cw, HFS, true) * lh(HFS) * 1.06 + 0.08;
    sl.addText(rich(c.h, { fontSize: HFS, bold: true, color: INK, fontFace: SER, charSpacing: -0.4 }),
      { x, y: ty, w: cw, h: hl, valign: 'top', isTextBox: true, margin: 0, lineSpacingMultiple: 0.94 });
    ty += hl + 0.09;
    const availP = yy + ch - ty - 0.06;
    let pfs = PFS0;
    const pLines = () => nlinesRich(c.p, cw, pfs, false) * lh(pfs) * 1.10;
    while (pfs > 9.6 && pLines() > availP) pfs = +(pfs - 0.2).toFixed(2);
    if (pLines() > availP + 0.03) warn.push(`s${s.num} card${i + 1} +${(pLines() - availP).toFixed(2)}" @${pfs}pt`);
    sl.addText(rich(c.p, { fontSize: pfs, color: BODY, fontFace: SAN }),
      { x, y: ty, w: cw, h: availP, valign: 'top', isTextBox: true, margin: 0,
        lineSpacingMultiple: 1.10 });
  });
  foot(sl, s); chrome(sl, s);
}

function lTable(sl, s) {
  sl.background = { color: PAPER };
  const e = ERA[s.era] || ERA.meta;
  // tables break the rail — wider measure, stronger presence
  const TM = 1.30, TW = R - TM;
  const y = head(sl, s, { titleW: CW, leadW: MEASURE });
  const cols = s.body.cols, rws = s.body.rows;
  const align = s.body.align || 'l'.repeat(cols.length);
  const hl = new Set(s.body.hl || []);

  const wgt = cols.map((c, j) => {
    let mx = plain(c).length * 1.2;
    rws.forEach(r => { mx = Math.max(mx, Math.min(plain(String(r[j])).length, 64)); });
    return Math.max(mx, 5);
  });
  const sum = wgt.reduce((a, b) => a + b, 0);
  let colW = wgt.map(v => TW * v / sum);
  const MINW = 0.60; let def = 0;
  colW = colW.map(v => { if (v < MINW) { def += MINW - v; return MINW; } return v; });
  if (def > 0) {
    const pool = colW.reduce((a, v) => a + (v > MINW ? v - MINW : 0), 0);
    colW = colW.map(v => v > MINW ? v - (v - MINW) / pool * def : v);
  }
  colW = colW.map(v => +v.toFixed(3));
  let wd = 0; colW.forEach((v, j) => { if (v > colW[wd]) wd = j; });
  colW[wd] = +(colW[wd] + (TW - colW.reduce((a, b) => a + b, 0))).toFixed(3);

  const nr = rws.length, avail = bottom(s) - y;
  const pad = nr >= 10 ? 3 : nr >= 8 ? 4 : 5;          // long tables breathe less
  const est = f => {
    const hdr = Math.max.apply(null, cols.map((c, j) => nlines(c, colW[j] - 0.22, f * 0.90, false)));
    const bl = rws.reduce((a, r) => a + Math.max.apply(null,
      r.map((c, j) => nlines(c, colW[j] - 0.22, f, false))), 0);
    return (hdr + bl) * lh(f) * 1.24 + (nr + 1) * (pad * 2 / 72 + 0.03);
  };
  let fs = 12.4;
  while (fs > 7.9 && est(fs) > avail) fs = +(fs - 0.25).toFixed(2);
  if (est(fs) > avail + 0.05) warn.push(`s${s.num} table +${(est(fs) - avail).toFixed(2)}"`);

  const tbl = [];
  tbl.push(cols.map((c, j) => ({ text: plain(c).toUpperCase(), options: {
    bold: true, color: INK, fill: { color: PAPER }, fontSize: +(fs * 0.78).toFixed(1),
    charSpacing: 1.1, align: align[j] === 'r' ? 'right' : 'left', fontFace: SAN,
    valign: 'bottom', margin: [3, 8, 5, 8] } })));
  rws.forEach((r, i) => {
    tbl.push(r.map((cell, j) => {
      const txt = String(cell);
      return { text: plain(txt), options: {
        fontSize: fs, color: hl.has(i) ? INK : BODY,
        bold: txt.indexOf('**') >= 0 || hl.has(i),
        fill: { color: hl.has(i) ? e.tint : PAPER },
        align: align[j] === 'r' ? 'right' : 'left', fontFace: SAN, valign: 'middle',
        margin: [pad, 8, pad, 8] } };
    }));
  });
  sl.addTable(tbl, { x: TM, y, w: TW, colW,
    border: [{ pt: 0, color: PAPER }, { pt: 0, color: PAPER },
             { pt: 0.75, color: RULE }, { pt: 0, color: PAPER }],
    autoPage: false, rowH: Math.min(0.48, Math.max(0.19, (avail - 0.05) / (nr + 1))) });
  // heavy rule under the header row
  const hdrH = Math.min(0.48, Math.max(0.19, (avail - 0.05) / (nr + 1)));
  sl.addShape(pres.ShapeType.line, { x: TM, y: y + hdrH * 0.92, w: TW, h: 0,
    line: { color: e.hex, width: 2 } });
  foot(sl, s); chrome(sl, s);
}

function lMath(sl, s) {
  sl.background = { color: PAPER };
  const e = ERA[s.era] || ERA.meta;
  const y = head(sl, s);
  const eqs = s.body.eqs, arr = s.body.bullets || [];
  const avail = bottom(s) - y;
  const EQDIR = '/home/claude/work/out/eq/';
  const DPI = 600, BASE = 12;          // equations are typeset by pdflatex at 12pt / 600 dpi
  const EW = CW - 0.74;                // inner width of the equation band

  const wIn = (q, pt) => q.imgw / DPI * (pt / BASE);
  const hIn = (q, pt) => q.imgh / DPI * (pt / BASE);
  const ptFit = q => BASE * EW * DPI / q.imgw;   // largest size that still fits the band

  const bandH = (pt, wfs) => eqs.reduce((a, q) => {
    const p = Math.min(pt, ptFit(q));
    const wl = q.where ? nlines(q.where, EW, wfs, false) : 0;
    return a + hIn(q, p) + (wl ? wl * lh(wfs) * 1.22 + 0.08 : 0) + 0.22;
  }, 0) + 0.20 * (eqs.length - 1);
  const listH = f => arr.reduce((a, t) => a + nlines(t, CW - 0.40, f, false) * lh(f) * 1.22, 0)
    + 0.13 * Math.max(0, arr.length - 1);

  // The prose gives way before the mathematics does: cap the equation band at a
  // share of the slide and let the list shrink into whatever is left.
  let pt = 19.5, wfs = 10.8;
  const cap = arr.length ? avail * (eqs.length >= 3 ? 0.52 : 0.62) : avail;
  while (pt > 12 && bandH(pt, wfs) > cap) pt = +(pt - 0.5).toFixed(2);
  while (pt > 9.5 && bandH(pt, wfs) > avail) pt = +(pt - 0.5).toFixed(2);

  let yy = y;
  eqs.forEach(q => {
    const p = Math.min(pt, ptFit(q));
    const iw = wIn(q, p), ih = hIn(q, p);
    const wl = q.where ? nlines(q.where, EW, wfs, false) : 0;
    const hh = ih + (wl ? wl * lh(wfs) * 1.22 + 0.08 : 0) + 0.22;
    block(sl, M, yy, CW, hh, e.tint);
    block(sl, M, yy, 0.055, hh, e.hex);
    sl.addImage({ path: EQDIR + q.img, x: M + 0.40, y: yy + 0.14, w: iw, h: ih });
    if (q.where) {
      sl.addText(rich(q.where, { fontSize: wfs, color: SOFT, italic: true, fontFace: SAN, strong: INK }),
        { x: M + 0.40, y: yy + 0.14 + ih + 0.06, w: EW, h: wl * lh(wfs) * 1.22 + 0.06,
          valign: 'top', isTextBox: true, margin: 0, lineSpacingMultiple: 1.04 });
    }
    yy += hh + 0.20;
  });
  if (arr.length) {
    list(sl, arr, M, yy + 0.04, CW, bottom(s) - yy - 0.06,
      { fs: 12.5, dotc: e.hex, gap: 0.12, floor: 9.8, numbered: false, tag: 's' + s.num });
  }
  foot(sl, s); chrome(sl, s);
}

function lCode(sl, s) {
  sl.background = { color: PAPER };
  const e = ERA[s.era] || ERA.meta;
  const y = head(sl, s);
  const lines = s.body.lines;
  const cw = 5.92, avail = bottom(s) - y;
  const maxc = Math.max.apply(null, lines.map(L => L.length));
  let cfs = Math.min(10.2, (cw - 0.86) * 72 / (0.655 * Math.max(1, maxc)));
  while (cfs > 7.4 && lines.length * lh(cfs) * 1.19 + 0.60 > avail) cfs = +(cfs - 0.25).toFixed(2);
  cfs = +cfs.toFixed(2);
  const hgt = Math.min(avail, lines.length * lh(cfs) * 1.19 + 0.60);

  block(sl, M, y, cw, hgt, PANEL);
  block(sl, M, y, cw, 0.045, e.hex);
  vhair(sl, M + 0.44, y + 0.42, hgt - 0.50, RULE2, 0.75);   // line-number gutter
  sl.addText(plain(s.body.file), { x: M + 0.20, y: y + 0.15, w: cw - 0.40, h: 0.22, fontSize: 8.6,
    color: MUTED, italic: true, fontFace: SAN, isTextBox: true, margin: 0 });

  const nums = lines.map((L, i) => ({ text: String(i + 1),
    options: { breakLine: i < lines.length - 1, color: FAINT } }));
  sl.addText(nums, { x: M + 0.06, y: y + 0.44, w: 0.32, h: hgt - 0.52, fontSize: cfs * 0.85,
    fontFace: MON, align: 'right', valign: 'top', isTextBox: true, margin: 0,
    lineSpacingMultiple: 0.985 * (1 / 0.85) });

  const runs = lines.map((L, i) => {
    const isC = L.trim().startsWith('#') || L.indexOf('←') >= 0;
    return { text: L === '' ? ' ' : L, options: { breakLine: i < lines.length - 1,
      color: isC ? e.hex : '211F1B', bold: isC } };
  });
  sl.addText(runs, { x: M + 0.56, y: y + 0.44, w: cw - 0.70, h: hgt - 0.52, fontSize: cfs,
    fontFace: MON, valign: 'top', isTextBox: true, margin: 0, lineSpacingMultiple: 0.985 });

  const bx = M + cw + 0.46;
  vhair(sl, M + cw + 0.23, y, avail, RULE, 0.75);
  list(sl, s.body.bullets, bx, y, R - bx, avail,
    { fs: 11.8, dotc: e.hex, gap: 0.13, floor: 9.6, numbered: false, tag: 's' + s.num });
  foot(sl, s); chrome(sl, s);
}

function lStats(sl, s) {
  sl.background = { color: PAPER };
  const e = ERA[s.era] || ERA.meta;
  const y = head(sl, s);
  const st = s.body.stats, avail = bottom(s) - y;
  const gx = 0.58, cw = (CW - (st.length - 1) * gx) / st.length;
  let need = 0;
  st.forEach(v => { need = Math.max(need, 1.46 + nlines(v.s, cw, 11.4, false) * lh(11.4) * 1.22 + 0.10); });
  const ch = Math.min(need, avail * 0.66);
  hair(sl, M, y, CW, INK, 1.6);
  st.forEach((v, i) => {
    const x = M + i * (cw + gx);
    if (i) vhair(sl, x - gx / 2, y + 0.14, ch - 0.14, RULE, 0.75);
    sl.addText(v.n, { x, y: y + 0.16, w: cw, h: 0.86, fontSize: 52, bold: true, color: e.hex,
      fontFace: SER, charSpacing: -2, valign: 'middle', isTextBox: true, margin: 0 });
    label(sl, v.l, x, y + 1.06, cw, INK, 8.6);
    sl.addText(rich(v.s, { fontSize: 11.4, color: BODY, fontFace: SAN }),
      { x, y: y + 1.36, w: cw, h: ch - 1.40, valign: 'top', isTextBox: true, margin: 0,
        lineSpacingMultiple: 1.10 });
  });
  const by = y + ch + 0.30;
  hair(sl, M, by - 0.16, CW, RULE, 0.75);
  list(sl, s.body.bullets, M, by, CW, bottom(s) - by,
    { fs: 12.5, dotc: e.hex, gap: 0.15, floor: 10.4, numbered: false, tag: 's' + s.num });
  foot(sl, s); chrome(sl, s);
}

function lFlow(sl, s) {
  sl.background = { color: PAPER };
  const e = ERA[s.era] || ERA.meta;
  const y = head(sl, s);
  const st = s.body.steps;
  const hasB = (s.body.bullets || []).length > 0;
  const bH = hasB ? 0.80 : 0;
  const avail = bottom(s) - y - bH;
  const gap = 0.16, sh = (avail - (st.length - 1) * gap) / st.length;
  const NX = M + 0.20, HX = M + 0.76, HW = 3.55;
  vhair(sl, NX, y + sh / 2, avail - sh, RULE2, 1.1);     // the connecting spine
  st.forEach((p, i) => {
    const yy = y + i * (sh + gap), mid = yy + sh / 2;
    block(sl, NX - 0.065, mid - 0.065, 0.13, 0.13, e.hex);
    sl.addText(String(i + 1).padStart(2, '0'), { x: NX + 0.18, y: mid - 0.135, w: 0.5, h: 0.27,
      fontSize: 11, bold: true, color: e.hex, fontFace: SER, isTextBox: true, margin: 0 });
    sl.addText(rich(p.h, { fontSize: 13, bold: true, color: INK, fontFace: SER, charSpacing: -0.3 }),
      { x: HX, y: yy + 0.04, w: HW, h: sh - 0.08, valign: 'middle', isTextBox: true, margin: 0,
        lineSpacingMultiple: 0.96 });
    vhair(sl, HX + HW + 0.22, yy + 0.12, sh - 0.24, RULE, 0.75);
    sl.addText(rich(p.p, { fontSize: 11.9, color: BODY, fontFace: SAN }),
      { x: HX + HW + 0.46, y: yy + 0.04, w: R - (HX + HW + 0.46), h: sh - 0.08, valign: 'middle',
        isTextBox: true, margin: 0, lineSpacingMultiple: 1.08 });
    if (i < st.length - 1) hair(sl, HX, yy + sh + gap / 2, CW - 0.76, RULE, 0.75);
  });
  if (hasB) {
    list(sl, s.body.bullets, M, y + avail + 0.22, CW, bH - 0.22,
      { fs: 12.0, dotc: e.hex, gap: 0.10, floor: 10.0, numbered: false, tag: 's' + s.num });
  }
  foot(sl, s); chrome(sl, s);
}

// ── figure appendix: one full slide per paper figure, appended after the
//    numbered deck. Additive only — it does not touch or resize any of the
//    fitted layouts for slides 1-100, so it cannot reintroduce the overflow
//    the rest of this generator is carefully tuned to avoid.
function lFigApx(sl, s) {
  sl.background = { color: PAPER };
  chrome(sl, s);
  const y0 = head(sl, s);

  const capFs = 11.6;
  const capLines = nlines(s.body.cap, CW, capFs, false);
  const capH = capLines * lh(capFs) * 1.28 + 0.10;
  const gap = 0.16;
  const boxBottom = bottom(s);
  const imgMaxH = Math.max(1.0, boxBottom - y0 - capH - gap);
  const imgMaxW = CW;

  const ratio = s.body.w / s.body.h;
  let iw = imgMaxW, ih = iw / ratio;
  if (ih > imgMaxH) { ih = imgMaxH; iw = ih * ratio; }
  const ix = M + (CW - iw) / 2;
  const iy = y0 + Math.max(0, (imgMaxH - ih) / 2);

  sl.addImage({ path: s.body.img, x: ix, y: iy, w: iw, h: ih });
  sl.addShape(pres.ShapeType.rect, { x: ix, y: iy, w: iw, h: ih,
    fill: { type: 'none' }, line: { color: RULE2, width: 0.75 } });

  sl.addText(rich(s.body.cap, { fontSize: capFs, color: MUTED, fontFace: SAN, italic: true, strong: BODY }),
    { x: M, y: y0 + imgMaxH + gap, w: CW, h: capH, valign: 'top', isTextBox: true, margin: 0,
      lineSpacingMultiple: 1.14 });
  if (s.notes) sl.addNotes(plain(s.notes));
}

const LAY = { title: lTitle, section: lSection, content: lContent, two: lTwo, cards: lCards,
  table: lTable, math: lMath, code: lCode, stats: lStats, flow: lFlow, quote: lQuote,
  figapx: lFigApx };

// Build the figure-appendix slides from appendix_figs/manifest.json, one per
// entry, numbered to continue immediately after the last numbered slide so
// the 1-100 numbering (and every cross-reference to it, elsewhere in this
// package) is completely undisturbed.
const APX_KEYS = Object.keys(APXMANIFEST).map(Number).sort((a, b) => a - b);
if (APX_KEYS.length) {
  const byNum = {}; S.forEach(s => { byNum[s.num] = s; });
  const lastNum = Math.max.apply(null, S.map(s => s.num));
  APX_KEYS.forEach((refNum, i) => {
    const entry = APXMANIFEST[String(refNum)];
    const ref = byNum[refNum];
    if (!ref || !entry) return;
    S.push({
      t: 'figapx',
      num: lastNum + 1 + i,
      era: ref.era,
      kicker: 'Figure appendix · slide ' + refNum,
      title: ref.title,
      lead: '',
      cite: '',
      notes: 'Figure discussed on slide ' + refNum + ' (' + plain(ref.title) + '); reproduced here at full size. ' +
             'Same image and caption as the inline figure in master-deck.html.',
      foot: '',
      body: { img: APXDIR + '/' + entry.file, cap: entry.caption, w: entry.w, h: entry.h },
    });
  });
}

S.forEach(s => { (LAY[s.t] || lContent)(pres.addSlide(), s); });

pres.writeFile({ fileName: DST }).then(() => {
  console.log('written: ' + S.length + ' slides');
  if (warn.length) { console.log('FIT (' + warn.length + '):'); warn.forEach(w => console.log('  ' + w)); }
  else console.log('no fit warnings');
});
