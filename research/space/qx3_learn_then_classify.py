"""QX3: learn-then-classify from labelled reference photons (research/space/PLAN_PREREG.md, Addendum H).

Unknown static pointing offset theta ~ N(0, tau^2). The learner receives n reference photons from a point source
at theta, then ONE test photon from H0 (point at theta) or H1 (equal binary of known d centred at theta).
Exact Bayes errors (equal priors) for: KNOWN, NONE (n = 0), COH (joint Helstrom on references + test, via the exact
reduction |theta>^{(x)n} ~ |sqrt(n) theta/2> and a PCA basis of the weighted reference Gram matrix), MF-DI,
PLUG, MF-SPADE and SYM ((n+1)-photon symmetric projection, closed form).
Run:  python research/space/qx3_learn_then_classify.py      Writes results/qx3/qx3.json
"""
from __future__ import annotations

import os
import sys
import time

import numpy as np
from scipy.stats import poisson

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
from research.qk.util import dump_json, results_dir, run_metadata  # noqa: E402
from research.space.x_suite import amps  # noqa: E402

NTEST = 24                                 # test-photon HG truncation (modes 0..NTEST)
A0S = (0.05, 0.1, 0.2)
TAUS = (0.2, 0.5)
NS = (0, 1, 2, 4, 8, 16, 32, 64, 128)
PCA_THR = 1e-13


def test_D(th, d):
    """D_i = |th_i><th_i| - (|th_i + d/2><.| + |th_i - d/2><.|)/2 in the HG basis, shape (K, nt, nt)."""
    a0, ap, am = amps(th / 2, NTEST), amps((th + d / 2) / 2, NTEST), amps((th - d / 2) / 2, NTEST)
    outer = lambda a: np.einsum("ia,ib->iab", a, a)    # noqa: E731
    return outer(a0) - 0.5 * (outer(ap) + outer(am))


def grid(s, K):
    th = np.linspace(-6 * s, 6 * s, K)
    w = np.exp(-th ** 2 / (2 * s * s))
    return th, w / w.sum()


def tnorm(M):
    return float(np.abs(np.linalg.eigvalsh(M)).sum())


def jitter_D(s, d, K=201):
    """Test-photon difference operator averaged over an offset ~ N(0, s^2)."""
    if s == 0:
        return test_D(np.array([0.0]), d)[0]
    th, w = grid(s, K)
    return np.einsum("i,iab->ab", w, test_D(th, d))


def bayes_jitter(s, d):
    return 0.5 - 0.25 * tnorm(jitter_D(s, d))


def coh_K(n, tau):
    k = int(np.ceil(12 * tau * np.sqrt(max(n, 1) / 0.08))) + 1
    return max(161, k + (k + 1) % 2)


def coh_error(n, tau, d, K, thr=PCA_THR):
    th, w = grid(tau, K)
    D = test_D(th, d)
    if n == 0:
        return 0.5 - 0.25 * tnorm(np.einsum("i,iab->ab", w, D)), 1
    G = np.sqrt(np.outer(w, w)) * np.exp(-n * np.subtract.outer(th, th) ** 2 / 8)
    lam, V = np.linalg.eigh(G)
    keep = lam > thr * lam.max()
    C = V[:, keep] * np.sqrt(lam[keep])                       # row i: coordinates of sqrt(w_i)|b_i>
    r, nt = C.shape[1], NTEST + 1
    C2 = np.einsum("ik,il->ikl", C, C).reshape(K, r * r)
    Delta = (C2.T @ D.reshape(K, nt * nt)).reshape(r, r, nt, nt).transpose(0, 2, 1, 3).reshape(r * nt, r * nt)
    return 0.5 - 0.25 * tnorm(Delta), r


def plug_error(v, d):
    D0 = jitter_D(0.0, d)
    lam, V = np.linalg.eigh(D0)
    pos = lam > 1e-12 * np.abs(lam).max()                     # strictly positive eigenspace of the known-theta D
    Pp = V[:, pos] @ V[:, pos].T
    return 0.5 - 0.5 * float(np.trace(Pp @ jitter_D(np.sqrt(v), d)))


def spade_error(n, tau, d):
    if n == 0:
        return bayes_jitter(tau, d), 1.0
    K = max(801, int(120 * tau * np.sqrt(n)) + 1)
    th, w = grid(tau, K)
    D = test_D(th, d)
    mu = n * th ** 2 / 4
    smax = int(poisson.ppf(1 - 1e-15, mu.max())) + 10
    tot, mass = 0.0, 0.0
    for S in range(smax + 1):
        L = poisson.pmf(S, mu) * w
        if L.sum() < 1e-300:
            continue
        tot += tnorm(np.einsum("i,iab->ab", L, D))
        mass += L.sum()
    return 0.5 - 0.25 * tot, mass


def sym_error(n, d):
    return 0.5 - (n / (n + 1)) * (1 - np.exp(-d * d / 16)) / 2


def run_point(a0, tau, t0):
    d = 4 * a0
    pk = bayes_jitter(0.0, d)
    rec = {"P_KNOWN": pk, "n": list(NS)}
    for key in ("COH", "COH_2K", "MFDI", "PLUG", "SPADE", "SYM", "rank", "spade_mass"):
        rec[key] = []
    for n in NS:
        v = 1 / (n + 1 / tau ** 2)
        K = coh_K(n, tau)
        pc, r = coh_error(n, tau, d, K)
        pc2, _ = coh_error(n, tau, d, 2 * K - 1)
        ps, mass = spade_error(n, tau, d)
        rec["COH"].append(pc)
        rec["COH_2K"].append(pc2)
        rec["rank"].append(r)
        rec["MFDI"].append(bayes_jitter(np.sqrt(v), d))
        rec["PLUG"].append(plug_error(v, d))
        rec["SPADE"].append(ps)
        rec["spade_mass"].append(mass)
        rec["SYM"].append(sym_error(n, d))
    for key in ("COH", "MFDI", "PLUG", "SPADE", "SYM"):
        rec["E_" + key] = [p - pk for p in rec[key]]
        rec["recovered_" + key] = [(0.5 - p) / (0.5 - pk) for p in rec[key]]
    rec["coh_K_conv_max_rel"] = max(abs(a - b) / max(abs(a - pk), 1e-300) for a, b in zip(rec["COH"], rec["COH_2K"]))
    print(f"QX3 a0={a0} tau={tau}: recovered COH {np.round(rec['recovered_COH'], 3).tolist()}", flush=True)
    print(f"   MFDI {np.round(rec['recovered_MFDI'], 3).tolist()}  SPADE {np.round(rec['recovered_SPADE'], 3).tolist()}",
          flush=True)
    print(f"   MFDI/COH excess {np.round(np.array(rec['E_MFDI']) / np.array(rec['E_COH']), 3).tolist()}  "
          f"K-conv {rec['coh_K_conv_max_rel']:.1e}  t={time.time() - t0:.0f}s", flush=True)
    return rec


def thr_check(out):
    rows = []
    for a0, tau, n in ((0.05, 0.5, 128), (0.1, 0.2, 64)):
        d = 4 * a0
        K = coh_K(n, tau)
        pk = bayes_jitter(0.0, d)
        e13 = coh_error(n, tau, d, K, 1e-13)[0] - pk
        e11 = coh_error(n, tau, d, K, 1e-11)[0] - pk
        rows.append({"a0": a0, "tau": tau, "n": n, "E_thr1e-13": e13, "E_thr1e-11": e11})
    out["pca_threshold_check"] = rows
    print("QX3 PCA threshold check", rows, flush=True)


def main() -> None:
    t0 = time.time()
    out = {"meta": run_metadata(), "NTEST": NTEST, "points": {}}
    thr_check(out)
    for tau in TAUS:
        for a0 in A0S:
            out["points"][f"a0{a0}|tau{tau}"] = run_point(a0, tau, t0)
    out["runtime_s"] = time.time() - t0
    dump_json(out, os.path.join(results_dir("qx3"), "qx3.json"))


if __name__ == "__main__":
    main()
