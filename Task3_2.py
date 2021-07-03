# Урок 3
# Задание 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.

from pymongo import MongoClient

MONGO_DB = "vacancies"
MONGO_COLLECTION = "data"

def show_with_salary(s):
    with MongoClient("localhost", 27017) as client:
        db = client[MONGO_DB]
        data = db[MONGO_COLLECTION]

        r = data.find({ '$or': [{'salary_from': {'$gt': s}}, {'salary_to': {'$gt': s}}]})
        for e in r:
            s = f'от {e["salary_from"]} до {e["salary_to"]}' \
                if e.get("salary_from") and e.get("salary_to") \
                else str(e["salary_from"]) if e.get("salary_from") \
                else f'до {e["salary_to"]}'
            print(e['name'] + ' - ' + s)

show_with_salary(150000)
