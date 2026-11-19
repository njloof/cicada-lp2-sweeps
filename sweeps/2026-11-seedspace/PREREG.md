# Campaign #28 PREREG — Track C: close the two big finite seed spaces under one own instrument

Registered and committed BEFORE any corpus statistic is touched (CI gate).
Owner approval 2026-11-19 ("let's write the prereg for track C"). MAP F20,
unblocked 2026-11-19 by the #26 REPORT (stopping rule). Seed 20261228.
Design rule inherited from #26 and paid off in #27: **the power plant is
registered FIRST and the primary statistic's detectability of its own target
is a gate on any negative verdict.**

## Why these spaces (dukotah MEASURED-CEILING, verified in the pinned checkout)

| space | their state (rows cited) | our action |
|---|---|---|
| Py2.7 `random.seed(w)` MT19937, `random29` reducer, full uint32 | `pair`/keyskip2 relation: full 2^32 EXCLUDED at power 1.00 (English plant) [[R27-CPORT-MT32-FULLSWEEP]]. `exact`/keyskip1: cursor 2,235,695,586 = **52.054 %** of 2^32, MIXED instrument (44.138 pp under the retired Round 19 panel, never re-scored; 7.916 pp under panel-R36, best 7.3071 vs claim bar 7.6342) [[R38-S1-S2-WINDOWS]] [[R42-S1-S2-WINDOW2-RECOVERED]] | re-sweep **full 2^32** under ONE instrument with our plant and our null |
| PHP `mt_rand`, uniform tier | **0.9705 %** of 2^32 per twist (41,680,896 seeds, best 6.856 vs bar 6.991) [[R32-B2-PHP-MT-RAND]]; prior-dense tier (48,036 seeds) excluded at power 0.95–0.99, nine registers [[R36-B2-PHP-AWAKE-PFV4]]; ~99.39 % open | sweep **full 2^32** per twist, both reductions |

We do NOT inherit their cursor: a mixed-instrument coverage sum is exactly
what their own doctrine refuses to cite as closure. Our closure claims cover
what OUR instrument swept, conditional on OUR plants.

## Space (exact, three cells)

Keystream → symbol: seed w ∈ [0, 2^32), one stream per w, offset 0 (no
leading draws discarded), pad applied from corpus position 0. Emission model:
`c_t = (p_t + σ·k_t) mod 29`, **both signs σ = ±1**, with the anti-doublet
rejection loop (a candidate emission equal to the previous emitted rune is
rejected and consumes extra key values — keyskip1 consumes 1 per reject,
keyskip2 consumes 2).

- **Cell A — Py2.7-MT**: `random.seed(w)` → MT19937 `init_by_array([w])`,
  reducer `random29` = `int(random()*29)` (two uint32 draws per symbol,
  53-bit quotient). 2^32 seeds × 2 signs.
- **Cell B — PHP canonical twist**: `mt_srand(w)` → `init_genrand(w)`,
  MT_RAND_MT19937 twist, output `temper(u32) >> 1` (31-bit), BOTH reductions:
  `RAND_RANGE_BADSCALING` `(int)(29.0·r/2^31)` and `r % 29`. 2^32 seeds ×
  2 signs × 2 reductions (draws shared).
- **Cell C — PHP legacy twist**: as B with the pre-7.1 MT_RAND_PHP broken
  twist (mask from loBit(u)).

**Relation-agnostic by construction.** The screen is skip-tolerant (below),
so a negative covers BOTH keyskip1 and keyskip2 emission models — which is
required, because #27 measured key consumption to be UNINFORMATIVE at emitted
level and skip-tolerant is our conservative default.

## Instrument (ours; generator core transcribed, validated, attributed)

`sweeps/2026-11-seedspace/engine.c` — new C engine. The generator/reducer
functions are transcribed from dukotah's `grind27.c` / `grind28.c`
(MIT license, (c) Dukotah; those cores are |delta|=0-validated against real
binaries by their authors). We do NOT reuse their scorer, panel, or bars.

**Screen (primary statistic).** Skip-tolerant quadgram log-likelihood of the
decoded 120-rune head of the pinned unsolved stream:
- rune → letter string via `core.validate.TRANS` (TH/EO/NG/OE/AE/IA/EA
  expand to two letters);
- score = Σ log P(ch | previous 3 letters) from `english_quadgrams.txt`
  (file order, weights normalized per 3-letter context; unseen context →
  unigram backoff; initial context THE, as in #26-A1);
- Viterbi over key consumption: per rune the key advances 1, 2 or 3
  (≤ 12 extra consumptions in the head — expected ≈ 3.5 under the corpus
  leak model q=1/29, s=0.813; Poisson(3.5) tail beyond 12 < 3e-4), each
  extra advance penalized 3.0 nats; score = max path.

**Adjudication (secondary, per candidate).** Top K = 1024 seeds per cell by
screen score → full-length (12,956-rune) skip-tolerant decode (total extra
consumptions ≤ 1200, expected ≈ 374) → house crib list (36-word union,
`core/cribs.py`); **≥ 2 legal crib hits → FLAG-FOR-ORACLE, never
auto-certified**. Per-word hits reported for human review.

## Gates (before any corpus statistic)

- **V1** engine Py2.7 core reproduces `vectors.json` `ks128` for **64/64**
  pinned seeds (file sha256 pinned in metadata.json).
- **V2** engine PHP cores reproduce `gen28.py` reference streams for its 8
  pinned seeds × 2000 draws × 4 twist×reduction combos, |delta| = 0
  (gen28.py sha256 pinned; their `genval.json` receipt — |delta|=0 vs real
  PHP 8.5.4 — cited; no PHP binary exists on this host or studio —
  disclosed limitation L4).
- **V3** `python3 -m core.validate` full pass.
- **V4** corpus pins: L = 12,956; doublets = 86.

## Power plants (FIRST output after this commit; synthetic only, no corpus touch)

20 plants per cell: house seeding `default_rng([20261228, crc32("plant"), d])`;
plaintext = #26-A1 quadgram-sampler stream (bit-identical loader/sampler);
plant corpus `S* = encode(P, K(w*))` through the REAL rejection-loop encoder
(keyskip1 semantics; screen is tolerant so this is the harder case); plant
seed w* uniform in [0, 2^32). Score w* with the same screen on S*.

**Registered margin gate: margin_gate = 2.0 nats.** Define, after the sweep,
`G = min(plants) − null_max`, where `null_max` = best screen score of the
real-corpus sweep over its own cell. Closure requires G ≥ 2.0 AND all 20
plants individually ≥ null_max + 2.0 (20/20, no exceptions — bar per #26
rule; report the plant ladder either way).

## Verdicts (verbatim, per cell)

- **FLAGGED** — any real-corpus seed ≥ B, where B = min(plants) − 2.0 nats:
  run adjudication; ≥ 2 legal cribs → flag-for-oracle and report to owner
  BEFORE any public statement.
- **CLOSED-NO-KEY** — no seed ≥ B and the power gate (20/20 above
  null_max + 2.0) passes: the cell's space is closed under our instrument,
  conditionals L1–L6 below.
- **UNPOWERED-NULL** — no seed ≥ B but the power gate fails: the sweep is
  recorded, the space stays OPEN; never reported as closure.

## Coverage × power reporting (doctrine: both or neither)

Coverage: 2^32/2^32 per cell (100 % of the registered space, both signs,
both PHP reductions; keyskip1 AND keyskip2 emission models via the tolerant
screen). Power: the plant ladder (20 scores per cell) vs the empirical
null_max, reported in the REPORT with the Gumbel fit of the score histogram
(descriptive). Log-binned score histograms + top-1024 candidates persisted
at sweep time (language-agnostic statistics, per doctrine R3).

## Execution (studio.local per standing owner steer)

Build on studio via the campaign driver (cc -O3; no OpenMP — seed-range
partitioning across 28 worker processes, checkpointed STATUS.json, resumable
budget chunks). `sweeps/` is already in studio.sh SYNC_PATHS; the driver
compiles in-tree and launches workers; results pulled via
`scripts/studio.sh pull`. **Calibration bench (200k seeds/cell) runs first;
the measured ETA is reported to the owner before the full launch.** Anchor:
dukotah's heavier grind27 pipeline measured 130.4k seeds/s aggregate on
6 cores (9.15 h per 2^32 lane); ours is lighter, so ~1–2 h per cell on
28 cores is expected — NOT days.

## Disclosed limitations

- **L1** offset 0 only (leading key-discard unmeasured); pad starts at
  corpus position 0 (mid-book key starts unmeasured).
- **L2** head screen sees only the first 120 runes and ≤ 12 extra key
  consumptions there; a true key whose head is not English-quadgram-scoreable
  at that margin is missed (plants bound this at English-quadgram plaintext).
- **L3** plaintext proxy is quadgram English; the corpus register is koan
  English (LP1-solved). Misspecification dilutes power; the plant ladder
  measures power only for the proxy.
- **L4** PHP cores validated against the pinned pure-Python reference
  `gen28.py` (whose own |delta|=0 receipt vs PHP 8.5.4 is cited); no PHP
  binary re-validation on our hosts. Py2.7 core validated directly
  (64/64 vectors).
- **L5** other Py2.7 reducers (`grb5_mod`/`grb5_rej`/`shuffle29`), string
  seeds, amd64 2-word init, i386: NOT in this space (dukotah rows: < 0.1 %
  covered, partial). Other generators' flat tails (glibc/Perl/TeX/Marsaglia)
  stay open.
- **L6** /dev/urandom-class (unseeded) pads are untestable by construction;
  hint-grammar generators (F20's third component) are a separate family and
  get their own PREREG (#29), not this scan.

## Reproduction (after completion)

    python3 -m core.validate
    python3 sweeps/2026-11-seedspace/drive.py --selftest      # V1/V2 gates
    python3 sweeps/2026-11-seedspace/plants.py                # plant ladders
    scripts/studio.sh run sweeps/2026-11-seedspace/drive.py --lane A --budget 480   # etc.
    # artifacts: results/seedspace_*.json, histograms, REPORT.md
