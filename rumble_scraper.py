import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
RUMBLE_CHANNEL_URL = os.getenv("RUMBLE_CHANNEL_URL")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Debugging prints
print(f"📌 RUMBLE_CHANNEL_URL: {RUMBLE_CHANNEL_URL}")
print(f"📌 TELEGRAM_BOT_TOKEN Loaded: {'Yes' if TELEGRAM_BOT_TOKEN else 'No'}")
print(f"📌 TELEGRAM_CHAT_ID: {TELEGRAM_CHAT_ID}")

def send_telegram_message(message):
    """Send a message to the Telegram channel."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("✅ Message sent successfully!")
    else:
        print(f"❌ Failed to send message: {response.status_code}, {response.text}")

def get_rumble_videos():
    """Scrape video titles and links from the Rumble channel page."""
    print(f"🔍 Fetching Rumble channel: {RUMBLE_CHANNEL_URL}")

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(RUMBLE_CHANNEL_URL, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to load Rumble channel! HTTP {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all video elements
    video_elements = soup.find_all("a", class_="video-item--a")

    videos = []
    for video in video_elements[:5]:  # Limit to 5 latest videos
        title = video.get("title", "No Title")
        link = "https://rumble.com" + video["href"]
        videos.append((title, link))

    return videos

def main():
    """Fetch and send Rumble videos to Telegram."""
    videos = get_rumble_videos()

    if not videos:
        print("❌ No videos found!")
        return

    print(f"✅ Found {len(videos)} videos!")

    for title, link in videos:
        message = f"🎥 *New Rumble Video:* {title}\n🔗 {link}"
        send_telegram_message(message)

if __name__ == "__main__":
    main()
