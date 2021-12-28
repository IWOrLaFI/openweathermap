import json
import time


def load_json(file_name_json, info=''):
    try:
        return json.load(open(file_name_json))
    except FileNotFoundError:
        return print(f"file {file_name_json} not found. {info}")


def find_coord_city(city_dict, city_name):
    """
         Search for coordinates (lat , lon) of a city dictionary of cities
        :param city_dict:
        :param city_name: city's name: str
        :return: json
        """

    for i in range(len(city_dict)):
        if city_dict[i]['name'] == city_name:
            lat = city_dict[i]['coord']['lat']
            lon = city_dict[i]['coord']['lon']
            return lat, lon
        i += 1
    return 404, 404


def weather_day(data):
    """
    Send the necessary information from json for the database in the required format
    :param data: data JSON
    :return: list : (date, temp, pcp, clouds, pressure, humidity, wind_speed),
    """

    def convert_dt(dt):
        """
        Convert date Unix to datatime 21 Dec 2021
        :param dt: date Unix
        :return: date dd-mm-yyyy
        """
        return time.strftime("%d-%m-%Y", time.localtime(dt))

    def f_temp(day, data_json):
        """
        Calculation of the average daily temperature.
        :param data_json: data json
        :param day:
        :return: average daily temperature in Celsius
        """
        temp_day = data_json['daily'][day]['temp']['day']
        temp_night = data_json['daily'][day]['temp']['night']
        temp_eve = data_json['daily'][day]['temp']['eve']
        temp_morn = data_json['daily'][day]['temp']['morn']
        a_temp = round(((temp_day + temp_night + temp_eve + temp_morn) / 4), 2)
        return a_temp

    def f_rain(day, data_json):
        """
        Find volume rain in data json
        :param data_json: data json
        :param day: day number
        :return: Precipitation volume
        """
        try:
            rain = (data_json['daily'][day]['rain'])
            return rain
        except KeyError:
            return 0

    def f_snow(day, data_json):
        """
         Find volume snow in data json
         :param day: day number
         :param data_json: data json
         :return: Precipitation volume
         """
        try:
            snow = data_json['daily'][day]['snow']
            return snow
        except KeyError:
            return 0

    weather_day_list = []
    for i in range(len(data)):
        date = convert_dt(data['daily'][i]['dt'])  # Time of the forecasted data (21 Dec 2021)
        temp = f_temp(i, data)  # Celsius
        pcp = round((f_rain(i, data) + f_snow(i, data)), 2)  # Precipitation volume, mm
        clouds = data['daily'][i]['clouds']  # Cloudiness %
        pressure = round((data['daily'][i]['pressure'] * 0.75006375541921), 2)  # Atmospheric pressure, mmHg
        humidity = data['daily'][i]['humidity']  # Humidity, %
        wind_speed = data['daily'][i]['wind_speed']  # Wind speed.metre/sec
        x = (date, temp, pcp, clouds, pressure, humidity, wind_speed)
        weather_day_list.append(x)
        i += 1
    return weather_day_list  # date, temp, pcp, clouds, pressure, humidity, wind_speed
