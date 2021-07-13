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

MONGO_DB = "mvideo"
MONGO_COLLECTION = "data"

from string import whitespace
CUSTOM_WHITESPACE = (whitespace + "\xa0").replace(" ", "")

def clear_string(s, whitespaces=CUSTOM_WHITESPACE):
    for space in whitespaces:
        s = s.replace(space, " ")
    return s

chrome_options = Options()
chrome_options.add_argument('start-maximized')
# chrome_options.add_argument('headless')


driver = webdriver.Chrome(options=chrome_options)

driver.get('https://mvideo.ru')

res = set()
done = False
with MongoClient("localhost", 27017) as client:
    db = client[MONGO_DB]
    data = db[MONGO_COLLECTION]
    while not done:
        els = driver.find_elements_by_xpath('//div[@data-block-id="Novinki"]//li[@class="gallery-list-item"]')
        if els:
            done = True
            for el in els:
                t = el.find_element_by_xpath(".//h3").get_attribute("title")
                if t not in res:
                    res.add(t)
                    r = {}
                    r["title"] = t
                    r["price"] = clear_string(el.find_element_by_class_name("fl-product-tile-price__sale").text)
                    done = False
                    data.update_one({"title": t}, {"$set": r}, upsert=True)
            el = driver.find_element_by_xpath('//div[@data-block-id="Novinki"]//a[contains(@class, "next-btn")]')
            #el = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-block-id="Novinki"]//a[contains(@class, "next-btn")]')))
            if el:
                el.click()
                time.sleep(1)
        else:
            done = True

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
