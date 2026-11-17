#!/usr/bin/env python3
"""Append per-line Romanization to ORACLE_PAGES ciphertext blocks.

OWNER-REQUESTED 2026-11-17, **DEFERRED**: run ONLY after the owner
announces their full annotation pass on all 58 pages is complete. Until
then this script must not be run against docs/ORACLE_PAGES.md.

For every numbered line inside the first fenced block after each
"**Ciphertext**" header that contains at least one runic codepoint,
append `   = ROM` where ROM is the line with each rune replaced by its
Gematria letter (core.validate TRANS) and every non-runic symbol
(`-` `.` `/` `*` `&` `$` `§` `◆N` `//` `///` quotes) passed through
unchanged. Idempotent: an existing trailing `= ...` roman segment is
stripped and recomputed, so re-running after later edits keeps lines
and romanization in sync (owner sync requirement).

Romanization is per PHYSICAL line (wrapped continuations romanize
separately, mirroring the wrap). Token/hex table fences and &/$/§
lines (no runes) are untouched.

Usage: python3 scripts/audit/append_romanization.py
"""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, os.path.abspath(ROOT))
from core.validate import GEMATRIA  # noqa: E402

MD = os.path.join(ROOT, "docs", "ORACLE_PAGES.md")

R2T = {r: t for r, t, _ in GEMATRIA}  # authoritative rune -> letter map


def _rune(c):
    return c in R2T


def roman(s):
    return "".join(R2T.get(c, c) if _rune(c) else c for c in s)


def main():
    md = open(MD).read()
    n = 0
    out = []
    pos = 0
    # process only the first fenced block after each **Ciphertext** header
    while True:
        h = md.find("**Ciphertext**", pos)
        if h < 0:
            out.append(md[pos:])
            break
        o = md.find("```", h)
        c = md.find("```", o + 3)
        if o < 0 or c < 0:
            out.append(md[pos:])
            break
        out.append(md[pos:o])
        body = md[o:c]
        lines = body.split("\n")
        for i, l in enumerate(lines):
            l = l.rstrip()
            if not any(_rune(ch) for ch in l):
                continue
            # strip a previously appended roman segment (idempotence)
            l = re.sub(r"\s+= .*$", "", l)
            # split off a generator line-annotation ("   red 13-dot lattice")
            m = re.match(r"^(.*\S)(   [A-Za-z\d].*)$", l)
            content, ann = (m.group(1), m.group(2)) if m else (l, "")
            # split off the line-number / continuation indent
            m = re.match(r"^(\s*(?:\d+\s+|\s+))(\S.*)$", content)
            num, body = (m.group(1), m.group(2)) if m else ("", content)
            if not any(_rune(ch) for ch in body):
                continue
            lines[i] = f"{num}{body}   = {roman(body)}{ann}"
            n += 1
        out.append("\n".join(lines))
        pos = c
    open(MD, "w").write("".join(out))
    print(f"romanized {n} lines")


if __name__ == "__main__":
    main()
