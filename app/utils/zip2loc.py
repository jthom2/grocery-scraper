import requests


# Used in /app/walmart/locate_store.py
# Prompts user for zip code, gathers city and state abbr.



def get_city_state(zip_code):
    url = f"https://api.zippopotam.us/us/{zip_code}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return None, None

    data = response.json()
    if not data or 'places' not in data:
        return None, None

    place = data['places'][0]
    city = place['place name']
    state = place['state abbreviation']
    return city, state

