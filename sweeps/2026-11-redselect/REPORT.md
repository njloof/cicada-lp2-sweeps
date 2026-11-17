# Campaign #15 REPORT — F2/F9: red digits 1–5 as selectors

PREREG: `PREREG.md`, commit `2931ab0` (before any output; CI gate).
Run 2026-11-16, seed 20261204, α = 0.05/3 ≈ 0.0167, MC D = 20,000/family.
Regen: `python3 sweeps/2026-11-redselect/f2.py` (8.6 s — PREREG estimate
< 60 s, held).

## Question

The five RED printed digits (owner-confirmed census: p36 L6=1, p37
L1/5/10=2/3/4, p38 L4=5) sit on stream lines. Do their VALUES select
anything that agrees — a position in their own line (D1), a line on their
page (D2), a word in their line (D3)? Statistic: coincidence pairs
Σᵣ C(nᵣ,2) over the five selected rune values (language-agnostic).

## Gates (all PASS)

57 krisyotam blocks; selected-line lengths exactly [25,23,20,19,23]
(campaign #12 E1 cross-pin); stream lines p36/p37/p38 = 11/11/11 (≥1/≥10/
≥5 required); L = 12,956 with per-page bit-identity vs `data/pages/`.

## Results — three NEGATIVEs, all powered

| fam | reading | selected (d→rune) | obs | null med/p95/max | p | ceiling p | min-achievable p | verdict |
|---|---|---|---|---|---|---|---|---|
| D1 | position-in-line (1-based) | T S Y D O | 0 | 0 / 1 / 6 | 1.000 | 0 (exact) | 0.00025 | NEGATIVE |
| D2 | line-index on page (1-based) | X R A B M | 0 | 0 / 3 / 10 | 1.000 | 1.06e-4 | 0.00030 | NEGATIVE |
| D3 | word-index in line (1-based) | T C NG U H | 0 | 0 / 1 / 2 | 1.000 | 0 (exact) | 0.01385 | NEGATIVE |

Every registered reading selects five MUTUALLY DISTINCT runes — obs = 0 in
all three families, sitting exactly at the null median. No flags.

**Power.** Min-achievable-p (smallest p any observation could receive under
the registered MC null) is below α in all three families, so these are real
negatives, not blind ones. D3 is the tightest: its largest null value is 2
(min-achievable p 0.01385 vs α 0.0167); any obs ≥ 3 would have been off the
null support and fired regardless.

## Enumeration (no verdict, per registration)

- D1 secondary, 0-based index d: Y R EO E I.
- p15 digit group and black 7: untouched (PREREG §0/§5).
- p53: owner F4 answered (L7/L8/L9 all-red, L6 last symbol red) — folded
  into PREREG §0; arrow semantics untested by design.

## Disclosures

1. **Pre-launch fix:** first launch died at gate G3 (12,949 ≠ 12,956) —
   krisyotam block index ≠ book page for pages ≥51 (empty p50 slot dropped,
   tail +1 shift; ws.py SEGS convention). Zero output under buggy code.
   Fixed to map blocks by BOOK position; DIGITS pages (36–38) unaffected.
2. **Pre-launch fix:** garbled family-assembly line (D3 observation) caught
   in review before any verdict was printed.
3. **Registered ceiling unreachable (D1, D3):** exact ceiling-p = 0 — no
   single value occurs in all five populations, so stat = 10 is impossible.
   The registered verdict rule was NOT changed; min-achievable-p was added
   as a DESCRIPTIVE power statement after the fact. All three families pass
   it anyway; verdicts are unaffected (all p = 1.0).
4. **D3 word population:** the five lines contain no '.' separators, so the
   registered '-' split equals campaign #11's full-separator split on the
   object under test. Trailing empty words (p37 L10 w7, p38 L4 w6) are
   excluded from null populations (declared; observed selections land on
   words 1–5, unaffected).
5. Stage-5 smoke run pre-launch (output gitignored `work/scratch/`,
   unused; verdicts meaningless).

## Reading

The red digits are real, owner-confirmed, RED — and under the three
in-document selection readings they select nothing that agrees. Combined
with campaign #7 (digits dead as additive keys) this retires the
"digit → position/line/word" family: the digits are either labels/counts
(section bookkeeping, cf. lattices-as-terminators) or keys for an external
object (page/line numbers into a different corpus — outside LP2's
self-contained scope). Remaining red-channel objects: p53 all-red lines +
arrow (oracle-identified, meaning open), p15 red 3299, 30-bit red-dot
stream (below floor).
