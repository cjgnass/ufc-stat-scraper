import re 
import json
import requests



def scrape_url(url):
    
    response = requests.get(url)
    
    

    

    return response

response = scrape_url('http://ufcstats.com/fight-details/b873c116e39c9920')
print(response)


    






