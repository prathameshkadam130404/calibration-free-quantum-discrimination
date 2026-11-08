# Quantum-limited classification of sub-diffraction scenes under unknown nuisances
## Plan, idea round, hypotheses and pre-registration (written 2026-11-07, BEFORE any computation)

This is direction 1 of `research/LIT_SURVEY_SPACE.md` §7, chosen by the user. It is a separate project from
the Earth-observation paper.

### 1. Model (standard; Tsang, Nair, Lu, PRX 2016)

- **Sources and PSF.** We use a 1D image plane and a Gaussian amplitude PSF ψ(x) ∝ exp(−x²/4σ²), so the
  intensity PSF is N(0, σ²). Sources are weak and incoherent, with brightness-weighted position
  distribution μ. Each detected photon is an independent sample.
- **Photon state.** Each photon is in the state ρ_μ = ∫ μ(dX) |ψ_X⟩⟨ψ_X|, where
  ⟨HG_n|ψ_X⟩ = e^{−a²/2} aⁿ/√n! and a = X/2σ.
- **Direct imaging (DI).** DI samples p_μ(x) = ∫ μ(dX) N(x; X, σ²). We call any classifier that
  operates on DI positions a *detect-first learner*. It may use unlimited computation and know all models.
- **SPADE.** SPADE counts photons in HG modes centred on the estimated centroid. The *quantum optimum* is
  any measurement, collective across photons included, bounded through the root fidelity
  F = ‖√ρ0 √ρ1‖₁.
- **Error exponents and photon numbers.** Per-photon distinguishability is the squared Hellinger distance
  H² = 1 − BC (BC is the Bhattacharyya coefficient) for a measurement, and 1 − F for the quantum optimum.
  The minimax over nuisances uses the least favourable nuisance (the maximum BC or F over the H0 family).
  For N photons, P_err ≥ BC^{2N}/4 and P_err ≤ BC^N/2, and likewise with F for the quantum optimum.
  Hence the photons needed for error δ satisfy N ≍ log(1/δ)/H².

### 2. Idea round (divergent; 32 ideas from 9 fields; most will die)

1. [quantum metrology] Unknown nuisances that match low moments push the leading signal to higher
   moments. Under DI each higher moment costs (d/σ)⁴ per order and under SPADE (d/σ)², so the quantum
   advantage *grows* with the number of nuisances. → **H-S2/S3**
2. [quantum optics] Fast pointing jitter turns a point source into a Gaussian mixture of displaced modes.
   Its HG populations are a Poisson mixture with P₂/P₁² = 3/2, against 1/2 for a binary. → the test
   statistic for **H-S2**
3. [astronomy] An unresolved stellar disc of unknown size acts as the same nuisance (uniform or semicircle
   spread; kurtosis 1.8 or 2 vs the binary's 1). → **H-S3**
4. [exoplanets] Faint companion vs single source with unknown centroid *and* jitter: the first two moments
   are matched, so the companion shows only in the 3rd and 4th moments. HG populations are blind to odd
   moments, yet the 4th moment is linear in ε. → **H-S4**
5. [quantum information] Sign-sensitive ports (HG_n ± HG_{n+1}) read the 3rd moment through coherences.
   Do they beat HG populations under the H-S4 nuisance? → measured by the quantum optimum in H-S4
6. [statistics] Minimax composite testing: a GLRT over the nuisance attains the least-favourable
   exponent. → the learner used in **H-S5**
7. [machine learning] A generic trained classifier (logistic regression on mode counts or on histogram
   moments) should reach the GLRT's photon complexity. → **H-S5** variant
8. [quantum optics] Crosstalk adds an order-zero background to every port. When the leakage is unknown it
   destroys SPADE's information on the matching moment. → **later stage (E)**
9. [control / coronagraphy] Learn the sorter correction from calibration photons ("dark-hole digging" for
   mode sorters); does M ≈ σ²/d² calibration photons restore the d⁻² scaling? → later stage (E)
10. [learning theory] Calibration–test photon trade-off: total photon complexity, with labels coming from
    known calibration stars. → later (E)
11. [space-domain awareness] Satellite plus debris at sub-diffraction separation under tracking jitter
    maps onto H-S4 with ε = brightness ratio. → application of H-S4
12. [astronomy] Spectroscopic binaries vs a single star with unknown rotation broadening: the same
    structure in the spectral domain (time-frequency mode sorting). → later
13. [atmospheric optics] Slow jitter (per frame) is removable by re-centring; only fast jitter
    (photon-rate × coherence time ≪ 1) acts as the per-photon nuisance. → stated as the scope condition
14. [signal processing] Kurtosis-based binary detection in speckle/lucky imaging is the classical
    analogue of the DI side. → novelty check
15. [quantum Fisher information] Multiparameter: estimate separation with unknown spread; the QFI matrix
    is singular at the matched point. → later
16. [information geometry] The least-favourable nuisance is the information projection of the binary onto
    the H0 family. → used in the computation
17. [quantum hypothesis testing] Quantum Chernoff vs root-fidelity bounds: same scaling exponent. → used
18. [photonics] A programmable MPLC implements HG and sign-sensitive ports. → implementation note
19. [statistics] Unequal brightness plus unknown spread: does the companion's 4th moment always survive?
    → H-S4
20. [quantum optics] A 2D PSF with anisotropic jitter has more nuisance parameters, so a larger
    predicted exponent. → later
21. [astronomy] Partially resolved stars (optimal modes; arXiv:2607.02065). → related work
22. [random processes] Non-Gaussian jitter (e.g. a uniform or wind-shake sinusoid) changes the constants,
    not the exponents. → robustness check in H-S3
23. [learning theory] Label complexity of learning the classifier when σ is only known approximately.
    → later
24. [statistical physics] A Poisson mixture over a jitter distribution is a "compound Poisson" problem;
    deconvolution limits. → background
25. [coding theory] Mode ports as a code; choosing which ports to sort under a fixed budget. → later
26. [quantum networks] Two-telescope versions: does nuisance amplification also hold for interferometric
    baselines? → later
27. [photon counting] Dark counts set a floor on P₂ ~ a⁴ signals; up to what dark-count rate does H-S2
    survive? → later (needed before any experiment)
28. [astronomy] Stellar-disc-vs-binary classification is a real problem: unresolved binaries masquerading
    as single stars. → motivation
29. [ML] Learned mode sorters trained on photon counts (diffractive networks). → related work
30. [quantum information] Collective measurements across photons cannot beat the per-photon fidelity
    bound by more than a constant in the exponent. → used for the lower bound
31. [statistics] Equivalence (TOST) on fitted exponents. → analysis rule
32. [systems] End-to-end comparison against the best coronagraph plus post-processing (S-G2). → later

### 3. Hypotheses and predictions (pre-registered)

Notation: a₀ = d/4σ. Exponent k means H² ∝ a₀^k (photon complexity ∝ a₀^{−k}). Fits use log–log regression
over a₀ ∈ [0.02, 0.1] (d/σ ∈ [0.08, 0.4]), where leading-order asymptotics should hold.

- **H-S1 (sanity; known point vs equal binary; known result, Lu et al. 2018).** Exponents: DI 4, SPADE 2,
  quantum 2. Leading constants from my expansion: DI H² ≈ a₀⁴; SPADE H² ≈ a₀²/2.
- **H-S2 (Gaussian-jitter nuisance, unknown variance; binary separation known).** Exponents: DI 8,
  SPADE 4, quantum 4. Constants from my expansion: DI H² ≈ 5.3 a₀⁸; SPADE H² ≈ 0.134 a₀⁴.
  Consequence: the advantage ratio N_DI/N_SPADE grows from ∝ a₀⁻² to ∝ a₀⁻⁴.
- **H-S3 (finite-disc nuisance; uniform and semicircle spread of unknown radius).** Exponents: DI 8,
  SPADE 4, quantum 4. The constants are smaller than in H-S2, because these spreads are closer to the
  binary in kurtosis.
- **H-S4 (faint companion ε vs single source with unknown centroid and unknown jitter).** Exponents in a₀:
  DI 6, SPADE 4, quantum 4. Exponents in ε at fixed a₀: DI 2, SPADE 1, quantum 1. If the quantum exponent
  in a₀ is below 4, a sign-sensitive measurement beats HG-SPADE, and we record which one.
- **H-S5 (finite-N learners, Monte Carlo of sufficient statistics).**
  - Learners: GLRT on binned DI counts, and GLRT on HG-mode counts (nuisance fitted by maximum
    likelihood); also a logistic-regression learner trained on labelled simulated scenes.
  - Measured: the photons needed for 90 % balanced accuracy at d/σ ∈ {0.2, 0.3, 0.4, 0.6, 0.8}.
  - Predicted slope of log(N_DI/N_SPADE) against log(σ/d): about 4 with the jitter nuisance and about 2
    without, each within ±1.

**Refutation criteria (fixed now):**
- A fitted exponent that differs from its prediction by more than 0.3 refutes that prediction. I will
  then report the measured exponent and correct the theory.
- A quantum exponent below the SPADE exponent means HG-SPADE is not optimal in scaling; the claim
  "SPADE is optimal" is then dropped.
- In H-S5, a slope outside the ±1 bands refutes the finite-N translation.

**Scope conditions stated in advance:** 1D; Gaussian PSF; fast jitter (independent per photon); no
crosstalk and no dark counts (both are later stages); equal-brightness binary except in H-S4.

### 4. What would be new (to be settled by the novelty check, not assumed)

The candidate contribution:
- unknown nuisances that match low moments raise the exponent of the quantum advantage, with matching
  lower bounds for every detect-first learner;
- the faint-companion version under jitter.

Known and not claimed: the no-nuisance one-vs-two result (Lu et al. 2018); the moment-scaling theory
(Tsang; Zhou & Jiang). The novelty check is running; its verdict will be recorded here before any claim
is made.

---
## Addendum A (2026-11-07, after pre-registration commit a4a713d; the text above is unchanged)

**Novelty check (research/space/novelty_check_2026-11-07.md, sonnet sweep; key papers read at abstract or HTML level).**
- C1 PARTLY KNOWN. The exponents follow from known moment-estimation limits: Tsang arXiv:1806.02781 Eqs. 34-35;
  Zhou & Jiang arXiv:1801.02917 Sec. VIII; semiparametric treatment of unknown lower moments in Tsang
  arXiv:1906.04578 and 2010.03518. Not found: the testing formulation (single source with unknown spread vs
  binary), the minimax over the nuisance, an explicit advantage-exponent statement, and the P_n values.
- C2 PARTLY KNOWN. Odd moments need adjacent-mode superpositions (Zhou & Jiang Eqs. 57-60). The composite
  centroid + jitter problem was not found.
- C3 MOSTLY NEW. Closest work: Triggiani & Lupo arXiv:2509.03511 Sec. IV.4.1 (point vs extended source at the
  covariance level; SPADE optimal only under compatibility conditions; nuisances listed as future work).
- Only SPADE paper with random displacement noise: Sakuldee & Rudnicki arXiv:2407.01995 (estimation, not
  testing).
=> We do NOT claim the exponents as new. Candidate new content is the constants, the (non-)optimality of
HG-SPADE, the optimal measurement, and the composite companion problem.

**Exact leading order (derived 2026-11-07).** For any symmetric spread family with kurtosis K and finite sixth
moment, against an equal binary, with a0 = d/(4 sigma), minimised over the unknown scale:
- quantum 1 - F = (K-1) a0^4 / 4 + O(a0^6). This is exact (sympy series of F = e^{-a0^2/2}(sqrt E[e^{-a^2}
  cosh^2(a a0)] + sqrt E[e^{-a^2} sinh^2(a a0)]), valid for every symmetric spread). The least favourable
  scale matches the second moment.
- HG-SPADE H^2 = (sqrt K - 1)^2 a0^4 / 4 (hand derivation; the n = 1 term is nulled by an O(a0^2) scale shift).
- DI H^2 = (4/3)(K-1)^2 a0^8 (Edgeworth, chi^2 = Delta kappa_4^2 / 24).
- So HG-SPADE loses a factor (sqrt K + 1)/(sqrt K - 1) in photons: 2 + sqrt 3 = 3.73 for Gaussian jitter,
  6.85 for a uniform disc. The factor diverges as K -> 1.
- A "binary-nulling" measurement attains the quantum value at leading order: rotate span{HG0, HG2} so that
  one port is the binary's own even mode; the orthogonal port 2' is dark under H1. Its port-2' probability
  under H0 is (K-1) tau^2 / 2. With d unknown the rotation can be set from the measured P1 (two-stage).
- Advantage ratios: N_DI/N_Q = 48 sigma^4 / ((K-1) d^4) with the nuisance, against 8 sigma^2 / d^2 for a known
  point. For d = 0.1 sigma that is 2.4e5 against 800.
- Smoke-test agreement (a0 = 0.05): Gaussian quantum 3.099e-6 vs 3.125e-6 predicted; SPADE 8.335e-7 vs
  8.375e-7; uniform quantum 1.247e-6 vs 1.25e-6; uniform SPADE 1.823e-7 vs 1.825e-7.

---
## Addendum B (2026-11-07): pre-registration of the noise model E1, written BEFORE s03 exists

**Models.**
- **Dark counts:** a rate r per detector port per signal photon. The port probabilities become
  p'_j = (p_j + r)/(1 + M r), with M = 7 ports: HG0..HG5 (or their nulling-rotated version) plus one remainder
  port.
- **DI background:** a uniform density r per sigma over a field of [-6 sigma, 6 sigma].
- **Coherent crosstalk:**
  - The sorter measures rows of U·B instead of B, where B is the HG or nulling basis.
  - U = expm(eta·A), with A a random real antisymmetric matrix (N(0,1) entries above the diagonal, 5 seeds).
  - U is KNOWN to the learner: it is in the likelihood, as after calibration, but it is not undone
    optically.
- **Scenario:** H-S2 (Gaussian jitter, unknown width) vs the equal binary. The nuisance is least favourable
  per receiver.
- **Grids:** a0 in geomspace(0.02, 0.2, 10); r in {1e-6, 1e-5, 1e-4, 1e-3}; eta in {1e-3, 3e-3, 1e-2, 3e-2}.

**Predictions** (leading order; B = background probability in the signal port):

| ID | Prediction | Tolerance |
|---|---|---|
| E1-P1 | NULL and SPADE under dark counts follow H2 = 1/2 (sqrt(B + Delta) - sqrt(B))^2, with Delta = (K-1) tau^2/2 for NULL. The local exponent in a0 moves from 4 (a0^4 >> B) to 8 (a0^4 << B). | per point, factor 1.5 for NULL with B = r; SPADE may differ by its constant |
| E1-P2 | The photon advantage N_DI/N_NULL saturates at 3/(128 B) in the background-limited regime (about 234 at B = 1e-4, 23 at B = 1e-3), independent of K. | factor 2 |
| E1-P3 | DI is essentially unchanged by background density r <= 1e-3 per sigma. | H2 within 10 % of noiseless |
| E1-P4 | Known coherent crosstalk acts like a background B_xt = c·eta^2 with c = O(1) (leakage of HG0 into the signal port). | crossover at a0^4 ~ eta^2 and saturated advantage ~ 3/(128 c eta^2); fitted c in [0.1, 10] |
| E1-P5 (finite N) | At r = 1e-4, NULL-GLRT and DI-GLRT photon numbers for 90 % accuracy at d/sigma in {0.2, 0.4, 0.8} give ratios within a factor 2 of the exact-H2 ratios. | factor 2 |

**Refutation:** any prediction outside its stated tolerance is reported as refuted, with the measured
behaviour.

**Not covered here (later):**
- E1d: UNKNOWN crosstalk calibrated from M point-source photons, and active optical compensation (the
  learning-to-measure question).
- Background light that enters the sorter as an optical mode (rather than as detector dark counts).

---
## Addendum C (2026-11-07): pre-registration of E1d, learning-to-measure by calibrated optical nulling, written BEFORE s04 exists

**Device.**
- The sorter implements U_err · R(theta) · B_null.
- U_err = expm(eta·A) is an unknown, static crosstalk unitary (A random real antisymmetric, 5 seeds), with
  eta in {0.01, 0.03}, i.e. about -38 dB and -28 dB of leakage.
- R(theta) is one programmable rotation mixing the binary-even port and the nulled port 2'.

**Calibration (the learning step).**
- The calibrator is an on-axis point source (HG0), sent through the same optics with M photons, split over
  2 rounds × 2 probe settings (theta_c ± delta).
- The port-2' amplitude is estimated by pairwise probing: alpha_hat = (n+ − n−) / (4 g delta · M/4). The
  slope g comes from the ideal design.
- theta is set so that the calibrator's port-2' amplitude equals its ideal design value. That is the
  condition making port 2' dark for the binary.

**Test.**
- After calibration, the H-S2 test (Gaussian jitter of unknown width vs the equal binary) is run on the
  calibrated device.
- The per-photon H2 uses the least-favourable width. Test photons are N_test = 1/H2, a conversion validated
  by s02: N90·H2 = 0.97-0.99.
- **Optimistic assumption, stated now:** the learner knows the calibrated device for the likelihood, e.g.
  via bright-light tomography. What remains is the shot noise of the residual leakage, which knowledge
  cannot remove.

**Cost.**
- Faint-reference regime (calibration photons as expensive as science photons):
  N_total(M) = M + N_test(M), minimised over M on geomspace(1e2, 1e11, 37); 40 calibration runs per point
  (median).
- Bright-reference regime: calibration photons are free.
- Incoherent floor: b_inc in {0, 1e-6}, added as dark counts in all ports.
- Separations: a0 in {0.025, 0.035, 0.05, 0.07, 0.1} (d = 0.1-0.4 sigma).

**Predictions.**
- **E1d-P1:** residual dark-port background after calibration, B_res, has median ≈ 1/(8M) (one real
  amplitude, shot-noise-limited). Tolerance: median(B_res)·M in [1/32, 1/2] for M where 1/(8M) exceeds the
  systematic floor (≈ eta² a0⁴).
- **E1d-P2:** with b_inc = 0, the optimal faint-reference total N_total* scales as (sigma/d)^k with k in
  [3.5, 4.5] over d = 0.1-0.4 sigma, for both eta. The uncalibrated known-crosstalk device has k ≈ 8 in its
  saturated regime.
- **E1d-P3:** N_total* / N_null(noiseless) in [1, 4]. Calibration costs at most a small constant factor.
- **E1d-P4:** bright-reference regime: N_test / N_null(noiseless) <= 1.2 once M ≥ 100/Delta.
- **E1d-P5:** with b_inc = 1e-6, the advantage over DI again caps at ≈ 3/(128 b_inc) ≈ 2.3e4, within a
  factor 2, at the smallest d.

**Refutation:** outside the stated tolerance means refuted, and it is reported as such.

**Not covered here:**
- drift of U_err during the run;
- a centroid or pointing error of the calibrator;
- learner ignorance of U_err in the test likelihood;
- 2D;
- crosstalk that leaks the odd mode, which needs an off-axis calibrator and a second control. The design
  check found it 10^5-fold below the even leakage for this crosstalk model.

---
## Addendum D (2026-11-07): outcome of E1d (one control), diagnosis, and pre-registration of E1d-2 (two controls), written BEFORE the two-control code

**E1d outcome** (s04_calibration.py, one control; results/s04_calibration/calibration.json):

| Prediction | Result | Verdict |
|---|---|---|
| P1 | median B_res·M = 0.26-0.28 | confirmed |
| P2 | slopes 4.16 / 4.38; uncalibrated 7.98 | confirmed |
| P3 | N*/N_ideal = 1.15-4.02 (eta = 0.01), 2.2-13.5 (eta = 0.03) | REFUTED (the eta = 0.01 maximum sits just outside the bound) |
| P4 | bright-reference N_test/N_ideal up to 2.8 (eta = 0.01), 12.6 (eta = 0.03) | REFUTED |
| P5 | advantage 2.0e4 / 1.8e4 vs cap 2.34e4 | confirmed |

**Diagnosis** (bright calibration, M = 1e12):
- The residual even-mode leakage is 1e-12 to 1e-8.
- The residual odd-mode leakage, which an on-axis calibrator cannot see, reaches up to 1.0e-6. That is
  2.6× the signal Delta at a0 = 0.025 for eta = 0.03, seed 4.
- It scales as a0²·eta_1², not a0⁴, so it dominates at small d.
- The Addendum C design check had used seed 0 only, which happens to have small odd leakage. That check was
  wrong to generalise.

**E1d-2 design.**
- A second control theta_2 rotates the HG1 port (row 1) into port 2'.
- Two extra calibrators: point sources displaced to +x_c and -x_c, with a_c = x_c/(2 sigma) = 0.5.
- The difference of their port-2' amplitudes isolates <w2|HG1> (odd part only). Each amplitude is
  estimated by pairwise probing on theta_2, using design slopes ±a_c e^{-a_c²/2}.
- theta_2 is set so that <w2|HG1> = 0.
- Budget M: on-axis M/2, and M/4 for each displaced calibrator. Two rounds, alternating the controls.

**Predictions for E1d-2** (same grids and tolerances as Addendum C):
- P2' slope k in [3.5, 4.5] (b_inc = 0).
- P3' N*/N_ideal in [1, 4] for both eta.
- P4' bright-reference N_test/N_ideal ≤ 1.2.
- P5' unchanged.
- P1' median B_res·M in [1/32, 1/2]. B_res now counts even + odd leakage. The on-axis share is M/2, so the
  expected value is about 2× that of E1d.

---
## Addendum E (2026-11-07): pre-registration of X1-X5, written BEFORE any X code exists
Design source: research/space/RESEARCH_2D_ENTANGLEMENT_SAR.md section 8. All quantities are exact per-photon
(or per-pair) distinguishabilities.
- H² is the squared Hellinger distance.
- −log BC is the Bhattacharyya exponent.
- 1 − F uses the root fidelity.
- Each receiver gets its least-favourable nuisance unless stated otherwise.
- sigma = 1; a0 = d/4 for binaries.
- Exponent fits are log-log over a0 ∈ [0.02, 0.1] unless stated otherwise.
- Refutation: outside the stated tolerance = refuted, and reported as such.

**X1 (2D).** Binary along x.
- P1a. Isotropic Gaussian spread on H0 only: quantum 1 − F = 0.25 a0² (within 10 % at a0 = 0.02); exponent
  2 ± 0.3. TriSPADE H² / quantum ≥ 0.9 (optimal). DI exponent 4 ± 0.3.
- P1b. Anisotropic Gaussian, variance ratio rho ∈ {0.1, 0.01, 1e-3, 1e-4}: quantum 1 − F within 15 % of
  rho a0²/(2(1+rho)) + 0.5 a0⁴ at every grid point. The fourth-order term dominates once rho < a0².
- P1c. Isotropic uniform disc (2D): quantum 1 − F = 0.25 a0² within 10 % at a0 = 0.02; the shape enters only at
  higher order.
- P1d. Instrumental isotropic Gaussian jitter on BOTH hypotheses (H1 jitter s1 fixed in
  {0.05, 0.1, 0.2, 0.4}; H0 width free):
  - the quantum local exponent is ≈ 2 where a0 ≫ s1/2;
  - it rises toward 4 where a0 ≪ s1/2;
  - the coefficient decreases monotonically in s1.
  - Tolerance: local exponent ≥ 3.3 at a0 = 0.02 for s1 = 0.4, and ≤ 2.7 at a0 = 0.1 for s1 = 0.05.
- P1e. 1D line-like jitter on BOTH hypotheses (s1 ∈ {0.05, 0.1, 0.2}, H0 width free):
  - the quantum-vs-DI exponent gap shrinks;
  - at a0 ≤ s1/6 the local exponents of quantum and DI differ by ≤ 1.5;
  - with s1 = 0 we recover 4 vs 8.

**X2 (2D matched-covariance scenes).**
- P2a. H1 = square of 4 equal sources at (±r, 0), (0, ±r), vs an isotropic Gaussian spread or a uniform disc
  (size free); a0 := r/2:
  - quantum exponent 4 ± 0.3;
  - DI exponent 8 ± 0.5;
  - 2D-HG population exponent 4 ± 0.3.
  - Support projection: rho1's eigenbasis as ports, with the remainder in one port. It attains ≥ 0.9 of quantum
    1 − F at a0 = 0.02.
- P2b (exploratory; prediction stated). H1 = equilateral triangle (radius r):
  - the third moment differs, so quantum exponent 3 ± 0.3 and DI 6 ± 0.5;
  - HG populations, being blind to odd moments, have exponent 4 ± 0.3.

**X3 (spectral doublet, 1D).** H0 = symmetric line-shape family with free width.
- P3a. Student-t with nu = 10 (K = 4) and nu = 30 (K = 3.23):
  - quantum 1 − F = (K − 1) a0⁴/4 and HG H² = (sqrt K − 1)² a0⁴/4, each within 10 % at a0 = 0.02.
- P3b (exploratory). nu = 5 and 6, where the sixth moment is infinite or borderline: exponents within [3.5, 4.5].
- P3c. Voigt truncated to |x| ≤ 6 × scale, Lorentzian fraction f ∈ {0.1, 0.3, 1}:
  - quantum and HG follow the K formulas with the effective (truncated) K, within 15 %;
  - HG/quantum ≥ 0.5 whenever the effective K ≥ 10.

**X4 (collective vs single-copy, fast nuisance).** Quantum Chernoff exponent (QCB) vs the measurement's
classical Chernoff exponent (both minimised over the nuisance).
- P4a. 1D H-S2 nulling: ratio ≥ 0.95 at a0 ≤ 0.05.
- P4b. 2D isotropic TriSPADE: ratio ≥ 0.95 at a0 ≤ 0.05.
- P4c. 1D companion (eps = 0.03, a0 = 0.05), at the quantum least-favourable nuisance:
  - an optimised single-copy projective measurement over the first 6 modes reaches ≥ 0.9 of the QCB;
  - so collective measurements are not needed there either.

**X5 (two photons sharing a slow common-mode jitter X ~ N(0, s_j²); optional differential jitter s_delta per
photon; crosstalk U applied to both; memory asymmetry M applied to photon 1 only).**
- P5a. Antisymmetric (HOM) probability:
  - H1 = (1 − e^{−4 a0²})/4 and H0 = 0 exactly (≤ 1e-10), for every s_j and every common U.
- P5b. Differential jitter background under H0: P_anti = (1 − (1 + s_delta²)^{-1/2})/2, the exact Gaussian
  average, within 5 %.
- P5c. Memory asymmetry eps (amplitude) gives an H0 background c·eps² with c ∈ [0.1, 10].
- P5d. Per photon (−log BC per pair / 2) for d ≤ 0.4:
  - with s_j ≥ d, HOM exceeds the best of {SPADE-pair, nulling-pair, DI-pair} by ≥ 2×;
  - with s_j = 0, single-photon SPADE beats HOM by ≈ 2× (within [1.5, 3]).
- P5e. The crossover jitter s_j*, where HOM equals the best local pair strategy, lies within a factor 2 of d/2.
- P5f. Frames of k = 4 and 8 photons, with nulling ports on each photon and full classical processing:
  - the per-photon exponent grows with k;
  - but stays below HOM's per-photon exponent at s_j = 2d (d = 0.2).
- P5g. The quantum pair bound (−log F_pair) is ≤ 2× HOM's −log BC per pair, so HOM is near-optimal for pairs.

**Not covered:**
- Airy PSF;
- crosstalk in 2D sorters (beyond X5's common U);
- a PPT/separable SDP bound;
- finite-N simulations for X1-X4.

---
## Addendum F (2026-11-07): pre-registration of QX1 (learned quantum receivers), written BEFORE any QX1 code exists

Design source: research/space/QML_RESEARCH.md, section 6.

**Receiver model.** A trainable real orthogonal map (Naimark isometry) acts on the first M = 8 HG modes:
- the modes are padded with A ancilla vacuum modes (A = 0 gives a projective measurement; A = 4 gives a
  POVM with M + A outcomes);
- one remainder port collects HG modes ≥ M;
- photon counting follows in every output port.

**Cases** (1D, sigma = 1, a0 = d/4):
- (a) H-S2: binary vs a single source with unknown Gaussian jitter (width free);
- (b) line jitter on BOTH hypotheses, s1 = 0.05 (H0 width free);
- (c) faint companion, eps = 0.03, with unknown centroid AND jitter.
- Separations a0 ∈ {0.05, 0.1}.

**QX1-A (model-based training, nuisance in the loss).**
- Loss: maximise the minimax per-photon Bhattacharyya exponent, min over a nuisance grid of
  −log Σ_j sqrt(p1_j p0_j(nu)).
- Method: Adam with 8 restarts (one from the HG identity, seven random).
- Exact evaluation afterwards: Chernoff and Bhattacharyya exponents, minimised over the nuisance with a fine
  grid plus refinement.
- Predictions:
  - QX1-A1: (a) learned ≥ 0.95 of the nulling receiver's minimax exponent, and the learned port vectors
    contain a vector with overlap ≥ 0.9 with the nulled port 2' (rediscovery of nulling).
  - QX1-A2: (b) learned ≥ 0.95 of the nulling receiver (nulling is not exactly optimal once H1 is jittered,
    so learned may exceed it).
  - QX1-A3: (c) projective learned (A = 0) Chernoff exponent in [0.90, 0.97] of the QCB at the same
    least-favourable nuisance; POVM learned (A = 4) ≥ projective, with gain ≤ 3 % of the QCB.

**QX1-B (data-driven, in situ).**
- The learner never sees port probabilities, only photon counts.
- Training set: case (a), a0 = 0.1. One H1 scene plus K = 5 H0 scenes with unknown jitter u ~ U[0.8, 1.2]
  (not labelled with u).
- Each SPSA step re-measures the scenes with T photons per scene at the two perturbed settings. The objective
  is the empirical minimax Bhattacharyya exponent over the K H0 scenes.
- 300 steps. Total training photons = 300 × 2 × 6 × T, reported.
- Prediction QX1-B1: the exact minimax exponent of the final receiver, relative to the QX1-A optimum, rises
  monotonically with T ∈ {1e5, 1e6, 1e7, 1e8} and is ≥ 0.9 at T = 1e8.

**QX1-C (robustness to unknown coherent crosstalk).** Case (a), a0 = 0.1. The device applies U_err =
expm(0.03 A_rand) after the learned map.
- Predictions:
  - QX1-C1: the nominal-trained receiver tested on the crosstalk device keeps ≤ 0.3 of the crosstalk-free
    optimum (background-limited).
  - QX1-C2: model-based retraining with the crosstalk device known gives ≥ 0.9, since a unitary error can
    be undone.
  - QX1-C3: data-driven in-situ training on the crosstalk device (T = 1e8) gives ≥ 0.8.

**Refutation:** outside the stated range = refuted, and reported as such.

**Not covered:** drift during training; complex (phase) modes; 2D; finite-N accuracy curves (exponents only).

---
## Addendum G (2026-11-07): pre-registration of QX1-R, reference-assisted learning, written BEFORE any QX1-R code exists

**Motivation (QX1-B / C3 refuted).** Learning from faint science photons failed. The training signal (port
changes ~a0⁴) is shot-noise buried, needing ~1/a0⁸ photons per gradient. Two further suspected faults:
- the SPSA perturbation (0.05 rad) is ~7× larger than the optimal rotation (~0.007 rad);
- each step uses a single perturbation draw.

QX1-R trains on BRIGHT laboratory reference scenes instead: internal calibration sources sent through the same
optics, where photons are cheap. The task is case (a), a0 = 0.1, as in QX1-B/C. The evaluation is the exact
minimax Bhattacharyya exponent on the science task, relative to the model-based optimum (QX1-A, a|0.1|A0).

**R1: data-driven learning on bright references of both classes**, i.e. a reference binary at the target
separation plus K = 5 reference single sources with emulated jitter u ~ U[0.8, 1.2].
- Learner: tuned SPSA (perturbation c = 0.003 rad, gradient averaged over 4 perturbation draws, 600 steps,
  start from HG). The objective is the empirical minimax Bhattacharyya exponent over the K references.
- Reference photons per scene per evaluation: T ∈ {1e8, 1e10, 1e12}.
- Run on two devices: crosstalk-free, and the QX1-C crosstalk device (U_err = expm(0.03 A_rand), unknown).
- Predictions:
  - QX1-R1a: the ratio rises with T on both devices;
  - QX1-R1b: ≥ 0.8 at T = 1e10 and ≥ 0.9 at T = 1e12.

**R2: null-digging on a bright reference binary under unknown crosstalk.**
- Start from the model-based nominal receiver. The device is U_err @ W(theta).
- The learner minimises only the empirical count fraction in the receiver's dark port (the output with the
  smallest nominal H1 probability) under a reference binary at the target separation.
- Method: SPSA (c = 0.003, 2 perturbation draws, 300 steps), with T ∈ {1e6, 1e8, 1e10} photons per
  evaluation.
- Predictions:
  - QX1-R2a: the science-task ratio is ≥ 0.9 at T = 1e10 and increases with T;
  - QX1-R2b: the residual dark-port probability under H1 falls with total reference photons M. The fitted
    log-log slope vs M is between −1.5 and −0.5 (shot-noise-limited, as in E1d).

**Refutation:** outside the stated ranges = refuted, and reported as such.

**Not covered:** drift between calibration and science; references at a different separation than the science
target; the companion case.

---
## Addendum H (2026-11-07): pre-registration of QX2 and QX3, written BEFORE any QX2/QX3 code exists

Design source: QML_RESEARCH.md section 6 (draft), refined by the derivations below, which were done on paper
before any code. 1D, sigma = 1, binary separation d, a0 = d/4. A point source at x is the coherent state
|x/2> of the HG oscillator, with amplitude overlap <x|y> = exp(-(x - y)^2 / 8).

### QX2: translation-invariant vs U(m)-invariant two-photon measurements (route R3-subgroup)

**Setting** (as X5):
- two photons per frame share a slow common jitter X ~ N(0, sj^2), independent across frames;
- a static unknown crosstalk U = expm(eps (A_k - A_k^T)) acts on HG modes 0..12 of each photon after the
  jitter, with A_k an upper-triangular standard-normal matrix (seeds 1000 + k, k = 0, 1, 2);
- H0: point source; H1: equal binary.
- Grid: d in {0.1, 0.2, 0.4, 1.0}; sj in {0, 0.1, 0.2, 0.4, 0.8};
  eps in {0, 1e-4, 3e-4, 1e-3, 3e-3, 0.01, 0.03, 0.1}.

**Derivation, recorded as the prediction basis.**
- In centre-of-mass / relative coordinates (a 50:50 transform of the two HG oscillators), the jitter enters
  only the centre-of-mass mode.
- Every translation-invariant POVM is block-diagonal in total momentum. Total momentum has the same
  distribution under H0 and H1 and is independent of the relative state. So the optimal translation-invariant
  measurement is the optimal measurement on the reduced relative state:
  - H0: pure |phi0>;
  - H1: (1/2)|phi0><phi0| + (1/4)(|phi_d><phi_d| + |phi_-d><phi_-d|), with |<phi0|phi_d>|^2 = e^{-d^2/8}.
- Its optimum is the projection onto phi0 (the relative-coordinate HG0, i.e. the states v_j = sum_m
  sqrt(C(j,m)) 2^{-j/2} |m, j-m>). The click probability under H1 is q_T = (1 - e^{-d^2/8})/2, against
  HOM's q_H = (1 - e^{-d^2/4})/4.
- Pair states commute with SWAP, so every optimal two-photon measurement refines HOM {antisym, sym}.

**Measurements.**
- M1: HOM.
- M2: coarse translation-invariant {rel0, not rel0}.
- M3: refined {antisym, sym minus rel0, rel0}.
- Q_pair: the exact optimal pair Bhattacharyya exponent -log F, computed from a coherent-state Gram matrix;
  it is invariant under U.
- L: a learned projective measurement in the symmetric subspace, plus the antisym outcome. The pair space is
  the triangle m + n <= 18, with an exact remainder outcome. Training is model-based (Adam plus an L-BFGS
  soft-min polish, as in QX1-A), in two variants:
  - (i) per instrument state, with the nuisance known;
  - (ii) minimax over a 50-state box: sj grid x {eps = 0} union {eps in {0.01, 0.03, 0.1}} x {k = 0, 1, 2}.
  - Ancilla variants A in {0, 8}.

**Predictions.**
- QX2-P1: at eps = 0, M3 = -(1/2) log(1 - q_T) for every sj (relative error <= 1e-6). The M3/HOM exponent
  ratio is <= 1.011 for d <= 0.4 and in [1.05, 1.08] at d = 1.
- QX2-P2: Q_pair/M3 decreases with sj; at sj = 0.8, Q_pair/M3 <= 1.15 for d <= 0.4.
- QX2-P3: M2 falls below HOM at some eps* <= 0.01, for every d <= 0.4, every k and sj in {0, 0.4}.
- QX2-P4: M3 >= HOM at every state (exact by Cauchy-Schwarz; a code check). At eps = 0.1, (M3/HOM - 1)
  <= 0.2 x its eps = 0 value.
- QX2-P5: L(i) with A = 0 reaches >= 0.99 of Q_pair at (sj, eps) in {(0, 0), (0.2, 0), (0.2, 0.03)},
  for d in {0.2, 0.4}.
- QX2-P6: L(ii) minimax / HOM is in [1.00, 1.10] for d in {0.2, 0.4}; the A = 8 gain over A = 0 is <= 2 %.

### QX3: learn-then-classify from labelled reference photons (route R1)

**Setting.**
- An unknown static pointing offset theta ~ N(0, tau^2) is common to everything.
- The learner gets n labelled reference photons from a point source at theta (a PSF/pointing calibrator),
  then ONE test photon, from H0 (point at theta) or H1 (binary of known d centred at theta), with equal
  priors.
- Metric: Bayes error P; excess risk E = P - P_KNOWN; recovered fraction (1/2 - P)/(1/2 - P_KNOWN).
- Grid: a0 in {0.05, 0.1, 0.2}; tau in {0.2, 0.5}; n in {0, 1, 2, 4, 8, 16, 32, 64, 128}.

**Strategies, all exact.**
- KNOWN: theta known. NONE: n = 0.
- COH: the joint Helstrom optimum on references plus test.
  - Exact reduction: |theta>^{(x)n} is unitarily equivalent to the collective coherent state |sqrt(n) theta/2>.
  - The reference space is represented by an eigenbasis (PCA) of its weighted Gram matrix. theta is on a
    uniform grid; convergence is checked with K -> 2K and with the PCA threshold.
- MF-DI: direct imaging of the references, then the Bayes-optimal test measurement. The posterior is
  N(m, v) with v = 1/(n + 1/tau^2); by translation invariance P depends on v only.
- PLUG: theta-hat = the posterior mean, then the known-theta Helstrom measurement.
- MF-SPADE: references counted in HG modes centred on the nominal axis. The sufficient statistic is
  S ~ Poisson(n theta^2/4), which loses the sign of theta. Then the Bayes-optimal test measurement.
- SYM: (n+1)-photon symmetric projection. Its closed form gives P = 1/2 - (n/(n+1))(1 - e^{-d^2/16})/2.
  Zero H0 background for any theta.

**Predictions.**
- QX3-P1 (sanity): E_COH <= E_MFDI <= E_PLUG and E_COH <= E_SPADE at every point.
- QX3-P2: E_MFDI/E_COH <= 1.2 for n >= 16, at every (a0, tau): measure-first suffices, as for qubits.
- QX3-P3: at n = 64, E_MFDI/E_COH varies by < 10 % across a0 at fixed tau, i.e. no gap that grows below the
  Rayleigh limit.
- QX3-P4: E_PLUG/E_MFDI is in [1.5, 3] for n >= 16.
- QX3-P5: E_SPADE/E_MFDI >= 5 at n = 128 for tau = 0.5 (the sign ambiguity makes it plateau).
- QX3-P6: E_MFDI x (n + 1/tau^2) is constant within +-15 % over n in [16, 128] (excess proportional to the
  residual pointing variance).
- QX3-P7: n90, the smallest grid n at which MF-DI recovers >= 90 % of the KNOWN advantage, is the same for all
  a0 at fixed tau, within one grid step. For single-copy error the reference cost does not scale with
  (sigma/d).

**Refutation:** outside the stated ranges = refuted, and reported as such.

**Not covered:**
- many-test-photon error exponents for QX3, where the residual offset must satisfy v << a0^2, so the cost
  would scale with (sigma/d)^2;
- data-driven training for QX2;
- 2D;
- bosonic indistinguishability beyond the two-photon symmetric/antisymmetric structure;
- the quantum memory needed by COH, SYM and all of QX2.

---
## Addendum I (2026-11-07): pre-registration of QX3-E (many-test-photon exponents), written BEFORE any QX3-E code exists

Follow-up to QX3 point 4: the single-copy metric hid the H0-background cost.

**Setting.**
- A static unknown pointing offset theta is shared by everything (flat prior).
- N test photons from one hypothesis: H0 a point at theta, H1 an equal binary (known d, a0 = d/4) centred at
  theta.
- Optionally kappa N labelled reference photons from a point source at theta.
- Metric: the error exponent per test photon, E = lim -(1/N) log P_err, reported as a fraction of a0^2.
- Grid: a0 in {0.05, 0.1, 0.2}.

**Derivation, recorded as the prediction basis.**
- Known theta: the QCB for pure vs mixed is -log <psi|rho1|psi> = a0^2 exactly, and the null test attains it.
- Q-SCHUR_k (stored test photons, no references): project groups of k test photons onto the symmetric subspace.
  - H0 never leaves it, for any theta and any static crosstalk.
  - Under H1, P(sym) = h_k(lambda1, lambda2), with lambda = (1 +- e^{-2 a0^2})/2.
  - E_k = -(1/k) log h_k, about ((k-1)/k) a0^2; E_inf = -log lambda1.
- Q-REF_kappa: each test photon is projected onto the symmetric subspace jointly with kappa fresh references
  (integer kappa). E = -log(1 - kappa (1 - e^{-a0^2})/(kappa + 1)).
- Classical, measure-first:
  - References plus a fraction f of the test photons are measured by direct imaging (centroid). The residual
    offset t has large-deviation rate g(t) = (kappa + f) t^2/2 per test photon.
  - The remaining (1 - f) N test photons are measured with a single-photon receiver at the estimate.
  - Exponent: E(kappa, f) = min over (t0, t1) of max over s in [0, 1] of
    [s g(t0) + (1-s) g(t1) - (1-f) log sum_j p0_j(t0)^s p1_j(t1)^{1-s}], then maximised over f.
  - C-SPADE: HG0..HG5 plus a rest port.
  - C-LEARN: a learned real orthogonal 6-mode receiver plus a rest port, trained to maximise this exponent
    (Powell, starting from SPADE).
- Leading-order estimate: the offset puts an H0 background u a0^2 into the port that carries the H1 signal a0^2.
  The Poisson Chernoff exponent h(u) of a zero-background test falls fast and only logarithmically slowly
  recovers as u -> 0, so E/a0^2 ~ min over u of [2(kappa + f) u + (1 - f) h(u)].
  - Rough values: 0.22 (kappa = 0), 0.42 (1), 0.59 (10), 0.67 (100), 0.72 (1000).
  - No single-photon receiver escapes this: every port with a second-order H1 signal has a second-order offset
    background, and the test photons carry at most unit centroid information per photon.

**Predictions.**
- QE1 (closed-form code check): Q-SCHUR_inf/a0^2 >= 0.98 for a0 <= 0.2; Q-SCHUR_k/a0^2 within 3 % of (k-1)/k
  for k in {2, 3, 4, 8, 16}, a0 <= 0.1.
- QE2: C-SPADE/a0^2 (best f) is
  - in [0.15, 0.30] at kappa = 0;
  - in [0.35, 0.50] at kappa = 1;
  - in [0.50, 0.67] at kappa = 10;
  - in [0.60, 0.75] at kappa = 100;
  - < 0.85 at kappa = 1000;
  - and varies by < 10 % between a0 = 0.05 and 0.1 at each kappa.
  - Grid: kappa in {0, 0.1, 0.3, 1, 3, 10, 30, 100, 1000}.
- QE3: C-LEARN <= 1.1 x C-SPADE at kappa in {0, 1, 10, 100} (a0 in {0.05, 0.1}).
- QE4: Q-SCHUR_inf / C-SPADE >= 3 at kappa = 0 and >= 1.3 at kappa = 100; HOM pairs (k = 2) beat C-SPADE at
  every kappa <= 1.
- QE5: Q-REF_kappa / C-SPADE(kappa) >= 1.1 for kappa in {1, 3, 10, 30, 100} (using the same references coherently
  beats measuring them).
- QE6 (finite-N check, exact):
  - Case: a0 = 0.1, kappa in {1, 10}, f = 0, a 3-cell SPADE receiver {HG0, HG1, HG>=2} at the DI estimate.
  - The exact Bayes error (Gaussian quadrature over the residual offset, full multinomial sum) for N up to
    8000 has a local exponent that approaches the large-deviation exponent of the same receiver monotonically,
    and is within 30 % of it at the largest N.

**Refutation:** outside the stated ranges = refuted, and reported as such.

**Not covered:**
- crosstalk (it would only add classical background; Schur sampling is immune);
- the photon-number cost of the quantum memory;
- 2D;
- joint coherent strategies beyond Q-SCHUR and Q-REF;
- classical receivers beyond 6 modes.
