"""
News Headlines Web Scraper
Scrapes top headlines from news websites and saves them to a text file.
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os

class NewsHeadlineScraper:
    def __init__(self):
        # Headers to mimic a real browser request
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_bbc_news(self):
        """Scrape headlines from BBC News"""
        try:
            url = "https://www.bbc.com/news"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            headlines = []
            
            # BBC uses various selectors for headlines
            selectors = [
                'h2[data-testid="card-headline"]',
                'h3[data-testid="card-headline"]',
                'h2.sc-4fedabc7-3',
                'h3.sc-4fedabc7-3'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                for element in elements:
                    headline = element.get_text().strip()
                    if headline and len(headline) > 10:  # Filter out very short texts
                        headlines.append(headline)
            
            return list(set(headlines))  # Remove duplicates
            
        except Exception as e:
            print(f"Error scraping BBC News: {e}")
            return []
    
    def scrape_reuters(self):
        """Scrape headlines from Reuters"""
        try:
            url = "https://www.reuters.com/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            headlines = []
            
            # Reuters headline selectors
            selectors = [
                'h3[data-testid="Heading"]',
                'h2[data-testid="Heading"]',
                'a[data-testid="Heading"]',
                '.story-title'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                for element in elements:
                    headline = element.get_text().strip()
                    if headline and len(headline) > 10:
                        headlines.append(headline)
            
            return list(set(headlines))
            
        except Exception as e:
            print(f"Error scraping Reuters: {e}")
            return []
    
    def scrape_generic_news_site(self, url, site_name="Generic Site"):
        """Generic scraper for news sites using common headline tags"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            headlines = []
            
            # Common headline selectors
            selectors = [
                'h1', 'h2', 'h3',
                '.headline', '.title', '.story-title',
                '[class*="headline"]', '[class*="title"]',
                'a[href*="/news/"]', 'a[href*="/story/"]'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                for element in elements:
                    headline = element.get_text().strip()
                    if headline and len(headline) > 15 and len(headline) < 200:
                        headlines.append(headline)
            
            return list(set(headlines))[:20]  # Return top 20 unique headlines
            
        except Exception as e:
            print(f"Error scraping {site_name}: {e}")
            return []
    
    def save_headlines_to_file(self, headlines, filename="news_headlines.txt"):
        """Save headlines to a text file"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"News Headlines - Scraped on {timestamp}\n")
                f.write("=" * 60 + "\n\n")
                
                for i, headline in enumerate(headlines, 1):
                    f.write(f"{i:2d}. {headline}\n")
                
                f.write(f"\n" + "=" * 60 + "\n")
                f.write(f"Total headlines: {len(headlines)}\n")
            
            print(f"Headlines saved to {filename}")
            return True
            
        except Exception as e:
            print(f"Error saving to file: {e}")
            return False
    
    def scrape_multiple_sources(self):
        """Scrape headlines from multiple news sources"""
        all_headlines = []
        
        print("Scraping BBC News...")
        bbc_headlines = self.scrape_bbc_news()
        if bbc_headlines:
            all_headlines.extend([f"[BBC] {h}" for h in bbc_headlines[:10]])
            print(f"Found {len(bbc_headlines)} BBC headlines")
        
        time.sleep(2)  # Be respectful with requests
        
        print("Scraping Reuters...")
        reuters_headlines = self.scrape_reuters()
        if reuters_headlines:
            all_headlines.extend([f"[Reuters] {h}" for h in reuters_headlines[:10]])
            print(f"Found {len(reuters_headlines)} Reuters headlines")
        
        return all_headlines

def main():
    """Main function to run the scraper"""
    scraper = NewsHeadlineScraper()
    
    print("News Headlines Web Scraper")
    print("=" * 40)
    
    # Option 1: Scrape from multiple known sources
    print("\nScraping from multiple news sources...")
    headlines = scraper.scrape_multiple_sources()
    
    if headlines:
        print(f"\nFound {len(headlines)} headlines total")
        
        # Save to file
        scraper.save_headlines_to_file(headlines)
        
        # Display first 5 headlines
        print("\nFirst 5 headlines:")
        for i, headline in enumerate(headlines[:5], 1):
            print(f"{i}. {headline}")
    else:
        print("No headlines found. Trying generic scraper...")
        
        # Option 2: Try generic scraper on a simple news site
        test_urls = [
            ("https://www.example-news.com", "Example News"),  # Replace with actual news URL
        ]
        
        for url, name in test_urls:
            print(f"Trying {name}...")
            headlines = scraper.scrape_generic_news_site(url, name)
            if headlines:
                scraper.save_headlines_to_file(headlines, f"{name.lower().replace(' ', '_')}_headlines.txt")
                break

if __name__ == "__main__":
    main()