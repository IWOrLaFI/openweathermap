import sqlite3
import requests
import json
import datetime
import time
import os

start_time1 = datetime.datetime.now()

API_KEY = '8410a325b25bba0213254a8489ade0bd'
FILE_NAME_JSON = 'city.list.json'  # download file from http://bulk.openweathermap.org/sample/

city_list = ('Dnipro', 'Kyiv', 'Lviv', 'Oleksandriya')  # list of cities to search. The number of cities is unlimited.


def load_json():
    try:
        return json.load(open(FILE_NAME_JSON))
    except FileNotFoundError:
        return print("file not found.\n Download file http://bulk.openweathermap.org/sample/")


city_dict = load_json()


def ci_list(country):
    """
    this function creates a list of cities in the country, so you can find the city is spelled for test.
    example: city_list('UA')
    :param country:
    :return:
    """
    city_l = []
    i = 0
    for i in range(len(city_dict)):
        if city_dict[i]['country'] == country.upper():
            city_l.append(city_dict[i]['name'])
        i += 1
    return print(sorted(city_l))


def data_api(city_name):
    """
     Search for coordinates (lat , lon) of a city dictionary of cities and request to api
    :param city_name: city's name: str
    :return: json
    """
    i = 0
    for i in range(len(city_dict)):
        if city_dict[i]['name'] == city_name:
            lon = city_dict[i]['coord']['lon']
            lat = city_dict[i]['coord']['lat']
            url = f'https://api.openweathermap.org/' \
              f'data/2.5/onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
            return requests.get(url).json()
        i += 1
    return 0


def convert_dt(dt):
    """
    Convert date Unix to datatime 21 Dec 2021
    :param dt: date Unix
    :return: date dd mmm yyyy
    """
    return time.strftime("%d %b %Y", time.localtime(dt))


def weather_day(data):
    """
    Send the necessary information from json for the database in the required format
    :param data: data JSON
    :return: list : (date, temp, pcp, clouds, pressure, humidity, wind_speed),
    """
    weather_day_list = []
    i = 0
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


def f_rain(i, data):
    """
    Find volume rain in data json
    :param i: day number
    :param data: data json
    :return: Precipitation volume
    """
    try:
        rain = (data['daily'][i]['rain'])
        return rain
    except KeyError:
        return 0


def f_snow(i, data):
    """
     Find volume snow in data json
     :param i: day number
     :param data: data json
     :return: Precipitation volume
     """
    try:
        snow = data['daily'][i]['snow']
        return snow
    except KeyError:
        return 0


def f_temp(i, data):
    """
    Calculation of the average daily temperature.
    :param data: data json
    :param i: day number
    :return: average daily temperature in Celsius
    """
    temp_day = data['daily'][i]['temp']['day']
    temp_night = data['daily'][i]['temp']['night']
    temp_eve = data['daily'][i]['temp']['eve']
    temp_morn = data['daily'][i]['temp']['morn']
    temp = round(((temp_day + temp_night + temp_eve + temp_morn) / 4), 2)
    return temp


def delete_table():
    """
    Func delete the file db
    :return:
    """
    try:
        return os.remove('db/weather.db'), print('db delete')
    except FileNotFoundError:
        return


def create_table_sql(city_name):
    """
    Create empty table. Name Table it's City's name.
    :param city_name: city's name
    :return:
    """
    with sqlite3.connect('db/weather.db') as db:
        cursor = db.cursor()
        query = f""" CREATE TABLE IF NOT EXISTS {city_name}(
        data TEXT UNIQUE,
        temp REAL,
        pcp REAL,
        clouds INTEGER,
        pressure REAL,
        humidity REAL,
        wind_speed REAL) """
        cursor.execute(query)
        db.commit()
    return print(f'Table {city_name} is created')


def added_info(city_name, data):
    """
    Added info to table.
    :param city_name: city's name
    :param data: data info -> weather_day(data)
    :return:
    """
    with sqlite3.connect('db/weather.db') as db:
        cursor = db.cursor()
    query = f"""INSERT INTO {city_name} VALUES( ? , ? , ? , ? , ? , ?, ?); """
    cursor.executemany(query, weather_day(data))
    db.commit()
    return print(f'added info {city_name}')


def start():
    delete_table()
    i = 0
    for i in range(len(city_list)):
        data = data_api(city_list[i])
        if data == 0:
            print(f'{city_list[i]} is not found')
            continue
        weather_day(data)
        create_table_sql(city_list[i])
        added_info(city_list[i], data)
        i += 1
    return print('Info added to db')


if __name__ == '__main__':
    start()
    print(datetime.datetime.now() - start_time1)
