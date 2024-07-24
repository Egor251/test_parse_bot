from bs4 import BeautifulSoup
import requests

import config


# Вспомогательная функция
def get_page_content(url: str):
    response = requests.get(url)
    return response.content


# Вспомогательная функция
def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


# Выделяем необходимые данные
def base_parse_lenta(soup) -> dict:
    links = []
    news = soup.find_all('a', class_='card-mini _topnews')
    for link in news:
        time = link.find('time').text.split(',')[0]
        title = link.find('h3', class_="card-mini__title").text
        href = config.site_for_parsing + link.get('href')
        if href:
            links.append({'time': time, 'title': title, 'link': href})
    return links


# Собираем всё вместе
def main_parse(url: str) -> list:
    links = []
    html_content = get_page_content(url)
    soup = parse_html(html_content)

    try:
        links = base_parse_lenta(soup)
    except Exception:
        print(f"Unsupported site: {config.site_for_parsing}")

    return links


if __name__ == '__main__':
    url = config.site_for_parsing
    html_content = get_page_content(url)
    soup = parse_html(html_content)

    print(base_parse_lenta(soup))

