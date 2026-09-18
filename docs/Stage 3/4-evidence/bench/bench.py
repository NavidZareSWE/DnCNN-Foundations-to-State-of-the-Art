"""
Stage 2/3 benchmark — parameter counts and CPU forward-pass latency.

Each architecture is instantiated from its own repository at the commit pinned in
STAGE3.md, in the configuration that repository uses for denoising.

  parameters : sum(p.numel() for p in model.parameters())
  latency    : mean of 3 forward passes at 256x256 after 1 warm-up pass,
               torch.no_grad(), CPU only, PyTorch 2.13.0, no CUDA.

CAVEATS (reproduced on every slide that quotes these numbers):
  * inputs are RANDOM TENSORS -> no PSNR/SSIM is measured here
  * absolute CPU latencies are NOT comparable to published GPU timings;
    only the ratios between rows are informative
"""
import importlib.util, sys, time, pathlib
import torch

REPOS = pathlib.Path("repos")

def load(path, name):
    """Load an architecture file directly by path, bypassing basicsr namespace collisions."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

def measure(model, shape=(1, 3, 256, 256), runs=3):
    model.eval()
    x = torch.randn(*shape)
    with torch.no_grad():
        model(x)                       # warm-up
        t0 = time.perf_counter()
        for _ in range(runs):
            model(x)
        dt = (time.perf_counter() - t0) / runs
    n = sum(p.numel() for p in model.parameters())
    return n, dt

def report(label, cfg, model, shape):
    try:
        n, dt = measure(model, shape)
        print(f"{label:34s} {cfg:38s} {n/1e6:8.3f} M {dt:8.3f} s")
    except Exception as exc:
        print(f"{label:34s} {cfg:38s} {'not measurable':>10s}   {type(exc).__name__}: {exc}")

def main():
    torch.set_num_threads(torch.get_num_threads())
    print(f"PyTorch {torch.__version__} | CUDA available: {torch.cuda.is_available()}")
    print(f"{'model':34s} {'configuration':38s} {'params':>10s} {'256^2':>10s}")

    m = load(REPOS / "KAIR/models/network_dncnn.py", "kair_dncnn")
    report("DnCNN-B", "DnCNN(in_nc=1, nc=64, nb=20)",
           m.DnCNN(in_nc=1, out_nc=1, nc=64, nb=20), (1, 1, 256, 256))

    m = load(REPOS / "SCUNet/models/network_scunet.py", "scunet")
    report("SCUNet", "config=[2]*7, dim=64",
           m.SCUNet(in_nc=3, config=[2]*7, dim=64), (1, 3, 256, 256))

    m = load(REPOS / "Restormer/basicsr/models/archs/restormer_arch.py", "restormer")
    report("Restormer", "dim=48, [4,6,6,8]", m.Restormer(), (1, 3, 256, 256))

    m = load(REPOS / "NAFNet/basicsr/models/archs/NAFNet_arch.py", "nafnet")
    report("NAFNet", "width=64, enc [2,2,4,8], mid 12",
           m.NAFNet(img_channel=3, width=64, middle_blk_num=12,
                    enc_blk_nums=[2, 2, 4, 8], dec_blk_nums=[2, 2, 2, 2]),
           (1, 3, 256, 256))

    m = load(REPOS / "P2N-plus/models.py", "p2n")
    for mode in ("plain", "SPI"):
        report(f"P2N+ backbone, SPI {'on' if mode=='SPI' else 'off'}",
               f"UNet_n2n_un(conv_type='{mode}')",
               m.UNet_n2n_un(conv_type=mode), (1, 3, 256, 256))

    # MambaIR is expected to fail without compiled CUDA extensions.
    # That failure is a reported RESULT, not a gap in the experiment.
    try:
        m = load(REPOS / "MambaIR/basicsr/archs/mambair_arch.py", "mambair")
        report("MambaIR", "denoising config", m.MambaIR(), (1, 3, 256, 256))
    except Exception as exc:
        print(f"{'MambaIR':34s} {'-':38s} {'not measurable':>10s}   {type(exc).__name__}: {exc}")

if __name__ == "__main__":
    main()
