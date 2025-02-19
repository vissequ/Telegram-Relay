import os
import feedparser
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Substack RSS feed URL from .env
SUBSTACK_RSS = os.getenv("SUBSTACK_RSS")

def list_substack_articles():
    """Fetch and display all articles from the Substack RSS feed."""
    if not SUBSTACK_RSS:
        print("Error: SUBSTACK_RSS is not set in the .env file.")
        return

    feed = feedparser.parse(SUBSTACK_RSS)

    if not feed.entries:
        print("No articles found.")
        return

    print("\n🔹 Substack Articles:\n")
    for idx, entry in enumerate(feed.entries, start=1):
        print(f"{idx}. {entry.title}")
        print(f"   📰 {entry.link}\n")

if __name__ == "__main__":
    list_substack_articles()
