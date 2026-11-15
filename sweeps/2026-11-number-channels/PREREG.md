# Campaign #7 PREREG — number channels as additive keys (2026-11-number-channels)

Registered 2026-11-15, before any campaign output exists.
Hypothesis: some LP2 unsolved page is `plaintext + numeric key`, where the key
is a **designed number sequence** from the LP1/LP2 solved material, a
**position-dependent page-number ramp**, or the page's own **printed digits**
— the "their numbers are the direction / either the words or their numbers"
clue, operationalized. Converges with Dukotah O4 untried U2 (LP1 numbers as
key schedule, "NEVER" run as of R39) and their zero-hit "page-number-as-key"
gap; our instrument is ours: language-agnostic χ², family-max MC null.

## Statistic (unchanged instrument)

D = (A − K) mod 29 over maximal-overlap windows, ᚠ-masked (tgt mask primary,
both for confirmation), MIN_LEN 50, χ² vs uniform 29 bins. Detection is
order-invariant (a reversed plaintext scores identically), so no reversal arm
is needed at the statistic level; decode adjudication reads BOTH directions
(post-#6 standard).

## Key families (the space swept)

**V — value sequences.** Sequence sources, computed at run time from the
pinned corpus (plus the md-printed A WARNING values, see caveats):
1. SOME WISDOM (05.jpg) md-wrapped line sums: 468, 853, 1039, 1237, 157,
   341, 1015, 562, 1015, 341 (first five = the community phrase sums;
   mirror-palindromic tail; 4/5 prime — verified in docs/PLAINTEXT_PALINDROMES.md)
2. A WARNING (01.jpg) printed line sums 757, 1009, 691, 353, 769.
   [Pre-output verification, 2026-11-15, during code build — no campaign output
   involved: these are **plaintext**-side line sums and the md wrapping
   reproduces them exactly. PTAW (plaintext line sums, all 10 md lines) =
   [332, 757*, 1009*, 691*, 353*, 769*, 911*, 1051*, 859*, 677*] — lines 2–10
   are **9/9 prime**, exactly dukotah's claim; line 1 (332) is the title line.
   The earlier "757 vs 758" mismatch was ciphertext-side only. docs/
   PLAINTEXT_PALINDROMES.md updated accordingly.]
3. WELCOME (03.jpg) md-wrapped line sums (computed)
4. DIVINITY Vigenère key numbers 6, 19, 28, 19, 20, 19, 13, 3
5. per-line sums of the four solved plaintext streams (AWARNING, WELCOME,
   ANEND56, PARABLE57) — the words' numbers, line granularity
6. matrix magic constant 1033 and its emirp 3301: single constants are
   **excluded** (constant shift = symbol permutation = χ²-invariant — same
   collapse argument as #3's k∈{0,1,28}); they enter only inside longer
   sequences (e.g. digit expansions 1-0-3-3, 3-3-0-1).

Transforms per sequence: value → {v mod 29, φ(v) mod 29, digitsum(v) mod 29}
× {direct, cumulative-prefix-sum} × {sign +, −} × {forward, reversed}
= 24 variants (dedup identical variants). Each variant is applied at **all
cyclic phases** (key length p ⇒ p phases) to every target page.

**R — page-number ramps.** K_i = (c·i + b) mod 29, i = window position,
c ∈ 1..28 (c = 0 excluded: constant, χ²-invariant), b ∈ 0..28. 812 keys per
target; tests "page number as position-dependent key" (zero-hit gap).

**D — printed digits.** Inline digits pages 10, 36, 37, 38 (`7`; `1`; `2-3-4`; `5`)
as periodic keys for their own page (phases = period). `1` and `7` alone are
constants → excluded per the invariance rule; `2-3-4` and `5-` … digit streams
of length ≥ 2 only. Disclosed: this family is nearly empty by corpus fact
(6 digit glyphs total in the stream).

## Null and decision rule (house standard)

- Per-family MC null of the global max: 20 in-page-shuffled target draws,
  seed 20261122, identical scan path.
- Escalation: obs ≥ family null median → extend to ≥ 200 draws before verdict.
- GO requires all three prongs: (1) obs ≥ 1.1 × family null max;
  (2) survives mask=both; (3) English cribs in the decode, read forward AND
  reversed. Otherwise NEGATIVE (or FLAG→EXPLAINED with anatomy).
- Self-pair degeneracy guard: none of these keys are permutation self-pads,
  but any flag gets the #6 anatomy pass (gcd fixed-point check does not apply
  to additive ramps; instead: check key-period artifacts — a period-p key
  concentrates D onto p cosets, so the null is drawn with the SAME key set).

## Power probe (registered)

Plant: A′ = E + K_window where E = English-strength stream (IoC ≈ 0.066,
solved-plaintext pool) and K = one key from each family at a random phase;
10 targets, seed 20261123; report recovery at family null median. A negative
is only published with its visibility statement.

## Cost

Space ≈ 150k windows (V ~105k, R ~45k, D ~dozens). Observed sweep: seconds.
Null: 20 × same ≈ under a minute per family. Escalation (200 draws) ≈ 10×.
Measured per the #6 lesson: the scan here is the vectorized path end-to-end.

## Caveats / not covered (declared up front)

- Word-boundary **self-keys** (word sums advancing a skip on the same page) =
  Dukotah U3; deliberately not duplicated here.
- Prime-sum **recognizer** clause (U4) is a scoring layer for candidate
  decodes, not a key space — out of scope; our census already verified its
  LP1 evidence (4/5 SOME WISDOM) and its LP2 absence (chance-level 56/57).
- Book-code / signed-number retrieval (U7), direction geometry (U8),
  circumference/ornament channels (no transcription exists — see
  docs/TRANSCRIPTION_AUDIT.md), reversed page-key ORDER (thread-56; LP2 page
  keys are unknown, nothing to reverse), page 55, LP1-as-target (LP1 is
  solved; only its numbers enter, as keys here).
- md line-wrapping caveat for A WARNING/WELCOME sums (item 2 above).
- Single-2017-root transcription caveat carried (docs/TRANSCRIPTION_AUDIT.md).

## Seeds

null 20261122; power probe 20261123.
