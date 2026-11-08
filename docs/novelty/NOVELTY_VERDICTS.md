# Novelty check for QX2, QX3 and QX3-E (claims S15-S17), 2026-11-07

**Sources.** Three retrieval sweeps (sonnet), with raw reports in this folder:
- N1: misalignment in one-vs-two hypothesis testing;
- N2: symmetric projection / purity testing / implementations;
- N3: coherent-state learning (full texts of 1410.8700, 1004.2468, 1208.0663).

Items I checked myself on arXiv abstract pages or text are marked **[me]**. "Not found" means not in the papers
read, which is not proof of absence. The unread items are listed at the end.

## 1. S17, QX3-E (many-photon testing under unknown pointing)

| Element | Verdict | Evidence |
|---|---|---|
| A zero-background null test is destroyed by any H0 background; the exponent recovers only as {1 - [ln ln q - 1]/ln q} x^2 | **KNOWN** | Schlichtholz, Linowski, Walschaers, Treps, Rudnicki, Sorelli, arXiv 2303.02654 (Optica Quantum 2023), Eq. (5) and (S12)-(S14), for crosstalk background **[me, text]**. Our h(u) law is the same function. Cite it; do not claim it. |
| A fixed pointing offset removes SPADE's zero-background property; the reflection branch where a binary looks like an offset point (s* = 2 theta) | **KNOWN** | Kariya, arXiv 2605.14432 (2026), singular-learning (Bayes free energy) framing **[me, abstract]**. This is our SPADE sign-confusability at t0 = d/2. |
| Discrimination error under KNOWN misalignment with corrective single-photon measurements | **KNOWN** | de Almeida, Kolodynski, Hirche, Lewenstein, Skotiniotis, arXiv 2003.01166 (PRA 103, 022406) **[me, abstract]** |
| Splitting light between direct imaging (centroid) and the sorter | **KNOWN for estimation** | Grace, Dutton, Ashok, Guha, arXiv 1908.01996 (JOSA A 2020), which minimises MSE (N1) |
| Universal, separation-independent calibration curve F(kappa) of the exponent vs calibration photons per signal photon, with the exponent-optimal split (f* = 0.41 at kappa = 0, 0 for kappa >= 1) | **NOT FOUND** | N1 |
| Symmetric-subspace (weak Schur) projection used for one-vs-two DISCRIMINATION, with zero background for any pointing and crosstalk; exponent ((k-1)/k) a0^2 -> -log lambda1 (0.98-0.999 of the known-centroid QCB) | **NOT FOUND** | The machinery is known for ESTIMATION: de Almeida, Lewenstein, Skotiniotis, arXiv 2110.00986 (PRA 112, 052605, 2025), robust to misalignment, with N = 2 = HOM **[me, abstract]**. HOM for super-resolution estimation: Parniak et al. 1803.07096. N2 found no hypothesis-testing treatment in two searches. |
| Reference-photon variant (each test photon symmetrised with kappa calibration photons) | **PARTLY KNOWN** | Programmable discriminators with symmetric projectors (Bergou-Hillery quant-ph/0504201, qubits). Reference-photon interference with a thermal-source photon for separation ESTIMATION: Muratore, Triggiani, Tamma, arXiv 2412.10057 **[me, abstract]**. |
| Quantum/classical comparison 1.6-5.7x in exponent; group-size crossovers (k = 2 beats up to ~3 references, k = 4 beats 1000, k = 8 beats 1e8) | **NOT FOUND** | N1, N2 |

**Positioning.** S17 is the hypothesis-testing counterpart of de Almeida et al. 2110.00986. It is combined with
the known fragility of the null test (Schlichtholz et al.; Kariya), now caused by a centroid that has to be LEARNED
from photons. What is new:
- the universal calibration curve;
- the zero-background symmetric-projection test with its exponent;
- the quantitative quantum-vs-classical learning comparison.

## 2. S16, QX3 (single-test-photon learn-then-classify)

| Element | Verdict | Evidence |
|---|---|---|
| A constant asymptotic gap (both excess risks ~ 1/n) between joint learning and Gaussian measure-first learning for coherent-state templates | **KNOWN (in principle)** | Sentis, Guta, Adesso, arXiv 1410.8700, EPJ QT 2015 **[me, text]**: a collective measurement gives lower excess risk than any Gaussian estimate-and-discriminate strategy. The ratio depends on alpha0 and is reported above 2 at some points (N3). The task there is vacuum vs |alpha> with alpha localised near a known alpha0. |
| Qubit contrast (measure-first optimal; E&D a factor 2 worse) | **KNOWN** | Sentis et al. 1208.0663; Guta-Kotlowski 1004.2468 (N3, full text) |
| The imaging/pointing instance (both hypotheses depend on theta), the value 1.184 and its independence of the separation | **NOT FOUND** | N3 (search level for 2016-2026) |
| The dark-port interference mechanism (test photon interfered with the collective reference mode, dark under H0 for every theta) | **NOT FOUND** | not in 1410.8700 (beam splitters only concentrate the training copies) |
| Plug-in within 0.8 % of Bayes | **NOT FOUND**; contrasts with the qubit results, where E&D is a factor 2 worse | N3 |

**Correction to RESULTS s.15 point 1.** "Coherent learning keeps a constant advantage, unlike for qubits" stays
true. But the constant-gap phenomenon for coherent-state templates is already known (SGA 2015); only the
imaging instance, its constant and the mechanism are new.

## 3. S15, QX2 (subgroup vs U(m) invariance)

Not re-searched here. N2 found no subgroup-invariance analysis. The status stays "not found, abstract level
(Q3 sweep)". It is a negative result in any case.

## 4. Residual gaps (unread)

- Full texts of: 2003.01166 (misalignment discrimination); Kariya 2605.14432 (PDF unreadable); Zanforlin et al.
  2202.09406; Stanisic-Turner 1806.01236; the Montanaro-de Wolf property-testing survey; O'Donnell-Wright
  1501.05028.
- The Sentis thesis 1407.4690 (coherent-state chapter).
- The tail of 2110.00986 (the agent read ~100k of 113k characters).
- Before submission, read Kariya and 2003.01166 in full: they are the closest classical-side overlaps for S17.

## 5. Full-text reading of the two closest papers (2026-11-08, read by me)

**Kariya, arXiv 2605.14432 (v3; HTML full text, sections I-V; appendices skimmed).**
- **Problem.** One source vs a WEAK companion (relative brightness eps, separation s); not the equal binary.
  The detector offset theta is "a fixed external parameter rather than a parameter endowed with a prior". It is
  never estimated from photons.
- **Tools.**
  - Singular learning theory: real log canonical thresholds and multiplicities of the Bayes free energy.
  - Aligned case: direct imaging and SPADE share lambda = 1/2 but differ in multiplicity.
  - Misaligned case: a binary-SPADE reduction (HG0 vs rest). Its KL information is ~ eps^2 s^4 against
    eps^2 s^2 for direct imaging, giving local power scales n^{-1/4} vs n^{-1/2}.
  - Finite-n Neyman-Pearson powers at eps = 0.3, theta = 0.1: direct imaging is stronger on the plotted grids,
    and binary SPADE has an exact blind separation s* = 2 theta.
- **What it does not contain.**
  - no Chernoff exponents and no calibration-photon budget, so no curve F(kappa);
  - no collective or symmetric measurements.
  - Its conclusion names "robust measurements or test statistics that preserve ... the aligned-SPADE advantage
    while avoiding structural blind spots" as FUTURE WORK. Our symmetric projection is such a measurement, for
    the equal binary.
- **Verdict.** Qualitative overlap only: misalignment destroys the zero-background advantage, and an offset
  creates a reflection blind spot. This is the same physics as our SPADE confusability (offset point at
  t0 = d/2 vs a centred binary), in a different model and framework.

**de Almeida, Kolodynski, Hirche, Lewenstein, Skotiniotis, arXiv 2003.01166 (PRA 103, 022406; ar5iv full text,
sections I-V and appendices A-C).**
- **Problem.** The EQUAL binary vs a single source, with a misaligned demultiplexer (offset delta, assumed
  KNOWN: "we take misalignment as experimental fact").
- **Tools.**
  - The qubit model (HG0, HG1): misalignment is a Bloch rotation, the separation lowers the purity (after
    Chrostowski et al. 2017).
  - ROTADE, a rotated two-mode measurement tailored to the known delta:
    - single-shot type-1 error ~ theta^6/576 against theta^2/4 for SPADE01;
    - a numerically optimised Chernoff exponent, up to 12 % better than SPADE01/B-SPADE.
  - All schemes reach the QCB at theta = 0, but the exponents are discontinuous as theta -> 0+ (the
    background effect).
- **What it does not contain.**
  - It explicitly does not learn the centroid. It cites Grace et al. 2020 for splitting photons between direct
    imaging and SPADE, and gives no exponent for that.
  - No collective measurements.
  - It leaves open discrimination when the two hypotheses' centres differ.
- **Verdict.** It confirms the known parts:
  - the background-induced discontinuity of the exponent;
  - single-photon corrective measurements, where ROTADE is equivalent to re-centring in the qubit picture and is
    therefore inside our classical family;
  - the purity view of the separation.
  - It does not contain the learned-calibration curve or the symmetric-projection test.

**Updated S17 verdict after full reading: unchanged.**
- Known:
  - the mechanism (Schlichtholz Eq. 5; de Almeida's exponent discontinuity; Kariya's blind spot);
  - the purity view (Chrostowski 2017; de Almeida 2020);
  - weak Schur sampling for estimation (2110.00986).
- Not found:
  - F(kappa) for a centroid learned from photons, and its exponent-optimal split;
  - the symmetric-projection DISCRIMINATION test with exponent ((k-1)/k) a0^2 -> -log lambda1;
  - the 1.6-5.7x quantum-vs-classical comparison;
  - the group-size crossovers.
- Both papers point to exactly this gap: Kariya names robust measurements as future work, and de Almeida et al.
  treat misalignment as known.

Remaining unread: Zanforlin et al. 2202.09406; the property-testing surveys; the Sentis thesis; the tail of
2110.00986.

## 6. Zanforlin et al., arXiv 2202.09406 (Nat. Commun. 2022), read by me in full (main text plus supplement sections VII-XI), 2026-11-08

- **Problem.** Star vs star plus a WEAK companion (relative intensity eps), in the asymmetric (Stein / relative
  entropy) setting.
- **Measurement and results.**
  - The receiver is a two-collector, two-mode interferometer (phase shift alpha, 50:50 beam splitter, photon
    counting). It saturates the quantum relative entropy, theta^2 k^2 eps d^2/4, which is linear in eps (DI is
    quadratic).
  - The same set-up estimates the separation of equal sources at the QCRB.
  - Experiment: pseudo-thermal pinholes at 1 m with a 5.3 mm baseline; 1.7 % accuracy at 15 um separation.
- **Pointing.** The optimal phase alpha (Eq. S17) depends on the source position x0. The supplement states
  explicitly that "this step assumes that we know the centre-of-mass of the two sources". There is no
  misalignment analysis. Interferometric phase stability uses multiplexed classical coherent reference pulses
  (calibration light, not stored quantum references).
- **Future work named in the paper:** "composite hypothesis testing".
- **Overlap with S17: NO** on the new elements:
  - no unknown or learned pointing;
  - no calibration-photon curve;
  - no collective or symmetric measurement;
  - a weak-companion model.
- **Relevance.** Its interferometer is another single-photon receiver whose optimal setting depends on the
  centroid. So the classical calibration limit of S17 applies to it too: an unknown x0 leaves a residual phase
  error, which becomes a background in the dark output. This strengthens the motivation for S17.

**S17 verdict after all three closest papers (Kariya, de Almeida 2020, Zanforlin) read in full: unchanged.**
Every prior one-vs-two test either assumes the centroid is known or treats a FIXED misalignment.
