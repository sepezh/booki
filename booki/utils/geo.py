""" geo utils """
import requests


def get_long_lat(address, zip_code, city, country):
    """Fetch longitude and latitude from address"""
    full_address = f'{address}, {zip_code} {city}, {country}'
    url = 'https://nominatim.openstreetmap.org/search?q="' + full_address + '"&format=json&email=booki@example.com'
    try:
        response = requests.get(url,headers={'User-Agent': 'booki/1.0'}, timeout=60)
        response.raise_for_status()
        response = response.json()
    except Exception as e:  # pylint: disable=bare-except
        print(f"Error fetching longitude and latitude: {e}")
        return 0, 0

    return float(response[0]["lon"]), float(response[0]["lat"])
