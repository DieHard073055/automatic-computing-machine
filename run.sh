#!/bin/sh
# Loads Telegram credentials from .env, runs one check, and appends timestamped output to the log.
cd "$(dirname "$0")" || exit 1
LOG="$HOME/Library/Logs/mibtenders.log"
set -a; . ./.env; set +a
/opt/homebrew/bin/python3 mibtenders.py 2>&1 | while IFS= read -r line; do
  echo "$(date '+%Y-%m-%d %H:%M:%S') $line"
done >> "$LOG"
# Drop lines older than 1 day (untimestamped lines sort before digits, so they go too).
# Rewrite in place, not mv, so launchd's open handle on the log stays valid.
cutoff=$(date -v-1d '+%Y-%m-%d %H:%M:%S')
awk -v c="$cutoff" 'substr($0, 1, 19) >= c' "$LOG" > "$LOG.tmp" && cat "$LOG.tmp" > "$LOG" && rm "$LOG.tmp"
