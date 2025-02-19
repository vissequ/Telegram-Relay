import os
import requests
import feedparser
import time

# Load environment variables from GitHub Secrets
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SUBSTACK_RSS = os.getenv("SUBSTACK_RSS")
RUMBLE_RSS = os.getenv("RUMBLE_RSS")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")

YOUTUBE_API_URL = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={YOUTUBE_CHANNEL_ID}&part=snippet,id&order=date&maxResults=1"

LAST_POSTS = {}

def send_telegram_message(message):
    """Send a message to the Telegram channel."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def check_rss(feed_url, source):
    """Check an RSS feed for new posts."""
    feed = feedparser.parse(feed_url)
    if feed.entries:
        latest = feed.entries[0]
        link = latest.link
        if LAST_POSTS.get(source) != link:
            LAST_POSTS[source] = link
            send_telegram_message(f"📰 New {source} post: *{latest.title}*\n{link}")

def check_youtube():
    """Check for new YouTube videos."""
    response = requests.get(YOUTUBE_API_URL).json()
    if "items" in response:
        latest = response["items"][0]
        video_id = latest["id"]["videoId"]
        video_title = latest["snippet"]["title"]
        video_link = f"https://www.youtube.com/watch?v={video_id}"
        if LAST_POSTS.get("youtube") != video_link:
            LAST_POSTS["youtube"] = video_link
            send_telegram_message(f"▶️ New YouTube Video: *{video_title}*\n{video_link}")

def main():
    check_rss(SUBSTACK_RSS, "Substack")
    check_rss(RUMBLE_RSS, "Rumble")
    check_youtube()

if __name__ == "__main__":
    main()
