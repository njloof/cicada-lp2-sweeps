# Handoff: LP2 Cross-Page Modular-Difference Sweep

**For:** Claude Code (or any coding agent)
**Author:** Human researcher + assistant analysis
**Date:** 2026-11-13
**Estimated total effort:** 4–8 hours (dominated by data validation, not compute)

---

## 1. Objective

Test the hypothesis that one or more unsolved *Liber Primus* LP2 pages (onion7 `0.jpg`–`55.jpg`, ~56 pages, ~12,956 runes total) were encrypted using **another LP2 page's ciphertext as the running pad** — i.e., pages acting as one-time pads for each other. If page M was encrypted as

    C_M[t] = (P_M[t] + C_N[t - o]) mod 29

then the difference stream `D = (C_M - C_N) mod 29` at the true offset `o` is the plaintext of page M and will show a strongly non-uniform 29-symbol distribution, while wrong alignments look uniform. This is the classic two-time-pad / Venona failure mode, transplanted to the base-29 Gematria Primus cipher.

**Why this is worth testing:** the unsolved pages are statistically "OTP-class" (flat frequency, doublet deficit), which is consistent with pad material drawn from structured-but-hidden sources; the puzzle author's own grammar loves self-combination (2012's XOR-of-two-images step, "3301 XOR" instructions, palindromic/mirrored structures on the solved pages); and the "Some Wisdom" page's mirrored number block hints at reflected/reused structure.

**What is already excluded — do not re-run these:** the community elimination ledger (github.com/Dukotah/cicada3301, `liber-primus/` directory) has ruled out: ciphertext autokey at lags 1–1000; periodic keys for all periods 11–11,781; key reuse in stretches >= 3,000 runes; pad restarts at page/section/paragraph/line/clause boundaries. Check the current ledger before duplicating any of those. The **cross-page pairwise space at arbitrary offsets is NOT in the ledger** — that is the gap this project fills.

## 2. Phase 0 — Dataset acquisition and validation (do this first, carefully)

### Sources (fetch at least two independent ones and diff them)

1. `github.com/Dukotah/cicada3301` — `liber-primus/` directory (active research repo, includes canonical rune transcriptions and the elimination ledger)
2. `github.com/iBotPeaches/cicada_3301` — `liber_primus/` directory (runic markdown transcriptions of solved + unsolved pages)
3. `github.com/scream314/cicada3301` — `liber_primus.md`
4. Uncovering Cicada wiki (uncovering-cicada.fandom.com) — page images and transcription notes

If the sandbox has no network access, scaffold the pipeline with synthetic data (see appendix C) and leave a clearly marked `data/` drop-in folder with instructions.

### Known data pitfalls (the community has been burned — verify, don't trust)

- An old circulating copy had `page_27` that was literally a duplicate prefix of `page_44`, producing phantom "key reuse" hits. Hash every page; assert no page is a prefix/substring duplicate of another.
- A historical transcription error ("MABU" vs "HOLY" ambiguity) misled analysis for years. Cross-check rune counts per page against at least two sources; investigate any disagreement before proceeding.
- Page ordering: LP2 pages are `0.jpg`–`57.jpg`; pages 56 ("AN END") and 57 ("PARABLE") are SOLVED. The sweep targets 0–55; keep 56–57 as (a) pipeline validation and (b) optional extra pad candidates (their known plaintexts).

### Encoding spec — Gematria Primus

29 runes. Index = position in the alphabet below; the cipher is additive over indices mod 29. (Prime values are the gematria layer — record them but the sweep uses indices.)

| idx | rune | latin | prime | idx | rune | latin | prime | idx | rune | latin | prime |
|----|----|----|----|----|----|----|----|----|----|----|----|
| 0 | ᚠ | F | 2 | 10 | ᛁ | I | 31 | 20 | ᛚ | L | 73 |
| 1 | ᚢ | U/V | 3 | 11 | ᛃ | J | 37 | 21 | ᛝ | NG/ING | 79 |
| 2 | ᚦ | TH | 5 | 12 | ᛇ | EO | 41 | 22 | ᛟ | OE | 83 |
| 3 | ᚩ | O | 7 | 13 | ᛈ | P | 43 | 23 | ᛞ | D | 89 |
| 4 | ᚱ | R | 11 | 14 | ᛉ | X | 47 | 24 | ᚪ | A | 97 |
| 5 | ᚲ | C/K/Q | 13 | 15 | ᛋ | S/Z | 53 | 25 | ᚫ | AE | 101 |
| 6 | ᚷ | G | 17 | 16 | ᛏ | T | 59 | 26 | ᚣ | Y | 103 |
| 7 | ᚹ | W | 19 | 17 | ᛒ | B | 61 | 27 | ᛡ | IA/IO | 107 |
| 8 | ᚺ | H | 23 | 18 | ᛖ | E | 67 | 28 | ᛠ | EA | 109 |
| 9 | ᚾ | N | 29 | 19 | ᛗ | M | 71 | | | | |

### Validation gates (pipeline must pass all before the sweep runs)

1. Total LP2 (pages 0–55) rune count ≈ 12,956 (accept ±2% and investigate any deviation).
2. Doublet count across the corpus ≈ 86 (order-of-magnitude check on the anti-doublet leak).
3. Decryption smoke tests reproducing known results:
   - Page 1 "A Warning": Atbash (index -> 28 - index) yields "BELIEVE NOTHING FROM THIS BOOK...".
   - "Welcome" pages: Vigenère over indices, key DIVINITY, with the ᚠ rule (see below) yields "WELCOME PILGRIM TO THE GREAT JOURNEY...".
   - If these fail, the transcription or the encoding is wrong — stop and fix.

## 3. Cipher model and the ᚠ interrupter

Known behavior on solved pages: encryption is `C = (P + K) mod 29` on rune indices, EXCEPT ᚠ (index 0), which appears in ciphertext unencrypted. Sources differ on keystream behavior at ᚠ: (a) the key position does not advance, or (b) the running key resets at each ᚠ. This ambiguity matters for cross-page pad reuse, so expose it as a parameter:

**Phase 1 (this handoff's core): positional, masked.** Assume the pad is consumed 1:1 by position. Mask (exclude from scoring) any aligned position where EITHER stream has ᚠ. This is conservative and exact if the pad stream is used verbatim.

**Phase 2 (only if Phase 1 is null): consumption-aware variants.** Re-index the pad so its consumption skips/resets at plaintext-ᚠ positions, variants (a) and (b) above. Each variant is a per-pair re-indexing; runtime impact negligible, programming effort ~2–4 h. Note variant (b) implies massive pad reuse and is likely already covered by the ledger's exclusion of pad restarts — check first.

## 4. The sweep (Phase 1 spec)

For every ordered pair (M, N), M != N, over pages 0–55 (optionally + 56, 57 plaintexts as extra pads):
- For every relative offset o in [-(len(N)-1), len(M)-1]:
  - Align windows, mask positions where either rune == 0 (ᚠ).
  - `D = (C_M - C_N) mod 29` on surviving positions.
  - Score the 29-bin histogram of D with chi-squared vs uniform; also record index of coincidence.
  - Discard windows with < 50 surviving positions.
- Variants to include in Phase 1 (cheap, just more pad arrays): pad = N forward; pad = N reversed. (Palindromic N||reverse(N) and lag-shifted self-alignments can wait for Phase 2.)
- Record every (M, N, o, orientation, n_masked, chi2, IoC) to CSV — full results, not just top hits. A clean null over this space is itself a publishable, ledger-worthy elimination.

## 5. Verified performance (from a synthetic benchmark, 2026-11-13)

Reference numpy kernel (appendix A) on 56 synthetic pages of realistic lengths (~13k runes total):

| Quantity | Value |
|---|---|
| Ordered pairs | 3,080 |
| Windows scored | 1,133,920 |
| Full sweep runtime (both directions incl. reversal doubles this) | ~7 s |
| Null global max chi2, 5 Monte Carlo shuffles | 77.8 – 82.3 (tight) |
| Bonferroni threshold, alpha 0.05 over 1.13M tests, chi2(28 df) | 87.8 |
| Planted signal (real LP-style English, 168 unmasked runes) | chi2 = 128.6 — 56% above MC max |
| Estimated detection floor | ~90–110 unmasked runes (excess scales ~linearly in n) |

Memory is trivial (<100 MB). No GPU, FFT, or suffix structures needed.

## 6. Calibration plan

1. Asymptotic Bonferroni (free): flag windows with chi2 > 87.8 (recompute for your actual window count W).
2. Monte Carlo (cheap, do it): shuffle runes within each page (destroys alignment structure, preserves per-page frequency), rerun the full sweep, record the global max. 20 shuffles ≈ 2–3 min at the benchmark rate. Treat the empirical MC max as the operative threshold.
3. Go criterion: any window exceeding the MC global max by >10%, AND surviving a sanity re-check with the alternative ᚠ handling. Then crib-drag: guess headings from known LP vocabulary (THE, WELCOME, PILGRIM, KNOW THIS, BELIEVE, PARABLE...) and propagate across the aligned window.
4. Report a clean null honestly: "cross-page pad reuse at all pairwise offsets, both orientations, positional consumption" eliminated — that is a real contribution to the elimination ledger.

## 7. Effort-vs-runtime tradeoffs (read before optimizing)

- **The kernel is NOT the bottleneck.** Brute force in numpy runs the entire pairwise space in seconds. Do not spend a single hour on FFT convolution, suffix automata, C extensions, or GPU kernels for Phase 1 — that effort buys nothing.
- **Spend the effort budget on data integrity instead.** Validation gates in section 2 (double-transcription diffing, smoke-test decryptions) are where this project lives or dies. A single systematic transcription error invalidates every downstream statistic; a slow-but-correct pipeline beats a fast wrong one.
- **Calibration: asymptotic + 20-shuffle MC is enough for Phase 1** (~3 min total). A 1,000-shuffle MC (~2 h) is only worth it if a window lands within ~10% of threshold. If you ever need that, a numba `@njit` port of the kernel (est. 1–2 h work, 10–50x speedup) beats rewriting in C++; GPU only makes sense if the variant grid grows >10x (Phase 2 orientations x consumption models x palindromic pads).
- **Variant discipline:** every orientation/consumption variant multiplies runtime linearly but also multiplies the multiple-comparison burden. Keep Phase 1 small (2 orientations), log the exact search space you tested, and let the MC calibration absorb the actual number of windows scored — never hand-wave the test count.
- **Check the community ledger before adding variants.** Re-running an excluded hypothesis (autokey, periodic keys, boundary restarts) wastes the one resource this project actually consumes: your time. The ledger is at github.com/Dukotah/cicada3301 (`liber-primus/PICKUP-HERE.md`, `ELIMINATION-LEDGER.md`).
- **Doublet-alignment pre-filter (optional heuristic):** if a page's ciphertext is reused as a pad, the positions of ᚠ/interrupter events may correlate between true pairs. A cheap alignment-count screen could triage pairs before full scoring — but it assumes a specific encryption mechanism and can produce false exclusions. Only use it as a prioritization hint, never as a filter that removes pairs from the final tested set.

## 8. Deliverables

- `data/` — validated corpus, one file per page, integer rune indices, plus `SOURCES.md` with fetch URLs, hashes, and the diff report between the two independent transcriptions.
- `validate.py` — the section-2 gates, failing loudly.
- `sweep.py` — Phase 1 sweep (adapt appendix A), writing `results/sweep_phase1.csv`.
- `calibrate.py` — Monte Carlo null, writing `results/null_maxima.csv`.
- `REPORT.md` — search space exactly as tested, null distribution, top-20 windows, go/no-go conclusion, and (if null) the proposed ledger entry in the community's elimination format.
- Tests: pytest cases asserting the two known decryptions reproduce.

## Appendix A — Reference kernel (validated; adapt freely)

```python
import numpy as np

def sweep_pair(A, B, min_len=50, q=29):
    # A: candidate encrypted page (int array 0..28). B: candidate pad page.
    # Masks rune 0 (Fehu interrupter) in both streams; scores all offsets.
    m, n = len(A), len(B)
    offs = np.arange(-(n - 1), m)
    I = np.arange(m)[None, :]
    J = I - offs[:, None]
    valid = (J >= 0) & (J < n)
    Jc = np.clip(J, 0, n - 1)
    Bm = B[Jc]
    valid &= (A[None, :] != 0) & (Bm != 0)
    D = (A[None, :] - Bm) % q
    rid = np.broadcast_to(np.arange(len(offs))[:, None], (len(offs), m))
    sel = valid.ravel()
    keys = rid.ravel()[sel] * q + D.ravel()[sel]
    counts = np.bincount(keys, minlength=len(offs) * q).reshape(len(offs), q)
    tot = counts.sum(1)
    chi2 = np.full(len(offs), np.nan)
    ok = tot >= min_len
    exp = tot[ok, None] / q
    chi2[ok] = ((counts[ok] - exp) ** 2 / exp).sum(1)
    return offs, chi2, tot
```

## Appendix B — English-to-rune mapping for synthetic power tests

Char-level (conservative — real LP plaintext compresses digraphs TH/NG/EA/AE/OE/EO/IA into single runes, which only strengthens detectability):

A24 B17 C5 D23 E18 F0 G6 H8 I10 J11 K5 L20 M19 N9 O3 P13 Q5 R4 S15 T16 U1 V1 W7 X14 Y26 Z15 (drop spaces/punctuation)

## Appendix C — If the sandbox has no network

Generate 56 pages of uniform random rune indices (lengths 150–320), plant one pair with `C_M = (P + C_N) mod 29` using appendix B text, and verify the pipeline recovers it at chi2 >> MC max (expected: signal ~128 vs null max ~82 at len ~168). Leave `data/README.txt` telling the human exactly where to drop validated transcriptions.
