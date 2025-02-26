import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def send_telegram_message(bot_token, chat_id, message):
    """Send a message to a Telegram channel."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Successfully sent message: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram message: {e}")

def get_substack_articles():
    rss_url = "https://arditimagazine.substack.com/feed"
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("Error: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set.")
        return
    
    # Set up headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(rss_url)
        
        # Wait for page to load (adjust time if needed)
        driver.implicitly_wait(10)
        
        # Get the page source after Cloudflare check
        page_source = driver.page_source
        driver.quit()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(page_source, 'xml')
        articles = soup.find_all('item')
        
        if not articles:
            print("No articles found in the feed...")
            return
            
        print(f"Found {len(articles)} articles. Sending to Telegram...")
        
        for i, article in enumerate(articles, 1):
            title = article.find('title').text
            link = article.find('link').text
            message = f"*{title}*\n{link}"
            send_telegram_message(bot_token, chat_id, message)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        if 'page_source' in locals():
            print(f"Page source sample: {page_source[:500]}")

if __name__ == "__main__":
    try:
        import requests
        from bs4 import BeautifulSoup
        from selenium import webdriver
    except ImportError:
        print("Please install required libraries:")
        print("pip install requests beautifulsoup4 lxml selenium")
        exit()

    get_substack_articles()
