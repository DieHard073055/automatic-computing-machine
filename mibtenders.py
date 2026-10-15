"""Post new tenders from https://mib.com.mv/tenders to a Telegram channel.

Env: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID (e.g. @mychannel or -100...).
Seen tender IDs are kept in seen.json next to this file.
"""
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

URL = "https://mib.com.mv/tenders"
SEEN = Path(__file__).with_name("seen.json")
CARD = re.compile(r'<a href="(https://mib\.com\.mv/tenders/(\d+))"(.*?)</a>', re.S)


def text(pattern, block):
    m = re.search(pattern, block, re.S)
    return html.unescape(m.group(1).strip()) if m else ""


def parse(page):
    tenders = []
    for link, tid, block in CARD.findall(page):
        tenders.append({
            "id": tid,
            "link": link,
            "title": text(r"<h4[^>]*>(.*?)</h4>", block),
            "status": text(r'<span class="py-1\.5[^"]*">(.*?)</span>', block),
            "notice": text(r"<span>(Notice Date:.*?)</span>", block),
            "closes": text(r"<span>((?:Registration )?Closes.*?)</span>", block),
        })
    return tenders


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (mibtenders bot)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def send(t):
    e = html.escape
    lines = [f"<b>{e(t['title'])}</b>"]
    lines += [e(x) for x in (t["status"] and f"Status: {t['status']}", t["notice"], t["closes"]) if x]
    lines.append(t["link"])
    data = urllib.parse.urlencode({
        "chat_id": os.environ["TELEGRAM_CHAT_ID"],
        "text": "\n".join(lines),
        "parse_mode": "HTML",
    }).encode()
    url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage"
    with urllib.request.urlopen(url, data, timeout=30) as r:
        if not json.load(r).get("ok"):
            raise RuntimeError(f"Telegram rejected tender {t['id']}")


def main():
    tenders = parse(fetch(URL))
    if not tenders:
        # Layout changed or page broke: fail loudly instead of silently posting nothing.
        sys.exit("No tenders parsed from page")
    seen = set(json.loads(SEEN.read_text())) if SEEN.exists() else set()
    new = [t for t in reversed(tenders) if t["id"] not in seen]  # oldest first
    for t in new:
        if "--dry-run" in sys.argv:
            print(t)
            continue
        send(t)
        seen.add(t["id"])
        SEEN.write_text(json.dumps(sorted(seen, key=int)))  # save after each post so a crash never reposts
    print(f"{len(tenders)} listed, {len(new)} new")


if __name__ == "__main__":
    main()
