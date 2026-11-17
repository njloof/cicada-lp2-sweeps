# PRIORS — Cicada 3301 group-history priors for LP2 (curated 2026-11-17)

Owner directive 2026-11-17: incorporate research on the group and their
previous-puzzle approaches as hints. Confidence tiers: **[OURS]** verified
in this repo; **[DUKOTAH]** their claims (pinned clone, unverified);
**[COMMUNITY]** mirrored archives restating public sources; **[H]**
external check verified against primary artifact bytes (2026-11-17 web
agent, byte-for-byte vs krisyotam/scream314/iBotPeaches + Boxentriq/
Register); **[RUMOR]** circulating but zero archive support — listed in §6
so we never build on them.

## 1. How LP1 (book 1, pp00–16) was actually solved — the house method

Per-page key table [DUKOTAH+COMMUNITY, mirrored; CI reproduces all four
known decodes]: p00/p02/p05/p10–13/p16 direct Gematria transliteration;
p01 **Atbash over reversed Gematria** ("A WARNING"); pp03–04 **Vigenère
mod 29, key DIVINITY** (canonical spelling DIUINITY) with the **ᚠ F-skip
rule**; pp06–09 Atbash + Caesar −3 (koan); pp14–15 Vigenère key
FIRFUMFERENFE = CIRCUMFERENCE typed through the rune alphabet; LP2 p56
**φ(prime) totient keystream mod 29**; p57 transliteration.

The crucial enabler every keyed case: **the key was a recoverable crib
from the puzzle's own vocabulary** (DIVINITY, CIRCUMFERENCE — words the
book itself tells you to "shed"/"find") or a derivable math rule (φ,
primes). Key resets observed at indices 59/95/108 [COMMUNITY].

**F-skip rule** [DUKOTAH]: only ᚠ is ever a null; null ᚠ removed WITHOUT
advancing the keystream; per-page subset (~90% recoverable). Calibrate
keys on interrupter-free blocks. Owner's p56 note "every clear-text F is
an ᚠ to be skipped" refers to this.

External verification adds two load-bearing facts [H]:
- LP1 plaintexts are **original koan prose, not quotations** (BELIEVE
  NOTHING / QUESTION ALL THINGS / DO FOUR UNREASONABLE THINGS EACH DAY).
  The literary canon (Mabinogion, Blake, Agrippa, Emerson, Liber AL,
  GEB) lives in the CHAIN stages as book-cipher keys — never as LP
  plaintext cribs. ⇒ external literary crib-dragging has **no LP1
  precedent**; LP1 keys came from the book's own vocabulary.
- **p56 "AN END" is the ONLY in-block ground truth and was solved by a
  derivable math rule** (totient keystream), not a word key. Any claimed
  LP2 method must recover p56 blind; word-key methods are ungeneralized.
  Its target: a 128-hex SHA-512 hash page, unfound 2014→2026; dukotah
  OSINT verdict: gated behind solving LP2 itself — do not spend on
  hash-hunting. (Note: onion7 also dropped `sexagesimal.bin`, 256 B —
  [OURS] verified NOT equal to canon_256, sha512 ≠ AN-END target; role
  undocumented, not a pad lead.)

## 2. Group habits (stylometry of the ciphertext-maker)

- ALL-CAPS, archaic koan-like stylized English; mean word length LP1 ~4.0,
  LP2 4.425 (register, not error).
- **V-for-U demystified [H]**: the rune alphabet has no V/K/Q/Z (U/V,
  C/K, S/Z conflated by construction) — EUERY/DIUINITY are transliteration
  ARTIFACTS, not archaizing style. Genuine tells: all-caps koan register,
  aphoristic imperatives; signed messages modern/terse ("Good luck. 3301").
  LP1 A WARNING W-drops (AWARNNG, CNOW, BOOC) are page-specific quirks,
  not global (DEEPWEB spells fine on p56/57).
- **Stylometry is below its floor [H/M]**: authentic connected prose ≈359
  words; dukotah's Round-9 Burrows'-Delta exclusion ruled INVALID (62%
  impostor false-inclusion). "3301 voice" scoring = weak evidence; score
  candidate decodes against the koan register but weight low.
- **Prime obsession**: 509×503 image dims; 509·503·3301 = PGP comment
  number; "THE PRIMES ARE SACRED / THE TOTIENT FUNCTION IS SACRED"
  (p05); [OURS] A WARNING plaintext line sums 9/9 prime (P≈1e-8); magic
  constant 1033 = emirp reverse of 3301.
- **Symmetry as house style**: page-level 180° palindromes (line sums
  341,1015,562,1015,341) [OURS]; owner's p7↔p23 flipped-5-dot bracket and
  p40↔p48 margin bracket FIT this habit — supports the 11-group
  segmentation reading (docs/MAP.md 6d).
- **PGP 7A35090F** is the sole authenticity gate; every genuine artifact
  signed; last signed Apr 2017.
- Anti-collaboration ethos ("We want the best, not the followers");
  per-solver personalized stages — some channels may be intentionally
  unresolvable in public.
- Signed 2016 clause set — "their numbers are the direction" — the only
  signed methodological hint ever given: numbers (red digits, lattices,
  tokens) as selectors/directions, not values.

## 3. Symbol lexicon (what motifs have meant before)

- **Cicada/instar/emergence**: core theme ("shed our own circumferences;
  find the divinity within and emerge" — hidden poem in 761.mp3, gematria
  761 = title sum). Cicada illustrations LP2 p2, p53, p55 [DUKOTAH].
- **Mayfly/ephemera** [DUKOTAH thematic read, unverified]: margin motifs
  pp24–26/57/14 read as "ephemeral = one-time" pointer — would nod at the
  OTP-class verdict. Our p2 walking-mayfly at the `$` position gains a
  candidate meaning here.
- **Lemniscus/infinity** [DUKOTAH class 18]: p0/p1/p2/p15 — matches owner
  notes (p1/p2 top+bottom, p15 under digits) exactly; dukotah also has it
  on **p0** — worth an owner look.
- **Post horn / Tristero / Pynchon**: ABSENT from all archives here —
  external check confirms zero hits in krisyotam/scream314/iBotPeaches/
  dukotah: **RUMOR**, do NOT treat as group motifs.
- **Mayfly external [H]**: the original 4 May 2014 /x/ symbol sheet
  already identified mayflies among LP2 ornaments; jbo-tools sections
  **pp23–26 as the "mayfly" ornament group** — matches your p24–25 pair
  and dukotah's pp24–26. Meaning documented only thematically
  (instar/emergence/shedding); no deeper code.
- **Lemniscus external**: on the 2014 symbol sheet ("Infinity symbol up
  top") but **no documented meaning in any 2012–17 artifact** — stays
  oracle-gated (round #6 S9), lore-free.
- Crowley Liber AL / Blake / Mabinogion / Agrippa / Self-Reliance: real
  2012–13 book-cipher canon [COMMUNITY, mechanics partly flagged], BUT
  all tested as LP2 keytexts and killed (§4).

## 4. Anti-priors — what is ALREADY DEAD (do not re-sweep)

- **Doublet deficit 0.66% vs 3.45% random (~86/12,956)** [DUKOTAH+OURS,
  reproduced]: mechanically EXCLUDES every additive keystream (prime,
  totient, Fibonacci, running-key, short Vigenère — all yield 2.9–3.4%).
  ⇒ A crib cannot be applied additively to LP2; "find the right keytext"
  is not the game.
- Autokey positively refuted at mechanism level (flat difference-diagonal
  cv=0.061 vs autokey-required ~1.0) [DUKOTAH].
- ~200 thematic keytexts (Cicada prose, Mabinogion, Blake, Book of the
  Law…) run rigid AND skip-aware: all null. Word-length skeleton vs 224
  texts: closed. Transposition, polygraphic, homophonic, seeded-PRNG
  (2.5e9 seeds), public pads (14.5e9 offsets): closed.
- ⇒ **The remaining lanes** (both teams' state): index/selection channels
  (red marks, digits, lattices, tokens), the separator/ornament channel,
  **non-stationarity** (T7: lag-1 gap autocorr p=0.0010 [DUKOTAH];
  replicated ours p=0.0006, signal localized, VOID at positions
  2739–4388), external/signed evidence, and the owner's decoration-
  segmentation lane.

## 5. Concrete implications for 6c + segmentation

1. **Crib vocabulary = the house list** `core/cribs.py` (36 words from
   solved-page vocabulary: DEEPWEB, WITHIN, PILGRIM, DIUINITY,
   CIRCUMFERENCE, SHED, EMERGE…) — for SCORING candidate decodes, not as
   keytexts. LLM scorer beats quadgrams on 3301's stylized English
   [DUKOTAH] — score candidate plaintexts with a koan-register scorer.
2. **T7 × segmentation test** (campaign #18 core): our replicated
   doublet-gap non-stationarity is LOCALIZED with a void at corpus
   positions 2739–4388. If the 11 decoration-groups are real streams,
   anomaly boundaries should sit at group edges. Deterministic, cheap,
   falsifiable.
3. Register tension to carry: koan all-caps style rarely uses medial
   apostrophes — #17's contraction reading stands (evidence is the
   marks themselves) but expect the plaintext register to be unusual;
   keep the multi-language fallback registered.
4. "Their numbers are the direction" (signed) ⇒ digits/lattice counts/
   token tables as selectors — consistent with #15 retiring digits 1–5 as
   *values* while keeping them as labels.
5. Key resets at fixed indices (59/95/108) [COMMUNITY] ⇒ per-group keys
   are the house pattern: the owner's segmentation is literally how LP1
   was keyed (per-page/per-section key changes). ⚿ NOT confirmed by the
   external check (traced only to connortumbleson-lineage notes) — treat
   as suggestive, not verified.

## 6. Rumor register — zero archive support, never build on these [RUMOR]

Pynchon/Tristero/post-horn/"the lot" · Hamlet "time is out of joint" ·
"what is the square root of the lot?" (LP2 release phrase — misremembered;
the real handoff is the signed "We look forward to hearing from you") ·
TFNT spectrogram/site (tfnt.com verified parked 2026-11-17) · solfeggio
frequencies · Playfair · steghide (OutGuess is the documented tool) ·
magic square summing to 3301 · KJV as 2012 book code (mainstream record
says Mabinogion) · Seattle "phone booth" (Seattle was a 2012 POSTER site)
· any post-2017 unsigned "Cicada" material (their 2017 warning: presume
fake). Also: krisyotam's DECODED-PAGES.md claim that p56/57 lack verified
plaintext is WRONG — `56.decoded`/`57.decoded` exist in stage11 [H].
