# PREREG — Campaign #10: T7 replication (doublet slip-rate non-stationarity)

Date: 2026-11-16. Committed BEFORE any campaign output exists (CI gate).
Queue slot 1, owner-agreed 2026-11-16 ([MAP.md](../../docs/MAP.md) §G).
Charter: independent replication of dukotah **T7** — the only live anomaly in
`Dukotah/cicada-lp2-sweeps`'s sister ledger
(`sources/dukotah/liber-primus/analysis/round44/W2-B3-doublet-sites/`,
row `R44-W2B3-D01-FALSIFIER`, filed `measured`, never certified) — **plus
the instrument contribution their own RESULTS disclose as missing**: no
positive-control plant has ever exercised SMOOTH RATE HETEROGENEITY, the
structure class T7 actually found ("no plant class specifically exercised
SMOOTH rate heterogeneity … T7's power against its own alternative is not
separately measured"). Their Round-45 ask, verbatim: "an
ordering-sensitive registered statistic with a *smooth-heterogeneity*
plant". This campaign registers both.

Nothing here certifies or decertifies T7 as evidence of intent. It is a
statistical replication with independent code, independent null sampling,
registered statistics chosen for the alternative, and a measured power
curve. A replication is shareable upstream; posting requires explicit
owner approval at the time of posting.

## Premise census (pinned pre-output, kill-gate)

Object: our corpus unsolved stream — book pages 0–49 + 51–55 concatenated
in book order (p50 runeless), `data/pages/lp2_*.txt`, values 0–28.
L = 12,956. Site = adjacent equal pair `x[i]==x[i+1]`, position = index of
FIRST rune. Measured 2026-11-16, before any null or plant was generated:

- **86 sites**, 0 cross-page, 28 distinct doubled values, **min gap 6**,
  largest gaps 712/662/553/537.
- Per-1,000-rune block counts (13 blocks, last 956):
  **[8, 3, 7, 2, 6, 9, 10, 8, 11, 2, 9, 6, 5]**.
- Observed statistics: Pearson ac1(gaps) = **+0.3795**; Spearman
  ac1(gaps) = **+0.2678**; block-rate χ²(12 df) = **15.712**; runs over
  block signs = 8.
- **Cross-lineage check:** our (pos, gaps, vals) are BIT-IDENTICAL to their
  persisted `results.json real_sites_U86` — two pipelines, one object. The
  replication is therefore about statistics and nulls, not extraction.
- KILL GATE: if a future re-run of the census does not reproduce these
  numbers exactly (corpus sha `9f5f14d4…483e`), report INSTRUMENT-
  INCOMPLETE and stop.

Descriptive note (not a test): min gap 6 is itself unlikely under an
unconstrained uniform process (expected ≈ 5.7 pairs closer than 6); the
filter's own suppression physics is the parsimonious cause — which is why
the primary null below conditions on spacing (N1) and the unconstrained
null is kept for comparability (N2).

## Hypothesis

**H-rate**: the doublet slip RATE varies smoothly along the book
(block-scale), beyond flat-Bernoulli leakage at n=86.
Alternative under test = the D-01 flat model as instantiated by our nulls.
No channel hypothesis (theirs: NEGATIVE at power 1.00 — not re-run).

## Statistics (registered; exactly four, no post-hoc additions)

- **S1 (primary)** block-rate χ²: 13 blocks (12×1000 + tail 956), expected
  ∝ block size, one-sided upper. Ordering-sensitive at the scale T7 found.
- **S2** Pearson lag-1 autocorrelation of the 85 gaps (direct comparability
  with their T7). Two-sided.
- **S3** Spearman lag-1 autocorrelation of the gaps (robustness; they
  reported +0.269 descriptively — we register it). Two-sided.
- **S4** runs test over block signs (blocks above/below expected rate;
  few runs = regional streaks = smooth structure; many = alternation).
  Two-sided.

α family-wide 0.01, Bonferroni over 4 → per-test **p ≤ 0.0025** fires.
Two-sided add-one p = 2·min(p_lo, p_hi) capped at 1; attainable minimum at
D = 10,000 is 0.0002 (their D=1,000 attainability defect, Addendum 2, is
designed around here, not re-run into).

## Nulls (two, both reported; N1 primary)

Point-process instantiation of the flat model — sites are slips, positions
uniform, conditioned on n = 86:

- **N1 (primary, conservative): hard-core uniform**, consecutive gap ≥ 6
  (the observed spacing constraint), sampled exactly via the shift trick
  y_j = p_j − 5·j on a uniform 86-subset of 0..12,529.
- **N2 (comparability): unconstrained** uniform 86-subset of 0..12,954.
  Matches the model class of their `site_matched_shuffle` (which is
  histogram-preserving; for position statistics the conditioned point
  process is the same model class without the value-availability subtlety).
  EQUIVALENCE CHECK (informative, not a gate): N2's Pearson-ac1 null
  moments must land within Monte-Carlo distance of their reported
  −0.011 ± 0.106; report both.

D = 10,000 draws each, seed 20261128, per-draw stream
`default_rng([seed, crc32(tag)%100000, draw])`, tag ∈ {N1, N2}. Staged:
2,000 draws first; if S1 or S2 lands ≤ 0.01 on N1, extend to 10,000
(escalation rule, same as #9).

## Plants — the power curve (this campaign's instrument contribution)

Generative alternatives, sampled through the SAME statistic code:

- **P-sin(δ)**: density ∝ 1 + δ·sin(2πt/12956 + φ), φ uniform [0, 2π),
  δ ∈ {0.3, 0.5, 0.7, 0.9} — smooth drift (drifting-filter-parameter
  proxy).
- **P-step(δ)**: density (1+δ) first half, (1−δ) second half, δ ∈ {0.35,
  0.5} — sessioned generation proxy.

Sampling: hard-core N1 draw, accept-with-probability ∝ density,
resample-until-accepted (exact to first order in the acceptance ratio;
max accept prob normalized). 200 draws per (family, δ). Power per
statistic = fraction exceeding the N1 critical value c_α (99.75th pct of
the registered null draws, per statistic, one- or two-sided as registered).
Also report the fitted δ of the OBSERVED profile against P-sin (descriptive
amplitude calibration) so the power curve can be read at the observed
signal size.

## Verdict rule

- **REPLICATE**: any of S1–S4 ≤ 0.0025 on N1. Report all 8 p-values
  (4 stats × 2 nulls) regardless.
- **NO-REPLICATE**: none fires. T7 does not survive independent
  statistics/nulls at our measured power — a materially useful negative
  ONLY if the power curve shows we had ≥0.8 power at the observed
  amplitude; that sentence is mandatory in either verdict.
- Power disclosure gate (hard rule, MAP §D): if every statistic's power at
  the observed-amplitude δ is < 0.5, the verdict line must read
  WEAKLY-POWERED and say why.
- No threshold, statistic, or null changes after seeing null/plant output;
  later changes only as dated addenda before real-data scoring.

## Cost (estimate at launch, per house rule)

Pure numpy on n=86 point processes: nulls 2×10,000 draws × 4 statistics,
plants 8×200 — estimated **< 5 min single-core local**, no studio. Check
run.log timing against this; disclose deviation.

## Not covered (registered)

Mechanism identification (drift vs sessions vs state — power curves
distinguish signal SHAPE at best); value/gap/position CHANNEL readings
(theirs, NEGATIVE at power 1.00, not re-run); any doublet definition other
than adjacent-equal on the concatenated stream (triplet runs, lag-2);
per-page block geometry (13×1000 is the registered scale; other block
sizes are post-hoc by construction); histogram/value-availability
correlations in the stream-shuffle sense; anything upstream of statistics
(intent, code, message existence).

## Files

`t7.py` (census gate, nulls, plants, battery, verdict), `run.log`,
`results/t7_nulls.json`, `results/t7_battery.json`, `REPORT.md`,
`metadata.json`. Tracked results are small JSON/CSV; nothing >50 MB ever
leaves work/.
