# MIB tenders → Telegram

Checks https://mib.com.mv/tenders every 10 minutes on this Mac (launchd) and posts new tenders to a Telegram channel.

## Setup
1. Put the bot token and channel in `.env` (git-ignored):
   ```
   TELEGRAM_BOT_TOKEN=123:abc
   TELEGRAM_CHAT_ID=@yourchannel
   ```
2. Load the job: `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.user.mibtenders.plist`
   (plist source: `com.user.mibtenders.plist` in this repo)

Logs: `~/Library/Logs/mibtenders.log`. Run once now: `launchctl kickstart gui/$(id -u)/com.user.mibtenders`
Stop: `launchctl bootout gui/$(id -u)/com.user.mibtenders`
Local test: `python3 mibtenders.py --dry-run`
