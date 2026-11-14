# Project notes (cicada-lp2-sweeps)

## Repo hygiene — learned the hard way (2026-11-14)

- **Never commit large result blobs.** A 173 MB sweep CSV blocked the GitHub
  push (100 MB hard limit) and its removal required rewriting the unpushed
  history — which re-pins every commit hash quoted in reports/metadata.
- Full-size artifacts go to `work/` (gitignored). Tracked `results/` CSVs ship
  as top-K rows with the full file's sha256 + a deterministic regeneration
  command disclosed in the campaign REPORT.
- Enforced by `scripts/check_repo_size.py` (50 MB, CI step).

## Campaign discipline (see docs/LEDGER.md rules)

- PREREG.md is committed before any campaign output exists (CI gate).
- `metadata.json` pins corpus sha256 + core git rev + seed. If history is ever
  rewritten, grep all docs/metadata for stale commit hashes and re-pin them.
- MC nulls must match the scan (family-specific); flags from ≤20-draw nulls
  are provisional until a sharper confirmation campaign.

## Standing constraints

- Commit messages end with `Co-Authored-By: Claude Code <noreply@anthropic.com>`.
- All public-facing actions (GitHub push, dukotah issue, wiki edits) require
  explicit user approval each time — prior approval does not carry over.
