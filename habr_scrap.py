from bs4 import BeautifulSoup
import requests


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


for num in urls:
    page_num = '?page=' + str(num)
    new_url = url.replace('?page=1', page_num)
    print(new_url)
    response = requests.get(new_url)
    content = response.content
    soup = BeautifulSoup(content, 'lxml')
    cards = soup.find_all('div', class_='vacancy-card')
    for section in cards:
        date = section.find('div', class_='vacancy-card__company').text
        company = section.find('div', class_='vacancy-card__company').text
        title = section.find('div', class_='vacancy-card__title').text
        location = section.find('div', class_='vacancy-card__meta').text.replace(' · ', ', ')
        salary = section.find('div', class_='vacancy-card__salary').text
        skills = section.find('div', class_='vacancy-card__skills').text.replace(' · ', ', ')
        print(f' Компания: {company}\n Вакансия: {title}\n Расположение: {location}\n Навыки: {skills}\n ЗП: {salary}\n ')
