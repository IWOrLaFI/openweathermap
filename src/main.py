from jsons_func import load_json, find_coord_city, weather_day
from request_to_api_openweather import request_to_api
from sql_func import delete_table, create_table_sql, added_info


FILE_NAME_JSON = '../src/city.list.json'  # download file from http://bulk.openweathermap.org/sample/
file_db_name = '../src/db/weather.db'
city_list = ('Dnipro', 'Kyiv', 'Lviv', 'Oleksandriya', 'Odessa')
# list of cities to search. The number of cities is unlimited.

city_dict = load_json(FILE_NAME_JSON, 'Download file http://bulk.openweathermap.org/sample/')


def start():
    delete_table(file_db_name)
    for i in range(len(city_list)):
        lat, lon = (find_coord_city(city_dict, city_list[i]))
        if lat == lon == 404:
            print(f'{city_list[i]} is not found')
            continue
        data = request_to_api(lat, lon)
        create_table_sql(file_db_name, city_list[i])
        added_info(file_db_name, city_list[i], weather_day(data))
        i += 1
    return print('Info added to db')


if __name__ == '__main__':
    start()
