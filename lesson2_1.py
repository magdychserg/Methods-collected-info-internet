import requests
from pprint import pprint
from lxml import html
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'}

url = 'https://lenta.ru/'

session = requests.Session()
response = session.get(url, headers=headers)

print(response.ok)
dom_lenta = html.fromstring(response.text)


def lenta_news_scraping(a=None, b=None):
    url = 'https://lenta.ru/'
    mini_news = dom_lenta.xpath("//div[@class='card-mini__text']")
    card_big = dom_lenta.xpath("//a[contains(@class, 'card-big')]")
    lenta_list = {}

    def filling_json(href, link, time, news_category, n, name_news):
        for x in href:
            if x.find('http'):
                x = url[:-1] + x
            link = x
            lenta_list[f'{n + 1} {news_category}'] = {
                'title': name_news,
                'time': time,
                'link': link}

    def regular_news():
        for n, i in enumerate(mini_news):
            news_category = 'regular_news'
            link = None
            name_news = i.xpath("./span[@class='card-mini__title']/text()")[0]
            time = ''.join(i.xpath("./div[@class='card-mini__info']/time/text()"))
            href = i.xpath("./../@href")
            if not time:
                news_category = 'prime_news'
            filling_json(href, link, time, news_category, n, name_news)

    def card_big_news():
        news_category = 'card_big_news'
        for n, i in enumerate(card_big):
            link = None
            name_news = ''.join(i.xpath("./div[2]/h3/text()"))
            time = ''.join(i.xpath("./div[3]/time/text()"))
            href = i.xpath("./@href")
            filling_json(href, link, time, news_category, n, name_news)

        big_news = dom_lenta.xpath("//a[contains(@class, 'card-feature')]/div[2]/h3/text()")[0]
        big_text = ''.join(dom_lenta.xpath("//span[contains(@class, 'card-feature__description')]/text()"))
        big_href = dom_lenta.xpath("//a[contains(@class, 'card-feature')]/@href")
        big_href = url[:-1] + big_href[0]
        lenta_list[f'1 news with photo'] = {
            'title': big_news + big_text,
            'time': '',
            'link': big_href}

    if a:
        regular_news()
    if b:
        card_big_news()

    with open('lenta_news.json', 'w', encoding='UTF-8') as f:
        json.dump(lenta_list, f)
        print('файл "lenta_news.json" создан!')

    return lenta_list

lenta = lenta_news_scraping()
items = list(lenta.items())
pprint(items[0])
pprint(items[-1])
pprint(items[105])
