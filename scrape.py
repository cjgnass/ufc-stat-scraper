
import requests
from typing import List, Tuple
from bs4 import BeautifulSoup

## Scrape Data ## 
def get_event_data(url: str) -> Tuple[str, List[dict]]:
    """
    Args:
        url (str): URL of event

    Returns:
        Tuple[str, List[dict]]: name of event, list of dictionaries of match data

    """
    event_data = {}
    event_name = get_event_name(url)
    match_urls = get_match_urls(url)

    
    match_url = match_urls[0]
    match_data = get_match_data(match_url)



    return event_name, event_data

def get_event_name(url: str) -> str:
    """
    Args:
        url (str): URL of event

    Returns:
        event_name (str): name of event
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    element = soup.find('span', class_='b-content__title-highlight')
    event_name = element.contents[0].strip()

    return event_name

def get_match_data(url: str) -> dict:
    """
    Args:
        url (str): URL of match

    Returns:
        dict: dictionary with fight data
             
    """
    data = {}
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    fighters = find_matchup(soup)
    match_name = fighters[0] + ' vs ' + fighters[1]


    
    return match_name,

def find_matchup(soup: BeautifulSoup) -> Tuple[str, str]:
    """
    Args:
        soup (BeautifulSoup): nested data structure that represents a document
    
    Returns:
        Tuple[str, str]: tuple containing the names of the two fighters (fighter1, fighter2) 
    """
    elements = soup.find_all('a', class_='b-link b-fight-details__person-link')
    fighter1 = elements[0].contents[0].strip()
    fighter2 = elements[1].contents[0].strip()
    
    return fighter1, fighter2

## Scrape URLs ##
def get_event_urls(url: str) -> List[str]:
    """
    Args:
        url (str): URL containing links to events

    Returns:
        List[str]: list of event URLs
    """
    event_urls = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all('a', class_='b-link b-link_style_black')
    for element in elements:
        event_urls.append(element['href'])

    return event_urls



def get_match_urls(url: str) -> List[str]:
    """
    Args:
        url (str): URL containing links to matches

    Returns:
        List[str]: list of match URLs
    """
    match_urls = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all('a', class_='b-flag b-flag_style_green')
    for element in elements:
        match_urls.append(element['href'])

    return match_urls










    






