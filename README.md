# MIB tenders → Telegram

Checks https://mib.com.mv/tenders every 30 minutes and posts new tenders to a Telegram channel.

## Setup
1. In Telegram, message @BotFather → `/newbot` → copy the bot token.
2. Create a channel, add the bot as an **admin** (with "Post messages").
3. Push this folder to a GitHub repo. In *Settings → Secrets and variables → Actions* add:
   - `TELEGRAM_BOT_TOKEN` — the token
   - `TELEGRAM_CHAT_ID` — `@yourchannel` (public) or the `-100…` id (private)
4. *Actions → MIB tenders → Run workflow* once to test. The first run posts whatever is currently listed.

Local test: `python3 mibtenders.py --dry-run`
