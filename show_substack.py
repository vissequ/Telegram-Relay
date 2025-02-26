import os
import feedparser
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SUBSTACK_RSS = os.getenv("SUBSTACK_RSS")

# Debugging prints
print(f"📌 Loaded TELEGRAM_BOT_TOKEN: {'Yes' if TELEGRAM_BOT_TOKEN else 'No'}")
print(f"📌 Loaded TELEGRAM_CHAT_ID: {TELEGRAM_CHAT_ID}")
print(f"📌 Loaded SUBSTACK_RSS: {SUBSTACK_RSS}")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID or not SUBSTACK_RSS:
    print("❌ Missing environment variables!")
    exit(1)

def send_telegram_message(message):
    """Send a message to Telegram channel."""
    print(f"📢 Sending message to Telegram: {message}")  # Debugging output
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    response = requests.post(url, json=payload)
    print(f"📌 Telegram API Response: {response.status_code}, {response.text}")  # Debug response

def list_substack_articles():
    """Fetch and display all articles from the Substack RSS feed."""
    feed = feedparser.parse(SUBSTACK_RSS)

    if not feed.entries:
        print("❌ No articles found!")
        return

    print(f"✅ Found {len(feed.entries)} articles!")  # Debugging output

    for idx, entry in enumerate(feed.entries[:5], start=1):  # Limit to 5 posts
        title = entry.title
        link = entry.link
        message = f"📰 *New Substack Post:* {title}\n{link}"
        send_telegram_message(message)

if __name__ == "__main__":
    list_substack_articles()
