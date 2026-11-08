"""Exact per-photon distinguishability exponents for H-S1..H-S4 (research/space/PLAN_PREREG.md).

1D Gaussian PSF (intensity N(0, sigma^2), sigma = 1). Per photon:
  DI       squared Hellinger H^2 = 1/2 int (sqrt p1 - sqrt p0)^2 dx      (direct imaging)
  SPADE    H^2 over Hermite-Gauss mode populations (sorter centred on the H1 centroid)
  SIGN     H^2 for sign-sensitive ports (|n> +- |n+1>)/sqrt2  (H-S4 only)
  QUANTUM  1 - F, F = root fidelity; rho1 has rank 2 so F = sqrt(M11 + M22 + 2 sqrt(det M)),
           M_ij = sqrt(w_i w_j) <psi_i| rho0 |psi_j>, computed in closed form or by quadrature (mpmath, no
           Hilbert-space truncation).
The H0 nuisance is chosen least favourably SEPARATELY for each receiver (min over nuisance of its H^2).
Run:  python research/space/s01_exponents.py      Writes results/s01_exponents/exponents.json
"""
from __future__ import annotations

import os
import sys

import mpmath as mp
import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.special import erf, gammaln, roots_hermite, roots_legendre

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
from research.qk.util import dump_json, results_dir, run_metadata  # noqa: E402

mp.mp.dps = 50
XG = np.linspace(-16.0, 16.0, 320001)
NMAX = 14
A0_GRID = np.geomspace(0.02, 0.1, 9)
GH_X, GH_W = roots_hermite(90)
GL_X, GL_W = roots_legendre(120)


def npdf(x, m, v):
    return np.exp(-(x - m) ** 2 / (2 * v)) / np.sqrt(2 * np.pi * v)


def hellinger_cont(p, q):
    d = (p - q) ** 2 / (np.sqrt(p) + np.sqrt(q) + 1e-300) ** 2
    return 0.5 * np.trapezoid(d, XG)


def hellinger_disc(p, q):
    p = np.append(p, max(1 - p.sum(), 0.0))
    q = np.append(q, max(1 - q.sum(), 0.0))
    den = (np.sqrt(p) + np.sqrt(q)) ** 2
    ok = den > 0
    return 0.5 * float(np.sum((p[ok] - q[ok]) ** 2 / den[ok]))


# ---------------- source-position distributions as (positions, weights) ----------------
def mu_points(xs, ws):
    return np.asarray(xs, float), np.asarray(ws, float)


def mu_gauss(c, s):
    return c + np.sqrt(2) * s * GH_X, GH_W / np.sqrt(np.pi)


def mu_uniform(R):
    return R * GL_X, GL_W / 2


def mu_semicircle(R):
    th = 0.5 * np.pi * GL_X
    w = GL_W * np.cos(th) ** 2
    return R * np.sin(th), w / w.sum()


# ---------------- receivers ----------------
def di_pdf(mu, kind=None, par=None):
    if kind == "gauss":
        c, s = par
        return npdf(XG, c, 1 + s * s)
    if kind == "uniform":
        R = par
        return (erf((XG + R) / np.sqrt(2)) - erf((XG - R) / np.sqrt(2))) / (4 * R)
    xs, ws = mu
    return sum(w * npdf(XG, x, 1.0) for x, w in zip(xs, ws))


def logfact(n):
    return gammaln(n + 1)


def rho_elements(mu, xs_centre, nmax=NMAX):
    """rho_nm = E[e^{-a^2} a^{n+m}] / sqrt(n! m!), a = (X - centre)/2."""
    xs, ws = mu
    a = (xs - xs_centre) / 2.0
    n = np.arange(nmax + 1)
    amp = np.exp(-a[:, None] ** 2 / 2 + n[None, :] * np.log(np.abs(a[:, None]) + 1e-300)
                 - 0.5 * logfact(n)[None, :]) * np.sign(a[:, None]) ** n[None, :]
    amp[:, 0] = np.exp(-a ** 2 / 2)
    return (amp * ws[:, None]).T @ amp


def spade_pops(mu, centre):
    return np.clip(np.diag(rho_elements(mu, centre)), 0, None)


def sign_ports(mu, centre, start):
    r = rho_elements(mu, centre)
    probs = [r[n, n] for n in range(start)]
    for n in range(start, NMAX, 2):
        for sg in (1, -1):
            probs.append(0.5 * (r[n, n] + r[n + 1, n + 1] + 2 * sg * r[n, n + 1]))
    return np.clip(np.array(probs), 0, None)


# ---------------- quantum root fidelity ----------------
def overlap_expect(kind, par, xi, xj):
    """<psi_i| rho0 |psi_j> = E_X[g(X-xi) g(X-xj)], g(u) = exp(-u^2/8) (sigma = 1)."""
    xi, xj = mp.mpf(xi), mp.mpf(xj)
    pre = mp.e ** (-(xi - xj) ** 2 / 16)
    m = (xi + xj) / 2
    if kind == "gauss":
        c, s = mp.mpf(par[0]), mp.mpf(par[1])
        return pre * (1 + s * s / 2) ** mp.mpf(-0.5) * mp.e ** (-(c - m) ** 2 / (4 + 2 * s * s))
    if kind == "point":
        c = mp.mpf(par)
        return pre * mp.e ** (-(c - m) ** 2 / 4)
    R = mp.mpf(par)
    if kind == "uniform":
        f = lambda x: mp.e ** (-(x - m) ** 2 / 4) / (2 * R)
    else:  # semicircle
        f = lambda x: mp.e ** (-(x - m) ** 2 / 4) * 2 * mp.sqrt(R * R - x * x) / (mp.pi * R * R)
    return pre * mp.quad(f, [-R, 0, R])


def one_minus_F(h1_pts, h1_w, kind, par):
    M = [[mp.sqrt(mp.mpf(h1_w[i]) * h1_w[j]) * overlap_expect(kind, par, h1_pts[i], h1_pts[j])
          for j in range(2)] for i in range(2)]
    det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    F = mp.sqrt(M[0][0] + M[1][1] + 2 * mp.sqrt(max(det, mp.mpf(0))))
    return float(1 - F)


# ---------------- scenario drivers ----------------
def h1_binary(a0):
    d = 4 * a0
    return [-d / 2, d / 2], [0.5, 0.5]


def h1_companion(a0, eps):
    d = 4 * a0
    return [0.0, d], [1 - eps, eps]


def best_1d(obj, lo, hi):
    r = minimize_scalar(obj, bounds=(lo, hi), method="bounded", options={"xatol": 1e-11})
    return float(r.fun), float(r.x)


def scenario_point(a0):
    pts, w = h1_binary(a0)
    mu1 = mu_points(pts, w)
    mu0 = mu_points([0.0], [1.0])
    return {"DI": hellinger_cont(di_pdf(mu1), di_pdf(mu0)),
            "SPADE": hellinger_disc(spade_pops(mu1, 0.0), spade_pops(mu0, 0.0)),
            "QUANTUM": one_minus_F(pts, w, "point", 0.0)}


def scenario_spread(a0, family):
    pts, w = h1_binary(a0)
    mu1 = mu_points(pts, w)
    p1, P1 = di_pdf(mu1), spade_pops(mu1, 0.0)
    m2 = (2 * a0) ** 2                       # second moment of the binary's positions (d/2)^2
    scale = {"gauss": np.sqrt(m2), "uniform": np.sqrt(3 * m2), "semicircle": np.sqrt(4 * m2)}[family]

    def par(u):
        return u * scale

    def mu0(u):
        if family == "gauss":
            return mu_gauss(0.0, par(u))
        return mu_uniform(par(u)) if family == "uniform" else mu_semicircle(par(u))

    def di0(u):
        if family == "gauss":
            return di_pdf(None, "gauss", (0.0, par(u)))
        if family == "uniform":
            return di_pdf(None, "uniform", par(u))
        return di_pdf(mu0(u))

    qkind = family
    qpar = (lambda u: (0.0, par(u))) if family == "gauss" else par
    out = {}
    out["DI"], uDI = best_1d(lambda u: hellinger_cont(p1, di0(u)), 0.3, 2.0)
    out["SPADE"], uSP = best_1d(lambda u: hellinger_disc(P1, spade_pops(mu0(u), 0.0)), 0.3, 2.0)
    out["QUANTUM"], uQ = best_1d(lambda u: one_minus_F(pts, w, qkind, qpar(u)), 0.3, 2.0)
    out["least_favourable_u"] = {"DI": uDI, "SPADE": uSP, "QUANTUM": uQ}
    return out


def scenario_companion(a0, eps):
    pts, w = h1_companion(a0, eps)
    mu1 = mu_points(pts, w)
    cen = eps * pts[1]
    m2 = eps * (1 - eps) * pts[1] ** 2
    p1 = di_pdf(mu1)
    P1 = spade_pops(mu1, cen)
    S1a, S1b = sign_ports(mu1, cen, 1), sign_ports(mu1, cen, 0)

    def unpack(v):
        return cen + v[0] * np.sqrt(m2), np.sqrt(m2) * abs(v[1])

    def opt(f):
        best = None
        for x0 in ([0.0, 1.0], [0.3, 0.8], [-0.3, 1.2]):
            r = minimize(lambda v: f(*unpack(v)), x0, method="Nelder-Mead",
                         options={"xatol": 1e-10, "fatol": 1e-30, "maxiter": 4000})
            if best is None or r.fun < best.fun:
                best = r
        return float(best.fun)

    return {
        "DI": opt(lambda c, s: hellinger_cont(p1, di_pdf(None, "gauss", (c, s)))),
        "SPADE": opt(lambda c, s: hellinger_disc(P1, spade_pops(mu_gauss(c, s), cen))),
        "SIGN_12": opt(lambda c, s: hellinger_disc(S1a, sign_ports(mu_gauss(c, s), cen, 1))),
        "SIGN_01": opt(lambda c, s: hellinger_disc(S1b, sign_ports(mu_gauss(c, s), cen, 0))),
        "QUANTUM": opt(lambda c, s: one_minus_F(pts, w, "gauss", (c, s))),
    }


def slope(xs, ys):
    return float(np.polyfit(np.log(xs), np.log(ys), 1)[0])


def run_sweep(name, fn, a0s):
    rows = [fn(a) for a in a0s]
    keys = [k for k in rows[0] if k != "least_favourable_u"]
    res = {k: {"a0": list(map(float, a0s)), "H2": [float(r[k]) for r in rows],
               "slope": slope(a0s, [r[k] for r in rows])} for k in keys}
    if "least_favourable_u" in rows[0]:
        res["least_favourable_u"] = [r["least_favourable_u"] for r in rows]
    print(name, {k: round(v["slope"], 3) for k, v in res.items() if isinstance(v, dict)}, flush=True)
    return res


def main() -> None:
    out = {"meta": run_metadata(), "a0_grid": list(map(float, A0_GRID))}
    out["H-S1_point"] = run_sweep("H-S1 point", scenario_point, A0_GRID)
    for fam in ("gauss", "uniform", "semicircle"):
        out[f"H-S{2 if fam == 'gauss' else 3}_{fam}"] = run_sweep(
            f"H-S{2 if fam == 'gauss' else 3} {fam}", lambda a, f=fam: scenario_spread(a, f), A0_GRID)
    out["H-S4_companion_eps0.03"] = run_sweep(
        "H-S4 eps=0.03 (a0 sweep)", lambda a: scenario_companion(a, 0.03), A0_GRID)
    eps_grid = np.geomspace(0.005, 0.05, 6)
    rows = [scenario_companion(0.05, e) for e in eps_grid]
    out["H-S4_companion_a0=0.05_eps_sweep"] = {
        k: {"eps": list(map(float, eps_grid)), "H2": [r[k] for r in rows],
            "slope_eps": slope(eps_grid, [r[k] for r in rows])} for k in rows[0]}
    print("H-S4 eps sweep slopes", {k: round(v["slope_eps"], 3)
                                    for k, v in out["H-S4_companion_a0=0.05_eps_sweep"].items()})
    dump_json(out, os.path.join(results_dir("s01_exponents"), "exponents.json"))


if __name__ == "__main__":
    main()
