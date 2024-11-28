import requests
import json
import time

# Define constants
API_URL = "https://data.lacity.org/resource/2nrs-mtv8.json"
OUTPUT_FILE = "la_city_crime_data.json"
LIMIT = 1000  # Maximum allowed by the API
TOTAL_RECORDS = 990293  # Total number of records in the dataset

def fetch_data():
    all_data = []
    offset = 0

    while offset < TOTAL_RECORDS:
        # Define query parameters
        params = {
            "$limit": LIMIT,
            "$offset": offset
        }
        
        # Make the request
        response = requests.get(API_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            all_data.extend(data)  # Add the data to the list
            print(f"Fetched {len(data)} records. Total records fetched: {len(all_data)}")
            
            # Check if there are fewer records returned than LIMIT; if so, we've reached the end
            if len(data) < LIMIT:
                break

            # Increment offset for next batch
            offset += LIMIT

            # Sleep to avoid hitting rate limits
            time.sleep(1)  # Adjust delay as needed
        else:
            print(f"Failed to fetch data at offset {offset}. Status code: {response.status_code}")
            break

    # Save all data to a JSON file
    with open(OUTPUT_FILE, "w") as file:
        json.dump(all_data, file)
    
    print(f"Data fetching completed. Total records saved: {len(all_data)}")

if __name__ == "__main__":
    fetch_data()
