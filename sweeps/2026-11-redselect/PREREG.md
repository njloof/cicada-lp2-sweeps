# Campaign #15 PREREG — F2/F9: red digits as selectors

Registered 2026-11-16, BEFORE any campaign output (CI gate). Queue slot 7:
"F2/F9 red-selection tests — slot-forward the moment oracle Task 1/2
confirms" — Task 1/2 confirmed round #1 (digits 1–5); F3 answered
2026-11-16 (printed, not wedge → sexagesimal reading dead; digits remain
red-channel marks).

## 0. Objects (owner-confirmed census; docs/RED_CENSUS.md)

Red digits (page, stream-line, value): **(p36, L6, 1), (p37, L1, 2),
(p37, L5, 3), (p37, L10, 4), (p38, L4, 5)**. Line lengths (campaign #12 E1,
krisyotam-anchored): 25, 23, 20, 19, 23.
Enumeration-only (no verdicts): black 7 @p10L8; p15 group
3278/**3299**(red)/3298/2838 (cumulative-rune-count hypothesis tested
2026-11-16 and REJECTED — nearest cum boundaries off by 84–178; disclosed,
stays unexplained); p53: **owner F4 answered 2026-11-16 — stream lines
L7/L8/L9 entirely red, last symbol of L6 red** (up-arrow after line 6);
red-dot 30-bit stream (below any windowed
statistic — descriptive pointer only, per MAP F2).

Dup-check: #7 (2026-11-number-channels) killed digits as ADDITIVE KEYS
(Vp/Vs/R_D). dukotah R44-P1 is census (213 runes). Selection TESTING of
these digits is open in both ledgers; campaign #12 E1 enumerated the
selected lines but never scored a selection reading.

## 1. Registered families (three verdicts, α = 0.05/3 ≈ 0.0167)

All statistics language-agnostic (value coincidences, no alphabet).
n = 5 selections — the honest constraint; ceilings are reported EXACTLY.

**D1 — digit → 1-based position within its own line.**
Selected value = line[L][d−1]. Statistic = coincidence pairs Σᵣ C(nᵣ,2)
over the 5 selected values. Null: each digit independently selects a
uniform position in its own line (MC, D = 20,000; preserves line value
compositions, destroys the digit→position link). Ceiling (exact): 10 =
C(5,2), attained iff all five selected values agree; ceiling p computed
analytically from the per-line value distributions.
Secondary reading (index d, 0-based) reported as enumeration, no verdict.

**D2 — digit → line index within its page.**
Selected = LAST rune of line d on the digit's page (p36 L1; p37 L2/L3/L4;
p38 L5). Statistic = coincidence pairs of the 5 last-rune values. Null:
uniform line index per page (MC D = 20,000). Gate G2: every needed line
exists (p36 ≥1, p37 ≥4, p38 ≥5 stream lines).

**D3 — digit → word index within its line.**
Words = krisyotam '-'-separated segments of line L (premise bit-identical
to campaign #11: 2,928 words, '-' separators). Selected = first rune value
of word d (wrap if page-line has < d words — declared). Statistic =
coincidence pairs. Null: uniform word position per line (MC D = 20,000).

**Verdict rule:** FIRE iff p ≤ α AND ceiling-p < α (a family whose ceiling
cannot reach α is declared STRUCTURALLY UNPOWERED up front and yields
enumeration, not a negative verdict). Any FIRE → crib/oracle registration
before interpretation.

## 2. Power

Ceilings are exact (all-five-agree constructions); ceiling p-values are
computed analytically under each family's null. No English plants are
meaningful at n=5 value-coincidences; the ceiling IS the power statement
(campaign #13 O3 precedent).

## 3. Kill gates

- G1: krisyotam parses to 57 page-blocks; selected-line lengths = [25,23,
  20,19,23] exactly (campaign #12 E1 cross-pin).
- G2: digit table = the 5 records above, exact; p37 has ≥10 stream lines,
  p38 ≥5, p36 ≥1.
- G3: corpus L = 12,956.

## 4. Seeds / runtime

Seed **20261204**; tags {"D1","D2","D3"}. All nulls are tiny-array MC —
estimated total runtime **< 60 s**.

## 5. Not covered (declared)

p15 4-digit groups (no anchor found); p53 arrow semantics (lines now
owner-identified, meaning untested);
30-bit red-dot stream testing (below floor — oracle/descriptive);
black 7 joint-channel variants; word-internal selections beyond first
rune; cross-page position readings; any two-digit COMBINATIONS as
two-digit indices (e.g. 1-2 → 12) — enumeration only.
