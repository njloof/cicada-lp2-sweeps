# Plaintext/palindrome census (LP1 + LP2 solved material)

Compiled 2026-11-14, after campaign #6 closed the cross-page pad geometry.
Question: the decoded plaintexts point at "palindrome"-style clues — what is
actually there, verified from our corpus, and what reading do they support?
Everything below is recomputed from the hash-anchored corpus / scream314
transcription, not quoted from community claims. Coverage of the *other* team's
untried list (Dukotah `analysis/round36/O4-clue-coverage/untried.md`) is noted
per item so we inherit rather than duplicate.

## Verified structures (computed here)

1. **SOME WISDOM (LP1 05.jpg) line prime-sums** — first five line sums
   (Gematria Primus, primes 2..109): `468, 853*, 1039*, 1237*, 157*`
   (asterisk = prime). 4/5 prime; matches the community's printed figures
   exactly, now verified directly from the rune transcription. Chance rate for
   sums of this size is ≈ 1/ln(s) ≈ 14%, so 4/5 ≈ p 0.001 — structure.
2. **SOME WISDOM mirror line-sums are exact palindromes**: lines 6–10 sum to
   `341, 1015, 562, 1015, 341`. This is the page's 180° rotational symmetry
   showing up at the line-sum level (mirror lines carry the same rune
   multisets). Consistent with the verified word-cell gematria equivalences
   (SHADOWS≡CABAL=341, BUFFERS≡MOURNFUL=199, CARNAL≡ANALOG=320, …).
3. **Numeric matrix**: 180°-rotational symmetric magic square, constant
   **1033**; 1033 is an emirp whose reverse is **3301**. (Verified earlier;
   the matrix equals the Third-Onion out-of-band matrix.)
4. **LP1 A WARNING plaintext** carries deliberate-looking letter play:
   W-drops (`AWARNNG`, `CNOW`, `CNOWLEDGE`), K→C (`BOOC`), V→U (`BELIEUE`).
   The W-drop is specific to this page (DEEPWEB/WITHIN spell fine in LP2 56/57).
   **A WARNING prime line-sums VERIFIED (2026-11-15, campaign #7 code build):**
   the claimed sums are **plaintext-side**, and the md wrapping reproduces
   them exactly. Plaintext line sums, all 10 md lines:
   `[332, 757*, 1009*, 691*, 353*, 769*, 911*, 1051*, 859*, 677*]` —
   lines 2–10 are **9/9 prime** (dukotah's claim, confirmed; line 1 = 332 is
   the title line). P(9 primes by chance at ~0.14 each) ≈ 1e-8: designed.
   The earlier "757 vs 758" mismatch was ciphertext-side only — the design
   lives on the plaintext side, consistent with "either the words or their
   numbers".

## Negative results of this census

- **No textual palindromes ≥ 4 letters** in ANEND56 or PARABLE57 plaintexts.
  The "palindrome" clue is not letter-palindromes in the LP2 plaintexts.
- **LP2 56/57 line prime-sums are chance-level** (1/5 prime; unsolved-page
  baseline ≈ 25%). Consequence: the typos (MROE, FOY, AEUE, LICETHEIN…,
  DIUINITY, ANDE) are **not load-bearing for line sums** — there is no prime
  line-sum structure on those pages to protect. (The typo-load-bearing
  question stays open only for phrase/chunk sums, which is post-hoc fishing
  territory without a pre-registered chunk rule.)
- WELCOME/AWARNING palindromic substrings (URTRU, EAOAE, …) are short,
  word-boundary-crossing noise.

## What the clues actually point to (reading, ranked)

1. **Reversed/re-entrant reading order**, not letter palindromes: "AN END
   WITHIN…" (56) + "FIND THE DIUINITY WITHIN ANDE MERGE" (57) + a page that
   is literally its own 180° rotation (SOME WISDOM). dukotah thread-56
   (Symmetry Theory, PARTIAL) has the concrete untried version: reversed
   ORDER of known page keys across pages. Inherited, not duplicated.
2. **Numbers-as-key channel** (matrix 1033, phrase sums, LP1 numbers):
   dukotah U2 (LP1 numbers as key schedule) + U4 (prime-line-sum recognizer)
   — converges with our pre-declared digit/ornament gap (campaign #7
   candidate). Shared gap, highest priority.
3. **Circumference reading** of page edges: dukotah lists it untried; our
   corpus has no ornament/edge channel transcribed at all — blocked on
   transcription, see [TRANSCRIPTION_AUDIT.md](TRANSCRIPTION_AUDIT.md).

## Reproduce

All figures recompute from `core.validate` machinery: line sums via
`GEMATRIA` primes over per-line rune indices (scream314 sections `05.jpg`
etc.); plaintexts via the four CI decodes (`python3 -m core.validate`).
