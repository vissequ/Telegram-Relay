import requests
from bs4 import BeautifulSoup
import os

def send_telegram_message(bot_token, chat_id, message):
    """Send a message to a Telegram channel."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"  # Allows clickable links
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Successfully sent message: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram message: {e}")

def get_substack_articles():
    # Hardcoded Substack RSS feed URL
    rss_url = "https://arditimagazine.substack.com/feed"
    
    # Get Telegram credentials from environment variables
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("Error: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set.")
        return
    
    try:
        # Fetch the RSS feed
        response = requests.get(rss_url)
        response.raise_for_status()  # Check if request was successful
        
        # Parse the XML content
        soup = BeautifulSoup(response.content, 'xml')
        
        # Find all items (articles) in the feed
        articles = soup.find_all('item')
        
        if not articles:
            print("No articles found in the feed...")
            return
            
        print(f"Found {len(articles)} articles. Sending to Telegram...")
        
        # Send each article to Telegram
        for i, article in enumerate(articles, 1):
            title = article.find('title').text
            link = article.find('link').text
            # Format message with headline and clickable link
            message = f"*{title}*\n{link}"
            send_telegram_message(bot_token, chat_id, message)
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the feed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Check if required libraries are installed
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("Please install required libraries:")
        print("pip install requests beautifulsoup4 lxml")
        exit()

    get_substack_articles()
