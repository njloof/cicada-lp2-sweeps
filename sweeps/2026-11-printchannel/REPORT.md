# Campaign #32 REPORT — print channels wave 1 (MAP F25)

**VERDICT: PARTIAL-COVERAGE-FLAGGED** (registered rule, PREREG §5 + §1b
escalation, applied verbatim; coverage 74.41% ∈ [70, 95) ⇒ prefix).
FLAGGED = flag-for-oracle: owner adjudication required before ANY
claim. Post-hoc diagnostics (below) identify the glyph-morphology main
effect as the leading explanation for BOTH flags.

## 1. Mandate

External-review Track B wave 1: machine-measured print channels —
does HOW runes were placed depend on WHAT was written? Language-
agnostic. dukotah R44 left sub-2-pixel placement and kerning
unexcluded by their own wording.

## 2. Data and gates

- **G0 PASS 56/56**: onion JPEGs (Internet Archive
  `ky2khlqdf7qdznac.onion`) sha1-EXACT vs dukotah
  `analysis/stego/provenance.json`, byte-exact precondition met
  (`acquire.py`, receipt results/acquire_receipt.json on studio).
- **G1 FAIL→PARTIAL band: 9,640 / 12,956 = 74.41%** unsolved runes
  aligned on clean lines (439 lines, 54 pages). Failure classes
  (per-page table `results/coverage32.json`): faded/header lines with
  genuinely missing ink (p0 l0, p40 l0, p15 l1), ornament-contaminated
  grid page (p15, 28% covered), off-by-one merged/extra-mark lines.
  Registered escalation §1b applies: tests run on the aligned subset
  (permutation null valid on any subset; plants calibrated on the SAME
  subset), verdict carries PARTIAL-COVERAGE- prefix.
- **G2 PASS, worst deviation 0 (registered tol 1e-6)**, 66 runes on 3
  random lines, naive pixel-loop re-implementation. G2 caught TWO real
  defects pre-verdict: (i) nearest-ink heuristic picked a stave
  fragment inside a ring glyph's hole; (ii) comp mode had silently
  ignored the §1b-registered FRAGMENT merge. Both fixed; no test ran
  under either.
- **G3 PASS**: core.validate ALL GATES (local — needs ibotpeaches
  images; sub-2-min gate, local allowed).

## 3. Engineering iterations (pre-output, disclosed; #26 precedent)

Calibration v1–v9 (calib32*.py) touched ONLY line rune-counts — never
values, never a statistic. Findings: y-projection bands merge lines
(inter-line ink bridges); dilation-merge fails (kerning ≈ fragment
gaps); narrow solid bars (h≈114, w≈9) are standalone stave runes
(count arithmetic, calib32f); low-h fragments belong to neighbours;
edge marginalia are wide AND sparse (density ≤ 0.25); glyph height is
114–115 px corpus-wide (uniform print — no per-page scale needed).
Registered in PREREG addendum §1b committed BEFORE any campaign output
(c83ede6).

## 4. Results (tests32.json; seed 20261232; studio)

| quantity | value |
|---|---|
| aligned runes / lines / pages | 9,640 / 439 / 54 |
| T1_obs (max eta², metric **area**) | **0.8455** |
| T1 null (within-line value-permutation, D=2,000) median / c95 | 0.0041 / 0.0053 |
| p_T1 | **5.0e-4** (= 1/2001, floor: no null draw reached T_obs) |
| T2: R / n | 0.0478 / 9,640 |
| p_T2 analytic / MC-cross-check | **2.7e-10** / 0 (of 20,000) |
| plant(i) power eps .02/.05/.10/.20 | 1.0 / 1.0 / 1.0 / 1.0 |
| plant(ii) power jitter .1/.3/1.0 | 0.6 / **0.05** / 0.0 |
| detectability gates | T1 PASS (power 1.0 ≥ 0.95 at eps 0.10); **T2 FAIL** (power 0.05 < 0.95 at jitter 0.3) |

min(p) = p_T1 ≤ 0.025 ⇒ FLAGGED per §5 verbatim. Note T1_obs is ~160×
the null c95 — far beyond the plant grid's reach (plants demonstrate
sensitivity, not scale). T2's plant gate failed exactly as the
lattice-sum algebra predicts: with near-uniform value frequencies the
registered plant(ii) class (frac(cx)=(v/29+jitter·U) mod 1) has ~zero
resultant regardless of jitter — T2 is UNPOWERED against that class;
its flag must not be read as "powered-and-significant".

## 5. POST-HOC confound diagnostics (run AFTER verdict; disclosed; do
not alter the registered verdict)

Both flags are dominated by the **glyph-morphology main effect**: the
value selects the glyph, and the glyph has its own print signature —
no channel required.

- Per-value WITHIN-LINE coefficient of variation: **area 0.0215
  (median)**, **w 0.0000, h 0.0000** — each rune value is printed as a
  fixed glyph whose ink area is determined to ~2% (JPEG noise level).
  eta²(area | value) = 0.85 is exactly this triviality. Placement
  metrics are NOT value-determined: gap CV 0.57, fx CV 0.27.
- frac(cx) is near-deterministic PER VALUE (per-value resultant
  0.8–0.9 for most values): the centroid's fractional part is a
  glyph-shape fingerprint against integer-ish typeset character cells.
  The global Rayleigh R=0.048 is the mixture of 29 fixed per-value
  fracs — morphology again, not a sub-pixel placement code.
- The T1 metric set (area/w/h/density) was registered before it was
  known that w/h are constant per value; the design flaw is
  disclosed: value→glyph→size is a confound the within-line
  permutation null does NOT remove (it permutes values across
  different glyphs, destroying the glyph-level noise structure that
  the observed statistic is made of).

## 6. Interpretation and next step (oracle decides)

The instrument works (G2 exact, plants sensitive, alignment audited).
What wave 1 measured and flagged is, on the leading reading, "the
same rune is always printed the same way" — typography, not encoding.
**Wave-1b proposal** (new PREREG, cheap, reuses the table): residualize
each metric by value (subtract per-value within-line mean), then test
whether the RESIDUAL placement of a rune depends on context
(neighbour values, line position) under a within-line, within-value
permutation null. That is the test that actually asks "does the print
encode the value beyond glyph identity". Also: PNG-source confirmation
before ANY sub-pixel interpretation (PREREG §6.1 was written for
exactly this).

## 7. Disclosures

1. JPEG lossy (PREREG §6.1): a FLAGGED needs PNG confirmation before
   interpretation — standing.
2. Coverage 74.41% < 95%: prefix travels with the verdict; excluded
   lines are faded-ink/ornament lines, not value-selective (count-gate
   failures); per-page table disclosed.
3. plant(i) injection is deterministic — the 20 draws/cell are
   degenerate (power ∈ {0,1}); registered grid applied as written.
4. plant(i) metric = argmax of T1_obs (registered in addendum; chosen
   from observed data).
5. T2 MC cross-check uses the large-n Exp(1) tail of n·R² (matches
   analytic to 0/20,000 exceedances).
6. Full table stays on studio (work/table32.jsonl, sha256
   `ff11c6c99d52b77037201d2fa5f396c4f65ce0cb5dddf63b303919284424b7c1`);
   repo carries only small receipts
   (coverage32.json, tests32.json) — repo-hygiene rule. Regeneration:
   `scripts/studio.sh run sweeps/2026-11-printchannel/table32.py` then
   `...tests32.py` (seed 20261232, host-independent streams).

## 8. ADDENDUM 2026-11-20 (owner adjudication package)

Full-page rendering (figs/p0_coverage.jpg) corrected one coverage
attribution: **p0 l0 and p15 l0 are RED-INK printed headers**, excluded
by the registered red-ink rule (redness < 45) — a policy cost, not
faded-ink loss; p15 l1 is a red/black MIXED line (red glyphs dropped →
undercount → gate fail). Revised failure taxonomy for the 25.6%
unaligned: red-ink/mixed lines (policy), ornament-contaminated grid
page (p15), off-by-one merged/extra-mark lines, and genuinely faded
runs (p40 l0, p49/p53 tails). Adjudication ask + figures:
ADJUDICATION.md. Figures regenerate via `mk_adj_fig32.py` (full pages,
never crops, owner policy 2026-11-17).
