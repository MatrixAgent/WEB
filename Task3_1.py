# Урок 3, задание 1
# реализовать функцию, записывающую собранные вакансии в созданную БД.

import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient

MONGO_DB = "vacancies"
MONGO_COLLECTION = "data"

def parse_salary(t):
    r1 = r2 = r3 = None
    if t[0] == 'от':
        r1 = int(t[1])
        r3 = t[2]
    elif t[0] == 'до':
        r2 = int(t[1])
        r3 = t[2]
    else:
        r1 = int(t[0])
        if t[1] == '\u2013': # символ '-' какой-то особый
            r2 = int(t[2])
            r3 = t[3]
        else:
            r3 = t[1]
    return (r1, r2, r3)

def load_vacancies(what, nPages):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    with MongoClient("localhost", 27017) as client:
        db = client[MONGO_DB]
        data = db[MONGO_COLLECTION]

        for _ in range(n):
            r = requests.get("https://syktyvkar.hh.ru/search/vacancy", headers=headers,
                             params={'text': v, 'page': str(n)})
            if r.status_code == 200:
                #    pprint(r.text)
                #    with open('html.html', 'w', encoding='utf-8') as f:
                #        f.write(r.text)

                soup = bs(r.text, 'html.parser')
                vl = soup.find_all(attrs={'class': "vacancy-serp-item"})
                if not vl:
                    break
                for e in vl:
                    d = {}
                    t = e.find(attrs={'data-qa': "vacancy-serp__vacancy-title"})
                    d['name'] = t.text
                    d['url1'] = t.attrs['href']
                    t = e.find(attrs={'data-qa': "vacancy-serp__vacancy-compensation"})
                    if t:
                        t = t.text.replace('\u202f', '').split()
                        d['salary_from'], d['salary_to'], d['salary_units'] = parse_salary(t)
                    d['url2'] = e.find(attrs={'data-qa': "vacancy-serp__vacancy-employer"}).attrs['href']
                    data.insert_one(d)
            else:
                print(f'Error: {r.status_code}')

v = input("Найти: ")
n = int(input("Кол-во страниц сайта: "))

load_vacancies(v, n)