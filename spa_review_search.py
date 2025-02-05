import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint

def scrape_google(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
    
    # Convert the response to a dictionary-like structure
    soup = BeautifulSoup(response.text, "html.parser")
    results = {
        'raw_html': response.text,
        'parsed_data': str(soup.prettify())
    }
    
    return results

# Test
query = "spa near me"
results = scrape_google(query)
pprint(results, width=120, sort_dicts=True)
