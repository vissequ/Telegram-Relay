import requests
from bs4 import BeautifulSoup

def get_substack_articles(substack_url):
    # Convert Substack URL to RSS feed URL
    if not substack_url.endswith('/'):
        substack_url += '/'
    rss_url = f"{substack_url}feed"
    
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
            
        # Print each article's title and link
        print(f"Found {len(articles)} articles:\n")
        for i, article in enumerate(articles, 1):
            title = article.find('title').text
            link = article.find('link').text
            print(f"{i}. {title}")
            print(f"   {link}\n")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the feed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Get Substack URL from user
    substack_url = input("Enter the Substack URL (e.g., https://example.substack.com): ").strip()
    
    # Validate URL basic format
    if not substack_url.startswith('http'):
        substack_url = 'https://' + substack_url
    
    print(f"\nFetching articles from {substack_url}...\n")
    get_substack_articles(substack_url)

if __name__ == "__main__":
    # Check if required libraries are installed
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("Please install required libraries:")
        print("pip install requests beautifulsoup4")
        exit()

    main()
