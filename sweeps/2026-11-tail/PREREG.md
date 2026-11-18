# Campaign #24 PREREG — tail closure: F3 affine residual + F10 mid-range cyclic + F14 LP1-as-target (registered 2026-11-18, BEFORE any campaign output)

Owner steer 2026-11-18: "run through the remaining tail candidates."
Three MAP-tail lanes, one campaign (precedent #12 = F17+F18). Per-lane
verdicts; a lane may finish while another runs.

## Premise facts (read-only, verified before registration, no decode output)

- F3 gap CONFIRMED from dukotah W2-C2 PREREG §3/§6.1: their 6.4M
  canon-as-key family is eps_j*C + eps_i*K + s with s in {0,1,28};
  their own not_covered clause excludes multipliers a != 1 AND the
  full Caesar layer. Our T2 (token->page affine) found no signal at
  planted strength.
- F10 gap from #6 PREREG guarantee 2: cyclic steps 2..28 (+rev-induced
  L-28..L-1) swept; steps 29..L-29 mid-range NOT covered. Registered
  pads 4,128; mid-range pads 26,250 (6.4x, incl. plaintext sources,
  fwd+rev). #6 AMENDMENT inherited: self-pair pads EXCLUDED (gcd
  fixed-point chi2 pileups; target-shuffle null structurally blind).
- F14: LP1 unsolved bulk = pp10-13 (~1,009 glyphs with no canon
  counterpart, dukotah B2 Part C). Two independent LP1 lineages exist:
  scream314 Unicode-rune transcription (ours, sources/scream314) and
  dukotah bitmap-derived index stream (armada18 lp1_runes_as_key.json,
  2,988 indices 0..28).

## Lane A — F3 affine canon-as-key residual (shrunk family, F13 lesson)

- Key K = our canon stream: books 0..49, 51..57 concatenated
  (12,956 + 85 + 100 = 13,141 runes; gate A-G1 asserts exactly).
  (dukotah's canon lane used 13,136 — lineage difference disclosed.)
- Family: p[m] = a*(C_j[m] + eps*K[o+m]) + s (mod 29), targets = 55
  unsolved pages, eps in {+1,-1}, a in 2..28 (a=1,s in {0,1,28} is
  their closed additive lane; a=28 kept - it is a Caesar-negation of
  the OTHER sign pattern, cheap), s in 0..28.
- Offsets (SHRUNK, disclosed): key start at each canon page start
  (58 alignments incl. o=0). Window L = min(len_j, lenK - o), skip
  L < 60. NOT covered: arbitrary-offset affine (their additive
  all-offset negative is the only coverage there); interrupter/skip
  transition models. Family size 55 x 58 x 1,566 ~= 5.0M decodes.
- Statistic: skeleton-LEGAL crib hits (36-crib merged vocab, MULTIWORD
  exempt, target-page skeleton, null mask empty - no interrupters in
  this family). m_n per page; M = max.
- Null: letter-shuffle surrogates of each page's best text,
  S=1,000/page, D=200, seed 20261224,
  per-replicate substreams Random(f"20261224:{d}") (resumable,
  bit-identical). p = (1 + #{nullmax >= M})/(D+1).
- Power: 3 plants - p56 true plaintext enciphered under in-family
  cells (a in 2..28, eps, s, key start = a real canon page start)
  scanned against p56's skeleton (p56 excluded from targets; used as
  plant carrier). Pass: planted cell legal hits >= 3 (the #23-calibrated
  bar). Plants test the scorer, not the key.
- Verdict: AFFINE-HIT (p<0.05 -> FLAG FOR OWNER REVIEW, never
  auto-certified) / AFFINE-NULL (affine residual closed at page-start
  coverage).

## Lane B — F10 mid-range cyclic steps (W harness extension)

- Family: pad = [S[(a*j + c) mod L] for j in range(L)], a coprime in
  29..L-29, cuts C(a) = {(a*floor(i*L/k)) mod L : i<k},
  k = ceil(L/(L-49)); fwd+rev; sources = #6's sources (pages + solved
  plaintexts); self-pair pads excluded (AMENDMENT inherited).
  26,250 pads, ~611M windows.
- GATE B-G1 (pre-scan, no output): exhaustive alignment-coverage check
  of the cut set for MID-RANGE steps (guarantee-1 machinery extended
  to 29..L-29). If violations: k-boost rule - raise k per source L
  until complete (deterministic; k used is disclosed). Abort if no k
  <= 16 achieves completeness.
- Statistic: chi2 vs uniform over 29 bins of (A - pad) mod 29
  (harness-native; shift-invariant by construction, so no Caesar
  dimension). Observed max over all (target, pad, orient, offset).
- Null: target-shuffle MC, 20 draws, seed 20261225, single sequential
  shuffle stream pre-drawn then scans parallelized (bit-identical
  stream, parallel execution); vectorized scan_max path with #6's
  startup self-check (scan_max == pair_scan loop on real streams).
- Decision rule (#6 inherited): GO iff obs > 1.1 x null-max AND
  mask=both survival AND English cribs in the decode. Escalation
  (obs >= null median) -> extend to >=200 draws before verdict.
- Runtime: observed ~1.2 h, null ~7.5 h serial local; parallelized
  (per-target / per-draw, multiprocessing) est. < 30 min total on
  this machine; studio offload (scripts/studio.sh, 28 cores) only if
  local exceeds ~1 h wall - RNG stream unaffected either way.

## Lane C — F14 LP1 pages as targets

- Lineage gate C-G1 FIRST (output-free): parse scream314 LP1 rune
  lines -> codepoints -> 29-index alphabet via our gematria set;
  report non-LP2 runes and their handling; cross-check against
  dukotah's 2,988-index stream (best-offset positional agreement
  reported; no pass threshold - this is a fidelity disclosure, per
  "transcription lineage check first"). Targets: LP1 pages from
  scream314 with >= 60 runes.
- Family: phi-prime keystream page-aligned x {skip, hold} x all
  null-combos over ciphertext-F positions, capped max_f = 20
  (LP1 futhark is F-rich; if F > 20 the combo space is truncated at
  20 and the truncation count is disclosed - #23 pages were all <= 17,
  LP1 may not be).
- Statistic: RAW crib hits (36-crib merged vocab) - NO skeleton
  constraint: LP1's bullet separators are NOT a qualified skeleton
  (#21 qualified LP2 dashes only); power lower than #23, disclosed.
  m_n per page, M = max; score_text for ties.
- Null: letter-shuffle surrogates, S=1,000/page, D=200,
  seed 20261226, per-replicate substreams. p = (1+#{nullmax>=M})/(D+1).
- Power: plants - p56/p57 plaintext enciphered page-aligned under
  in-family cells against LP1-length carriers; report whether planted
  page exceeds the null-max bar.
- Verdict: LP1-HIT (p<0.05 -> flag for owner) / LP1-NULL (phi-prime
  family retired for LP1 too, coverage as stated).

## Global gates

- G1 corpus N = 12,956 (books 0-49, 51-55).
- G2 dukotah LP1 stream: len 2,988, all values 0..28.
- G3 #23 census reproduction (skeleton module sanity): F4=129.

## Disclosures

- Lane A shrinks offsets to page-starts (F13 shrink-the-family
  lesson); a hit at a non-page-start affine alignment would be
  missed - coverage stated.
- Lane B inherits #6's mask/floor geometry (mask=tgt primary,
  mask=both survival prong; floor 40 tracked).
- Lane C's phi-prime-on-LP1 prior is LOW: phi-prime is an LP2
  convention (p56 only); LP1 is heavily mined by dukotah (dup risk
  high, owner accepted by steering the tail).
- No lane auto-certifies anything; all hits are flags for the owner.
- Runtime estimates at registration: A ~5 min; B ~30 min parallel
  local (priced from measured 139k win/s loop, 1,072 pair/s vector);
  C minutes (F-capped). Total same-day, no studio unless B stalls.

---

## POST-REGISTRATION CORRECTIONS (appended 2026-11-18; sealed text above untouched)

1. Lane A canon length: PREREG said 13,141 (12,956+85+100) — arithmetic
   slip, p57 is 95 runes. Measured 13,136, EXACTLY dukotah's canon
   length: the disclosed lineage difference does not exist; gate A-G1
   asserts 13,136.
2. Lane A page starts: 57, not 58 — p50 is the runeless hole and is not
   in the book list; no alignment is lost (0-rune page start coincides
   with its successor).
3. Tooling (disclosed): studio.sh SYNC_PATHS extended with `docs`
   (docs/img excluded — 14 MB owner crops) and the single file
   sources/dukotah/liber-primus/data/english_quadgrams.txt, so
   core/skeleton works on the Studio. Owner steer 2026-11-18: run on
   studio.local. Lane A ran there (564 s); RNG streams untouched
   (letter-shuffle substreams seeded per replicate; identical either
   host).
