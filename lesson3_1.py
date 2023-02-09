
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
from time import sleep
import json


def job_scraping(*args):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'}
    try:
        for website in list(args):
            # в зависимости от сайта:
            if website == 'HH':
                params = {'page': 0, 'hhtmFrom': 'vacancy_search_catalog'}
                job_search = 'prodavets-konsultant'
                site_name = 'https://hh.ru/vacancies/'
                url, name_file = f'{site_name}{job_search}', 'HH_vacancies.json'
            if website == 'SJ':
                params = {'page': 1}
                site_name = 'https://www.superjob.ru/'
                job_search = 'prodavec-konsultant.html'
                url, name_file = f'{site_name}vakansii/{job_search}', 'SJ_vacancies.json'
            if website == 'RR':
                params = {'sort': 'relevance', 'specialization_ids': '2195', 'page': 1}
                job_search = 'vacancy/'
                site_name = 'https://www.rabota.ru/'
                url, name_file = f'{site_name}{job_search}', 'RR_vacancies.json'

            session = requests.Session()
            response = session.get(url, headers=headers, params=params)
            json_vacancies, num, start_node, adding_a_path = {}, 0, list(args), site_name

            while len(start_node) > 10:
                print(f"Обработка страницы № {params['page']}")
                dom = bs(response.text, 'html.parser')
                if website == 'HH':
                    start_node = dom.find_all('div', {'class': ['vacancy-serp-item-body__main-info']})
                if website == 'SJ':
                    start_node = dom.find_all('div', {'class': '_2lp1U _2J-3z _3B5DQ'})
                if website == 'RR':
                    start_node = dom.find_all('header', {'class': 'vacancy-preview-card__header'})

                for vacancy in start_node:
                    num += 1
                    minimal_salary, maximal_salary, currency_name, currency_name_letter = None, None, None, []
                    if website == 'HH':
                        vacansy_text_and_link = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
                        vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
                        adding_a_path = 'h'
                    if website == 'SJ':
                        vacansy_text_and_link = vacancy.find('a', {'class': 'YrERR'})
                        vacancy_salary = vacancy.find('span', {'class': '_2eYAG'})
                    if website == 'RR':
                        vacansy_text_and_link = vacancy.find('a', {'class': 'vacancy-preview-card__title_border'})
                        vacancy_salary = \
                        vacancy.find('div', {'class': 'vacancy-preview-card__salary'}).findChildren(recursive=False)[0]
                    # здесь обрабатываем строчку с зарплатой, превращая цифры в int, а валюту в str
                    if vacancy_salary:
                        string_salary = vacancy_salary.text
                        for letter in string_salary[::-1]:
                            if letter.isdigit():
                                break
                            currency_name_letter.append(letter)
                        currency_name = ''.join(currency_name_letter[::-1])
                        currency_name = currency_name.replace('\xa0', '')
                        regular_salary = re.findall('(\d+)', string_salary)
                        if len(regular_salary) == 2:
                            if not string_salary.find('до'):
                                maximal_salary = int(regular_salary[0] + regular_salary[1])
                            else:
                                minimal_salary = int(regular_salary[0] + regular_salary[1])
                        elif len(regular_salary) == 0:
                            pass
                        else:
                            minimal_salary = int(regular_salary[0] + regular_salary[1])
                            maximal_salary = int(regular_salary[2] + regular_salary[3])
                    # собираем словари
                    json_vacancies[num] = {
                        'название': vacansy_text_and_link.text.replace('\n', '').strip(),
                        'ссылка': adding_a_path + vacansy_text_and_link['href'][1:],
                        'зарплата от': minimal_salary,
                        'зарплата до': maximal_salary,
                        'валюта': currency_name,
                        'сайт': site_name}

                response = session.get(url, headers=headers, params=params)
                params['page'] += 1
                sleep(5)

            with open(name_file, 'w', encoding='UTF-8') as f:
                json.dump(json_vacancies, f)
                print(f'{name_file} создан! сохранено вакансий {num} шт.')
    except:
        print("эй, переданы не те аргументы, надо эти: 'HH', 'SJ', 'RR'")

job_scraping('HH', 'SJ', 'RR')