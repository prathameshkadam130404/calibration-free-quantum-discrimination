# Format, venue norms and writing rules for the calibration-free discrimination paper (checked 2026-11-08)

## 1. Target venue and format

**Target: Physical Review A, Regular Article** (Quantum information / quantum optics). The reasons:
- free subscription route, no mandatory charges (research/VENUE.md);
- the closest prior work is there (de Almeida et al., PRA 103, 022406 (2021); PRA 112, 052605 (2025));
- no length limit for Regular Articles.

**Fallback:** Quantum Science and Technology (IOP; any format at submission; policies in research/VENUE.md).
Excluded by the no-APC rule: PRX Quantum, PRX Intelligence, Phys. Rev. Research, Optica Quantum, npj QI,
Quantum.

### PRA rules (official pages, read 2026-11-08)

| Item | Rule | Source |
|---|---|---|
| Article type | Regular Article: no length limit. Letter: 4,500 words (~5 pages in REVTeX). | journals.aps.org/pra/authors; journals.aps.org/authors/length-guide |
| Source format | A PDF is enough for review. LaTeX preferred, with REVTeX 4.2 (apstemplate.tex) and the journal option `pra`. | pra/authors; length-guide |
| Abstract | One self-contained paragraph; summarise subjects, results and conclusions; no displayed equations or tables; no numbered references; no coined words or unexplained acronyms; about 5 % of the article and < 500 words. | journals.aps.org/authors/style-basics |
| References | PRA encourages titles for all references. | pra/authors |
| Data availability | A Data Availability Statement is REQUIRED (submissions from 11 Dec 2024). Public data and code must be cited in the reference list with a persistent identifier (DOI preferred; Zenodo etc.). Supplemental Material and personal websites are discouraged for data. | journals.aps.org/authors/data-availability-statements |
| AI use (policy updated June 2026) | AI cannot be an author. SUBSTANTIVE use must be disclosed in the paper, with the tool name and version, how it assisted, and how the authors directed and verified the output. Substantive use includes scientific reasoning, drafting claims, literature synthesis, derivations, code that affects results, simulations and data analysis. Research use goes in Methods; figure use in the caption; other use in the Acknowledgments. Light polishing need not be disclosed. | journals.aps.org/authors/appropriate-use-ai-tools; aps.org news 2026/06 |
| Language | American English. | pra/authors |
| Accessibility | Colour-blind-safe palettes; meaning carried by words or symbols, not colour alone. | pra/authors |
| Supplemental Material | The paper must stand alone. Derivations may go in appendices. | pra/authors |

**Consequence for this paper.** This research was carried out with substantial AI assistance (Claude):
derivations, code, simulations, literature sweeps and drafting. The AI-use disclosure is mandatory. The
accountable human author must complete the verification part, and must confirm or edit every claim.

## 2. Writing rules adopted, with the skill repositories they come from

Repositories read (2026-11-08):
- K-Dense-AI/scientific-agent-skills (skills/scientific-writing);
- SNL-UCSB/paper-writing-skill (SKILL.md, author_profile/editorial_principles.md);
- Orchestra-Research/AI-Research-SKILLs (20-ml-paper-writing/ml-paper-writing/references/writing-guide.md).

Also found but not read:
- Master-cai/Research-Paper-Writing-Skills (ML/CV oriented);
- google-deepmind/science-skills.

None of them ships an APS/REVTeX template; the official REVTeX 4.2 (MiKTeX) is used instead.

1. **No fabrication; evidence binding** (K-Dense).
   - Every number traces to a results JSON and every claim to a ledger row: research/CLAIMS_LEDGER.md S15-S17d
     and research/space/RESULTS.md sections 14-16.
   - Tables are generated from JSON by script, not typed by hand.
   - No invented references, DOIs, affiliations, funding or data DOIs: unknown items stay as visible TODOs.
2. **Report what failed** (K-Dense).
   - Refuted pre-registered predictions and fixed code faults go in an appendix.
   - Confirmatory (pre-registered) results are kept separate from exploratory and post-hoc ones.
3. **Problem first** (SNL principle 7): open with the astronomy and quantum-imaging problem, not with
   "quantum machine learning".
4. **One identity sentence, 1-3 falsifiable claims, front-loaded** (Orchestra / Nanda / Karpathy).
5. **Claim-first headings** (SNL principle 3): each section heading states its conclusion.
6. **A takeaway at the end of every results section** (SNL principle 8).
7. **Named over vague** (SNL principle 2): no "significant", "novel" or "promising"; name the measurement,
   the number and the regime.
8. **Old before new, stress position, subject-verb proximity** (Gopen-Swan, via Orchestra).
9. **Write comprehensively, then compress 30-50 %** (SNL principle 4). Rewrite the introduction after the
   results are final (SNL principle 1).
10. **Bound generalisability** (K-Dense): 1D, ideal memory, asymptotic exponents, the classical family tested.
