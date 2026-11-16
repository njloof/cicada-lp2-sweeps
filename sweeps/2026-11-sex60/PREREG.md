# Campaign #12 / F18 — in-document OTP consumption tests — PREREG

> **SUPERSEDED-BEFORE-RUN (same day, zero output produced):** the v1 PB1
> statistic + registered null is provably degenerate — see `PREREG2.md` for
> the proof and the amended registration. §4 is replaced; §0–3 and §5–7
> (premises, kill gates, enumerations, deferrals, cost) stand unchanged.

_Dated 2026-11-16, committed BEFORE any campaign output exists (CI gate).
Queue slot 4 part 2; F17 census = `CENSUS.md` (c44081c), descriptive, no
gate._

## 0. Premise correction carried into the registration

The F18 queue line said "sexagesimal margin digits pp34–39 as VALUES". The
F17 census falsified the per-page form of that premise: the pp34–39
"cuneiform" is ONE stamp, pixel-identical ×6 (+ p33 footer) — it carries no
per-page digits. The consumables that survived the census are listed in
CENSUS.md §"What F17 hands to F18". This PREREG registers tests ONLY for
those, and defers the rest (see §6).

## 1. Hypothesis (owner's in-document-OTP thesis, restricted form)

Objects formally distinguished from the text serve as keys/selectors for
other parts. The strongest surviving instance: the pp49–51 base-60 token
table (256 bytes, `canon_256.bin`) is consumed BY the pages — the reverse
of every direction tested so far: the pages' runes act as indices/selector
stream into the table, and the selected byte stream is scored.

## 2. Dup-check (what is NOT re-run)

| reading | owner | status |
|---|---|---|
| token bytes → indices into rune corpus (idx_abs/gaps/page) | dukotah C7 `token_as_index` | NEGATIVE (English-only) |
| token bytes mod 29 as self-gematria | dukotah C7 `self_gem` | NEGATIVE |
| token table → page additive pad (canon-as-key) | dukotah C2 | CLOSED |
| token → page affine a≠1 | ours T2 | weakly powered — re-power is queue slot 6 (F13), NOT this campaign |
| **page runes → indices into token table (reverse scan)** | — | **OPEN — this campaign (PB1)** |
| red digits 1–5 as selector | ours F2/F9, queue slot 7 | enumeration only here (E1); stats there |
| stamp placement-as-key | dukotah W2-B2 not_covered ("placements enumerated but not swept") | swept trivially: placement is CONSTANT per page-set (census) → no per-page key exists; E2 enumeration |

## 3. Pinned premises + kill gates

- Blob: `sources/dukotah/liber-primus/analysis/pp49_51/canon_256.bin`
  (the SHIPPED canon; 0xc6 at idx 246 per dukotah#14 follow-up), 256 bytes,
  sha256 `3b9b07d9a26e6d55c432d94d2661fdff3c2b348daed06821f2bdb23184a4b290`,
  161 distinct values, range 0–255. **G1**: sha + length match at load.
- Corpus: unsolved stream book 0–49+51–55, L=12,956, sha256
  `9f5f14d4…483e`. **G3**: per-page bit-identical to `data/pages/` (all 55).
- **G2 (plant feasibility)**: for every offset s∈0..227 the image
  {B[(r+s) mod 256] mod 29 : r∈0..28} must have ≥12 classes (measured at
  registration: min 14, median 18, max 21 — passes; re-checked at run).
  If any offset <12 it is excluded from the family max; if <50 offsets
  survive → UNAVAILABLE-BY-PREMISE, stop.

## 4. Registered family PB1 — page→blob windowed selection

For each unsolved page p (55) and offset s (0..227):

    D_s,p[i] = B[(v_p[i] + s) mod 256] mod 29

(v = rune values 0–28; the offset slides the 29-entry window across the
table; s>28 is exactly "rune + shift into table".)

- **Statistic**: per-page 29-cell χ² = (29/n)Σh² − n (n≥50), family MAX
  over (p, s). One family → no Bonferroni needed; the null reproduces the
  same max.
- **Null**: derive-from-shuffled — each draw permutes each page's values
  (B fixed), recomputes the full 55×228 grid, takes the max. Seed 20261201;
  stream `default_rng([SEED, crc32(tag)%100000, draw])`. Stage 20;
  escalation to 200 draws on disjoint streams iff obs ≥ null median
  (honored, reported).
- **Plants (power, mandatory)**: 10/family — random (page, s*), 35-rune
  window, crib values drawn from the offset's image alphabet (G2 makes
  this always feasible), runes set so D = crib in the window; self-check
  decode==crib; power = fraction > null p95. No value-dependent key here
  (B is fixed), so the campaign-#11 structural blindness does not apply —
  but the 35/236 dilution does, and the plant measures it.
- **Verdict**: PB1 fires iff MC p ≤ 0.05. A fire proceeds to the crib gate
  (transliterate best (s,p) decode, `core.cribs.crib_hits`); ≥1 hit is
  FLAGGED-FOR-ORACLE, never certified. Mandatory power sentence in the
  REPORT whatever the verdict.

## 5. Enumerations (no verdicts — registered as such)

- **E1 red digits**: (digit, page, line) = (1,36,6),(2,37,1),(3,37,5),
  (4,37,10),(5,38,4) + p10 inline 7 black; selected-line lengths + first
  runes recorded. n=5 — no null exists; stats live in F2/F9 (slot 7).
  Value consumption is additionally gated on the owner's wedge-vs-printed
  answer (round #2 F3): if printed, the values are not LP2 data.
- **E2 stamp placement**: bracket {33…39}, header×6 + footer×1, constant —
  recorded; placement-as-key is vacuous for constant placement.

## 6. Deferred (new registrations, not post-hoc amendments)

Stamp glyph values as pad/selector — pending oracle round #3 (S1/S2);
red-digit-as-value consumption — pending owner F3; blob→page affine
re-power — slot 6 (F13); transpositions, mod-28, Beaufort sign on PB1,
non-English registers, p50 internals.

## 7. Cost

Vectorized (per draw: one 55×228 einsum of 29×29 selection matrices);
20 stage + 200 escalated draws + 10 plants ≈ well under 60 s single box.
Runtime estimate at launch: **<60 s**; will be reported measured.
