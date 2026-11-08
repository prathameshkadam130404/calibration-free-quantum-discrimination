"""X1-X5 suite (research/space/PLAN_PREREG.md, Addendum E; design in RESEARCH_2D_ENTANGLEMENT_SAR.md s.8).

Gaussian PSF, sigma = 1, a = X/2, binary a0 = d/4. Exact per-photon (or per-pair) distinguishabilities:
squared Hellinger H2, Bhattacharyya exponent -log BC, quantum 1-F (root fidelity) and the quantum Chernoff
exponent (QCB). 1D quantum quantities use mpmath eigendecompositions; 2D separable cases use products of 1D
quantities.
Run:  python research/space/x_suite.py X1 X4 X5 X3 X2      Writes results/x_suite/<X>.json
"""
from __future__ import annotations

import os
import sys
import time
from itertools import combinations_with_replacement
from math import factorial

import mpmath as mp
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize, minimize_scalar
from scipy.special import roots_hermite, roots_legendre

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
from research.qk.util import dump_json, results_dir, run_metadata  # noqa: E402
from research.space.s01_exponents import one_minus_F  # noqa: E402

mp.mp.dps = 40
GH_X, GH_W = roots_hermite(60)
GHW = GH_W / np.sqrt(np.pi)
GL_X, GL_W = roots_legendre(80)
XG = np.linspace(-12.0, 12.0, 24001)
A0S = np.geomspace(0.02, 0.1, 9)
NM = 16                                    # 1D HG truncation (modes 0..NM)


# ----------------------------------------------------------------- 1D building blocks
def amps(a, nmax=NM):
    a = np.atleast_1d(np.asarray(a, float))
    out = np.empty((len(a), nmax + 1))
    out[:, 0] = np.exp(-a ** 2 / 2)
    for k in range(1, nmax + 1):
        out[:, k] = out[:, k - 1] * a / np.sqrt(k)
    return out


def gpts(c, s):
    return c + np.sqrt(2) * s * GH_X, GHW.copy()


def mix(*parts):
    return np.concatenate([p[0] for p in parts]), np.concatenate([p[1] * p[2] for p in parts])


def binary(d):
    return np.array([-d / 2, d / 2]), np.array([0.5, 0.5])


def jit_binary(d, s1):
    if s1 == 0:
        return binary(d)
    return mix((*gpts(-d / 2, s1), 0.5), (*gpts(d / 2, s1), 0.5))


def rho1d(mu, nmax=NM, centre=0.0):
    A = amps((mu[0] - centre) / 2, nmax)
    return (A * mu[1][:, None]).T @ A


def di1d(mu):
    return sum(w * np.exp(-(XG - x) ** 2 / 2) / np.sqrt(2 * np.pi) for x, w in zip(*mu))


def bc_cont(p, q):
    return float(np.trapezoid(np.sqrt(p * q), XG))


def bc_disc(p, q):
    p, q = np.clip(p, 0, None), np.clip(q, 0, None)
    return float(np.sum(np.sqrt(p * q)))


def gauss_bc(v1, v2):                      # BC between centred normals of variances v1, v2
    return float(np.sqrt(2 * np.sqrt(v1 * v2) / (v1 + v2)))


def mpm(M):
    return mp.matrix(np.asarray(M, float).tolist())


def fid_mp(r0, r1):
    E, Q = mp.eigsy(mpm(r0))
    n = len(E)
    S = Q * mp.diag([mp.sqrt(max(E[i], 0)) for i in range(n)]) * Q.T
    E2, _ = mp.eigsy(S * mpm(r1) * S)
    return sum(mp.sqrt(max(E2[i], 0)) for i in range(n))


def pops(r):
    return np.clip(np.diag(r), 0, None)


def null_rows(d, nmax=NM):
    """Rows of the 1D nulling basis: rotate span{0,2} onto the binary's even mode."""
    B = np.eye(nmax + 1)
    e = np.linalg.eigh(rho1d(binary(d), nmax))[1][:, -1]
    e02 = np.array([e[0], e[2]]) / np.hypot(e[0], e[2])
    B[0, [0, 2]] = e02
    B[2, [0, 2]] = [-e02[1], e02[0]]
    return B


def probs(r, B):
    return np.clip(np.einsum("in,nm,im->i", B, r, B), 0, None)


def opt1(f, lo, hi):
    r = minimize_scalar(f, bounds=(lo, hi), method="bounded", options={"xatol": 1e-9})
    return float(r.fun), float(r.x)


def opt_robust(f, lo, hi, n=41):
    """Grid search then bounded refinement around the best grid point (guards against local minima)."""
    us = np.linspace(lo, hi, n)
    vals = [f(u) for u in us]
    i = int(np.argmin(vals))
    a, b = us[max(i - 1, 0)], us[min(i + 1, n - 1)]
    r = minimize_scalar(f, bounds=(a, b), method="bounded", options={"xatol": 1e-10})
    return (float(r.fun), float(r.x)) if r.fun <= vals[i] else (float(vals[i]), float(us[i]))


def gh(n):
    """Proper n-point Gauss-Hermite rule for a standard normal: nodes, weights (sum 1)."""
    x, w = roots_hermite(n)
    return np.sqrt(2) * x, w / np.sqrt(np.pi)


def slope(x, y):
    return float(np.polyfit(np.log(x), np.log(y), 1)[0])


def local_slopes(x, y):
    return list(map(float, np.gradient(np.log(y), np.log(x))))


# ----------------------------------------------------------------- X1: 2D
def x1():
    out = {"meta": run_metadata()}
    # P1a/P1b: Gaussian spread on H0 only, variance ratio rho (rho = 1 isotropic)
    for rho in (1.0, 0.1, 0.01, 1e-3, 1e-4):
        rec = {"a0": list(map(float, A0S)), "Q": [], "DI": [], "TRI": [], "HG": [], "NULL": [], "pred_Q": []}
        for a0 in A0S:
            d = 4 * a0
            pts, w = binary(d)
            r1 = rho1d((pts, w))
            P1 = pops(r1)
            B = null_rows(d)
            N1 = probs(r1, B)
            p1x = di1d((pts, w))

            def parts(u):
                sx = u * d / 2
                sy2 = rho * sx * sx
                tau_y = sy2 / 4
                r0x = rho1d(gpts(0.0, sx))
                py0 = 1.0 / np.sqrt(1 + 2 * tau_y)          # <0|rho0y|0>
                py1 = py0 * tau_y / (1 + 2 * tau_y)          # <1|rho0y|1>
                return sx, sy2, r0x, py0, py1

            def q(u):
                sx, _, _, py0, _ = parts(u)
                ox = one_minus_F(list(pts), list(w), "gauss", (0.0, sx))
                return 1 - (1 - ox) * py0 ** 0.5

            def di(u):
                sx, sy2, *_ = parts(u)
                v = 1 + sx * sx
                return 1 - bc_cont(p1x, np.exp(-XG ** 2 / (2 * v)) / np.sqrt(2 * np.pi * v)) * gauss_bc(1.0, 1.0 + sy2)

            def tri(u):
                _, _, r0x, py0, py1 = parts(u)
                px = pops(r0x)
                p0 = np.array([px[0] * py0, px[1] * py0, px[0] * py1])
                p1 = np.array([P1[0], P1[1], 0.0])
                return 1 - bc_disc(np.append(p1, 1 - p1.sum()), np.append(p0, 1 - p0.sum()))

            def hg(u):
                _, _, r0x, py0, _ = parts(u)
                return 1 - bc_disc(P1, pops(r0x)) * py0 ** 0.5

            def nul(u):
                _, _, r0x, py0, _ = parts(u)
                return 1 - bc_disc(N1, probs(r0x, B)) * py0 ** 0.5

            for k, f in (("Q", q), ("DI", di), ("TRI", tri), ("HG", hg), ("NULL", nul)):
                rec[k].append(opt1(f, 0.05, 1.5)[0])
            rec["pred_Q"].append(float(rho * a0 ** 2 / (2 * (1 + rho)) + 0.5 * a0 ** 4))
        rec["slopes"] = {k: slope(A0S, rec[k]) for k in ("Q", "DI", "TRI", "HG", "NULL")}
        rec["TRI_over_Q"] = [t / q_ for t, q_ in zip(rec["TRI"], rec["Q"])]
        rec["Q_over_pred"] = [q_ / p for q_, p in zip(rec["Q"], rec["pred_Q"])]
        out[f"gauss_rho{rho}"] = rec
        print("X1 rho", rho, {k: round(v, 2) for k, v in rec["slopes"].items()},
              "Q/pred", [round(v, 3) for v in rec["Q_over_pred"][::4]], "TRI/Q", round(rec["TRI_over_Q"][0], 3),
              flush=True)
    # P1c: isotropic uniform disc (non-separable): quantum via the closed form (2D quadrature)
    r_nodes = np.sqrt(0.5 * (GL_X + 1))
    th = 2 * np.pi * np.arange(64) / 64
    RR, TT = np.meshgrid(r_nodes, th, indexing="ij")
    WW = np.repeat((0.5 * GL_W)[:, None], 64, axis=1) / 64
    dx, dy, dw = (RR * np.cos(TT)).ravel(), (RR * np.sin(TT)).ravel(), WW.ravel()
    rec = {"a0": list(map(float, A0S)), "Q": [], "TRI": []}
    for a0 in A0S:
        d = 4 * a0
        P1 = pops(rho1d(binary(d), 4))

        def disc(Rd):
            return Rd * dx / 2, Rd * dy / 2

        def q(u):
            ax, ay = disc(u * d / np.sqrt(2))                # matches E[x^2] = R^2/4 = d^2/8 at u=1
            e = np.exp(-ax ** 2 - ay ** 2)
            C = np.sum(dw * e * np.cosh(a0 * ax) ** 2)
            S = np.sum(dw * e * np.sinh(a0 * ax) ** 2)
            return 1 - np.exp(-a0 ** 2 / 2) * (np.sqrt(C) + np.sqrt(S))

        def tri(u):
            ax, ay = disc(u * d / np.sqrt(2))
            Ax, Ay = amps(ax, 2), amps(ay, 2)
            p0 = np.array([np.sum(dw * (Ax[:, 0] * Ay[:, 0]) ** 2), np.sum(dw * (Ax[:, 1] * Ay[:, 0]) ** 2),
                           np.sum(dw * (Ax[:, 0] * Ay[:, 1]) ** 2)])
            p1 = np.array([P1[0], P1[1], 0.0])
            return 1 - bc_disc(np.append(p1, 1 - p1.sum()), np.append(p0, 1 - p0.sum()))

        rec["Q"].append(opt1(q, 0.05, 2.0)[0])
        rec["TRI"].append(opt1(tri, 0.05, 2.0)[0])
    rec["slopes"] = {k: slope(A0S, rec[k]) for k in ("Q", "TRI")}
    rec["Q_over_0.25a0^2"] = [q_ / (0.25 * a ** 2) for q_, a in zip(rec["Q"], A0S)]
    out["disc_iso"] = rec
    print("X1 disc", rec["slopes"], "Q/(0.25a0^2)", [round(v, 3) for v in rec["Q_over_0.25a0^2"][::4]], flush=True)
    # P1d: instrumental isotropic jitter on BOTH (H1 jitter s1 fixed; H0 width free)
    for s1 in (0.05, 0.1, 0.2, 0.4):
        rec = {"a0": list(map(float, A0S)), "Q": []}
        for a0 in A0S:
            d = 4 * a0
            r1x = rho1d(jit_binary(d, s1))
            r1y = rho1d(gpts(0.0, s1))

            def q(u):
                s0 = np.sqrt(s1 ** 2 + (u * d / 2) ** 2)
                r0 = rho1d(gpts(0.0, s0))
                return float(1 - fid_mp(r0, r1x) * fid_mp(r0, r1y))

            rec["Q"].append(opt1(q, 0.05, 2.0)[0])
        rec["local_slope_Q"] = local_slopes(A0S, rec["Q"])
        out[f"both_iso_s1{s1}"] = rec
        print("X1 both-iso s1", s1, "local slope (a0=0.02 .. 0.1):", [round(v, 2) for v in rec["local_slope_Q"][::2]],
              flush=True)
    # P1e: 1D line-like jitter on BOTH
    for s1 in (0.0, 0.05, 0.1, 0.2):
        rec = {"a0": list(map(float, A0S)), "Q": [], "DI": []}
        for a0 in A0S:
            d = 4 * a0
            mu1 = jit_binary(d, s1)
            r1 = rho1d(mu1)
            p1 = di1d(mu1)

            def q(u):
                s0 = np.sqrt(s1 ** 2 + (u * d / 2) ** 2)
                return float(1 - fid_mp(rho1d(gpts(0.0, s0)), r1))

            def di(u):
                v = 1 + s1 ** 2 + (u * d / 2) ** 2
                return 1 - bc_cont(p1, np.exp(-XG ** 2 / (2 * v)) / np.sqrt(2 * np.pi * v))

            rec["Q"].append(opt1(q, 0.3, 1.7)[0])
            rec["DI"].append(opt1(di, 0.3, 1.7)[0])
        rec["local_slope_Q"] = local_slopes(A0S, rec["Q"])
        rec["local_slope_DI"] = local_slopes(A0S, rec["DI"])
        out[f"both_line_s1{s1}"] = rec
        print("X1 both-line s1", s1, "slopes Q", [round(v, 2) for v in rec["local_slope_Q"][::2]],
              "DI", [round(v, 2) for v in rec["local_slope_DI"][::2]], flush=True)
    return out


# ----------------------------------------------------------------- X2: matched-covariance 2D scenes
def x2():
    out = {"meta": run_metadata()}
    n2 = 6                                                    # per-axis truncation for 2D HG
    r_nodes = np.sqrt(0.5 * (GL_X + 1))
    th = 2 * np.pi * np.arange(48) / 48
    RR, TT = np.meshgrid(r_nodes, th, indexing="ij")
    WW = np.repeat((0.5 * GL_W)[:, None], 48, axis=1) / 48
    ux, uy, uw = (RR * np.cos(TT)).ravel(), (RR * np.sin(TT)).ravel(), WW.ravel()
    g1x, g1w = gh(30)
    gx, gy = np.meshgrid(g1x, g1x, indexing="ij")
    gw = np.outer(g1w, g1w).ravel()
    gx, gy = gx.ravel(), gy.ravel()
    grid = np.linspace(-7, 7, 181)
    GX, GY = np.meshgrid(grid, grid, indexing="ij")
    dA = (grid[1] - grid[0]) ** 2

    def rho2(px, py, w):
        Ax, Ay = amps(px / 2, n2), amps(py / 2, n2)
        A = (Ax[:, :, None] * Ay[:, None, :]).reshape(len(px), -1)
        return (A * w[:, None]).T @ A

    def di2(px, py, w):
        p = np.zeros_like(GX)
        for x, y, ww in zip(px, py, w):
            p += ww * np.exp(-((GX - x) ** 2 + (GY - y) ** 2) / 2) / (2 * np.pi)
        return p

    def ov(xi, yi, xj, yj, px, py, w):
        mx, my = (xi + xj) / 2, (yi + yj) / 2
        pre = np.exp(-((xi - xj) ** 2 + (yi - yj) ** 2) / 16)
        return pre * np.sum(w * np.exp(-((px - mx) ** 2 + (py - my) ** 2) / 4))

    scenes = {"square": lambda r: (np.array([r, -r, 0.0, 0.0]), np.array([0.0, 0.0, r, -r])),
              "triangle": lambda r: (r * np.cos(2 * np.pi * np.arange(3) / 3), r * np.sin(2 * np.pi * np.arange(3) / 3))}
    for sname, sc in scenes.items():
        for fam in ("gauss", "disc"):
            rec = {"a0": list(map(float, A0S)), "Q": [], "DI": [], "HG": [], "SUPP": []}
            for a0 in A0S:
                r = 2 * a0
                hx, hy = sc(r)
                M = len(hx)
                hw = np.full(M, 1.0 / M)
                r1 = rho2(hx, hy, hw)
                P1 = pops(r1)
                Bs = np.linalg.eigh(r1)[1].T                   # support-projection ports = eigenbasis of rho1
                S1 = probs(r1, Bs)
                p1 = di2(hx, hy, hw)
                m2 = r * r / 2                                # E[x^2] of the scene

                def spread(u):
                    if fam == "gauss":
                        s = u * np.sqrt(m2)
                        return gx * s, gy * s, gw
                    R = u * 2 * np.sqrt(m2)                   # disc: E[x^2] = R^2/4
                    return ux * R, uy * R, uw

                def q(u, hx=hx, hy=hy, M=M, m2=m2):
                    """Exact overlaps in mpmath (1-F depends on square roots of ~1e-15 eigenvalues at small a0)."""
                    G = mp.matrix(M, M)
                    for i in range(M):
                        for j in range(M):
                            mx = mp.mpf(hx[i] + hx[j]) / 2
                            my = mp.mpf(hy[i] + hy[j]) / 2
                            mm = mp.sqrt(mx * mx + my * my)
                            pre = mp.e ** (-((mp.mpf(hx[i]) - hx[j]) ** 2 + (mp.mpf(hy[i]) - hy[j]) ** 2) / 16)
                            if fam == "gauss":
                                s2 = mp.mpf(u) ** 2 * m2
                                e = (1 + s2 / 2) ** -1 * mp.e ** (-(mm * mm) / (4 + 2 * s2))
                            else:
                                R = mp.mpf(u) * 2 * mp.sqrt(m2)
                                e = 2 / R ** 2 * mp.quad(lambda rr: rr * mp.e ** (-(rr * rr + mm * mm) / 4)
                                                         * mp.besseli(0, rr * mm / 2), [0, R])
                            G[i, j] = pre * e / M
                    E, _ = mp.eigsy(G)
                    return float(1 - sum(mp.sqrt(max(E[k], 0)) for k in range(M)))

                def hg(u):
                    return 1 - bc_disc(P1, pops(rho2(*spread(u))))

                def supp(u):
                    return 1 - bc_disc(S1, probs(rho2(*spread(u)), Bs))

                def di(u):
                    return float(1 - np.sum(np.sqrt(di2(*spread(u)) * p1)) * dA)

                rec["Q"].append(opt_robust(q, 0.3, 1.7)[0])
                rec["HG"].append(opt_robust(hg, 0.3, 1.7)[0])
                rec["SUPP"].append(opt_robust(supp, 0.3, 1.7)[0])
                rec["DI"].append(opt_robust(di, 0.3, 1.7, 21)[0] if a0 >= 0.04 else float("nan"))
            ok = ~np.isnan(np.array(rec["DI"], float))
            rec["slopes"] = {k: slope(A0S, rec[k]) for k in ("Q", "HG", "SUPP")}
            rec["slopes"]["DI(a0>=0.04)"] = slope(A0S[ok], np.array(rec["DI"], float)[ok])
            rec["SUPP_over_Q"] = [s / q_ for s, q_ in zip(rec["SUPP"], rec["Q"])]
            out[f"{sname}|{fam}"] = rec
            print("X2", sname, fam, {k: round(v, 2) for k, v in rec["slopes"].items()},
                  "SUPP/Q@0.02", round(rec["SUPP_over_Q"][0], 3), flush=True)
    return out


# ----------------------------------------------------------------- X3: spectral line shapes (1D)
def x3():
    out = {"meta": run_metadata()}
    t_nodes, t_w = roots_legendre(400)

    def family(kind, par):
        """Symmetric spread on [-W, W] as quadrature, rescaled to unit second moment; returns pts, w, kurtosis."""
        W = 12.0 if kind == "t" else 6.0 * (1 + par)
        x = W * t_nodes
        if kind == "t":
            dens = (1 + x * x / par) ** (-(par + 1) / 2)
        else:                                        # Voigt: Gaussian (sd 1) * Lorentz (HWHM gamma = par), truncated
            g = np.exp(-x ** 2 / 2)
            dens = np.array([np.sum(g * par / np.pi / ((xx - x) ** 2 + par ** 2) * W * t_w) for xx in x])
        w = dens * W * t_w
        w = w / w.sum()
        x = x / np.sqrt(np.sum(w * x * x))
        return x, w, float(np.sum(w * x ** 4))

    cases = [("t", 30), ("t", 10), ("t", 6), ("t", 5), ("voigt", 0.1), ("voigt", 0.3), ("voigt", 1.0)]
    for kind, par in cases:
        xs, ws, K = family(kind, par)
        rec = {"a0": list(map(float, A0S)), "K_eff": K, "Q": [], "HG": [], "NULL": [], "DI": []}
        for a0 in A0S:
            d = 4 * a0
            pts, w = binary(d)
            r1 = rho1d((pts, w))
            P1 = pops(r1)
            B = null_rows(d)
            N1 = probs(r1, B)
            p1 = di1d((pts, w))

            def mu0(u):
                return xs * u * d / 2, ws

            def q(u):
                p, ww = mu0(u)
                a = p / 2
                C = np.sum(ww * np.exp(-a * a) * np.cosh(a * a0) ** 2)
                S = np.sum(ww * np.exp(-a * a) * np.sinh(a * a0) ** 2)
                return float(1 - np.exp(-a0 ** 2 / 2) * (np.sqrt(C) + np.sqrt(S)))

            rec["Q"].append(opt1(q, 0.5, 1.5)[0])
            rec["HG"].append(opt1(lambda u: 1 - bc_disc(P1, pops(rho1d(mu0(u)))), 0.5, 1.5)[0])
            rec["NULL"].append(opt1(lambda u: 1 - bc_disc(N1, probs(rho1d(mu0(u)), B)), 0.5, 1.5)[0])
            rec["DI"].append(opt1(lambda u: 1 - bc_cont(p1, di1d(mu0(u))), 0.5, 1.5)[0])
        rec["slopes"] = {k: slope(A0S, rec[k]) for k in ("Q", "HG", "NULL", "DI")}
        rec["Q_over_formula@0.02"] = rec["Q"][0] / ((K - 1) * A0S[0] ** 4 / 4)
        rec["HG_over_formula@0.02"] = rec["HG"][0] / ((np.sqrt(K) - 1) ** 2 * A0S[0] ** 4 / 4)
        rec["HG_over_Q@0.02"] = rec["HG"][0] / rec["Q"][0]
        out[f"{kind}{par}"] = rec
        print("X3", kind, par, "K", round(K, 2), {k: round(v, 2) for k, v in rec["slopes"].items()},
              "Q/formula", round(rec["Q_over_formula@0.02"], 3), "HG/formula", round(rec["HG_over_formula@0.02"], 3),
              "HG/Q", round(rec["HG_over_Q@0.02"], 3), flush=True)
    return out


# ----------------------------------------------------------------- X4: QCB vs single-copy
def _qcb_terms(r0, r1):
    E0, Q0 = mp.eigsy(mpm(r0))
    E1, Q1 = mp.eigsy(mpm(r1))
    n = len(E0)
    O = Q0.T * Q1
    tol = mp.mpf("1e-14")                                   # eigenvalues below this are exact zeros (rank)
    e0 = [E0[i] if E0[i] > tol else mp.mpf(0) for i in range(n)]
    e1 = [E1[j] if E1[j] > tol else mp.mpf(0) for j in range(n)]
    terms = [(e0[i], e1[j], O[i, j] ** 2) for i in range(n) for j in range(n) if e0[i] > 0 and e1[j] > 0]
    return terms, Q0, e0


def _min_over_s(tr):
    """min over s in [0, 1] of tr(s), including the endpoints (support limits)."""
    r = minimize_scalar(lambda s: float(tr(s)), bounds=(0.0, 1.0), method="bounded", options={"xatol": 1e-9})
    cands = [(float(tr(r.x)), r.x), (float(tr(0.0)), 0.0), (float(tr(1.0)), 1.0)]
    return min(cands)[1]


def qcb_mp(r0, r1):
    terms, _, _ = _qcb_terms(r0, r1)

    def tr(s):
        s = mp.mpf(s)
        return sum(a ** s * b ** (1 - s) * c for a, b, c in terms)

    return float(-mp.log(tr(_min_over_s(tr))))


def cchern(p, q, tol=1e-25):
    p, q = np.asarray(p, float), np.asarray(q, float)
    p, q = np.where(p > tol, p, 0.0), np.where(q > tol, q, 0.0)
    both = (p > 0) & (q > 0)

    def tr(s):
        return float(np.sum(p[both] ** s * q[both] ** (1 - s)))

    return float(-np.log(tr(_min_over_s(tr))))


def x4():
    out = {"meta": run_metadata()}
    nm = 12
    a0s = [0.02, 0.035, 0.05]
    rec = {"a0": a0s, "QCB": [], "NULL": [], "HG": []}
    for a0 in a0s:
        d = 4 * a0
        r1 = rho1d(binary(d), nm)
        B = null_rows(d, nm)
        N1, P1 = probs(r1, B), pops(r1)

        def r0(u, d=d):
            return rho1d(gpts(0.0, u * d / 2), nm)

        rec["QCB"].append(opt_robust(lambda u: qcb_mp(r0(u), r1), 0.6, 1.4, 21)[0])
        rec["NULL"].append(opt_robust(lambda u: cchern(N1, probs(r0(u), B)), 0.6, 1.4)[0])
        rec["HG"].append(opt_robust(lambda u: cchern(P1, pops(r0(u))), 0.6, 1.4)[0])
    rec["NULL_over_QCB"] = [a / b for a, b in zip(rec["NULL"], rec["QCB"])]
    rec["HG_over_QCB"] = [a / b for a, b in zip(rec["HG"], rec["QCB"])]
    out["1D_HS2"] = rec
    print("X4 1D H-S2 NULL/QCB", [round(v, 3) for v in rec["NULL_over_QCB"]], "HG/QCB",
          [round(v, 3) for v in rec["HG_over_QCB"]], flush=True)
    rec = {"a0": a0s, "QCB": [], "TRI": []}
    for a0 in a0s:
        d = 4 * a0
        r1x = rho1d(binary(d), nm)
        P1 = pops(r1x)

        def qcb2(u, d=d, r1x=r1x):
            r0 = rho1d(gpts(0.0, u * d / 2), nm)
            terms, Q0, e0 = _qcb_terms(r0, r1x)
            n = nm + 1

            def tr(s):
                s = mp.mpf(s)
                tx = sum(a ** s * b ** (1 - s) * c for a, b, c in terms)
                ty = sum(e0[i] ** s * Q0[0, i] ** 2 for i in range(n) if e0[i] > 0)   # <0|rho0y^s|0>
                return tx * ty

            return float(-mp.log(tr(_min_over_s(tr))))

        def tri(u, d=d, P1=P1):
            px = pops(rho1d(gpts(0.0, u * d / 2), nm))
            p0 = np.array([px[0] * px[0], px[1] * px[0], px[0] * px[1]])   # isotropic: y pops = x pops
            p1 = np.array([P1[0], P1[1], 0.0])
            return cchern(np.append(p1, 1 - p1.sum()), np.append(p0, 1 - p0.sum()))

        rec["QCB"].append(opt_robust(qcb2, 0.1, 1.5, 21)[0])
        rec["TRI"].append(opt_robust(tri, 0.1, 1.5)[0])
    rec["TRI_over_QCB"] = [a / b for a, b in zip(rec["TRI"], rec["QCB"])]
    out["2D_iso"] = rec
    print("X4 2D iso TRI/QCB", [round(v, 3) for v in rec["TRI_over_QCB"]], flush=True)
    eps, a0 = 0.03, 0.05
    d = 4 * a0
    cen = eps * d
    r1 = rho1d((np.array([0.0, d]), np.array([1 - eps, eps])), nm, cen)
    m2 = eps * (1 - eps) * d * d

    def r0v(v):
        return rho1d(gpts(cen + v[0] * np.sqrt(m2), np.sqrt(m2) * abs(v[1])), nm, cen)

    best = min((minimize(lambda v: qcb_mp(r0v(v), r1), x0, method="Nelder-Mead",
                         options={"xatol": 1e-4, "fatol": 1e-14, "maxiter": 200}) for x0 in ([0, 1], [0.3, 0.8])),
               key=lambda r: r.fun)
    R0 = r0v(best.x)
    k = 6
    iu = np.triu_indices(k, 1)

    def basis_from(theta):
        A = np.zeros((k, k))
        A[iu] = theta
        B = np.eye(nm + 1)
        B[:k, :k] = expm(A - A.T)
        return B

    def neg(theta):
        B = basis_from(theta)
        return -cchern(probs(r1, B), probs(R0, B))

    rng = np.random.default_rng(7)
    starts = [np.zeros(len(iu[0]))] + [rng.normal(scale=0.3, size=len(iu[0])) for _ in range(6)]
    opt = max(-minimize(neg, x0, method="Nelder-Mead", options={"maxiter": 6000, "xatol": 1e-8, "fatol": 1e-16}).fun
              for x0 in starts)
    hgv = cchern(pops(r1), pops(R0))
    out["companion"] = {"eps": eps, "a0": a0, "nuisance_v": list(map(float, best.x)), "QCB": float(best.fun),
                        "optimised_single_copy": opt, "HG": hgv, "ratio_opt_over_QCB": opt / float(best.fun),
                        "ratio_HG_over_QCB": hgv / float(best.fun)}
    print("X4 companion", {k_: (round(v, 4) if isinstance(v, float) else v) for k_, v in out["companion"].items()},
          flush=True)
    return out


# ----------------------------------------------------------------- X5: two photons, common-mode slow jitter
def x5():
    out = {"meta": run_metadata()}
    nm = 14
    m = nm + 1
    SW = np.zeros((m * m, m * m))
    for i in range(m):
        for j in range(m):
            SW[i * m + j, j * m + i] = 1.0
    PA = (np.eye(m * m) - SW) / 2
    gxn, gwn = gh(20)                                                     # common jitter (proper rule)
    dxn, dwn = gh(8)                                                      # differential jitter (proper rule)
    grid = np.linspace(-7, 7, 141)
    G1, G2 = np.meshgrid(grid, grid, indexing="ij")
    dA = (grid[1] - grid[0]) ** 2

    def photon_rho(h, d, y):
        if h == 0:
            v = amps(y / 2, nm)[0]
            return np.outer(v, v)
        a = amps(np.array([(y - d / 2) / 2, (y + d / 2) / 2]), nm)
        return 0.5 * (np.outer(a[0], a[0]) + np.outer(a[1], a[1]))

    def pair_state(h, d, sj, sd, U, M1):
        R = np.zeros((m * m, m * m))
        xs = [(0.0, 1.0)] if sj == 0 else list(zip(gxn * sj, gwn))
        ds = [(0.0, 1.0)] if sd == 0 else list(zip(dxn * sd, dwn))
        for X, wx in xs:
            for d1, w1 in ds:
                r1 = M1 @ U @ photon_rho(h, d, X + d1) @ U.T @ M1.T
                for d2, w2 in ds:
                    r2 = U @ photon_rho(h, d, X + d2) @ U.T
                    R += wx * w1 * w2 * np.kron(r1, r2)
        return R

    def di_pair(h, d, sj):
        p = np.zeros_like(G1)
        xs = [(0.0, 1.0)] if sj == 0 else list(zip(gxn * sj, gwn))
        for X, wx in xs:
            if h == 0:
                f1, f2 = np.exp(-(G1 - X) ** 2 / 2), np.exp(-(G2 - X) ** 2 / 2)
            else:
                f1 = 0.5 * (np.exp(-(G1 - X - d / 2) ** 2 / 2) + np.exp(-(G1 - X + d / 2) ** 2 / 2))
                f2 = 0.5 * (np.exp(-(G2 - X - d / 2) ** 2 / 2) + np.exp(-(G2 - X + d / 2) ** 2 / 2))
            p += wx * f1 * f2 / (2 * np.pi)
        return p

    def local_pair(R, B):
        W = np.einsum("ia,jb->ijab", B, B).reshape(m * m, m * m)          # rows: port pairs (i, j)
        return np.clip(np.einsum("pa,ab,pb->p", W, R, W), 0, None)

    def fid(R0, R1):
        w, v = np.linalg.eigh(R0)
        S = (v * np.sqrt(np.clip(w, 0, None))) @ v.T
        e = np.linalg.eigvalsh(S @ R1 @ S)
        return float(np.sum(np.sqrt(np.clip(e, 0, None))))

    I = np.eye(m)
    A = np.triu(np.random.default_rng(1000).normal(size=(m, m)), 1)
    U_x = expm(0.03 * (A - A.T))
    A2 = np.triu(np.random.default_rng(2000).normal(size=(m, m)), 1)

    def evaluate(d, sj, sd=0.0, U=I, M1=I):
        R0, R1 = pair_state(0, d, sj, sd, U, M1), pair_state(1, d, sj, sd, U, M1)
        pa0, pa1 = float(np.trace(PA @ R0)), float(np.trace(PA @ R1))
        bc = np.sqrt(max(1 - pa0, 0) * max(1 - pa1, 0)) + np.sqrt(max(pa0, 0) * max(pa1, 0))
        res = {"Panti_H0": pa0, "Panti_H1": pa1, "HOM": float(-np.log(bc)), "Q_pair": float(-np.log(fid(R0, R1)))}
        for name, B in (("SPADE_pair", I), ("NULL_pair", null_rows(d, nm))):
            res[name] = float(-np.log(bc_disc(local_pair(R0, B), local_pair(R1, B))))
        p0, p1 = di_pair(0, d, sj), di_pair(1, d, sj)
        res["DI_pair"] = float(-np.log(float(np.sum(np.sqrt(p0 * p1)) * dA)))
        return res

    chk = {}
    for d in (0.1, 0.2, 0.4):
        for sj in (0.0, 0.2):
            for tag, U in (("noXT", I), ("XT", U_x)):
                r = evaluate(d, sj, 0.0, U)
                chk[f"d{d}|sj{sj}|{tag}"] = {"Panti_H0": r["Panti_H0"], "Panti_H1": r["Panti_H1"],
                                             "pred_H1": (1 - np.exp(-d * d / 4)) / 4}
    for sd in (0.01, 0.03, 0.1):
        r = evaluate(0.2, 0.0, sd)
        chk[f"sdelta{sd}"] = {"Panti_H0": r["Panti_H0"], "pred": (1 - (1 + sd * sd) ** -0.5) / 2}
    for eps in (0.01, 0.03, 0.1):
        r = evaluate(0.2, 0.1, 0.0, I, expm(eps * (A2 - A2.T)))
        chk[f"memory{eps}"] = {"Panti_H0": r["Panti_H0"], "c_fit": r["Panti_H0"] / eps ** 2}
    out["checks"] = chk
    print("X5 checks", {k: {kk: f"{vv:.3e}" for kk, vv in v.items()} for k, v in chk.items()}, flush=True)
    sjs = [0.0, 0.02, 0.05, 0.1, 0.2, 0.4, 0.8]
    for d in (0.1, 0.2, 0.4):
        rows = {sj: evaluate(d, sj) for sj in sjs}
        rec = {"sj": sjs}
        for k in ("HOM", "SPADE_pair", "NULL_pair", "DI_pair", "Q_pair"):
            rec[k + "_per_photon"] = [rows[s][k] / 2 for s in sjs]
        best_local = [max(rows[s]["SPADE_pair"], rows[s]["NULL_pair"], rows[s]["DI_pair"]) / 2 for s in sjs]
        rec["best_local_per_photon"] = best_local
        rec["HOM_over_best_local"] = [h / b for h, b in zip(rec["HOM_per_photon"], best_local)]
        rec["Q_over_HOM"] = [q / h for q, h in zip(rec["Q_pair_per_photon"], rec["HOM_per_photon"])]
        out[f"jitter_d{d}"] = rec
        print("X5 d", d, "HOM/best_local", [round(v, 2) for v in rec["HOM_over_best_local"]],
              "Q/HOM", [round(v, 2) for v in rec["Q_over_HOM"]], flush=True)
    d, sj = 0.2, 0.4
    B = null_rows(d, nm)
    xs = list(zip(gxn * sj, gwn))

    def port_probs(h, X):
        p = probs(photon_rho(h, d, X), B)[:6]
        return np.append(p, max(1 - p.sum(), 1e-300))

    PX = {h: np.array([port_probs(h, X) for X, _ in xs]) for h in (0, 1)}
    WX = np.array([w for _, w in xs])
    frames = {}
    for kph in (2, 4, 8):
        bc = 0.0
        for combo in combinations_with_replacement(range(7), kph):
            n = np.bincount(combo, minlength=7)
            coef = factorial(kph) / np.prod([factorial(int(c)) for c in n])
            pr = [coef * float(np.sum(WX * np.prod(PX[h] ** n, axis=1))) for h in (0, 1)]
            bc += np.sqrt(pr[0] * pr[1])
        frames[kph] = float(-np.log(bc) / kph)
    hom_pp = evaluate(d, sj)["HOM"] / 2
    out["frames_d0.2_sj0.4"] = {"null_frame_per_photon": frames, "HOM_per_photon": hom_pp}
    print("X5 frames", frames, "HOM per photon", hom_pp, flush=True)
    return out


def main() -> None:
    which = sys.argv[1:] or ["X1", "X4", "X5", "X3", "X2"]
    fns = {"X1": x1, "X2": x2, "X3": x3, "X4": x4, "X5": x5}
    for w in which:
        t = time.time()
        res = fns[w]()
        res["runtime_s"] = time.time() - t
        dump_json(res, os.path.join(results_dir("x_suite"), f"{w}.json"))
        print(f"{w} done in {time.time() - t:.0f} s", flush=True)


if __name__ == "__main__":
    main()
