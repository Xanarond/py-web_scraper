from bs4 import BeautifulSoup
import requests
import json


def scrap_relocate():
    url = 'https://relocate.me/search/web-developer?page=1'
    link = requests.get(url)
    status = link.status_code
    content = link.content
    # print(status)
    soup = BeautifulSoup(content, 'lxml')
    pages = soup.find('span', class_='pages hide-for-small-only')
    last_url = pages.find_all('a')[-1].get_text()
    N = int(last_url)
    urls = list(range(1, N + 1))
    diction = []
    for num in urls:
        page_num = '?page=' + str(num)
        new_url = url.replace('?page=1', page_num)
        print(new_url)
        response = requests.get(new_url)
        content = response.content
        soup = BeautifulSoup(content, 'lxml')
        cards = soup.find_all('div', class_='jobs-list__job')
        page_str = 'Page:' + str(num)
        diction.append(page_str)
        for inx, card in enumerate(cards, start=1):
            page = page_num.replace('?page=', 'Page: ')
            title = card.find('div', class_='job__title').text.strip()
            more_info = 'https://relocate.me/' + card.find('a').get('href')
            title_info = title.replace('\n', ' ').split(" in ")
            vacancy = str(title_info[0])
            location = str(title_info[1])
            job_company = card.find('div', class_='job__company').text.strip()
            job_preview = card.find('p', class_='job__preview').text.strip()
            skills = card.find('div', class_='job__tags_wrapper').text.strip().replace('\n', ', ')
            about = {
                'vacancy': vacancy,
                'location': location,
                'job_company': job_company,
                'job_preview': job_preview,
                'skills': skills,
                'more_info': more_info
            }
            diction.append(about)
            # print(page)
            # print(f'{inx}:\n Компания: {job_company}\n Вакансия: {vacancy}\n Расположение: {location}\n Навыки: {skills}\n '
            #       f'Подробности: {more_info}')
    return diction


with open("relocate.json", "w", encoding='utf-8') as write_file:
    json.dump(scrap_relocate(), write_file, indent=4, ensure_ascii=False, separators=(',', ': '))
