#!/usr/bin/env python3
"""CI gate: every campaign dir with results must have a PREREG.md.
Exits non-zero otherwise. Campaigns may mark a PREREG RETROACTIVE (disclosed,
not hidden) — the gate enforces existence, the report enforces honesty."""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fail = []
sd = os.path.join(ROOT, "sweeps")
for name in sorted(os.listdir(sd)):
    cdir = os.path.join(sd, name)
    if not os.path.isdir(cdir): continue
    res = os.path.join(cdir, "results")
    has_results = os.path.isdir(res) and any(
        f for f in os.listdir(res) if not f.startswith("."))
    if has_results and not os.path.exists(os.path.join(cdir, "PREREG.md")):
        fail.append(name)
if fail:
    print("FAIL: campaigns with results but no PREREG.md:", ", ".join(fail))
    sys.exit(1)
print("PREREG gate OK")
