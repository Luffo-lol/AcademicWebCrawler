import requests
from bs4 import BeautifulSoup
import time

def crawl(url, depth=1):
    visited = set()  # Keeps track of visited sites
    with open('sites/visited.txt', 'r') as file:  # Load previously visited URLs
        for line in file:
            visited.add(line.strip())

    keywords = [
        'faculty', 'people', 'researchers', 'staff', 'team',
        'directory', 'profile', 'bio', 'lab', 'academic',
        'staff-directory', 'department', 'professors', 'research'
    ]

    usefulUrls = set()

    def is_profile_page(soup):
        """Check if a page matches typical patterns of a faculty profile."""
        # Check for common headings
        headings = soup.find_all(['h1', 'h2', 'h3'])
        if any('Professor' in heading.text or 'Faculty' in heading.text for heading in headings):
            return True

        # Check for contact details (like email addresses)
        if soup.find('a', href=lambda href: href and 'mailto:' in href):
            return True

        # Check for sections with profile-like structure
        profile_keywords = ['Biography', 'Research', 'Contact', 'Education']
        for section in soup.find_all(['div', 'section']):
            if any(keyword in section.text for keyword in profile_keywords):
                return True

        return False

    def scrapePage(currURl, currDepth):
        if currURl in visited or currDepth > depth:
            return
        try:
            response = requests.get(currURl, timeout=5)
            response.raise_for_status()
            visited.add(currURl)

            soup = BeautifulSoup(response.text, 'html.parser')

            # Check if the URL or page content matches the profile criteria
            if any(keyword in currURl for keyword in keywords) or is_profile_page(soup):
                usefulUrls.add(currURl)

            print(f"Links found on {currURl}:")
            for a_tag in soup.find_all('a', href=True):
                link = a_tag['href']

                # Convert relative links to absolute links
                if not link.startswith("http"):
                    link = requests.compat.urljoin(currURl, link)

                print(link)
                # Follow the link (if it's not already visited)
                scrapePage(link, currDepth + 1)

            # Delay to avoid overloading servers
            time.sleep(1)

        except Exception as e:
            print(f"Error scraping {currURl}: {e}")

    scrapePage(url, 1)

    with open('sites/visited.txt', 'w') as file:
        for item in visited:
            file.write(item + '\n')

    with open('sites/usefulWebsites1.txt', 'a') as file:
        for item in usefulUrls:
            file.write(item + '\n')


with open('sites/firstSearch.txt', 'r') as file:
    for item in file:
        crawl(item.strip(), depth=2)
