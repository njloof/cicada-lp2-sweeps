# Campaign #21 PREREG — separator-skeleton qualification (registered 2026-11-17, BEFORE any campaign output)

Owner queue: MAP slot 10 ("6c constraint-based crib design, English-first").
Step 1 (punctuation census) DONE pre-registration as descriptive tabulation
(red_census precedent; commits d61c7c0/87a6c90/cbd525b). This PREREG covers
the hypothesis tests.

## Context (pre-existing facts, NOT outputs of this campaign)

- Separator channel VALIDATED on p57 (the only page where PT = CT, direct
  transliteration): within-line dashes at true word boundaries 15/15;
  ◆4 = sentence period 2/2; ◆23 = book-end 1/1; line wraps split words
  WITHOUT dashes (3 cases). (design pass, 4a0225d)
- Census: krisyotam 181 dots = 19 plain + 165 ◆ (◆4=129 after owner
  stipulation: line-final ◆3 + next-line initial '-' = one ◆4, both marks
  removed — stipulated, not measured); 17 quote marks bare in blocks.
  Dots 127 medial / 18 final / 3 initial. Split on '-' AND '.'/quotes:
  3,371 words, mean 3.91.
- p56 CT (85 runes) decodes via phi-prime totient, skip-null-F, 1 null
  (established CI, core/tests): PT = ANENDWITHINTHEDEEPWEBTHEREEXISTSAPA
  GETHASHES TOITMROEFOYONEAEUERYPILGRIMTOSEECOUTTHISPAGE (84 chars;
  spacing per word segmentation below).
- DESIGN-PASS PEEK DISCLOSURE: while verifying the position-mapping
  mechanics I glanced at the first four p56 dash positions vs PT boundaries
  and saw a MIXED picture (some boundary hits, at least one apparent miss).
  The exact statistic was NOT computed before this registration; V1 below
  is the first computation. This peek lowers prior confidence; it does not
  change the statistic or the verdict rule.

## Hypothesis

H: the `-`/`◆4` separator skeleton of the UNSOLVED pages is plaintext-text
structure (words/sentences), as p57 proves it is on the one checkable page —
so it may be adopted as crib constraints for future decodes.

## Gates (deterministic; any FAIL = abort, report, no verdict)

- G1 corpus: N = 12,956 over pp0–49,51–55 (core.validate); census
  reproduction via punct_text_census logic: ◆4 = 129, ◆13 = 32, ◆10 = 3,
  ◆23 = 1, quotes 14 `"` + 3 `'`, inline dots (folded) = 148.
- G2 p57 reproduction: dash-boundary 15/15, ◆4-period 2/2, ◆23 1/1,
  wraps-without-dash = 3 (script re-derives from blocks + translit, no
  hard-coded counts).
- G3 p56 decode: brute_interrupters reproduces ('skip', 1 null, 3 crib
  hits); PT length 84. Design-pass finding (mechanics only, registered
  here): the canonical signed plaintext (dukotah solved_plaintext.txt,
  PGP block) reads "AN END WITHIN THE DEEP WEB THERE EXISTS A PAGE THAT
  HASHES TO … IT IS THE DUTY OF EUERY PILGRIM TO SEEK OUT THIS PAGE" =
  91 letters, but the rune stream holds only 85 runes (84 after 1 null)
  ⇒ the stream cannot encode the full canonical wording; the CI decode
  diverges from canonical in the mid-tail (HASHESTO→EUERY region) and
  shows TOSEECOUT for SEEK (the K→C conflation, owner-noted, in ground
  truth). The alignment instrument must therefore work by verified
  regions, not whole-text mapping (V1).

## V1 (primary, confirmatory): p56 dash ↔ PT word-boundary alignment

- Dash positions: every `-` between runes in the p56 block rune segment
  (krisyotam), converted to CT stream indices (◆/¶/§/`*` contribute 0).
  Cross-check source: relikd `•` separators (independent transcription);
  disagreements listed; primary statistic uses the block.
- Verified-region instrument (registered, deterministic):
  1. decode D = CI decode output (84 chars, skip/1-null convention);
  2. canonical C = signed plaintext letters (91, hash lines excluded);
  3. A = difflib.SequenceMatcher(None, D, C).get_matching_blocks(), kept
     blocks of length ≥ 4, canonical side merged alphabet (K→C,V→U,Z→S,
     Q→C); each kept block maps decode positions → canonical positions;
  4. aligned decode positions = those whose canonical image is a
     canonical word-start (words per the signed text);
  5. dashes whose decode position lies outside kept blocks are EXCLUDED
     and listed (registered exclusion, not silent).
- Statistic: k = aligning dashes of n (n = dashes inside verified
  regions). Null: place n separators uniformly at random among the G
  gaps that lie inside verified regions; B' = aligned slots.
  p = Σ_{i≥k} C(B',i)C(G−B',n−i)/C(G,n) (analytic hypergeometric,
  seedless).
- Verdict contribution per rule below.

## V2 (gate, tooling): merged-alphabet scorer blind holdout

- Scorer (deterministic): merged-alphabet (K→C,V→U,Z→S,Q→C) quadgram score
  (dukotah english_quadgrams.txt) + koan crib hits (core/cribs.py) +
  mean-word-length plausibility vs 3.9–4.4.
- Task: rank true p56 PT and true p57 PT above 1,000 letter-shuffle decoys
  each (seed 20261221, same length, same merged alphabet).
- PASS iff both true texts rank #1. Fail ⇒ scorer not usable as decode
  scorer; campaign records SCORER-FAIL, V1 still reported.

## V3 (report-only, non-falsifying per #18 rule): per-unit skeleton panel

- 11 v2 units: word-length χ² vs LP2-native koan corpus (p56+p57 PT words,
  ~110 words — small-corpus caveat); sentence lengths (words between dots)
  mean/range; quote pairing (17 marks: open/close distance). Descriptive.

## Verdict rule (pre-registered)

- SKELETON-QUALIFIED: V1 p < 0.05 AND V2 PASS → separator skeleton adopted
  as crib constraint set for future decode scoring (constraints: word
  lengths, sentence breaks, quote positions, merged alphabet).
- SKELETON-PAGE-DEPENDENT: V1 p ≥ 0.2 → channel real on p57 only; p56
  skeleton is noise; unsolved-page skeleton demoted to suggestive; crib
  constraints NOT adopted; feeds oracle round (why does p56 differ?).
- 0.05 ≤ p < 0.2: INCONCLUSIVE — no adoption, no rejection; #22 candidate.

## Disclosures

- Design-pass peek above.
- p56 PT segmentation includes W-drop quirks (community-established);
  tolerance classes pre-specified to avoid post-hoc boundary widening.
- relikd vs block separator disagreements (if any) listed, not silently
  reconciled.
- V2 shuffles are a weak null (destroy structure trivially); random-English
  decoys reported but not gated.
- LP2-native koan corpus is 2 pages; V3 is descriptive by construction.

Runtime: seconds, single machine (no studio). Deterministic + one seed.
