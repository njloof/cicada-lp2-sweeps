# LP2 elimination ledger

One row per campaign. A row is the citable unit: hypothesis | space | null | verdict |
coverage caveats | link. This is what the community should reuse, not the raw CSVs.

| # | date | hypothesis | space | null calibration | verdict | coverage / not covered | link |
|---|------|-----------|-------|------------------|---------|------------------------|------|
| 1 | 2026-11-13 | cross-page running pad: `C_M − C_N = P_M` at true (M,N,o) | 3,798,361 windows — 55 targets × 59 pads × {fwd,rev} + palindrome mirrors (straddling), all offsets, n≥50, ᚠ-masked | 20× in-page-shuffle MC of the global max: min 88.5 / med 99.0 / max 118.8 | **NEGATIVE** (obs max 111.6 self-mirror p≈0.10; best cross-page 86.4 < null median; decode non-English) | 55/56 unsolved pages (p55 untranscribable); single-2017-root transcription; NOT covered: pad transforms (atbash/shift of C_N), interleaved constructions, page 55 | [report](../sweeps/2026-11-crosspage-pad/REPORT.md) |
| 2 | 2026-11-14 | pad transforms & constructions: sum family (covers subtractive/atbash pads), alternating weaves, self-matched mirror audit | 7,522,132 windows (A 3,798,416 + B 3,723,716) — registered PREREG before run | 20× MC of full A+B space, per family: A med 145.2/max 167.7; B med 90.6/max 122.0 (seed 20261114) | **NEGATIVE** (A max 147.2 p≈0.5; B 91.5 p≈0.5; 0/55 audit flags; decodes non-English) | additive transforms covered by collapse; NOT covered: multiplicative pad scaling k·C_N, position-dependent pad derivations, non-alternating interleavings, page 55 | [report](../sweeps/2026-11-pad-transform/REPORT.md) |
| 3 | 2026-11-14 | pad algebra: multiplicative scaling k·C_N (k∈2..27), stride/skip pads (skip_by_two analog), calibrated page-mirror-outlier audit | 63,149,262 windows (D 60,518,822 + E 2,630,440) — preregistered before run; collapses (k=0/1/28, sign symmetry) declared up front | 20× per-family MC, seed 20261115: D med 102.5/max 119.4; E med 92.7/max 121.2; F ratio med 2.06/max 2.32 | **NEGATIVE (D p≈0.7, E p≈0.5) — F FLAG: page 12 mirror-outlier ratio 2.418 > null max 2.32 (0/20, p≤0.048; structural, exploratory anatomy: ±1 shifted-mirror excess 23% vs 7% chance)** | all pad multipliers, stride-2/3 fwd+rev, both ᚠ conventions; 55/56 pages; NOT covered: non-uniform interleavings, position-dependent pad derivations, scaling×mirror product, page 55 | [report](../sweeps/2026-11-pad-algebra/REPORT.md) |

## Instrument notes (load-bearing for reading the rows)

- The χ² statistic is **language-agnostic** (29-symbol non-uniformity, no English
  adjudication) — deliberately, to avoid the English-only-negative failure mode
  documented in Dukotah/cicada3301 Round 18.
- Bonferroni bands are anti-conservative here (overlapping windows are correlated);
  every verdict is decided against the **MC null of the max**, never a p-value band.
- Corpus: 55 unsolved pages hash-anchored to published images; 4 smoke decodes
  reproduced in CI (`python3 -m core.validate`).

## Community findings alongside the negatives

- [Numbering reconciliation](NUMBERING.md) — LP1 vs LP2 vs 2014 release filenames.
- [Page 55](PAGE55.md) — missing from every lineage; untranscribable from published images.
- PARABLE pos-80 adjudication (ᚣ Y over scream314's ᛖ E) — data/SOURCES.md.
- Doublet count reproduced exactly: 86 across LP2 0–54.
