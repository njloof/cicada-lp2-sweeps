# Campaign #17 PREREG — language triage BEFORE crib design (MAP 6c, stage 1)

Registered 2026-11-17, BEFORE any campaign output (CI gate). Owner's design
objection (2026-11-17): "shouldn't we first determine what the plaintext
language is? if not English the crib misleads" — accepted; this campaign is
the triage that gates the 6c crib design. dukotah B6 (Latin/German/Welsh/
OE models over the archive) never fired, but it can only see
monoalphabetic-equivalent decodes — the true construction's language is
unresolved.

## 0. Objects

- **Unsolved word structure**: krisyotam `-`/`.` separators over book
  pp0–49, 51–55 (single-root fidelity caveat — owner's ◆-pass corroborated
  separators broadly; word-gap machine segmentation impossible, so the
  census rides krisyotam's dividers; disclosed).
- **Owner punctuation**: inline `'`/`"` marks from the completed pass
  (owner confirmed REAL: apostrophes "denoting contractions").
- **In-book English reference**: solved plaintext p56 + p57 words
  (~60 words — small-n disclosed; same book, same encoder, same style —
  the right reference class, unlike generic corpora).

## 1. Registered statistics (language-agnostic measurements first, then
one triage verdict; α = 0.05 single test)

**S1 — word-length histogram.** Bins {1, 2, 3, 4–6, 7+} over all unsolved
words. Report fractions + mean. Descriptive anchors (no verdict): English
continuous-text expectation ~ {5, 17, 23, 42, 13} %; Latin expectation:
1-letter ≈ 0 %, long-word mass high.

**S2 — short-word signature.** f1 = fraction 1-letter words, f2 = fraction
≤2-letter words. English text: f1 ~ 4–7 % (a/I), f1≈0 kills English;
Latin: f1 ≈ 0, f2 low (et/in ex.); French/Italian: high elision-apostrophe
rates. Descriptive against S1.

**S3 — apostrophe position class.** Per apostrophe: word-INITIAL (elision:
French/Italian l'/d'/n') vs word-MEDIAL (English contraction don't/it's) vs
word-final (possessive 's). Deterministic table. A single medial or final
apostrophe REFUTES the Latin hypothesis (Latin has no apostrophes); initial-
only with high rate would support Romance-elision over English.

**S4 — English-reference χ².** Statistic: χ² between unsolved histogram
(S1 bins) and the solved-page reference proportions, with MC null =
permutation of pooled (solved+unsolved) word labels, D = 20,000, seed
20261205. VERDICT: p > 0.05 → CONSISTENT-English (crib design proceeds
English-first); p ≤ 0.05 → DEVIANT (crib must be a parametric
multi-language family with per-language nulls — registered as a future
campaign, not run here). Reference n≈60 ⇒ LOW POWER disclosed: DEVIANT
readings may reflect reference noise; CONSISTENT is the weak direction.

## 2. Kill gates

G1: 57 blocks parse; separator geometry EXACT vs campaign #11 (2,729
`-`, 173 `.`). AMENDED pre-output (zero output had occurred): #11's
2,928-word count predates the tail relabel (its page set lacked book 55),
so the separator counts — which match bit-exactly — are the pin. G2: solved reference word list
reproduces from the Plaintext blocks verbatim. G3: L = 12,956.

## 3. Runtime

Text parsing + 20k permutations on 3000+ labels: **< 20 s**, local.

## 4. Not covered (declared)

Any decode, any crib testing (gated on this verdict), letter-frequency
language ID (needs the key), non-Germanic/Romance families (LP1 + solved
pages + Cicada publication history make them far priors), krisyotam
separator error model (owner pass is the current fidelity bound).
