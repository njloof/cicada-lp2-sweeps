# Campaign #25 PREREG — tail hand-offs: F3′ arbitrary-offset affine + LP1 plaintext confirmation (registered 2026-11-18, BEFORE any campaign output)

Owner steer 2026-11-18: "write up and execute the remaining tail
handoffs" (the two open items recorded when #24 closed) + standing rule:
nontrivial compute on studio.local.

## Lane D — F3′ affine canon-as-key at ARBITRARY key offsets

#24 Lane A closed affine at PAGE-START key offsets; dukotah's additive
all-offset negative covers only a=1. This lane covers a != 1 at
arbitrary offsets, via a crib-anchored inversion (forward scan would be
55 x 13,136 x 27 x 29 x 2 ~= 2.3T decodes — infeasible; inversion shrinks
to slot anchors, F13 lesson).

- Cell family (unchanged from Lane A except offsets):
  D[m] = a*(C_j[m] + eps*K[o+m]) + s (mod 29), eps in {+-1}, a in 2..28,
  s in 0..28, page-aligned (key position for rune m is o+m), o ANY offset
  with decode window L = min(len_j, 13136 - o) >= 60. Targets: 55
  unsolved pages. K = 13,136-rune canon (books 0-49,51-57).
- Inversion: for a crib w (merged, 36-crib vocab), a rune-space preimage
  sequence R (merge + digraph TH/EO/NG/OE/AE/IA/EA expansions; 37 total
  preimages across the vocab, enumerated exhaustively — no cap needed),
  a page rune start t, and (u = eps*a^-1, eps, s): the required key
  window is K[o+t+m] = u*(R_m - s) - eps*C_j[t+m] (mod 29); look the
  window up in a per-length hash of all canon windows (13,136 windows x
  lengths 3..13). Surviving (cell, anchor) pairs are deduped to cells.
- ANCHOR SHRINK (disclosed coverage limit): anchors are SLOT-ALIGNED —
  single-word cribs must fill a whole word slot (start = slot start,
  length = slot length; 2,767 slots over 55 pages, skeleton nulls=());
  MULTIWORD cribs (DEEPWEB, ANEND, HASHESTO) may start at any slot start
  and span slots (exempt, ~8.3k anchors). A hit whose crib occurrence
  starts mid-slot or mid-rune (inside a digraph) is NOT found.
  Justification: dashes are verified word boundaries (#21); cribs are
  words.
- Statistic: per surviving cell, full-window decode -> merged text ->
  skeleton-LEGAL crib hits (hits_of, nulls=(), target-page skeleton,
  MULTIWORD exempt). M = max over pages; p vs null.
- Null: letter-shuffle surrogates of each page's best text, S=1,000/page,
  D=200, seed 20261227, per-replicate substreams Random("20261227:{d}")
  (resumable, bit-identical). p = (1 + #{nullmax >= M})/(D+1).
  Multiplicity note: length-3 anchors (WEB) expect ~3.6e5 spurious
  survivors (13,136/29^3 per needed window x 1,624 (u,s,eps) per slot);
  the null is built on the same survivor-max structure and absorbs it.
- Power plants: p57 PT (PT=CT) enciphered at 3 cells with key start at
  NON-page-start offsets (mid-page: p20 start + 31, p33 start + 7,
  a in 2..28, eps, s), scanned through the identical inversion path;
  pass = planted cell legal hits >= 3 (#23 bar).
- Verdict: AFFINE2-HIT (p<0.05 -> FLAG FOR OWNER REVIEW, never
  auto-certified) / AFFINE2-NULL (arbitrary-offset affine residual closed
  under the stated anchor shrink).

## Lane E — LP1 pages under the corrected premise (plaintext confirmation)

#24 Lane C premise correction: scream314 LP1 is a mixed-format doc;
pp11/12 are English plaintext, LP1 bulk is "largely readable koan
English". This lane tests that premise mechanically on the 9 LP1 rune
pages (>=60 runes, scream314 lineage) and closes the simple-layer
residual.

- Families per page (trivial size): affine letter maps x -> (a*x + s)
  mod 29 over rune indices, a in 1..28 (a=1 = Caesar incl. identity;
  a=28 = atbash), s in 0..28, x fwd and reversed stream: 1,624 decodes
  per page, 9 pages = 14,616. No phi-prime (retired by #23/Lane C), no
  interrupters.
- Statistic: merged quadgram log-prob per letter (core/skeleton scorer
  vocab, english_quadgrams.txt), best over the family per page.
  Secondary: crib hits of the best decode (reported, not tested).
- Null: per page, letter-shuffle of the page's own letters (multiset
  preserved), S=1,000 shuffles, family max per shuffle, D=200 replicate
  draws, seed 20261228, per-replicate substreams. Per-page p; Holm
  across the 9 pages.
- Controls: p56/p57 true PTs through the scorer (must land English-high:
  >= -1.6/letter); raw identity decode of pp11/12-style English reported
  if present. Power: a planted English page under an affine cell must be
  detected (identity-vs-shuffle sanity).
- Verdict: any page surviving Holm with English-level score ->
  LP1-PAGE-PLAINTEXT (FLAG FOR OWNER: new ground-truth plaintext, never
  auto-certified; would be the first LP2-side read of LP1 content).
  Else LP1-SIMPLE-NULL (identity/Caesar/affine/atbash/reverse retired
  for the 9 LP1 rune pages; phi-prime already retired by Lane C).

## Global gates

- G1 N = 12,956 (55 unsolved pages). G2 canon len 13,136.
- G3 census F4(diamond-4)=129. G4 preimage enumeration = 37 total.

## Disclosures

- Lane D anchor shrink (slot-aligned, above) is the only coverage gap
  vs the full arbitrary-offset affine family; window >= 60; no
  interrupter/skip model; key = canon only.
- Lane E pages are scream314 lineage (9.2% agreement with dukotah
  stream, #24 C-G1): a page readable here is readable in THIS lineage
  only; cross-lineage confirmation is owner/oracle work.
- No lane auto-certifies; hits are flags for the owner.
- Runtime estimates: Lane D ~30 s inversion + ~2 min survivors + null
  ~10 min on studio (priced from #24 Lane A 564 s at 5M decodes; here
  ~4.2e5 survivor decodes + same null shape). Lane E < 10 min studio
  including nulls (~2.9M quadgram scorings). All on studio.local per
  standing rule; local smoke tests only.
