# Red-ink census — LP2 book pages 0–57 (exploratory, descriptive)

Run 2026-11-15 by owner request. **Exploratory tabulation, not a hypothesis
test** — no PREREG (campaign discipline applies to sweep verdicts; this doc
makes claims only about what pixels are where). Script:
`scripts/audit/red_census.py` (full data + crops in gitignored
`work/red_census/`; 337 items, 11.5 s). Red rule: `R>150 ∧ R−max(G,B)>80`
(same as [STREAM_TAIL_EVIDENCE.md](STREAM_TAIL_EVIDENCE.md)); components =
8-connected BFS; bands = ink profile (gray<135, x 620–1800).

Book page N = image `N+17.jpg`. `band` = 0-based ink band (page-absolute);
on pp36–38 band = stream line + 1 (band 0 is a runeless heading band —
verified against the four margin digits below).

## The four red channels found

1. **Dot-lattice ornaments** (35 total) — red square-dot diamonds marking
   section breaks. Three size classes: **13-dot standard** (30×, ~38×84 px),
   **10-dot small** (4×: pp36, 38, 49, 56), **23-dot large** (1×: p57 band 2).
   Positions quantize to the line grid (~188 px pitch).
2. **Rubricated title bands** — giant red drop-cap (h≈500 px, x 602–880) +
   red opening/section-initial words (the `glyph` runs at band 0/section
   starts) + a lattice at the word's end. Pages: 0, 3, 6, 8, 15, 23, 27, 33,
   39, 40, 54, 56, 57. Consistent with dukotah `armada_osint/redrune/`
   rubrication verdict.
3. **Red printed digits — the selection channel (NEW, needs owner re-read).**
   The stream transcribes printed digits inline (`-7-`, `1-`, `2-3-4-`, `5-`,
   data/SOURCES.md); the census finds **five of them printed in red**:

   | digit | page | stream line | census band | x–y | colour |
   |---|---|---|---|---|---|
   | 1 | 36 | 6 | 7 | 620–644 · 1693–1783 | **RED** |
   | 2 | 37 | 1 | 2 | 606–664 · 694–787 | **RED** |
   | 3 | 37 | 5 | 6 | 607–662 · 1538–1633 | **RED** |
   | 4 | 37 | 10 | 11 | 602–669 · 2570–2663 | **RED** |
   | 5 | 38 | 4 | 5 | 603–664 · 1316–1409 | **RED** |
   | 7 | 10 | 8 (inline, between dividers ᐧ7ᐧ, ~70 % along the line) | 7 | — | **black** (`p10_line8.png`) |

   Each digit is the **only** margin digit on its line (line-initial, before
   the first rune) — not a line-number series; the other lines carry no
   digit. So red selects {1,2,3,4,5} across pp36–38 and leaves p10's `7`
   black. Pixel-confirmed crops: `work/red_census/crops/ADJ_p36_band7.png`,
   `ADJ_p37_band2.png`, `p37_margins.png`, `p38_margins.png`.
   Related: p15's four digit lines (campaign #7 family D) —
   `3258 3222 3152 3038 / 3278 3299 3298 2838 / 3288 3294 3296 2472 /
   4516 1206 708 1820` — with **`3299` in red** (line 2, group 2;
   `p15_digits_LABELLED.png`). One red group among 16.
4. **Full red rune lines — p53.** Book p53 (= stream seg 52) lines **7, 8, 9**
   (lengths 24, 22, 4) print entirely in red stylized runes (census
   components: 25/24/4 — stylized letters split), and a **red arrow ↑** sits
   at the right end of line 6 (x 1721–1767, y 1651–1763, pointing up along
   the line). These are part of dukotah's 187-red-rune set; the arrow is
   easy to miss in a runes-only pass. Crop: `p53_glyph1.png` (arrow).

## Matrix inventory (35)

| page | band | y | x | dots | class |
|---|---|---|---|---|---|
| 0 | 0 | 688–771 | 1406–1443 | 13 | std |
| 2 | 8 | 2194–2277 | 1626–1664 | 13 | std |
| 3 | 0 | 688–771 | 1560–1597 | 13 | std |
| 3 | 4 | 1630–1713 | 1356–1393 | 13 | std |
| 3 | 5 | 2116–2201 | 934–971 | 13 | std |
| 6 | 3 | 1252–1337 | 742–781 | 13 | std |
| 6 | 4 | 1740–1823 | 1332–1370 | 13 | std |
| 7 | 9 | 2473–2557 | 724–761 | 13 | std |
| 7 | 9 | 2474–2557 | 1634–1671 | 13 | std |
| 14 | 6 | 1818–1901 | 998–1035 | 13 | std |
| 15 | 0 | 688–771 | 917–955 | 13 | std |
| 15 | 0 | 688–771 | 1440–1477 | 13 | std |
| 15 | 6 | 1750–1833 | 1280–1319 | 13 | std |
| 22 | 5 | 1700–1785 | 1631–1667 | 13 | std |
| 23 | 3 | 1176–1259 | 1534–1571 | 13 | std |
| 26 | 11 | 2760–2843 | 1636–1673 | 13 | std |
| 27 | 1 | 932–1015 | 1684–1721 | 13 | std |
| 32 | 5 | 1630–1713 | 930–967 | 13 | std |
| 33 | 0 | 687–771 | 1268–1306 | 13 | std |
| 33 | 2 | 1440–1525 | 1448–1485 | 13 | std |
| 33 | 4 | 1928–2013 | 1142–1179 | 13 | std |
| 36 | 6 | 1452–1511 | 974–1011 | 10 | small |
| 38 | 11 | 2542–2599 | 602–637 | 10 | small |
| 39 | 7 | 1630–1713 | 837–875 | 13 | std |
| 39 | 8 | 1872–1957 | 944–983 | 13 | std |
| 39 | 11 | 2814–2897 | 1540–1578 | 13 | std |
| 49 | 2 | 1076–1135 | 1692–1729 | 10 | small |
| 53 | 8 | 2266–2349 | 822–861 | 13 | std |
| 54 | 0 | 932–1015 | 1194–1232 | 13 | std |
| 55 | 3 | 1252–1337 | 1034–1073 | 13 | std |
| 56 | 0 | 688–771 | 964–1002 | 13 | std |
| 56 | 1 | 1076–1135 | 1054–1091 | 10 | small |
| 56 | 8 | 2092–2175 | 1558–1595 | 13 | std |
| 57 | 0 | 932–1015 | 1140–1178 | 13 | std |
| 57 | 2 | 1740–1824 | 1644–1712 | 23 | LARGE |

**Matrices alone make 7 more pages "red pages" than the rubrication list**:
pp 2, 14, 22, 26, 32, 49, 55 carry exactly one lattice and no other red —
they were absent from dukotah's heavy-red page list (their glyph-box
threshold misses dot ornaments). Full red-page set: 0, 2, 3, 6, 7, 8, 14,
15, 22, 23, 26, 27, 32, 33, 36, 38, 39, 40, 49, 53, 54, 55, 56, 57.

## Owner double-check queue (crops in `work/red_census/crops/`)

1. The five red margin digits (`ADJ_*`, `p37_margins`, `p38_margins`) and
   p15's four digit lines (`p15_digits_LABELLED.png`) — confirm reads and
   colours; confirm p10's `7` is black.
2. p53: red arrow after line 6 (`p53_glyph1.png`) and lines 7–9 all-red
   (`p53_glyph2/20/51.png` sample the three lines).
3. Spot-check one matrix per size class (`p02_matrix1` std, `p36_matrix1`
   small, `p57_matrix2` LARGE) and the 7 matrix-only pages (2, 14, 22, 26,
   32, 49, 55).
4. Every digit-page band is cropped regardless of colour
   (`p{10,15,36,37,38}_digitband*.png`) for the digit-channel re-read.

## Caveats

- `glyph` counts on title-band pages are stylized-letter **fragments**
  (one letter can split into 2–3 components) — counts there are
  component counts, not glyph counts.
- Band↔stream-line offset varies per page (tall title bands merge lines);
  the checklist strips (`scripts/audit/make_checklist.py`) remain the
  authoritative line pairing.
- dukotah `redrune` flags glyph-box redness ≥0.3; it should agree on all
  rubrication and p53, but structurally cannot see the dot lattices or
  digit colours — the matrix inventory and red-digit selection are the
  net-new channels here (worth offering upstream on #14).
