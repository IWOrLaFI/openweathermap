import requests

print('/cities GET\n',
      requests.get('http://127.0.0.1:5000/cities').text)
print('/mean GET  (value_type=temp, city=dnipro)\n',
      requests.get('http://127.0.0.1:5000/mean?value_type=temp&city=dnipro').text)
print('/mean GET  (value_type=pressure, city=lviv)\n',
      requests.get('http://127.0.0.1:5000/mean?value_type=pressure&city=lviv').text)
print('/records GET  (city=dnipro, start_dt=28-12-2021, end_dt=01-01-2022)\n',
      requests.get('http://127.0.0.1:5000/records?city=dnipro&start_dt=28-12-2021&end_dt=01-01-2022').text)
print('/records GET (city=Oleksandriya, start_dt=30-12-2021, end_dt=31-12-2021)\n',
      requests.get('http://127.0.0.1:5000/records?city=Oleksandriya&start_dt=30-12-2021&end_dt=31-12-2021').text)
