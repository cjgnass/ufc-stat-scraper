
import requests
from typing import List
from bs4 import BeautifulSoup


## Scrape Match Data ## 
def scrape_match_data(url: str) -> str:
    """
    Args:
        url (str): URL of match event

    Returns:
        (str): data of match 
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = find_matchup(soup)
    
    return content

def find_matchup(soup: BeautifulSoup) -> str:
    """
    Args:
        soup (BeautifulSoup): nested data structure that represents a document
    
    Returns:
        (str): matchup
    """
    return soup.find('a', class_='b-link').contents

## Scrape URLs ##
def scrape_event_urls(url: str) -> List[str]:
    """
    Args:
        url (str): URL containing links to events

    Returns:
        event_urls: (List[str]): list of event URLs
    """
    event_urls = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all('a', class_='b-link b-link_style_black')
    for element in elements:
        event_urls.append(element['href'])

    return event_urls



def scrape_match_urls(url: str) -> List[str]:
    """
    Args:
        url (str): URL containing links to matches

    Returns:
        match_urls (List[str]): list of match URLs
    """
    match_urls = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all('a', class_='b-flag b-flag_style_green')
    for element in elements:
        match_urls.append(element['href'])

    print(soup.find('span', class_='b-content__title-highlight').text.strip())
    return match_urls








    






