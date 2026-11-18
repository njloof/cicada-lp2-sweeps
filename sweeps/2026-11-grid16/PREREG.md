# Campaign #22 PREREG — p15 grid as 16 stream pointers (registered 2026-11-18, BEFORE any campaign output)

Owner queue: MAP slot 9 follow-up after round #7; owner chose option (a)
"grid-as-16-pointers". Object: the RECORDED p15 4x4 decimal grid, 16
numbers row-major:
3258 3222 3152 3038 / 3278 3299(red) 3298 2838 / 3288 3294 3296 2472 /
4516 1206 708 1820. Recorded in ORACLE_PAGES p15 L2 + relikd + rtkd
(three witnesses). Context (NOT re-tested here): containment 11/16 void
p=3.3e-7, 12/16 span p=3.3e-8, row 4 fully outside, consecutive digit
sums only in red row — seen pre-registration (round #7), carried as
discovery context, not confirmation.

## Hypothesis

H: the 16 numbers are stream positions selecting content in the unsolved
corpus stream (N = 12,956 over books 0-49, 51-55).

## What is touched vs untouched (disclosed)

- Row 2's 4 numbers: doublet hits glanced in #20 (0 hits, both 0/1-based
  conventions); 5-letter raw transliterations seen (UOEWT/OWGEA/ACUO/
  IUIU, gibberish, never crib-scored).
- The other 12 numbers: NO statistic ever computed at their positions.
- Registered statistic uses all 16; row 2's doublet contribution is
  fixed at 0 by the #20 glance, so the S1 datum is effectively the 12
  untouched positions (disclosed; all-16 p is slightly conservative).

## Conventions (registered)

- Global stream = flat(book) for books 0..49 then 51..55; N=12,956
  (gate G1).
- Position convention: PRIMARY 0-based global index; SECONDARY 1-based
  (index-1). Holm across the two.
- Doublet site = global index of the FIRST rune of an adjacent-identical
  pair within a page (site count ~86, gate G2; within-page only, per
  core.validate Gate 4 definition).

## S1 (primary): doublet-site hits

k = count of the 16 positions landing on doublet sites. Null:
hypergeometric, K = site count, n = 16 draws from N. p = P(X >= k).
Power (disclosed): expected hits 0.106; P(>=1)=0.101, P(>=2)=0.0050 —
near-blind at k<=1 by construction.

## S2 (secondary): phi-prime aligned-window crib scan

Registered convention: the phi-prime keystream is globally aligned to
the corpus stream start (p56's page-local success is the only prior;
alternative alignments have zero power here — disclosed). For each
position g (0-based only), window = 12 runes [g, g+12); aligned naive
decode P[i] = (C[g+i] - K[g+i]) mod 29 (NO null-F handling — a global
null map does not exist); transliterate; count CRIBS hits on the merged
alphabet (all 36, phrase cribs included — no skeleton constraint here,
positions are not word-aligned). Statistic: total hits over 16 windows.
Null: MC, 16 uniformly random valid positions, identical rule,
D = 20,000, seed 20261222; p = (1 + #{null >= obs}) / (D+1).

## S3 (report-only): window transliterations + row-4 contrast

Print the 16 window decodes; contrast rows 1-3 (inside void/span) vs
row 4 (fully outside) descriptively. No p-values.

## Gates

G1 N = 12,956. G2 doublet site count == 86 (core.validate Gate 4 map).
G3 grid rows == recorded witnesses (exact 16-number match).

## Verdict rule (pre-output)

- GRID-SELECTS: any of {S1-0b, S1-1b, S2} survives Holm (alpha 0.05)
  -> grid adopted as selector channel; follow-up = what it selects.
- GRID-NULL: none survives and at least one test was powered
  (S2 observed > 0 but beatable, or S1 k >= 2 not reached with
  P(>=k) measurable) -> pointer reading retired for p15.
- GRID-NULL-WEAKLY-POWERED: all observed zeros and all near-blind ->
  honest weak label; pointer reading SUSPENDED, not retired; feeds
  oracle (ink-channel sweep option (b) remains).

## Disclosures

- Grid seen pre-registration (owner S12 answer 2026-11-18) — this
  campaign tests a NEW channel (pointer semantics), not the containment
  facts; the selection of pointer-semantics as the test was made after
  seeing containment (post-hoc channel choice, disclosed).
- #20's frozen confirmation already closed the containment reading as
  one-off; nothing here reopens it.
- Runtime: MC 20k x 16 windows x 36 cribs, < 60 s local, no studio.

---

## POST-REGISTRATION CORRECTIONS (appended 2026-11-18; sealed text above untouched)

1. FIRST COMPLETED RUN INVALID (disclosed per discipline): the S2 MC
   early-break capped `beats` at 101/20000 when obs=0, producing
   p=0.0050 and a spurious GRID-SELECTS verdict. With obs=0 the null
   total is >= 0 with probability 1, so p=1.0 by construction. Fixed
   (MC skipped when obs=0) and re-run; no numbers from the invalid run
   were used.
2. Instrument lesson: never early-break an MC on a beats cap without
   first handling the obs=0 degenerate case (#21 lesson family:
   boundary conditions of the statistic itself).

3. (2026-11-18, external review; LEDGER C2) The grid has a CLOSED FORM:
   |3301 − prime(F+1)| over distinct Fibonacci F = 0…987, square spiral from
   the red 3299 (16/16 vs the recorded 4×4; regression-gated in
   core/validate.py gate 6). The pointer reading tested here is DEAD — the
   values are a known object, not pointers — and the containment premise
   inherited from #20 is RETRACTED (eleven small-F cells lie in 2838–3299 by
   construction). The 0/16 measurements stand; the interpretive framing is void.
