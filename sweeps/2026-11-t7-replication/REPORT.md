# Campaign #10 report — T7 replication + smooth-heterogeneity power curve

Run 2026-11-16. PREREG `d1d81a8` (before any output; CI gate). Corpus
sha `9f5f14d4…483e`, book-page labels. Verdict: **REPLICATE** — with the
mandatory power sentence below.

## What replicated

| stat | obs | p (N1 hard-core, primary) | p (N2 unconstrained) | fires at 0.0025? |
|---|---|---|---|---|
| S1 block-rate χ² (13 blocks) | 15.71 | 0.151 | 0.201 | no |
| **S2 Pearson ac1(gaps)** | **+0.3795** | **0.0006** | **0.0008** | **YES** |
| S3 Spearman ac1(gaps) | +0.2669 | 0.0094 | 0.0078 | no (suggestive) |
| S4 block-sign runs | 8 | 0.915 | 0.934 | no |

D = 10,000 (escalation fired at stage 2,000: S2 p=0.002 ≤ 0.01; extended on
disjoint per-draw streams, seed 20261128). Nulls: N1 hard-core gap≥6
(the observed spacing constraint), N2 unconstrained uniform 86-subset —
both independent point-process implementations of the flat-Bernoulli model.
**Equivalence check passed:** our N2 Pearson null −0.009 ± 0.104 vs dukotah's
reported −0.011 ± 0.106 — same model class, same moments within MC
distance. Premise cross-check: our (pos, gaps, vals) tuple is
**bit-identical** to their persisted `real_sites_U86` (two pipelines, one
object).

**T7 is now replicated: independent extraction, independent nulls,
registered ordering-sensitive statistic, p = 0.0006.** Still `measured`,
never certified as intent — that is a different question than replication.

## The power curve (the instrument contribution their Round-45 ask named)

Plants: conditional-IPP sites with smooth density, one phase per draw,
same hard-core spacing; 200 draws/family; power vs the N1 critical values.

| plant | S1 | S2 | S3 | S4 | mean ac1 |
|---|---|---|---|---|---|
| sin δ=0.3 | 0.02 | 0.01 | 0.00 | 0.015 | +0.019 |
| sin δ=0.5 | 0.17 | 0.04 | 0.01 | 0.055 | +0.108 |
| sin δ=0.7 | 0.545 | 0.18 | 0.035 | 0.10 | +0.190 |
| sin δ=0.9 | 0.96 | 0.355 | 0.05 | 0.115 | +0.263 |
| step δ=0.35 | 0.14 | 0.035 | 0.01 | 0.105 | +0.091 |
| step δ=0.5 | 0.475 | 0.115 | 0.055 | 0.325 | +0.153 |

**Mandatory power sentence (verdict rule):** at the observed profile's
fitted sinusoidal amplitude (δ_fit = 0.28) every registered statistic has
power ≤ 0.02 — against the SMOOTH class this campaign is WEAKLY-POWERED,
and the REPLICATE verdict must be read with that.

**But the two halves fit together into one informative statement:** the
observed ac1 (+0.380) EXCEEDS the mean of even the δ=0.9 sinusoid plant
(+0.263) — the observed structure is outside the smooth-gentle class
entirely. It is concentrated: the largest gaps come in consecutive runs —
0-based gap indices 17–19 = 400+712+537 (**a 1,649-rune span with zero
doublets**, pos 2739–4388), plus 553+390 adjacent at indices 8–9, plus an
isolated 662 at index 63. Block-count statistics (S1, S4) are blind to this (their nulls
absorb 13-bin multinomial noise at p≈0.15/0.91) while gap-sequence
statistics see it clearly.

**Implication for dukotah Round 45:** among their three named mechanism
classes, the power curve disfavors "drifting filter parameter" (smooth
sinusoid: undetectable at observed amplitude, and observed ac1 exceeds its
max-δ mean) and favors **localized sessions / stateful rejection loops**.
The right R45 plant is a LOCAL VOID plant (planted doublet-free span of
~1,600 runes), with a registered max-run/void-length statistic — not
another block-geometry test.

## Numbers, runtime, regeneration

- Windows/draws: 2×10,000 nulls + 6×200 plants; runtime **2.6 s** local
  (PREREG estimate <5 min — held).
- Escalation: fired and honored per PREREG (2,000 → 10,000, disjoint
  streams).
- No disclosed reruns; no threshold/statistic changes post-registration.

```
python3 sweeps/2026-11-t7-replication/t7.py --stage 2000   # full pipeline, auto-escalates
```

## Not covered (as registered)

Mechanism identification (power curves distinguish signal SHAPE at best);
channel readings (theirs, NEGATIVE at power 1.00); other doublet
definitions; other block geometries; value-availability correlations;
intent/message existence. Plant samplers are documented proxies
(conditional-IPP + greedy hard-core), not exact constrained joints.

## Upstream

A replication this cheap and this sharp is worth posting to
Dukotah/cicada3301 (their T7 row + the void-plant suggestion for R45).
Public action — requires explicit owner approval, drafted on request.

---

## Corrections (appended 2026-11-18, external review; LEDGER C1)

- "doublet-free span" (body + R45 paragraph) is WRONG: the span 2739–4388
  contains doublets at 2740/3140/3852 (0-based, second rune of pair). Read:
  *three consecutive large gaps 400/712/537 against a corpus-typical ~150*.
  The R45 void-plant suggestion stands (a planted large-gap region is still
  the right plant); the ac1 +0.380 anomaly is unchanged.
- "Replication" is better read as *reproduction*: same 86 sites as dukotah.
  Our independent null designs validate the statistic's calibration, not the
  observation's forking-paths risk.
