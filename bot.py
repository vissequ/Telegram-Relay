import os
import requests
import feedparser

# Load environment variables from GitHub Secrets
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SUBSTACK_RSS = os.getenv("SUBSTACK_RSS")

LAST_POST = None  # Stores the last posted article link

def send_telegram_message(message):
    """Send a message to the Telegram channel."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def check_substack():
    """Check Substack for new posts and send to Telegram if new."""
    global LAST_POST
    feed = feedparser.parse(SUBSTACK_RSS)
    if feed.entries:
        latest = feed.entries[0]  # Get the latest post
        link = latest.link

        if LAST_POST != link:
            LAST_POST = link
            message = f"📰 *New Substack Post:* {latest.title}\n{link}"
            send_telegram_message(message)

def main():
    check_substack()

if __name__ == "__main__":
    main()
