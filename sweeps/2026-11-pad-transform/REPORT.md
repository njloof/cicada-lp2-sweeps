# Campaign 2026-11-pad-transform — REPORT

Run 2026-11-14. **Pre-registered before output** (PREREG.md, committed `5ed624a`,
earlier than any Phase 2 computation). Instrument: `core/kernel.py` extended with
`stat="sum"`; campaign CLIs in this dir. Corpus hash, seed, exact counts: metadata.json.

## Verdict: NEGATIVE — all three families

| family | windows | observed max | MC null (20×) | empirical p | readability prong |
|---|---|---|---|---|---|
| A sum `(C_M+C_N)` | 3,798,416 | **147.2** (p23 self-rev o=63, n=144) | min 128.0 / med 145.2 / **max 167.7** | ≈ 0.5 | garbage |
| B weave pads | 3,723,716 | **91.5** (26 vs 29:w2 o=−480, n=72) | min 82.7 / med 90.6 / **max 122.0** | ≈ 0.5 | — (fails χ² prong) |
| C self-mirror audit | 55 pages | flags by registered rule: **0** | own-diff p99 + global 118.8 | — | — |

- Best **cross-page** sum hit: 38↔48 revfwd/rev, χ²=84.2 — below campaign #1's null
  median, deep in noise. (Reciprocal pairs are one observation, as before.)
- Top A windows survive mask=both and *strengthen* (147.2→157.0, 145.4→154.0) —
  but the family's own null reaches 167.7, so survival proves nothing. Disclosed.
- Readability: the top A window (S stream, n=144) transliterates to
  `AFSEATRTHTHDOHWMTH…` (and ×inv2: `BFIAAPTHUUTHTREFU…`) — rune-frequency noise, no language.

## The methodological result (the one worth keeping)

**Family-specific nulls are not optional.** The sum statistic's null distribution
(median 145.2) sits ~46 χ² points above the difference statistic's (median 99.0):
sums of draws from shared-frequency multisets concentrate (f⊛f convolution), so
"χ² in the 140s" means something completely different in the two families. Had we
judged the sum sweep against campaign #1's null (max 118.8), **four self-mirror
windows would have been crowned as hits** (147.2, 145.4, 137.8, 132.2). The
preregistered per-family MC caught all four. This is the second demonstration in two
campaigns that Bonferroni-style or borrowed thresholds would have produced false
positives on this corpus.

## Family C, disclosed design bias

All 55 pages exceed their own difference-family p99 — the gate is vacuous as
specified, because the mirror family contains ~2–3× as many windows as the
difference family (rev + both straddling mirror orderings vs fwd alone), so its max
beats a p99 by construction. The binding prong was `> global MC max 118.8`:
**0/55 pages flagged**. The ratio ranking (mirror_max / own_diff_p99) is retained as
a *structural* note for Phase 3 scoping, not a finding: page 12 = 2.42 stands apart
(next-highest 1.98; median ≈ 1.7), continuing its campaign #1 anomaly streak.

## Ledger entry

> **Pad-transform & construction sweep (2026-11-14, preregistered).** Families: sum
> stream `(C_M+C_N)` (covers subtractive pad, atbash pad, target-atbash by
> constant-shift collapse), alternating-weave pads `interleave(C_N,rev)` /
> `interleave(rev,C_N)`, and a self-matched per-page self-mirror audit (all 55 pages).
> 7,522,132 windows; 20× MC null of the full A+B space per family (seed 20261114).
> Observed maxima 147.2 (A) and 91.5 (B) vs family null maxima 167.7 / 122.0;
> both p≈0.5; decodes non-English; 0/55 audit flags. **Negative.** Covers: all
> additive pad transforms (shifts collapse), atbash, subtraction, reversal, mirror
> palindromes, alternating weaves, both ᚠ conventions; 55/56 unsolved pages.
> **Not covered: page 55; multiplicative pad scaling (k·C_N, k≠1); position-dependent
> pad derivations; non-uniform interleavings beyond alternating.**

## Disclosures

1. Family C's p99 prong was vacuous by design (window-count asymmetry); fixed in
   spirit by the global-null prong, and the ratio column is labeled structural.
2. Mask=both numbers for family A lack their own MC null (they are sensitivity
   numbers only; nothing hinges on them since the primary prong failed).
3. Transcription single-root caveat and page-55 exclusion carry over from
   campaign #1 unchanged.
