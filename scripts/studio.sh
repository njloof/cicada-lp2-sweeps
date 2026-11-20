#!/bin/sh
# studio.sh — guarded remote compute on studio.local (the Mac Studio).
#
# Why this exists: the auto-mode classifier (correctly) refuses arbitrary
# remote writes/executions. This script pins the blast radius in reviewed
# code so a single permission rule — Bash(scripts/studio.sh:*) — suffices:
#   * host is hardcoded; no other host is reachable through this script
#   * sync pushes ONLY the campaign tree (fixed list; repo-relative)
#   * run executes ONLY ~/cicada-venv/bin/python inside ~/cicada-c7, and
#     only arguments matching a conservative allowlist (no shell metachars)
#   * pull fetches ONLY paths under sweeps/ or work/ on the remote side
#
# Usage:
#   scripts/studio.sh sync                     # push fixed tree
#   scripts/studio.sh run <script.py> [args]   # run under campaign venv python
#   scripts/studio.sh pull <remote-rel> <dest> # fetch a result file
#   scripts/studio.sh status                   # host check
set -eu

HOST="studio.local"
REMOTE_HOME="cicada-c7"                      # relative to remote $HOME
VENV_PY="~/cicada-venv/bin/python"
# Fixed sync list (repo-relative). Keep this minimal and auditable.
SYNC_PATHS="core data/pages data/manifest.json data/solved_plaintexts.json docs sources/scream314/liber_primus.md sources/dukotah/liber-primus/data/english_quadgrams.txt sources/dukotah/liber-primus/data/krisyotam_runes.txt sources/dukotah/liber-primus/data/keys/armada18/lp1_runes_as_key.json sources/dukotah/liber-primus/data/keys/armada18/lp1_english_forward.txt sources/dukotah/liber-primus/data/keys/armada18/lp1_english_reversed.txt sources/dukotah/liber-primus/data/keys/armada18/emerson_essays_first_series.txt sources/dukotah/liber-primus/analysis/round27/P0-spec/vectors.json sources/dukotah/liber-primus/analysis/round28/L4/gen28.py sources/dukotah/liber-primus/analysis/round28/L4/receipts/genval.json sources/dukotah/liber-primus/analysis/round19/G3/gen_py27.py sources/dukotah/liber-primus/analysis/stego/provenance.json sweeps"

die() { echo "studio.sh: $*" >&2; exit 2; }

case "${1:-}" in
  status)
    ssh -o ConnectTimeout=5 "$HOST" 'hostname; sysctl -n hw.ncpu; ~/cicada-venv/bin/python -c "import numpy; print(numpy.__version__)"'
    ;;
  sync)
    [ "$#" -eq 1 ] || die "sync takes no arguments"
    # -R recreates the repo-relative structure under REMOTE_HOME
    # shellcheck disable=SC2086
    rsync -aR --exclude __pycache__ --exclude results/null_*checkpoint* --exclude docs/img $SYNC_PATHS "$HOST:$REMOTE_HOME/"
    ;;
  run)
    [ "$#" -ge 2 ] || die "run needs a script"
    shift
    # conservative allowlist: word chars, dot, slash, dash, equals, comma
    for a in "$@"; do
      printf '%s' "$a" | grep -Eq '^[A-Za-z0-9_./,=-]+$' || die "argument rejected: $a"
    done
    ssh "$HOST" "cd ~/$REMOTE_HOME && $VENV_PY $*"
    ;;
  pull)
    [ "$#" -eq 3 ] || die "pull needs <remote-rel> <dest>"
    case "$2" in
      sweeps/*|work/*) ;;
      *) die "remote path must be under sweeps/ or work/" ;;
    esac
    rsync "$HOST:$REMOTE_HOME/$2" "$3"
    ;;
  *)
    die "usage: studio.sh {status|sync|run <script.py> [args]|pull <remote-rel> <dest>}"
    ;;
esac
