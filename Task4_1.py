# Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.news

import requests
from pprint import pprint
from datetime import datetime
from lxml.html import fromstring
#from datetime import datetime

#from fp.fp import FreeProxy
from string import whitespace
CUSTOM_WHITESPACE = (whitespace + "\xa0").replace(" ", "")
# t = datetime.today().date()
# t.strftime("%Y-%m-%d")
#
# "19:25 вчера"
#proxies = FreeProxy().get_proxy_list()

def parse_time(s):
    date_str = s.split('+')[0]
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S').strftime('%d.%m.%Y')

def clear_string(s, whitespaces=CUSTOM_WHITESPACE):
    for space in whitespaces:
        s = s.replace(space, " ")
    return s
# info['price'] = list(map(
#     clear_string,
#     item.xpath('.//span[contains(@class, "_price")]//text()')
# ))

def get_dom(url):
    response = requests.get(url, headers=headers) #, proxies={"http": proxies[0]})
    return fromstring(response.text)

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
                  " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}

# mail.ru
dom = get_dom("https://news.mail.ru")
items = dom.xpath('//a[@class="list__text"]')
items += dom.xpath('//a[@class="photo"]')
l = []
for item in items:
    info = {}
    info['title'] = clear_string(item.xpath('./text()')[0])
    info['url'] = item.xpath('./@href')[0]

    dom = get_dom(info['url'])
    info['time'] = parse_time(dom.xpath('//span[contains(@class, "note__text")]/@datetime')[0])
    info['source'] = clear_string(dom.xpath('//span[@class="note"]//span[@class="link__text"]/text()')[0])

    l.append(info)

# lenta.ru
dom = get_dom("https://lenta.ru")
items = dom.xpath('//div[@class="first-item" or @class="item"]')
for item in items:
    info = {}
    info['title'] = clear_string(item.xpath('.//a/text()')[0])
    info['url'] = item.xpath('.//a/@href')[0]
    if 'https' not in info['url']:
        info['url'] = 'https://lenta.ru' + info['url']

    dom = get_dom(info['url'])
    t = dom.xpath('//time[@pubdate]/@datetime')
    if t:
        info['time'] = parse_time(t[0])
    else:
        info['time'] = dom.xpath('//span[contains(@class, "formattedDate")]/text()')[0]
        info['timestamp'] = datetime.now()
    src = dom.xpath('//a[@class="source"]/text()')
    if src:
        info['source'] = src[0]

    l.append(info)

# Яндекс.Новости
dom = get_dom("https://yandex.ru/news")
items = dom.xpath('//article')
for item in items:
    info = {}
    info['title'] = clear_string(item.xpath('.//h2[@class="mg-card__title"]/text()')[0])
    info['url'] = item.xpath('.//a[@class="mg-card__link"]/@href')[0]
    info['source'] = item.xpath('.//a[@class="mg-card__source-link"]/text()')[0]
    info['when'] = item.xpath('.//span[@class="mg-card-source__time"]/text()')[0]
    info['timestamp'] = datetime.now()

    l.append(info)

pprint(l)

