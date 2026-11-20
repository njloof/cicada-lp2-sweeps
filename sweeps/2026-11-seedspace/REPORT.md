# Campaign #28 REPORT — Track C seed-space closure: ALL LANES CLOSED-NO-KEY

Registered before output: PREREG `f1ab025` (+ pre-sweep addendum `a0d421f`).
Engine cores transcribed from dukotah `grind27.c`/`grind28.c` (MIT, (c)
Dukotah); scorer, panel, bars, and cursors are NOT inherited — one own
instrument throughout. Studio.local, 28 cores, 2026-11-18 17:54 →
2026-11-19 16:39 (studio time). Seeds swept: **12,884,901,888** (3 × 2^32).

## Verdicts (registered rules, verbatim)

B = plant_min − 2.0 nats; CLOSED-NO-KEY requires no seed ≥ B AND 20/20
plants ≥ null_max + 2.0.

| lane | space (per seed: both signs; B/C also both reductions) | seeds scored (hist) | null_max (seed) | plant min/med | B | gate | **VERDICT** |
|---|---|---:|---|---|---|---|---|
| A Py2.7-MT `init_by_array`+`random29` | 2^32 × 2σ | 8.59e9 | −371.37 (2,801,660,027) | −268.75 / −241.01 | −270.75 | PASS (min margin 102.6) | **CLOSED-NO-KEY** |
| B PHP `init_genrand` MT19937 twist | 2^32 × 2σ × 2red | 1.718e10 | −368.32 (528,211,554) | −282.74 / −257.00 | −284.74 | PASS (min margin 85.6) | **CLOSED-NO-KEY** |
| C PHP legacy MT_RAND_PHP twist | 2^32 × 2σ × 2red | 1.718e10 | −373.09 (2,829,869,681) | −275.15 / −248.48 | −277.15 | PASS (min margin 97.9) | **CLOSED-NO-KEY** |

Zero seeds reached B in any cell → no adjudication triggered, no
flag-for-oracle. Descriptive Gumbel tail scale (top-25-nat window): 40.9 /
40.4 / 36.5 nats — null_max sits in the ordinary tail; the plant ladder
sits 86–103 nats above it, far over the 2.0-nat registered gate.

## What this closes (vs dukotah measured ceilings)

- **Py2.7 `random.seed(w)` → `random29`, keyskip1 relation**: their `exact`
  cursor stopped at 2,235,695,586 = 52.054% under a MIXED instrument
  (44.138 pp under the retired Round-19 panel, never re-scored). We re-swept
  **100% of 2^32** under one instrument with our plants and null.
- **PHP `mt_rand` uniform tier**: they covered 0.9705% per twist. We swept
  **100% of 2^32 × both twists × both reductions** (BADSCALING + mod29).
- **Relation-agnostic**: the skip-tolerant DP screen (≤12 extra consumptions
  in the 120-rune head, 3.0 nats/extra) covers BOTH keyskip1 and keyskip2
  emission models — required because #27 measured key consumption
  undecidable at emitted level.
- `pair`/keyskip2 was already excluded by dukotah at power 1.00; our result
  independently re-excludes it with our instrument.

We cite ONLY our own coverage: closure = what OUR instrument swept,
conditional on OUR plants (their doctrine, applied to us).

## Validation (pre-output gates)

V1 64/64 seeds vs pinned `vectors.json` ks128 (sha256 d4ff48ea…);
V2 32/32 streams (8 seeds × {mt,php} × {scale,mod} × 2000) vs pinned
`gen28.py` (sha256 04a98ba0…; their |delta|=0-vs-PHP-8.5.4 receipt cited —
no PHP binary on our hosts, L4); V3 `core.validate` full pass; V4 corpus
L=12,956, doublets=86. Both hosts, bit-identical.

## Disclosed execution history (engineering only; no statistic changed)

1. **Oversubscription reconfigure (pre-verdict, before 5% of any lane):**
   first launch ran 3 lanes concurrently (84 workers/28 cores); measured
   per-worker degradation ~7× for B/C (CPU-bound, no I/O overlap) → ~27 h
   projected vs ~9 h sequential. Killed all 84 and relaunched with the
   PREREG's registered execution plan (28 workers, sequential lanes).
   Checkpoints are atomic (state file every 2M seeds, tmp+fsync+rename);
   restarts RESUME FROM CURSOR — no coverage gap, only ≤2M/worker rescans.
2. **Supervisor failure + fix:** the lane-sequencing supervisor was
   ssh-tethered and died after lane A completed (2026-11-18 20:47), leaving
   B unlaunched ~10.5 h. Fixed by self-daemonizing (double-fork+setsid,
   `drive.py` commit 4f9aee4); B and C then completed unattended.
3. **verdict.py output-format bug** (numpy `savetxt` `%llu`→`%d`, ebdf015):
   display artifact only; merge/gate math unaffected (lane A verdict
   identical before/after).
4. Coverage accounting counts COMPLETED worker ranges only (a partial
   cursor never counts toward closure) — the doctrine from #26/#27.

## Conditionals on the closure (verbatim PREREG L1–L6)

- **L1** offset 0 only; pad from corpus position 0 (leading-discard and
  mid-book starts NOT covered).
- **L2** head screen = first 120 runes, ≤12 extra consumptions; a true key
  whose head is not English-quadgram-scoreable at that margin is missed
  (plants bound this for quadgram-English plaintext).
- **L3** plaintext proxy = quadgram English; corpus register = koan English.
- **L4** PHP cores validated vs pinned pure-Python `gen28.py` (their
  |delta|=0 receipt cited), no local PHP re-validation.
- **L5** other Py2.7 reducers (`grb5_mod`/`grb5_rej`/`shuffle29`), string
  seeds, amd64-2-word init, i386 NOT in space; glibc/Perl/TeX/Marsaglia
  flat tails stay open.
- **L6** unseeded (/dev/urandom-class) pads untestable by construction;
  hint-grammar generators = separate family (#29).

## Artifacts & reproduction

Tracked here: `results/verdict.json`, `results/hist_{A,B,C}.txt` (0.5-nat
bins), `results/top_{A,B,C}.tsv` (top-1024 per lane: score, seed, sign,
red). Full worker state files (hist+top per worker, ~55 MB total) stay in
`studio:~/cicada-c7/sweeps/2026-11-seedspace/results/w_*/` (gitignored per
repo rule).

    python3 -m core.validate
    python3 sweeps/2026-11-seedspace/drive.py --selftest     # V1/V2/V4
    python3 sweeps/2026-11-seedspace/plants.py               # plant ladders
    scripts/studio.sh run sweeps/2026-11-seedspace/drive.py --runall 28   # resume-safe full sweep
    scripts/studio.sh run sweeps/2026-11-seedspace/verdict.py             # merge + verdict
