#!/usr/bin/env python3
"""
PageFetcher - A script to fetch web pages and search for Impressum links.

Usage: python page_fetcher.py <path_to_pages.txt>
"""

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time


def is_valid_url(url):
    """Check if the URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def fetch_page(url):
    """Fetch a webpage and return its content."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def find_impressum_links(html_content, base_url):
    """Search for Impressum links in the HTML content."""
    if not html_content:
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    impressum_links = []
    
    # Search for links containing "Impressum" text
    links = soup.find_all('a', href=True)
    
    for link in links:
        link_text = link.get_text(strip=True).lower()
        if 'impressum' in link_text:
            href = link['href']
            # Convert relative URLs to absolute URLs
            absolute_url = urljoin(base_url, href)
            impressum_links.append({
                'text': link.get_text(strip=True),
                'url': absolute_url
            })
    
    # Also search for text containing "Impressum" that might be linked
    impressum_elements = soup.find_all(string=lambda text: text and 'impressum' in text.lower())
    for element in impressum_elements:
        parent = element.parent
        if parent and parent.name == 'a' and parent.get('href'):
            href = parent['href']
            absolute_url = urljoin(base_url, href)
            if not any(link['url'] == absolute_url for link in impressum_links):
                impressum_links.append({
                    'text': element.strip(),
                    'url': absolute_url
                })
    
    return impressum_links


def process_pages_file(file_path):
    """Process the pages.txt file and search for Impressum links on each page."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Count only valid URLs (skip comments and empty lines)
        valid_urls = []
        for line in lines:
            url = line.strip()
            if url and not url.startswith('#') and not line.lstrip().startswith('#'):
                valid_urls.append(url)
        
        print(f"Processing {len(valid_urls)} URLs from {file_path}")
        print("-" * 60)
        
        for line_num, line in enumerate(valid_urls, 1):
            url = line.strip()
            
            if not is_valid_url(url):
                print(f"Line {line_num}: Invalid URL - {url}")
                continue
            
            print(f"\nLine {line_num}: Checking {url}")
            
            # Fetch the page
            html_content = fetch_page(url)
            if html_content is None:
                continue
            
            # Search for Impressum links
            impressum_links = find_impressum_links(html_content, url)
            
            if impressum_links:
                print(f"✓ Found {len(impressum_links)} Impressum link(s):")
                for i, link in enumerate(impressum_links, 1):
                    print(f"  {i}. Text: '{link['text']}'")
                    print(f"     URL:  {link['url']}")
            else:
                print("✗ No Impressum links found")
            
            # Small delay to be respectful to servers
            time.sleep(1)
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)


def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python page_fetcher.py <path_to_pages.txt>")
        print("\nExample: python page_fetcher.py pages.txt")
        sys.exit(1)
    
    pages_file = sys.argv[1]
    
    print("PageFetcher - Impressum Link Finder")
    print("=" * 40)
    
    process_pages_file(pages_file)
    
    print("\n" + "=" * 40)
    print("Processing complete!")


if __name__ == "__main__":
    main()