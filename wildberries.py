import json
import requests
import csv


def receive(url):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'DNT': '1',
        'Origin': 'https://www.wildberries.ru',
        'Referer': 'https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=popular&search=pampers+6+%D1%82%D1%80%D1%83%D1%81%D0%B8%D0%BA%D0%B8&xsubject=814&fbrand=6398&f54383=61656&f63494=70403%3B70404',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0',
        'sec-ch-ua': '"Not A(Brand";v="99", "Opera";v="107", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print('Data received. Response status: ', response.status_code)
        return data
    else:
        print('Data receiving error. Response status: ', response.status_code)


def parse(data):
    result = []
    data = data.get('data').get('products')
    for product in data:
        name = product.get('name')
        price = product.get('priceU') // 100
        price_sale = product.get('salePriceU') // 100
        try:
            string = name.replace(',', '').split()
            quantity = int(string[string.index('шт') - 1])
            price_one = round(price_sale / quantity, 2)
        except (Exception,):
            price_one = '---'
        result.append([name, price_one, price_sale, price])
    with open('products.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Название', 'Цена за штуку', 'Цена со скидкой', 'Цена без скидки'])
        writer.writerows(result)
    print('CSV file was written.')


if __name__ == '__main__':
    url_address = 'https://search.wb.ru/exactmatch/ru/common/v4/search?ab_testing=false&appType=1&curr=rub&dest=-5817295&f54383=61656&f63494=70403;70404&fbrand=6398&page=1&query=pampers%206%20%D1%82%D1%80%D1%83%D1%81%D0%B8%D0%BA%D0%B8&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false&xsubject=814'
    req_data = receive(url_address)
    if req_data:
        parse(req_data)
    else:
        print('Data from Wildberries not received.')
