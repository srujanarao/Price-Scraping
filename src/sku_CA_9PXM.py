from bs4 import BeautifulSoup
import requests
from getuseragent import UserAgent
import undetected_chromedriver as uc
import time
import pandas as pd
import ssl
import csv

ssl._create_default_https_context = ssl._create_unverified_context

csv_file = open('Results_CA_9PXM.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['SKU', 'Price'])

data = pd.read_csv('input_file_CA_9PXM.csv')
sku_list = data['SKU'].tolist()
sku_list = [sku for sku in sku_list if str(sku) != 'nan']
min_price_list = []

myuseragent = UserAgent("all", requestsPrefix=True).Random()
session = requests.Session()

main_url = f'https://www.pc-canada.com'
driver = uc.Chrome(headless=False)
driver.get(main_url)
time.sleep(15)

for sku in sku_list:
    sku_prices = []

    url_1 = f'https://www.cdw.ca/search/?key={sku}'
    source = session.get(url_1, headers=myuseragent, allow_redirects=False).text
    soup = BeautifulSoup(source, 'lxml')

    try:
        price_url_content = soup.find('div', class_='container').script.text.split('"')[1]
        generic_url = 'https://www.cdw.ca'
        price_url = generic_url + (price_url_content)
        source = session.get(price_url, headers=myuseragent, allow_redirects=False).text
        soup = BeautifulSoup(source, 'lxml')
        price_1 = soup.find('span', class_='price-type-selected').text
        sku_prices.append(price_1)

    except Exception as e:
        price_1 = "SKU Not found"

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
        url2_final = "SKU Not Found"
    else:
        url2_final = url2_list[0]

    if url2_final != "SKU Not Found":
        source = session.get(url2_final, headers=myuseragent, allow_redirects=True).text
        soup = BeautifulSoup(source, 'lxml')
        price_2 = soup.find_all('b')
        price_2 = soup.find_all('b')[7].text
        if '$' in price_2:
            price_2 = str(price_2).strip('$')
            sku_prices.append(price_2)
        else:
            print("URL 2 is unstable. Search bar not yielding any results \n")

    url_3 = f'https://www.pc-canada.com/item/{sku}'
    driver.get(url_3)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    try:
        mfgr = soup.find('span', class_='active-crumb').text
        if str(mfgr) == sku:
            price_3 = soup.find('p',
                                class_='d-flex align-items-center mb-0 lh-1 text-red-500 fs-3xl fs-lg-4xl fs-xxxl-5xl '
                                       'fw-bold').text
            price_3 = price_3.strip().strip('$')
            sku_prices.append(price_3)

        else:
            price_3 = "SKU Not Found in url3"
            print(price_3)
            print("a")
    except:
        price_3 = "SKU Not Found in url3"
        print(price_3)
        print("b")

    print(f"SKU {sku} Prices from different websites are: {sku_prices} ")
    try:
        sku_min_price = min(sku_prices)
        print(f"SKU {sku}'s minimum price : {sku_min_price} ")
        print()
        min_price_list.append(sku_min_price)
    except:
        print(f"SKU {sku} does not have a price listed in all 3 sites")
        sku_min_price = "SKU Not Found"
        min_price_list.append(sku_min_price)

for i in range(len(sku_list)):
    print()
    print(sku_list[i], min_price_list[i])
    csv_writer.writerow([sku_list[i], min_price_list[i]])
