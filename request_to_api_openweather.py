import requests
API_KEY = '8410a325b25bba0213254a8489ade0bd'


def request_to_api(lat, lon):
    url = f'https://api.openweathermap.org/' \
          f'data/2.5/onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    return requests.get(url).json()
