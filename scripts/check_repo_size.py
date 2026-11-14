#!/usr/bin/env python3
"""Repo hygiene gate: no tracked file over MAX_MB.

GitHub hard-blocks pushes containing any blob >100 MB, and removing one
afterwards requires rewriting history (we learned this shipping campaign #3's
173 MB D-sweep). Policy: full-size sweep outputs live in work/ (gitignored);
tracked results ship top-K rows + sha256 of the full file + a deterministic
regeneration command in the campaign REPORT.
"""
import os, subprocess, sys

MAX_MB = 50

def main():
    files = subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.split()
    big = [(f, os.path.getsize(f)) for f in files if os.path.exists(f)
           and os.path.getsize(f) > MAX_MB * 1024 * 1024]
    if big:
        for f, sz in big:
            print(f"TOO BIG: {f}  ({sz/1e6:.1f} MB > {MAX_MB} MB) — "
                  f"move the full artifact to work/ and ship top-K rows + hash + regen command")
        sys.exit(1)
    print(f"repo size gate OK ({len(files)} tracked files, all <= {MAX_MB} MB)")

if __name__ == "__main__":
    main()
