# Campaign #11 report — LP2 word-sum self-keys (F1)

Run 2026-11-16. PREREG `955c597` (before any output; CI gate). Corpus sha
`9f5f14d4…483e`, book-page labels. Verdict: **NEGATIVE all families —
WEAKLY-POWERED** (mandatory power sentence below; read the negative with
it).

## What was tested

LP2's own word structure as a **self-derived key schedule** — the one
word-sum reading open in both ledgers after the dup-check:

| reading | owner | status |
|---|---|---|
| LP2 word sums as cleartext symbol stream | dukotah R10-L2, R37-C3 | NEGATIVE (pre-existing) |
| LP1 word/line/sentence sums as keystream | dukotah R37-C1-U2 | NEGATIVE (pre-existing) |
| separator identity/shape as message | dukotah R11-S2, R44-P3 | NEGATIVE — typography |
| **LP2 own word sums as self-key schedule** | **this campaign** | **NEGATIVE (this run)** |
| LP2 line sums as self-key | ours #8 (LS) | NEGATIVE (power 10/10) |

Families (page-local, additive, mod 29): WS1 self-word (key = own word
sum; one-rune words excluded — D ≡ 0 identically, declared in PREREG),
WS2 prev-word, WS3 word-length, WS4 running word-sum.

## Numbers

Premise kill gates PASS: 12,956 runes bit-identical to the pinned corpus
on all 55 pages; separators `-` 2,729 / `.` 173; 2,928 words (mean 4.42).

| family | obs χ² (page) | null median | null max | MC p (D) | fires? |
|---|---|---|---|---|---|
| WS1 self-word | 47.67 (p27) | 48.12 | 72.37 | 0.537 (200) | no |
| WS2 prev-word | 47.70 (p11) | 49.10 | 62.36 | 0.667 (20) | no |
| WS3 word-length | 51.63 (p22) | 46.49 | 64.98 | 0.164 (200) | no |
| WS4 running-sum | 46.94 (p8) | 46.42 | 65.97 | 0.458 (200) | no |

Null = **derive-from-shuffled** (page values permuted, keys re-derived per
draw — mandatory for self-derived keys; it correctly absorbs the pages'
marginal non-uniformity, which is why null medians ≈ 47 rather than the
iid-χ² expectation ≈ 28). Escalation fired (WS1/WS3/WS4 ≥ median) and was
honored at 200 draws; WS2 stayed at 20 (obs < median). No family within
0.1 of its null max; no crib stage reached.

## The power sentence — and why it bites harder than usual

**Power against the registered plant class is 0/10 in all four families**
(planted χ² means 29–33 vs null p95 ≈ 54–59). The negative is therefore
**weakly powered against localized structure**, and the mechanism is
structural, not a sizing accident:

> Under a **value-dependent self-derived key**, editing a window to plant
> structure *changes the keys downstream of the window*, rotating those
> decodes and washing out the page marginal the χ² measures. Planted pages
> scored **below** the null median (χ² means 29–33 vs median ≈ 47): the
> plant's 35-rune English window is diluted ~7× by the page, and its
> key-propagation side-effect actively *reduces* the marginal.

Instrument lesson (registering for future designs): with value-dependent
self-derived keys, a page-marginal statistic is structurally blind to
local plants; a re-run would need a **word-window statistic** (max χ² over
k-consecutive-word windows, matched null) — a new registration, not a
post-hoc change. Given the LOW prior (separators = typography, R11-S2 +
P3) and #8's powered line-sum negative, a powered re-run is **not
recommended** ahead of queue slot 4 (F17/F18); F1 closes at
page-marginal resolution with the blindness disclosed.

## Numbers, runtime, regeneration

- 4 families × 55 pages; nulls 3×200 + 1×20 draws; 40 plants; runtime
  **3.0 s** (PREREG estimate <60 s — held).
- Disclosed: first execution crashed at import (TRANS key error) **before
  any output**; no statistical parameter changed post-registration.

```
python3 sweeps/2026-11-wordsums/ws.py        # full pipeline, auto-escalates
```

## Not covered (as registered)

Beaufort sign; modulus 28; keys crossing page boundaries; `/`-delimited
segmentation; digitsum/prime-sum/other key transforms; separator identity
(theirs, closed); word semantics; decoded-layer boundaries; non-English
registers; window statistics (see power section); p50 (runeless).
