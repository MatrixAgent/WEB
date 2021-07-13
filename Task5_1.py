from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from pymongo import MongoClient

SCROLL_PAUSE_TIME = 0.5
COUNT = 4 # Кол-во попыток сделать PAGE_DOWN без изменения содержимого после которого сбор завершается

MONGO_DB = "mail"
MONGO_COLLECTION = "data"

chrome_options = Options()
chrome_options.add_argument('start-maximized')
# chrome_options.add_argument('headless')


driver = webdriver.Chrome(options=chrome_options)

driver.get('https://mail.ru/')

el = driver.find_element_by_class_name("email-input")
el.send_keys("study.ai_172")
el.send_keys(Keys.ENTER)
time.sleep(1.5)
el = driver.find_element_by_class_name("password-input")
el.send_keys("NextPassword172!")
el.send_keys(Keys.ENTER)

time.sleep(5)

res_prev = set()
res = set()
count = COUNT
limit = 5 # Ограничение чтобы не ждать пока не проскроллим весь ящик
while count > 0:
    if len(res) >= limit:
        break
    #els = WebDriverWait(driver, 5).until(EC.element_to_be_selected((By.CLASS_NAME, "llc")))
    els = driver.find_elements_by_class_name("llc")
    if els:
        res.update([el.get_attribute('href') for el in els])
        if len(res_prev) != len(res):
            res_prev = res.copy()
            count = COUNT
        else:
            count -= 1
        els[0].send_keys(Keys.PAGE_DOWN)
        time.sleep(SCROLL_PAUSE_TIME)
    else:
        break

with MongoClient("localhost", 27017) as client:
    db = client[MONGO_DB]
    data = db[MONGO_COLLECTION]
    while (res):
        l = res.pop()
        driver.get(l)
        r = {}
        el = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[@class='letter-contact']")))
    #        el = driver.find_element_by_class_name("letter-contact")
        r["url"] = l
        r["sender_address"] = el.get_attribute("title")
        r["sender_name"] = el.text
        r["subject"] = driver.find_element_by_class_name("thread__subject").text
        r["time"] = driver.find_element_by_class_name("letter__date").text
        r["body"] = driver.find_element_by_class_name("letter-body__body-content").text
        print(r)
        data.update_one({"url": l}, {"$set": r}, upsert=True) # Делаем update в виду того, что время имеет вид "Вчера ..."

print("Done!")
#
# buttonsPanel = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='_8v6CFFrbuZ']")))
#
# button48 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "vLDMfabyVq")))
# button48.click()
#
# button12 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Показывать по 12']")))
# button12.click()


#
# time.sleep(10)
#
# hpCheck = driver.find_element_by_xpath("//input[@name='Производитель HP']")
# hpCheck.click()
#
# lenovoCheck = driver.find_element_by_xpath("//input[@name='Производитель Lenovo']")
# hpCheck.click()
#
# # goods = driver.find_elements_by_class_name('sku-card-small-container')
# # for good in goods:
# #     print(good.find_element_by_class_name('sku-card-small__title').text)
# #     print(good.find_element_by_class_name('sku-price__integer').text)
