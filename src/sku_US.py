from bs4 import BeautifulSoup
import requests
from getuseragent import UserAgent
import pandas as pd
import csv
import time

csv_file = open('Results_US.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['SKU', 'Price', 'Product_Name', 'CDW_Part'])

data = pd.read_csv('input_US.csv')
sku_list = data['SKU'].tolist()
sku_list = [sku for sku in sku_list if str(sku) != 'nan']
price_list = []
product_names_list = []
cdw_parts_list = []

myuseragent = UserAgent("all", requestsPrefix=True).Random()
session = requests.Session()
time.sleep(5)

for sku in sku_list:
    url = f'https://www.cdw.com/search/?key={sku}'
    source = session.get(url, headers=myuseragent, allow_redirects=False).text
    soup = BeautifulSoup(source, 'lxml')

    try:
        price_url_content = soup.find('div', class_='container').script.text.split('"')[1]
        generic_url = 'https://www.cdw.com'
        price_url = generic_url + (price_url_content)
        source = session.get(price_url, headers=myuseragent, allow_redirects=False).text
        soup = BeautifulSoup(source, 'lxml')
        price = soup.find('span', class_='price-type-selected').text
        product_name = soup.find('h1', class_='fn').text
        cdw_part = soup.find('span', class_='edc').text

    except Exception as e:
        try:
            search_list = soup.find_all('div', class_='search-result coupon-check')
            sku_found = False
            for product in search_list:
                mfg = product.find('span', class_='mfg-code').text
                mfg = mfg[6:]
                if sku == mfg:
                    sku_found = True
                    price = product.find('div', class_='price-type-price').text
                    product_name = product.find('a', class_='search-result-product-url').text
                    cdw_part = product.find('span', class_='cdw-code').text
                    cdw_part = cdw_part[6:]
            if not sku_found:
                price = "SKU exact match not found"
                product_name = "Not applicable"
                cdw_part = "Not applicable"

        except Exception as e:
            price = "SKU exact match not found"
            product_name = "Not applicable"
            cdw_part = "Not applicable"

    price_list.append(price)
    product_names_list.append(product_name)
    cdw_parts_list.append(cdw_part)
    print(sku, price, product_name, cdw_part)
    print()
    csv_writer.writerow([sku, price, product_name, cdw_part])

csv_file.close()
