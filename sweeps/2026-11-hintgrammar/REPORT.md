# Campaign #29 REPORT — Track C hint-grammar generators: ALL CELLS CLOSED-NO-GRAMMAR

Registered before output: PREREG `b8c779a` + addenda `fbdde20`, `8b32cc1`,
`f63d29e` (all pre-statistic). Owner approval 2026-11-19. Studio.local,
28 cores; gates G1–G3 + plants local, scan + nulls studio. Seed 20261229.

## What was swept

592,574 deterministic decodes of the 12,956-rune unsolved corpus head under
the registered skip-tolerant screen (#28 relaxation: 120-rune window, 13
ctx-carrying extra-states, advance 1..3, 3.0 nats/extra):

| cell | family | candidates | argmax (noise) | obs_max |
|---|---|---:|---|---:|
| K1 | plaintext-autokey, seeds = hint substrings, w∈[2..24], keyskip0 (L9) | 427,202 | armfwd off 2613 w24 +1 | −400.01 |
| K2 | ciphertext-autokey, w∈[2..64], keyskip1+causality leak | 252 | w50 −1 fskip-on | −418.17 |
| K3 | running keys: armfwd/armrev/scream × t0 × signs × A0/A1 × dir × Fskip | 137,120 | scream t0 1428 −1 | −403.21 |
| K4 | math streams: primes, fib, φ(prime), 1033/3301, π, e, √2 × off × signs × Fskip | 28,000 | e off 176 +1 | −405.04 |

## Verdicts (registered rules: B = plant_min − 2.0; CLOSED iff no candidate
## ≥ B AND 20/20 plants ≥ null_max + 2.0)

| cell | plant min/med | null_max (D) | B | obs_max | min margin | VERDICT |
|---|---|---|---|---:|---:|---|
| K1 (all 23 lags, 20/20 each) | −246.8…−275.7 / ≈−232 | −387.04 (20) | −248.8…−277.7 | −400.01 (per-w obs −434.5…−400.0) | 111.3 (w15) | **CLOSED-NO-GRAMMAR** |
| K2 | −298.5 / −261.7 | −408.16 (200) | −300.5 | −418.17 | 109.6 | **CLOSED-NO-GRAMMAR** |
| K3 | −289.3 / −248.3 | −387.08 (200) | −291.3 | −403.21 | 97.8 | **CLOSED-NO-GRAMMAR** |
| K4 | −303.0 / −243.6 | −391.11 (200) | −305.0 | −405.04 | 88.1 | **CLOSED-NO-GRAMMAR** |

Zero candidates reached B in any cell or lag → no adjudication triggered, no
flag-for-oracle (`adjudication.json` empty). K1 escalation rule (addendum 2)
not triggered: obs −400.01 < null median −394.45. Nulls: K1/K2/K4 = corpus
page-permutation surrogates; K3 = hint-value permutation surrogates; seed
20261229, draw-level resume.

## What this closes (Track C, with #28)

- **#28** closed the RANDOM-seed generators (12.88e9 seeds, Py2.7-MT + PHP
  MT, both twists/reductions). **#29** closes the structured FLAT aperiodic
  remainder: plaintext-autokey (unfiltered emission, L9), ciphertext-autokey
  (filtered, leak policy, L10 — Wulfic's "autokey to 12,863" claim class),
  running keys from every book-internal pinned text (armada18 LP1 English
  fwd/rev, scream314 LP1 stream, solved plaintexts), and derivable math
  streams (primes, Fibonacci, φ(prime), 1033/3301, π, e, √2).
- Periodic Vigenère L1–40 was already excluded (MAP §eliminated: IoC +
  doublet deficit).
- NOT covered (open by disclosure): external literary keytexts (PRIORS §1 —
  chain-stage doctrine; if the group broke their own habit for LP2, this
  campaign cannot see it, L4); key-transposition/atbash-feed chains (L6);
  filtered plaintext-autokey (structurally undecodable, L9); unseeded pads
  (#28 L6, untestable by construction).

## Validation (pre-output)

- **G1** `core.validate` full pass.
- **G2** φ(prime) reproduces the p56 known decode blind (hold-interrupter,
  3/3 cribs) — the registered grammar provably contains a known solution.
- **G3** letter-map round-trip with collapses V→U, K→C, Q→C, Z→S.
- Engine round-trip: K1 exact decode of keyskip0 plants (bit-exact letters);
  K2 plant round-trips for both signs × both F-skip variants.

## Disclosed limitations (PREREG L1–L11 + this report)

- **L9 (structural, addendum 3)** plaintext-autokey under keyskip1 is NOT
  causally decodable — the key runs ahead of the emission once cumulative
  rejects ≥ w. K1 is closed only against UNFILTERED (keyskip0) autokey
  emission. K2 covers the filtered ciphertext-autokey class with the
  registered leak policy; other filter policies uncovered (L10).
- **L11** streams shorter than 132 values contribute no full head:
  anend (85), parable (95), p56hex (128) — covered only as K1 seed
  substrings (anend/parable) or not at all (p56hex as a KEY stream; its
  G2-role φ(prime) stream is full-length).
- K1 per-w null uses the global K1 null_max (conservative).
- Head screen = first 120 runes (window from lag w); tails unkeyed-untested
  for K3 (L2); offsets/lags bounded as registered (L3); external literary
  hints excluded (L4, PRIORS §1) — Emerson appears ONLY in plants.
- Grid 5.9e5 > PREREG's ≈2.6e5 estimate (fskip × A × dir cross-product);
  coverage reported here is the actual grid.

## Artifacts & reproduction

    python3 -m core.validate                                # G1
    python3 sweeps/2026-11-hintgrammar/scan.py --gates      # G1-G3
    python3 sweeps/2026-11-hintgrammar/scan.py --plants     # synthetic ladder
    cc -O2 -o sweeps/2026-11-hintgrammar/engine29 sweeps/2026-11-hintgrammar/engine29.c
    scripts/studio.sh run sweeps/2026-11-hintgrammar/scan.py --scan
    scripts/studio.sh run sweeps/2026-11-hintgrammar/scan.py --nulls
    python3 sweeps/2026-11-hintgrammar/scan.py --verdict

Tracked: results/{plants,scan,nulls,verdict}.json (small). Worker scratch
(hint blobs, surrogate corpora) in work/ (gitignored).
