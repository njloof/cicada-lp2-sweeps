# Campaign #12 report — sexagesimal census (F17) + in-document OTP (F18)

Run 2026-11-16. Queue slot 4. Registrations: census `CENSUS.md`
(descriptive, no gate, c44081c); PREREG `d478ca9` as amended **before any
output** by PREREG2 `60d2857`. Verdict: **census MEASURED (premise
correction) + PB1 NEGATIVE, WEAKLY-POWERED** (mandatory power sentence
below).

## Part 1 — F17 census: the premise changed

The "Babylonian sexagesimal margin digits pp34–39" of both ledgers are
**two conflated objects**:

1. **A black cuneiform-like stamp** — ONE device, pixel-identical (maxdiff
   0, independently re-verified) on the tops of pp34–39 + a footer
   instance on p33. It brackets the pp33–39 section and carries **no
   per-page information**; its only content is its glyph values (unknown)
   and its placement (constant). Machine wedge-counting **failed and is
   disclosed** (fused strokes; erosion merges, DT over-segments) —
   identification went to oracle round #3 (S1–S3, sheets in
   `docs/img/oracle/sex60_*.png`), which is exactly dukotah W2-B2's
   unclosed item ("identification against real cuneiform sign lists").
2. **Red printed digits 1–5** on pp36–38 (values known from
   `docs/RED_CENSUS.md`; owner round-1 confirmed). Their LP2-nativeness
   (wedge vs printed) is the owner's open round-#2 F3 answer; if printed,
   they are not consumable data.

## Part 2 — PB1: page→blob reverse scan

The registered consumption test (queue: "page→blob reverse scan"): page
runes select entries of the 256-byte base-60 token table
(`canon_256.bin`, sha pinned), D_s,p[i] = B[(v[i]+s) mod 256] mod 29,
228 offsets × 55 pages × sliding windows W=60/stride=30; statistic = max
window χ² (~88k windows); null = derive-from-shuffled (permutation
preserves every marginal exactly, destroys order).

**Pre-output amendment (disclosed):** v1's page-MARGINAL χ² under a
value-independent key is provably a function of the value counts alone →
the registered null was degenerate (null ≡ obs). Proof is two lines
(PREREG2); **zero v1 output exists**. v1 marked SUPERSEDED-BEFORE-RUN;
the windowed statistic is the first order-sensitive register.

| quantity | value |
|---|---|
| obs | 253.20 (p35, s=26, win 210) |
| null (D=20, seed 20261201) | median 280.27, p95 304.24, max 318.93 |
| MC p | **1.0** — obs sits BELOW the null median |
| escalation | not fired (obs < median) — D stays 20 |
| power | **0/10** English-strength plants vs p95 |
| runtime | 0.23 s (PREREG estimate <60 s — held) |

## The power sentence

**PB1 is NEGATIVE and weakly powered against English-strength plants
(0/10).** Mechanism (instrument lesson #2, the mirror of campaign #11's):
under a FIXED MANY-TO-ONE output map (29 runes → ~18 classes through the
table), the window χ² is dominated by the STRUCTURAL concentration
inherited from the page's value marginal (null median ≈ 280); a 35-rune
English window shifts the statistic by less than the null spread
(p95−median ≈ 24). A powered re-run would need class-conditional or
order-sensitive statistics (crib matching, bigrams) — a new registration,
and **not recommended**: the table is 7.17 bits/byte measured high-entropy
(dukotah), and every consumption reading of it — theirs (index, pad,
self-gematria) and now ours (reverse selection) — is negative.

Side observation, recorded honestly: the real pages decode *flatter* than
random permutations of themselves (obs < median). That is an anti-signal
well inside noise; nothing should be built on it.

## Enumerations (no verdicts, as registered)

- **E1** selected lines: p36L6 n=25 (first T), p37L1 n=23 (J), p37L5 n=20
  (J), p37L10 n=19 (EA-digraph rune), p38L4 n=23 (H); p10L8 n=21 (Y, the
  black 7). Cross-check: non-empty krisyotam line counts pp34–39 =
  [12,12,11,11,11,12] — **exact match to dukotah T3**, so the line
  indexing is anchored.
- **E2** stamp placement: bracket {33…39}, header×6 + footer×1, constant
  → placement-as-key is vacuous.

## Files / regeneration

```
python3 census_sex60.py     # census re-verification + oracle sheets
python3 f18.py              # PB1 full pipeline (stage 20, auto-escalate)
```

## Not covered (as registered)

Stamp glyph values as pad/selector (pending oracle S1/S2); red-digit
value consumption (pending owner F3); blob→page affine a≠1 re-power
(queue slot 6, F13); transpositions; mod 28; Beaufort sign; non-English
registers; p50 internals; class-conditional statistics (see power).
