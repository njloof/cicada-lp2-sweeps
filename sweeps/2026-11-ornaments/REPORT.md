# Campaign #13 report — F7: dot-lattices as data (language-agnostic structural tests)

Run 2026-11-16. Queue slot 5. Registration: `PREREG.md` (`db6f467`),
committed before any output. Object: the 35 red dot-lattices
(`lattices.csv`, owner-confirmed classes 13×30 / 10×4 / 23×1). Verdict:
**O1 FLAG (p = 0.00065) — structural, not linguistic; O2 NEGATIVE
(powered); O3 NEGATIVE (powered); O4 descriptive.**

## Disclosures (both mechanical, neither touches a registered statistic)

1. **O3 exact enumeration instead of MC.** The registered null set is finite
   and *smaller* than the registered stage (C(30,3) = 4,060 < D = 10,000),
   so the MC was replaced by exhaustive enumeration of the identical null —
   exact p. (Same null, same statistic; O1 was exact as registered.)
2. **O2 plant rerun.** First run scored the power plant with a construction
   bug (tie-break permutation applied to gaps but the monotone assignment
   built in permuted space → scored a random assignment, 0/20). Fixed;
   obs/null draws are seed-pinned and **bit-identical** across the rerun
   (p 0.38506, |ρ| 0.1582 unchanged); plant now 20/20 as theory requires
   (rearrangement-inequality ceiling |ρ| ≈ 0.56 > p95 0.335).

Also disclosed: PREREG §1-O4 predicted "band-0 lattice count (4)"; measured
8 (p54/p56/p57 band-0 instances sit at y = 932/688 — band numbering is
page-relative). Descriptive family, no verdict, no effect.
PREREG §2 listed the full 35-item multiset for O2; the statistic pairs each
gap with its LEFT (section-opener) lattice, so the effective multiset is
{13×30, 10×4} — the lone 23-dot lattice (p57 band2) is the last lattice in
the book and has no following gap. Null logic unchanged.

## O1 — section-head alignment: **FLAG**

22 lattice pages vs 14 pre-declared red-rune head pages (dukotah redrune
list, cited not re-derived), universe 57 pages (0–57 minus 50):

| quantity | value |
|---|---|
| observed overlap | **11** (expected under independence 5.4) |
| hypergeometric p (one-sided) | **0.00065** ≤ α = 0.0167 |
| exact power | minimum detectable overlap = 10 (so the flag is not knife-edge) |
| heads WITHOUT lattices | 8, 37, 40 |
| lattice-only pages (unsolved) | 2, 14, 22, 26, 32, 49, 55 (+36, 38 via digits) |

**What this is and is not.** It is the first quantification of the
lattice↔rubric relationship: 11 of 14 red-word section heads also carry dot
lattices; two independently-censused red features co-locate far above
chance. It is **not** a message: both features mark section openings, so
"same rubrication system" fully explains the association, and this campaign
cannot separate "co-ornaments" from "one encodes the other". Per the
registered verdict rule, the FLAG routes to the oracle **before**
interpretation: round #4 tasks S4/S5 (sheets
`docs/img/oracle/f7_S4_p{08,37,40}.png`, `f7_S5_p{02,14,22,26,32,49,55}.png`)
— do pp8/37/40 hide a missed lattice (flag weakens), and do the lattice-only
pages hide a missed red head (flag strengthens toward "complete section
marker set")?

## O2 — dot-count vs section length: NEGATIVE (powered)

34 consecutive-lattice gaps (image anchors, page·3600+y0) vs the opener's
dot count; Spearman |ρ|; null = permute the count multiset (D = 10,000,
seed 20261202).

obs |ρ| = 0.158 vs null median 0.121, p95 0.335 → **p = 0.385**.
Power: **20/20** monotone-rearrangement plants beat p95 (ceiling |ρ| ≈ 0.56,
plant p ≈ 0.0001). Verdict: section length is unrelated to dot count, and
the test could have said otherwise.

## O3 — dot-counts as position selectors: NEGATIVE (powered)

30 stream lattices (5 on solved pp56–57 excluded as registered); rune =
stream[page_start + dots − 1]; statistic = coincidence pairs Σᵣ C(nᵣ,2);
null = exhaustive over all 4,060 placements of the three 10-counts.

obs 26 vs null median 25, p95 30, max 40 → **exact p = 0.447**.
Power: the **exhaustive ceiling plant** (best possible placement of the
observed counts) reaches 40, p = 0.00049 — the multiset CAN speak, and said
nothing. Limitation disclosed: selection depends only on (page, dots), so
same-page lattices with equal counts select the same rune — 8 of the 26
observed coincidences are structurally forced (the null prices this at
≈ 0.81·8; p already reflects it). Position-aware selection (line-index
anchoring) is blocked by the band≠line trap (p27) and stays not-covered.
Selected stream (descriptive): `C EA H H H EA EA C C EA N N N Y T N I W F F
F O E U U U NG O NG D` — no crib stage fired (negative, none required).

## O4 — descriptive (no verdict)

- 35 lattices occupy only **24 distinct y-positions** (687/688, 932×3,
  1076×2, 1630×3, …) — a shared discrete vertical grid, NOT a uniform 188 px
  pitch (the earlier "~188 px pitch" note is corrected: 188 occurs once in
  the 23 consecutive differences).
- Heights separate size classes cleanly: 13-dot → 83–85 px, 10-dot → 57–59,
  23-dot → 84.
- band-0 lattices: 8; per-page counts 1–3; x-range 602–1729.

## Files / regeneration

```
python3 f7.py        # full pipeline, 0.63 s (PREREG estimate <30 s — held)
python3 sheets.py    # oracle round-#4 sheets S4/S5
```

## Not covered (as registered + measured limits)

Line-index-anchored selection (band≠line trap); the 74 ornament BANDS'
internal structure (this campaign tested the 35 LATTICES — band glyph
shapes remain dukotah's physical classification); counts as selectors with
alternative anchors (page_end, band-relative, mod line length); cross-page
ordering beyond consecutive gaps; pp8/37/40 & lattice-only-page census
completeness (oracle S4/S5 pending); any claim that the O1 flag encodes
information beyond shared section-marking function.
