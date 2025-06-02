from scrape import scrape_event_urls, scrape_match_data, scrape_match_urls



starting_url = "http://ufcstats.com/statistics/events/completed?page=all"
event_urls = scrape_event_urls(starting_url)

match_urls = scrape_match_urls(event_urls[0])
print(match_urls)





