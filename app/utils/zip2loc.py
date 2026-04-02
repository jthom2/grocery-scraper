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

if __name__ == "__main__":
    zip_input = input("Enter zip code: ")
    res_city, res_state = get_city_state(zip_input)
    if res_city and res_state:
        print(res_city)
        print(res_state)
    else:
        print("Zip code not found.")

