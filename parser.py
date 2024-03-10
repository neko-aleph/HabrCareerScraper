import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def parse(q: str) -> list[dict[str, str]]:
    vacancies: list[dict[str, str]] = []

    page = 1
    while True:
        result = parse_page(q, page)
        if not result:
            break
        vacancies.extend(result)
        page += 1

    return vacancies


def parse_page(q, page: int) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []

    ua = UserAgent()
    headers = {'User-Agent': ua.random}

    url = f'https://career.habr.com/vacancies?q={q}&type=all&page={page}'

    with requests.get(url, headers=headers) as response:
        if response.status_code != 200:
            raise ConnectionError

        soup = BeautifulSoup(response.text, 'html.parser')
        vacancies = soup.find_all('div', class_='vacancy-card')

        for vacancy in vacancies:
            date = vacancy.find('time').text

            link_relative = vacancy.find('a', class_='vacancy-card__icon-link')['href']
            link = f'https://career.habr.com{link_relative}'

            company = vacancy.find('div', class_='vacancy-card__company-title').text

            title = vacancy.find('div', class_='vacancy-card__title').text

            try:
                salary = vacancy.find('div', class_='vacancy-card__salary').text
            except AttributeError:
                salary = 'Не указана'

            try:
                meta = vacancy.find('div', class_='vacancy-card__meta').text
            except AttributeError:
                meta = 'Не указаны'

            try:
                skills = vacancy.find('div', class_='vacancy-card__skills').text
            except AttributeError:
                skills = 'Не указаны'

            try:
                company_rating = vacancy.find('div', class_='vacancy-card__company-rating').text
            except AttributeError:
                company_rating = 'Отсутствует'

            result.append({
                'title': title,
                'link': f'https://career.habr.com{link}',
                'company': company,
                'company_rating': company_rating,
                'salary': salary,
                'meta': meta,
                'skills': skills,
                'date': date
            })

    print(f'Страница {page} обработана')
    return result
