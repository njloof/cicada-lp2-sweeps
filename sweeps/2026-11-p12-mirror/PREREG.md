# PREREG — 2026-11-p12-mirror (Phase 4 / confirmation campaign #4)

**Status: REGISTERED BEFORE OUTPUT.** Written 2026-11-14, after campaign #3's
registered F verdict (page-12 flag, p ≤ 0.048 at 20 draws) and its disclosed
exploratory anatomy, and before any campaign-#4 computation. #4 is a
**confirmation** campaign: its hypotheses were formed on the same corpus, so it
sharpens how extreme p12 is under the null — it cannot manufacture independence
from the selection that found it. That caveat is part of the registration, not a
post-hoc addition.

## Questions and tests

**G_null — sharp p-value for the registered F statistic.**
Statistic: exactly campaign #3's F (per page: mirror-family max / own-diff p99;
headline: max ratio across 55 pages; observed 2.418, page 12).
Null: **1,000** in-page shuffles (length/frequency/F-density preserved), seed
**20261116**, max-vs-max as registered in #3. Report p = (1 + #{null ≥ obs})/1001.
Count fixed here: 1,000 is the registered space, not a dial.

**H_shift — prospective corpus-wide shifted-mirror test (new statistic, the
cleanest independent evidence).**
Per page: S = max over reversed alignments of (h[1] + h[28]) / n_valid — the
share of mirror partners differing by ±1 in gematria order (observed: p12 =
0.231 at rev o=−83; corpus median ≈ 0.064 ≈ chance).
Null: same 1,000 shuffles, per shuffle recompute S for all pages, record the
**max across pages** (max-vs-max; no page selection involved in the statistic —
the hypothesis "some page carries a shifted mirror" is registered prospectively
even though p12's candidacy motivated it).
Also recorded per shuffle: p12's own rev-family χ² max (sharpens the #3
exploratory 0/200 anatomy null to 0/1000).

**I_noise — transcription robustness (sensitivity curve, descriptive).**
All published transcriptions trace to one 2017 root (data/SOURCES.md), so
independent-lineage replication is impossible; this is the substitute.
Corruption model: replace f·n_f non-ᚠ runes of p12 with uniform draws from 1..28
(mask geometry preserved by construction), f ∈ {0.02, 0.05, 0.10}, 200
replicates each, seed 20261117. Report median (and 10th-pct) of: rev-family
χ² max, and |Δ|=1 fraction at the fixed window (o=−83). Disclosed: uniform
substitution is a deliberately destructive proxy for structured glyph errors;
this is a survival curve, not a null.

**J_structure — descriptives, no thresholds.**
(a) Pivot localization: map the anti-diagonal constant 177 (pivot ≈ rune 88.5
of 261) back to the raw transcription; report the nearest structural markers
(line breaks, word/section marks, printed-number channel).
(b) ±1 run structure: run-length profile of the ±1 indicator sequence in the
window, vs its shuffle distribution (2,000 shuffles, seed 20261118).
(c) Controls: G/H statistics on the solved plaintexts (ANEND56, PARABLE57) —
does the mirror instrument fire on known-true LP2 material?

## Decision rule (fixed now)

**CONFIRMED** iff G p ≤ 0.01 **and** H p ≤ 0.01.
**SUPPORTED** iff exactly one clears. **Dissolved** iff neither does
(p12's #3 flag then gets a public downgrade note). I_noise and J_structure
are context, not gates; whatever they show gets reported verbatim.
Nothing here is a solve; the output is a calibrated structural finding.

## Instrument

`core/kernel.py` unchanged (as ever for pad-transform campaigns); per-alignment
histograms come from `pair_scan`'s existing return contract. Campaign-local
code only. Resumable checkpointing as in #2/#3 (bit-identical RNG stream).

## Deliverables

results/ CSVs (G/H null maxima per shuffle, per-page S table, noise curve,
run-length table), metadata.json (corpus sha, core rev, seeds, counts),
REPORT.md, ledger row #4, and — if CONFIRMED — the release-ready p12 note.

## Gaps this does NOT close (pre-declared)

Same-page structure ≠ cipher: none of these tests adjudicate whether the
mirror structure is *intentional* vs an artifact of page construction or
transcription lineage; page 55 remains untranscribable; single-root caveat
is mitigated (I_noise) but never eliminated.
