# Задание 1
# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json; написать функцию, возвращающую список репозиториев.

import os
from dotenv import load_dotenv
import requests
from pprint import pprint

load_dotenv()
token = os.getenv('TOKEN', None)
#token = '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'
print(token)

def req_repos(user):
    repos = requests.get('https://api.github.com/users/' + user + '/repos', auth=('', token))
    if repos.status_code == 200:
        return repos
    else:
        print('Error!')
        return None

def get_repos(user):
    repos = req_repos(user)
    if repos is not None:
        l = []
        for r in repos.json():
            l.append(r['html_url'])
        return l
    else:
        return None

user = input('User: ')
repos = req_repos(user)
if repos is not None:
    pprint(repos.json())
    with open('repos.json', 'w') as f:
        f.write(repos.text)

repos = get_repos(user)
if repos is not None:
    pprint(repos)
