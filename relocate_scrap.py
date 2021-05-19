from bs4 import BeautifulSoup
import requests

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

for num in urls:
    page_num = '?page=' + str(num)
    new_url = url.replace('?page=1', page_num)
    print(new_url)
    response = requests.get(new_url)
    content = response.content
    soup = BeautifulSoup(content, 'lxml')
    cards = soup.find_all('div', class_='jobs-list__job')
    for inx, card in enumerate(cards, start=1):
        page = page_num
        title = card.find('div', class_='job__title').text.strip()
        more_info = 'https://relocate.me/' + card.find('a').get('href')
        title_info = title.split(" in ")
        vacancy = title_info[0]
        location = title_info[1]
        job_company = card.find('div', class_='job__company').text.strip()
        job_preview = card.find('p', class_='job__preview').text.strip()
        skills = card.find('div', class_='job__tags_wrapper').text.strip().replace('\n', ', ')
        # print(page)
        print(f'{inx}:\n Компания: {job_company}\n Вакансия: {title}\n Расположение: {location}\n Навыки: {skills}\n '
              f'Подробности:{more_info}')
