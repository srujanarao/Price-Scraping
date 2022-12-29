from bs4 import BeautifulSoup
import requests
from getuseragent import UserAgent
import pandas as pd
import csv
import time
import sys
from datetime import datetime
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Generate Results in a csv file appended with current time
current_datetime = datetime.now()
str_current_datetime = str(current_datetime)
results_file = 'Results_US_' + str_current_datetime + '.csv'
csv_file = open(results_file, 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['SKU', 'Price', 'Product_Name', 'CDW_Part'])

# Check for input file in argument list
try:
    input_file = sys.argv[1]
except:
    print("Input filename missing from the argument list")
    sys.exit()

# Prepare SKU's list
data = pd.read_csv(input_file)
sku_list = data['SKU'].tolist()
sku_list = [sku for sku in sku_list if str(sku) != 'nan']
price_list = []
product_names_list = []
cdw_parts_list = []
generic_url = 'https://www.cdw.com'

myuseragent = UserAgent("all", requestsPrefix=True).Random()
session = requests.Session()
time.sleep(5)

for sku in sku_list:
    url = f'https://www.cdw.com/search/?key={sku}'
    source = session.get(url, headers=myuseragent, allow_redirects=False).text
    soup = BeautifulSoup(source, 'lxml')

    # When search displays a single result
    try:
        price_url_content = soup.find('div', class_='container').script.text.split('"')[1]
        price_url = generic_url + (price_url_content)
        source = session.get(price_url, headers=myuseragent, allow_redirects=False).text
        soup = BeautifulSoup(source, 'lxml')
        # Scrape Price, Product name and CDW Part details from the search results page
        price = soup.find('span', class_='price-type-selected').text
        product_name = soup.find('h1', class_='fn').text
        cdw_part = soup.find('span', class_='edc').text

    except Exception as e:
        # When search displays multiple results
        try:
            search_list = soup.find_all('div', class_='search-result coupon-check')
            sku_found = False
            for product in search_list:
                mfg = product.find('span', class_='mfg-code').text
                mfg = mfg[6:]
                if sku == mfg:
                    # When search displays multiple results and one of them matches with the exact SKU
                    sku_found = True
                    # Scrape Price, Product name and CDW Part details from the search results page
                    price = product.find('div', class_='price-type-price').text
                    product_name = product.find('a', class_='search-result-product-url').text
                    cdw_part = product.find('span', class_='cdw-code').text
                    cdw_part = cdw_part[6:]

            # When search displays multiple results but none of them match with the exact SKU
            if not sku_found:
                price = "SKU exact match not found"
                product_name = "Not applicable"
                cdw_part = "Not applicable"

        # When search displays "No Results Found!!"
        except Exception as e:
            price = "SKU exact match not found"
            product_name = "Not applicable"
            cdw_part = "Not applicable"

    price_list.append(price)
    product_names_list.append(product_name)
    cdw_parts_list.append(cdw_part)
    print(sku, price, product_name, cdw_part)
    print()
    # Write the results into a csv file
    csv_writer.writerow([sku, price, product_name, cdw_part])

csv_file.close()
