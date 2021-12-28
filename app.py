import sqlite3
from flask import Flask, jsonify, request

from sql_func import table_list_from_db, select_param_be_city

app = Flask(__name__)
file_db_name = 'db/weather.db'


@app.route('/cities', methods=['GET'])
def get_list():
    cities = table_list_from_db(file_db_name)
    return jsonify(cities)


@app.route('/mean', methods=['GET'])
def get_average_param():

    try:
        value_type = request.args['value_type']  # temp, pcp, clouds, pressure, humidity, wind_speed
        city = request.args['city']
        x = select_param_be_city(file_db_name, value_type, city)
        n = 0
        for i in range(len(x)):
            n += x[i][0]
        result = round((n / (i + 1)), 2)
        return jsonify(result)
    except sqlite3.OperationalError:
        result = 'wrong request, try : http://127.0.0.1:5000/mean?value_type=PARAMETR&city=NAME_CITY, ' \
                 'PARAMETR = temp or , pcp, clouds, pressure, humidity, wind_speed, ' \
                 'NAME_CITY = name city, ' \
                 'example: http://127.0.0.1:5000/mean?value_type=temp&city=dnipro'
        return jsonify(result)


if __name__ == '__main__':
    app.run()
