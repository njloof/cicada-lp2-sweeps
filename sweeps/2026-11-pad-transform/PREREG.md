# PREREG — 2026-11-pad-transform (Phase 2)

**Status: REGISTERED BEFORE OUTPUT.** Written 2026-11-14; no Phase 2 sweep has been
run. Amendments permitted only before the first result-producing run, and then
appended below with timestamp + disclosure (never edited away).

## Motivation

Campaign #1 (crosspage-pad) closed the plain **difference** family
(`D = C_M − C_N`) NEGATIVE. Its ledger row names what it could not see: pad
*transformations* and pad *constructions*. This campaign covers the ones that are
mathematically distinct, with two collapses noted up front (they are free coverage,
not extra space):

1. **Pad Caesar shifts are χ²-no-ops**: `D = C_M − (C_N + s) = (C_M − C_N) − s`
   merely translates the histogram → identical χ². Not swept; stated as covered-by-collapse.
2. **Target atbash + difference ≡ negated sum** (see family B).

## Families swept

**A. Sum family** (new): `S = (C_M + C_N) mod 29` at every (M, N, o, orientation).
Covers in one stroke: subtractive pad (`C_M = P − C_N ⇒ P = C_M + C_N`), pad-as-atbash
(`P = C_M − (28 − C_N) = S − 28`, constant shift ⇒ same χ²), and target-atbash variants.
Same targets/pads/masking/min_len/orientations as campaign #1, incl. mirror pads
(straddling only). Expected window count ≈ campaign #1's 3,798,361; exact count
recorded in metadata.json.

**B. Alternating-weave pads** (new): `W = interleave(C_N, rev(C_N))` (length 2n;
also `interleave(rev, fwd)`). Block weaves N‖rev(N) are campaign #1's mirror set —
not repeated. All offsets, n_valid ≥ 50, both weaves.

**C. Self-mirror self-matched audit** (instrument audit, not a hypothesis sweep):
campaign #1's top hits were self-mirror (page vs its own reversal). For **every**
page 0–54 (no cherry-picking), compute the mirror-family χ² distribution and compare
its max against the **99th percentile of that same page's difference-family**
χ² distribution (self-matched null, preserves the page's own symbol frequencies).
Anomaly flag = mirror max > own diff-p99 AND > global MC null max (118.8).

## Instrument & calibration

Identical kernel (`core/kernel.py`), masking modes (primary tgt; sensitivity both),
statistics (χ² 29-bin, IoC). MC null: 20 in-page shuffles of the **full Phase 2
space (A+B)** per campaign rules of campaign #1, seed 20261114; families A and B
also reported against their own family-max nulls. English cribs used only as the
readability prong of the decision rule, never as the statistic (language-agnostic
instrument preserved).

## Decision rule (fixed now)

GO on a family iff observed max χ² > 1.1 × that family's MC null max **and** the
window survives mask=both **and** the window decodes with English cribs.
Family C flags are structural findings, never "solves"; they feed Phase 3 scoping.

## Deliverables

results/ CSVs (floor 40), null_maxima.csv, metadata.json (corpus hash, core rev,
seed, exact window counts), REPORT.md with ledger row + coverage/not-covered.

## Disclosure of priors

Campaign #1's null median (99) vs Bonferroni (92) showed this window geometry
routinely produces χ² in the 90s–110s. Expect top-of-list noise; only the MC bar
means anything. If everything comes back negative again, that is the result, and
it closes the pad-transform entry in the community ledger.
