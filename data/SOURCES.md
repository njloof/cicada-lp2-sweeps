# Sources, provenance, and cross-source diff report

Fetched 2026-11-13. Build with `python3 build_corpus.py` (reproducible from `sources/`),
verify with `python3 validate.py` (all gates must pass).

## Repositories (shallow clones in `sources/`)

| repo | HEAD | role |
|---|---|---|
| Dukotah/cicada3301 | `9087dc36b5aa64c1786428e32180261ab9420c29` | canonical corpus + elimination ledger + validation rig |
| iBotPeaches/cicada_3301 | `a0a616d85717af59f8b806875b43d51e06e1e874` | published page images (unified numbering = onion7 + 17) |
| scream314/cicada3301 | `10733feb487bb8beb9966d534727ee5897aa54fc` | solved-page ciphertexts/plaintexts (LP1 + LP2 56/57) |

Key file SHA-256:
```
9b211a06…  dukotah/liber-primus/data/krisyotam_runes.txt   (canonical rune stream)
d404fb7a…  dukotah/liber-primus/dataset/liber_primus.json  (image hashes, gematria, solved refs)
cd3c6d55…  dukotah/liber-primus/SOLVED-PAGES.json          (known plaintexts)
0f7545d4…  scream314/liber_primus.md                       (transcription + solves)
```

## Numbering — RECONCILED (the handoff's assumption was wrong)

Three schemes circulate; the LP2 pages are **not** where the handoff thought:

- **Unified / 2014 release**: `00.jpg`–`74.jpg` (ibotpeaches). Pages 0–16 = **LP1**, 17–74 = LP2.
- **onion7 / LP2**: `0.jpg`–`57.jpg`. LP2 N = unified N+17.
- **"Runes" folder**: solved-page labels like `Runes - 01.jpg` — these are **LP1** pages.

Consequences:
1. "A WARNING", "WELCOME", "SOME WISDOM", "A KOAN", "CIRCUMFERENCE" are **LP1** pages
   (release files 01–16), *not* LP2 pages. The only solved LP2 pages are **56 (AN END)**
   and **57 (PARABLE)**. (Confirmed by dukotah `docs/SOLVED-PAGES-AND-INTERRUPTERS.md` and
   ibotpeaches `markdown/73.md`/`74.md`.)
2. The handoff's "pages 0–55, ≈12,956 runes" is really **LP2 0–54 = 12,956 runes** (55 pages);
   page 55 is the missing one (below).
3. Dukotah's `dataset/liber_primus.json` zips the krisyotam stream positionally to images:
   its entries 55/56 carry **AN END/PARABLE runes under image-55/56 labels** (off-by-one at
   the tail). Image hashes themselves are correct per label; we relabel to true LP2 numbers.

## Corpus

- **LP2 0–54** (unsolved targets): krisyotam `%`-segments 0–54, 12,956 runes, 55 pages.
  Each page's published image SHA-1 re-verified against `sources/ibotpeaches` bytes
  (56/56 pass, incl. page 56). Line structure preserved from the stream.
- **LP2 56 AN END** (85 runes) — solved, φ(prime) shift-down keystream; used as smoke test + pad candidate.
- **LP2 57 PARABLE** (95 runes) — solved, direct transliteration; smoke test + pad candidate.
- **LP2 55 — MISSING FROM ALL LINEAGES.** Image exists (`72.jpg`, sha1 `4f3d2d52…` published;
  4 lines ≈ 70 runes + cicada art) but krisyotam, relikd and scream314 all jump 54→56.
  Excluded from the sweep; disclosed in the report. Transcription attempt (2026-11-13,
  `p55_transcribe.py`): glyph templates built from the 55 verified pages (1,149 reconciled
  glyphs), held-out accuracy **46%** — below any usable bar. Root cause diagnosed from the
  page-0 band: the decorative font interpenetrates (X-shaped runes touch neighbours, every
  connected component is band-height) and word separators are dot-matrix ornaments, so
  component segmentation is structurally impossible. Confirms dukotah's glyph-reader
  failure (0.145) was fundamental, not effort. Page 55 remains untranscribed.
- Non-rune channel: printed digits inline on pages 10, 36, 37, 38 (`-7-`, `1-`, `2-3-4-`, `5-`)
  and markers `&` (section), `$` (page-end), `§` (EOF) — excluded from index streams, consistent
  with all community analysis.

## Cross-source diff (what "two independent transcriptions" really means)

- dukotah `analysis/transcription/TRANSCRIPTION-VERDICT.md`: **every machine-readable LP2
  transcription traces to one 2017 root (rtkd/iddqd)** — krisyotam, relikd, wiki, cadrypt,
  JBO all derive from it. Unanimity ≠ independence. We therefore treat the stream as
  single-root, image-audited, and lean on functional validation (smoke decodes) instead.
- Our own diffs:
  - krisyotam stream == dukotah dataset JSON: **identical** (asserted in builder).
  - PARABLE: dukotah == ibotpeaches (0 diffs); scream314 differs at pos 80 (ᛖ vs ᚣ).
    **Adjudicated ᚣ (Y)**: gives DIUINITY (LP's canonical V→U spelling); scream314 yields
    "DIUINITE". A live example of the transcription traps the handoff warned about.
  - scream314 unsolved-blob sections match the stream exactly except its "dump 23–26"
    section (1,021 runes), which is absent from the stream — unresolved scream314-side
    discrepancy; the stream (image-hash-anchored) wins. scream314 section labels are
    unreliable (duplicated pages, sloppy ranges) — used only for solved pages.

## Smoke-test status (validate.py)

| test | result |
|---|---|
| A WARNING (LP1) atbash → BELIEVE/FROMTHIS/TRUE | PASS |
| WELCOME (LP1) Vigenère DIVINITY, null-F search → WELCOME/PILGRIM/JOURNEY | PASS |
| AN END (LP2 56) φ(prime) shift-down, null-F search → DEEPWEB/PILGRIM/HASHESTO | PASS |
| PARABLE (LP2 57) direct transliteration → DIUINITY/EMERGE | PASS |
| total 0–54 = 12,956; doublets = 86; no prefix/substring duplicates; charset | PASS |

## Ledger cross-check (why this project is still open)

dukotah `ruled_out` includes "page-on-page key reuse / in-depth" — but ARMADA
`analysis/armada/FOLLOWUP-TESTS.md` #4 shows what was actually tested: **shared-keystream**
(`c1−c2 = p1−p2`, English-minus-English, weak IoC), **offset 0 only** ("1,485 pairs (aligned)"
= C(55,2)), and it self-labels "negative / inconclusive". Their FINAL-VERDICT #4 *recommends*
"scan all page-pair alignments and offsets" — it was never run. Our hypothesis
(pad = C_N ⇒ D = C_M − C_N = **P_M**, pure plaintext signal; all offsets; both orientations)
is strictly stronger and uncovered. Confirmed gap.
