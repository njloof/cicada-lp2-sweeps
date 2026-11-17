# Campaign #14 PREREG — F13: token table as TARGET (blob-as-target + T2 shrunk-family re-power)

Registered 2026-11-16, BEFORE any campaign output (docs/LEDGER.md rule; CI
gate). Queue slot 6 (docs/MAP.md §G): "Campaign #14 = F13 (page→blob + T2
shrunk-family re-power); F18 overlap check first".

**F18 overlap check (slot-6 precondition, done here before registration):**
campaign #12 PB1 covered page-runes→blob SELECTION (D = B[(v+s) mod 256] mod 29,
a=1, weakly powered via the many-to-one map, instrument lesson #2). What PB1
did NOT cover: (i) blob-as-TARGET subtraction (blob as ciphertext, page as
key), (ii) affine multiplier a≠1 in the pad direction with a POWERED window
regime (T2's W=60 family max was structurally unreachable for plants). This
campaign registers exactly (i) and (ii). PB1-affine (selection with a≠1) is
**deliberately not re-registered**: it inherits lesson #2's χ² blindness
(many-to-one output map), and registering a knowingly-blind negative violates
the power-reporting rule; disclosed here and in metadata.

## 0. Dup-check (verified this session, not assumed)

| direction | status |
|---|---|
| blob→page additive/Beaufort/atbash, sign, offsets (their keytest.py) | DONE negative — **no affine multiplier** (read the pinned source: key_streams() yields base + reversed only) |
| blob→page affine a∈2..28 (our T2, orientations campaign) | DONE negative, **weakly powered** (planted ≤72-token windows vs family-median 91.6 from 1.9M windows) — re-power open |
| page-runes→blob selection (our PB1) | DONE negative, weakly powered |
| **blob-as-target: D = B − a·v (blob as ciphertext, page as key)** | **OPEN in both ledgers — R2 below** |
| **long-window affine pad regime (power fix)** | **OPEN — R1 below** |

## 1. Registered families (two verdicts, α = 0.05/2 = 0.025)

Blob B = `canon_256.bin` (sha256 3b9b07d9…4b290, 256 bytes — same pin as #12).
Pages = unsolved stream book 0–49+51–55 (L = 12,956), values 0–28.
χ²(S; n) = (29/n)·Σᵣ Cᵣ² − n throughout.

**R1 — T2 re-power (token pad → page, affine, LONG windows).**
D[i] = (v[i] − a·(B[(o+i) mod 256] mod 29)) mod 29; a ∈ 2..28 (a=1 = T1
direct bridge, done; a=0 constant, excluded); o ∈ 0..255; constant b excluded
by shift-invariance of the statistic (declared, as T2).
**Re-power vs T2:** (1) canon table ONLY (T2 scanned 3 table variants — the
superseded/e0 witnesses differ at ≤2 bytes; dropping them shrinks the family
~3× with negligible hypothesis loss, disclosed); (2) window W = 240, stride =
120 (T2 used 60/30): pages shorter than W contribute nothing (declared cost),
ladder gate G2 below; (3) plant is a LONG English window (the T2 W-lesson:
plants at n≤72 can never beat a 1.9M-window family median; English-strength
χ² scales ∝ W).
Statistic = family max window χ². Null = target-shuffle (each page's values
permuted independently; marginals preserved), D = 20, escalate to 200 iff
obs ≥ median (house pattern). Plant: 20 draws, crib from English letter
frequencies over 29 runes, v edited so D = crib on one window.

**R2 — blob-as-target (page as key INTO the token table).**
D[j] = (B[(j+o) mod 256] − a·v[j mod Lp]) mod 29, j = 0..255 (whole blob,
fixed n = 256 — no windowing); a ∈ 1..28; o ∈ 0..255; 55 pages. Sign is NOT
a separate axis: s = −1 folds into a′ = 29 − a (declared; Beaufort covered).
Statistic = max χ² over the family. Null = page-shuffle (same pattern),
D = 20, escalation as R1. Plant: 20 draws — virtual target B′ = (crib +
a·v) mod 29 for one random (page, a, o) with English crib of length 256;
family re-scored against B′ (the pinned blob is never edited).
n = 256 English plant: E[χ²] ≈ 256·(29·0.066 − 1) ≈ 219 vs expected null max
≈ 80–100 → R2 is powered by construction; the ceiling is reported anyway.

**O-enumerations (no verdicts):** E1 = argmax table for each family
(page, a, o, χ²); E2 = top-5 transliterations of R2 argmax (crib_hits only
if a family FIRES).

## 2. Verdict rule

FIRE iff p ≤ 0.025 AND plant > family p95 (else WEAKLY-POWERED negative,
mandatory power sentence). Any FIRE → crib stage + oracle registration
before interpretation.

## 3. Kill gates

- G1: blob sha256 + len 256 (as #12). Corpus L = 12,956.
- G2 (R1 ladder): W = 240 requires ≥12 pages of length ≥ W (measured 35);
  else drop ladder 240→180→120 and record the rung used.
- G3: R2 family size = 55×28×256 = 394,240 configs (exact count reported).

## 4. Seeds / runtime

Seed **20261203**; streams `default_rng([seed, crc32(tag)%100000, draw])`,
tags {"R1","R2","plant-R1","plant-R2"}. Estimated total runtime
**≤ 25 min local background** (R1 ≈ 21 s/family-run × ~41 runs dominates;
R2 ≈ 4 s/run). No studio offload unless escalation fires (then studio with
bit-identical streams per house rule).

## 5. Not covered (declared)

PB1-affine selection a≠1 (lesson #2 blindness, above); p50's 104-token
stream as a separate target (needs its own census first — canon_256 is the
canonical table used); mod-28 variants; transpositions; non-English crib
plants; multi-page key chaining (v spanning page boundaries); the e0/
superseded table variants in R1 (witness-discounted, disclosed).
