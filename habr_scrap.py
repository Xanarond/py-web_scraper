from bs4 import BeautifulSoup
import requests
import json


def habr_scrap():
    url = 'https://career.habr.com/vacancies?page=1'
    link = requests.get(url)
    # print(link.status_code)
    html = link.content
    soup = BeautifulSoup(html, 'lxml')
    cards = soup.find_all('div', class_='vacancy-card')
    section = soup.find('div', class_='paginator')
    href = section.find_all('a')

    page_num = []
    for num in href:
        a = num.get_text()
        page_num.append(a)

    bad_chars = ['Next ›', '‹ Prev']
    ready_set = list(set(page_num))
    test_string = filter(lambda w: w not in bad_chars, ready_set)
    max_href = max(list(test_string))
    N = int(max_href)
    urls = list(range(1, N + 1))
    direct = []
    for num in urls:
        page_num = '?page=' + str(num)
        new_url = url.replace('?page=1', page_num)
        print(new_url)
        response = requests.get(new_url)
        content = response.content
        soup = BeautifulSoup(content, 'lxml')
        cards = soup.find_all('div', class_='vacancy-card')
        page_str = 'Page:' + str(num)
        direct.append(page_str)
        for section in cards:
            date = section.find('div', class_='vacancy-card__date').text
            company = section.find('div', class_='vacancy-card__company').text
            title = section.find('div', class_='vacancy-card__title').text
            location = section.find('div', class_='vacancy-card__meta').text.replace(' · ', ', ')
            salary = section.find('div', class_='vacancy-card__salary').text
            skills = section.find('div', class_='vacancy-card__skills').text.replace(' · ', ', ')
            more_info = 'https://career.habr.com/' + section.find('a', class_='vacancy-card__icon-link').get('href')
            # print(
            #     f' Компания: {company}\n Вакансия: {title}\n Расположение: {location}\n Навыки: {skills}\n ЗП: {salary}\n Подробности: {more_info}\n ')
            about = {
                'date': date,
                'company': company,
                'title': title,
                'location': location,
                'salary': salary,
                'skills': skills,
                'more_info': more_info
            }
            direct.append(about)
    return direct


with open("habr.json", "w", encoding='utf-8') as write_file:
    json.dump(habr_scrap(), write_file, indent=4, ensure_ascii=False, separators=(',', ': '))
