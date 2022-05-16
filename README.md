Зміст завдання
-
    1. Використовуючи API сайту openweathermap.org, “витягнути” щоденний прогноз на 7 днів 
        для п’яти українських міст на Ваш вибір. Отримані дані помістити в sqlite базу даних. 
        Таблиці в базі даних повинні мати такі стовбці: 
        date, 
        temp(середня температура за добу в градусах цельсія), 
        pcp (опади за день), 
        clouds, 
        pressure, 
        humidity, 
        wind_speed.

    2. За допомогою flask-restfull побудувати rest-api з такими ресурсами та параметрами:
        /cities GET
            Return – список міст в базі даних в форматі json
        /mean GET
            Params: 
                value_type – одне з [temp, pcp, clouds, pressure, humidity, wind_speed]
                city – назва міста
            return – середнє значення вибраного параметру для вибраного міста в форматі json
        /records GET
                city – назва міста
                start_dt – початкова дата
                end_dt – кінцева дата
            return – значення всіх параметрів для вибраного міста впродовж вибраного терміну в форматі json
        /moving_mean
                value_type – одне з [temp, pcp, clouds, pressure, humidity, wind_speed]
                city – назва міста
            return – значення вибраного параметру перераховане за алгоритмом ковзного середнього (moving average) 
                для вибраного міста для всіх дат в форматі json

    3. Створити файл request_samples.py із запитами до побудованого rest api з попереднього завдання. 
        Для кожного  ресурсу повинно бути 2 приклади запитів. Форматувати вивід результатів запитів. 
