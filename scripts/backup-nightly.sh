#!/bin/zsh
#
# The nightly entry point for `sts backup`, run by launchd.
#
# WHY A WRAPPER AND NOT THE PLIST DIRECTLY
#
# Two reasons, both about credentials.
#
# `sts backup` needs SUPABASE_URL and the service key. Those live in exactly
# one place on this machine, the .env beside the deploy worktree, and they
# deliberately do NOT exist in the canonical worktree: a production service key
# has no business sitting in a tree that gets branched, stashed and rebased.
# sts.py reads ROOT/.env first and falls back to the process environment, which
# is the designed escape hatch for precisely this. So the wrapper sources the
# one real .env and hands the values over for the length of one command.
#
# And a launchd plist is a world-readable file in ~/Library/LaunchAgents.
# Putting the key in its EnvironmentVariables block would copy a production
# credential to a second location on disk for no benefit. The plist names this
# script; only this script touches the secret.
#
# WHAT IT DOES NOT DO
#
# It does not pass storage files. A full `sts backup` also downloads the
# 94 MB research bundle, and that object is immutable - backing it up 365 times
# a year would spend 34 GB to store one file. The nightly run still records the
# bucket inventory (names, sizes, mimetypes), so a bundle that changed would be
# visible in the diff, and one full copy including the file already exists.
# Run `python3 scripts/sts.py backup` by hand when the bundle actually changes.
#
# It also does not copy anything off this machine. Local disk is a second copy
# of Supabase, which is the point, but two copies in one apartment is not
# disaster recovery. That step is still open.

set -euo pipefail

REPO="${STS_REPO:-$HOME/Code/active/sts-v0.7.3}"
ENV_FILE="${STS_ENV_PATH:-$HOME/Code/active/survivingthesingularity/.env}"

echo "=== $(date '+%Y-%m-%d %H:%M:%S %Z') sts backup ==="

if [[ ! -f "$ENV_FILE" ]]; then
  echo "FAILED: no .env at $ENV_FILE (set STS_ENV_PATH to override)"
  exit 1
fi

# Export only what the backup needs. Sourcing the whole file would drag the
# Stripe and Resend keys into the environment of a job that has no use for them.
SUPABASE_URL="$(/usr/bin/grep -m1 '^SUPABASE_URL=' "$ENV_FILE" | cut -d= -f2- | tr -d '"'"'"' ')"
SUPABASE_SERVICE_KEY="$(/usr/bin/grep -m1 '^SUPABASE_SERVICE_KEY=' "$ENV_FILE" | cut -d= -f2- | tr -d '"'"'"' ')"
export SUPABASE_URL SUPABASE_SERVICE_KEY

if [[ -z "$SUPABASE_URL" || -z "$SUPABASE_SERVICE_KEY" ]]; then
  echo "FAILED: SUPABASE_URL or SUPABASE_SERVICE_KEY missing from $ENV_FILE"
  exit 1
fi

cd "$REPO"
# --no-files: see above. sts backup exits non-zero when any table dumps short
# of the server's own row count, so launchd surfaces a broken backup instead of
# a directory full of quietly incomplete files.
exec /usr/bin/python3 scripts/sts.py backup --no-files
