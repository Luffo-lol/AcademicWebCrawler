import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin


def get_all_sitemap_urls(robots_url):
    rp = RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    sitemaps = rp.site_maps()

    all_urls = set()

    def extract_urls_from_sitemap(sitemap_url):
        try:
            response = requests.get(sitemap_url, timeout=5)
            soup = BeautifulSoup(response.content, 'xml')
            urls = [loc.text for loc in soup.find_all('loc')]
            for url in urls:
                if url.endswith('.xml'):
                    extract_urls_from_sitemap(url)  # recursive call for sub-sitemaps
                else:
                    all_urls.add(url)
        except Exception as e:
            print(f"Error fetching sitemap {sitemap_url}: {e}")

    if sitemaps:
        for sitemap in sitemaps:
            extract_urls_from_sitemap(sitemap)

    return all_urls


def crawl_from_sitemap(base_url):
    visited = set()
    usefulUrls = set()

    keywords = [
        'faculty', 'people', 'researchers', 'staff', 'team',
        'directory', 'profile', 'bio', 'lab', 'academic',
        'staff-directory', 'department', 'professors', 'research'
    ]

    def is_profile_page(soup):
        headings = soup.find_all(['h1', 'h2', 'h3'])
        if any('Professor' in heading.text or 'Faculty' in heading.text for heading in headings):
            return True

        if soup.find('a', href=lambda href: href and 'mailto:' in href):
            return True

        profile_keywords = ['Biography', 'Research', 'Contact', 'Education']
        for section in soup.find_all(['div', 'section']):
            if any(keyword in section.text for keyword in profile_keywords):
                return True

        return False

    robots_url = urljoin(base_url, '/robots.txt')
    sitemap_urls = get_all_sitemap_urls(robots_url)

    for currURL in sitemap_urls:
        if currURL in visited:
            continue
        try:
            response = requests.get(currURL, timeout=5)
            response.raise_for_status()
            visited.add(currURL)

            soup = BeautifulSoup(response.text, 'html.parser')

            if any(keyword in currURL.lower() for keyword in keywords) or is_profile_page(soup):
                usefulUrls.add(currURL)
                print(f"Useful URL found: {currURL}")

            time.sleep(1)

        except Exception as e:
            print(f"Error scraping {currURL}: {e}")

    with open('sites/visited.txt', 'w') as file:
        for item in visited:
            file.write(item + '\n')

    with open('sites/usefulWebsites1.txt', 'a') as file:
        for item in usefulUrls:
            file.write(item + '\n')


# Load URLs from firstSearch.txt and crawl using sitemap
with open('sites/firstSearch.txt', 'r') as file:
    for item in file:
        crawl_from_sitemap(item.strip())
