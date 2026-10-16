#!/bin/sh
# Loads Telegram credentials from .env and runs one check.
cd "$(dirname "$0")" || exit 1
set -a; . ./.env; set +a
exec /opt/homebrew/bin/python3 mibtenders.py
