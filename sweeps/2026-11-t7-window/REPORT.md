# Campaign #30 REPORT — T7 fixed-window certification: CERTIFIED-NONSTATIONARY

Registered before output: PREREG `d326090` (no statistic computed at
registration; gates + plants ran first). Owner approval 2026-11-19.
Local run (0.9 s), seed 20261230. Registered rule applied verbatim.

## Result

Single pre-named window W\* = [2787, 4436] — 1,650 doublet-site positions
centered on the layout-derived p15 axis junction J = 3611.5 (edges named
in advance; doublet-independent by derivation):

| quantity | value |
|---|---|
| X_obs (doublet sites in W\*) | **3** |
| N1 null (hard-core, D=10,000) | mean 10.95, sd 3.01, t_crit 5 (add-one P=0.026) |
| p (N1, one-sided low) | **0.00240** |
| p (exact hypergeometric sanity) | 0.00327 — consistent (ratio 1.36) |
| rate ratio | **0.274** (window emits ~27% of baseline doublet rate) |
| jitter robustness (report-only) | X = 3 for every edge shift −100…+100 |

**VERDICT: CERTIFIED-NONSTATIONARY** (p ≤ 0.05 registered rule). The
anti-doublet emission process ran at ~1/4 of its baseline rate through a
~1,650-rune window centered on the p15 decimals/∞ axis. This is the
programme's first certified positive structural finding about the LP2
emission process. Per PREREG §7.4: non-stationarity is certified at the
named window; mechanism is NOT identified (sessions / stateful loop /
re-seeding all remain open, now with a named target).

## Power curve (F21 — reported with the verdict)

Window plants (density ρ inside W\*, hard-core K=86, 200 each, α=0.05):

| ρ | 0 | 0.25 | 0.5 | 0.75 | 1.0 |
|---|---|---|---|---|---|
| power | 1.000 | 0.935 | 0.415 | 0.120 | 0.025 |

Detectability gate PASS (power(0)=1.0 ≥ 0.99); ρ=1 calibration 0.025 ≈ α.
The observed ratio 0.274 sits in the well-powered region (between ρ=0.25
and 0.5 plants, power ≈ 0.7 interpolated). Disclosure: power at ρ=0.5 is
0.415 < 0.8 — the test certifies strong deficits; a gentle (≤25%) rate
change would NOT have been detected, so the certified window's true rate
is bounded loosely above (~0.4 × baseline at the 200-plant scale).

## Gates

- **G1** census EXACT: 12,956 runes, 86 sites, min gap 6, block profile
  == #10 pin, ac1 = 0.3795.
- **G2** J recomputed from page/line structure == 3611.5 (p15 starts
  3603, L0 = 9 runes).
- **G3** N1 ac1 null −0.011 ± 0.103 vs #10 recorded −0.009 ± 0.104
  (instrument lineage intact).

## Lineage and multiplicity (PREREG §7, travels with this result)

1. 5th look at the same 86 sites (#10 discovery+replication, #18 S1,
   #19 V1/V1b, #26-A2, this). J's DERIVATION is layout-only; its
   SELECTION as window landmark is void-motivated (#19, demoted). The
   test itself was prescribed by the external review (reopen wording,
   LEDGER row 26) whose r4 demotion created it; single window, single
   width, single direction, α=0.05, no search.
2. Prior looks' p-values (#19 V1 0.0168 / V1b 0.0084) tested centering
   geometry; this campaign tests RATE directly — a different statistic,
   not a re-run. Cumulative look-count is disclosed; no combination rule
   is applied.
3. What CERTIFIED does and does not say: the emission was
   non-stationary at ~1,650-rune scale at the named window. It does NOT
   say the window is the only anomalous region (the equal-block test
   #10 S1 was non-significant), nor that the axis causes anything, nor
   any keying mechanism.

## Consequences

- Dukotah Round-45's target question gets an answer from an independent
  instrument: the non-stationarity is real at window scale (their X1
  gap-permutation p=0.00025 + our two independent statistics). Relay =
  owner decision, each time.
- Mechanism lanes reopen with a target: per-block/re-seeded keying
  models (Wulfic per-section-restart claim now testable against a named
  window — F18(ii) cross-ledger review is the cheap next step).
- T7's recorded-only demotion (C8) is superseded for the WINDOW claim
  only if the review accepts the lineage disclosure; wording here is
  "CERTIFIED per registered rule, lineage attached".

## Reproduction

    python3 sweeps/2026-11-t7-window/t7w.py

Tracked: results/t7w.json (small). Seed 20261230; streams
`default_rng([20261230, crc32(tag)%100000, d])`.
