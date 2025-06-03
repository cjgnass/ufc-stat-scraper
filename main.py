from scrape import get_event_urls, get_event_data
import json
from pprint import pprint




starting_url = "http://ufcstats.com/statistics/events/completed?page=all"
event_urls = get_event_urls(starting_url)#[::-1]
event1_url = event_urls[50]
event_data = get_event_data(event1_url)


with open('output.json', 'w') as f:
    json.dump(event_data, f, indent=4)








