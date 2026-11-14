# PREREG — 2026-11-pad-algebra (Phase 3)

**Status: REGISTERED BEFORE OUTPUT.** Written 2026-11-14; no Phase 3 computation has
been run. Amendments only before the first result-producing run, appended with
timestamp + disclosure.

## Motivation

Campaigns #1 (difference) and #2 (sum, alternating weaves) covered the additive
pad algebra. Their ledger rows name what remains: **multiplicative pad scaling**,
**stride/skip pad consumption** (the cross-page analog of dukotah's `skip_by_two`,
their self-declared coverage hole), and the recurring **page-level mirror outlier**
note (page 12 ranked 1st two campaigns running, ratio 2.42 vs median ≈ 1.7).

## Collapses declared up front (free coverage, not swept)

- `k = 28 ≡ −1`: `C_M − 28·C_N = C_M + C_N` → campaign #2 family A. **Covered.**
- `k = 0`: pad ≡ 0 → D = C_M (the page's own histogram; no pad hypothesis). **Excluded as trivial.**
- `k = 1`: campaign #1. **Covered.**
- Sign symmetry: `C_M + k·C_N = C_M − (29−k)·C_N` → the k∈[2,27] difference sweep
  covers multiplicative **sum** pads too (k ↔ 29−k). Stated, not swept twice.
- Mask invariance: `k·0 = 0` — pad-side ᚠ positions are identical for every k, so
  window geometry is k-invariant and pad-F positions remain valid signal (D = C_M).

## Families swept

**D_mult — multiplicative pad scaling (new).** `D = (C_M − k·C_N) mod 29`,
k ∈ {2..27} (26 multipliers), all ordered pairs (55 targets × 57 ciphertext pads +
2 plaintext pads), orientations fwd + rev, mirror orderings **excluded** (declared
scope: scaling × palindrome is a later product space). All offsets, n_valid ≥ 50,
primary mask tgt, sensitivity both. Expected ≈ 26× campaign #1's fwd+rev window
count (~6×10⁷); exact count recorded in metadata.json.

**E_stride — stride/skip pads (new).** `pad[t] = C_N[g·t]`, g ∈ {2,3}, and reversed
analogs `pad[t] = C_N[n−1−g·t]`; difference statistic. Cross-page analog of dukotah's
uncovered `skip_by_two`. Pads shorter than 50 runes after striding drop out
(short pages); participating-pair count recorded.

**F_outlier — page-level mirror-outlier audit (structural, properly calibrated).**
For each page: ratio = mirror-family max / own-diff p99 (quantities defined exactly
as campaign #2 family C, vacuous-p99 disclosure acknowledged). Null: 20 shuffles;
per shuffle recompute the ratio for all 55 shuffled pages and record the **max ratio
across pages** (the correct null for "is any page an outlier", fixing #2's
window-count asymmetry by construction — max-vs-max). Flag iff observed ratio >
null max ratio. Structural finding only; never a solve.

## Instrument & calibration

`core/kernel.py` unchanged (scaled/strided pads are constructed in the campaign
CLI — pad-side transformations need no kernel change). Per-family MC null:
20 in-page shuffles, seed **20261115**, resumable checkpointing (bit-identical RNG
stream across chunked runs). Family D null expected well above family A's? No —
difference-statistic geometry, null expected near campaign #1's band (med ≈ 99);
any deviation is exactly what the MC exists to measure.

## Decision rule (fixed now)

GO on D or E iff observed max χ² > 1.1 × that family's MC null max **and** the
window survives mask=both **and** decodes with English cribs.
F flags are structural (feed Phase 4 scoping); no readability prong.

## Cost & runtime disclosure (pre-declared, so the chunking is not post-hoc)

D sweep ≈ 10–15 min; its 20-shuffle MC ≈ 4–5 h, run in resumable foreground chunks.
E and F are minutes-scale. If wall-clock forces it, MC stays at 20 — the count is
part of the registered space, not a dial.

## Deliverables

results/ CSVs (floor 40), per-family null_maxima.csv, metadata.json (corpus hash,
core rev, seed, exact counts), REPORT.md + ledger row with coverage/not-covered.

## Remaining gaps after this campaign (pre-declared, so the ledger never overstates)

Non-alternating/non-uniform interleavings beyond stride; position-dependent pad
derivations (keystream from page N via gematria or ornament channels); page 55;
pads derived from LP1 pages (out of scope by design: LP1 is solved).
