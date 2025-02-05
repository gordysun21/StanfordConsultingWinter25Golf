import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# URL to scrape
url = "https://www.golfpass.com/travel-advisor/resorts/"

# Send GET request
response = requests.get(url)

# Function to fetch resort details
def fetch_resort_details(state, resort_tag):
    resort_name = resort_tag.text.strip() if resort_tag else "Unknown Resort"
    if resort_name == "Westin Hapuna Beach Resort (Hawaii Island)":
        return None

    resort_url_tag = resort_tag.find('a', href=True)  # Look for anchor tags with href attributes
    resort_url = resort_url_tag['href'] if resort_url_tag else None

    if resort_url:
        resort_response = requests.get(resort_url)
        if resort_response.status_code == 200:
            resort_soup = BeautifulSoup(resort_response.content, 'html.parser')

            # Check if the resort has a spa using data attributes
            spa_data = resort_soup.find(attrs={"data-key": "spa"})
            has_spa = spa_data["data-value"] if spa_data and "data-value" in spa_data.attrs else "No"

            price_data = resort_soup.find(attrs={"data-key": "price-range"})
            price = price_data["data-value"]

            propert_class_data = resort_soup.find(attrs={"data-key": "property-class"})
            property_class = propert_class_data["data-value"]

            print(resort_name,end="\n")
            return {
                "State/Territory": state,
                "Resort Name": resort_name,
                "Resort URL": resort_url,
                "Has Spa": has_spa,
                "Price Range": price,
                "Property Class": property_class
            }
    return None

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Dictionary to hold state-level resort URLs
    state_resorts_urls = {}

    # Find all state-level resort items (assuming they are grouped in columns)
    state_items = soup.find_all('div', class_='PromoImageOnTop-title')  # Update class based on inspection

    for item in state_items:
        # Extract the state name
        state_name = item.text.strip()  # Update class based on inspection

        state_resorts_url_tag = item.find('a', href=True)  # Look for anchor tags with href attributes
        state_resorts_url = state_resorts_url_tag['href'] if state_resorts_url_tag else None

        # Add to the dictionary
        if state_name not in state_resorts_urls:
            state_resorts_urls[state_name] = []
        state_resorts_urls[state_name].append(state_resorts_url)

    # List to store detailed resort data
    detailed_data = []

    # Function to process state resort page
    def process_state_resort_page(state, state_resort_url):
        if state_resort_url:
            state_resort_response = requests.get(state_resort_url)
            if state_resort_response.status_code == 200:
                state_resort_soup = BeautifulSoup(state_resort_response.content, 'html.parser')
                resort_name_tags = state_resort_soup.find_all('div', class_='StandardCoursePromo-title')  # Update based on inspection
                for resort_tag in resort_name_tags:
                    resort_details = fetch_resort_details(state, resort_tag)
                    if resort_details:
                        detailed_data.append(resort_details)

    # Use ThreadPoolExecutor to parallelize resort page scraping
    with ThreadPoolExecutor(max_workers=10) as executor:
        for state, state_resorts in state_resorts_urls.items():
            for state_resort_url in state_resorts:
                executor.submit(process_state_resort_page, state, state_resort_url)

    # Convert the detailed data to a DataFrame
    df = pd.DataFrame(detailed_data)

    # Save to a CSV file
    df.to_csv('detailed_golf_resorts.csv', index=False)
    print("Detailed scraping completed and data saved to detailed_golf_resorts.csv")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
