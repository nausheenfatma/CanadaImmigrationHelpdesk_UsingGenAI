"""
This script takes a base url and crawls all the  web links (outlinks) found within the page. 
It then does to the outlinks and extracts more web links until a certain specified depth
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
from enum import Enum
import re
from collections import deque



# Start URL
start_url = "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/"

# Domain filter
base_domain = urlparse(start_url).netloc

# Track visited URLs to avoid loops
visited = set()

# immigration related path
immigration_path_path = "/en/immigration-refugees-citizenship/"

MAX_DEPTH = 3  # set your desired max depth


class Language(Enum):
    ENGLISH = 'English'
    FRENCH = 'French'
    UNKNOWN = 'Unknown'
    

def is_immigration_subpage(url):
    """ 
    Check whether the url string is a URL of our interest i.e a child path page of immigration-refugees-citizenship webpage

    Args:
        url (str): url string

    Returns:
        boolean: True if page of interest
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc == base_domain and parsed_url.path.startswith(immigration_path_path)


def get_language_from_url(url):
    """
    Determines the language of a Canada.ca URL based on the path.
    Returns 'English', 'French', or 'Unknown'.
    """
    path = urlparse(url).path.lower()

    if '/en/' in path:
        return Language.ENGLISH
    elif '/fr/' in path:
        return Language.FRENCH
    else:
        return Language.UNKNOWN
    
    
def clean_url(full_url:str):
    """
    This method cleans up a URL string
    i) removes the fragment identifier or hash anchor #wb-cont
    ii) removes suffix .html from url
    
    The cleaning of url prevents scraping of duplicate urls of different forms.
    
    Args:
        full_url (str): raw url string 

    Returns:
        str: clean url string
    """
    
    #  urlparse() breaks the URL into parts: scheme, netloc, path, params, query, and fragment.
    parsed = urlparse(full_url)

    #_replace() sets query and fragment to empty strings.
    clean = parsed._replace(query='', fragment='')
    
    # urlunparse() stitches the clean parts back together
    clean = urlunparse(clean)
    
    # Remove the '.html' extension if it exists
    clean = re.sub(r'\.html$', '', clean)
    return clean


def scrape_outlinks(url):
    """
    
    Returns all the outlinks found in the url page to crawl

    Args:
        url (str): input url to crawl

    Returns:
        set (str): set of outlinks
    """
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract and return links to subpages
        links = set()
        for link_tag in soup.find_all("a", href=True):
            full_url = urljoin(url, link_tag["href"])
            full_url = clean_url(full_url)

            # Only scrape English language pages
            language = get_language_from_url(full_url)
            
            if is_immigration_subpage(full_url) and full_url not in visited and language == Language.ENGLISH:
                links.add(full_url)
        return links
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return set()



def crawl(start_url):
    queue = deque([(start_url, 0)])  # each item is (url, depth)
    
    #BFS craw all links popped from queue (beginning from start url page)
    while queue:
        current_url, depth = queue.popleft()
        if current_url in visited or depth > MAX_DEPTH:
            continue
        
        visited.add(current_url)
        out_links = scrape_outlinks(current_url)
        for link in out_links:
            if link not in visited:
                queue.append((link, depth + 1))

crawl(start_url)