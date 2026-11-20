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
  LP1 rune pages 01/03/04/05/06/09/10/13/14/16 are solved (2014 public wave —
  wiki "CICADA 3301 2014 PUZZLE FACTS PART 4", 12 Jan 2014; atbash,
  atbash+shift3, identity, Vigenère DIVINITY with key CONTINUOUS across the
  03/04 break / FIRFUMFERENFE) — all regression-gated in `core/validate.py`
  with content pins (rune count + sha256[:16], since per-JPEG triage mis-files
  pages); 03/14 had been carried as open leads until the 2026-11-18 external
  review (LEDGER C3), and 04/09/10/13/16 were confirmed from the review's
  round-2 recipes (LEDGER C6 — known-solutions gate now closes that failure
  mode).
- **Headline statistic (promoted 2026-11-18, LEDGER C4):** the unsolved
  corpus carries 86 doublets vs ~445 expected (~17σ; suppression 0.81 /
  leak ~0.19). The machine-applied anti-doublet filter is the defining
  artifact of the unsolved bulk — solved pages are NOT homogeneous
  (p56 2.38%, p57 1.06%, small-n caveat; unsolved 0.66%). Top mechanism
  target: leak fingerprint + the key-consumption question (does the filter
  skip key? dukotah says yes, Wulfic no — decides the decoder class for
  every sweep, and invalidates rigid-alignment power claims: dukotah R34
  B1 measured skip-invisibility, prefilter power 0.66/0.71 not 0.998).
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
  **all red** ⚿; p15 four 4-digit groups, one red (`3299`) ⚿ — **CLOSED
  FORM 2026-11-18:** the 16 numbers = `|3301 − prime(F+1)|` over distinct
  Fibonacci F, square-spiral from the red `3299` = 3301−prime(1) (LEDGER C2;
  validate gate 6). Containment/pointer readings retracted; red = spiral
  origin, consistent with red-marks-openings.
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
| U4 | Is the doublet slip-rate non-stationarity (dukotah **T7**, p≈0.001, their only live anomaly) real? (independent replication = highest-value community contribution available) | our run-structure nulls on the 86 doublet sites, independent of their oracle machinery | F5 — **ANSWERED 2026-11-19: REAL (#30 CERTIFIED-NONSTATIONARY, window rate 0.274, p=0.0024, lineage disclosed; see F23)** |
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
| **F5** | **T7 replication — doublet slip-rate non-stationarity** (dukotah's ONLY live anomaly, p≈0.001, `measured` never certified; their R45 target). Independent check with OUR run-structure nulls (#4's 2000-rep machinery) on the 86 doublet sites — no oracle, no English, independent lineages | ordering-sensitive statistic (their gap-permutation null + lag-1 gap autocorr, target +0.380) vs. our own gap-permutation runs; **register the smooth-heterogeneity plant they say is missing** (their C5 shows per-page tests are blind — plant must be block-scale); then localize | **high** (their stats discipline + it's their one open door; independent replication is the community contribution) | good (descriptive/structural, no max-scan) | low | none — **their doublet-site list format** (read `W2-B3-doublet-sites/`) | none (independence IS the value) | **DONE 2026-11-16 — campaign #10 REPLICATED (S2 p=0.0006, D=10,000, independent nulls; site tuple bit-identical to theirs). Bonus: power curve shows the signal is LOCALIZED (1,649-rune doublet-free span pos 2739–4388), not smooth drift — R45 should plant voids. Upstream post pending owner approval → POSTED 2026-11-18, dukotah #13 cmt 6995327465.** CORRECTION 2026-11-18 (LEDGER C1): "doublet-free" WRONG — span contains doublets 2740/3140/3852; read as three consecutive large gaps 400/712/537. REPLICATE = reproduced (same 86 sites; validates null calibration, not forking-paths independence) |
| F1 | **Word-sum self-keys (U3)** — literal word-boundary sums via dividers (LP1 line-sum design's LP2 analog; #8 tested LINE sums) | LS variant with divider-delimited words on p51 (divider-fidelity-verified page) first, then corpus | med-high (house style A2) — **downgraded: their R11-S2 found separators `/.-` are typography, not designed marks**; LP1 line sums are *plaintext*-side anyway | good (long windows) | low | divider-fidelity beyond p51; re-read their separator finding before registering | dup-check DONE 2026-11-16: their LP1-sums-as-keystream (R37-C1-U2) + word-sums-as-cleartext (R10-L2/R37-C3) covered; LP2 self-word-sums as key schedule was open | **DONE 2026-11-16 — campaign #11 NEGATIVE all families (p 0.16–0.67) but WEAKLY-POWERED (0/10 plants): page-marginal χ² structurally blind to local plants under value-dependent self-derived keys (key propagation rotates downstream decodes). Re-run needs word-window statistic; NOT recommended vs LOW prior + #8's powered line-sum negative. LEDGER row 11** |
| F2 | **Red selection channel** — digits 1–5 (red, pp36–38) + p15 red 3299 + p53 arrow as *selectors* (pick line/word/position); also the red-dot **30-bit stream** (dukotah measured it but it's below THEIR L<13 recognizer floor — untested by anyone). **Owner confirmed 2026-11-16: red digits 1–5 pp36–38 CONFIRMED (p36 L6=1, p37 L1/5/10=2/3/4, p38 L4=5); NEW observation: red "10-dot pattern" at p38 L10 (sentence/paragraph end?) — crop follow-up queued; digit-style ANSWERED 2026-11-16: printed not wedge (F3, sexagesimal dead)** | design: digit d at line L selects position/direction | **high (channel now owner-confirmed)** | TBD by design; 30-bit stream below any windowed statistic — descriptive/oracle only | low | follow-up crops (ours), then design | census dup w/ their R44-P1 (213 runes) — our selection TESTING is not dup | **DONE 2026-11-16 — campaign #15** (D1/D2/D3 selection readings all NEGATIVE p=1.000 powered; digits retired as in-LP2 selectors; 30-bit stream still below floor — descriptive/oracle only) |
| F7 | **Ornament bands / dot-lattices as data** — 35 lattices (3 dot-counts) + their 74 ornament bands, which they tested only with an **English-underpowered register and explicitly re-listed** | language-agnostic structural test: lattice/band (page, position, count) triplets vs. run-structure nulls — our complement niche | med-high (their own reopen list) | good (structural, language-free — exactly our instrument's edge) | low | none | low (they re-listed it BECAUSE underpowered) | **DONE campaign #13 (`db6f467`): O1 head-alignment FLAG p=0.00065 (11/14, exp 5.4) — structural, oracle round #4 S4/S5 gate interpretation; O2/O3 NEGATIVE powered (p=0.385 / exact 0.447); O4 shared y-grid, 188-px pitch refuted. Band glyph internals remain dukotah's; lattices carry NO count/page-level information** |
| F17 | **Base-60 sexagesimal margin digits pp34–39** (their enumeration; never tested as data) | census the sexagesimal groups; arithmetic relations to page structure / token table base-60 (same base as pp49–51!) | med-high (owner's form-distinction reading + base-60 recurs) | n/a (descriptive first) | low | none | low (enumerated, not tested) | **CENSUS DONE 2026-11-16** (`sweeps/2026-11-sex60/CENSUS.md`): the "pp34–39 digits" = ONE black stamp pixel-identical ×6 (tops pp34–39) + p33 footer (brackets the section; placement is its only per-page info) + RED printed digits 1–5 pp36–38 (values known; wedge-vs-printed = owner round-#2 F3). Stamp values → oracle round #3 (S1–S3). Machine wedge-count failed, disclosed. F18 PREREG next |
| F18 | **In-document OTP** (owner thesis 2026-11-16: objects formally distinguished FROM THE TEXT serve as keys/selectors for other parts). Coverage matrix — page→page: **closed** (theirs C2 all-pairs ±/shift/offsets, 6.4M; ours #1–#9, ~370M, incl. multiplicative+orientations); token-table→page additive: **closed** (their C2 canon-as-key); token→page affine a≠1: only our T2, **weakly powered**; solved-plaintext→page: **closed** (their R44-R1 roster incl. solved-derived streams); **base-60 margin digits as VALUES: OPEN** — they tested only instruction/size-match readings (LP2-H1 T3: first-digit 0–4 can't index 13–14 sections; count≠table dims), never as keystream/pad/selector; **page→token-blob (reverse direction): OPEN**; margin-art set-partition (sexagesimal 34–39 / mayfly 24–26,57,14 / dendrites 8–14,32,55) as a per-set cipher-variation axis: THEIR OWN unfired suggestion ("faint open thread, low EV") | F17 census first; then: sexagesimal values as pad over set-pages (long-range, set-local), as selectors; page→blob reverse scan | med-high | pad-over-page good (targets long); selector TBD | low-med | F17 census; owner Task-1 digit-style answer | low (their T3 ≠ value consumption) | **DONE 2026-11-16** (LEDGER row 12): PB1 reverse scan NEGATIVE p=1.0, weakly-powered 0/10 (many-to-one map dominates window χ² — class-conditional stats would be needed, not recommended); per-page sexagesimal VALUES falsified by census (stamp identical ×6) — value-as-pad premise dead, stamp glyph values → oracle #3, red-digit values → owner F3 |
| F3 | **Token-table residual semantics** — most readings killed by dukotah (key/text/container/hash/QR/index; "OTP-class blob"). Residual: **affine canon-as-key a≠1** (their 6.4M canon-as-key sweep — verify a∈2..28 was covered; our T2 says no signal at planted strength anyway) and coordinate/pair-split readings | check their CAMPAIGN-IX config list for affine coverage; if a≠1 uncovered, one small preregistered family | low-med post-digest (was med-high) | fixable (shrink family, F13 note) | low | dup-verify | **high** | GATED(dup-check) — demoted |
| F4 | **Columnar / transposed / boustrophedon reads** | their transposition-only elimination + English-only boustrophedon red_team largely cover this; our edge is only the language-agnostic angle on transposition | low (post-digest) | med | low | none | high | DEPRIORITIZED (demoted by digest) |
| F6 | **LP1→LP2 key continuity** | their ~200 keytexts incl. Cicada prose very likely cover DIVINITY/atbash-as-pad on LP2 | low post-digest | good | low | none | **very high** | DEPRIORITIZED (demoted by digest) |
| F8 | **p53 red lines + arrow** — all-red stream lines 7–9 + arrow: emphasis = "read here/how"? Owner 2026-11-16: **arrow confirmed pointing UP**; lines 7–9 confirmed red in excerpt but crops too tight to certify whole lines — wider crops owed | orientation/direction hypotheses (up = back-refers to lines 1–6? to page top?) | med-high (arrow direction = data) | TBD | low | wider crops (ours) | low | PARTIAL-OWNER — crops owed, then testable |
| F9 | **Digits as selectors** (not keys — #7 killed additive use): p10 `7`, pp36–38 `1–5`, p15 groups → position/line/word indices | enumerate selection readings; test decoded-position consistency | med | TBD | low | rides on F2 owner check | low | **PARTIAL 2026-11-16 (campaign #15): digits 1–5 tested, ALL selection readings NEGATIVE powered; p10 `7` + p15 groups remain enumeration-only (no anchor found)** |
| F10 | **Mid-range cyclic steps** (29..L−29, priced out of #6) | studio run of the existing W harness | low (OTP-class meta lowers residual hope) | good (harness proven) | **high** (studio, est. days) | studio scheduling | low | DEPRIORITIZED (expensive closure of a thin slice) |
| F11 | **Position-dependent pads** (pad value varies by place/digit/ornament) | needs a concrete generator family first; their pad-restoration oracle already disfavors generator models | low | unknown | unknown | design | med | DEPRIORITIZED (unscoped) |
| F12 | **Triple products / non-uniform interleavings** | 3-page composites: space ~O(55³) — cost explodes; only with a sharp generator | low | unknown | high | design | low | DEPRIORITIZED |
| F13 | **p50/tokens as TARGET** (pages-as-keys INTO the token blob — reverse of their canon-as-key) + T2 strong-signal regime (shrink family so planted χ² can beat the matched median) | re-scan with family = page-derived pads × token-table target ONLY | low-med | fixable (the W lesson: shrink the family) | low | none | low-med (verify their direction coverage) | **DONE campaign #14 (`31c38c3`): R1 re-powered NEGATIVE p=0.905 (20/20 plants — W-lesson fixed), R2 blob-as-target NEGATIVE p=0.810 (20/20). Token consumption map now complete both directions, last two powered. Residual: p50 104-token stream needs a CENSUS (not a sweep)** |
| F14 | **LP1 pages as targets** | our harness on LP1 streams (transcription lineage check first) | low-med | good | low | LP1 stream fidelity | high (LP1 heavily mined) | READY (rank low) |
| F15 | **Image/physical channel** | largely CLOSED by dukotah R44 (stego, geometry, chroma, font variants, 8–19 bar-units); figural motifs = their oracle queue | low | unknown | high | tooling | **very high** | DEPRIORITIZED (theirs) |
| F16 | **Owner readthroughs p49/p51/p55** (+ divider-fidelity spot checks; + p27:93 U-vs-B glyph — their ledger also wants a human eye here, we could answer it) | human eyes on crops we already cut (work/audit/) | — | — | owner time | owner | none | **GATED(owner) — feeds everything** |

### D-addendum (2026-11-18, external review plan — QUEUED, owner ranks)

Derived from the external review (work/LP2_external_review.md; verified
claims in LEDGER Corrections). Not yet triaged per §E — owner picks.

| ID | Idea | Notes | Status |
|----|------|-------|--------|
| F17 | **Track A — anti-doublet filter as mechanism** (review's lead track, ~30%) | Model comparison, not scans: register {constant leak, per-section leak, sessions w/ changepoints, state-dependent rejection, hand error}; fit to the full 12,955-pair sequence; compare by likelihood + parametric-bootstrap predictive checks on a fixed battery (gap ac1, 3-gap sum, block dispersion). Leak fingerprint: 0.19 observed vs 0.034 single-redraw (excluded) — enumerate code idioms × predicted leak. **Key-consumption decision first** (dukotah skip vs Wulfic independent-replacement): decides decoder class for every sweep; all rigid-alignment power claims (incl. #23/#24A/#25D plants) are optimistic until resolved. **Reviewer round-2 hand-off (2026-11-18)**: 15 leak idioms enumerated A–O, survivors D-with-drift (stationarity gate 1/5), J-scattered, M, N, O; closed-form leak rate q(1−s)/(1−qs), q=1/29 → s=0.813 reproduces LP2's 0.664% doublet rate. Fit plan: Bernoulli baseline; changepoint BIC k=1–4 (anywhere / page boundaries / sections); 2-state HMM pinned at 1/29; stopping rule ΔBIC>10 under page-holdout, else retire the changepoint lane (reviewer's "F9"). **CAMPAIGN #26 DONE 2026-11-19** (PREREG b45ad51; addenda a06a8be G4 + 5ee80d3 power-plant-relative; REPORT): **A1 SEPARATES** — key-skip vs plaintext-redraw (key held) separate via dc_chi2 at p=1.5e-18; UNIFORM replacement ≡ skip (memo survives only for that); corpus leans key-skip (F2 dc flat p=0.038); **discriminator scan OWNER-GATED**, decoder-class decision OPEN (#23/#24A/#25D annotations NOT applied). **A2 NULL-RETIRE, UNINFORMATIVE per registered power rule** — P1 ΔBIC₂=−24.7 (k=2 = 66-rune burst [5771,5837]) / P2 p=0.576 (D=10k) / P3 miss / CV sign fail; power 0/10: 37.9-nat penalty vs ~13 available — T7 pattern VISIBLE at k=4 (bounds 2741/4389, middle rate 0.0012) yet unconfirmable by any location-search BIC statistic; HMM collapses to one state. T7 = recorded anomaly (#10 gap-ac1), mechanism neither certified nor refuted; reopen requires fixed-window rate-ratio test (edges named in advance, no location search) — NEW campaign. Track C unblocked per stopping rule. FOLLOW-UP SCAN #27 (owner-approved, PREREG c0ec6ca, 2026-11-19): directional English-difference-excess test on the 12,869 nonzero corpus diffs — V1 p=0.405, V2 p=0.072, α̂=+0.034±0.023 (at redraw prediction, noise-compatible); power 6/20, 9/20 ⇒ **UNINFORMATIVE**: two-sample identifiability ≠ single-stream decidability (English diff-dists mod 29 nearly uniform, corpus Z≈1.5) — key consumption NOT decidable at emitted level on this corpus; skip-tolerant stays conservative default, #23/#24A/#25D annotations remain deferred. **Review round-4 corrections (2026-11-19, LEDGER C8)**: redraw inflation ≈ **0.09×** observed excess, not ~10×; **"corpus leans key-skip" RETRACTED** (density ratio at χ²=41.4 = 1.37 redraw-lean — negligible); dc_chi2 = ALL adjacent pairs, no oracle (fit.py L408–410) — SEPARATES stands as two-sample only. **Round-5 (C9)**: reviewer's chi-square power ≈0.07 and our #27 directional recoveries (V1 30%, V2 45%, bar 19/20) are DIFFERENT tests — same verdict (corpus does not select a rule), NOT replications; skip-tolerance = working assumption, not finding | **DONE (both lanes UNINFORMATIVE; question stays open by measurement, not by assumption)** |
| F18 | **Week-one reconciliation** | (i) ~~lineage diff: explain 9.2% LP1 agreement~~ **CLOSED 2026-11-19 = CATEGORY ERROR (LEDGER C8)**: stream B (armada18 `lp1_runes_as_key.json`) is the solved LP1 English re-spelled into runes — exact LCS vs B: decoded 2,648 (94.6% of A) vs ciphertext 1,426 (51.0%) (C9 canonical, single denominator); the "disagreement" compared ciphertext to a plaintext-derived key file; no image audit needed (general scream-vs-images caveat stands separately); (ii) cross-ledger review BEFORE new sweeps: Wulfic (claims periodic keys to 11,781, autokey to 12,863, per-section restarts — may close §7.5 gaps), Leo-Y-Zhang, TheronEagle, jens-wedin | (ii) QUEUED |
| F19 | **Track B — print channels, machine-measured** (~25%) | Glyph metrics table (position/size/ink/spacing × 13,136 runes, connected components, onion JPEGs — dukotah lists sub-2px placement + kerning as not excluded); line-break model (388/604 breaks mid-word — predict from glyph widths, residuals = channel; dup-check both ledgers first); owner queue items presented BLIND with decoys (review methodology point) | QUEUED |
| F20 | **Track C — finite seed spaces only** (~20%) | dukotah MEASURED-CEILING: ~52% of Python 2.7 MT space, ~99% PHP mt_rand unswept — closeable with existing decoder + null on studio; hint-grammar generators (every solved key was announced in nearby plaintext — enumerate hint×operation yielding flat aperiodic keys). **UNBLOCKED 2026-11-19** (#26 done; stopping rule releases Track C) — PREREG before output; design rule inherited from #26: register the power plant FIRST and make the primary statistic's detectability of its own target a gate. **Campaign #28 PREREG registered 2026-11-19** (this commit): full 2^32 re-sweep under one own instrument — cell A Py2.7-MT `init_by_array`+`random29`, cells B/C PHP mt_rand both twists × scale/mod, both signs, skip-tolerant quadgram-LL head screen (relation-agnostic: covers keyskip1+2 per #27), 20-plant ladder/cell + margin_gate 2.0 nats gates any CLOSED-NO-KEY; hint-grammar generators deferred to #29 | **DONE 2026-11-19 = ALL LANES CLOSED-NO-KEY (LEDGER row 28; 12,884,901,888 seeds under one instrument): A null_max −371.4 vs plant_min −268.7 (margin 102.6 nats), B −368.3/−282.7 (85.6), C −373.1/−275.2 (97.9); 0 seeds ≥ B; dukotah Py2.7-exact 52% mixed cursor → 100% single-instrument; PHP 0.97%/twist → 100% × 2 twists × 2 reductions; conditionals L1–L6 (offset-0, 120-rune head, quadgram proxy). Hint-grammar generators = #29. **#29 DONE 2026-11-19 = ALL CELLS CLOSED-NO-GRAMMAR (LEDGER row 29): 592,574 aperiodic structured decodes — plaintext-autokey (keyskip0, L9: filtered plaintext-autokey undecodable by construction), ciphertext-autokey (Wulfic class), running keys from all pinned book-internal hints, derivable math streams; obs maxes −400…−418 all null-level, margins 88–140 nats, 0 flags; G2 proves grammar contains p56 solution. TRACK C CLOSED modulo disclosures: external literary keytexts (L4), key-transposition chains (L6), filtered PT-autokey (L9), unseeded (#28 L6)** |
| F21 | **Method items (no campaign slot needed)** | Programme-level registered-statistics ledger (25 campaigns + ~350 upstream rows ⇒ p≈0.001 by chance); power reported as curve over plant size w/ intervals; every max-stat null states its minimum detectable plant; plants must pass through the filter model (F17 output feeds this) | ADOPTED as practice |
| F22 | **Stopping rule** | Review: decide NOW what ends the programme (e.g. no confirmed positive from F17–F20 by fixed date → maintenance mode). Owner decision required | GATED(owner) |
| F23 | **T7 fixed-window certification** (the #26-A2 reopen path) | Single pre-named window W\* = 1,650 sites centered on the layout-derived p15 axis junction J=3611.5; statistic X = doublet sites in W\* vs #10-matched hard-core null (D=10,000); power curve over window rates ρ∈{0,.25,.5,.75,1}; edges doublet-independent by derivation (r5 constraint), selection lineage disclosed | **DONE 2026-11-19 = CERTIFIED-NONSTATIONARY** (campaign #30; PREREG d326090; LEDGER row 30): X=3 in W\* vs null mean 10.95, p=0.0024 (hypergeom 0.0033), rate ratio 0.274, jitter-robust; power curve 1.00/0.94/0.42/0.12/0.03; lineage disclosed (5th look; void-motivated landmark selection, review-prescribed test). First certified positive of the programme. Mechanism open (sessions/stateful/re-seed) with named target; relay owner-gated |

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

## F. Standing principle

The queue below (§G) is the ordering; this section records *why* the top
slot is what it is: F5 is time-sensitive (their Round 45 targets T7 — an
independent replication is worth most *before* their certification, and a
GO-adjacent result is shareable upstream, owner-approval each time), cheap,
and squarely in our complement niche (language-agnostic, independent nulls,
#4's structural-null machinery already built).

## G. The explicit queue (agreed 2026-11-16)

**Revision rule (owner's):** the queue is revised when NEW INFORMATION
arrives — dukotah replies/Round-45 results, oracle-queue answers, a GO flag,
a new high-prior idea that earns its §D row. Between revisions we proceed
strictly in order; no following of footsteps as they appear.

| slot | task | depends on |
|------|------|-----------|
| **1** | **Campaign #10 = F5 (T7 replication)** — **DONE 2026-11-16: REPLICATE, p=0.0006; power curve localizes the signal to a 1,649-rune void (LEDGER row 10). Upstream post = owner decision.** Void wording corrected 2026-11-18 (LEDGER C1): not doublet-free — three consecutive large gaps 400/712/537. **2026-11-19 (review r4, LEDGER C8): localization DEMOTED to recorded-only** — best-k2 likelihood split p≈0.58 does not support the window (and #26 P1 found a 66-rune burst instead); surviving statement = global gap serial correlation (lag-1 +0.380, p≈0.0006, post-hoc ×2 on same data); future F9 work: leak-1/29 sensitivity plant ~1,650 runes, D-stationary working model | — |
| **2** | **Oracle queue #1** — `docs/ORACLE_QUEUE.md`. **Owner answered 2026-11-16: red digits 1–5 CONFIRMED; p53 arrow = UP; lattices 13/10/23 confirmed (p49=10-dot); p27:93 leans U (crop too tight); NEW: red 10-dot pattern p38 L10.** Ours now: wider crops (p53 L7–9, p27:93, p38 L10) + wedge-vs-printed digit comparison sheet; then p10/p15 rows + p49/p51/p55 readthroughs remain open | our crop tooling |
| **3** | **Campaign #11 = F1 (word-sums)** — **DONE 2026-11-16: NEGATIVE all families, weakly-powered (0/10 plants; instrument lesson: page-marginal statistic blind to local plants under value-dependent keys — LEDGER row 11). Dup-check resolved: LP2 self-word-sums as key schedule was open in both ledgers; now closed at page-marginal resolution** | — |
| **4** | **Campaign #12 = F17+F18** — **DONE 2026-11-16: census corrected the premise (stamp pixel-identical ×6 + p33 footer; red digits values known) and PB1 reverse scan NEGATIVE p=1.0 weakly-powered (LEDGER row 12). Open hand-offs: oracle S1–S3 (stamp values) + owner F3 (digit style) gate any follow-up; slot 6 (F13) keeps the blob→page affine re-power** | — |
| **5** | ~~Campaign #13 = F7~~ **DONE 2026-11-16** (O1 FLAG p=0.00065 structural → oracle #4 S4/S5; O2/O3 negative powered) | none |
| **6** | ~~Campaign #14 = F13~~ **DONE 2026-11-16** (R1/R2 both NEGATIVE, powered 20/20; token direction map closed; LEDGER row 14) | none |
| **6b** | ~~black 4-dot diamond channel~~ **DONE 2026-11-17 = campaign #16** (LEDGER row 16): T1 diamond = rendered `.` CONFIRMED 126/127=99.2% (owner ◆-pass ground truth); T2 ornament alphabet: `&`=13-dot (18/18), `§`=23-dot (1/1), **`$` NOT a large lattice (8/9 non-adjacent) — unmapped**; ◆10 inline at `.`-positions never at `$`; T3 fourdots detector exact 28/50, ρ=0.823 (v2 backlog = enumerated disagreements); T4 residual plain `.`=19 (17 line-final, 0 red-adjacent) — no positional split diamond-vs-dot; open oracles: `$` shape?, 19 residual dots, black-vs-red ◆13 (6 marks unstarred), p49 r6c3 0s-vs-0S (S/s class) | — |
| **7** | ~~F2/F9 red-selection tests~~ **DONE 2026-11-16 = campaign #15** (D1/D2/D3 ALL NEGATIVE p=1.000, all powered — every reading selects 5 distinct runes; digit→position/line/word family retired; LEDGER row 15) | none |
| **6c** | **Language triage DONE 2026-11-17 = campaign #17** (LEDGER row 17): apostrophes 6/6 MEDIAL = English contractions (Latin REFUTED, Romance-elision disfavoured); word-length chi² vs in-book English reference CONSISTENT p=0.506 (low power); **crib design proceeds English-first** (multi-language family = registered fallback). Remaining 6c work: | — apostrophe p41L10 (raised mark, machine-confirmed), double quotes p43L1 (visible "::", survives in krisyotam as the single '.'), p42 L3/L6, p53 L3/L6 (owner-confirmed; NOT in transcription — **krisyotam is lossy for punctuation**). Owner's decode insight: word lengths + punctuation are crib constraints ("apostrophe mid-word narrows to a very small set"). Needs: machine census (raised-dot vs mid-dot detector, all pages), then constraint-based crib design (F1 successor). Also refines #16: krisyotam '.' is heterogeneous (sentence-dots AND quotes) — ordinal test must allow that | none (census is machine-side) |
| **6d** | **Decoration segmentation DONE 2026-11-17 = campaign #18** (LEDGER row 18): owner hypothesis (decorations delimit passages) formalized as **10 groups** (owner-corrected P1=pp0–2 fence+∞; table in sweeps/2026-11-segments/PREREG.md + visual doc docs/SEGMENTS.md). Gates G1–G3 EXACT (12,956; partition; T7 void sites 2740/3140/3852/4389 reproduced exactly). Panel: S2 doublet deficit 9/9 groups SUPPORTS Holm p=0.008 (weak discrimination disclosed); S1 void wholly inside P4 (p7↔p23 bracket) p=0.27 NEUTRAL; S3 dots p=0.94, S4 word-lengths p=0.85 NEUTRAL. **VERDICT NO-GROUPS-EVIDENCE, 0 REFUTES** → segmentation = presentation frame + tracked artifact; pipeline stays pooled. Re-test trigger **FIRED 2026-11-17**: owner round-7 full decoration pass (committed 396e2c2) moves 3 boundaries — scrolls pp3–7 (P2+P3 merge), cicadas incl. p26, mirrored scrolls continuous pp40–55 (P8+P9 merge) → **v2 = 7 unsolved groups** in docs/SEGMENTS.md (Q1 pp0–2 · Q2 pp3–7 · Q3 pp8–22 · Q4 pp23–26 · Q5 pp27–32 · Q6 pp33–39 · Q7 pp40–55; 12,956 verified). #19 re-test queued pending owner sign-off on v2 (open: p23 hinge, pp16–21 interior, Q4 membership 23–26 vs 24–26) | owner sign-off on SEGMENTS.md v2 |
| **8** | **Campaign #19 = p15 axis reading** — **DONE 2026-11-17: AXIS-ALIGNED** (LEDGER row 19; PREREG 9924022). T7 void centers on the p15 decimals/∞ axis: largest-gap midpoint 115.5 runes from the &-junction, permutation p=0.0168; fixed-span p=0.0084; Holm min adj p=0.0168. Gates exact (terminator map, junction J=3611.5, 7/7 boundary fidelity). V4: v2-unit homogeneity holds (dots 0.82, wlen 0.69). Axis = tracked structural feature, no re-keying. Follow-ups: (a) does the axis SELECT (decimals 2838/3278/3298/3299 all inside pre-axis span 1874–3602 — selector design vs #15-style powered nulls); (b) 6c crib design may now treat pp8–14 / pp16–22 as separate crib units. CORRECTION 2026-11-18 (LEDGER C2): the grid has a closed form (A3) that needs no axis, and follow-up (a) is moot (containment was construction); **axis DEMOTED to recorded-only — not carried** (review: p=0.0168 with post-hoc landmark motivation; we add: single registered junction, but the p15 choice itself was furniture-motivated) | ~~owner steer on (a)/(b)~~ closed by C2 |
| **9** | ~~Campaign #20~~ **DONE 2026-11-17: DECIMALS-STRUCTURED** (LEDGER row 20; PREREG c12578c) — all four grid rows inside the T7 void (p=2.6e-4) and pre-axis span (p=3.2e-4); digit sums {20,21,22,23} consecutive (p=0.0039); Holm all survive; post-hoc origin disclosed -> **confirmation campaign (#22?) with independent prediction required before adoption**. Design-pass detail below. | CONFIRMED ROUND #7 DONE (owner 2026-11-18): S11 no new decimal group -> ONE-OFF per frozen rule; S12 REFUTED (3299 middle); S13 weak-consistent. GRID DISCLOSURE: recorded 4x4 = 16 numbers (3 witnesses); corrected object: 11/16 void p=3.3e-7, 12/16 span p=3.3e-8, row 4 fully outside, consecutive sums only in red row (x4 p=0.016) — seen pre-registration, new discovery not confirmation; #22 DONE 2026-11-18 GRID-NULL-WEAKLY-POWERED (LEDGER 22; PREREG a4eacf9): doublet hits 0/16 both conventions, phi-prime aligned-window crib hits 0/16 — pointer reading suspended (near-blind); option (b) RESOLVED via dukotah r18-L3: 3299 uniquely light-inked page-wide (anchor survives); decimals track CLOSED. **CORRECTION 2026-11-18 (external review; LEDGER C2): the grid has a CLOSED FORM — `|3301 − prime(F+1)|` over distinct Fibonacci F = 0…987, 16/16 vs our recorded 4×4, square spiral from red 3299 (verified; validate gate 6 + pytest). Containment p=3.3e-7/p=3.3e-8 RETRACTED (11 small-F cells ∈ 2838–3299 by construction — wrong null); pointer reading dead; 3299 ink anchor reinterpreted as spiral origin. Contributes fix to dukotah round44 (14/16 → 16/16, signed-vs-absolute on 1206/4516) — POSTED 2026-11-18, dukotah #14 cmt 6995323383. Round 2 (LEDGER C6): grid null re-measured with the reviewer's arithmetic, p ≈ 0.105–0.13 — **do NOT re-register the grid lane**; only optional live design is a BLIND image-channel prediction at the page holding stream position 3301** | Objects: 3278 / **3299**(red) / 3298 / 2838, all inside the pre-axis span 1874–3602; axis AXIS-ALIGNED (#19). Design constraints BEFORE PREREG: enumerate the reading space (0/1-based stream position, position-within-Q3, mod-section, digit-sum, red 3299 as anchor, ±21/±1 neighbor structure); statistic must be a POWERED structural one with planted-signal calibration (lesson #11: page-marginal stats blind to local plants; #15's powered-null template). Prior med (small digits retired by #15 but 4-digit stream-position readings untested; "their numbers are the direction" is signed). Dup-check vs dukotah hint-lenses (acrostic/selection fns) before spending | design pass first |
| **10** | **Campaign #21 (QUEUED, owner: same) = 6c constraint-based crib design, English-first (#17 gate).** Units: v2 sections as separate crib units — start pp8–14 / pp16–22 (axis-certified pair). Method per PRIORS: cribs = decode-SCORING vocabulary (core/cribs.py 36 words), NOT keytexts (additive dead); koan-register scorer (LLM > quadgrams per dukotah); p56 MANDATORY blind holdout; owner constraints: word lengths + punctuation (medial apostrophes, double quotes), krisyotam punctuation-lossy caveat. CONSTRAINT (owner 2026-11-17): the rune alphabet conflates U/V, C/K, S/Z (no K/Q/V/Z runes) — frequency analysis and crib scoring must run on the MERGED 23-letter alphabet (fold K→C, V→U, Z→S in any English-side comparator; cribs already written merged: DIUINITY). CENSUS DONE 2026-11-17 (text channel per owner steer "we have dots noted for every page"; scripts/audit/punct_text_census.py, work/punct_census/text_census.csv): krisyotam 181 dots = 19 block-plain + 165 ◆ tokens (◆4=129 after OWNER STIPULATION 2026-11-17: line-final ◆3 + next-line initial '-' TOGETHER render one ◆4 — both marks removed; the 2 occurrences p5/p11 both matched; stipulated not measured; ◆13=32, ◆10=3, ◆23=1) + residual: p37 L5 dot lost from block; p7/p10/p15/p38 one ◆ each with no file dot (p10 = #16 disclosed artifact). Dot positions: 127 medial / 18 final / 3 initial — dots are overwhelmingly SUB-WORD separators (krisyotam wrote no dash at dot boundaries): splitting on `-` AND `.`/quotes gives 3,371 words, mean len 3.91 (dash-only 4.08; LP1 koan ~4.0) = crib skeleton. SEPARATOR-CHANNEL VALIDATION (design pass, p57 — the only page where PT=CT): within-line dashes sit at true word boundaries 15/15 (LICE=LIKE via the C/K conflation, THE, INSTAR, TO, WE/MUST/SHED/OUR/OWN, FIND, DIUINITY/WITHIN/AND/EMERGE); ◆4 = sentence period 2/2 (SURFACE. CIRCUMFERENCES.); ◆23 = book-end 1/1; line wraps split words WITHOUT dashes (T|UNNELNG, C|IRCUMFERENCES, TH|E — 3 cases; dash ≠ line-wrap artifact). Channel verified on ground truth: dash=word, ◆4=sentence. p56 alignment (skip-aware, null-F mapping) = #21 gate. QUOTE MARKS (owner correction 2026-11-17: marks are BARE in the blocks, not ⟦⟧-wrapped — my first pass missed them): 17 marks = 14 `"` (8 medial/4 final/2 initial) + 3 `'` (all medial) on 16 lines across p6/7/21/22/35/40(×4)/41/42/43/53; several flank ◆4 (`◆4"` p6/p40/p42/p53, `"◆4` p22/p40/p42) — quote-diamond adjacency is a crib constraint. PUNCT dict (6 marks) is stale vs blocks (17) — treat blocks as authoritative. Raised-vs-mid image probe needed ONLY for the 19 plain residuals + quote shapes (oracle round #6 stays gated). **CAMPAIGN #21 DONE 2026-11-17 = SKELETON-QUALIFIED** (LEDGER row 21; PREREG 2f8c015): p56 dashes inside verified regions (difflib vs PGP canonical, merged alphabet) align to canonical word boundaries k=15/15, hypergeometric p=8.9e-13; p57 gate 16/16 + marks 3/3; merged quadgram+crib scorer ranks both true PTs above 0/1000 shuffles. Skeleton ADOPTED as crib constraint set (word lengths, sentence breaks, quote positions, merged alphabet); relikd `•` at letter 23 = its lone disagreement (WEB\|THERE, block side favoured — canonical says 23 not a word start). PAYOFF BUILT (a) 2026-11-17: core/skeleton.py — per-page slots/crib-placement pruning (single-word cribs may never straddle a dash; wrap positions merge; phrase cribs DEEPWEB/ANEND/HASHESTO exempt), V2 scorer, skeleton_penalty; 6 tests green. Payoff: median constrained/free = 0.305 (~69% of candidate crib placements pruned), mean 0.326, zero-cells 0.6% (work/skeleton_payoff/payoff.csv). Next: wire pruning into decode sweeps (brute_interrupters candidate space). | pushed 2026-11-18 |
| **11** | **Campaign #23 DONE 2026-11-18 (LEDGER row 23) = skeleton-constrained phi-prime sweep, all 55 unsolved pages. VERDICT PHI-FAMILY-NULL** (p=1.0; M=1 legal crib hit, null-max median 1). 499,604 decodes; 50/55 pages produced zero crib-shaped decodes; family retired for unsolved pages (coverage: phi-prime page-aligned, skip/hold, all null subsets, 36-crib vocab, skeleton-pruned). Power: needs >=3 legal cribs/page; single-crib blind (disclosed). | none |
| **12** | **Campaign #30 = F23 (T7 fixed-window certification)** — owner-approved 2026-11-19 ("Let's proceed with T7 certification"). The reopen path #26-A2 prescribed: single pre-named window (J±825, layout-derived edges), rate-ratio vs hard-core null, power curve first. Complementary to dukotah Round-45 (their T7 lane; a certified/refuted window is exactly what their certification needs — relay = owner decision each time). **DONE 2026-11-19: CERTIFIED-NONSTATIONARY (X=3 vs exp 10.95, p=0.0024, ratio 0.274; see F23 row + LEDGER 30). Upstream relay = owner decision. Follow-up lanes opened: F18(ii) cross-ledger review (Wulfic per-section-restart vs named window) is the cheap next step** | — |
| tail | **Campaign #24 DONE 2026-11-18 (LEDGER row 24; PREREG 1a48cec; all lanes on studio.local per owner steer). Lane A F3 = AFFINE-NULL (M=2 vs null-max median 2, p=1.0, ~5.0M decodes, plants 8/9; page-start coverage — arbitrary-offset affine open). Lane B F10 = NEGATIVE after REGISTERED ESCALATION (obs 131.0; 200-draw null max 136.1, p=0.0149; GO prongs all fail — mask=both n=49<floor, 0 cribs; mid-range cyclic steps 29..L−29 closed, self-pairs excluded). Lane C F14 = LP1-NULL + PREMISE CORRECTION (scream314 LP1 vs dukotah stream: 9.2% agreement; pp11/12 English plaintext — LP1 bulk is readable koan English, not ciphertext; completeness check M=1, p=1.0, plant raw 9 p=0.005). **Campaign #25 DONE 2026-11-18 (LEDGER row 25; PREREG 86f6755; both lanes studio.local). Lane D F3' = AFFINE2-NULL**: arbitrary-offset affine closed via crib-anchored slot inversion (16,666 anchors, 421,846 survivor cells, M=2 vs null-max hist {2:197,3:3} beaten 200/200 p=1.0, plants 3/3 exact-cell recovery; coverage: slot-aligned anchor shrink disclosed). Lane E = **LP1-PAGE-PLAINTEXT — 6/9 rune pages English-level** (Holm 0.0448, p-floor 0/200, margins disclosed): 01/06 atbash, 05/10/13/16 IDENTITY under standard futhark — WARNING preamble, primes/totient wisdom, the koan, DIUINITY index, YOUR MIND PROGRAMS REALITY, QUESTION ALL THINGS; 03/04/14 simple layers retired** | **OWNER: adjudicate Lane E flag (visual check of the 6 decodes — LANE_E_REPORT.md excerpts; 4 identity reads would be first LP2-side readings of LP1 rune pages)**; residual tails: mid-slot affine occurrences (anchor shrink), ~~03/04/14 LP1 pages (non-simple layers)~~ retired 2026-11-18 (solved, C3+C6), full-affine LP1 secondary (reported untested). **CORRECTION 2026-11-18 (LEDGER C3): 03/14 were never open — solved in the public wave (DIVINITY +7 / FIRFUMFERENFE +2); 03 already decoded by our own validate gate in CI. Lead retired. Round-2 correction (LEDGER C6): wave = 2014, not 2017; 04 SOLVED via reviewer recipe — DIVINITY key CONTINUOUS across the 03/04 break (phase 387 mod 8 = 3, 4 interrupters at in-page 27/49/71/120), verified in rig; LP1 rune pages now fully readable (01/03/04/05/06/09/10/13/14/16 + 11/12/15 folds). validate.py = full known-solutions regression suite (LP1 ×10 + p56/p57 + grid), content-pinned, mandatory pre-campaign. Week-one follow-up ~~explain 9.2% LP1 lineage agreement~~ **CLOSED 2026-11-19 = category error (LEDGER C8)**: stream B = solved English re-spelled into runes; only consumer was the #24 C-G1 gate comparison — LP1-NULL verdict unaffected** |
| deprioritized | F4 · F6 · F11 · F12 · F15 (community coverage) | — |

Dup-check debts (cheap read-only, fold into whichever slot is running):
their canon-as-key transform set = ±/shift/offsets only (verified in
`W2-C2-page-pairs/PREREG.md` §0 — affine a≠1 NOT covered → our T2/T13
niche confirmed); word-boundary sums vs their generator oracle — RESOLVED
2026-11-16 (R37-C1-U2 covers LP1 sums as keystream; LP2 self-sums were open,
closed by our #11); their keytext roster vs DIVINITY-on-LP2 (F6 — probably covered).

Watch: Dukotah #13/#14 replies (none as of 2026-11-16); their Round 45
(T7 lane) — slot 1 is deliberately first to stay complementary.
