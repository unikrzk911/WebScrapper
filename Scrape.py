from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_product_link(page):
    url = f'https://www.sastodeal.com/catalogsearch/result/index/?p={page}&q=headphone'
    links = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    products = soup.find_all('li', class_='item product product-item')
    for item in products:
        links.append(item.find('a', class_='product-item-link').get('href'))
    return links


def get_product_detail(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find('h1', class_='page-title').text
    price = soup.find('span', class_='price').text
    seller = soup.find('span', class_='wk-block-title-css').text
    availability = soup.find('span', class_='stockqty').span.text
    product = {
        'title': title,
        'price': price,
        'seller': seller,
        'availability': availability
    }
    return product


def main():
    results = []
    for i in range(1, 9):
        print('Getting page ', i)
        urls = get_product_link(i)
        for url in urls:
            results.append(get_product_detail(url))
        print('Total results: ', len(results))
        data = pd.DataFrame(results)
        data.to_csv('data.csv')


if __name__ == '__main__':
    main()
