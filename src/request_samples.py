import requests


list_requests = [
    ['/cities GET',
     'http://127.0.0.1:5000/cities'],

    ['/mean GET  (value_type=temp, city=dnipro)',
     'http://127.0.0.1:5000/mean?value_type=temp&city=dnipro'],

    ['/mean GET  (value_type=pressure, city=lviv)',
     'http://127.0.0.1:5000/mean?value_type=pressure&city=lviv'],

    ['/records GET  (city=dnipro, start_dt=08-01-2022, end_dt=12-01-2022)',
     'http://127.0.0.1:5000/records?city=dnipro&start_dt=08-01-2022&end_dt=12-01-2022'],

    ['/records GET (city=Oleksandriya, start_dt=10-01-2022, end_dt=11-01-2022)',
     'http://127.0.0.1:5000/records?city=Oleksandriya&start_dt=10-01-2022&end_dt=11-01-2022'],

    ['/moving_mean GET (value_type=pressure, city=lviv)',
     'http://127.0.0.1:5000/moving_mean?value_type=pressure&city=lviv'],

    ['/moving_mean GET (value_type=temp, city=dnipro)',
     'http://127.0.0.1:5000/moving_mean?value_type=temp&city=dnipro']
]


def req_func():
    for i in range(len(list_requests)):
        print(list_requests[i][0])
        print(requests.get(list_requests[i][1]).text)
    return print('done')


req_func()
