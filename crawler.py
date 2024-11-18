#this program scrapes through defined websites and saves the websites that are profiles of professers names
#this website will pull the 

import requests
from bs4 import BeautifulSoup
import time

def crawl (url, depth = 1):
    visited = set()#sets up empty matrix of visitied sites
    with open('sites/visited.txt','r') as file:#opens folder
        for line in file:
            visited.add(line.strip())#saves all previously visited urls form the folder
    
    keywords = [
    'faculty', 'people', 'researchers', 'staff', 'team', 
    'directory', 'profile', 'bio', 'lab', 'academic', 
    'staff-directory', 'department', 'professors', 'research'
    ]

    usefulUrls = set()

    def scrapePage(currURl, currDepth):#scrapes page for all data in the page
        if currURl in visited or currDepth > depth:#
            return#chechs if current url has been chech or if the current url to too deep
        try:
            response = requests.get(currURl, timeout = 5)#checks validity of site
            response.raise_for_status()
            visited.add(currURl)

            soup = BeautifulSoup(response.text, 'html.parser')#parses all html content

            for keyword in keywords:
                if keyword in currURl:
                    usefulUrls.add(currURl)
            
            print(f"Links found on {currURl}:")
            for a_tag in soup.find_all('a', href=True):
                link = a_tag['href']
                print(link)

                # Follow the link (if it's not already visited)
                if link.startswith("http"):
                    scrapePage(link, currDepth + 1)

            # Delay to avoid overloading 
            time.sleep(1)
        
        except Exception as e:
            print(f"Error scraping {currURl}: {e}")

    scrapePage(url,1)

    with open('sites/visited.txt', 'w') as file:
    # Write each item in the set to the file
        for item in visited:
            file.write(item + '\n')

    with open('sites/usefulWebsites1.txt', 'a') as file:
    # Write each item in the set to the file
        for item in usefulUrls:
            file.write(item + '\n')


with open('sites/firstSearch.txt', 'r') as file:
    #iterates through the websites we want and scrapes useful links from them
    for item in file:
        crawl(item, depth=2)
    
        