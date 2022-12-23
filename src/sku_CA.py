from bs4 import BeautifulSoup, SoupStrainer
import requests
from getuseragent import UserAgent
import pandas as pd
import csv
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

csv_file = open('results_CA.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['SKU', 'Price'])

data = pd.read_csv('input_file_CA.csv')
sku_list = data['SKU'].tolist()
sku_list = [sku for sku in sku_list if str(sku) != 'nan']

product_names_list = []
cdw_parts_list = []
min_price_list = []
url3_list = []
records = []
price_list = []

for sku in sku_list:
    url_1 = f'https://www.cdw.ca/search/?key={sku}'
    myuseragent = UserAgent("all", requestsPrefix=True).Random()
    session = requests.Session()
    source = session.get(url_1, headers=myuseragent, allow_redirects=False).text
    soup = BeautifulSoup(source, 'lxml')

    try:
        price_url_content = soup.find('div', class_='container').script.text.split('"')[1]
        generic_url = 'https://www.cdw.ca'
        price_url = generic_url + (price_url_content)

        source = session.get(price_url, headers=myuseragent, allow_redirects=False).text
        soup = BeautifulSoup(source, 'lxml')
        price_1 = soup.find('span', class_='price-type-selected').text
        price_list.append(price_1)
        product_name = soup.find('h1', class_='fn').text
        product_names_list.append(product_name)
        cdw_part = soup.find('span', class_='edc').text
        cdw_parts_list.append(cdw_part)

        print(sku, price_1, product_name, cdw_part)
        print()
        csv_writer.writerow([sku, price_1])

    except Exception as e:
        price_1 = "SKU Not found"
        price_list.append(price_1)
        product_name = "Not applicable"
        product_names_list.append(product_name)
        cdw_part = "Not applicable"
        cdw_parts_list.append(cdw_part)
        print(sku, "SKU Not found", "Not applicable", "Not applicable")
        print()
        csv_writer.writerow([sku, price_1])

csv_file.close()