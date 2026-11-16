# Campaign #11 PREREG — LP2 word-sum self-keys (F1 / U3)

Registered 2026-11-16, **before any sweep output** (CI gate). Queue slot 3
(docs/MAP.md §G). Corpus sha256 `9f5f14d4…483e`, book-page labels.

## Hypothesis

LP2's own word structure (delimited by its printed dividers) carries a
self-derived key schedule: a decode C − key(word-geometry of C) shows
value-distribution structure beyond chance on some page. This is the
word-boundary analog of campaign #8's line-sum LS family (NEGATIVE, power
10/10), and the LP2-internal analog of dukotah's LP1-sum schedules
(R37-C1-U2, negative).

## Dup-check (both ledgers, run before registration)

| reading | who | status |
|---|---|---|
| LP2 word sums as cleartext SYMBOL stream | dukotah R10-L2 (R1–R9), R37-C3-U5-L3 | NEGATIVE |
| LP1 word/line/sentence sums as keystream | dukotah R37-C1-U2 | NEGATIVE (bounded) |
| separator identity/shape/run-length as message | dukotah R11-S2, R44-P3(b1/b2/b3) | NEGATIVE — "typography" |
| **LP2 own word sums as self-key SCHEDULE** | — | **open in both ledgers** (R10-L2 `not_covered`: "sums as keystream (not symbol stream)"; "counts used as KEY SCHEDULE … (not as message)") |
| LP2 LINE sums as self-key | ours #8 (LS) | NEGATIVE, power 10/10 |

Honest prior: LOW. Their separator-typography finding (identity stream
0.81 bits/token, punctuation-like frequencies) argues separators carry no
message. Counter-consideration registered up front: a key derived from the
word geometry of an underlying plaintext would produce exactly
typographic-looking separators — the typography finding weighs on
separators-as-message, not on separators-as-key-boundaries.

## Object (premise census — PINNED at registration)

krisyotam witness (`sources/dukotah/.../krisyotam_runes.txt`), segs 0–54
(= book pages 0–49 + 51–55; tail +1 shift per docs/STREAM_TAIL_EVIDENCE.md):

- 12,956 runes, **bit-identical to data/pages/lp2_NN.txt on all 55 pages**
  (verified at registration)
- separators on the unsolved stream: `-` = 2,729, `.` = 173
- words (maximal rune runs delimited by `-` or `.`): 2,928; mean length
  4.4249; max 14; min 1; 99 one-rune words; every page ≥ 17 words
- word-length distribution (top): 3×726, 4×514, 2×465, 5×318, 6×252, 7×214,
  8×159, 1×99

**Kill gates:** G1 12,956 + bit-identical (above); G2 separator/word counts
match the census exactly; G3 no page with 0 words. Any fail → abort, no
verdict.

**Caveats (registered):** divider geometry is single-root (krisyotam;
relikd agrees on the RUNES — dukotah P3 §Step-1, 12,956/12,956 — but not
independently on separators; owner's p51 read corroborates dividers on one
page). Word segmentation ignores `/` line marks (declared; `/`-delimited
variant not covered).

## Families (page-local, self-derived, additive)

Word w, page-local; Σ(w) = sum of rune VALUES in w (mod 29). Decode
D_i = (C_i − key_i) mod 29 for rune i in word w:

- **WS1 self-word**: key = Σ(w). NOTE structural degeneracy: one-rune
  words have D ≡ 0 identically → WS1 χ² computed over runes of words with
  len ≥ 2 only (99 words excluded, declared here).
- **WS2 prev-word**: key = Σ(w−1); first word of page → key 0.
- **WS3 word-length**: key = len(w) mod 29.
- **WS4 running-word-sum**: key = Σ of all rune values in words strictly
  before w on the page, mod 29.

## Statistic + null

Per family, per page: χ² over 29 value cells of the decoded page runes
(language-agnostic; no English adjudication at scan time). Family statistic
= **max over the 55 pages**. MC p = (1 + #{null ≥ obs})/(D+1).

Null: **derive-from-shuffled** (the #8 method win — mandatory since keys
are self-derived): per draw, per page, uniformly permute the page's rune
values (word geometry fixed), re-derive keys from the permuted stream,
recompute the family max. D = 20 initially.

**Escalation (house rule):** any family with obs ≥ its null median → 200
draws on disjoint per-draw streams. Streams: `default_rng([20261130,
crc32(tag) % 100000, draw])`.

**Verdict rule:** family fires if MC p ≤ 0.05/4 = 0.0125 (Bonferroni over
4 families; MC-of-the-max is the calibration, not a band). A firing family
additionally requires its argmax page's decode to hit ≥1 of the 25-crib
roster (fwd+rev) before any "flag" language; else "structure, no reading".
**Mandatory power sentence** in the report regardless of verdict.

## Power (plants)

Per family, 10 draws: random page, window = 8 consecutive whole words;
crib = values drawn from solved p56/p57 plaintext value distribution
(English-strength); plant forward pass sets C_i := crib_i + key_i with
self-derived keys recomputed as we go (WS1 closed form per word:
S = Σcrib/(1−|w|) mod 29, valid for |w| ≥ 2). Assert decode(C') = crib on
window inside each plant. Power = fraction of plants whose page χ² exceeds
the family's 20-draw null p95.

## Cost

4 families × 55 pages × ≤201 draws + 40 plants — estimated <60 s local.
No studio offload.

## Not covered (declared up front)

Beaufort sign (key − C); modulus 28; keys crossing page boundaries;
`/`-line-delimited segmentation; digitsum/other key transforms; separator
IDENTITY channels (theirs, closed); word CONTENT/semantics; decoded-layer
word boundaries (chicken-and-egg); non-English registers; p50 (runeless);
LP1-side sums (theirs).
