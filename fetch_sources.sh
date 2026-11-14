#!/bin/sh
# Fetch the three upstream community repos pinned to the exact SHAs this analysis
# was validated against (see data/SOURCES.md). GitHub allows direct shallow fetch
# of a reachable SHA. Usage: ./fetch_sources.sh
set -eu

clone_pinned() {
  url="$1"; sha="$2"; dir="$3"
  if [ -d "$dir/.git" ] && [ "$(git -C "$dir" rev-parse HEAD)" = "$sha" ]; then
    echo "OK   $dir already at $sha"; return
  fi
  echo "FETCH $dir @ $sha"
  rm -rf "$dir.tmp"; mkdir -p "$(dirname "$dir")"
  git init -q "$dir.tmp"
  git -C "$dir.tmp" remote add origin "$url"
  git -C "$dir.tmp" fetch -q --depth 1 origin "$sha"
  git -C "$dir.tmp" checkout -q FETCH_HEAD
  rm -rf "$dir"; mv "$dir.tmp" "$dir"
}

clone_pinned https://github.com/Dukotah/cicada3301   9087dc36b5aa64c1786428e32180261ab9420c29 sources/dukotah
clone_pinned https://github.com/iBotPeaches/cicada_3301 a0a616d85717af59f8b806875b43d51e06e1e874 sources/ibotpeaches
clone_pinned https://github.com/scream314/cicada3301 10733feb487bb8beb9966d534727ee5897aa54fc sources/scream314

# content hashes of the files the corpus is anchored to (sha256)
check() { echo "$1  $2" | shasum -a 256 -c -; }
check 9b211a06a4bc31d60516edfad274f145aca0d8bc397d88889313d67adf0cbc55 sources/dukotah/liber-primus/data/krisyotam_runes.txt
check d404fb7a1b09751c4058f6a7603114fc3d6bb8de4446067b053846ad6e35b763 sources/dukotah/liber-primus/dataset/liber_primus.json
check cd3c6d55800375dea4d5d95f87f758ba5e832396e63fb2130f1079eb63bafc85 sources/dukotah/liber-primus/SOLVED-PAGES.json
check 0f7545d470f2056b45b5de2c8c116ecdea66969fdca6be57ccbd8e591e40ee92 sources/scream314/liber_primus.md
echo "sources verified."
