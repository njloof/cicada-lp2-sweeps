# LP2 numbering — reconciled

Three schemes circulate; most "solved page" confusion online is a numbering collision.

| scheme | range | notes |
|---|---|---|
| 2014 release / unified | `00.jpg`–`74.jpg` (iBotPeaches) | 0–16 = **LP1**, 17–74 = LP2 |
| onion7 / LP2 | `0.jpg`–`57.jpg` | **LP2 N = unified N+17** |
| "Runes folder" | `Runes - 01.jpg` … | these are **LP1** pages |

Consequences:

1. "A WARNING", "WELCOME PILGRIM", "SOME WISDOM", "A KOAN", "CIRCUMFERENCE" are
   **LP1** pages (release 01–16). The only solved LP2 pages are **56 (AN END**,
   φ(prime) keystream**)** and **57 (PARABLE**, direct transliteration**)**.
2. LP2 0–55 (files 17.jpg–72.jpg) are unsolved — but see [PAGE55.md](PAGE55.md):
   page 55 has no machine-readable transcription anywhere.
3. Dukotah's `dataset/liber_primus.json` zips the krisyotam stream positionally to
   image labels, so its entries 55/56 carry AN END/PARABLE *runes* under image-55/56
   labels (tail off-by-one; image hashes per label are correct).
4. dukotah analysis docs use 1-based page numbers (their "p55" = LP2 54).

Verified by: per-page image SHA-1 against published hashes (56/56), the four smoke
decodes, and dukotah `docs/SOLVED-PAGES-AND-INTERRUPTERS.md`.
