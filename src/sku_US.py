from bs4 import BeautifulSoup
import requests
from getuseragent import UserAgent
import pandas as pd
import csv

csv_file = open('price_output.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['SKU', 'Price'])

data = pd.read_csv('Scraping.csv')
sku_list = data['SKU'].tolist()
sku_list = [sku for sku in sku_list if str(sku) != 'nan']
price_list = []
product_names_list = []
cdw_parts_list = []
records = []

for sku in sku_list:
    url = f'https://www.cdw.com/search/?key={sku}'
    myuseragent = UserAgent("all", requestsPrefix=True).Random()
    session = requests.Session()
    source = session.get(url, headers=myuseragent, allow_redirects=False).text
    soup = BeautifulSoup(source, 'lxml')

    try:
        price_url_content = soup.find('div', class_='container').script.text.split('"')[1]
        generic_url = 'https://www.cdw.com'
        price_url = generic_url + (price_url_content)

        source = session.get(price_url, headers=myuseragent, allow_redirects=False).text
        soup = BeautifulSoup(source, 'lxml')
        price = soup.find('span', class_='price-type-selected').text
        price_list.append(price)
        product_name = soup.find('h1', class_='fn').text
        product_names_list.append(product_name)
        cdw_part = soup.find('span', class_='edc').text
        cdw_parts_list.append(cdw_part)

        print(sku, price, product_name, cdw_part)
        print()
        csv_writer.writerow([sku, price])

    except Exception as e:
        price = "SKU Not found"
        price_list.append(price)
        product_name = "Not applicable"
        product_names_list.append(product_name)
        cdw_part = "Not applicable"
        cdw_parts_list.append(cdw_part)
        print(sku, "SKU Not found", "Not applicable", "Not applicable")
        print()
        csv_writer.writerow([sku, price])

