import sqlite3
from flask import Flask, jsonify, request

from sql_func import table_list_from_db, select_param_be_city, select_weather_date_city

app = Flask(__name__)
file_db_name = '../src/db/weather.db'


@app.route('/cities', methods=['GET'])  # http://127.0.0.1:5000/cities
def get_list():
    """
    :return: список міст в базі даних в форматі json.
    """
    cities = table_list_from_db(file_db_name)
    return jsonify(cities)


@app.route('/mean', methods=['GET'])  # http://127.0.0.1:5000/mean?value_type=temp&city=dnipro
def get_average_param():
    """
    :param: value_type – одне з [temp, pcp, clouds, pressure, humidity, wind_speed]
    :param: city – назва міста
    :return: середнє значення вибраного параметру для вибраного міста в форматі json
    """
    try:
        value_type = request.args['value_type']  # temp, pcp, clouds, pressure, humidity, wind_speed
        city = request.args['city']
        x = select_param_be_city(file_db_name, value_type, city)
        n = 0
        i = 0
        for i in range(len(x)):
            n += x[i][1]
        result = round((n / (i + 1)), 2)
        return jsonify(result)
    except sqlite3.OperationalError:
        result = 'wrong request, try : http://127.0.0.1:5000/mean?value_type=PARAMETR&city=NAME_CITY, ' \
                 'PARAMETR = temp or , pcp, clouds, pressure, humidity, wind_speed, ' \
                 'NAME_CITY = name city, ' \
                 'example: http://127.0.0.1:5000/mean?value_type=temp&city=dnipro'
        return jsonify(result)


@app.route('/records', methods=['GET'])
def get_records_param():  # http://127.0.0.1:5000/records?city=dnipro&start_dt=28-12-2021&end_dt=01-01-2022
    """
    :param: city – назва міста
    :param: start_dt – початкова дата
    :param: end_dt – кінцева дата
    :return: значення всіх параметрів для вибраного міста впродовж вибраного терміну в форматі json
    """
    city = request.args['city']
    start_dt = request.args['start_dt']
    end_dt = request.args['end_dt']
    result = select_weather_date_city(file_db_name, city, start_dt, end_dt)
    return jsonify(result)


@app.route('/moving_mean', methods=['GET'])  # http://127.0.0.1:5000/mean?value_type=temp&city=dnipro
def get_moving_mean():
    """
    :param: value_type – одне з [temp, pcp, clouds, pressure, humidity, wind_speed]
    :param: city – назва міста
    :return: начення вибраного параметру перераховане за алгоритмом ковзного середнього (moving average)
            для вибраного міста для всіх дат в форматі json
    """
    param_sma = {}
    try:
        value_type = request.args['value_type']  # temp, pcp, clouds, pressure, humidity, wind_speed
        city = request.args['city']
        x = select_param_be_city(file_db_name, value_type, city)
        for i in range(len(x)-2):
            t = {(x[i+1][0]): round(((x[i-1][1]) + (x[i][1]) + (x[i+1][1]))/3, 2)}
            param_sma.update(t)
        return jsonify(param_sma)
    except sqlite3.OperationalError:
        result = 'wrong request, try : http://127.0.0.1:5000/moving_mean?value_type=PARAMETR&city=NAME_CITY, ' \
                 'PARAMETR = temp or , pcp, clouds, pressure, humidity, wind_speed, ' \
                 'NAME_CITY = name city, ' \
                 'example: http://127.0.0.1:5000/moving_mean?value_type=temp&city=dnipro'
        return jsonify(result)


if __name__ == '__main__':
    app.run()
