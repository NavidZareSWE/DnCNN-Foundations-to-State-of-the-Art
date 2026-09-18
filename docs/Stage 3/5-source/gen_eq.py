# -*- coding: utf-8 -*-
"""
Attach real LaTeX source to every display equation in deck.json and render each
one with pdflatex -> PDF -> transparent PNG, for embedding in the PPTX.

Rendered at 12pt / 600 dpi, so display width in inches = px / 600 * (target_pt / 12).
"""
import json, os, io, subprocess, shutil, hashlib

OUT = '/home/claude/work/out/eq'
OUT_WEB = '/home/claude/work/out/eq_web'
DPI = 600          # print resolution, embedded in the PPTX
DPI_WEB = 200      # screen resolution, inlined as base64 in the HTML deck
BASE_PT = 12

TEX = {
(6, 0):  r"y \;=\; x \;+\; v",

(9, 0):  r"\hat{x} \;=\; \arg\max_{x}\, p(x \mid y) \;=\; \arg\max_{x}\, p(y \mid x)\, p(x)",
(9, 1):  r"\hat{x} \;=\; \arg\min_{x}\, \big[\, -\log p(y \mid x) \;-\; \log p(x) \,\big]",
(9, 2):  r"\hat{x} \;=\; \arg\min_{x}\, \tfrac{1}{2}\lVert y - x \rVert_{2}^{2} \;+\; \lambda\,\Phi(x)",

(10, 0): r"\mathrm{MSE} \;=\; \frac{1}{MN}\sum_{i}\sum_{j}\big[\, x(i,j) - \hat{x}(i,j) \,\big]^{2}",
(10, 1): r"\mathrm{PSNR} \;=\; 10\log_{10}\!\left(\frac{\mathrm{MAX}^{2}}{\mathrm{MSE}}\right)\ \mathrm{dB}"
         r"\;=\; 20\log_{10}(\mathrm{MAX}) \;-\; 10\log_{10}(\mathrm{MSE})",

(11, 0): r"\mathrm{SSIM}(x,\hat{x}) \;=\; \big[\, l(x,\hat{x}) \,\big]^{\alpha}\,"
         r"\big[\, c(x,\hat{x}) \,\big]^{\beta}\,\big[\, s(x,\hat{x}) \,\big]^{\gamma},"
         r"\qquad \alpha = \beta = \gamma = 1",
(11, 1): r"\mathrm{SSIM} \;=\; \frac{(2\mu_{x}\mu_{\hat{x}} + C_{1})(2\sigma_{x\hat{x}} + C_{2})}"
         r"{(\mu_{x}^{2} + \mu_{\hat{x}}^{2} + C_{1})(\sigma_{x}^{2} + \sigma_{\hat{x}}^{2} + C_{2})}",

(15, 0): r"\hat{x}(i,j) \;=\; \frac{1}{|W|}\sum_{(p,q)\,\in\, W} y(p,q)",
(15, 1): r"\operatorname{Var}\big[\hat{x}\big] \;=\; \frac{\sigma^{2}}{|W|}"
         r"\qquad\Longrightarrow\qquad \sigma_{\mathrm{out}} \;=\; \frac{\sigma}{\sqrt{|W|}}",

(17, 0): r"\text{hard:}\quad T_{h}(c) \;=\; c\cdot\mathbf{1}\big[\,|c| > \lambda\,\big]"
         r"\qquad\qquad \text{soft:}\quad T_{s}(c) \;=\; \operatorname{sign}(c)\,\max\big(|c| - \lambda,\; 0\big)",

(18, 0): r"\hat{x} \;=\; \arg\min_{x}\, \tfrac{1}{2}\lVert y - x \rVert_{2}^{2} \;+\; \lambda\lVert \nabla x \rVert_{1},"
         r"\qquad \lVert \nabla x \rVert_{1} \;=\; \sum_{i,j}\sqrt{(\partial_{h}x)^{2} + (\partial_{v}x)^{2}}",

(21, 0): r"\hat{Y}_{S} \;=\; T_{3D}^{-1}\Big(\gamma\big(T_{3D}(Y_{S})\big)\Big),"
         r"\qquad \gamma(c) \;=\; c\cdot\mathbf{1}\big[\,|c| > \lambda_{3D}\,\sigma\,\big]",
(21, 1): r"T_{3D} \;=\; T_{2D} \otimes T_{1D}",

(23, 0): r"Y_{j} \;=\; X_{j} \;+\; N_{j}, \qquad X_{j}\ \text{low rank}",
(23, 1): r"\hat{X}_{j} \;=\; \arg\min_{X_{j}}\, \frac{1}{\sigma_{n}^{2}}\lVert Y_{j} - X_{j} \rVert_{F}^{2}"
         r"\;+\; \lVert X_{j} \rVert_{w,*}, \qquad \lVert X \rVert_{w,*} \;=\; \sum_{i} w_{i}\,\sigma_{i}(X)",

(30, 0): r"\frac{u_{t} - u_{t-1}}{\Delta t} \;=\; -\sum_{i=1}^{N_{k}}\big(K_{i}^{t}\big)^{\!\top}"
         r"\phi_{i}^{t}\big(K_{i}^{t}\,u_{t-1}\big) \;-\; \psi^{t}\big(u_{t-1},\, f\big)",
(30, 1): r"\psi^{t}(u) \;=\; \nabla_{\!u} D_{t}(u,f) \;=\; \lambda^{t} A^{\!\top}\big(Au - f\big),"
         r"\qquad A = I\ \text{ for denoising}",

(33, 0): r"\ell(\Theta) \;=\; \frac{1}{2N}\sum_{i=1}^{N}\Big\lVert\, \mathcal{R}(y_{i};\Theta)"
         r"\;-\; \big(y_{i} - x_{i}\big) \,\Big\rVert_{F}^{2}",

(43, 0): r"\arg\min_{z}\ \mathbb{E}_{y}\big\{L(z,y)\big\} \quad\text{with}\quad L(z,y) = (z-y)^{2}"
         r"\quad\Longrightarrow\quad z = \mathbb{E}_{y}\{y\}",
(43, 1): r"\arg\min_{\theta}\ \sum_{i} L\big(f_{\theta}(\hat{x}_{i}),\; \hat{y}_{i}\big)"
         r"\qquad\text{subject to}\qquad \mathbb{E}\big\{\hat{y}_{i} \mid \hat{x}_{i}\big\} = y_{i}",

(45, 0): r"p(s,n) = p(s)\,p(n \mid s), \quad p(n \mid s) = \prod_{i} p(n_{i} \mid s_{i}),"
         r"\quad \mathbb{E}[n_{i}] = 0 \;\Longrightarrow\; \mathbb{E}[x_{i}] = s_{i}",

(47, 0): r"D_{1} = y \circledast k_{1},\ \ k_{1} = \begin{pmatrix} 0 & \tfrac{1}{2} \\[2pt] \tfrac{1}{2} & 0 \end{pmatrix}"
         r"\qquad D_{2} = y \circledast k_{2},\ \ k_{2} = \begin{pmatrix} \tfrac{1}{2} & 0 \\[2pt] 0 & \tfrac{1}{2} \end{pmatrix}"
         r"\qquad (\text{stride } 2)",
(47, 1): r"L_{\mathrm{res}} \;=\; \tfrac{1}{2}\Big( \big\lVert D_{1} - f_{\theta}(D_{1}) - D_{2} \big\rVert^{2}"
         r"\;+\; \big\lVert D_{2} - f_{\theta}(D_{2}) - D_{1} \big\rVert^{2} \Big)",
(47, 2): r"L_{\mathrm{cons}} \;=\; \tfrac{1}{2}\Big( \big\lVert D_{1} - f_{\theta}(D_{1}) - D_{1}\big(y - f_{\theta}(y)\big) \big\rVert^{2}"
         r"\;+\; \big\lVert D_{2} - f_{\theta}(D_{2}) - D_{2}\big(y - f_{\theta}(y)\big) \big\rVert^{2} \Big)",

(52, 0): r"\mathrm{Attention}(Q,K,V) \;=\; \mathrm{softmax}\!\left(\frac{QK^{\!\top}}{\sqrt{d_{k}}}\right) V",
(52, 1): r"\text{cost} \;=\; O\big(W^{2}H^{2}\big) \qquad \text{for a } W \times H \text{ image}",

(53, 0): r"Q = W_{d}^{Q}\,W_{p}^{Q}\,Y, \qquad K = W_{d}^{K}\,W_{p}^{K}\,Y, \qquad V = W_{d}^{V}\,W_{p}^{V}\,Y",
(53, 1): r"\mathrm{Attention}(\hat{Q},\hat{K},\hat{V}) \;=\; \hat{V}\cdot\mathrm{softmax}\!\left(\frac{\hat{K}\hat{Q}^{\!\top}}{\alpha}\right)",

(54, 0): r"\mathrm{Gate}(X) \;=\; \phi\big(W_{d}^{1}\,W_{p}^{1}\,\mathrm{LN}(X)\big)\ \odot\ \big(W_{d}^{2}\,W_{p}^{2}\,\mathrm{LN}(X)\big)",

(57, 0): r"\mathrm{GLU}(X,f,g,\sigma) \;=\; f(X) \odot \sigma\big(g(X)\big)"
         r"\qquad\qquad \mathrm{GELU}(x) \;=\; x\,\Phi(x)",
(57, 1): r"\Longrightarrow\quad \mathrm{GELU}\ \text{is a special case of GLU, with}\ f, g = \mathrm{id}\ \text{and}\ \sigma = \Phi",
(57, 2): r"\mathrm{SimpleGate}(X,Y) \;=\; X \odot Y",

(60, 0): r"h'(t) \;=\; A\,h(t) + B\,x(t), \qquad y(t) \;=\; C\,h(t) + D\,x(t)",
(60, 1): r"\bar{A} = \exp(\Delta A), \qquad \bar{B} = (\Delta A)^{-1}\big(\exp(A) - I\big)\cdot \Delta B",
(60, 2): r"h_{k} = \bar{A}h_{k-1} + \bar{B}x_{k}, \quad y_{k} = C h_{k} + D x_{k}"
         r"\qquad\Longleftrightarrow\qquad \bar{K} = \big(C\bar{B},\; C\bar{A}\bar{B},\; \ldots,\; C\bar{A}^{L-1}\bar{B}\big),"
         r"\quad y = x \circledast \bar{K}",
}

PREAMBLE = r"""\documentclass[%dpt,border=1pt]{standalone}
\usepackage{amsmath,amssymb}
\usepackage{newtxtext,newtxmath}
\begin{document}
$\displaystyle %s$
\end{document}
""" 

FALLBACK = r"""\documentclass[%dpt,border=1pt]{standalone}
\usepackage{amsmath,amssymb}
\begin{document}
$\displaystyle %s$
\end{document}
"""


def render(tex, key, tmp):
    """Compile one equation to a transparent PNG. Returns (path, px_w, px_h)."""
    for tmpl in (PREAMBLE, FALLBACK):
        src = tmpl % (BASE_PT, tex)
        io.open(os.path.join(tmp, 'e.tex'), 'w', encoding='utf-8').write(src)
        r = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'e.tex'],
                           cwd=tmp, capture_output=True)
        if r.returncode == 0 and os.path.exists(os.path.join(tmp, 'e.pdf')):
            break
    else:
        raise RuntimeError('pdflatex failed for %s\n%s' %
                           (key, open(os.path.join(tmp, 'e.log')).read()[-1500:]))
    name = 'eq_%d_%d.png' % key
    out = os.path.join(OUT, name)
    subprocess.run(['pdftocairo', '-png', '-r', str(DPI), '-transp', '-singlefile',
                    os.path.join(tmp, 'e.pdf'), out[:-4]], check=True, capture_output=True)
    subprocess.run(['pdftocairo', '-png', '-r', str(DPI_WEB), '-transp', '-singlefile',
                    os.path.join(tmp, 'e.pdf'), os.path.join(OUT_WEB, name)[:-4]],
                   check=True, capture_output=True)
    from PIL import Image
    w, h = Image.open(out).size
    for f in ('e.pdf', 'e.aux', 'e.log'):
        p = os.path.join(tmp, f)
        if os.path.exists(p): os.remove(p)
    return name, w, h


def main():
    S = json.load(open('/home/claude/work/deck/deck.json', encoding='utf-8'))
    shutil.rmtree(OUT, ignore_errors=True)
    shutil.rmtree(OUT_WEB, ignore_errors=True)
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(OUT_WEB, exist_ok=True)
    tmp = '/tmp/eqbuild'
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp, exist_ok=True)

    n = 0
    missing = []
    for s in S:
        if s['t'] != 'math':
            continue
        for i, q in enumerate(s['body']['eqs']):
            key = (s['num'], i)
            if key not in TEX:
                missing.append(key)
                continue
            tex = TEX[key]
            name, w, h = render(tex, key, tmp)
            q['latex'] = tex
            q['img'] = name
            q['imgw'] = w
            q['imgh'] = h
            n += 1
    if missing:
        raise SystemExit('no LaTeX written for: %s' % missing)

    json.dump(S, open('/home/claude/work/deck/deck.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('rendered %d equations at %d dpi -> %s' % (n, DPI, OUT))
    big = sorted(((q['imgw'], s['num']) for s in S if s['t'] == 'math'
                  for q in s['body']['eqs']), reverse=True)[:5]
    print('widest (px, slide):', big)


if __name__ == '__main__':
    main()
