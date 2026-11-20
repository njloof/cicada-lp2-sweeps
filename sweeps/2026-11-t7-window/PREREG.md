# Campaign #30 PREREG — T7 fixed-window rate-ratio certification (MAP F23)

Registered 2026-11-19, BEFORE any campaign output (CI gate). Owner
approval 2026-11-19 (verbatim): "Let's proceed with T7 certification...
we will get to the others soon enough."

## 0. Mandate

The external review's reopen condition for the T7 localization reading,
as recorded verbatim in #26's close (LEDGER row 26 / MAP F17):

> reopen requires fixed-window rate-ratio test (edges named in advance,
> no location search) — NEW campaign

and review round-5: **fixed-window edges must be independent of the 86
doublet locations**. Review r4 (C8) additionally accepted as the plant
spec for future F9 work: *leak-1/29 sensitivity plant ~1,650 runes,
D-stationary working model*. This campaign is that test, nothing more.

Surviving T7 statement to be tested: global gap lag-1 autocorrelation
+0.380 (p=0.0006, #10; X1 red-team p=0.00025), post-hoc twice on the
same 86 sites. The localization reading (a ~1,650-rune reduced-rate
window) was DEMOTED to recorded-only by review r4 because every
location-SEARCHING statistic (#26-A2 BIC lanes) failed with zero power.
This campaign replaces the search with a single pre-named window.

## 1. Objects (all registered before this campaign)

- Stream = pp00–55 book order, p50 skipped, 12,956 runes; doublet site =
  position p ∈ [0, 12954] with s[p] == s[p+1]; K = 86 sites (#10 census
  convention, gate G1).
- **Axis junction J = 3611.5** — midpoint between the last rune of p15
  line 0 and the first rune below p15's `&`/`$` lines. LAYOUT-derived
  (p15 starts at 3603, L0 = 9 runes ⇒ J = 3603 + 9 − 1 + 0.5). Pinned by
  #19 gate G4; recomputed from data here as gate G2 below. No doublet
  position enters its derivation.
- **Registered window W\* = {p : J − 825 ≤ p ≤ J + 825} = [2787, 4436]**
  — exactly 1,650 integer doublet sites centered on J. Width 1,650 = the
  reviewer's accepted sensitivity-plant scale; center = J. Both named in
  this document before any statistic is computed. No other window,
  width, center, or shift is registered for the verdict.

## 2. Honest-edge triage (design pass, pre-registration)

Requirement: edges independent of the 86 doublet locations.

- **J-centered window — ADOPTED.** Derivation is pure layout (line
  structure of p15). Selection lineage disclosed in §6.
- Void edges 2739/4388 — REJECTED: derived from the doublet gaps
  themselves; direct violation of the r5 constraint.
- Equal blocks (13 × 1,000) — REJECTED: already tested as #10 S1
  (block-χ², p=0.151); §E.2 forbids reruns without a stronger
  instrument, and this is the same information at lower resolution.
- SEGMENTS v2 Q1–Q7 decoration boundaries — REJECTED for this campaign:
  v2 lacks owner sign-off (gated), and #18 S2 showed the doublet
  deficit already tracks those groups (p=0.008) — the boundary source
  is not independent of the signal's magnitude. Kept as a separate lane
  pending v2 sign-off.
- Page-boundary-anchored windows, other landmarks — REJECTED: arbitrary
  choices; registering several would reinstate the location search this
  campaign exists to remove.

## 3. Registered statistic and nulls

**PRIMARY — X = |sites ∩ W\*|** (doublet sites inside W\*), one-sided
in the LOW direction (reduced rate inside the window).

- **N1 (primary null, #10-matched):** 86 sites uniform without
  replacement over [0, 12954] with hard-core gap ≥ 6 (the filter's
  constraint, #10 `draw_n1` transform), D = 10,000, seed 20261230,
  per-draw streams `rng_for("N1", d) = default_rng([SEED, crc32(tag) %
  100000, d])`. p = (1 + #(X_perm ≤ X_obs)) / (D + 1).
- **H (analytic sanity, reported alongside):** exact hypergeometric,
  N = 12,955 sites, K = 86, n = 1,650; p = P(X ≤ X_obs). Null mean
  10.95. Discrepancy between N1 and H p-values beyond a factor ~2 is
  reported as an instrument note (hard-core should only tighten
  dispersion).

No secondary statistic carries verdict weight. **±100-rune edge jitter
of W\* is computed REPORT-ONLY** (robustness disclosure; it cannot
change the verdict — the verdict is defined on W\* alone).

## 4. Power curve (F21 rule) and detectability gate

Plants at W\*: inhomogeneous hard-core draws (density ρ inside W\*, 1
outside, K = 86, greedy gap ≥ 6, #10 `draw_plant` mechanics), ρ ∈ {0,
0.25, 0.5, 0.75, 1.0}, 200 draws each, per-ρ critical value from the N1
draws at α = 0.05 (largest t with add-one P(X ≤ t) ≤ 0.05). Power(ρ) =
fraction of plant draws with X ≤ critical value.

- **Detectability gate:** power(ρ = 0) ≥ 0.99, else
  INSTRUMENT-FAIL (no verdict on real data).
- **Disclosure rule:** power(ρ = 0.5) is reported with the verdict; if
  < 0.8, any negative verdict is stated as *excluding void-class
  non-stationarity only*, never as "stationarity supported" (C8 wording
  adopted).

## 5. Kill gates (run before plants and statistic)

- **G1 census:** stream length 12,956; 86 doublet sites; min gap 6;
  per-1k block profile == [8,3,7,2,6,9,10,8,11,2,9,6,5]; Pearson gap
  ac1 == 0.3795 (±1e-3). Any mismatch ⇒ INSTRUMENT-INCOMPLETE, stop.
- **G2 junction:** J recomputed from page/line structure == 3611.5 ±
  0.5.
- **G3 null calibration:** fresh N1 draws reproduce #10's recorded ac1
  null mean/SD (−0.009 ± 0.104) within ±0.01 / ±0.01 (instrument
  lineage check, not a statistic).

## 6. Verdict rule (registered pre-output, applied verbatim)

- **CERTIFIED-NONSTATIONARY** — p(N1) ≤ 0.05. The reduced-rate window
  becomes a certified structural fact: the emission process was
  non-stationary at ~1,650-rune scale, centered on the p15 axis;
  mechanism classes (sessions / stateful loop / re-seeding) reopen with
  a named target.
- **LOCALIZATION-RETIRE** — p(N1) > 0.05. The localization reading is
  formally retired; T7 survives only as the global gap-ac1 correlation
  (recorded, unmechanized). This is the answer dukotah Round-45 needs
  either way.
- **INSTRUMENT-FAIL** — detectability gate fails; no verdict.

## 7. Disclosures (pre-output)

1. **Lineage / multiplicity.** This is the 5th look at the same 86
   sites (#10 discovery+replication, #18 S1, #19 V1/V1b, #26-A2, this).
   The window CENTER was selected because #19 found the void centered on
   J (that finding was demoted to recorded-only). The derivation of J is
   doublet-independent; the *selection* of J as landmark is
   void-motivated. Mitigations: the test was prescribed by the external
   review whose skepticism motivated the demotion; single window, single
   width, single direction, α = 0.05, no search; full lineage travels
   with any positive result.
2. Expectation: under the null E[X] = 10.95; the four void-internal
   sites already public (#19 §0: 2740/3140/3852/4389) put 3 of 4 inside
   W\* by inspection of published numbers. No new statistic has been
   computed as of this commit; X is computed only after gates + plants.
3. The D-stationary working model (constant leak) is the null by
   fiat of C8; N1's hardcore constraint is the filter-model plant
   requirement (F21) at site level — no re-emission simulation (the
   statistic depends on sites only; the filter's constraint is exactly
   the hardcore condition).
4. Verdict wording for CERTIFIED will NOT claim mechanism
   identification; it certifies non-stationarity at the named window.

## 8. Machinery

`t7w.py` (this dir): census/G1 reuse #10 conventions verbatim; N1 draw
= #10 `draw_n1`; plants = #10 `draw_plant` mechanics with window
indicator density. D=10,000 nulls + 5×200 plants — local, minutes, no
studio. Artifacts: results/t7w.json (small). Seed 20261230.
