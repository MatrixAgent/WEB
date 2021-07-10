# Задание 2
# Зарегистрироваться на https://openweathermap.org/api и написать функцию, которая получает погоду в данный момент для
# города, название которого получается через input. https://openweathermap.org/current

import os
from dotenv import load_dotenv
import requests
from pprint import pprint

load_dotenv()
key = os.getenv('KEY', None)
print(key)

def cur_weather():
    c = input('Город: ')
    params = {
        'q': c,
        'units': 'metric',
        'appid': key
    }
    repos = requests.get('http://api.openweathermap.org/data/2.5/weather', params = params)
    if repos.status_code == 200:
        pprint(repos.json())
    else:
        print('Error!')

cur_weather()
