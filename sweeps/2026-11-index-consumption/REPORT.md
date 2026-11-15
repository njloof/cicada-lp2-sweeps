# Campaign 2026-11-index-consumption — REPORT

Run 2026-11-14. **Pre-registered before output** (PREREG.md + code, commit
`3e1f64e`, earlier than any campaign output). One labeled post-output
AMENDMENT section in the PREREG (cut-placement was fixed *before* output;
after output: a sort-only extraction bug, the self-pair degeneracy below, and
a supplementary power probe). Corpus hash, seed, exact counts: metadata.json.

## Verdict

| family | windows | observed max | MC null (20×, seed 20261120) | empirical p | verdict |
|---|---|---|---|---|---|
| P drop-decimation (all phases) | 13,460,746 | 94.95 (10←27:d3.0r o=66, n=76) | min 95.41 / med 101.84 / max 114.47 | ≈1.0 | **NEGATIVE** |
| W cyclic, registered (self-pairs included) | 79,771,062 | **195.2** (49←49:c23.3 o=5, n=60) | min 101.29 / med 107.36 / max 118.87 | 0.048 | **FLAG → EXPLAINED** (fixed-point degeneracy; not a GO: decode fails prong 3) |
| W cyclic, AMENDED (self-pairs excluded) | 78,048,642 | 105.4 (32←45:c23.0r o=−153, n=113) | min 101.29 / med 107.36 / max 118.87 (**identical to registered**, all 20 draws) | 0.5714 | **NEGATIVE** |

The amended null is **bit-identical to the registered null in all 20 draws**
(same seed): the null's argmax never touched the self-pair channel — which is
exactly what "structurally blind" means, now confirmed empirically rather than
by argument. The degeneracy lives only on the observed-data side.

Decision rule (fixed pre-run): GO iff observed > 1.1 × family null max **and**
mask=both survival **and** English cribs. P fails prong 1 (and sits below its
null *minimum*). The registered W passes prong 1 (195.2 > 1.1 × 118.87 = 130.8)
and prong 2 (mask=both 203.0) but **fails prong 3**: the decode is
`ᚠMFᚠCEᚠXVᚠKBᚠY\ᚠZRᚠ…` — an ᚠ pileup, not language. Not a GO. The flag is
fully explained mechanically (below).

**Total registered sweep: 93,231,808 windows** (P 13.46M + W 79.77M);
cumulative ≈329M across six campaigns.

## The self-pair fixed-point degeneracy (the 195.2 anatomy)

For a self-pair cyclic pad (pad source == target), D = A − A∘π with
π(i) = ±a·i + δ (mod L). π has exactly **gcd(a∓1, L) fixed points**, each a
guaranteed D = 0 (ᚠ). The χ² pileup is manufactured by arithmetic, not content:

- **16/16** rows above χ² = 130 are self-pairs; every one has gcd(a±1, L) ≥ 22.
- Observed D-zero fraction matches g/L + (1−g/L)·IoC within ~0.01:
  page 49 (a=23, L=66, g/L = 1/3): predicted 0.358, observed **0.350**, χ² 195.2;
  pages 4/12 (a=28, L=261, g/L = 1/9): observed 0.16–0.17.
- The target-shuffle null is **structurally blind**: it shuffles the target
  against the *real* pad, destroying exactly the self-agreement the degeneracy
  exploits (pad ⊥ target is assumed by construction). Escalating to 200 draws
  would resolve nothing — more draws of a null that cannot see the channel.

**Amendment (labeled, in PREREG):** self-pair pads excluded from W in both
scan and null (`--exclude-self`). Amended observed max 105.4 vs its own
matched null (median 107.36): **p = 0.5714, negative, escalation not
triggered**; mask=both 105.4→110.0 (n 113→108), decode `K[RNKNKXZURLJKXPDBWY…`
— noise through and through. The degeneracy is instrument-general, not campaign-local:
*any* permutation-style self-pair scan can manufacture ᚠ pile-ups this way, and
shuffle-of-target nulls will not see them. (Retrospective note: #1's observed
max was itself a self-mirror at p ≈ 0.10 — the mild version of the same channel;
#1's cross-page best, 86.4, was never competitive, so its verdict stands.)

## What was swept

- **P** — drop-decimation `S[b::a]`, a∈2..28, **all phases b<a** (closes our
  phase-0-only gap from #3/#5 and dukotah's "widths ≠ 4" gap), fwd+rev;
  surviving widths {2,3,4,5} (≥6 length-vacuous, disclosed).
- **W** — cyclic (wrap-around) reads `[S[(a·j+c) mod L]]`, a∈2..28 coprime to
  L, cut set spread in the step-a coordinate with **exhaustive alignment
  coverage verified at startup** (59 sources × all coprime steps × all
  alignments × all 55 targets × real ᚠ positions: 0 violations), fwd+rev.

## Power (coverage × power, both probes)

- **Registered plant** (D = target's own runes — near-uniform ciphertext):
  P 0/10 and W 0/10 reach the null median. Correct answer to a weak question:
  the registered plant is not what an encryption signal looks like.
- **Supplementary plant** (English-strength plaintext, IoC ≈ 0.066; labeled
  post-hoc, AMENDMENT A3): P **3/10** recovered at the median threshold, and
  the planted window became the family global max (141.3 > null max 114.5);
  W **7/10** recovered (longer windows ⇒ more power), planted window again
  the family global max (189.1 > null max 118.9). A true pad at English
  strength in a ≥50-rune window would surface in these families' top rows;
  recovery at the median alone is ~30–70% at n ≈ 50–175 (per-plant variance
  of plaintext strength dominates the threshold).
  (Registered-plant W scan reports planted-corpus max 175.17 — that is the
  surviving page-7 degenerate self-pair window, target 7 not being among the
  planted set; another face of the same degeneracy.)

## Ledger entry

> **Index-consumption sweep (2026-11-14, preregistered).** The consumption-rule
> axis: drop-decimation pads S[b::a] with **all phases** (P; widths {2..5},
> closes phase-0-only and widths≠4 gaps) and cyclic wrap-around reads
> S[(a·j+c) mod L] with cut sets giving **provably complete alignment
> coverage** (W; exhaustive check, 0 violations). 93,231,808 windows; 20×
> per-family MC null of the global max (seed 20261120). P: observed 94.95 <
> null min 95.41 — **negative** (p ≈ 1.0). W: registered observed 195.2 >
> 1.1×null max — flag raised, then **explained**: 16/16 extreme rows are
> self-pair permutation scans whose gcd(a±1,L) fixed points manufacture ᚠ
> pile-ups (zero-fraction matches g/L + (1−g/L)·IoC); decode non-English →
> fails the registered GO's third prong; target-shuffle nulls are structurally
> blind to self-agreement. Amended W (self-pairs excluded, matched null —
> bit-identical to the registered null, confirming the channel's one-sided
> location): observed 105.4, p = 0.57 — **negative**. Power: English-strength
> planted pads surface (planted window becomes family max; 7/10 recovered in
> W). **Not covered (pre-declared):
> mid-range cyclic steps 29..L−29; non-uniform interleavings; triple products;
> digit/ornament channels; page 55; LP1 (by design).**

## Disclosures

1. **CHI2_COL off-by-one (sort-only):** tracked top-100k CSVs initially sorted
   by n_valid (column index copied from #5 where `k` shifted χ² to 6). Heap
   membership, window counts and obs_max use the true χ² and were always
   correct; tracked CSVs regenerated from the intact full `work/` files
   (deterministic re-sort; full-file sha256 unchanged).
2. **Self-pair degeneracy** — see anatomy; PREREG AMENDMENT A2.
3. **Supplementary power probe** is post-hoc, labeled (A3); the registered
   probe is reported unchanged alongside it.
4. **p57 ≡ PARABLE57 stream duplication** (as #5): visible as identical
   49←57 / 49←PARABLE57 rows; duplication cannot inflate a max.
5. Mask=both numbers are sensitivity-only (no nulls of their own); the amended
   W leader moves 105.4→110.0 (n 113→108) — noise-consistent.
6. Single-2017-root transcription caveat and page-55 exclusion carry over;
   regeneration: `python3 sweeps/2026-11-index-consumption/run.py` (registered)
   and `run.py --exclude-self --skip P` (amended W), full CSVs to
   `work/index-consumption/`.
