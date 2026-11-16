# LP2 knowledge & frontier map (living document)

Started 2026-11-16, after campaign #9. Purpose: keep the research
**methodical** — a single place that says what we know, what we've closed,
what's genuinely open, and how a new idea earns a campaign slot. This doc
does not replace the citable units ([LEDGER.md](LEDGER.md) rows, per-campaign
REPORTs); it organizes them. Update it whenever a campaign closes, an owner
check lands, or an idea is added/demoted — same commit discipline as anything
else tracked.

> **Idea lifecycle:** queue entry (§D) → design note (like
> `CAMPAIGN9_MIRROR_DESIGN.md`) → PREREG committed before any output (CI gate)
> → campaign → LEDGER row → map update. New ideas enter the **queue**, never
> the current sprint. One campaign at a time; the owner picks from the ranked
> queue.

---

## A. KNOWN — high-confidence facts (with anchors)

### A1. Corpus & provenance
- LP2 = book pages 0–57 (`data/pages/lp2_00..57.txt`), hash-anchored per-page
  to published images (56/56 SHA-1). Corpus sha256 `9f5f14d4…483e`.
- **Solved:** p56 AN END (φ/prime-shift keystream), p57 PARABLE (direct
  transliteration). **Runeless:** p50 (13×8 base-60 token table only).
  **Unsolved:** 55 rune pages = book 0–49 + 51–55 (12,956 runes).
- Numbering traps resolved: [NUMBERING.md](NUMBERING.md) (three circulating
  schemes; most "solved page" confusion is a label collision); tail +1 shift
  proven and relabel applied (`2089fc2`,
  [STREAM_TAIL_EVIDENCE.md](STREAM_TAIL_EVIDENCE.md), upstream #14).
- Single-transcription-lineage risk is mitigated, not eliminated: owner's
  from-scratch p51 read matched the lineage at 92/92 runes incl. dividers —
  first independent divider-fidelity corroboration; other pages remain
  single-root for divider/dot fidelity.

### A2. Design vocabulary (from solved material — our idea generator)
Every mechanism the designers demonstrably used, i.e. templates worth
re-using as hypothesis sources:
- **Keystream pads:** φ(prime) shift sequence (p56); atbash; keyed Vigenère
  (DIVINITY, LP1).
- **Line-sum gematria:** SOME WISDOM 4/5 prime line-sums; A WARNING 9/9
  prime plaintext line-sums (verified, P≈1e-8) — sums of *plaintext* lines,
  prime-checked. [PLAINTEXT_PALINDROMES.md](PLAINTEXT_PALINDROMES.md)
- **180° rotational symmetry:** SOME WISDOM mirror line-sums are exact
  palindromes (341,1015,562,1015,341); magic square constant 1033 (emirp of
  3301). Page-level and matrix-level symmetry is a house style.
- **Letter play:** W-drops, K→C, V→U (A WARNING) — deliberate noise rules
  exist. DIUINITY spelling is canonical.
- **Interrupters / null-F:** LP1 filler ᚠ runs; 29-symbol alphabet with no
  V/K/Q/Z.
- **Word dividers, sentence dots, line marks** exist in the stream encoding
  (krisyotam `-`/`.`/`/`) — word boundaries ARE observable at stream level
  (footnote #8).

### A3. Non-rune channels present in the unsolved pages (enumerated)
From [RED_CENSUS.md](RED_CENSUS.md) + campaign #7 (owner double-check queue
= RED_CENSUS last section; items marked ⚿ are awaiting it):
- **Printed digits:** p10 inline `7` (black); pp36–38 margin digits 1–5,
  **all red** ⚿; p15 four 4-digit groups, one red (`3299`) ⚿.
- **Red ink:** title-band rubrication (drop-cap + opening word); 35
  dot-lattice section ornaments (13-dot ×30, 10-dot ×4, 23-dot ×1 p57);
  7 pages red ONLY via matrix (2,14,22,26,32,49,55); **p53 stream lines 7–9
  all-red + red arrow after line 6** ⚿.
- **Token tables pp49–51:** 256 base-60 tokens (1 byte each, 8/row);
  canonical `canon_256.bin`; split cells adjudicated by pixels
  (165=0I, 172=2S, 246=3I — dukotah's shipped bin agrees; doc/bin drift
  theirs, disclosed upstream). **Semantics unknown.**
- **Doublets:** 86 across unsolved LP2 (count reproduced exactly; dukotah
  independently: 86 residual sites, and their T7 non-stationarity claim says
  the *spacing* is non-uniform — F5).
- **More channels from dukotah's enumeration** (their census, adopted):
  base-60 sexagesimal margin digits pp34–39 (never tested — F17); mayflies
  pp24–26/57/14; dendrites pp8–14/32/55; 14 red section-head pages
  (0,3,6,7,8,15,23,27,33,37,39,40,53,54); drop caps on 15/58 pages
  (`SLXHXFUMDSFAINGP`); 74 ornament bands; 458 ᚠ interrupters; figural
  motifs (crosses/trees/shrouded corpse). Their red-ink census: 213 runes +
  30-bit dot stream (consistent with our RED_CENSUS inventory).
- **Structural:** per-page line lengths/divider positions; p57 = 95 runes,
  p56 = 85 runes.

### A4. Statistical facts about the raw streams
- Under our instrument (χ² of 29-symbol non-uniformity, language-agnostic,
  mask="tgt", MIN_LEN=50), **no unsolved-page stream, and no result of any
  tested pairwise transform, shows designed non-uniformity at a rate beyond
  multiple-testing noise** (campaigns #1–#9; ~370M windows total).
- p12 shows mild real structure (own-page χ² p=0.003 uncorrected; ±1
  shifted-mirror excess survives 10% corruption) but is **not an outlier**
  against matched nulls (p=0.099 at 1000 draws) — real-but-not-special.

---

## B. ELIMINATED — hypothesis families and test strength

Strength classes: **E** = exhaustive over a declared space w/ matched
MC-of-max null; **P** = priced/partial (some region excluded); **W** = weak
power (short windows / criterion unreachable) → *re-openable with a better
statistic*.

### B1. Ours (LEDGER #1–#9, all E unless noted)
| closed family | what exactly died | strength | re-open? |
|---|---|---|---|
| cross-page additive pads (diff/sum, all offsets, both orders, straddling) | any uniform running pad between any two pages, fwd/rev | E, 3.8M+7.5M win | no |
| pad transforms: k·C_N, atbash (collapse), stride/decimation pads **all phases**, cyclic wrap (provably complete alignment) | index-consumption axis incl. phase gaps dukotah left open | E, ~350M win | mid-range cyclic steps priced out → F10 |
| pairwise products & composites (stride×scale×mirror junctions) | all pairwise multiplicative composites, effective g∈2..5 | E, 161M win | triple products → F12 |
| self-derived keys (line-sums, φ/digitsum lags, cumulative feedback) | segment-internal value keys; VT o=0 max proven algebraic artifact | E, derive-from-shuffled null | word-sum variant → F1 |
| number channels as **additive keys** (LP1 line sums, DIVINITY, 1033/3301 digits, ramps, printed digits) | value-sequences used as running pads | E (D family W: 6 digit glyphs corpus-wide) | digits as **selectors** → F9 |
| reading orientations × mirror pairs (8 classes, proven collapse, control bit-exact vs #1/#2) | every global page orientation (id/rl/rg/r180 both sides) × mirror pairing | E, O1 10/10 powered, p=0.055@200 = persistent-nothing | no |
| token-table bridges (T1 orientations, T2 affine a·T) | token streams as pads onto pages, affine-scaled | T1 E-ish (8/10); **T2 W** (planted n≤72 can't beat family median) | T2 strong-signal regime → F13 |
| p12 mirror "flag" | dissolved at 1000 draws | E | no |
| (instrument truths, not hypotheses: mask tests RAW values; self-pair scans need pad-side nulls; ≤20-draw flags are provisional; English-only adjudication forbidden) | | | |

### B2. Community — dukotah ledger (digested 2026-11-16 from their
Round-44 state: `ELIMINATION-LEDGER.md` 1,323 lines + `LEDGER.json` 348 rows;
paths below relative to `sources/dukotah/liber-primus/`)
| closed family (theirs) | strength / caveat |
|---|---|
| ~200 thematic/literary **keytexts** (incl. Welsh Mabinogion, Cicada PGP prose), all offsets/signs/atbash, skip-tolerant re-run; positive controls recover the true key | E; residual: pages 20/22/25/27/29 sign +1 truncated; 10/33 R42-C1 texts corrupt (404) |
| **Autokey** (PT&CT, 4 variants) — *mechanism-level refutation*: difference-diagonal flat (cv 0.061) where autokey demands lumpy; k-history + cumulative-gematria feedback null | E+, strongest class of negative (refuted, not merely failed) |
| periodic Vigenère L1–40, Hill 2×2 exhaustive (682,080) + 3×3, fractionation/bifid, homophonic, transposition-only, block/Lehmer, multiplicative gematria (no closed group), alphabet-ORDER relabel (29! hill-climb = noise), un-rewrite (116 orderings) | E/mostly mechanistic; IoC·N=1.000 + doublet deficit jointly unmatchable by any of these |
| book ciphers (KJV/Mabinogion/Milton/Welsh, 912 decodes), Latin/Greek/OE/Hebrew/Norse registers, word-length skeleton (224 texts, 22.6M words) | E-ish; register panel is English-centric (their own caveat L7-A) |
| number-theoretic keystreams (primes, φ ladder, Fibonacci, prime gaps, digit planes, totient escalation; 7 lenses) + plaintext-blind pad-restoration oracle (1,800 configs — every generator RAISES doublet rate) | E, control-validated |
| seeded PRNGs: 2.52×10⁹ unix-epoch seeds ×10 gens; KDF 692k; PHP mt_rand / bash $RANDOM **full orbits** / Perl / TeX / glibc / .NET / ISAAC / BBS / LFSR / Geffe; Py2.7-MT exhaustive 2³² under `pair` (crossers oracle-adjudicated noise) | E-with-tails: Py2.7-MT `exact` relation PARKED 44.14%; PHP/Perl/TeX/glibc tails, Marsaglia CDROM 679/756 units, bash 5.1 PIE orbit unswept; /dev/urandom untouchable by construction |
| seedless public pads (Bitcoin 0–303,726, NIST Beacon, random.org, RAND digits, Cicada's own bytes; ~14.5×10⁹ offsets) | E; Marsaglia CDROM partial |
| onion-2 growing-string timing channel (112/255 intervals, 1.9M cells) | E |
| hint lenses (koan-as-ops 185, solved-plaintext acrostics 3,508 selection fns, turtle renders, drop-cap catalog, printed-line acrostic, WordNet "meaning=road") | E, control-validated |
| **image channels**: file stego (OutGuess from source + controls, LSB/DCT/EXIF/trailer), glyph micro-geometry, font-variant selection, sub-pixel/kerning, chroma bitstream, onion-image dictionary stego (24,078 extractions), p15 4×4 grid, hash-stride parse | E at 8–19 bar-units (R44); figural motifs documented, NOT coded (oracle queue) |
| **token tables pp49–51 as data**: not prime/RSA, not runic key (337,944 cfgs), not text, no container magic, no 32B hash preimage, no repeating XOR, no QR, no external-key ciphertext (AES/RC4/ChaCha/XOR + 1,752 HMAC vs p56 hash), not a section index, **canon-as-key over all pages (6.4M decodes)** | E; verdict "behaves as OTP-class blob." **Our T2 affine bridge is inside their canon-as-key space only if a=1 was included — verify; affine a≠1 may be their gap** |
| transcription integrity | VERIFIED (not eliminated): 3–4 witness lineages char-identical, classifier 99.2%, T1 450/450 |
| non-cipher framings: LP2-as-image/DSP (whiter than noise), MDL (exactly incompressible), bioinformatics | E; message-vs-filler **UNDECIDABLE** (10-stat band overlap) |

Their **established** items we adopt: interrupter convention (only ᚠ null,
does not advance keystream); separators `/.-` = typography (their R11-S2 —
relevant to our F1 divider fidelity: dividers are *typographic*, weakening
word-sum as a designed channel — check before #10); soft **anti-repeat
filter** machine-generated over a memoryless base (p_keep≈0.18, ~83% lag-1
suppression; doublet deficit 0.66% vs 3.45%; IoC·N=1.000); AN-END hash
preimage unreachable by construction; 2014 master = Ghostscript 9.05–9.14
400-DPI render.

Their **only live anomaly — T7** (verified firsthand against
`analysis/round44/SYNTHESIS.md` §2): anti-repeat slip rate is NON-STATIONARY
across the book — per-1k doublet blocks [8,3,7,2,6,9,10,8,11,2,9,6,5],
**lag-1 gap autocorrelation +0.380**, battery p=0.0010, and their X1
red-team's independent 20,000-draw gap-permutation null p=0.00025. Filed
`measured`, never certified (row `R44-W2B3-D01-FALSIFIER`); their C5 cell
showed the per-PAGE doublet test is structurally blind to this block-scale
pattern. Their stated Round-45 need: an ordering-sensitive registered
statistic with a **smooth-heterogeneity plant** (no existing cell has power
against that alternative). Queue:
`analysis/round44/W2-B3-doublet-sites/ORACLE-T7-QUEUE.md`. → our F5.

Their **open leftovers**: base-60 sexagesimal margin digits pp34–39
(enumerated, never tested); 74 ornament bands (tested only with an
English-underpowered register — reopen listed); red-dot 30-bit stream
(measured-only; below their L<13 recognizer floor); p27:93 U-vs-B glyph
(human needed); figural motifs (oracle queue); R13 DIRECTION filed open.

### B3. What the negatives say collectively
Nine E-class negatives on our side carve the same region their 348 rows
carve: **no pairwise, uniform, algebraic pad (additive or multiplicative,
any global orientation, any index consumption) between any two LP2 pages
produces designed structure** — and their side adds: no single-alphabet
cipher class, no ~200 external keytexts, no seeded/seedless pad source
below the tails, no image channel, no token-table reading.

**Dukotah's meta-conclusion (adopt with eyes open):** LP2 0–54 is
**OTP-class** — the ciphertext cannot separate a true external pad from a
short-seed keystream (they planted a short-seed keystream and recovered it
at 98.9%, and it looked exactly like the corpus). Pad **unpublished by
design**; and message-*existence* is undecidable from the ciphertext alone.
Our nine negatives are *consistent with* that verdict, not evidence against
it. Consequence for this map: stream-cipher hunting has thin marginal value
now; what's left is (a) the **index/selection channels** that no stream
test touches (red marks, digits, lattices, tokens-as-coordinates), (b)
**independent certification of T7** — their one live anomaly, and an
independent check is exactly what their discipline asks for, (c) the bounded
**tails** of their PRNG sweeps (theirs to run; we don't duplicate), (d)
register-panel gaps (their negatives are English-registered; our
language-agnostic χ² is the complement, which is why F5/F7 are *ours* to
run and F6 is not).

---

## C. UNKNOWN — the real questions (ranked by leverage)

| # | question | what would answer it | probed by |
|---|----------|---------------------|-----------|
| U1 | What is the keying model of pp0–49/51–55? | any GO prong hit | all frontiers |
| U2 | What are the pp49–51 token tables FOR? — dukotah has killed key/text/container/hash/QR/index readings ("OTP-class blob"); **affine-scaled canon-as-key (our T2, a≠1) and coordinate/pair-split readings may still be open on their ledger** | a reading that yields structure or text | F3 |
| U3 | Do red marks / lattices / digits SELECT (indices) rather than decorate? | digits 1–5 / lattice dot-counts mapping to positions that reveal structure | F2, F7, F9 |
| U4 | Is the doublet slip-rate non-stationarity (dukotah **T7**, p≈0.001, their only live anomaly) real? (independent replication = highest-value community contribution available) | our run-structure nulls on the 86 doublet sites, independent of their oracle machinery | F5 |
| U5 | Is p50 (runeless token page) a key, a target, or a divider? | token-vs-page tests beyond affine (F3/F13) | F3, F13 |
| U6 | Does LP1 key continuity reach LP2 (vocabulary, keys, mechanisms)? | LP1-derived keys firing on LP2 w/ matched null | F6 (**likely closed by their ~200 keytexts — dup-check untried.md before spending anything**) |
| U7 | Plaintext language/register? (their negatives are English-registered; our instrument is deliberately language-agnostic — the complementarity is our niche) | any GO + human read | downstream |
| U8 | Image/physical channel? — largely CLOSED by dukotah (stego/geometry/chroma/font, 8–19 bar-units); figural motifs remain (their oracle queue) | signal in pixel domain | F15 (DEPRIORITIZED — theirs) |
| U9 | Unknown unknowns: features nobody has catalogued yet | systematic per-page feature census | F16 + owner reads |

---

## D. FRONTIER QUEUE

Scores: **prior** (evidence the designers did this elsewhere: LP1/solved LP2
analogy) · **power** (can a planted signal beat the family null? hard rule
below) · **cost** · **blocker** · **dup** (dukotah overlap risk).
Status: **READY** / **GATED(owner)** / **GATED(dup-check)** / **DEPRIORITIZED**.
Rows are ordered by current rank. Post-digest reshuffle (2026-11-16): F5
promoted (T7), F7 promoted (their English-underpowered reopen), F17 new;
F3/F4/F6/F10/F15 demoted by community coverage.

| id | frontier | first cheap test | prior | power | cost | blocker | dup | status |
|----|----------|------------------|-------|-------|------|---------|-----|--------|
| **F5** | **T7 replication — doublet slip-rate non-stationarity** (dukotah's ONLY live anomaly, p≈0.001, `measured` never certified; their R45 target). Independent check with OUR run-structure nulls (#4's 2000-rep machinery) on the 86 doublet sites — no oracle, no English, independent lineages | ordering-sensitive statistic (their gap-permutation null + lag-1 gap autocorr, target +0.380) vs. our own gap-permutation runs; **register the smooth-heterogeneity plant they say is missing** (their C5 shows per-page tests are blind — plant must be block-scale); then localize | **high** (their stats discipline + it's their one open door; independent replication is the community contribution) | good (descriptive/structural, no max-scan) | low | none — **their doublet-site list format** (read `W2-B3-doublet-sites/`) | none (independence IS the value) | **READY — recommend as next campaign (#10) or alongside F1** |
| F1 | **Word-sum self-keys (U3)** — literal word-boundary sums via dividers (LP1 line-sum design's LP2 analog; #8 tested LINE sums) | LS variant with divider-delimited words on p51 (divider-fidelity-verified page) first, then corpus | med-high (house style A2) — **downgraded: their R11-S2 found separators `/.-` are typography, not designed marks**; LP1 line sums are *plaintext*-side anyway | good (long windows) | low | divider-fidelity beyond p51; re-read their separator finding before registering | med (their pad-restoration oracle, 1,800 generators — check word-sums specifically) | READY — currently booked #10, **reconsider vs F5** |
| F2 | **Red selection channel** — digits 1–5 (red, pp36–38) + p15 red 3299 + p53 arrow as *selectors* (pick line/word/position); also the red-dot **30-bit stream** (dukotah measured it but it's below THEIR L<13 recognizer floor — untested by anyone) | owner double-check crops (RED_CENSUS queue) → then design: digit d at line L selects position/direction | high (red = deliberate; LP1 loves emphasis; 14 red section-head pages per their census) | TBD by design; 30-bit stream is below ANY windowed statistic — descriptive/oracle only | low | **owner eyes** (queue exists) | census dup w/ their R44-P1 (213 runes) — our selection TESTING is not dup | **GATED(owner)** |
| F7 | **Ornament bands / dot-lattices as data** — 35 lattices (3 dot-counts) + their 74 ornament bands, which they tested only with an **English-underpowered register and explicitly re-listed** | language-agnostic structural test: lattice/band (page, position, count) triplets vs. run-structure nulls — our complement niche | med-high (their own reopen list) | good (structural, language-free — exactly our instrument's edge) | low | none | low (they re-listed it BECAUSE underpowered) | **READY — promoted by digest** |
| F17 | **Base-60 sexagesimal margin digits pp34–39** (their enumeration; never tested as data) | census the sexagesimal groups; arithmetic relations to page structure / token table base-60 (same base as pp49–51!) | med (base-60 recurs — token tables are base-60 too) | n/a (descriptive first) | low | none | low (enumerated, not tested) | **READY — new from digest** |
| F3 | **Token-table residual semantics** — most readings killed by dukotah (key/text/container/hash/QR/index; "OTP-class blob"). Residual: **affine canon-as-key a≠1** (their 6.4M canon-as-key sweep — verify a∈2..28 was covered; our T2 says no signal at planted strength anyway) and coordinate/pair-split readings | check their CAMPAIGN-IX config list for affine coverage; if a≠1 uncovered, one small preregistered family | low-med post-digest (was med-high) | fixable (shrink family, F13 note) | low | dup-verify | **high** | GATED(dup-check) — demoted |
| F4 | **Columnar / transposed / boustrophedon reads** | their transposition-only elimination + English-only boustrophedon red_team largely cover this; our edge is only the language-agnostic angle on transposition | low (post-digest) | med | low | none | high | DEPRIORITIZED (demoted by digest) |
| F6 | **LP1→LP2 key continuity** | their ~200 keytexts incl. Cicada prose very likely cover DIVINITY/atbash-as-pad on LP2 | low post-digest | good | low | none | **very high** | DEPRIORITIZED (demoted by digest) |
| F8 | **p53 red lines + arrow** — all-red stream lines 7–9 + arrow: emphasis = "read here/how"? | owner check (in F2 queue) then orientation/direction hypotheses | med | TBD | low | owner | low | GATED(owner) |
| F9 | **Digits as selectors** (not keys — #7 killed additive use): p10 `7`, pp36–38 `1–5`, p15 groups → position/line/word indices | enumerate selection readings; test decoded-position consistency | med | TBD | low | rides on F2 owner check | low | GATED(owner) |
| F10 | **Mid-range cyclic steps** (29..L−29, priced out of #6) | studio run of the existing W harness | low (OTP-class meta lowers residual hope) | good (harness proven) | **high** (studio, est. days) | studio scheduling | low | DEPRIORITIZED (expensive closure of a thin slice) |
| F11 | **Position-dependent pads** (pad value varies by place/digit/ornament) | needs a concrete generator family first; their pad-restoration oracle already disfavors generator models | low | unknown | unknown | design | med | DEPRIORITIZED (unscoped) |
| F12 | **Triple products / non-uniform interleavings** | 3-page composites: space ~O(55³) — cost explodes; only with a sharp generator | low | unknown | high | design | low | DEPRIORITIZED |
| F13 | **p50/tokens as TARGET** (pages-as-keys INTO the token blob — reverse of their canon-as-key) + T2 strong-signal regime (shrink family so planted χ² can beat the matched median) | re-scan with family = page-derived pads × token-table target ONLY | low-med | fixable (the W lesson: shrink the family) | low | none | low-med (verify their direction coverage) | READY (rank low) |
| F14 | **LP1 pages as targets** | our harness on LP1 streams (transcription lineage check first) | low-med | good | low | LP1 stream fidelity | high (LP1 heavily mined) | READY (rank low) |
| F15 | **Image/physical channel** | largely CLOSED by dukotah R44 (stego, geometry, chroma, font variants, 8–19 bar-units); figural motifs = their oracle queue | low | unknown | high | tooling | **very high** | DEPRIORITIZED (theirs) |
| F16 | **Owner readthroughs p49/p51/p55** (+ divider-fidelity spot checks; + p27:93 U-vs-B glyph — their ledger also wants a human eye here, we could answer it) | human eyes on crops we already cut (work/audit/) | — | — | owner time | owner | none | **GATED(owner) — feeds everything** |

### Power hard rule (lessons #7-Vs, #8, #9-T2, all in one line)
> A family whose *planted* windows cannot exceed its own null median is not
> testable with χ²-of-max — either **shrink the family** (fewer windows →
> lower median) or **change the statistic**. Every PREREG must include the
> power probe result *before* the verdict is called informative.

---

## E. TRIAGE PROTOCOL for new ideas (the "methodically" part)

1. **Write it down here** (§D) with the score row — no campaign without a
   queue row first. A new idea displaces nothing until the owner agrees.
2. **Dup check first:** dukotah untried.md + their eliminations + our LEDGER
   "NOT covered" cells. We inherit their open list; we don't redo weak
   negatives (ours or theirs) without a *stronger instrument*, not just a
   rerun.
3. **Prior from design vocabulary (§A2):** "the designers did this exact
   thing in solved material" ≫ "a cipher could do this". LP1 analogy is our
   cheapest prior.
4. **Power before cost:** run the hard rule. An unpowered test is a
   scheduled disappointment, not cheap insurance.
5. **Blocker honesty:** GATED items don't enter the sprint; they enter the
   owner queue (F2/F8/F9/F16 are all the same queue).
6. **One campaign at a time, prereg first, null matches the scan, escalate
   at the median, disclose everything** (LEDGER rules — unchanged).
7. **Every close updates this map**: §B row, §C re-rank if anything was
   learned, §D statuses (a negative should *demote or kill* at least one
   frontier row — if it doesn't, we scanned something we didn't care about).
8. **Convergence note:** dukotah's ARMADA-DOCTRINE independently evolved the
   same rules ("aim at the instrument before the space — every real finding
   came from auditing a closure/instrument/input, never a new key-space
   sweep"; "Value = coverage × power, report both or neither"; pre-register,
   plant, persist language-agnostic stats). Where our ledgers differ: ours is
   language-agnostic by construction, theirs is English-registered with a
   12-register panel. Two honest teams, same discipline, different
   instruments — that complement is the map's main asset.

## F. Current standing order (as of 2026-11-16, post-digest)

1. **F16/F2 owner queue** — the only hard blocker; crops are cut and waiting
   (bonus: their ledger also wants a human eye on p27:93 U-vs-B).
2. **#10 decision pending owner pick:** F5 (T7 replication — now our
   highest-prior unblocked idea: independent check of the community's only
   live anomaly, cheap, in our complement niche) vs F1 (word-sum, booked,
   but downgraded by their separator-is-typography finding). My recommendation:
   **F5 first**, F1 second — and a T7 replication result is shareable
   upstream (public action → needs owner approval each time).
3. Cheap descriptive between campaigns: F7 ornaments, F17 sexagesimal
   margins, F13/F3 dup-checks against their config listings (read-only
   repo work; no PREREG gate — censuses, not hypothesis tests; a flag
   promotes to a preregistered campaign).
4. Dup-check debts from the digest: did their canon-as-key cover affine
   a≠1 (F3)? did their 1,800-generator oracle cover word-sums (F1)? did
   their keytext list include DIVINITY-on-LP2 (F6 — probably yes)?
5. Watch Dukotah #13/#14 for replies (none as of 2026-11-16); their Round 45
   will likely hit T7 — our independent replication is time-sensitive to be
   complementary rather than redundant.
