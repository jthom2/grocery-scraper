import requests
from functools import lru_cache
import time

from app.utils.cache import TTLCache


# Used in /app/walmart/locate_store.py
# Prompts user for zip code, gathers city and state abbr.
# Uses aggressive in-memory caching with 24-hour TTL to eliminate external API calls for repeated lookups

_ZIP_CACHE = TTLCache(ttl_seconds=24 * 60 * 60)  # 24-hour cache


from app.errors import ScraperNetworkError, ScraperParsingError, ScraperDataNotFoundError


@lru_cache(maxsize=256)
def _fetch_from_api(zip_code):
    # fetch zip code data from external API (cached separately for rare misses)
    url = f"https://api.zippopotam.us/us/{zip_code}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 404:
            raise ScraperDataNotFoundError(f"ZIP code not found: {zip_code}", status_code=404, url=url)
        elif response.status_code != 200:
            raise ScraperNetworkError(f"API returned {response.status_code}", status_code=response.status_code, url=url)

        data = response.json()
        if not data or 'places' not in data or not data['places']:
            raise ScraperParsingError(f"Unexpected API response for {zip_code}", status_code=response.status_code, url=url)

        place = data['places'][0]
        city = place['place name']
        state = place['state abbreviation']
        return city, state
    except (requests.RequestException, KeyError, IndexError) as e:
        if isinstance(e, requests.RequestException):
            raise ScraperNetworkError(f"API request failed: {e}", url=url)
        raise ScraperParsingError(f"Failed to parse API response: {e}", url=url)


def get_city_state(zip_code):
    # get city and state for a zip code with aggressive caching
    # checks TTL cache first (24-hour), then falls back to external API
    # this cache-aside pattern eliminates one network round-trip for repeated ZIP lookups
    cached = _ZIP_CACHE.get(zip_code)
    if cached is not None:
        return cached
    
    result = _fetch_from_api(zip_code)
    _ZIP_CACHE.set(zip_code, result)
    return result

