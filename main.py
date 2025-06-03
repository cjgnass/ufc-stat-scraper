from scrape import get_event_urls, get_event_data
import json
import os

starting_url = "http://ufcstats.com/statistics/events/completed?page=all"
event_urls = get_event_urls(starting_url)#[::-1]

for event_url in event_urls:
    event_data = get_event_data(event_url)
    event_name = event_data['event'].replace(' ', '-').replace(':', '').replace('.', '') + '.json'
    print(event_name)
    with open(os.path.join('events', event_name), 'w') as f:
        json.dump(event_data, f, indent=4)

