# Paper plan: calibration-free discrimination of unresolved sources (target: PRA Regular Article)

Rules: STYLE_AND_VENUE.md. Evidence: research/CLAIMS_LEDGER.md (S15-S17d) and research/space/RESULTS.md
(sections 14-16). Novelty: research/space/novelty_qx/NOVELTY_VERDICTS.md.

## Identity sentence
When the pointing of a telescope is unknown, any measure-first learner that decides "one star or a close binary"
must calibrate the pointing and stays background-limited. Projecting stored photons onto their symmetric subspace
needs no calibration and reaches 98-99.9 % of the known-pointing quantum limit.

## Working title
Calibration-free quantum discrimination of unresolved sources: symmetric projection versus pointing calibration

## Claims (each mapped to ledger rows)
1. **C1 (S17, classical side).**
   - Measure-first learners reach only a universal, separation-independent fraction F(kappa) of the
     known-pointing exponent a0^2: 0.17-0.20 (no calibration) up to 0.69 (1000 calibration photons per test
     photon).
   - Mechanism: background from residual pointing error, with the known log law (Schlichtholz et al.).
   - New: the curve and its exponent-optimal split.
2. **C2 (S17, quantum side).** Symmetric projection of k stored test photons:
   - has zero H0 background for any pointing and static crosstalk, and an exponent ((k-1)/k) a0^2 tending to
     0.98-0.999 a0^2;
   - gives a 1.6-5.7x advantage over C1;
   - needs k = 4 to beat 1000 calibration photons per test photon;
   - and spending the same references coherently beats measuring them by 1.5-1.7x.
3. **C3 (S16, one test photon).**
   - Joint learning keeps a constant 18 % excess-risk advantage (ratio 1.184).
   - Mechanism: a port dark under H0 for every pointing.
   - Plug-in is within 0.8 % of Bayes, and sign-blind calibration is useless.
   - The constant-gap phenomenon itself is known for coherent states (Sentis-Guta-Adesso).
- **Supporting negative result (S15):** translation invariance buys only ~d^2/16 over HOM, so the full
  permutation symmetry used in C2 is the right invariance.

## Outline (claim-first headings)
I. Introduction.
- Problem: one-vs-two discrimination below the Rayleigh limit.
- Prior work: optimality of aligned SPADE; fragility to misalignment and crosstalk; known-misalignment
  corrections; weak Schur sampling for estimation.
- The gap: testing with an unknown pointing that must be learned.
- Contributions C1-C3.

II. Setting: one-versus-two testing with an unknown pointing.
- Model, coherent-state picture and figure of merit (exponent per test photon).
- Known-pointing benchmark: QCB = a0^2, attained by the null test.

III. Measure-first learners stay background-limited for any calibration budget.
- The large-deviation exponent formula; receivers (direct-imaging centroiding, SPADE, learned 6-mode receivers).
- The curve F(kappa), the optimal split and the mechanism.
- Exact finite-N check.
- Takeaway.

IV. Symmetric projection removes the calibration problem.
- Exponent h_k, invariance and group sizes.
- Coherent use of references (Q-REF).
- Comparison (Table I, Fig. 1).
- Takeaway.

V. With one test photon, joint learning keeps a constant 18 % advantage.
- Exact reduction to a collective mode; ratio 1.184; the dark-port mechanism; plug-in; sign-blind calibration.
- Takeaway.

VI. Translation invariance alone buys almost nothing.
- 2/(1 + e^{-d^2/8}); fragility under crosstalk; learned HOM refinements.
- Takeaway.

VII. Discussion: implementation (memory, multiport interference), limitations, outlook.

Appendices.
- A: large-deviation exponent.
- B: symmetric-projection probabilities.
- C: collective-mode reduction.
- D: numerics and checks.
- E: pre-registered predictions, outcomes and fixed faults.

Back matter.
- Data Availability Statement: code and data DOI still TODO (Zenodo).
- AI-use disclosure (mandatory).
- Acknowledgments.

## Figures and tables
| Item | Content | Source |
|---|---|---|
| Fig. 1 | exponent fraction vs kappa: C-SPADE curve, learned point at kappa = 0, Q-SCHUR_k lines, Q-REF curve | results/qx3e/qx3e.json |
| Fig. 2 | exact finite-N error vs N (kappa = 1, 10) vs symmetric projection | qx3e.json finite_N |
| Fig. 3 | single-photon excess-risk ratio vs n | results/qx3/qx3.json |
| Table I | exponent fractions by kappa (generated) | qx3e.json |
| Table II | translation-invariant vs HOM vs pair bound (generated) | results/qx2/qx2.json |

## Status
- 2026-11-08: plan, style, REVTeX skeleton, generated tables; sections I-VII drafted.
- 2026-11-08: Figures 1-3 generated (gen_figures.py, validated colour-blind-safe palette).
  - Appendices A-E written in appendix.tex, with the pre-registration table generated from JSON.
  - Clean build, 10 pages.
  - Generating the tables caught a transcription error in RESULTS s.15 P2 (1.153 -> 1.161), now corrected.
- 2026-11-08: introduction rewritten after the results; text compressed from 4,755 to about 3,730 words (-22 %);
  bullet lists turned into prose where PRA style expects it.
  - From submission/sn-article.tex: the four authors, the affiliation, the corresponding e-mail, "no external
    funding", and the code repository.
  - The data availability statement cites the repository (QKrepo).
  - The S12 memory tolerances were added to the Discussion.
  - 9 pages, clean build.
- 2026-11-08: AI-use statement completed with the lead author's own statement (P. B. Kadam directed all of the
  work and verified and checked all calculations by hand).
  - The project moved to its own repository, prathameshkadam130404/calibration-free-quantum-discrimination
    (private on creation), which the Data Availability Statement now cites.
  - Clean build, 9 pages, no TODOs.
- 2026-11-08: repository made public, so the "openly available" statement holds.
- Before submission (human):
  - Optionally mint a Zenodo DOI, which APS prefers.
  - Confirm the co-author list.
