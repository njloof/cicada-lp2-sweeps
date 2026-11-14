# Campaign 2026-11-product-spaces — REPORT

Run 2026-11-14. **Pre-registered before output** (PREREG.md, committed `1005c25`,
earlier than any campaign output; methodology commit `dc4e327` vectorizes the
null-max computation — same registered statistic, startup self-check asserts
equality with the loop path on real streams). Corpus hash, seed, exact counts:
metadata.json.

## Verdict: NEGATIVE on all three families (K, L, M) — no escalation triggered

| family | windows | observed max | MC null (20×, seed 20261119) | empirical p | GO prong (1.1×max) |
|---|---|---|---|---|---|
| K stride-ext + strided mirrors | 10,976,270 | **91.65** (8←43:s2m smirror o=−62, n=205) | min 89.2 / med 97.4 / **max 107.0** | 0.952 | 117.7 — fail |
| L scaling × stride | 110,948,708 | **112.44** (24←39:s3 k=27 o=42, n=77) | min 105.9 / med 114.2 / **max 126.5** | 0.619 | 139.1 — fail |
| M scaling × mirror junction | 39,580,268 | **95.62** (42←21:fwdrev k=9 o=−241, n=258) | min 89.8 / med 97.6 / **max 109.1** | 0.667 | 120.0 — fail |

Decision rule (fixed pre-run): GO iff observed > 1.1 × family null max **and**
mask=both survival **and** English cribs. All three fail the first prong
comfortably; all three observed maxima sit **below their family null medians**;
decodes are garbage (below). The pre-declared escalation rule (obs ≥ null
median → extend to ≥200 draws) did not fire for any family.

**Total: 161,505,246 windows** — campaign #5 more than doubles the cumulative
swept space (≈236M across five campaigns).

## What was swept

- **K** — (a) stride pads g∈{4..8} fwd+rev: **g≥6 vacuous by length**
  (longest page 261 runes; 261//6 < 50 = MIN_LEN — pre-declared; effective
  stride coverage after this campaign is g∈{2..5}); (b) strided mirror pads
  g∈{2..5}, both strided streams × both orderings, straddle-only.
- **L** — the D×E product space: `D = (C_M − k·W) mod 29`, k∈2..27 over all
  strided pads g∈{2..5} fwd+rev. Solved-plaintext pads contribute no strided
  pads ≥50 (lengths 84/95) — pre-declared.
- **M** — the product #3's D excluded: k-scaled **mirror-junction** pads
  (fwdrev/revfwd, straddle-only), 57 cipher + 2 plaintext mirrors, trivial
  self-pair identities excluded as in #1.

## Observed structure (all noise-consistent)

- **L leaders are small-window frequency noise**: of the top 500 rows, only
  42 have n≥100 (median n = 63); k is near-flat across the multiplier range
  (mode k=2 at 30/500 vs 19 expected under flat — ≈2.5σ, not remarkable over
  26 bins with 500 correlated draws). Decodes: `TURTAPBUGAAQMU…`, no language.
- **M leaders are large-window, low-amplitude** (449/500 with n≥100, median
  n=237, top_frac 0.10–0.12, k flat): the page-frequency-profile signature,
  not a keystream. Decode: `[28]BEPRBA[28]LSUR…`, no language. Mask=both moves
  leaders both directions (95.62→100.47, 95.19→91.14, 90.87→85.50) — the #3
  D pattern, noise-consistent.
- **K leaders** skew to strided-mirror geometry (393/500 smirror) with median
  n=104; top window 8←43:s2m weakens under mask=both (91.65→86.23).
  Decode: `THAY[27]S[27]WTFUNE…`, no language.
- **The borrowed-threshold trap, live:** L's observed 112.44 sits ~10 χ² above
  #3's difference-family null median (102.5) — against a borrowed D null it
  would read "elevated". Its own family null median is 114.19: the strided
  geometry lifts the whole band, and 112.44 is *below* median. Third campaign
  in a row demonstrating that nulls are family-specific; a borrowed threshold
  would have manufactured a lead out of nothing.

## Ledger entry

> **Product-space sweep (2026-11-14, preregistered).** Pairwise products left
> open by #3: stride extension g∈{4..8} + strided-mirror junctions (K);
> scaling × stride k·C_N[g·t], k∈2..27, g∈{2..5} (L); scaling × mirror-junction
> k·[C_N‖rev(C_N)] straddle-only (M). 161,505,246 windows; 20× per-family MC
> null of the global max (seed 20261119); pre-declared escalation rule
> (obs ≥ null median → 200 draws) not triggered. Observed maxima 91.65 /
> 112.44 / 95.62 vs family null maxima 107.0 / 126.5 / 109.1; all below their
> own null medians; decodes non-English; mask=both non-surviving.
> **Negative on all three families.** Covers: effective stride g∈{2..5}
> (g≥6 length-vacuous, disclosed), scaled mirror junctions, strided mirrors;
> 55/56 unsolved pages; both ᚠ conventions. **Not covered (pre-declared):
> triple products (k × stride × mirror); position-dependent pad derivations
> (digit/ornament channels); non-uniform interleavings; page 55; LP1 pads
> (out of scope by design).**

## Disclosures

1. **Vectorized null path** (`dc4e327`): the null computes χ² across all
   offsets in one pass (only the max is needed). Identical filters (min_len,
   straddle, trivial offsets); startup self-check asserts equality with the
   observed-run loop path on real streams before any shuffle. Registered
   statistic unchanged.
2. **Stream duplication:** the PARABLE page stream *is* its plaintext stream
   (page reads directly; p57 ≡ PARABLE57 verified), so M's PARABLE-pad rows
   duplicate page-57-pad rows (visible in the leaders table: identical
   90.63/88.39). Duplication cannot inflate a max statistic; disclosed for
   completeness. (ANEND56 ≠ page-56 stream — that page has a real pad.)
3. g≥6 stride coverage is length-vacuous (pre-declared); the ledger says
   effective stride coverage g∈{2..5}.
4. Repo copies of the sweep CSVs ship as top 100,000 rows (χ²-sorted); full
   files stream to `work/product-spaces/` — sha256 in metadata.json,
   deterministic regeneration: `python3 sweeps/2026-11-product-spaces/run.py`
   (~65 min, mask tgt). All reported statistics use the full sweep.
5. Mask=both numbers are sensitivity-only (leaders table); both-mask values
   have no nulls of their own. Three L leaders fall below n=50 under
   mask=both (blank in leaders_both.csv).
6. Reciprocal/duplicate pair counting and the single-2017-root transcription
   caveat carry over from #1–#3 unchanged; page 55 excluded (missing).
