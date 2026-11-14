# LP2 cross-page pad sweep — Phase 1 report

Date: 2026-11-13. Pipeline: `core/build_corpus.py` → `core/validate.py` (ALL GATES PASS) →
`run.py` → `calibrate.py` (this dir, over `core/kernel.py` + `core/mc.py`). Tests: `python3 -m pytest -q` (11 passed).

## Hypothesis

Some unsolved LP2 pages were enciphered using **another LP2 page's ciphertext as a
running pad**: `C_M[t] = (P_M[t] + C_N[t−o]) mod 29`. At the true (M, N, o) the
difference stream `D = (C_M − C_N)` equals the plaintext `P_M` and its 29-symbol
histogram is non-uniform (χ² ≫ 28); wrong alignments are uniform.

This is strictly stronger than the community's eliminated "page-on-page key reuse"
(shared keystream ⇒ c1−c2 = p1−p2, English-minus-English, offset 0 only — see
data/SOURCES.md "Ledger cross-check"). The gap was real; this sweep fills it.

## Search space

| component | count |
|---|---|
| target pages M (unsolved LP2) | 55 (pages 0–54, 12,956 runes) |
| pad streams N | 57 (pages 0–54 + AN END + PARABLE ciphertext) + 2 solved **plaintexts** |
| orientations | fwd, rev (complete direction space — target-reversal is a no-op: χ² is order-invariant and covers the same anti-diagonals as pad-reversal) |
| Phase 1b mirror pads | N‖rev(N), rev(N)‖N, junction-straddling windows only (sub-windows duplicate fwd/rev) |
| offsets | all o with ≥50 surviving positions |
| **total windows tested** | **3,798,361** |

ᚠ handling (refined vs handoff): target-side F positions are dropped (alignment-safe
under both null-F interpretations); pad-side F positions are **kept** (D = C_M − 0 =
P_M is genuine signal). Handoff's both-side masking run as sensitivity — all top hits
survive it (see below).

## Null calibration

`calibrate.py`: 20 in-page shuffles of every target (preserves lengths, symbol
frequencies, F density), identical sweep machinery, global max χ² per shuffle.
Bonferroni sanity band for 3.8M tests at α=0.05: **χ² ≈ 92.2** (Wilson–Hilferty).

MC null maxima (results/null_maxima.csv): min **88.5**, median **99.0**, max **118.8**
(n=20; empirical p for the observed max: 2/20 shuffles ≥ 111.6 → p ≈ 0.10).

Note the MC max (119) far exceeds the naive Bonferroni band (92.2): overlapping
windows are heavily correlated, so independence-based thresholds are anti-conservative
for max-statistics. The MC is the decision instrument; Bonferroni is kept only as a
sanity band.

## Results

Full space max χ² = **111.6** — M=12 vs itself, rev orientation, o=−83 (mirror
anti-diagonal, n=169). Top hits are dominated by the **self-rev family** (a page
against its own reversal = mirror-structure test, not cross-page). Top CROSS-page
hit: M=0 vs pad 17 rev o=72, χ²=86.4 (n=181).

### Verdict: NO-GO

- Global max 111.6 < MC null max 118.8 (and < the handoff's bar of 1.1× MC max = 130.7);
  empirical p ≈ 0.10. The page-12 mirror anomaly is max-statistic noise.
- Cross-page max 86.4 < null **median** (99.0) → p ≈ 1. No cross-page pad signal anywhere
  in the space, in either orientation, including the palindrome mirror set and the
  solved-page ciphertext/plaintext pads.
- The best cross-page window (M=0, pad 17, rev, o=72) was decoded to text: no English
  cribs (only 2-letter noise hits) — a skewed-but-linguistically-dead distribution,
  exactly what a high null draw looks like.
- Go criterion (χ² > 1.1× MC max **and** survives alternative ᚠ handling **and** reads
  as text): fails all three prongs.

| rank | target | pad | orient | offset | n | χ² | note |
|---|---|---|---|---|---|---|---|
| 1 | 12 | 12 (self) | rev | −83 | 169 | 111.6 | mirror; p≈0.10 |
| 2 | 26 | 26 | rev | −59 | 199 | 94.4 | self-mirror |
| 3 | 12 | 12 | revfwd | −83 | 249 | 92.6 | same test as rank 1 |
| 4 | 34 | 34 | rev | 14 | 241 | 91.7 | self-mirror |
| 5 | 14 | 14 | rev | −5 | 130 | 91.3 | self-mirror |
| 6 | 34 | 34 | fwdrev | −247 | 255 | 90.6 | same test as rank 4 |
| 7 | 15 | 15 | rev | −19 | 134 | 88.9 | self-mirror |
| 8 | 25 | 25 | rev | 198 | 73 | 87.1 | self-mirror |
| 9 | 40 | 40 | rev | −46 | 180 | 86.8 | self-mirror |
| 10 | **0** | **17** | rev | 72 | 181 | 86.4 | **best cross-page; decodes to garbage** |
| 11 | 15 | 15 | revfwd | −19 | 152 | 85.3 | same test as rank 7 |
| 12 | 24 | 4 | rev | 199 | 69 | 85.3 | sign-mirror of rank 14 |
| 13 | 20 | 20 | rev | 130 | 137 | 85.1 | self-mirror |
| 14 | 4 | 24 | rev | 190 | 70 | 84.9 | same test as rank 12 |
| 15 | 14 | 14 | revfwd | −5 | 135 | 83.0 | same test as rank 5 |
| 16 | 10 | 10 | revfwd | −191 | 256 | 82.9 | self-mirror |
| 17 | 17 | 17 | rev | −53 | 214 | 81.7 | self-mirror |
| 18 | 4 | 20 | fwd | −208 | 59 | 81.1 | cross, tiny window |
| 19 | 51 | 24 | fwdrev | −227 | 253 | 80.9 | cross, mirror straddle |
| 20 | 44 | 44 | rev | 177 | 94 | 80.6 | self-mirror |

Reciprocal pairs (24↔4) are the same anti-diagonal read in both directions
(D → −D): one observation, not two. 14 of the top 20 are self-mirror (within-page),
and mirror orientations (rev/revfwd/fwdrev) hold 78 of the top 100 — the
anti-diagonal family is where correlated null maxima live, not a pad signal.

Sensitivity: all top hits survive handoff both-side ᚠ masking (χ² 85–110, some
strengthen: p34 91.7→96.3, p40 86.8→89.0). Masking convention does not drive results.

## Disclosures

1. **LP2 page 55 is missing from every community lineage** (image 72.jpg exists,
   4 lines ≈ 80 runes; krisyotam/relikd/scream314 all jump 54→56). Template-matching
   transcription attempted from published images (`tools/p55_transcribe.py`): held-out
   glyph accuracy 46% on verified pages — the decorative font interpenetrates
   (glyphs touch via diagonal strokes), so segmentation is structurally impossible.
   Confirms dukotah's independent glyph-reader failure (0.145 alignment). Page 55
   stays excluded; the sweep covers 55/56 unsolved pages.
2. All machine-readable transcriptions share a single 2017 root (data/SOURCES.md);
   independence was established functionally (4 smoke decodes + image hashes), not
   by lineage.
3. Printed number channel (pages 10, 36–38) excluded from rune streams.
4. Mirror-pad sub-window redundancy removed by straddle dedup; real and null spaces
   identical.

## Ledger entry

> **Cross-page running-pad sweep (2026-11-13, this repo).** Hypothesis: unsolved LP2
> page M encrypted with another page's ciphertext as running pad,
> C_M[t] = P_M[t] + C_N[t−o] (mod 29). Space: 55 targets (LP2 0–54) × 59 pad streams
> (all pages + AN END/PARABLE ciphertext + their plaintexts) × {fwd, rev} + palindrome
> mirrors N‖rev(N), rev(N)‖N (straddling windows only) × all offsets, n≥50 after
> ᚠ-masking = 3,798,361 windows. Instrument calibrated by 20 in-page-shuffle MC nulls
> of the global max (max 118.8, median 99.0). Observed global max 111.6 (self-mirror,
> p≈0.10); best cross-page 86.4 (< null median, decodes to non-English). **Negative —
> covers and closes the gap left by ARMADA follow-up test #4 (offset-0-only,
> shared-keystream IoC). Coverage: 55/56 unsolved pages (p55 untranscribable, all
> lineages). Power: strong plaintext-χ² test at every alignment, both directions,
> palindrome orderings; not covered: interleaved pad constructions, pad derived from
> page N via transformation (atbash/shift of C_N — Phase 2), page 55.**
