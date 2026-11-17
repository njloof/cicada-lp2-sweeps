# Campaign #16 PREREG — black 4-dot diamonds ↔ krisyotam `.` separators

Registered 2026-11-17, BEFORE any campaign output (CI gate). MAP slot 6b.
The owner's completed full 58-page annotation pass (docs/ORACLE_PAGES.md @
c52bf40, sha256 c66edb29e9a2b3a4…) replaced krisyotam characters with
`◆N` marks at owner-adjudicated positions: ~128 `◆4`, 22 `◆13(*/black)`,
3 `◆10*`, 2 `◆3` (line-wrapped ◆4, owner assumption), 1 `◆23`. This
upgrades the pre-campaign exploration (173 `.` vs 156 clusters, 17 pages
exact) from detector inference to ground truth: the ordinal pixel test is
SUPERSEDED by direct transcription-level correspondence.

## 0. Objects

- **Baseline**: krisyotam verbatim, `BOOK` map (scripts/audit/
  insert_transcriptions.py), 57 blocks; `.` total 173 (156 on unsolved
  pages).
- **Owner truth**: numbered lines inside each `**Ciphertext**` fenced
  block of ORACLE_PAGES.md @ c52bf40. Extraction = per-line character
  diff vs baseline line (same page, same line number); owner `◆N(\*)?`
  runs recorded with the baseline character they replace (or "insertion"
  if none).
- **Detector**: sweeps/2026-11-ornaments/fourdots.csv (169 clusters,
  51 pages; run-CC detector, owner-validated ±1 line).

## 1. Registered tests (deterministic structural campaign — no MC nulls,
no p-values; verdicts are rates against pre-registered thresholds.
Precedent: #13 O4 descriptive. Any inferential claim about cipher
CONTENT is out of scope and declared below.)

**T1 — substitution target census (the core hypothesis).**
H: the black 4-dot diamond is the RENDERED `.` sentence separator.
Every `◆4` extraction is classified by replaced char ∈ {`.`, `-`, other,
insertion}. VERDICT: CONFIRMED iff ≥95 % of ◆4 replace `.`; REFUTED iff
<80 %; otherwise MIXED → full enumeration, no verdict. Exceptions
enumerated exhaustively (page, line, position, replaced char).

**T2 — large-lattice ↔ `&`/`$`/`§` mapping.**
For each ◆13/◆10/◆23 mark: is its line ADJACENT (within 1 line) to a
standalone `&`/`$`/`§` baseline segment? Report the 3×3 table
(◆size × ornament) both directions. H: ◆23↔§ (1/1); ◆13 at section ends
(adjacent to `&` or `$`); ◆10 likewise. No threshold — the table IS the
answer to the walkthrough header question (which size is which symbol);
interpretation deferred to owner.

**T3 — detector validation.**
Per unsolved page: owner ◆4 count vs fourdots.csv cluster count. Report
exact-match count, Spearman ρ (descriptive, n≈51), and the full
disagreement list — this enumerates detector v2's required fixes
(known misses p3/15/33/20/23 expected to reappear as owner>detector).

**T4 — residual-dot structure (descriptive).**
`.` NOT replaced by ◆4 remain (expected ≈45 unsolved-page). Report:
per-page residual counts; share of ◆4 vs residual `.` at line-final
position (last `.` on its line before `/`); share adjacent to a red
(`*`) word. No verdict — this feeds the 6c crib design (owner:
punctuation + short words = plaintext constraints).

## 2. Kill gates

- G1: krisyotam parses to 57 `%`-blocks; BOOK map covers 0–57.
- G2: ORACLE_PAGES.md parses ≥55 numbered-line blocks; every ◆-bearing
  line number exists in baseline (extraction sanity; owner did NOT
  renumber — line counts per page must equal baseline segment counts,
  checked per page, violations listed).
- G3: corpus L = 12,956 (core.validate).
- G4: for the 7 LATTICE_ONLY pages (2,14,22,26,32,49,55) baseline
  segment counts include &/$ lines (guards the renumbering regression).

## 3. Runtime

Pure text parsing + small CSV joins; estimated **< 10 s**, local (no
studio offload). Deterministic — no RNG, no seed.

## 4. Not covered (declared)

Any claim that ◆4/'.' encode cipher-content distinctions (this campaign
only tests TRANSCRIPTION↔IMAGE correspondence); pixel re-detection
(detector v2 is follow-up work fed by T3); `◆3` wrap semantics beyond
owner's stated assumption; quote/apostrophe census (6c, next); word-sum
crib design (F1 successor); margin 3L/5R decoration (S8c closed).
