from bs4 import BeautifulSoup
import requests
from getuseragent import UserAgent
import undetected_chromedriver as uc
import time
import sys
from datetime import datetime
import pandas as pd
import ssl
import csv
ssl._create_default_https_context = ssl._create_unverified_context

# Generate Results in a csv file appended with current time
current_datetime = datetime.now()
str_current_datetime = str(current_datetime)
results_file = 'Results_CA_9PXM_'+str_current_datetime+'.csv'
csv_file = open(results_file, 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['SKU', 'Minimum_Price', 'Site'])

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
min_price_list = []
site_list = []
generic_url_1 = 'https://www.cdw.ca'
main_url_3 = f'https://www.pc-canada.com'
driver = uc.Chrome(headless=False)
driver.get(main_url_3)
time.sleep(10)

myuseragent = UserAgent("all", requestsPrefix=True).Random()
session = requests.Session()
time.sleep(5)

for sku in sku_list:
    sku_prices = []

    # This part is for fetching SKU's price from https://www.cdw.ca
    site_1 = 'www.cdw.ca'
    url = f'https://www.cdw.ca/search/?key={sku}'
    source = session.get(url, headers=myuseragent, allow_redirects=False).text
    soup = BeautifulSoup(source, 'lxml')

    # When search displays a single result
    try:
        price_url_content = soup.find('div', class_='container').script.text.split('"')[1]
        price_url = generic_url_1 + (price_url_content)
        source = session.get(price_url, headers=myuseragent, allow_redirects=False).text
        soup = BeautifulSoup(source, 'lxml')
        price_1 = soup.find('span', class_='price-type-selected').text
        sku_prices.append(price_1)

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
                    price_1 = product.find('div', class_='price-type-price').text
                    sku_prices.append(price_1)

            # When search displays multiple results but none of them match with the exact SKU
            if not sku_found:
                price_1 = "SKU exact match not found"

        # When search displays "No Results Found!!"
        except Exception as e:
            price_1 = "SKU exact match not found"

    # This part is for fetching SKU's price from https://www.cendirect.com
    site_2 = 'www.cendirect.com'
    url2_list = []
    url_2 = f'https://www.cendirect.com/main_en/find_simple.php?rSearchKeyword={sku}'
    source = session.get(url_2, headers=myuseragent, allow_redirects=False).text
    soup = BeautifulSoup(source, 'lxml')

    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))

    for link in links:
        if f'/main_en/tech-specs-{sku}-' in str(link):
            url2_list.append(link)

    if len(url2_list) == 0:
        url2_final = "SKU Not Found in www.cendirect.com "
    else:
        url2_final = url2_list[0]

    if url2_final != "SKU Not Found in in www.cendirect.com":
        source = session.get(url2_final, headers=myuseragent, allow_redirects=True).text
        soup = BeautifulSoup(source, 'lxml')
        price_2 = soup.find_all('b')
        price_2 = soup.find_all('b')[7].text
        if '$' in price_2:
            price_2 = str(price_2).strip()
            sku_prices.append(price_2)
        else:
            print("https://www.cendirect.com is unstable. Search bar is not displaying any results. Try again after sometime. \n")

    # This part is for fetching SKU's price from https://www.pc-canada.com
    site_3 = 'www.pc-canada.com'
    url_3 = f'https://www.pc-canada.com/item/{sku}'
    driver.get(url_3)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    try:
        mfgr = soup.find('span', class_='active-crumb').text
        if str(mfgr) == sku:
            price_3 = soup.find('p',
                                class_='d-flex align-items-center mb-0 lh-1 text-red-500 fs-3xl fs-lg-4xl fs-xxxl-5xl '
                                       'fw-bold').text
            price_3 = price_3.strip()
            sku_prices.append(price_3)

        else:
            price_3 = "SKU Not Found in www.pc-canada.com"
    except:
        price_3 = "SKU Not Found in www.pc-canada.com"

    print(f"SKU {sku} Prices from different websites are: {sku_prices} ")
    try:
        sku_min_price = min(sku_prices)
        if sku_min_price == price_1:
            site = site_1
        elif sku_min_price == price_2:
            site = site_2
        elif sku_min_price == price_3:
            site = site_3
        print(f"SKU: {sku} Minimum Price: {sku_min_price}  Source: {site}")
        print()
        min_price_list.append(sku_min_price)
        site_list.append(site)
    except:
        print(f"SKU {sku} does not have a price listed in all 3 sites")
        sku_min_price = "SKU not found in all 3 sites"
        site = "SKU not found in all 3 sites"
        min_price_list.append(sku_min_price)
        site_list.append(site)

# Write the results into a csv file
for i in range(len(sku_list)):
    print()
    print(sku_list[i], min_price_list[i])
    csv_writer.writerow([sku_list[i], min_price_list[i], site_list[i]])

csv_file.close()