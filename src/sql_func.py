import os
import sqlite3
from datetime import datetime


def delete_table(file_db_name='db/weather.db'):
    """
    Func delete the file database
    :return: message 'db delete'
    """
    try:
        return os.remove(file_db_name), print('db delete')
    except FileNotFoundError:
        return


def create_table_sql(file_db_name, city_name):
    """
    Create empty table. Table's name  it's city's name.
    :param file_db_name:
    :param city_name: city's name
    :return: message 'Table city_name is created'
    """
    with sqlite3.connect(file_db_name) as db:
        cursor = db.cursor()
        query = f""" CREATE TABLE IF NOT EXISTS {city_name}(
        date TEXT UNIQUE,
        temp REAL,
        pcp REAL,
        clouds INTEGER,
        pressure REAL,
        humidity REAL,
        wind_speed REAL) """
        cursor.execute(query)
        db.commit()
    return print(f'Table {city_name} is created')


def added_info(file_db_name, city_name, data):
    """
    Added info to table.
    :param file_db_name:
    :param city_name: city's name
    :param data: data info -> weather_day(data)
    :return: message 'added info {city_name}'
    """
    with sqlite3.connect(file_db_name) as db:
        cursor = db.cursor()
    query = f"""INSERT INTO {city_name} VALUES( ? , ? , ? , ? , ? , ?, ?); """
    cursor.executemany(query, data)
    db.commit()
    return print(f'added info {city_name}')


def table_list_from_db(file_name):
    """
    Create table's list
    :return:
    """
    with sqlite3.connect(file_name) as db:
        cursor = db.cursor()
    query = 'SELECT name from sqlite_master where type= "table"'
    cursor.execute(query)
    db.commit()
    return (cursor.execute(query)).fetchall()


def select_param_be_city(file_name, value_type, city_name):
    """
    Select parameters in database and send it.
    :param file_name: name file database
    :param value_type: parameter
    :param city_name: city name
    :return: parameters
    """
    with sqlite3.connect(file_name) as db:
        cursor = db.cursor()
    query = f'SELECT date, {value_type} from {city_name} '
    result = cursor.execute(query).fetchall()
    db.commit()
    return result


def day_param_model(data):
    result = {'date': data[0],
              'temp': data[1],
              'pcp': data[2],
              'clouds': data[3],
              'pressure': data[4],
              'humidity': data[5],
              'wind_speed': data[6]
              }
    return result


def select_weather_date_city(file_name, city_name, start_dt, end_dt):
    """
    select date for find city weather
    :param file_name: name database
    :param city_name: city's name
    :param start_dt: first (start) date
    :param end_dt: lost (end) date
    :return: list parameters days
    """
    s_dt = datetime.strptime(start_dt, '%d-%m-%Y')
    e_dt = datetime.strptime(end_dt, '%d-%m-%Y')
    list_days = []
    with sqlite3.connect(file_name) as db:
        cursor = db.cursor()
        query = f"SELECT * FROM {city_name} "
        param = cursor.execute(query).fetchall()
        for i in range(len(param)):
            date = datetime.strptime(param[i][0], '%d-%m-%Y')
            if s_dt <= date <= e_dt:
                list_days.append(day_param_model(param[i]))
        db.commit()
    return list_days
