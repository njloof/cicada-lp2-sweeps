# Campaign #9 report — reading orientations × mirror pairs (2026-11-orientations)

Run 2026-11-15/16. **Verdict: NEGATIVE — all four families** (details and
numbers below). Pre-registered before output at `ab28743` (PREREG.md; CI
gate); runner + labeled corrections at `6b5d63d`. Corpus: book-page labels
(post-relabel `2089fc2`), sha256 `9f5f14d4…483e` (sorted concat of
`data/pages/lp2_*.txt`), 55 unsolved pages, p50 runeless excluded as
target. Instrument `core/kernel.py` UNCHANGED.

## Space and declared collapses (measured, not assumed)

Orientation group {id, rl, rg, r180} on both pages of a pair: 16 combos →
**8 classes** by the proven r180-composition collapse (χ² reversal-invariance;
diagonal o maps to (m−n)−o). Output-blocking pilot on 3 real mirror pairs
(all 8 collapse pairs × diff/sum): **exact match, PASS**, re-run before
every obs pass. The sum operand-order collapse was FALSIFIED at registration
(tgt mask is target-side; 23/24 real-pair maxima differ) — sums scanned in
BOTH orders; PREREG carries the labeled correction.

**Control arm PASS:** O2 (all ordered id-only pairs, diff+sum, both orders)
reproduces #1's best cross-page diff max **81.08** (4>20, o=−208, n=59) and
#2's sum max **83.92** (37>53 [old label 52], o=103, n=121) BIT-EXACTLY —
harness and corpus unchanged; O1 results are valid.

## Families, windows, observed maxima

| fam | space | windows | obs max | key (offset, n) |
|-----|-------|---------|---------|-----------------|
| O1 | 27 mirror pairs × 8 classes × 4 directed ops | 317,416 | 89.41 | `7-48 id.rl sum(M,N)` (−66, 204) |
| O2 | 55×54 ordered pairs × {diff,sum} (control) | 2,189,160 | 83.92 | `37>53 sum` (103, 121) = #2 max |
| T1 | token tables p49/p50/p51, 8-token rows, 8 classes, both ops/orders, idx-246 variants | 8,128 | 62.55 | `canon p51−p50 id.rl diff` (−31, 69) |
| T2 | pad = a·(T mod 29), a∈2..28, 3 tables × 55 pages | 1,945,188 | 94.75 | `canon p49 a=26 → p17` (20, 75) |

Total **4,459,892 windows / 497,493,630 positions** (PREREG estimated ≈3M —
the estimate predated the second look at O2's ordered-pair count; measured
figure here, as registered to report). Zero-check: 0/8 classes flagged.

## Null — and two disclosed rerun events

Family-specific target-shuffle MC of the FULL family max (orientations,
pairing, ops, offsets all inside the max), 20 draws, seed 20261126:

| fam | draws | min | median | p95 | max | obs | p (draws ≥ obs) |
|-----|-------|-----|--------|-----|-----|-----|-----------------|
| O1 | 200 (escalated) | 71.12 | 80.37 | 90.44 | 96.81 | 89.41 | **0.055** (11/200) |
| O2 | 20 | 80.54 | 88.24 | 103.03 | 106.76 | 83.92 | 0.800 |
| T1 | 20 | 59.08 | 66.94 | 71.64 | 76.47 | 62.55 | 0.950 |
| T2 | 200 (escalated) | 80.76 | 91.63 | 103.43 | 110.97 | 94.75 | 0.320 (64/200) |

(20-draw figures, before escalation: O1 med 81.10 / max 95.17 / p=0.050;
T2 med 90.86 / max 102.90 / p=0.250 — the escalation sharpened O1's p from
the suggestive 1/20 to 11/200: persistent but far below any defensible
threshold, and 89.41 is nowhere near the registered 1.1×max bar.)

Disclosed implementation failures, both caught and rerun BEFORE any verdict
(artifacts kept in `work/orientations/`):
1. **Salted RNG stream**: family stream offset used `abs(hash(fam))` —
   Python salts `str.__hash__` per process, so draws were not reproducible
   from the pinned seed. First 20-draw run discarded; offset replaced with
   `crc32(fam)`. (Draws were statistically valid — independence held — but
   metadata seed-pinning would have been a lie.)
2. **Token-grid bug**: `tok_read` modeled tokens as 2-byte units (rows of
   16 bytes). Dukotah's `canonicalize.py` is explicit: 8 tokens per row,
   one byte per token (p51 r8c7 → 184+7·8+6 = idx 246 ✓). T1 non-id
   orientations had been applied on the wrong grid; fixed, obs rerun (T1 max
   65.07 → 62.55), null rerun. T2 unaffected (id-orientation only); O1/O2
   unaffected. The null-seed fix and this fix land in the same clean rerun.

## Escalation (PREREG rule: obs ≥ family null median → ≥200 draws)

Fired for **O1** (89.41 ≥ 81.10) and **T2** (94.75 ≥ 90.86); O2/T1 sat
below their medians (no escalation). 180 additional draws each on the same
crc32-seeded per-draw streams (draws 20–199), 758 s wall on 8 cores.
Verdicts held: O1 p=0.055, T2 p=0.320. One disclosed tooling bug: the
parallel path's checkpoint prefix-flush stalled (rescan started at the
pre-run length instead of the current one — all 360 draw values recovered
bit-exactly from the run log and re-verified against the flushed prefix;
bug fixed in `run_par.py` with a comment).

## GO prongs

| prong | requirement | status |
|-------|-------------|--------|
| 1 | obs > 1.1 × family null max | FAIL all families (best: O1 89.41 vs 1.1×96.81 = 106.5) |
| 2 | mask=both survives, n ≥ 50 | top O1 window survives (86.31, n=196) — moot without prong 1 |
| 3 | decode fwd+rev vs crib list | **0 substantive hits** in 80 leaders × 2 directions (one 3-letter chance match `…YNMWEBRAJ…`; expected FP ≈ 0.5) |
| 4 | bonus: scheme hits second pair | rl-class leaders do recur (7-48, 0-55, 8-47 all id.rl top rows) — but with no significant max this is pattern, not evidence |

**No GO.** Crib list note: the "25-crib house list" of #1–#8 was never
committed (disclosed gap); #9 versions it in `core/cribs.py` as the union of
the two transcript-recovered variants (36 words, 32 representable in the
29-rune alphabet — no V/K/Q/Z).

## Power (seed 20261127, 10 plants/family)

Plant = crib-English residues (cycled `PIGRIMWITNINTHETUNNEL`) written into
the pad page so the planted window decodes to crib text; recovery = planted
row is the max over the planted pair's whole scan (all classes/ops/orders —
a plant surfacing under the wrong class would be a plumbing bug) AND χ² ≥
family null median. A physical plant lights BOTH mirror rows
((no-flip,+off) with D=res and (flip,−off) with D=−res; negation permutes
χ² bins → identical statistic), so either row counts.

| fam | registered criterion | argmax (planted row wins pair) | note |
|-----|----------------------|-------------------------------|------|
| O1 | **10/10** | 10/10 | hypothesis arm fully powered — the negative is informative |
| O2 | 10/10 | 10/10 | control sensitivity confirmed |
| T1 | **8/10** | 8/10 | 2 misses = orientation collisions in the tiny space (a different class's offset-0/full-overlap row beat the planted χ² 163–171); all 10 ≥ median |
| T2 | 3/10 | 8/10 | **registered criterion structurally unreachable**: planted windows are ≤72 tokens (χ² 67–82) vs family median 91.6 inflated by 1.9M windows — same failure mode as #7's Vs (n≳90). T2's NEGATIVE is therefore WEAKLY POWERD; argmax coverage 8/10 shows the plumbing works (2 genuine misses at a=28) |

O1's 10/10 matters most: if an orientation-pair design existed at
crib-strength signal, this campaign would have found it.

## idx-246 / token-table provenance disclosure

T1/T2 scanned BOTH variants: `canon` = shipped `canon_256.bin` (idx 246 =
**0xc6**, 3I — matching our pixel adjudication and the owner's read) and
`e0` = the dissenting-witness reading (root+relikd 3i; also what
`canonicalize.py` reproduces on the pinned witness lineage). dukotah's own
CAMPAIGN-VII doc hex (0xe0) is stale against their shipped bin — doc/bin
drift disclosed in docs/STREAM_TAIL_EVIDENCE.md; upstream follow-up on
issue #14 pending owner approval.

## Runtime and regeneration

Observed sweep 28 s local (PREREG estimated <2 min — held). 20-draw null
~8 min local (serial, checkpointed). Escalation 360 draws (O1,T2 → 200):
758 s wall via `run_par.py` on 8 cores (bit-identical by per-draw stream
reconstruction; draw values verified equal to the serial prefix).

```
python3 sweeps/2026-11-orientations/run.py --phase obs      # pilot + sweep
python3 sweeps/2026-11-orientations/run.py --phase null     # 20 draws serial
python3 sweeps/2026-11-orientations/run_par.py --fams O1,T2 --draws 200  # esc
python3 sweeps/2026-11-orientations/decode_check.py         # prong 3
python3 sweeps/2026-11-orientations/power.py                # plants
```

Full sweep CSVs (8.2 MB total) in gitignored `work/orientations/`; sha256 in
`results/obs_maxima.csv`. Tracked results files are complete (max 12 KB).

## Not covered (as registered)

Columnar/transposed reads; boustrophedon; triple products; position-
dependent pads; interleavings; literal word-sum U3 (→ #10); red-digit/red-
matrix selection channels (awaiting owner double-check); ornaments;
LP1-as-target; p50 as target. Additional measured limits: T1/T2 token
streams (72–104 positions) cannot exceed the family null median by
construction at planted-signal strength — power section quantifies.
