"""QX3-E: many-test-photon error exponents under an unknown static pointing offset (PLAN_PREREG.md, Addendum I).

N test photons (H0 point / H1 equal binary, a0 = d/4, sigma = 1) share an unknown pointing theta; optionally
kappa*N labelled point-source reference photons. Exponents per test photon, as fractions of a0^2 (known-theta QCB):
  Q-SCHUR_k : symmetric-subspace projection of k stored test photons (no references), closed form
  Q-REF     : (kappa+1)-photon symmetric projection of each test photon with kappa fresh references, closed form
  C-SPADE   : DI centroid (references + fraction f of test photons) + HG0..HG5 + rest at the estimate;
              large-deviation exponent min_{t0,t1} max_s [...] maximised over f
  C-LEARN   : as C-SPADE with a learned real orthogonal 6-mode receiver (Powell, from SPADE)
  finite-N  : exact Bayes error of the 3-cell SPADE receiver (f = 0) for N up to 8000
Run:  python research/space/qx3e_exponents.py      Writes results/qx3e/qx3e.json
"""
from __future__ import annotations

import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize, minimize_scalar
from scipy.special import gammaln, logsumexp
from scipy.stats import poisson

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
from research.qk.util import dump_json, results_dir, run_metadata  # noqa: E402
from research.space.x_suite import amps, binary, gh, qcb_mp, rho1d  # noqa: E402

A0S = (0.05, 0.1, 0.2)
KAPPAS = (0, 0.1, 0.3, 1, 3, 10, 30, 100, 1000)
KS = (2, 3, 4, 8, 16)
MR = 6                                     # learned receiver acts on HG modes 0..MR-1 (+ rest port)


# ----------------------------------------------------------------- quantum closed forms
def schur(a0, k=None):
    l1 = (1 + np.exp(-2 * a0 * a0)) / 2
    if k is None:
        return float(-np.log(l1))
    h = sum(l1 ** j * (1 - l1) ** (k - j) for j in range(k + 1))
    return float(-np.log(h) / k)


def qref(a0, kap):
    return float(-np.log(1 - kap * (1 - np.exp(-a0 * a0)) / (kap + 1)))


# ----------------------------------------------------------------- receivers: port probabilities vs offset t
def spade_ports(t, d, h, ncell=7):
    def cells(mu):
        if ncell == 3:
            return np.stack([poisson.pmf(0, mu), poisson.pmf(1, mu), poisson.sf(1, mu)], 1)
        P = poisson.pmf(np.arange(ncell - 1)[None, :], mu[:, None])
        return np.hstack([P, poisson.sf(ncell - 2, mu)[:, None]])

    t = np.atleast_1d(t)
    if h == 0:
        return cells(t ** 2 / 4)
    return 0.5 * (cells((t + d / 2) ** 2 / 4) + cells((t - d / 2) ** 2 / 4))


def learned_ports(W, t, d, h):
    t = np.atleast_1d(t)

    def one(x):
        A = amps(x / 2, MR - 1) @ W.T
        return np.hstack([A ** 2, poisson.sf(MR - 1, x ** 2 / 4)[:, None]])

    if h == 0:
        return one(t)
    return 0.5 * (one(t + d / 2) + one(t - d / 2))


# ----------------------------------------------------------------- large-deviation exponent
TG = np.concatenate([[0.0], np.geomspace(1e-5, 1.0, 120)])     # offset grid (scaled by d below)
SG = np.linspace(0.0, 1.0, 101)
TG_C = np.concatenate([[0.0], np.geomspace(1e-5, 1.0, 40)])   # coarse grids for training only
SG_C = np.linspace(0.0, 1.0, 41)


def pair_value(p0, p1, g0, g1, alpha):
    """max_s [s g0 + (1-s) g1 - alpha log sum p0^s p1^(1-s)] (exact one-sided limits at s = 0, 1)."""
    m = (p0 > 0) & (p1 > 0)
    l0, l1 = np.log(p0[m]), np.log(p1[m])

    def neg(s):
        return -(s * g0 + (1 - s) * g1 - alpha * logsumexp(s * l0 + (1 - s) * l1))

    r = minimize_scalar(neg, bounds=(0.0, 1.0), method="bounded", options={"xatol": 1e-11})
    return -min(r.fun, neg(0.0), neg(1.0))


def exponent(ports, d, rate, f, refine=True, tg_scale=2.0, tgrid=None, sgrid=None, even=True):
    """min over (t0, t1) of the pairwise value; rate = kappa + f; ports(t, h) -> (len(t), J).

    even=True is valid only for receivers whose port probabilities are even in the offset t (SPADE); any
    receiver that mixes HG modes of opposite parity must use even=False (offsets of both signs).
    """
    tgrid = TG if tgrid is None else tgrid
    SGr = SG if sgrid is None else sgrid
    tpos = tgrid * tg_scale * d
    tg = tpos if even else np.concatenate([-tpos[:0:-1], tpos])
    P0, P1 = ports(tg, 0), ports(tg, 1)
    g = rate * tg ** 2 / 2
    alpha = 1 - f
    M = (P0[:, None, :] > 0) & (P1[None, :, :] > 0)
    L0 = np.log(np.where(P0 > 0, P0, 1.0))
    L1 = np.log(np.where(P1 > 0, P1, 1.0))
    Fg = np.full((len(tg), len(tg)), -np.inf)
    for c in range(0, len(SGr), 20):                                # chunk over s to bound memory
        S = SGr[c:c + 20]
        expo = S[:, None, None, None] * L0[None, :, None, :] + (1 - S)[:, None, None, None] * L1[None, None, :, :]
        lse = logsumexp(np.where(M[None], expo, -np.inf), axis=3)    # (S, n0, n1)
        val = S[:, None, None] * g[None, :, None] + (1 - S)[:, None, None] * g[None, None, :] - alpha * lse
        Fg = np.maximum(Fg, val.max(0))
    if not refine:
        return float(Fg.min()), None
    best = (np.inf, None)
    for flat in np.argsort(Fg, axis=None)[:6]:
        i, k = np.unravel_index(flat, Fg.shape)

        def F(x):
            t0, t1 = (abs(x[0]), abs(x[1])) if even else (x[0], x[1])
            return pair_value(ports(np.array([t0]), 0)[0], ports(np.array([t1]), 1)[0],
                              rate * t0 ** 2 / 2, rate * t1 ** 2 / 2, alpha)

        r = minimize(F, [tg[i], tg[k]], method="Nelder-Mead",
                     options={"xatol": 1e-9 * d, "fatol": 1e-16, "maxiter": 600})
        xr = list(np.abs(r.x)) if even else list(r.x)
        cand = min((r.fun, xr), (float(Fg[i, k]), [tg[i], tg[k]]))
        if cand[0] < best[0]:
            best = cand
    return float(best[0]), best[1]


def best_over_f(ports, d, kap, refine=True):
    fs = np.linspace(0.0, 0.9, 19)
    vals = [exponent(ports, d, kap + f, f, refine=False)[0] for f in fs]
    i = int(np.argmax(vals))
    lo, hi = fs[max(i - 1, 0)], fs[min(i + 1, len(fs) - 1)]
    r = minimize_scalar(lambda f: -exponent(ports, d, kap + f, f, refine=False)[0], bounds=(lo, hi),
                        method="bounded", options={"xatol": 1e-4})
    f = float(r.x) if -r.fun >= vals[i] else float(fs[i])
    E, tt = exponent(ports, d, kap + f, f, refine=refine)
    return E, f, tt


# ----------------------------------------------------------------- learned single-photon receiver
def W_of(th):
    G = np.zeros((MR, MR))
    G[np.triu_indices(MR, 1)] = th
    return expm(G - G.T)


def learn_receiver(a0, kap, f0, seed):
    d = 4 * a0
    npar = MR * (MR - 1) // 2
    rng = np.random.default_rng(seed)

    def obj(x):
        W, f = W_of(x[:npar]), 0.9 / (1 + np.exp(-x[npar]))
        return -exponent(lambda t, h: learned_ports(W, t, d, h), d, kap + f, f, refine=False,
                         tgrid=TG_C, sgrid=SG_C, even=False)[0]

    f_init = np.log(max(f0, 1e-3) / max(0.9 - f0, 1e-3))
    best = None
    for r in range(3):
        x0 = np.append(np.zeros(npar) if r == 0 else 0.3 * rng.normal(size=npar), f_init)
        res = minimize(obj, x0, method="Powell", options={"maxiter": 4000, "xtol": 1e-4, "ftol": 1e-10})
        if best is None or res.fun < best.fun:
            best = res
    W, f = W_of(best.x[:npar]), 0.9 / (1 + np.exp(-best.x[npar]))
    E, tt = exponent(lambda t, h: learned_ports(W, t, d, h), d, kap + f, f, refine=True, even=False)
    return E, float(f), tt, W


# ----------------------------------------------------------------- exact finite N (3-cell SPADE, f = 0)
def exact_finite(a0, kap, N, nodes=80, k1max=None, k2max=30):
    d = 4 * a0
    x, w = gh(nodes)
    delta = x / np.sqrt(kap * N)
    k1max = k1max or int(N * (a0 * a0 + 0.02) + 60)
    k1 = np.arange(k1max + 1)[:, None]
    k2 = np.arange(k2max + 1)[None, :]
    k0 = N - k1 - k2
    lm = gammaln(N + 1) - gammaln(k0 + 1) - gammaln(k1 + 1) - gammaln(k2 + 1)
    logP = []
    for h in (0, 1):
        P = spade_ports(delta, d, h, ncell=3)
        L = np.log(P)
        terms = lm[None] + k0[None] * L[:, 0, None, None] + k1[None] * L[:, 1, None, None] \
            + k2[None] * L[:, 2, None, None] + np.log(w)[:, None, None]
        logP.append(logsumexp(terms, axis=0))
    perr = 0.5 * float(np.sum(np.exp(np.minimum(logP[0], logP[1]))))
    mass = [float(np.exp(logsumexp(lp))) for lp in logP]
    return perr, mass


# ----------------------------------------------------------------- experiment
def part_quantum(out):
    rec = {}
    for a0 in A0S:
        d = 4 * a0
        r0, r1 = rho1d((np.array([0.0]), np.array([1.0]))), rho1d(binary(d))
        rec[str(a0)] = {"QCB_known_numeric": float(qcb_mp(r0, r1)), "a0sq": a0 * a0,
                        "schur_inf": schur(a0), "schur_k": {k: schur(a0, k) for k in KS},
                        "qref": {k: qref(a0, k) for k in (1, 3, 10, 30, 100)}}
        print(f"QX3-E quantum a0={a0}: QCB/a0^2 {rec[str(a0)]['QCB_known_numeric'] / a0 ** 2:.6f}, "
              f"SCHUR_inf/a0^2 {schur(a0) / a0 ** 2:.4f}", flush=True)
    out["quantum"] = rec


def spade_job(args):
    a0, kap = args
    d = 4 * a0
    E, f, tt = best_over_f(lambda t, h: spade_ports(t, d, h), d, kap)
    return {"kappa": kap, "E": E, "E_over_a0sq": E / a0 ** 2, "f": f, "worst_t0_t1": tt}


def learn_job(args):
    a0, kap, f0 = args
    E, f, tt, W = learn_receiver(a0, kap, f0, seed=int(1000 * a0) + kap)
    return {"E": E, "E_over_a0sq": E / a0 ** 2, "f": f, "W": W.tolist(), "worst_t0_t1": tt}


def part_classical(out, t0, pool):
    rec = {}
    jobs = [(a0, kap) for a0 in A0S for kap in KAPPAS]
    for (a0, kap), row in zip(jobs, pool.map(spade_job, jobs)):
        rec.setdefault(str(a0), []).append(row)
    for a0 in A0S:
        print(f"QX3-E C-SPADE a0={a0}: " + ", ".join(f"k{r['kappa']}:{r['E_over_a0sq']:.3f}(f{r['f']:.2f})"
                                                     for r in rec[str(a0)]) + f"  t={time.time() - t0:.0f}s", flush=True)
    out["c_spade"] = rec


def part_learned(out, t0, pool):
    rec = {}
    jobs = []
    for a0 in (0.05, 0.1):
        for kap in (0, 1, 10, 100):
            sp = next(r for r in out["c_spade"][str(a0)] if r["kappa"] == kap)
            jobs.append((a0, kap, sp["f"]))
    for (a0, kap, _), row in zip(jobs, pool.map(learn_job, jobs)):
        sp = next(r for r in out["c_spade"][str(a0)] if r["kappa"] == kap)
        row["over_spade"] = row["E"] / sp["E"]
        rec[f"a0{a0}|k{kap}"] = row
        print(f"QX3-E C-LEARN a0={a0} kappa={kap}: {row['E_over_a0sq']:.4f} a0^2, learned/SPADE {row['over_spade']:.4f}"
              f"  t={time.time() - t0:.0f}s", flush=True)
    out["c_learn"] = rec


def part_finite(out, t0):
    rec = {}
    a0 = 0.1
    d = 4 * a0
    for kap in (1, 10):
        E_ld = exponent(lambda t, h: spade_ports(t, d, h, ncell=3), d, kap, 0.0)[0]
        Ns = [250, 500, 1000, 2000, 4000, 8000]
        res = [exact_finite(a0, kap, N) for N in Ns]
        pe = [r[0] for r in res]
        loc = [-(np.log(pe[i + 1]) - np.log(pe[i])) / (Ns[i + 1] - Ns[i]) for i in range(len(Ns) - 1)]
        schur_pe = [0.5 * np.exp(-N * schur(a0)) for N in Ns]          # leading order of (1/2) h_N
        rec[f"k{kap}"] = {"N": Ns, "P_err": pe, "mass": [r[1] for r in res], "local_exponent": loc,
                          "LD_exponent": E_ld, "local_over_LD": [v / E_ld for v in loc],
                          "schur_P_err_leading": schur_pe}
        print(f"QX3-E finite kappa={kap}: local/LD {[round(v / E_ld, 3) for v in loc]}, P_err {pe[-1]:.2e}"
              f"  t={time.time() - t0:.0f}s", flush=True)
    out["finite_N"] = rec


def main() -> None:
    t0 = time.time()
    out = {"meta": run_metadata()}
    part_quantum(out)
    with ProcessPoolExecutor(max_workers=5) as pool:          # ~400 MB peak per worker
        part_classical(out, t0, pool)
        part_learned(out, t0, pool)
    part_finite(out, t0)
    out["runtime_s"] = time.time() - t0
    dump_json(out, os.path.join(results_dir("qx3e"), "qx3e.json"))


if __name__ == "__main__":
    main()
