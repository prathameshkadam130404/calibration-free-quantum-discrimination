"""Generate Figures 1-3 of the calibration-free paper from the results JSON.

Run from the repository root:  python submission_v2/pra_calibration_free/gen_figures.py
Reads  results/qx3e/qx3e.json, results/qx3/qx3.json
Writes results/qx3/qx3_largen.json (exploratory large-n points, recomputed with the QX3 code)
       submission_v2/pra_calibration_free/figures/fig1_exponents.pdf, fig2_finite_n.pdf, fig3_single_photon.pdf
Palette: dataviz reference categorical slots 1-3 (validated: CVD dE 9.2, normal-vision dE 27.6; aqua carries
direct labels because its contrast is below 3:1). Colour follows the entity: measure-first = blue, coherent
references = orange, symmetric projection = aqua.
"""
from __future__ import annotations

import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
OUT = os.path.join(os.path.dirname(__file__), "figures")
BLUE, ORANGE, AQUA, INK, MUTED = "#2a78d6", "#eb6834", "#1baf7a", "#0b0b0b", "#52514e"
COL_W = 3.375                                # PRA single-column width (inches)
plt.rcParams.update({"font.size": 8, "font.family": "STIXGeneral", "mathtext.fontset": "stix",
                     "axes.linewidth": 0.6, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelcolor": INK, "ytick.labelcolor": INK,
                     "xtick.major.width": 0.6, "ytick.major.width": 0.6, "legend.frameon": False,
                     "legend.fontsize": 7, "lines.linewidth": 1.2, "savefig.bbox": "tight"})
K0_X = 0.03                                  # plotting position of kappa = 0 on the log axis


def load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return json.load(fh)


def grid(ax):
    ax.grid(True, which="major", color="#e4e3df", linewidth=0.5)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def fig1(qe):
    q = qe["quantum"]["0.1"]
    a2 = q["a0sq"]
    rows = qe["c_spade"]["0.1"]
    kap = np.array([r["kappa"] for r in rows], float)
    val = np.array([r["E_over_a0sq"] for r in rows])
    x = np.where(kap == 0, K0_X, kap)
    fig, ax = plt.subplots(figsize=(COL_W, 2.75))
    grid(ax)
    for k, ls in ((2, ":"), (4, "-."), (8, "--")):
        v = q["schur_k"][str(k)] / a2
        ax.axhline(v, color=AQUA, linestyle=ls, linewidth=1.0)
        ax.text(1.6e3, v + 0.012, f"$k={k}$", color=INK, fontsize=7, ha="right", va="bottom")
    vinf = q["schur_inf"] / a2
    ax.axhline(vinf, color=AQUA, linestyle="-", linewidth=1.2, label="symmetric projection, $k$ photons")
    ax.text(1.6e3, vinf - 0.015, r"$k\to\infty$", color=INK, fontsize=7, ha="right", va="top")
    ax.plot(x, val, "-o", color=BLUE, markersize=3.5, label="measure-first, mode sorting")
    lr = qe["c_learn"]["a00.1|k0"]["E_over_a0sq"]
    ax.plot([K0_X], [lr], "s", color=BLUE, markerfacecolor="white", markersize=4.5,
            label="measure-first, optimized")
    kr = np.array([1, 3, 10, 30, 100], float)
    ax.plot(kr, [q["qref"][str(int(k))] / a2 for k in kr], "-^", color=ORANGE, markersize=3.5,
            label="coherent references")
    ax.set_xscale("log")
    ax.set_xlim(0.02, 2e3)
    ax.set_ylim(0, 1.05)
    ax.set_xticks([K0_X, 0.1, 1, 10, 100, 1000])
    ax.set_xticklabels(["0", "0.1", "1", "10", "100", "1000"])
    ax.minorticks_off()
    ax.axvline(0.055, color="white", linewidth=4)            # visual break between kappa = 0 and the log axis
    ax.set_xlabel(r"calibration photons per target photon, $\kappa$")
    ax.set_ylabel(r"exponent / known-pointing limit $a_0^2$")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.01), ncol=2, handlelength=1.8, columnspacing=1.0,
              fontsize=6.5)
    fig.savefig(os.path.join(OUT, "fig1_exponents.pdf"))
    plt.close(fig)


def fig2(qe):
    fn = qe["finite_N"]
    q = qe["quantum"]["0.1"]
    lam_p = (1 + np.exp(-2 * 0.01)) / 2
    lam_m = 1 - lam_p
    fig, ax = plt.subplots(figsize=(COL_W, 2.3))
    grid(ax)
    for key, ls, lab in (("k1", "-", r"measure-first, $\kappa=1$"), ("k10", "--", r"measure-first, $\kappa=10$")):
        ax.plot(fn[key]["N"], fn[key]["P_err"], ls, marker="o", color=BLUE, markersize=3.5, label=lab)
    N = np.array(fn["k1"]["N"], float)

    def log_h(n, kk):                              # ln of the complete homogeneous polynomial h_kk(lam_p, lam_m)
        r = lam_m / lam_p
        return kk * np.log(lam_p) + np.log((1 - r ** (kk + 1)) / (1 - r))

    p4 = 0.5 * np.exp((N / 4) * log_h(N, 4))
    pall = np.array([0.5 * np.exp(log_h(n, int(n))) for n in N])
    ax.plot(N, p4, "-.", marker="^", color=AQUA, markersize=3.5, label="symmetric projection, groups of $k=4$")
    ax.plot(N, pall, "-", marker="^", color=AQUA, markersize=3.5, label="symmetric projection, all $N$ photons")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"target photons $N$ ($a_0=0.1$)")
    ax.set_ylabel(r"error probability")
    ax.set_xticks(N)
    ax.set_xticklabels([f"{int(v)}" for v in N])
    ax.minorticks_off()
    ax.legend(loc="lower left")
    assert abs(q["schur_k"]["4"] - (-log_h(4, 4) / 4)) < 1e-12        # same formula as the results file
    fig.savefig(os.path.join(OUT, "fig2_finite_n.pdf"))
    plt.close(fig)


def largen_points():
    path = os.path.join(ROOT, "results", "qx3", "qx3_largen.json")
    if os.path.exists(path):
        return load("results/qx3/qx3_largen.json")
    from research.space import qx3_learn_then_classify as qx3
    d, tau = 0.4, 0.2
    pk = qx3.bayes_jitter(0.0, d)
    rec = {"a0": 0.1, "tau": tau, "n": [], "ratio_MFDI_over_COH": [], "note": "exploratory, not pre-registered"}
    for n in (256, 512, 1024):
        pc = qx3.coh_error(n, tau, d, qx3.coh_K(n, tau))[0]
        em = qx3.bayes_jitter(np.sqrt(1 / (n + 1 / tau ** 2)), d) - pk
        rec["n"].append(n)
        rec["ratio_MFDI_over_COH"].append(em / (pc - pk))
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1)
    return rec


def fig3(q3):
    big = largen_points()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(COL_W, 4.2), sharex=False)
    for ax in (ax1, ax2):
        grid(ax)
    for tau, col, mk in (("0.2", BLUE, "o"), ("0.5", ORANGE, "s")):
        p = q3["points"][f"a00.1|tau{tau}"]
        n = np.array(p["n"][1:], float)
        r = np.array(p["E_MFDI"][1:]) / np.array(p["E_COH"][1:])
        ax1.plot(n, r, "-", marker=mk, color=col, markersize=3.5, label=rf"$\tau={tau}$")
    ax1.plot(big["n"], big["ratio_MFDI_over_COH"], "o", color=BLUE, markerfacecolor="white", markersize=4,
             label=r"$\tau=0.2$, exploratory")
    ax1.set_xscale("log")
    ax1.set_ylim(1.0, 1.22)
    ax1.set_ylabel("excess risk: measure-first / joint")
    ax1.set_xlabel(r"calibration photons $n$ ($a_0=0.1$)")
    ax1.legend(loc="lower right", ncol=1)
    ax1.text(0.02, 0.92, "(a)", transform=ax1.transAxes, color=INK)
    p = q3["points"]["a00.1|tau0.5"]
    n = np.array(p["n"][1:], float)
    for key, col, mk, lab in (("COH", AQUA, "^", "joint (coherent)"), ("MFDI", BLUE, "o", "measure-first, direct imaging"),
                              ("SPADE", ORANGE, "s", "measure-first, mode counting")):
        ax2.plot(n, p["recovered_" + key][1:], "-", marker=mk, color=col, markersize=3.5, label=lab)
    ax2.axhline(p["recovered_COH"][0], color=MUTED, linewidth=0.8, linestyle=":")
    ax2.text(130, p["recovered_COH"][0] - 0.003, "no calibration", color=INK, fontsize=7, va="top", ha="right")
    ax2.set_xscale("log")
    ax2.set_ylim(0.75, 1.0)
    ax2.set_ylabel("fraction of known-pointing advantage")
    ax2.set_xlabel(r"calibration photons $n$ ($a_0=0.1$, $\tau=0.5$)")
    ax2.legend(loc="lower left", bbox_to_anchor=(0.0, 1.02, 1.0, 0.2), mode="expand", ncol=2, fontsize=6.5)
    ax2.text(0.02, 0.92, "(b)", transform=ax2.transAxes, color=INK)
    fig.tight_layout(h_pad=1.0)
    fig.savefig(os.path.join(OUT, "fig3_single_photon.pdf"))
    plt.close(fig)


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    qe, q3 = load("results/qx3e/qx3e.json"), load("results/qx3/qx3.json")
    fig1(qe)
    fig2(qe)
    fig3(q3)
    print("figures written to", OUT)


if __name__ == "__main__":
    main()
