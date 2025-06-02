
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
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    name = get_event_name(soup)
    date = get_event_date(soup)

    event_data['event'] = name
    event_data['date'] = date

    fight_urls = get_fight_urls(url)
    fight_data_list = get_fights_data(fight_urls)

    for fight_data in fight_data_list:
        event_data[fight_data['name']] = fight_data

    return event_data

def get_event_name(soup: BeautifulSoup) -> str:
    """
    Args:
        soup (BeautifulSoup): nested data structure that represents a document

    Returns:
        event_name (str): name of event
    """
    element = soup.find('span', class_='b-content__title-highlight')
    event_name = element.contents[0].strip()

    return event_name

def get_event_date(soup: BeautifulSoup) -> str:
    """
    Args:
        soup (BeautifulSoup): nested data structure that represents a document

    Returns:
        event_name (str): date of event
    """
    element = soup.find('li', class_='b-list__box-list-item')
    event_date = element.contents[2].strip()

    return event_date

def get_fights_data(urls: List[str]) -> List[dict]:
    """
    Args: 
        urls (List[str]): list of URLs of fights

    Returns:
        List[dict]: list of dictionaries with data of fights
    """
    fight_data_list = []
    for url in urls:
        fight_data_list.append(get_fight_data(url))
    
    return fight_data_list





def get_fight_data(url: str) -> dict:
    """
    Args:
        url (str): URL of match

    Returns:
        dict: dictionary with fight data
             
    """
    fight_data = {}
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    fighters = find_fighters(soup)
    name = fighters[0] + ' vs ' + fighters[1]
    fight_data['name'] = name
    fight_data['fighter1'] = fighters[0]
    fight_data['fighter2'] = fighters[1]



    
    return fight_data



def find_fighters(soup: BeautifulSoup) -> Tuple[str, str]:
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


def get_fight_urls(url: str) -> List[str]:
    """
    Args:
        url (str): URL containing links to matches

    Returns:
        List[str]: list of match URLs
    """
    fight_urls = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all('a', class_='b-flag b-flag_style_green')
    for element in elements:
        fight_urls.append(element['href'])

    return fight_urls










    






