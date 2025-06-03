
import requests
from typing import List, Tuple
from bs4 import BeautifulSoup

## Scrape Stats ## 
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

    fighters = get_fighters(soup)
    name = fighters[0] + ' vs ' + fighters[1]
    winner = get_winner(soup)
    method = get_method(soup)
    time_end = get_time_end(soup)
    round_end = get_round_end(soup)
    score = None
    fighter1_fight_stats, fighter2_fight_stats = get_fighter_fight_stats(soup)
   

    fight_data['name'] = name
    fight_data['fighter1'] = fighters[0]
    fight_data['fighter2'] = fighters[1]
    fight_data['winner'] = winner
    fight_data['method'] = method
    fight_data['time_end'] = time_end
    fight_data['round_end'] = round_end
    if 'Decision' in fight_data['method']:
        score = get_score(soup)
    fight_data['score'] = score
    fight_data['fighter1_fight_data'] = fighter1_fight_stats
    fight_data['fighter2_fight_data'] = fighter2_fight_stats

    return fight_data

def get_fighter_fight_stats(soup: BeautifulSoup) -> Tuple[dict, dict]:
    """
    Args:
        soup (BeautifulSoup): nested data structure that represents a document 

    Returns:
        Tuple[dict, dict]: ()
    """ 
    fighter1_fight_stats = {}
    fighter2_fight_stats = {}
    elements = soup.find_all('p', class_='b-fight-details__table-text', limit=20)[2:]
    stats = []
    for element in elements:
        stats.append(element.get_text(strip=True))
    
    fighter1_fight_stats['kd'] = int(stats[0])
    fighter2_fight_stats['kd'] = int(stats[1])

    fighter1_sig_str_landed, fighter1_sig_str_att = parse_of(stats[2])
    fighter1_fight_stats['sig_str_landed'] = fighter1_sig_str_landed
    fighter1_fight_stats['sig_str_att'] = fighter1_sig_str_att
    fighter2_sig_str_landed, fighter2_sig_str_att = parse_of(stats[3])
    fighter2_fight_stats['sig_str_landed'] = fighter2_sig_str_landed
    fighter2_fight_stats['sig_str_att'] = fighter2_sig_str_att

    fighter1_strikes_landed, fighter1_strikes_att = parse_of(stats[6])
    fighter1_fight_stats['str_landed'] = fighter1_strikes_landed
    fighter1_fight_stats['str_att'] = fighter1_strikes_att
    fighter2_strikes_landed, fighter2_strikes_att = parse_of(stats[7])
    fighter2_fight_stats['str_landed'] = fighter2_strikes_landed
    fighter2_fight_stats['str_att'] = fighter2_strikes_att

    fighter1_td_comp, fighter1_td_att = parse_of(stats[8])
    fighter1_fight_stats['td_comp'] = fighter1_td_comp
    fighter1_fight_stats['td_att'] = fighter1_td_att
    fighter2_td_comp, fighter2_td_att = parse_of(stats[9])
    fighter2_fight_stats['td_comp'] = fighter2_td_comp
    fighter2_fight_stats['td_att'] = fighter2_td_att

    fighter1_fight_stats['sub_att'] = int(stats[12])
    fighter2_fight_stats['sub_att'] = int(stats[13])

    fighter1_fight_stats['ctrl_time'] = get_ctrl_time(stats[16])
    fighter2_fight_stats['ctrl_time'] = get_ctrl_time(stats[17])

    return fighter1_fight_stats, fighter2_fight_stats    

def get_ctrl_time(time_str: str) -> int:
    """
    Args:
        time_str (str): string representing the control time for a fighter

    Returns:
        int: seconds of control time
    """ 
    minutes, seconds = map(int, time_str.split(':'))
    ctrl_time = minutes * 60 + seconds
    return ctrl_time

def parse_of(s: str) -> Tuple[int, int]:
    """
    Args:
        s (str): string representing a stat of the form '# of attempted' of '# of successful'

    Returns:
        Tuple[int, int]: returns tuple of int (# of attempted, # of successful)
    """ 
    parts = s.split(' of ')
    first = int(parts[0])
    second = int(parts[1])
    return first, second

def get_score(soup: BeautifulSoup) -> Tuple[int, int]:
    """
    Args:
        soup (BeautifulSoup): nested data structure that represents a document 

    Returns:
        Tuple[int, int]: (judges score for losing fighter, judges score for winning fighter)
    """ 
    elements = soup.find_all('i', class_='b-fight-details__text-item')
    judge1 = elements[4].get_text(strip=True)[-8:-1]
    judge2 = elements[5].get_text(strip=True)[-8:-1]
    judge3 = elements[6].get_text(strip=True)[-8:-1]
    judges = [judge1, judge2, judge3]
    score = [0, 0]
    for judge in judges:
        score[0] += int(judge[:2])
        score[1] += int(judge[-2:])
    return tuple(score)

def get_time_end(soup: BeautifulSoup) -> str:
    """
    Args:
        soup (BeautifulSoup): nested data structure that represents a document 

    Returns:
        str: time the fight ended
    """
    element = soup.find_all('i', class_='b-fight-details__text-item')[1]
    return element.get_text(strip=True)[-4:]

def get_round_end(soup: BeautifulSoup) -> int:
    """
    Args:
        soup (BeautifulSoup): nested data structure that represents a document 

    Returns:
        int: round the fight ended
    """  
    element = soup.find('i', class_='b-fight-details__text-item')
    round = int(element.get_text(strip=True)[-1])
    return round

def get_method(soup: BeautifulSoup) -> str:
    """
    Args: 
        soup (BeautifulSoup): nested data structure that represents a document
    
    Returns: 
        str: name of the winning fighter
    """
    element = soup.find('i', style='font-style: normal')
    if element:
        return element.get_text(strip=True)
    return ''

def get_winner(soup: BeautifulSoup) -> str:
    """
    Args: 
        soup (BeautifulSoup): nested data structure that represents a document
    
    Returns: 
        str: name of the winning fighter
    """
    fighters = soup.find_all('div', class_='b-fight-details__person')
    
    for fighter in fighters:
        status = fighter.find('i', class_='b-fight-details__person-status')
        if status and status.get_text(strip=True) == 'W':
            name_tag = fighter.find('h3', class_='b-fight-details__person-name')
            if name_tag and name_tag.a:
                return name_tag.a.get_text(strip=True)
    
    return ''

def get_fighters(soup: BeautifulSoup) -> Tuple[str, str]:
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



# response = requests.get('http://ufcstats.com/fight-details/212527d462690304')
# soup = BeautifulSoup(response.text, 'html.parser')
# print(get_fighter_fight_stats(soup))






    






