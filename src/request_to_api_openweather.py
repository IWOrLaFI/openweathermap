import requests
TOKEN = '8410a325b25bba0213254a8489ade0bd'


def request_to_api(lat, lon):
    """
    request to api openweathermap
    :param lat: city's geographic coordinate latitude
    :param lon: city's geographic coordinate longitude
    :return:
    """
    url = f'https://api.openweathermap.org/' \
          f'data/2.5/onecall?lat={lat}&lon={lon}&appid={TOKEN}&units=metric'
    return requests.get(url).json()
