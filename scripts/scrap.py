import requests
from bs4 import BeautifulSoup
import time 
from pageinfo import PageInfo
import json

MEMBER_PREVIEWS_JSON = 'data/member_previews.json' 
TEST_YODA_FIRST_PAGE_PREVIEWS = 'data/test_yoda_first_page_previews.html'
BASE_URL = 'https://www.nogizaka46.com'

def fetch_soup(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def fetch_test_soup(url):
    html_content = open('data/test_output.html')
    soup = BeautifulSoup(html_content, "html.parser")
    return soup

'''
scrape URLs from one dashboard page.
'''
def scrape_page_previews(url):
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
        soup = fetch_soup(url) 
        
        bl_list = soup.find("div", class_="bl--list")
        
        links = []
        thumb_links = []
        titles = []
        dates = []
        

        for item in bl_list.find_all("a", class_="bl--card js-pos a--op hv--thumb"):
            link = item["href"] # it's a relative link, missed the prefix
            links.append(BASE_URL + link)

        for bl_thumb in bl_list.find_all('div', class_ = 'bl--card__img hv--thumb__i'):
            bl_bg = bl_thumb.find('div', class_='m--bg js-bg')
            thumb_link = bl_bg['data-src']
            thumb_links.append(thumb_link)
        
        for card_text in bl_list.find_all('div', class_ = 'bl--card__tx'):
            title = card_text.find('p', class_='bl--card__ttl').text
            titles.append(title)

            _date = card_text.find('p', class_ = 'bl--card__date').text
            dates.append(_date)


        #print(f'links ({len(links)}): {links}\n thumb_links ({len(thumb_links)}): {thumb_links}\n \
        #      titles ({len(titles)}): {titles}\n dates ({len(dates)}): {dates}\n')

        cards = []
        for i in range(len(links)):
            card = PageInfo(
                page_link=links[i]
                , thumb_link = thumb_links[i]
                , title = titles[i]
                , datez = dates[i]
            )
            cards.append(card.to_dict())
            
        return cards

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
    
    #dash_page_urls = [ "https://www.nogizaka46.com/s/n46/diary/MEMBER/list?ima=1521&ct=36760" ] ## TODO sostituisci con quello sopra
    page_previews = []
    

    for url in dash_page_urls:
        print(f"scraping url {url}...")
        time.sleep(2)
        cur_page_previews = scrape_page_previews(url)
        page_previews += cur_page_previews

    
    #print (f"detail_page_urls: {detail_page_urls}")
    
    with open(MEMBER_PREVIEWS_JSON, 'w') as f:  # 'w' mode truncates the file
        pass
    with open(MEMBER_PREVIEWS_JSON, 'a') as f:
        json.dump(page_previews, f, indent=2)


if __name__ == '__main__':
    main()