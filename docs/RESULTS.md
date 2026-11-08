# Results: quantum-limited classification of sub-diffraction scenes under unknown nuisances (2026-11-07)

Pre-registration: `research/space/PLAN_PREREG.md`, committed a4a713d before any computation; Addendum A was
added afterwards. Code: `research/space/s01_exponents.py` (exact per-photon quantities) and
`research/space/s02_photon_complexity.py` (finite-N learners). Data: `results/s01_exponents/exponents.json`
and `results/s02_photon_complexity/photon_complexity.json`. Logs are in `research/logs/`.

Model: 1D Gaussian PSF of width σ, weak incoherent light, a₀ = d/4σ.

## 1. Pre-registered outcomes

Exponents are the k in "photons needed ∝ a₀^−k"; fits over a₀ ∈ [0.02, 0.1].

| Hypothesis | Prediction | Measured | Verdict |
|---|---|---|---|
| H-S1 known point vs binary | DI 4, SPADE 2, Q 2 | DI 3.98, SPADE 2.00, Q 2.00 | confirmed (known result, sanity) |
| H-S2 Gaussian-jitter nuisance | DI 8, SPADE 4, Q 4 | DI 7.92, SPADE 3.99, Q 3.98 | confirmed |
| H-S3 uniform disc | DI 8, SPADE 4, Q 4 | DI 7.92, SPADE 4.00, Q 3.99 | confirmed |
| H-S3 semicircle disc | DI 8, SPADE 4, Q 4 | DI 7.92, SPADE 4.00, Q 3.99 | confirmed |
| H-S4 companion, separation (ε = 0.03) | DI 6, SPADE 4, Q 4 | DI 6.01, SPADE 4.00, SIGN₁₂ 3.99, Q 3.99 | confirmed |
| H-S4 companion, brightness ε ∈ [0.005, 0.05] (a₀ = 0.05) | DI 2, SPADE 1, Q 1 | DI 1.88, SPADE **0.59**, Q 0.94 | DI and Q confirmed; **SPADE refuted on the pre-registered window** (see §3) |
| H-S5 finite-N slope of log(N_DI/N_SPADE) vs log(σ/d) | ≈2 (point), ≈4 (jitter), ±1 | 1.93 (point), 3.70 (jitter) | confirmed |

DI = direct imaging (best detect-first learner); SPADE = Hermite–Gauss mode counting; Q = quantum optimum
(root fidelity, any measurement, collective included). In every row the nuisance is set to its least
favourable value separately for each receiver.

## 2. Exact results (equal binary vs a single source with an unknown symmetric spread)

**Proposition S1 (closed-form fidelity).** Let ρ₀ be a single source spread by any symmetric distribution of
positions, with a = X/2σ, and let ρ₁ be the equal binary. The root fidelity is exactly

F = e^{−a₀²/2} ( √E[e^{−a²} cosh²(a a₀)] + √E[e^{−a²} sinh²(a a₀)] ).

ρ₁ has rank 2, so F = tr √(V†ρ₀V) with a 2×2 matrix V†ρ₀V. Its entries are closed-form overlaps of shifted
PSFs, so no truncation of the Hilbert space is involved. Numerical check: s01 uses this exact 2×2 form.

**Proposition S2 (leading order; sympy series in `PLAN_PREREG.md` Addendum A).** Let K be the kurtosis of the
spread family and assume a finite sixth moment. Minimising over the unknown scale:

| Receiver | Per-photon distinguishability at leading order |
|---|---|
| Quantum optimum | 1 − F = (K − 1) a₀⁴ / 4 + O(a₀⁶); least favourable scale = matched second moment |
| HG-SPADE | H² = (√K − 1)² a₀⁴ / 4 |
| Direct imaging | H² = (4/3)(K − 1)² a₀⁸ (Edgeworth) |

Numerical checks at a₀ = 0.02 (s01):

| Case | Q measured / predicted | SPADE measured / predicted |
|---|---|---|
| Gaussian (K = 3) | 7.99e-8 / 8.00e-8 | 2.142e-8 / 2.144e-8 |
| Uniform (K = 1.8) | 3.199e-8 / 3.20e-8 | 4.668e-9 / 4.67e-9 |

**Consequences:**
- Photons needed scale as log(1/δ)/(1−F) or log(1/δ)/H². Hence N_DI/N_Q ≈ 48 σ⁴ / ((K−1) d⁴) with the
  nuisance, against ≈ 8 σ²/d² for a known point. At d = 0.1σ with Gaussian jitter that is about 2.4 × 10⁵,
  against about 800 without the nuisance.
- **HG-SPADE is not optimal under the nuisance.** It needs a factor (√K + 1)/(√K − 1) more photons than the
  optimum: 2 + √3 ≈ 3.73 for Gaussian jitter, 6.85 for a uniform disc. The factor diverges as K → 1, i.e. as
  the nuisance spread becomes two-point-like.
- **A binary-nulling measurement attains the optimum at leading order.** Rotate span{HG₀, HG₂} so that one
  port is the binary's own even mode. The orthogonal port is dark under H1 and has probability (K−1)τ²/2
  under H0. The finite-N learner (NULL-GLRT) uses 3.0–3.7× fewer photons than SPADE-GLRT under jitter (§4).
  With an unknown separation, the rotation angle can be set from the measured HG₁ rate (two-stage). This
  two-stage scheme is proposed, not simulated.

## 3. Faint companion (ε) vs single source with unknown centroid and jitter

- **Separation exponents:** DI 6, SPADE 4, Q 4, as predicted. The sign-sensitive ports (|1⟩ ± |2⟩) add only
  about 12 % over SPADE. Mixing |0⟩ with |1⟩ is useless (exponent 6), because the star swamps it.
- **Brightness exponent of SPADE (refuted prediction, now explained):**
  - The blurred single source also populates HG₂, at a rate 3ε relative to the companion. This gives
    H² ≈ ½ ε a_d⁴ (√½ − √(3ε/2))², with a_d = d/2σ. Predicted 9.6e-8 vs measured 9.4e-8 at ε = 0.005;
    4.7e-7 vs 3.6e-7 at ε = 0.05, where higher ports matter.
  - So the local ε-slope falls below 1 at moderate ε. On ε ∈ [10⁻⁴, 10⁻³] the measured slope is 0.97,
    so the asymptotic exponent is 1.
  - The pre-registered window, chosen too wide, therefore fails the criterion. The asymptotic claim stands
    only with this correction.
- **Quantum vs SPADE:** at ε = 0.03 the quantum optimum is 2.15× better than SPADE. Projecting onto the
  support of the companion hypothesis (the eigenbasis of ρ₁) reaches 73 % of the optimum, against 46 % for
  SPADE (e.g. 4.99e-7 / 6.80e-7 / 3.16e-7 at a₀ = 0.05). **The optimal measurement for this composite
  problem is still unknown** (open).

## 4. Finite-N learners (H-S5)

Photons needed for 90 % balanced accuracy; 300 trials per class per N.

| d/σ | DI-GLRT jitter | SPADE-GLRT jitter | NULL-GLRT jitter | SPADE-LR jitter | DI point | SPADE point |
|---|---|---|---|---|---|---|
| 0.2 | 4.1e9 | 1.0e6 | 3.1e5 | 1.1e6 | 1.4e5 | 707 |
| 0.3 | 1.7e8 | 2.2e5 | 6.0e4 | 1.8e5 | 2.4e4 | 297 |
| 0.4 | 2.2e7 | 6.2e4 | 2.1e4 | 5.8e4 | 1.0e4 | 166 |
| 0.6 | 8.4e5 | 1.4e4 | 4.2e3 | 1.3e4 | 1.7e3 | 72 |
| 0.8 | 1.1e5 | 4.4e3 | 1.3e3 | 3.5e3 | 576 | 45 |

- **Slopes in log(σ/d):** DI 7.62, SPADE 3.92, NULL 3.94 (jitter); DI 3.94, SPADE 2.00 (point).
- **A generic trained classifier works.** Logistic regression on SPADE count frequencies is trained on
  labelled scenes with widths drawn from ±20 % and tested at the least favourable width. It matches the
  model-based GLRT: no special learner is needed once the measurement is right.
- At d = 0.2σ under jitter, the best detect-first learner needs about 13,000× more photons than NULL-GLRT.

## 5. Status of the claims (novelty checks: `novelty_check_2026-11-07.md`, `novelty_check_nulling_2026-11-07.md`)

- **Exponent scaling (DI 4k vs Q 2k when lower moments are lost):** KNOWN in substance. It follows from Tsang
  arXiv:1806.02781 and Zhou & Jiang arXiv:1801.02917. Not claimed.
- **Testing formulation with a minimax over an unknown spread; the closed-form fidelity (S1); the constants
  (S2); SPADE's suboptimality factor (√K+1)/(√K−1):** not found in the literature. Most checks were at
  abstract level; one key paper was read partly in full. → candidate new.
- **Binary-nulling measurement:** PARTLY KNOWN in spirit. Triggiani & Lupo arXiv:2509.03511 use a
  hypothesis-dependent rotation of the first-order HG modes. Ours rotates the second-order (HG₀/HG₂) plane
  for a composite null. → candidate new as a specific construction.
- **Faint companion under centroid + jitter nuisance:** scalings verified; the optimal measurement is open.
- **Before any paper claim**, read in full Triggiani & Lupo (the remaining sections and Appendices D/E),
  Lu et al. 2018, Grace & Guha 2022, Deshler et al. 2024 and Sorelli et al. 2021.

## 6. Limits (stated plainly)

- Everything here is 1D with a Gaussian PSF. The jitter is fast (independent per photon) and Gaussian. There
  is no crosstalk, no dark counts and no background. Crosstalk is the documented failure mode of SPADE
  (arXiv:2303.02654), and a dark-count floor competes with signals that scale as a₀⁴.
- These are measurement advantages with matched classical lower bounds. They are not a separation for
  quantum *computing*. The quantum resource is the optical measurement before detection.
- No experiment and no on-sky data. The simulations use the standard idealised model.

## 7. Next steps (not started)

- **E1:** a crosstalk + dark-count model, to find which nuisance and noise levels keep the a₀⁴ advantage.
- **E2:** the optimal measurement for the companion problem (Helstrom / pretty-good measurement numerics).
- **E3:** 2D and anisotropic jitter (more nuisance parameters; predicted larger exponents).
- **E4:** a simulation of the two-stage adaptive nulling with unknown d.
- **E5:** full-text novelty reading (§5).
- **E6:** a space-domain-awareness and binary-star application study with realistic photon budgets.

## 8. Noise model E1: dark counts and known crosstalk (pre-registered 20ec391; code s03_noise.py; data results/s03_noise/noise.json)

Scenario H-S2: Gaussian jitter of unknown width (K = 3) vs an equal binary. The sorter has 7 detector ports.
B denotes the background probability in the signal (nulled) port.

| Prediction | Measured | Verdict |
|---|---|---|
| E1-P1: NULL follows H2 = 1/2 (sqrt(B + Delta) - sqrt B)^2; the local exponent moves from 4 to 8 | NULL/prediction = 0.85-1.00 at every point and noise level; local exponent 7.5-8.0 in the background-limited corner, 3.9-6.6 at a0 = 0.2 | confirmed |
| E1-P2: N_DI/N_NULL saturates at 3/(128 B), within a factor 2 | dark r = 1e-6: 2.21e4 vs 2.34e4; 1e-5: 2.46e3 vs 2.34e3; 1e-4: 280 vs 234; 1e-3: 38 vs 23 | confirmed (the excess at large r is DI's own loss, see P3) |
| E1-P3: DI changes by < 10 % for background r <= 1e-3 per sigma | maximum change 1.3 % (1e-6), 5 % (1e-5), **16 % (1e-4), 39 % (1e-3)** | **refuted for r >= 1e-4** |
| E1-P4: known crosstalk acts as a background c·eta^2 with c in [0.1, 10] | c = 1.65-1.74 for all eta; saturated advantage 1.29e4 / 1.5e3 / 137 / 15.7 vs predicted 1.35e4 / 1.5e3 / 137 / 15.8 (eta = 1e-3 / 3e-3 / 1e-2 / 3e-2) | confirmed |
| E1-P5: finite-N GLRT ratios within a factor 2 of exact H2 at r = 1e-4 | d = 0.2: 371 vs 275; 0.4: 222 vs 224; 0.8: 50 vs 57 | confirmed |

Why P3 failed: DI's signal is a fourth-cumulant (He₄) shape change. Part of it lives in the image wings, at
|x| ≳ 2-3σ, where the image density is comparable to a background of 1e-4 to 1e-3 per σ.

**Main conclusion (practical).**
- **The extra (σ/d)⁴ advantage exists only above a crossover separation.** With background B in the nulled
  port, the crossover is d_c ≈ 4σ (2B/(K−1))^{1/4}. Below d_c the advantage over the best detect-first
  learner stops growing and caps at ≈ 3/(128 B), independent of K.
- **Known crosstalk counts as B ≈ 1.7 η².**
- **Examples** (Gaussian jitter):

  | Background | Example source | d_c | Advantage cap |
  |---|---|---|---|
  | B = 1e-5 | -50 dB | 0.22σ | ≈ 2,300× |
  | B = 1e-4 | -40 dB | 0.40σ | ≈ 230× |
  | B = 1e-3 | -30 dB | 0.71σ | ≈ 23× |
  | B = 1e-2 | -20 dB | 1.26σ (outside the small-a0 regime) | a few × |

- **Present-day multi-plane light converters** report crosstalk of roughly −20 to −30 dB. This value comes
  from the survey literature and is not verified here. It would put today's hardware in the "≈ 2-20×"
  regime for deep sub-Rayleigh binaries under jitter.
- The noiseless 10⁴-10⁵× figures need a background of 1e-5 or lower in the signal port.

**Consequence for the method.** The advantage is now limited by the device, not by physics. The natural
next question is E1d: learning-to-measure. Can calibration photons be used to null the leakage
optically (a programmable sorter), and what does that cost?

**Prediction for E1d (to be pre-registered before coding).**
- A shot-noise-limited estimate of the leakage amplitude from M calibration photons leaves a residual
  background of about 1/M.
- Reaching B ≲ a0⁴ therefore costs M ~ a0^-4 calibration photons. That is the same order as the
  measurement itself, so the a0^-4 scaling, and with it the (σ/d)⁴ advantage, is restored up to a constant.
- If a bright reference source supplies the calibration photons, the cost is lower still.

## 9. E1d: learning-to-measure by calibrated optical nulling

Pre-registered in Addendum C (59ef11f) and Addendum D (93ef056). Code: s04_calibration.py (one control),
s05_calibration2.py (two controls). Data: results/s04_calibration, results/s05_calibration2.

**Setting.**
- The sorter has unknown static coherent crosstalk: eta = 0.01 or 0.03, about -38 / -28 dB, 5 random
  draws each.
- Programmable rotations null the dark port.
- The rotation is *learned* from M calibration photons, by pairwise probing on point-source calibrators sent
  through the same optics.
- The test is H-S2: Gaussian jitter of unknown width vs an equal binary; N_test = 1/H2.
- **Faint reference:** calibration photons cost the same as science photons; we minimise M + N_test.
- **Bright reference:** calibration is free.

**Results** (median over 30 calibration runs per point; d = 0.1-0.4 sigma). N_ideal is the noiseless,
crosstalk-free nulling receiver.

| | Uncalibrated (known crosstalk) | One control (E1d) | Two controls (E1d-2) |
|---|---|---|---|
| Scaling of the total photons in sigma/d | k ≈ 7.98 | k = 4.16 / 4.38 ✓ | k = 3.67 / 3.68 ✓ |
| Faint-reference total / N_ideal | up to ~2×10⁴ at d = 0.1 sigma | 1.15-4.0 (eta = 0.01); 2.2-13.5 (eta = 0.03) ✗ | 3.3-6.4 for both eta ✗ (tolerance was ≤ 4) |
| Bright-reference N_test / N_ideal | — | up to 2.8 / 12.6 ✗ | ≤ 1.09 (eta = 0.01) ✓; ≤ 1.34 (eta = 0.03) ✗ (tolerance 1.2) |
| Residual leakage × M (median) | — | 0.26-0.28 ✓ | 0.96 ✗ (tolerance ≤ 0.5) |
| Advantage over DI at d = 0.1 sigma with incoherent floor 1e-6 | — | 2.0e4 / 1.8e4 ✓ | 2.0e4 / 2.0e4 ✓ (cap 2.34e4) |

**What was learned.**
- **One control fails because of odd-mode leakage.** The light that defeats one-control nulling is the
  binary's *odd* mode leaking into the dark port. An on-axis calibrator cannot see it. It scales as
  a0²·eta², not a0⁴, so it wins at small separations: up to 2.6× the signal (Addendum D). The pre-registered
  design check had looked at one crosstalk draw only, and it happened to have almost none.
- **A displaced pair of calibrators fixes it.** With point sources at ±x_c, the two amplitudes differ only
  by the odd part. A second control then cuts the odd leakage from ≤ 1e-6 to ≤ 7e-9.
- **The (σ/d)⁴ scaling survives unknown crosstalk once the device learns its own null.** The calibration
  overhead is a constant factor, about 3-6× in the faint-reference regime and 1.0-1.34× with a bright
  reference. Without calibration the cost is up to about 10⁴×.
- **What the method cannot remove** is an incoherent floor: dark counts, scattered light, crosstalk that
  fluctuates faster than the calibration. That floor caps the advantage at ≈ 3/(128 b_inc), confirmed again
  here.
- **Refuted, by modest margins:** three constant-factor tolerances (P3', P4' at eta = 0.03, P1'). The scaling
  predictions (P2', P5') held.

**Limits of E1d.**
- U_err is static. The learner knows the calibrated device in the test likelihood (an optimistic
  assumption).
- The model is 1D and has only two controls.
- No drift and no calibrator pointing error are included.
- The "bright reference" assumes the reference light passes through the identical optical path.

## 10. Full-text novelty verdict (2026-11-07; supersedes the abstract-level status in section 5)

Readings (saved in `research/space/novelty_fulltext/R1-R4`) covered Triggiani & Lupo 2509.03511; Lu et al.
1802.02300; Grace & Guha 2107.00673 with its supplement; Sorelli et al. 2105.12396; Deshler et al. 2403.17988;
Tsang 1806.02781 and 1703.08833; Zhou & Jiang 1801.02917; Sakuldee & Rudnicki 2407.01995; Gessner, Fabre &
Treps 2004.07228; Linowski et al. 2211.09157; Schlichtholz et al. 2303.02654; Ozer et al. 2409.04323; Xin et
al. 2503.24292 (iEFC on a photonic-lantern nuller). Some readings went through a summariser.

**Passages I checked myself at source:**
- Grace & Guha Supplement I.7 (identical second moments).
- Triggiani & Lupo Eq. 18 ("independent of rho^alpha up to the order chi^2") and Eq. 29 (point source).

| Claim | Verdict | Decisive prior statement |
|---|---|---|
| Unknown-spread nuisance pushes the exponents to DI ~ (sigma/d)^8 vs quantum ~ (sigma/d)^4 | **KNOWN** | Tsang 1806.02781 Eqs. 4.14 and 5.1; Zhou & Jiang Thm 3 (estimation). **Grace & Guha Suppl. I.7 (testing):** for identical second moments the QCE is O(gamma^kappa) and DI O(gamma^{2kappa}). Our minimax reduces to this case, because the least-favourable scale matches the second moment. |
| S1: closed-form root fidelity for any symmetric spread | NOT FOUND | TL Eq. 7 gives only the general trace formula; Lu's closed form covers a point source only. |
| S2: constants (K-1)a0^4/4 (quantum), (sqrt K-1)^2 a0^4/4 (HG-SPADE), (4/3)(K-1)^2 a0^8 (DI) | NOT FOUND | Grace & Guha I.7 and Tsang give only O(·). Grace & Guha Eq. 7 has a DI gamma^4 term that is a SECOND-moment difference, so it does not apply here. |
| S3: HG-SPADE suboptimal by (sqrt K+1)/(sqrt K-1); binary-nulling (HG0-HG2 rotation) attains the optimum | NOT FOUND, and **answers a stated open question** | Grace & Guha I.7: "The TriSPADE measurement will not be quantum-optimal in this case, and finding an optimal measurement remains an open question for future work." TL Conclusions: the optimal measurement where SPADE fails is open. Known ingredients: TL rotate first-order modes only (2D orientation); Lu's dark port is dark under the POINT hypothesis; Deshler rejects HG0 only. |
| S5: faint companion with unknown centroid AND jitter, exponents 6/4/4 | NOT FOUND (setting partly known) | Deshler assumes a known centroid; de Almeida 2003.01166 uses a fixed misalignment; Kariya 2605.14432 (misaligned SPADE, singular learning theory) finds a KL-zero branch for an offset sorter and is related. |
| S7: background B in the dark port caps the advantage at 3/(128B); crossover d_c = 4 sigma (2B/(K-1))^{1/4}; known crosstalk acts as B ≈ 1.7 eta^2 | **PARTLY KNOWN** (mechanism); formulae NOT FOUND | Gessner, Fabre & Treps: any crosstalk gives F ∝ d^2 and d_min ∝ N^-1/4; SPADE still beats DI while \|r\|^2/(1-P_scat)^2 < 1/8. Linowski: SPADE loses to ideal DI as d -> 0 for unbalanced sources. Sorelli: dark counts make the FI vanish (qualitative). Liu et al. 2608.01765: background-robust HG0/HG1 one-vs-two test. All of these are estimation or point-vs-two; none is a composite fourth-order test. |
| S8: learning the null by pairwise probing; odd-mode leakage needs a displaced ±x calibrator pair; the (sigma/d)^4 scaling is restored at constant photon overhead | NOT FOUND for mode sorters; the **method (pairwise probing) is KNOWN in coronagraphy** | EFC / iEFC pairwise probing (coronagraphs; photonic-lantern nuller, Xin 2503.24292). Sorelli Sec. IX suggests measuring the crosstalk matrix "with the help of two test sources". Ozer calibrates with one coherent source, as a data-side correction. Nothing found on photon-cost scaling, odd-leak invisibility or restored scaling. |

**How the contribution can be stated honestly:**
- For the problem flagged as open by Grace & Guha (2022, Suppl. I.7) and by Triggiani & Lupo (2025), we
  give, in 1D for a symmetric binary against a single source with an unknown symmetric spread:
  - the exact fidelity;
  - the leading-order constants;
  - the size of HG-SPADE's shortfall;
  - a linear-optics measurement that attains the quantum limit at leading order.
- We then quantify how detector background and calibratable crosstalk cap or preserve the advantage.
- We do not claim the scaling exponents.
- We do not claim pairwise probing as a method. We claim its application to mode-sorter nulls, together with
  the photon-cost analysis.

**Still open for a paper:**
- 2D;
- a non-perturbative (all-orders) optimality proof for the nulling measurement;
- an unknown separation (two-stage scheme, proposed and not simulated);
- drift;
- the optimal companion measurement.

## 11. X1-X5: 2D, matched scenes, spectral lines, collective vs single-copy, two-photon test

Pre-registered in Addendum E (111b4bc). Code: `research/space/x_suite.py`. Data: `results/x_suite/X*.json`.

**Four code faults, found by my own consistency checks and fixed before any verdict:**
1. A thinned (invalid) Gauss–Hermite rule in X2 and X5.
2. An optimiser stuck in local minima in X2 and X4.
3. The quantum and classical Chernoff minimisation excluded the boundary s -> 1, where rank-deficient states have
   their optimum (X4).
4. float64 rounding in the rank-4 fidelity at a0 = 0.02 (X2); fixed with mpmath and exact overlaps.

The earlier outputs are kept as `*_run1_buggy.json` and `X2_run2_floatQ.json`. The verdicts use the corrected
runs; the predictions were not changed.

| ID | Prediction | Result | Verdict |
|---|---|---|---|
| P1a | 2D isotropic: Q = 0.25 a0^2, exponent 2, TriSPADE >= 0.9 Q, DI 4 | Q = 1.0000e-4 at a0 = 0.02; exponents 2.00 / 3.98; TriSPADE/Q = 1.00 | confirmed |
| P1b | anisotropic rho: Q within 15 % of rho a0^2/(2(1+rho)) + 0.5 a0^4 | Q/pred = 0.968-0.999 everywhere (rho 0.1 ... 1e-4) | confirmed |
| P1c | 2D uniform disc: Q = 0.25 a0^2 | Q/(0.25 a0^2) = 1.000 | confirmed |
| P1d | jitter on both (2D iso): local exponent >= 3.3 (s1 = 0.4, a0 = 0.02), <= 2.7 (s1 = 0.05, a0 = 0.1); decreasing in s1 | 3.99 and 2.54; Q at a0 = 0.02: 1.23e-5 > 3.69e-6 > 9.6e-7 > 2.3e-7 | confirmed |
| P1e | 1D line jitter on both: Q and DI exponents within 1.5 at a0 <= s1/6 | s1 = 0.2, a0 = 0.02: 7.81 vs 7.99 | confirmed |
| P2a | square vs isotropic spread: Q 4, DI 8 +- 0.5, HG 4, support >= 0.9 Q | Q 3.99 / 4.00; DI 7.55 (Gaussian), **7.03 (disc)**; HG 3.99 / 4.00; support/Q = 1.000 | confirmed except DI-disc (refuted) |
| P2b | triangle: Q exponent 3, DI 6, HG 4 | **Q 3.99**; DI 5.96; HG 4.00 | Q prediction refuted |
| P3a | Student-t nu = 30, 10: constants within 10 % | Q/formula 0.998, 0.997; HG/formula 0.999, 0.998 | confirmed |
| P3b | nu = 5, 6: exponents in [3.5, 4.5] | 3.92-3.94 (formulas still within 0.6 %) | confirmed |
| P3c | Voigt: K formulas within 15 %; HG/Q >= 0.5 when K_eff >= 10 | formulas within 0.5 % (K_eff 5.3-6.6); second clause untested (no case with K_eff >= 10) | confirmed / untested |
| P4a | 1D nulling / QCB >= 0.95 | 0.997-0.999 (HG 0.14-0.15) | confirmed |
| P4b | 2D TriSPADE / QCB >= 0.95 | 0.997-0.999 | confirmed |
| P4c | companion: optimised single-copy >= 0.9 QCB | 0.947 (HG 0.264) | confirmed |
| P5a | HOM: H0 = 0, H1 = (1 - e^{-4 a0^2})/4 for any common jitter and crosstalk | max abs P_H0 = 2e-18; H1 relative error <= 2e-14 | confirmed |
| P5b | differential-jitter background (1 - (1 + s_d^2)^{-1/2})/2 | exact to 4 digits (after the quadrature fix) | confirmed |
| P5c | memory asymmetry background c eps^2, c in [0.1, 10] | c = 3.7-3.9 | confirmed |
| P5d | s_j >= d: HOM >= 2x best local pair strategy; s_j = 0: SPADE about 2x HOM | 9.0-9.3x at s_j = d (up to 507x at s_j = 8d); 2.0x at s_j = 0 | confirmed |
| P5e | crossover s_j* within x2 of d/2 | **s_j* = 0.29-0.34 (d/2), about d/6.5** (HOM wins earlier) | refuted |
| P5f | classical frames of k = 4, 8 photons grow with k but stay below HOM | 1.82e-5 -> 1.94e-5 -> 2.16e-5 per photon vs HOM 6.23e-4 | confirmed |
| P5g | quantum pair bound <= 2x HOM | <= 1.78 for s_j > 0; **2.01-2.03 at s_j = 0** | refuted (marginal, s_j = 0 only) |

**What this establishes:**
1. **2D.**
   - A round blur (jitter or stellar disc) only halves the exponent, to 0.25 a0^2, and standard TriSPADE is
     optimal there. The 1D fourth-order story does not carry over to typical 2D imaging.
   - Elongated blur follows rho a0^2/(2(1+rho)) + 0.5 a0^4. Fourth order needs rho <~ a0^2.
2. **Jitter on both hypotheses (the correction to the 1D model).**
   - The scaling advantage is lost once the jitter exceeds the separation.
   - In 1D line jitter, the photon advantage over direct imaging at a0 = 0.02 falls from 5.9e5 (s1 = 0) to
     2.4e4 / 2.9e3 / 242 (s1 = 0.05 / 0.1 / 0.2 sigma). A large constant factor remains, but the scaling is
     no longer better than direct imaging's.
3. **Matched round scenes are genuine fourth-order problems.** Square and triangle vs a round blur:
   - projecting onto H1's support reaches the quantum bound exactly (1.000);
   - HG-mode sorting reaches only 55-65 % (square) and 2-9 % (triangle), because it is blind to the
     triangle's odd moments;
   - the triangle's third moment gives direct imaging a sixth-order signal, but the quantum exponent stays 4.
4. **Spectral lines.**
   - The constants (K-1) a0^4/4 and (sqrt K - 1)^2 a0^4/4 hold within 0.6 % for Student-t (nu >= 5) and
     truncated Voigt profiles.
   - Nulling is exactly optimal for all line shapes tested (NULL/Q = 1.000).
   - HG reaches (sqrt K - 1)/(sqrt K + 1) = 29-44 % of it.
5. **Entanglement inside one receiver (fast nuisances) is not needed.**
   - Single-copy measurements reach 99.7-99.9 % of the quantum Chernoff bound (1D nulling, 2D TriSPADE).
   - In the companion case an optimised single-copy measurement reaches 94.7 %.
6. **Entanglement does help under slow, common-mode errors.**
   - The two-photon antisymmetric (HOM) test is exactly immune to shared jitter and static crosstalk.
   - It beats every single-photon strategy: mode sorting, nulling and direct imaging on pairs, and classical
     processing of frames up to 8 photons.
   - The margin is 9x when the jitter equals the separation and up to about 500x at 8x.
   - The crossover sits at s_j about d/6.5. Below it, single-photon SPADE is 2x better.
   - For s_j >~ d, HOM is within 1-10 % of the two-photon quantum bound.
   - Costs: memory asymmetry gives an H0 background of 3.8 eps^2; differential jitter gives s_d^2/4.
7. **Refuted predictions, recorded as such:** P2a (DI-disc exponent, fitted only in the pre-asymptotic window
   a0 >= 0.04), P2b (triangle quantum exponent 4, not 3), P5e (the crossover comes about 3x earlier than
   predicted), P5g (marginal, at s_j = 0 only).

**Novelty status.** The HOM / Schur-sampling robustness principle is known (de Almeida et al., PRA 2025). New
here, as far as the literature checks go:
- the testing formulation under slow common-mode jitter plus crosstalk;
- the quantitative crossover against the best single-photon strategies (s_j* about d/6.5);
- the tolerances (3.8 eps^2, s_d^2/4);
- the 2D boundary formula;
- the instrumental-jitter correction;
- support-projection optimality for matched round scenes;
- the robustness of the constants across spectral line shapes.

## 12. QX1: learned quantum receivers (pre-registered 0e9b641; code research/space/qx1_learned_receiver.py; data results/qx1/qx1.json)

**Model.** A trainable orthogonal (Naimark) map on the first 8 HG modes (+ A = 0 or 4 ancilla vacuum modes),
followed by photon counting, plus an exact remainder port.

**Two implementation fixes, made before the full run:**
- **Remainder port.** It was computed as 1 − Σports, which made the gradient exactly zero. It now uses the
  exact constant 1 − tr ρ_M.
- **Optimiser.** A decaying Adam step plus an L-BFGS soft-min polish. The optimal rotation is ~a0²/√2 ≈ 0.007
  rad, so it needs ~1e-4 precision.

| ID | Prediction | Result | Verdict |
|---|---|---|---|
| QX1-A1 | (a) learned ≥ 0.95 of nulling; a port with overlap ≥ 0.9 with the nulled port 2' | Bhattacharyya (training objective) 0.975-0.994 of nulling; overlap 0.9905-0.9998. Chernoff 0.90-0.97 of nulling (0.914 / 0.899 at a0 = 0.05) | confirmed on the trained objective and the overlap; **the Chernoff ratio falls below 0.95 at a0 = 0.05** |
| QX1-A2 | (b) jitter on both hypotheses: learned ≥ 0.95 of nulling | **1.01-1.03 × nulling**; 98.8 % of QCB (nulling: 96.1-97.9 %) | confirmed: **learning beats the hand-designed receiver** |
| QX1-A3 | (c) companion: projective learned in [0.90, 0.97] QCB at the least-favourable nuisance; POVM ≥ projective, gain ≤ 3 % | projective 0.831 / 0.865; POVM 0.843 / 0.846 (a0 = 0.05 / 0.1). Full minimax: 0.72-0.83 of QCB | **refuted**: below 0.90; the POVM gain is ≤ 1.2 % and not always positive. The fixed-point optimisation in X4 (94.7 %) is better |
| QX1-B1 | data-driven SPSA from photon counts: monotone in T, ≥ 0.9 at T = 1e8 | 0.0004, 0.0003, 0.12, **0.22** of the model-based optimum (T = 1e5…1e8; 3.6e8…3.6e11 training photons). It ends worse than its own HG start (0.275) | **refuted** |
| QX1-C1 | nominal receiver on a crosstalk device ≤ 0.3 | 0.045 | confirmed |
| QX1-C2 | retraining with known crosstalk ≥ 0.9 | 1.0015 | confirmed (a unitary error is fully undone) |
| QX1-C3 | in-situ data-driven retraining under crosstalk (T = 1e8) ≥ 0.8 | 0.0005 | **refuted** |

**What this establishes (honest):**
1. **Model-based learning works.**
   - From the plain HG starting point, gradient training of a photonic receiver rediscovers the hand-derived
     nulling measurement (overlap ≥ 0.99) without being told it exists.
   - Where nulling is not exactly optimal (jitter on both hypotheses), the learned receiver beats it by
     1-3 %, reaching 98.8 % of the quantum Chernoff bound.
   - This is "quantum-aware design by learning": the states are known to the optimiser.
2. **Extra output ports (a non-projective POVM) add ≤ 1 %.** Projective receivers are essentially enough
   here.
3. **The faint companion stays hard.**
   - The learned minimax receiver reaches only 72-86 % of the QCB, below the 94.7 % found earlier by
     optimising at a fixed nuisance point.
   - Learning did NOT find a better companion measurement. The minimax objective over a 2D nuisance grid,
     trained on the Bhattacharyya surrogate, is the likely limitation; this is unproven.
4. **Naive data-driven learning from science photons fails at sub-Rayleigh signal levels.**
   - Even 3.6 × 10¹¹ training photons gave ≤ 22 % of the optimum, worse than not training at all.
   - The reason is structural: the training signal (changes in port probabilities ~a0⁴ ≈ 1e-4) is buried in
     shot noise. A gradient estimate needs ~1/a0⁸ photons per step.
   - Only one SPSA configuration was tried, with no tuning. A better optimiser could do better, but the
     scaling argument stands.
   - **Design lesson:** learn the measurement from bright calibration references (E1d: residual ∝ 1/M), or
     from a physical model, not from the faint science photons.
5. **Unknown coherent crosstalk is fully undone by retraining when the device is characterised** (1.0015 ×
   the crosstalk-free optimum). In-situ data-driven retraining fails, for the same shot-noise reason.

**Novelty status.** Trained optics for quantum-optimal inference is known: Filipovich, Duplinskii & Lvovsky,
arXiv:2609.08014; Hu, Xin & Lu, arXiv:2611.08034. New here, as far as the searches show:
- learning under composite nuisances, with exact ground truth;
- learned beats hand-designed when H1 is jittered;
- the negative result for data-driven learning from faint photons, with its 1/a0⁸ scaling explanation;
- crosstalk undone by retraining.

## 13. QX1-R: reference-assisted learning (pre-registered 3951968; code research/space/qx1r_reference_learning.py; data results/qx1r/qx1r.json)

**Setting.** Case (a), a0 = 0.1. All training photons come from bright laboratory reference scenes sent through
the same optics, never from the science target. The evaluation is the exact minimax Bhattacharyya exponent on
the science task, relative to the model-based optimum (4.76e-5).

| ID | Prediction | Result | Verdict |
|---|---|---|---|
| R1b | data-driven (tuned SPSA) ≥ 0.8 at T = 1e10, ≥ 0.9 at T = 1e12 | 0.986 / 0.988 / 0.989 (crosstalk-free) and 0.986 / 0.977 / 0.975 (unknown crosstalk) at T = 1e8 / 1e10 / 1e12 | confirmed |
| R1a | the ratio rises with T on both devices | rises on the crosstalk-free device (0.986 → 0.989); **falls slightly with crosstalk** (0.986 → 0.975, within ~1 %) | partly refuted |
| R2a | null-digging (dark-port fraction only) ≥ 0.9 at T = 1e10 | 0.175 / 0.275 / 0.195 | **refuted** |
| R2b | the residual dark-port leak falls with photons (slope −1.5 … −0.5) | 1.0e-4, 4.9e-5, 8.6e-5; slope −0.02 (a plateau) | **refuted** |

**What this establishes:**
1. **Data-driven learning works when the optimiser is tuned.**
   - With small perturbations (0.003 rad), normalised gradients averaged over 4 draws, and 600 steps, a learner
     that sees only photon counts reaches 98.6-98.9 % of the model-based optimum on the crosstalk-free device.
   - It reaches 97.5-98.6 % on a device with UNKNOWN crosstalk (an untrained receiver there: 4.5 %).
   - This already holds at T = 1e8 photons per scene per evaluation, about 2.9e12 photons per training run.
2. **Correction to section 12, point 4, and claim S13.**
   - QX1-B and QX1-C3 used T = 1e8 too and reached only 0.22 / 0.0005. Their failure was therefore caused by the
     optimiser settings: a 0.05 rad perturbation, ~7× the optimal rotation, and single-draw gradients.
   - It was NOT a structural shot-noise limit. The "~1/a0⁸ photons per gradient" explanation given there is
     retracted.
   - What remains true is the photon COST: ~3e12 training photons is impossible to collect from a faint target
     but trivial from a bright internal reference (seconds of lab light). The design lesson, learn from bright
     references, stands. Only the reason given changes.
3. **A narrow objective fails.**
   - Minimising only the dark-port leak of a reference binary cuts the leak 15-30× (from the crosstalk level of
     ~1.5e-3), but it stalls at ~1e-4 and leaves the science exponent at ≤ 28 % of the optimum.
   - The full task objective, with both reference classes in a minimax, is what works.
   - So the receiver must be trained against the actual discrimination task, not against a proxy darkness
     criterion. Why the proxy stalls (a degenerate objective over 28 parameters, or the optimiser) is not
     resolved.
4. **Bottom line for QML here.** A photonic receiver trained purely from photon counts of bright labelled
   reference scenes reaches ~98 % of the quantum-optimal design, even through unknown crosstalk. This is the
   strongest practical QML result of the project.
   - **Caveats:** 1D only; one separation; the references must match the science geometry (same separation,
     jitter range); no drift between calibration and science; the model-based optimum itself is 97.8 % of the
     QCB at a0 = 0.1.

## 14. QX2: translation-invariant vs U(m)-invariant two-photon measurements (pre-registered 3afbfbc; code research/space/qx2_invariant_pairs.py; data results/qx2/qx2.json)

**Setting** (as X5): two photons per frame share a slow common jitter X ~ N(0, sj^2); a static unknown crosstalk
U = expm(eps(A_k - A_k^T)) acts on HG modes 0..12; H0 point, H1 equal binary of separation d.
- M1 = HOM.
- M2 = coarse translation-invariant {rel0, not rel0}.
- M3 = refined {antisym, sym minus rel0, rel0}.
- Q_pair = exact optimal pair Bhattacharyya exponent (-log F, from a coherent-state Gram matrix, U-invariant).
- L = learned projective measurement inside the symmetric subspace, plus the antisym outcome.

**Code fault fixed before any verdict.**
- The pre-registered pair triangle m + n <= 18 cannot hold crosstalk acting on modes 0..12, because pairs of
  modes reach m + n = 24. At eps = 0.1, 0.3 % of the probability fell into the remainder outcome, and HOM
  evaluated inside the triangle came out below its exact value.
- NT was raised to 24. Remainders are now <= 4e-11, and the in-triangle HOM matches its closed form to 4e-10.
- The predictions were not changed.

| ID | Prediction | Result | Verdict |
|---|---|---|---|
| P1 | eps = 0: M3 = -(1/2)log(1 - q_T) for every sj; M3/HOM <= 1.011 for d <= 0.4, in [1.05, 1.08] at d = 1 | agrees with the closed form to <= 5e-10 at every sj; M3/HOM = 1.0006 / 1.0025 / 1.0100 (d = 0.1 / 0.2 / 0.4), 1.064 (d = 1) | confirmed |
| P2 | Q_pair/M3 decreases with sj; <= 1.15 at sj = 0.8 for d <= 0.4 | decreasing; 2.00-2.01 at sj = 0 → 1.0003 / 1.0012 / 1.0048 at sj = 0.8 | confirmed |
| P3 | M2 falls below HOM at some eps* <= 0.01 (d <= 0.4, every k, sj in {0, 0.4}) | eps* = 1e-4 (d <= 0.2), 1e-4 to 3e-4 (d = 0.4); H0 leak = 25 eps^2; at eps = 0.01 M2 keeps 5-37 % of HOM | confirmed |
| P4 | M3 >= HOM at every state; at eps = 0.1 its gain over HOM <= 0.2 x the eps = 0 gain | M3 - HOM >= 0 everywhere (min +4e-13); remaining gain 4-7 % of the eps = 0 gain | confirmed |
| P5 | L(i), nuisance known, >= 0.99 of Q_pair at (0,0), (0.2,0), (0.2,0.03) | 0.9994-0.9999 | confirmed |
| P6 | L(ii), minimax over the 50-state box, / HOM in [1.00, 1.10]; ancillas (A = 8) add <= 2 % | 1.0023 (d = 0.2), 1.0097 (d = 0.4); bound min Q_pair/HOM 1.0037 / 1.0149; A = 8 adds < 0.05 % | confirmed |

**What this establishes:**
1. **The physical symmetry group buys almost nothing (route R3(i) is essentially empty for this task).**
   - Restricting the immunity to translations instead of all of U(m) gains at most
     2/(1 + e^{-d^2/8}) - 1 ≈ d^2/16 in click probability over HOM: 0.06-1 % for d <= 0.4 sigma.
   - This is exact, and independent of the jitter strength.
   - Reason: translation-invariant measurements can only read the relative coordinate of the two photons, and
     HOM already reads its odd part. The even part adds only an O(d^4) signal.
2. **That small gain is fragile.**
   - The coarse translation-invariant test (M2) leaks 25 eps^2 under H0 and drops below HOM once eps >= 1e-4.
   - The refined version (M3) can never fall below HOM (Cauchy-Schwarz), but at eps = 0.1 it keeps only 4-7 % of
     its tiny gain.
   - So "trading crosstalk immunity for information" is not a useful design axis below the Rayleigh limit.
3. **HOM is near-optimal wherever jitter immunity matters.**
   - The best possible pair measurement (Q_pair) exceeds HOM by 0.4 % (d = 0.2) and 1.5 % (d = 0.4) at sj = 0.8.
   - As sj grows, Q_pair converges to the translation-invariant optimum M3, as the derivation requires.
4. **Learning (the QML part).**
   - A learned pair measurement reaches 99.9 % of the pair bound when the instrument state is known.
   - Trained minimax over the whole jitter-crosstalk box it beats HOM by only 0.2-1 % at the worst case; that is
     62-65 % of the 0.4-1.5 % that is available.
   - But it is never below HOM anywhere, including unseen crosstalk draws (not pre-registered: held-out minimum
     1.0016 / 1.0067 x HOM). It is 1.5-1.7x HOM at zero jitter.
   - So the useful learned object is a HOM refinement: guaranteed no worse than HOM, and much better when the
     nuisance happens to be small.
   - Extra POVM outcomes (ancillas) add nothing.
5. **Caveats:** 1D; two photons only (k > 2 Schur sampling not tested); ideal quantum memory; the learned
   measurements need two-photon entangling operations, not just linear optics.

**Novelty status.**
- The Schur-Weyl / block structure is textbook, and HOM immunity is known (de Almeida et al.).
- Not found:
  - the exact subgroup-vs-U(m) gap 2/(1 + e^{-d^2/8});
  - its fragility law (25 eps^2 for this crosstalk model);
  - the learned minimax HOM-refinement numbers.
- This is a solid negative result for route R3(i), not a positive advantage.

## 15. QX3: learn-then-classify from labelled reference photons (pre-registered 3afbfbc; code research/space/qx3_learn_then_classify.py; data results/qx3/qx3.json)

**Setting.**
- An unknown static pointing offset theta ~ N(0, tau^2) is common to everything.
- The learner gets n labelled reference photons from a point source at theta, then ONE test photon: H0 a point
  at theta, H1 an equal binary of known d centred at theta.
- Metric: exact Bayes errors; excess risk E = P - P_KNOWN; recovered fraction (1/2 - P)/(1/2 - P_KNOWN).
- The known-theta advantage is 1/2 - P_KNOWN = 0.678 a0^2.
- Numerical checks:
  - COH grid convergence (K -> 2K): <= 5e-9 relative to the excess;
  - PCA threshold 1e-13 -> 1e-11: changes the excess by 1e-12 relative;
  - COH(n = 0) equals NONE.

| ID | Prediction | Result | Verdict |
|---|---|---|---|
| P1 | E_COH <= E_MFDI <= E_PLUG and E_COH <= E_SPADE | holds at every n >= 1 for all six (a0, tau). At n = 0 all strategies are the same quantity (NONE), computed on different quadrature grids; they differ by <= 2e-9 relative | confirmed |
| P2 | E_MFDI/E_COH <= 1.2 for n >= 16 | 1.153-1.188 | confirmed (but the ratio does not tend to 1; point 1) |
| P3 | at n = 64 the ratio varies < 10 % across a0 | 1.174-1.180 (tau = 0.2), 1.180-1.186 (tau = 0.5): < 1 % | confirmed |
| P4 | E_PLUG/E_MFDI in [1.5, 3] for n >= 16 | 1.001-1.008 (at most 1.031, at n = 0-2) | **refuted** |
| P5 | E_SPADE/E_MFDI >= 5 at n = 128, tau = 0.5 | 19.5-19.8 (and 5.8 at tau = 0.2) | confirmed |
| P6 | E_MFDI x (n + 1/tau^2) constant within +-15 % on n in [16, 128] | within -2.6 % / +1.8 % | confirmed |
| P7 | n90 (MF-DI) is the same for all a0 at fixed tau | tau = 0.2: n90 = 0 for all a0 (95.5 % with no training); tau = 0.5: n90 = 8 for all a0 | confirmed |

**What this establishes:**
1. **Coherent learning keeps a constant advantage, unlike for qubits.**
   - E_MFDI/E_COH rises to an asymptote of 1.184. This was checked beyond the pre-registered grid (exploratory,
     a0 = 0.1, tau = 0.2): 1.1817 / 1.1831 / 1.1838 at n = 256 / 512 / 1024.
   - It is the same for every a0 (within 1 %) and both tau. The joint measurement on references plus test is
     worth ~18 % more reference photons, for all n.
   - Measure-first with direct imaging is the best Gaussian measure-first here: it is equivalent to homodyne on
     the collective reference mode, which reaches the QFI for theta.
   - Mechanism (derived after the run):
     - The n references are unitarily equivalent to one collective coherent mode |sqrt(n) theta/2>.
     - Interfering the test photon with it (weights sqrt(n) : 1) gives one output that is dark under H0 for
       EVERY theta. Under H1 that output carries a theta-INDEPENDENT binary with a0^2 reduced by n/(n+1).
     - So the coherent learner pays for the reference uncertainty as a slightly smaller separation:
       E ~ adv/(n+1).
     - Checked numerically: the dark port alone comes within 3 % of E_COH at n = 128 (tau = 0.5) and within 19 %
       at tau = 0.2, where the prior still matters and the bright port uses it.
     - Measure-first pays for it as an incoherent jitter of the test PSF: E_MFDI = c x adv/(n + 1/tau^2), with
       c = 1.12-1.17 for n >= 16 (the P6 constant), rising toward ~1.18 as the residual offset shrinks.
     - The asymptotic ratio of the two costs is c, i.e. the 1.18.
   - Contrast: for qubit templates, measure-first is optimal (Sentis et al. 1208.0663).
   - Prior art: in spirit this matches Sentis-Guta-Adesso 1410.8700, where a joint measurement beats Gaussian
     estimate-first for coherent states, most at low signal energy; one test photon is the extreme of that.
   - Caveat: COH needs the reference photons stored and coherently combined, i.e. quantum memory and multi-photon
     operations.
2. **Plug-in is essentially Bayes-optimal here (P4 refuted).**
   - Estimating theta and applying the known-theta Helstrom measurement costs <= 0.8 % extra for n >= 16.
   - The qubit factor-of-~2 plug-in penalty (Guta-Kotlowski) does not appear: misalignment enters the Helstrom
     projector only at second order.
3. **A sign-blind training measurement is almost useless.**
   - HG counting of the references on the nominal axis (SPADE) recovers 95.6 % at n = 128 against 95.5 % with no
     training at all (tau = 0.2), and only 82.7 % at tau = 0.5 against 99.1 % for direct imaging.
   - Post-hoc explanation:
     - SPADE posteriors are symmetric about the axis.
     - The single-copy excess is, to leading order, linear in the posterior second moment about the axis.
     - By the tower property, the average of that second moment equals the prior tau^2 for any n.
   - So calibration must break the sign symmetry (centroid measurement), which is why it gains nothing.
4. **The single-copy metric hides the background problem (an important limitation).**
   - At tau = 0.2 no learning is needed at all (95.5 % at n = 0), because an offset shared by both hypotheses
     moves both click probabilities alike.
   - For many test photons (error exponents) a residual offset creates an H0 background. The reference cost would
     then scale as (sigma/d)^2 (pre-registered as not covered, not computed).
   - The coherent mechanism above (an output dark under H0 for every theta) is exactly what removes that
     background. That makes the many-test-photon version the natural follow-up, where the coherent gain could be
     large rather than 18 %.
5. **Cost of learning by measure-first.** E_MFDI = c x 0.678 a0^2/(n + 1/tau^2) with c ~ 1.1-1.2, so the number of reference
   photons for a given recovered fraction does not depend on the separation (single-copy metric).
6. **SYM**, the (n+1)-photon symmetric projection: zero H0 background for any theta, but for single-copy error it
   reaches only (1 - e^{-a0^2})/(2 x 0.678 a0^2) = 73.5 % of the known advantage as n -> infinity. It ignores the
   Helstrom structure, so it is not the single-copy optimum.

**Novelty status (abstract-level, Q1 sweep):**
- Learn-then-classify is solved for qubits (no coherent gap) and studied for coherent-state templates (a joint
  gain at low energy, SGA 2015).
- Not found:
  - the imaging instance with an unknown pointing nuisance;
  - the asymptotic constant 1.18 and its independence of the separation;
  - the interference mechanism (H0-dark port, separation shrink vs jitter);
  - the near-optimality of plug-in;
  - the uselessness of sign-blind SPADE calibration.
- A full-text check of SGA 2015 is needed before any claim about the constant.

## 16. QX3-E: many-test-photon exponents under an unknown pointing offset (pre-registered b65b853; code research/space/qx3e_exponents.py; data results/qx3e/qx3e.json)

**Setting.**
- N test photons from one hypothesis (H0 point, H1 equal binary, a0 = d/4) share a static unknown pointing
  offset; optionally kappa N labelled point-source reference photons.
- Metric: the error exponent per test photon as a fraction of a0^2, the known-pointing optimum (the numerical
  QCB equals a0^2 to 1e-8).
- Classical learner:
  - references plus a fraction f of the test photons by direct imaging (centroid);
  - then a single-photon receiver at the estimate: SPADE, or a learned 6-mode receiver;
  - exponent from the exact large-deviation formula, maximised over f.
- Quantum learner: symmetric-subspace projection of k stored test photons (Q-SCHUR_k, no references), or of
  each test photon with kappa references (Q-REF).

**Code faults fixed before any verdict.**
1. The first run crashed: 14 parallel workers exhausted memory. No results were produced. Fixed with 5
   workers and s-chunking.
2. The worst-case search covered only non-negative offsets t.
   - That is valid for SPADE, whose ports are even in t, but not for learned receivers that mix HG0 and HG1.
   - The learned receivers exploited this half-domain adversary and appeared 28-35 % better than SPADE. Their
     true exponents (both signs) were BELOW SPADE (0.13 / 0.26 a0^2 at kappa = 0 / 1).
   - Fixed with a two-sided domain for non-even receivers, and the receivers were retrained. The faulty run is
     kept as results/qx3e/qx3e_run1_halfdomain.json. SPADE values are identical in both runs.
   - The kappa = 0 learned value was checked on a dense two-sided grid plus 60 random restarts.

| ID | Prediction | Result | Verdict |
|---|---|---|---|
| QE1 | Q-SCHUR_inf >= 0.98 a0^2 (a0 <= 0.2); Q-SCHUR_k within 3 % of (k-1)/k (a0 <= 0.1) | 0.9988 / 0.9950 / 0.9800 (a0 = 0.05 / 0.1 / 0.2); Q-SCHUR_k within 1.5 % of (k-1)/k | confirmed |
| QE2 | C-SPADE/a0^2: [0.15, 0.30] at kappa = 0; [0.35, 0.50] at 1; [0.50, 0.67] at 10; [0.60, 0.75] at 100; < 0.85 at 1000; a0-variation < 10 % | 0.174 / **0.334** / 0.525 / 0.629 / 0.691; exactly a0-independent (the worst case is a Poisson-vs-Poisson pair) | partly refuted (kappa = 1 slightly below range) |
| QE3 | C-LEARN <= 1.1 x C-SPADE | 1.000 at kappa = 1, 10, 100 (both a0); at kappa = 0: **1.166** (a0 = 0.1), 0.98 (a0 = 0.05; the optimiser did not find the gain) | partly refuted (kappa = 0) |
| QE4 | Q-SCHUR_inf/C-SPADE >= 3 at kappa = 0, >= 1.3 at kappa = 100; HOM pairs beat C-SPADE at kappa <= 1 | 5.6-5.7 and 1.56-1.59 (vs the best learned at kappa = 0: 4.9); HOM/C-SPADE 2.7-2.9 (kappa = 0), 1.41-1.49 (kappa = 1) | confirmed |
| QE5 | Q-REF/C-SPADE >= 1.1 for kappa in {1, ..., 100} | 1.48-1.73 | confirmed |
| QE6 | exact finite-N local exponent approaches the LD exponent monotonically, within 30 % at N = 8000 | within 2.7 % at N = 8000 (kappa = 1 and 10); monotone for kappa = 1, **not for kappa = 10** (0.93, 1.19, 1.09, 0.99, 1.03) | partly refuted (monotonicity) |

**What this establishes:**
1. **Classical pointing calibration cannot make a zero-background test work.**
   - With static pointing uncertainty, the best classical learner tested here reaches only 17-20 % of the
     known-pointing exponent with no references.
   - With references, it reaches 33 % (1 per test photon), 52 % (10), 63 % (100) and 69 % (1000). An
     exploratory point, not pre-registered: 82 % at 1e8 references per test photon.
   - The curve E/a0^2 = F(kappa) is universal: it is exactly independent of the separation.
   - Mechanism: every residual offset t puts an H0 background u a0^2 (u = t^2/4a0^2) into the port carrying the
     H1 signal. The Chernoff exponent h(u) of a near-zero-background test recovers only logarithmically as
     u -> 0, so E/a0^2 ~ min over u of [2 kappa u + h(u)].
   - Spending test photons on centroiding helps only when references are scarce: f* = 0.41 at kappa = 0, and 0
     for kappa >= 1.
   - A learned single-photon receiver ties SPADE for kappa >= 1. At kappa = 0 it gains up to 17 %, by measuring
     the centroid and the binary signal with the same sign-sensitive ports. It does not escape the background
     limit.
2. **The quantum learner needs no references at all.**
   - Projecting k stored test photons onto their symmetric subspace has exactly zero H0 background for every
     pointing offset (and every static crosstalk).
   - It reaches ((k-1)/k) a0^2, and 98-99.9 % of the known-pointing optimum as k grows.
   - Group sizes needed to beat classical calibration:
     - k = 2 (HOM pairs, 0.49 a0^2) beats classical with up to ~3 references per test photon;
     - k = 3 (0.66) beats it up to ~100;
     - k = 4 (0.74) beats it at 1000;
     - k = 8 (0.87) beats it even at 1e8.
   - Spending the same references coherently (Q-REF) beats measuring them by 1.5-1.7x.
   - Advantage factors (quantum exponent / best classical exponent):
     - 4.9-5.7x with no references;
     - 3.0x with 1 reference per test photon;
     - 1.9x with 10;
     - 1.6x with 100.
3. **Finite-N check.** At a0 = 0.1 and N = 8000 test photons, the exact classical Bayes error is 1.6e-13
   (kappa = 1) and 3.3e-20 (kappa = 10). Symmetric projection gives ~1.4e-35. The exact local exponents agree
   with the large-deviation exponents to 3 %.
4. **This is the clearest quantum-learning advantage of the project.**
   - Classical learners must calibrate the nuisance and pay for it forever; the coherent learner never has to
     learn it, because the invariance is built into the measurement.
   - It is an exponent-level factor of 1.6-5.7x, not a scaling advantage.
5. **Caveats.**
   - k photons must be stored and released together into a collective symmetric projection (quantum memory). The
     implementation route, multiport interference of synchronised photons, i.e. weak Schur sampling of the
     transverse state, still has to be checked.
   - Ideal memory and detectors.
   - 1D.
   - Asymptotic exponents (with a finite-N check at one a0).
   - The classical family is DI centroiding plus one fixed single-photon receiver (SPADE or a learned 6-mode).
     Fully adaptive multi-stage classical receivers are not excluded, though each test photon carries at most
     unit centroid information.

**Novelty status: not yet checked.**
- Known: weak Schur sampling robust to misalignment for ESTIMATION (de Almeida et al. 2110.00986), and the
  pair/HOM version (X5).
- Unchecked:
  - hypothesis-testing studies of misalignment (Grace-Guha 2022; Zanforlin et al. 2022; Lupo-group crosstalk
    papers);
  - the universal calibration curve F(kappa) and its logarithmic tail;
  - the group-size crossovers.
- A literature check is required before any claim.

## Novelty update for sections 14-16 (2026-11-07; research/space/novelty_qx/NOVELTY_VERDICTS.md, sweeps N1-N3)

This supersedes the novelty-status lines of sections 15 and 16.

- **Section 16 (QX3-E).**
  - Known:
    - the near-zero-background log law, which is exactly Schlichtholz et al. 2303.02654 Eq. (5) for crosstalk.
      The mechanism in point 1 should cite it, not claim it.
    - that a fixed offset removes SPADE's zero-background property, and the reflection confusability (Kariya
      2605.14432).
    - discrimination under known misalignment (de Almeida et al. 2003.01166).
    - weak Schur sampling robust to misalignment, for ESTIMATION (de Almeida-Lewenstein-Skotiniotis
      2110.00986).
  - Not found:
    - the universal calibration curve F(kappa) for a centroid learned from photons, and its exponent-optimal
      split;
    - the symmetric-projection test for one-vs-two DISCRIMINATION with its exponent ((k-1)/k) a0^2;
    - the 1.6-5.7x comparison and the group-size crossovers.
  - Partly known: the reference-photon variant (programmable discriminators; reference-photon interference for
    estimation, 2412.10057).
- **Section 15 (QX3).**
  - Known: the constant asymptotic joint-vs-Gaussian-measure-first gap for coherent-state templates
    (Sentis-Guta-Adesso 1410.8700; ratio alpha0-dependent, > 2 at some points).
  - Not found:
    - the imaging/pointing instance;
    - the constant 1.184 and its separation-independence;
    - the dark-port mechanism;
    - plug-in near-optimality.
- **Section 14 (QX2).** Not re-searched. It is a negative result.
- **Still to read before any submission:** full texts of Kariya 2605.14432 and de Almeida et al. 2003.01166 (the
  closest overlaps for S17), and Zanforlin et al. 2202.09406.

**Correction (2026-11-08) to section 15, row P2:** for n >= 16 the ratio E_MFDI/E_COH is 1.161-1.188, not 1.153-1.188. The value 1.153 is the n = 8 point; this was found when the paper's prediction table was generated from the JSON. The verdict (confirmed) is unchanged.
