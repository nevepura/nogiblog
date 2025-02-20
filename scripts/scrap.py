import requests
from bs4 import BeautifulSoup
import time 

DETAIL_PAGE_URLS_FILE = 'data/detail_page_urls.txt' 

'''
scrape URLs from one dashboard page.
'''
def scrape_hrefs(url):
    """
    Scrapes the href attribute from <a> elements with a specific class.

    Args:
        url: The URL of the HTML page to scrape.

    Returns:
        A list of href values, or an empty list if no matching elements are found 
        or if there's an error during the request.  Returns None if the URL 
        is invalid or there's a serious connection problem.
    """
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        soup = BeautifulSoup(response.content, "html.parser")

        hrefs = []
        for a_tag in soup.find_all("a", class_="bl--card js-pos a--op hv--thumb"):
            href = a_tag.get("href")
            if href:  # Check if the href attribute exists and is not empty
                hrefs.append(href)

        return hrefs

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        if isinstance(e, requests.exceptions.HTTPError):  # Check if it is an HTTPError
             return [] # Return empty list in case of HTTP error
        else:
            return None # Return None in case of other request exceptions
    except Exception as e:  # Catch other potential errors (e.g., parsing errors)
        print(f"An error occurred: {e}")
        return []

def main():
    pass
    
    '''
    collect url of all pages of a member
    each url contains the url of N (= 10) pages. list the urls of the single pages
    for each URL get URL of the pages. 
    for each page URL get its content and save it in a folder. 
    '''
    dash_page_urls = [ "https://www.nogizaka46.com/s/n46/diary/MEMBER/list?ima=1521&ct=36760" 
                      , 'https://www.nogizaka46.com/s/n46/diary/MEMBER/list?ima=2602&page=1&ct=36760&cd=MEMBER' 
                      , 'https://www.nogizaka46.com/s/n46/diary/MEMBER/list?ima=4625&page=2&ct=36760&cd=MEMBER' 
                      , 'https://www.nogizaka46.com/s/n46/diary/MEMBER/list?ima=4647&page=3&ct=36760&cd=MEMBER'
                      , 'https://www.nogizaka46.com/s/n46/diary/MEMBER/list?ima=4703&page=4&ct=36760&cd=MEMBER'
                      , 'https://www.nogizaka46.com/s/n46/diary/MEMBER/list?ima=4714&page=5&ct=36760&cd=MEMBER'
                      ]
    detail_page_urls = []
    BASE_URL = 'https://www.nogizaka46.com'

    for url in dash_page_urls:
        print(f"scraping url {url}...")
        time.sleep(2)
        scraped = (scrape_hrefs(url))
        scraped = list(map(lambda s: BASE_URL + s, scraped))
        detail_page_urls = [*detail_page_urls, *scraped]
    
    #print (f"detail_page_urls: {detail_page_urls}")
    
    with open(DETAIL_PAGE_URLS_FILE, 'w') as f:  # 'w' mode truncates the file
        pass
    with open(DETAIL_PAGE_URLS_FILE, 'a') as f:
        for u in detail_page_urls:
            f.write(u + '\n')


if __name__ == '__main__':
    main()