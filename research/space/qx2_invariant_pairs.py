"""QX2: translation-invariant vs U(m)-invariant two-photon measurements (research/space/PLAN_PREREG.md, Addendum H).

Two photons per frame share a slow common jitter X ~ N(0, sj^2); a static unknown crosstalk U acts on HG modes
0..12 of each photon. H0: point source; H1: equal binary of separation d (sigma = 1).
Measurements: M1 = HOM {antisym, sym}; M2 = {rel0, not rel0}; M3 = {antisym, sym minus rel0, rel0}; Q_pair =
exact optimal pair Bhattacharyya exponent (-log F, Gram matrix of coherent-state components); L = learned
projective measurement in the symmetric subspace (triangle m + n <= NT) plus the antisym outcome.
Run:  python research/space/qx2_invariant_pairs.py      Writes results/qx2/qx2.json
"""
from __future__ import annotations

import os
import sys
import time
from math import comb

import numpy as np
import torch
from scipy.linalg import expm

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
from research.qk.util import dump_json, results_dir, run_metadata  # noqa: E402
from research.space.x_suite import amps, gh  # noqa: E402

torch.set_default_dtype(torch.float64)
NT = 24                                   # pair triangle m + n <= NT; must be >= 2*(NX-1) so all crosstalk pairs fit
NX = 13                                   # crosstalk acts on HG modes 0..12
GX, GW = gh(20)
DS = (0.1, 0.2, 0.4, 1.0)
SJS = (0.0, 0.1, 0.2, 0.4, 0.8)
EPSS = (0.0, 1e-4, 3e-4, 1e-3, 3e-3, 0.01, 0.03, 0.1)
KS = (0, 1, 2)

SYM = [(m, n) for m in range(NT + 1) for n in range(m, NT + 1 - m)]
ANTI = [(m, n) for m in range(NT + 1) for n in range(m + 1, NT + 1 - m)]
SI, SJ = np.array([p[0] for p in SYM]), np.array([p[1] for p in SYM])
AI, AJ = np.array([p[0] for p in ANTI]), np.array([p[1] for p in ANTI])
SF = np.where(SI == SJ, 0.5, 1 / np.sqrt(2))
NSYM = len(SYM)


def rel0_basis():
    """Rows v_j (sym coordinates) spanning {relative-coordinate HG0} within the triangle."""
    V = np.zeros((NT + 1, NSYM))
    for c, (m, n) in enumerate(SYM):
        j = m + n
        V[j, c] = np.sqrt(comb(j, m)) * 2.0 ** (-j / 2) * (1.0 if m == n else np.sqrt(2))
    return V


VREL = rel0_basis()


def crosstalk(eps, k):
    U = np.eye(NT + 1)
    if eps > 0:
        A = np.triu(np.random.default_rng(1000 + k).normal(size=(NX, NX)), 1)
        U[:NX, :NX] = expm(eps * (A - A.T))
    return U


def components(h, d, sj):
    """Weights and positions (photon 1, photon 2) of the pure pair components."""
    xs, ws = (np.array([0.0]), np.array([1.0])) if sj == 0 else (GX * sj, GW)
    if h == 0:
        return ws, xs, xs
    parts = [(ws / 4, xs + s1 * d / 2, xs + s2 * d / 2) for s1 in (-1, 1) for s2 in (-1, 1)]
    return tuple(np.concatenate([p[i] for p in parts]) for i in range(3))


def state_data(h, d, sj, U):
    """sqrt(w)-weighted sym coordinates (K, NSYM), antisym probability, remainder probability."""
    w, p1, p2 = components(h, d, sj)
    u, v = amps(p1 / 2, NT) @ U.T, amps(p2 / 2, NT) @ U.T
    s = (u[:, SI] * v[:, SJ] + u[:, SJ] * v[:, SI]) * SF
    a = (u[:, AI] * v[:, AJ] - u[:, AJ] * v[:, AI]) / np.sqrt(2)
    ns, na = np.sum(s ** 2, 1), np.sum(a ** 2, 1)
    return s * np.sqrt(w)[:, None], float(w @ na), max(float(w @ (1 - ns - na)), 0.0)   # clamp -1e-16 roundoff


def bhatt(p, q):
    return float(-np.log(np.sum(np.sqrt(np.clip(p, 0, None) * np.clip(q, 0, None)))))


def fixed_outcomes(data):
    S, pa, pr = data
    proj = S @ VREL.T
    perp = S - proj @ VREL
    return {"anti": pa, "sym": float(np.sum(S ** 2)), "rel0": float(np.sum(proj ** 2)),
            "perp": float(np.sum(perp ** 2)), "rem": pr}


def fixed_exponents(o0, o1):
    def vec(o, kind):
        if kind == "HOM":
            return [o["anti"], o["sym"], o["rem"]]
        if kind == "M2":
            return [o["rel0"], o["perp"] + o["anti"], o["rem"]]
        return [o["anti"], o["perp"], o["rel0"], o["rem"]]

    return {k: bhatt(np.array(vec(o0, k)), np.array(vec(o1, k))) for k in ("HOM", "M2", "M3")}


def q_pair(d, sj):
    w0, a0, b0 = components(0, d, sj)
    w1, a1, b1 = components(1, d, sj)

    def ov(x, y):
        return np.exp(-np.subtract.outer(x, y) ** 2 / 8)

    G = np.sqrt(np.outer(w0, w1)) * ov(a0, a1) * ov(b0, b1)
    return float(-np.log(np.linalg.svd(G, compute_uv=False).sum()))


# ----------------------------------------------------------------- learned measurement in the symmetric subspace
def pack(states):
    kmax = max(max(s0[0].shape[0], s1[0].shape[0]) for s0, s1 in states)

    def pad(S):
        return np.vstack([S, np.zeros((kmax - S.shape[0], NSYM))])

    t = {"S0": torch.tensor(np.array([pad(s0[0]) for s0, _ in states])),
         "S1": torch.tensor(np.array([pad(s1[0]) for _, s1 in states]))}
    for i, key in ((1, "a"), (2, "r")):
        t[key + "0"] = torch.tensor([s0[i] for s0, _ in states])
        t[key + "1"] = torch.tensor([s1[i] for _, s1 in states])
    return t


def make_W(th, A, iu):
    n = NSYM + A
    G = torch.zeros(n, n)
    G[iu] = th
    return torch.matrix_exp(G - G.T)[:, :NSYM]


def exps_learned(W, t):
    p0 = (torch.einsum("om,vkm->vko", W, t["S0"]) ** 2).sum(1)
    p1 = (torch.einsum("om,vkm->vko", W, t["S1"]) ** 2).sum(1)
    bc = torch.sqrt(p0 * p1 + 1e-300).sum(1) + torch.sqrt(t["a0"] * t["a1"] + 1e-300) \
        + torch.sqrt(t["r0"] * t["r1"] + 1e-300)
    return -torch.log(bc)


def train_learned(states, A, steps=1200, restarts=2, seed=0):
    t = pack(states)
    n = NSYM + A
    iu = torch.triu_indices(n, n, 1)
    iu = (iu[0], iu[1])
    g = torch.Generator().manual_seed(seed)
    best = (-np.inf, None, None)
    for r in range(restarts):
        th = torch.zeros(len(iu[0])) if r == 0 else 0.05 * torch.randn(len(iu[0]), generator=g)
        th.requires_grad_(True)
        opt = torch.optim.Adam([th], lr=0.02)
        sched = torch.optim.lr_scheduler.ExponentialLR(opt, gamma=(1e-2) ** (1.0 / steps))
        for _ in range(steps):
            loss = -exps_learned(make_W(th, A, iu), t).min()
            opt.zero_grad()
            loss.backward()
            opt.step()
            sched.step()
        scale = float(exps_learned(make_W(th, A, iu), t).min().detach())
        lb = torch.optim.LBFGS([th], lr=1.0, max_iter=300, tolerance_grad=1e-30, tolerance_change=1e-30,
                               line_search_fn="strong_wolfe")

        def closure():
            lb.zero_grad()
            e = exps_learned(make_W(th, A, iu), t) / max(scale, 1e-300)
            lv = 0.01 * torch.logsumexp(-e / 0.01, 0)
            lv.backward()
            return lv

        lb.step(closure)
        e = exps_learned(make_W(th, A, iu), t).detach().numpy()
        if e.min() > best[0]:
            best = (float(e.min()), e.copy(), th.detach().clone())
    return best


# ----------------------------------------------------------------- experiment
def part_fixed(out):
    rec = {}
    for d in DS:
        q_h, q_t = (1 - np.exp(-d * d / 4)) / 4, (1 - np.exp(-d * d / 8)) / 2
        rec[d] = {"q_H": q_h, "q_T": q_t, "M3_pred_eps0": -0.5 * np.log(1 - q_t),
                  "HOM_pred": -0.5 * np.log(1 - q_h), "Q_pair": {}, "rows": []}
        for sj in SJS:
            rec[d]["Q_pair"][sj] = q_pair(d, sj)
            for eps in EPSS:
                for k in (KS if eps > 0 else (0,)):
                    U = crosstalk(eps, k)
                    o0, o1 = fixed_outcomes(state_data(0, d, sj, U)), fixed_outcomes(state_data(1, d, sj, U))
                    ex = fixed_exponents(o0, o1)
                    rec[d]["rows"].append({"sj": sj, "eps": eps, "k": k, **ex, "leak_H0_perp": o0["perp"],
                                           "anti_H0": o0["anti"], "rem_H0": o0["rem"]})
        print(f"QX2 fixed d={d}: Q_pair {[round(v, 6) for v in rec[d]['Q_pair'].values()]}", flush=True)
    out["fixed"] = {str(d): v for d, v in rec.items()}
    return rec


def box_states(d):
    states, labels = [], []
    for sj in SJS:
        for eps, k in [(0.0, 0)] + [(e, k) for e in (0.01, 0.03, 0.1) for k in KS]:
            U = crosstalk(eps, k)
            states.append((state_data(0, d, sj, U), state_data(1, d, sj, U)))
            labels.append({"sj": sj, "eps": eps, "k": k})
    return states, labels


def held_out(d, A, th):
    n = NSYM + A
    iu = torch.triu_indices(n, n, 1)
    W = make_W(th, A, (iu[0], iu[1]))
    rows = []
    for sj in (0.4, 0.8):
        for eps in (0.03, 0.05, 0.1):
            for k in (3, 4):
                U = crosstalk(eps, k)
                t = pack([(state_data(0, d, sj, U), state_data(1, d, sj, U))])
                rows.append({"sj": sj, "eps": eps, "k": k, "L": float(exps_learned(W, t).detach()[0])})
    return rows


def part_learned(out, t0):
    out["learned_single"], out["learned_box"] = {}, {}
    for d in (0.2, 0.4):
        for sj, eps in ((0.0, 0.0), (0.2, 0.0), (0.2, 0.03)):
            U = crosstalk(eps, 0)
            val = train_learned([(state_data(0, d, sj, U), state_data(1, d, sj, U))], 0, seed=7)[0]
            qp = q_pair(d, sj)
            out["learned_single"][f"d{d}|sj{sj}|eps{eps}"] = {"L": val, "Q_pair": qp, "ratio": val / qp}
            print(f"QX2 L(i) d={d} sj={sj} eps={eps}: L/Q_pair {val / qp:.4f}  t={time.time() - t0:.0f}s", flush=True)
        states, labels = box_states(d)
        hom = -0.5 * np.log(1 - (1 - np.exp(-d * d / 4)) / 4)
        qmin = min(q_pair(d, sj) for sj in SJS)
        for A in (0, 8):
            val, per_state, th = train_learned(states, A, seed=11 + A)
            held = held_out(d, A, th)
            out["learned_box"][f"d{d}|A{A}"] = {"minimax": val, "HOM": hom, "minimax_over_HOM": val / hom,
                                                "min_Q_pair": qmin, "per_state": list(map(float, per_state)),
                                                "labels": labels, "held_out_not_preregistered": held}
            print(f"QX2 L(ii) d={d} A={A}: minimax/HOM {val / hom:.4f}, min Q_pair/HOM {qmin / hom:.4f}, "
                  f"held-out min/HOM {min(h['L'] for h in held) / hom:.4f}  t={time.time() - t0:.0f}s", flush=True)


def main() -> None:
    t0 = time.time()
    out = {"meta": run_metadata(), "NT": NT, "NX": NX}
    part_fixed(out)
    part_learned(out, t0)
    out["runtime_s"] = time.time() - t0
    dump_json(out, os.path.join(results_dir("qx2"), "qx2.json"))


if __name__ == "__main__":
    main()
