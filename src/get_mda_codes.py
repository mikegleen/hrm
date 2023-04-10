from bs4 import BeautifulSoup as Bs
import requests
import sys

url = 'https://collectionstrust.org.uk/mdacodes/'


def main():
    page = requests.get(url)
    # print(page.status_code)
    soup = Bs(page.text, 'html.parser')
    articles = soup.find_all('article')
    # print(f'{len(articles)=}')
    for article in articles:
        town = article.find('p', class_='mda-town').text
        if town != 'London':
            continue
        # print(f'{town=}')
        museum = article.h4.text
        print(f'{museum}')


if __name__ == '__main__':
    assert sys.version_info >= (3, 10)
    main()
