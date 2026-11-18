# Campaign #23 PREREG — skeleton-constrained phi-prime sweep, all 55 unsolved pages (registered 2026-11-18, BEFORE any campaign output)

Owner queue: MAP slot 11 (new, owner "Go" 2026-11-18). First decode
application of the adopted separator skeleton (#21 SKELETON-QUALIFIED;
core/skeleton.py, pruned interrupter sweep wired and tested).

## Hypothesis

H: at least one unsolved page decodes under the p56 convention family —
phi-prime keystream aligned to page start, ciphertext-F interrupters
(skip/hold), English koan-register cribs — well enough to beat the
family's own null as adjudicated by the skeleton-pruned scorer.

## Coverage statement (doctrine: coverage x power, report both)

Family tested: phi-prime page-aligned keystream ONLY; skip and hold
null conventions; ALL null subsets over ciphertext-F positions (F<=17
on every page; total enumeration 499,604 combo x convention decodes
over 55 pages); 36-crib merged vocabulary (core/cribs.py); skeleton
legality constraint (word/sentence marks, merged alphabet). NOT tested:
other keystreams/alignments, other languages, keyphrases. A null
retires THIS family for unsolved pages (shape of #15's retirement).

## Statistic

- Candidate = (page, null-combo, convention) decode; text = translit,
  uppercased, merged alphabet.
- legal_hits(candidate) = count of the 36 cribs occurring at >=1
  skeleton-legal placement (phrase cribs DEEPWEB/ANEND/HASHESTO exempt,
  #21 module).
- m_n = max legal_hits over page n's candidates (ties: raw hits, then
  quadgram score; best candidate retained per page).
- M = max over pages of m_n. Per-page m_n all reported (transparency).
- Solved pages 56/57 EXCLUDED (controls, below).

## Null (MC null of the max — house rule, never a raw p-band)

Per page: S = 1,000 surrogate texts = uniform letter-permutations of
that page's BEST-candidate text (preserves per-candidate letter
multiset: conservative, keeps non-uniform frequencies). Page null-max =
max legal_hits over its S surrogates. Global null-max = max over pages.
D = 200 replicates, seed 20261223. p = (1 + #{null-max >= M}) / (D+1).
Deterministic crib scan; shuffles seeded.

## Gates

- G1 corpus N = 12,956 (books 0-49, 51-55).
- G2 p56 control: interrupter_sweep(56, [DEEPWEB,PILGRIM,HASHESTO])
  reproduces true combo (skip,(47,)) with legal 2 / raw 3 (the
  documented mid-tail-divergence value; test_skeleton.py).
- G3 skeleton census reproduces #21 G1 counts (◆4=129 etc.).

## Power (planted controls, text-space; disclosed semantics)

After the run: pick 3 pages by seeded draw; in each, splice a crib
(length-matched to a legal slot) into the page's best-candidate text at
a legal position; recompute m_n; report whether planted page exceeds
the null-max threshold. Tests the SCORER's sensitivity, not the key
hypothesis (disclosed limitation).

## Verdict rule (pre-output)

- PHI-SKELETON-HIT: p < 0.05 -> the winning page+combo is FLAGGED FOR
  OWNER REVIEW (visual + crib reading). NOTHING auto-certified; no
  decode claim.
- PHI-FAMILY-NULL: p >= 0.05 -> phi-prime+interrupter family retired
  for unsolved pages, coverage as above, power from plants.
- Either way: per-page table + top candidates persisted (work/, size
  gate).

## Disclosures

- Design-pass peek: NONE beyond already-published facts (p56/p57
  solved values, skeleton counts). No unsolved-page decode output has
  been computed before this registration.
- phi-prime page-alignment is an assumption inherited from p56 only;
  p57 needs no key. If pages use another alignment this run cannot see
  it (coverage, above).
- Legal-placement constraint is defined in true-plaintext letter space;
  wrong-convention decodes are penalized by design (demonstrated on
  p56's shifted PILGRIM).
- Runtime: 499,604 decodes + null 55x1000x200 crib scans; estimated
  < 10 min local single machine; no studio (RNG stream seeded here).
