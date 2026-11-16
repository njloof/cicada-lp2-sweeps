# Campaign #12 / F17 — the pp34–39 "sexagesimal" census (descriptive, no gate)

Run 2026-11-16. Queue slot 4, part 1 (census first, no gate; F18 consumption
tests get their own PREREG). Book-page labels; page N = image `N+17.jpg`.

## Premise correction (the important one)

Both ledgers speak of "Babylonian sexagesimal margin **digits** pp34–39".
The census finds **two distinct objects** that have been conflated under
that name — and they have opposite statuses:

| object | ink | where | values |
|---|---|---|---|
| **A. the cuneiform-like STAMP** | black | p33 bottom + **tops** of pp34–39 | UNKNOWN — oracle round #3 |
| **B. the margin digits 1–5** | red | pp36–38, line-initial | KNOWN (1,2,3,4,5) — style question open |

## A. The stamp — one repeated device, not per-page digits

dukotah R44-W2-B2 corrected the blind-agent inventory: the device occurs on
**seven** pages (p33 bottom + tops of pp34–39, bracketing exactly the
pp33–39 section) and the pp34–39 instances are **bitwise identical**
(their IoU 1.0; p33 same device at IoU 0.853, resampled at a different y).

**Independently re-verified here** (`census_sex60.py`): the 365×390 px stamp
region is **pixel-identical (maxdiff 0)** on all six images 51–56.jpg.
Faint-ink check: threshold 128→200 adds only anti-aliasing halo (29.4k →
32.6k px), no hidden marks.

Consequence: the stamp carries **no per-page information**. Its degrees of
freedom are exactly (i) the values of its glyphs — a constant tuple — and
(ii) its placement: a 7-page bracket pp33–39, header on 34–39, footer on 33.

Component geometry (reading order, image 51.jpg; dukotah census, boxes
re-anchored):

| glyph | x0 | y0 | w | h | area px |
|---|---|---|---|---|---|
| G1 | 1029 | 216 | 72 | 96 | 2,528 |
| G2 | 1101 | 179 | 144 | 178 | 8,756 |
| G3 | 1261 | 195 | 59 | 106 | 1,726 |
| G4 | 1304 | 157 | 87 | 99 | 3,070 |
| G5 | 1029 | 371 | 131 | 175 | 6,228 |
| G6 | 1176 | 381 | 130 | 125 | 5,548 |
| G7 | 1336 | 376 | 54 | 93 | 1,538 |

(7 components; "6-glyph" in dukotah's prose counts one pair as a single
sign — the split is a segmentation convention, the crops are the record.)

**Machine wedge-counting FAILED and is disclosed as failed.** Two methods:
(1) tail-erosion + component heads — wedges touch and merge (single cores
up to 2,630 px); (2) inscribed-radius (chamfer DT) peak detection — the
strokes are too thick and fused (inscribed radius 8–16 px vs the ~4 px
separation assumed) and it over-segments (7–41 "heads" per glyph, unstable
to the threshold). This device is a stylized, stroke-fused "woven" design,
not clean monumental cuneiform — automated wedge segmentation is not
credible at this resolution. Sign/digit identification is therefore an
**oracle task** (round #3, sheets in `docs/img/oracle/sex60_*.png`), and it
is exactly the item dukotah left open ("identification against real
cuneiform sign lists" — their not_covered).

## B. The red digits — values known, style question open

From `docs/RED_CENSUS.md` (2292dcd), owner round-1 confirmed reads:

| digit | page | stream line | colour |
|---|---|---|---|
| 1 | 36 | 6 | RED |
| 2 | 37 | 1 | RED |
| 3 | 37 | 5 | RED |
| 4 | 37 | 10 | RED |
| 5 | 38 | 4 | RED |
| 7 | 10 | 8 (inline) | black |

Each is the only margin digit on its line (line-initial). As base-60 these
are five single digits < 10 — no positional grouping exists. **Gate for
F18:** whether these are LP2-native (wedge) or modern scanner annotations
(printed) is the owner's open round-#2 F3 question; if printed, they are
not consumable data and F18 tests them only as placement.

## What F17 hands to F18 (consumable inventory)

1. **Red digit values {1,2,3,4,5} + line positions** (gated on the
   wedge-vs-printed answer) — selector candidates.
2. **Stamp placement**: the 7-page bracket {33…39} + header/footer
   orientation — a range selector; *placement-as-key is dukotah
   not_covered* ("the stamp's 7 placements … enumerated but not swept as
   keys").
3. **Stamp glyph values** — pending oracle round #3; if they read as
   numbers, a constant base-60 tuple; if as signs, a transliteration.
4. The pp49–51 base-60 token table (256 tokens) remains the natural
   consumption target (same base; dukotah tested only count-vs-dimension
   and first-digit indexing, never value consumption).

## Files / regeneration

- `census_sex60.py` — re-verifies identity, prints the table, rebuilds all
  three sheets (`python3 census_sex60.py`).
- Sheets: `docs/img/oracle/sex60_stamp_p34.png` (G-labeled stamp),
  `sex60_glyphs_p34.png` (tiles; boxes interlock — read on the full stamp),
  `sex60_wedge_ref.png` (synthetic schematic, not a scan).
- Cited, not recounted: dukotah R44-W2-B2 (black census, IoU, catalog);
  dukotah R44-P1 (red census); our `docs/RED_CENSUS.md` (red digits).
