# Campaign 2026-11-pad-algebra — REPORT

> **Addendum (same day, campaign #4):** the page-12 F flag below did not survive
> a 1000-shuffle null (p=0.099; 20-draw max 2.32 vs 1000-draw max 3.57 — a
> tail-resolution artifact). See `../2026-11-p12-mirror/REPORT.md`.

Run 2026-11-14. **Pre-registered before output** (PREREG.md, committed `8db3b52`,
earlier than any Phase 3 computation). Instrument: `core/kernel.py` **unchanged**
(as preregistered) — scaled/strided pads are constructed in the campaign CLI
(`run.py`, committed `3dc51ec`). Corpus hash, seed, exact counts: metadata.json.

## Verdict: NEGATIVE (D, E) — with one calibrated structural FLAG (F: page 12)

| family | windows | observed max | MC null (20×, seed 20261115) | empirical p | readability prong |
|---|---|---|---|---|---|
| D_mult `(C_M − k·C_N)` k∈2..27 | 60,518,822 | **101.1** (7←36 rev k=11 o=147, n=61) | min 96.1 / med 102.5 / **max 119.4** | ≈ 0.7 | garbage |
| E_stride g∈{2,3} + reversed | 2,630,440 | **93.1** (45←0:s3 o=211, n=57) | min 86.8 / med 92.7 / **max 121.2** | ≈ 0.5 | — (fails χ² prong) |
| F_outlier page ratio | 55 pages | **2.418** (p12) | min 1.75 / med 2.06 / **max 2.32** | **≤ 0.048 (0/20)** | — (structural) |

Decision rule (fixed pre-run): GO iff observed > 1.1 × family null max **and**
mask=both survival **and** English cribs (D, E); F flags iff ratio > null max ratio.
D: 101.1 ≪ 1.1×119.4 → fail (and below null median). E: 93.1 ≪ 1.1×121.2 → fail. **F: 2.418 > null max 2.32 → page 12 FLAGGED as a structural outlier** — the flag feeds Phase 4 scoping; per registration it is not a solve and carries no readability claim.

## What was swept

- **D_mult** — the multiplicative gap left by campaigns #1/#2: 26 multipliers
  (collapses declared in the PREREG: k=0 trivial, k=1 = #1, k=28 ≡ −1 = #2-A,
  sign symmetry k↔29−k covers multiplicative *sum* pads). All ordered pairs
  (55 targets × 57 pads incl. 2 solved plaintexts), fwd + rev, mirror orderings
  excluded by scope. Self-pair fwd o=0 excluded as trivial (D=(1−k)·C_M is a
  symbol permutation of the page's own histogram — disclosed here and in run.py).
- **E_stride** — `pad[t] = C_N[g·t]` and `pad[t] = C_N[n−1−g·t]`, g∈{2,3}: the
  cross-page analog of dukotah's self-declared uncovered `skip_by_two`.
  11,110 (target, strided-pad) pairs participated (striding shrinks pads;
  pads < 50 runes drop out).
- **F_outlier** — per-page mirror-max / own-diff-p99 ratio (campaign #2 family-C
  quantities, but with the *correct* max-vs-max null that fixes #2's vacuous-p99
  window-count asymmetry).

## Observed structure

- D top windows are small-n frequency noise: only 4/20 of the top rows have
  n≥100; the k-distribution of top rows is flat (no multiplier concentrates).
  Rows 1 and 4 (7←36 rev k=11, 36←7 rev k=8) are one reciprocal observation.
- Mask=both sensitivity *weakens* D's leaders (101.1→98.0, 98.6→87.7, 96.7→88.5;
  two windows strengthen marginally, 94.2→96.4, 92.7→94.0) — the opposite of
  campaign #2's sum family, and noise-consistent.
- Decodes of the top three D windows:
  `HAEIJNGJAHHUJGEAHLUCHPJLXMHJHFEO…`, `AESADSDSLTSLDCNGCHOSEOONLRPAEEO…`
  (n=185; E/O/D/F repetition = page frequency profile, not language),
  `EEUSTEUHFAEUEOFTEJFJJEUMEMEUEMTH…` — no language in any.
- E's max 93.1 sits inside campaign #1's *difference-family* null band
  (med 99.0 / max 118.8) despite the strided geometry.
- F: page 12 ratio 2.418 stands apart again (next 1.979; median 1.49). Its
  mirror_max 111.56 is the same self-mirror window that was campaign #1's global
  max — the p12 thread now has three independent campaign sightings.
  Registered null: 0/20 shuffled replicates reached p12's ratio (max 2.32 vs observed 2.418; margin ~4% — thin, hence the confirmation campaign scheduled before announcement).

### p12 anatomy (EXPLORATORY — post-hoc, after the registered F statistic was computed; never a solve)

The flagged window is a **pure reversed alignment, offset −83, n=169/261 runes**:
in page coordinates it compares `A[i]` vs `A[177−i]` (pivot ≈88.5).

- The excess is **not** plain palindromy: the D histogram peaks at **28 (EA) ×20
  and 1 (U) ×19** — mirror partners differ by **±1** in 23.1% of positions (chance
  6.9%) — while d=0 sits at 1.2%, *below* the page's own ᚠ density. A shifted
  (±1-jittered) mirror structure, not a Caesar-clean one.
- Survives mask=both (110.1, n=162); excess spread across all four quarters
  (χ² 38/63/64/35) — whole-window, not a local artifact.
- Not a frequency artifact: 200 in-page shuffles of p12 (exploratory seed
  20261112, max over all rev alignments) give med 69.1 / max 97.0 — observed
  111.56 is 0/200 (p < 0.005).
- Not a corpus property: median |Δ|=1 fraction at own rev-max across 55 pages is
  0.064 ≈ chance. p12 ranks 1/55 on both revmax and |Δ|=1 fraction (next 0.101).
  Contrast p26/p34: high revmax with the excess at d=0 (0.080/0.112) — plain
  palindromic leanings; p12's is purely shifted.
- Not in the published toolkit (checked against the pinned dukotah snapshot):
  their per-page statistics are marginal (χ²-vs-uniform, entropy —
  `run_stats.py`) and their positional statistic is forward-lag Pearson
  autocorrelation at lags 2–40 (`r2_fractionation_signature.py`) — neither
  tests reversal alignments, and index-covariance cannot detect a
  joint-histogram ±1 excess. No self-reversal scan exists in their live code.
  (Absence in this snapshot ≠ absence in the world; wiki "palindromic"
  mentions concern LP1-era structures.)
- Caveats: p12 was examined *because* it topped the registered ratio list
  (selection acknowledged — the registered max-vs-max null is the citable test);
  ±1 is index-adjacency in the gematria ordering, not a visual glyph-confusion
  class of the 2017 font, but a transcription-process origin cannot be excluded.

## Ledger entry

> **Pad-algebra sweep (2026-11-14, preregistered).** Multiplicative pad scaling
> `D=(C_M−k·C_N) mod 29`, k∈2..27 (sign symmetry covers multiplicative sum pads;
> k=0/1/28 collapsed by registration), all pairs fwd+rev, mirrors excluded;
> stride/skip pads `C_N[g·t]`, `C_N[n−1−g·t]`, g∈{2,3} (cross-page analog of
> dukotah's uncovered `skip_by_two`); properly calibrated page-mirror-outlier
> audit (max-vs-max null). 63,149,262 windows; 20× per-family MC null
> (seed 20261115). Observed maxima 101.1 (D) and 93.1 (E) vs family null maxima
> 119.4 (D) / 121.2 (E); F ratio 2.418 vs null max 2.32; decodes non-English; F: p12 ratio 2.418 vs null max ⟪NULL_F⟫.
> **Negative on both pad-algebra families; page 12 FLAGGED as a calibrated mirror outlier (p ≤ 0.048, structural)** Covers: all pad multipliers, stride-2/3 consumption fwd+rev,
> both ᚠ conventions; 55/56 unsolved pages. **Not covered (pre-declared):
> non-uniform interleavings beyond stride; position-dependent pad derivations
> (gematria/ornament channels); scaling×palindrome mirror product space;
> page 55; LP1 pads (out of scope by design).**

## Disclosures

1. Self-pair fwd o=0 excluded per orientation in D (trivial all-structure window,
   analogous to campaigns #1/#2 trivial-offset exclusions); the exclusion is
   applied identically inside the MC (same code path).
2. `window_counts.json` was initially clobbered by the second `--skip` run
   (bookkeeping bug, fixed to merge-on-write; E+F re-run verified deterministic —
   identical maxima and row counts). No analysis output affected.
3. Reciprocal pairs (M,N) and (N,M) appear as separate rows by construction;
   the top pair above is one physical observation counted twice.
4. Mask=both numbers are sensitivity-only (the primary prong decides; D/E
   leaders' both-mask numbers lack their own nulls).
5. The p12 anatomy section is **exploratory/post-hoc** (the page was examined
   because it topped the registered F list; its own null, seed 20261112, is a
   supplementary diagnostic, not the registered test). Structural only; feeds
   Phase 4 scoping.
6. Transcription single-root caveat and page-55 exclusion carry over from
   campaigns #1/#2 unchanged.
