from scrape import get_event_urls, get_match_data, get_match_urls, get_event_data



starting_url = "http://ufcstats.com/statistics/events/completed?page=all"
event_urls = get_event_urls(starting_url)[::-1]
event1_url = event_urls[0]

event1_name, event1_data = get_event_data(event1_url)
print(event1_data)






