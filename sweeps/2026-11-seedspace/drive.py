#!/usr/bin/env python3
"""Campaign #28 driver — validation gates V1/V2, corpus export, bench, launch.

Run from repo root or campaign dir. On studio the same file compiles the
engine in-tree and launches lane workers (seed-range partition).

    python3 drive.py --selftest            # V1 + V2 + V4 (engine health; no corpus statistic)
    python3 drive.py --corpus              # write corpus.bin (pinned unsolved stream)
    python3 drive.py --bench N             # per-lane throughput (synthetic timing)
    python3 drive.py --launch lane NWORK   # partition [0,2^32) and run workers (studio)
    python3 drive.py --kill                # kill engine workers (pre-resume; avoids double-scan)
    python3 drive.py --runall              # supervisor: lanes A,B,C sequentially, 28 workers each (studio)
"""
import json, os, subprocess, sys, time, zlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
ENG = os.path.join(HERE, "seedspace_engine")
QUAD = os.path.join(ROOT, "sources/dukotah/liber-primus/data/english_quadgrams.txt")
VECT = os.path.join(ROOT, "sources/dukotah/liber-primus/analysis/round27/P0-spec/vectors.json")
GEN28_DIR = os.path.join(ROOT, "sources/dukotah/liber-primus/analysis/round28/L4")
CORPUS = os.path.join(HERE, "corpus.bin")
SEED = 20261228
SPACE = 2**32

def sh(*a, **kw):
    return subprocess.run(a, capture_output=True, text=True, **kw)

def build():
    if os.path.exists(ENG):
        os.remove(ENG)
    r = sh("cc", "-O3", "-std=gnu11", "-o", ENG, os.path.join(HERE, "engine.c"), "-lm")
    if r.returncode:
        print(r.stderr); sys.exit(1)
    print("build: OK")

def selftest():
    ok = True
    # sha pins (metadata.json)
    meta = json.load(open(os.path.join(HERE, "metadata.json")))
    import hashlib
    for key, path in (("vectors_sha256", VECT),
                      ("gen28_sha256", os.path.join(GEN28_DIR, "gen28.py"))):
        want = meta["validation_files"][key]
        got = hashlib.sha256(open(path, "rb").read()).hexdigest()
        print(f"sha {key}: {'PASS' if got == want else 'FAIL'}")
        ok &= got == want

    # V1: engine Py2.7 core == pinned vectors.json ks128, 64/64
    vecs = json.load(open(VECT))["seed_vectors"]
    bad = 0
    for v in vecs:
        out = sh(ENG, "--ks", "A", str(v["seed"]), "128")
        ks = [int(x) for x in out.stdout.split()]
        if ks != v["ks128"]:
            bad += 1
            print(f"  V1 mismatch seed {v['seed']}")
    print(f"V1 vectors.json 64/64: {'PASS' if bad == 0 else f'FAIL ({bad})'}")
    ok &= bad == 0

    # V2: engine PHP cores == gen28.py reference (8 seeds x 2000 x 4 combos)
    sys.path.insert(0, GEN28_DIR)
    import gen28
    seeds = json.load(open(os.path.join(GEN28_DIR, "receipts/genval.json")))["seeds"]
    bad = 0
    for s in seeds:
        for mode in ("mt", "php"):
            for scaling in ("scale", "mod"):
                ref = gen28.php_stream(s, mode, scaling, 2000)
                lane = "B" if mode == "mt" else "C"
                out = sh(ENG, "--ks", lane, str(s), "2000", scaling)
                got = [int(x) for x in out.stdout.split()]
                if got != ref:
                    bad += 1
                    print(f"  V2 mismatch seed {s} {mode}/{scaling}")
    n = len(seeds) * 4
    print(f"V2 gen28 reference {n}/{n}: {'PASS' if bad == 0 else f'FAIL ({bad})'}")
    ok &= bad == 0

    # V4: corpus pins (L, doublets) via core.validate
    from core import validate as V
    PAGES = list(range(50)) + list(range(51, 56))
    s = np.array([x for p in PAGES for x in V.flat(p)], dtype=np.int64)
    dbl = int((np.diff(s) == 0).sum())
    v4 = len(s) == 12_956 and dbl == 86
    print(f"V4 corpus L={len(s)} doublets={dbl}: {'PASS' if v4 else 'FAIL'}")
    ok &= v4
    print("SELFTEST:", "PASS" if ok else "FAIL")
    return ok

def corpus():
    from core import validate as V
    PAGES = list(range(50)) + list(range(51, 56))
    s = bytes(x for p in PAGES for x in V.flat(p))
    assert len(s) == 12_956
    open(CORPUS, "wb").write(s)
    print(f"corpus.bin: {len(s)} bytes")

def bench(n):
    for lane in "ABC":
        r = sh(ENG, "--bench", lane, str(n), QUAD, CORPUS)
        print(r.stdout.strip() or r.stderr)

def launch(lane, nwork):
    # partition [0, 2^32) into nwork contiguous ranges; one worker each;
    # workers checkpoint atomically; relaunching this command resumes.
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    chunk = SPACE // nwork
    procs = []
    for i in range(nwork):
        lo, hi = i * chunk, (i + 1) * chunk if i < nwork - 1 else SPACE
        wdir = os.path.join(HERE, "results", f"w_{lane}_{i}")
        os.makedirs(wdir, exist_ok=True)   # per-worker state file (no shared writes)
        log = open(os.path.join(HERE, "results", f"worker_{lane}_{i}.log"), "a")
        procs.append(subprocess.Popen(
            [ENG, "--sweep", lane, str(lo), str(hi), QUAD, CORPUS, wdir],
            stdout=log, stderr=log))
    print(f"launched {nwork} workers lane {lane}; pids {[p.pid for p in procs]}")
    return procs

def ps():
    # read-only: engine workers + runall supervisor
    r = sh("ps", "-axo", "pid=,etime=,command=")
    for line in r.stdout.splitlines():
        if "seedspace_engine" in line or "runall" in line:
            print(line.strip())

def kill():
    # Kill engine workers. MUST precede any relaunch: two workers on the same
    # seed range would double-count hist/top at merge time. Checkpoints are
    # atomic (state file every 2M seeds), so at most one chunk is re-scanned.
    ps = sh("ps", "-axo", "pid=,comm=").stdout.splitlines()
    n = 0
    for line in ps:
        parts = line.split()
        if len(parts) == 2 and parts[1].endswith("seedspace_engine"):
            try:
                os.kill(int(parts[0]), 15)
                n += 1
            except ProcessLookupError:
                pass
    print(f"killed {n} engine workers")

def runall(nwork=28):
    # PREREG execution section: 28 worker processes, lanes run SEQUENTIALLY
    # (measured 2026-11-18: 3 concurrent lanes = 84 workers on 28 cores
    # degrades per-worker rate ~7x for B/C; CPU-bound, no I/O to overlap).
    # Resume semantics: workers read their atomic state file and continue.
    for lane in "ABC":
        procs = launch(lane, nwork)
        print(f"lane {lane}: {nwork} workers running", flush=True)
        for p in procs:
            p.wait()
        print(f"lane {lane}: DONE", flush=True)

def status(nwork=28):
    for lane in "ABC":
        tot = 0
        for i in range(nwork):
            p = os.path.join(HERE, "results", f"w_{lane}_{i}", f"state_{lane}.txt")
            if os.path.exists(p):
                with open(p) as f:
                    for line in f:
                        if line.startswith("CURSOR "):
                            tot += int(line.split()[1]) - i * (SPACE // nwork)
                            break
        print(f"lane {lane}: {tot}/{SPACE} seeds ({100.0*tot/SPACE:.2f}%)")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(0)
    if a[0] == "--selftest":
        if not os.path.exists(ENG): build()
        sys.exit(0 if selftest() else 1)
    if a[0] == "--corpus":
        corpus(); sys.exit(0)
    if a[0] == "--bench":
        bench(int(a[1])); sys.exit(0)
    if a[0] == "--launch":
        launch(a[1], int(a[2])); sys.exit(0)
    if a[0] == "--ps":
        ps(); sys.exit(0)
    if a[0] == "--kill":
        kill(); sys.exit(0)
    if a[0] == "--runall":
        if not os.path.exists(ENG): build()
        runall(int(a[1]) if len(a) > 1 else 28); sys.exit(0)
    if a[0] == "--status":
        status(int(a[1]) if len(a) > 1 else 28); sys.exit(0)
    print("unknown arg"); sys.exit(2)
