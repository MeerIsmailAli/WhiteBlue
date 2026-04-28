import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from collections import deque

class PhoneCrawler:
    def __init__(self, start_url):
        # Starting point of crawl
        self.start_url = start_url
        
        # Extract domain (e.g., example.com)
        self.domain = urlparse(start_url).netloc
        
        # Keep track of visited URLs to avoid loops
        self.visited = set()
        
        # Store unique phone numbers
        self.phone_numbers = set()

    def normalize_phone(self, phone):
        """
        Convert phone numbers into a consistent format.
        Example: 98765-43210 → +919876543210
        """
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)

        # Handle Indian numbers (basic logic)
        if len(digits) == 10:
            return "+91" + digits
        elif len(digits) > 10 and digits.startswith("91"):
            return "+" + digits
        elif digits.startswith("0"):
            return "+91" + digits[1:]

        # Fallback
        return "+" + digits

    def extract_phones(self, text):
        """
        Extract phone numbers from text using regex
        """
        phone_pattern = re.compile(
            r'(\+?\d{1,3}[\s-]?)?\(?\d{2,5}\)?[\s-]?\d{3,5}[\s-]?\d{4}'
        )

        # Find all matches
        for match in re.finditer(phone_pattern, text):
            raw_phone = match.group()
            normalized = self.normalize_phone(raw_phone)
            
            # Store only unique numbers
            self.phone_numbers.add(normalized)

    def get_links(self, soup, base_url):
        """
        Extract all valid links from a page (same domain only)
        """
        links = set()

        for tag in soup.find_all("a", href=True):
            href = tag['href']
            
            # Convert relative → absolute URL
            full_url = urljoin(base_url, href)
            parsed = urlparse(full_url)

            # Only allow same-domain links
            if parsed.netloc == self.domain:
                links.add(full_url)

        return links

    def crawl(self, max_pages=50):
        """
        Main crawling logic using BFS
        """
        # Queue for BFS traversal
        queue = deque([self.start_url])

        while queue and len(self.visited) < max_pages:
            # Get next URL to process
            url = queue.popleft()

            # Skip if already visited
            if url in self.visited:
                continue

            print(f"Crawling: {url}")
            self.visited.add(url)

            try:
                # Fetch webpage
                response = requests.get(url, timeout=5)

                # Skip if request failed
                if response.status_code != 200:
                    continue

                # Parse HTML
                soup = BeautifulSoup(response.text, "html.parser")

                # Extract phone numbers from visible text
                self.extract_phones(soup.get_text())

                # Extract links and add to queue
                for link in self.get_links(soup, url):
                    if link not in self.visited:
                        queue.append(link)

            except Exception as e:
                # Handle errors gracefully
                print(f"Error fetching {url}: {e}")
                continue

        # Return final list of unique phone numbers
        return list(self.phone_numbers)


# -------------------------------
# main entry
# -------------------------------
if __name__ == "__main__":
    url = "https://www.nitk.ac.in/"
    
    crawler = PhoneCrawler(url)
    phones = crawler.crawl(max_pages=20)

    print("\nExtracted Phone Numbers:")
    for p in phones:
        print(p)        