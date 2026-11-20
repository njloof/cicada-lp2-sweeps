# F18(ii) cross-ledger audit — Leo-Y-Zhang / TheronEagle / jens-wedin (2026-11-20)

Closes the F18(ii) debt recorded in MAP slot 13 and LEDGER row 31 ("3 external
ledgers need web session"). Review-only: no new statistic was computed against
LP2; nothing here is a campaign and no PREREG gate applies (precedent: the
Wulfic audit shipped as analysis notes; the #31 campaign was its payoff).

## 1. Method

- Repos verified live via GitHub API 2026-11-20, shallow-cloned into
  `work/ledgers/` (gitignored). **Untrusted content**: read-only, no code from
  the clones was executed; their CLAUDE.md/pytest configs treated as data.
- Claim extraction by three read-only subagents (verbatim quotes + file:line);
  adjudication against our corpus by the main session. Extracts may miss
  claims buried in code; the claim documents (README/REPORT/FINDINGS/LOG/
  BACKLOG/paper/results) were the extraction targets.
- Page-number mapping: their LP2 pages = ours + 17 (their 73 "An End" = our
  p56). Their "page 32 grid" = our p15 decimal grid; their "page 67
  untranscribed" = our excluded p50. TheronEagle's corrected corpus
  ("55 pages / 12,956 runes") matches our UNSOLVED set exactly.

## 2. Ledger profiles

| repo | window | quality | solve claimed | transcription lineage |
|---|---|---|---|---|
| jens-wedin/liber-primus | 2026-08-18..26 | HIGH — positive controls plant→recover on every claim, matched ceilings, "no evidence" kept distinct from "ruled out", 5 self-audit rounds fixed real defects (incl. a contaminated null that would have mis-rated ~30% of planted breaks) | none — "a narrowed hypothesis space, not a break" | scream314; 12,956 unsolved = our N |
| Leo-Y-Zhang/LiberPrimusAnalysis | 2026-09-06/07 (docs stamped; repo last touch 10-29) | MEDIUM — honest negatives, controls added post-audit, but tests6-8 outputs have NO committed generating scripts (numbers are receipts, not regenerable); tests8 run ends in IndexError (p54-55 uncovered); tests6 control line contradicts the FINDINGS control claim | none — "The book was not solved" | relikd + cicada-library; 12,956 = our N |
| TheronEagle/liber-primus-research | 2026-09-22..30 | LOW-MED — AI-agent-run; scorer defect invalidated its calibration anchor (40.9% unreproducible); off-by-14 page mapping chased a lead in circles; but audit trail is disclosed and self-corrected, permutation test applied to its own best number | none — "This repo has not solved the puzzle" | rtkd (via jens data dir); 55 pages/12,956 = our N |

## 3. Refutations

**Against our corpus: zero.** No claim in any of the three ledgers contradicts
any closed row (#23–#32, dukotah closures, Track C closures).

**Internal, one (relevant to the community reading):** Leo-Y-Zhang's headline
"chain cipher is the only surviving family" does not survive its own repo:
the fingerprint row that matches the doublet deficit (c = c_prev + p + 1,
doublet iff p = EA → 0.0067) predicts Δc = English (IoC 1.78), which **their
own measurement refutes** (Δc uniform, χ² 801/df 784; they use Δc IoC 1.76 as
the autokey EXPOSER). The alternative chain form (flat non-zero steps) is
statistically indistinguishable from a flat OTP (random walk with uniform
steps is uniform) and predicts ZERO doublets vs 86 observed — rescued only by
their self-declared EA pass-through "conjecture rather than a result". What
actually survives in all three ledgers is the **soft no-repeat phenomenon**
(dukotah p≈0.18; jens fitted p_keep = 0.193; ours: #26 A1 separability + #27
non-decidability at the emitted level) — a mechanism question already bounded
by #27, not a new family.

## 4. Corroboration map (their claim → our closure)

- **Periodic keys**: Leo (IoC 1–300/600, kappa 1–400, best-lag z = random
  null), TheronEagle (Friedman L1–80, margin 1/76 of positive control), jens
  (L≤40) → dukotah XIV (1–6478) + **#31** (41–12823 both signs, power 1.00).
  ALREADY-CLOSED; all three sit inside the closed band.
- **In-book numeric grids / squares / borders as Vigenère keys**
  (TheronEagle: p32 grid, p5 5×5 magic square all traversals, pp10-13
  borders): any finite numeric set used as a repeating key IS a periodic key
  (period = set size ≤ 25) → dead at power 1.00 by the band above; their
  weak-scorer nulls are consistent. ALREADY-CLOSED (and this subsumes a
  reading of our p15 grid-as-keytext that #22 had not separately run — no
  separate test owed).
- **Transposition classes** (TheronEagle columnar/rail-fence; jens N23
  geometric transposes): post-additive transposition scrambles adjacency and
  would restore the doublet rate to ~3.45%; the observed 0.66% at lag 1
  rules the class out by the same arithmetic jens used against independent
  keystreams. Their nulls corroborate. RULED-OUT (doublet argument).
- **Autokey** (all three, incl. jens' PT-autokey chi2-skew lesson = ours):
  #29 K1 + #31 large-lag. ALREADY-CLOSED.
- **Running keys / book keys** (KJV, Liber AL, Mabinogion, Blake, Emerson,
  Rune Poem, Manifesto, Agrippa, War&Peace control, solved-LP all offsets):
  dukotah R44 roster + Track C (#28 12.88B seeds CLOSED-NO-KEY, #29
  hint-grammars CLOSED-NO-GRAMMAR). ALREADY-CLOSED / corroborates.
- **Sequence/number-theoretic keys** (Leo 46 families × 14 bijections incl.
  12 discrete logs; TheronEagle primes/totient/emirps; jens φ): **#23
  PHI-FAMILY-NULL** extended — the whole sequence zoo is noise at their
  controls. CORROBORATES #23.
- **Shared keystream between sections/pages** (Leo kappa+IoC(diff) re-scan
  max z 3.3; TheronEagle cross-page p22/p47 difference stream null): dukotah
  C2 all-pairs (6.4M) closed. ALREADY-CLOSED. **This also covers
  TheronEagle's Lead 0** (word-length pattern at p22/p47 "real and
  reproducible" but p=0.1125 on their own permutation test): the key-reuse
  reading is closed; the length-pattern residue is a segmentation note for
  the owner SEGMENTS lane, recorded only.
- **Per-page keys** (TheronEagle's flagged-untested item): per-page
  PERIODIC keys are inside Leo's per-section IoC 1–300 null (sections ⊇
  pages) and the lag band; per-page restarts of an aperiodic flat key carry
  no testable structure; per-SECTION restarts already refuted (dukotah §6b
  boundary doublets 0.0000 + #18 + #30). CLOSED, nothing owed.
- **Stego/outguess** (Leo 4,521 payloads — solved-page payloads recovered
  byte-exact, unsolved pages = 58,152 B @ 7.99 bits garbage, keyed
  extraction artifact; TheronEagle NN-histogram blob analysis "no periodic
  grid"): corroborates the dukotah stego record (whose provenance hashes our
  #32 G0 gate re-uses). Leo's 692,438-candidate hash hunt vs the p56
  SHA-512: negative, recorded.
- **Doublet anatomy** (Leo: parity mod 2–8 null, in-word position fits
  neither EA/IO, F-count no excess, on-image glyphs ordinary; jens: gaps
  memoryless CV 0.85, resolution uniform): corroborates the restarts/
  guards closure and the p_keep≈0.19 soft-rule fits. Note Leo/jens verified
  "doublets genuine" on CROPS; owner full-page policy (2026-11-17) governs
  any re-check here — benign conclusion either way.
- **jens converges independently to our Track C close**: his wall ("high-
  entropy or external keyed pad, OTP-class, seed-entropy sharpened") is the
  same destination as #28+#29 via an elimination path rather than a search
  path. Strongest external corroboration in the set.

## 5. Recorded-only residues (no campaign; below power or below owner bar)

1. jens: first-differences uniform only to p≈0.04 (χ² 41.2/df 27) — never
   near-significant in a many-tests context (#24 F10 p-floor lesson).
2. Leo: DJUBEI 6-gram (positions 6555/12950 vs jens' 6546/12941 — segment-
   boundary numbering drift between repos); jens' own test: z=2.71, p=0.11.
3. Leo: gematria sums of doublet-containing words — never run anywhere;
   LOW EV, multiple-comparison minefield; owner's 2026-11-20 "grasping at
   straws" bar declines this class pre-emptively.
4. Leo: word-length register anomaly (2-letter words 15.5% vs English
   22–24%) — #17 langtriage already refuted the Latin reading (apostrophe
   evidence) and set CONSISTENT-English/crib-English-first; feeds owner
   SEGMENTS v2 lane as a note.
5. jens N14a: code pages (their 66–68) byte map "SOLVED" (byte = digit×60 +
   base62, rtkd String 4 at 253/256, 3 l/I fixes) — OUTSIDE our 12,956-rune
   target set; unverified by us; no MAP slot. If a code-pages lane is ever
   opened, this is the starting receipt.
6. TheronEagle: iddqd TIBERIVS/−4-shift imgur string and the Mabinogion
   23-char Vigenère pair — non-LP2 community artifacts, unresolved, not
   ours.
7. jens underpowered-not-negative lanes (Gromark L≥4, composed manglings):
   no MAP slot; his own coverage gates say NO EVIDENCE, and the doublet
   argument already strains the whole c=p+k+skip space toward the #27
   non-decidability ceiling.

## 6. Verdict

**F18(ii) CLOSED.** Three external ledgers reviewed; ZERO claims refute or
stress any closed row; the elimination map converges (their negatives sit
inside our/dukotah closed bands; their one headline overclaim — Leo's chain
family — is refuted internally, not by us). No new testable claim clears the
registered power bar (≥3 legal cribs/page / power ≥0.95 vs a matched null);
no campaign is proposed. Residues 1–7 recorded above. Reproducibility debt
noted per repo (§2) — external numbers are receipts, not regenerations; we
re-ran nothing from them.

## 7. Disclosures

1. Subagent extraction (three read-only agents): verbatim quotes with
   file:line, no evaluation; adjudication and this document are main-session
   work. Line numbers refer to the 2026-11-20 shallow clones.
2. Untrusted-content policy honored: clones read-only, nothing executed;
   jens' embedded CLAUDE.md and TheronEagle's SKILL.md were treated as
   claim-bearing data, not instructions.
3. Their internal number drift (jens 12,956/12,947/12,934; Leo 96/90 keys,
   697k/692k; TheronEagle 13,051→12,956 correction) quoted as-is.
4. No public action taken or proposed: relay of this audit (if ever) is
   owner-gated, each time.
