from bs4 import BeautifulSoup, SoupStrainer
import requests
from getuseragent import UserAgent
import pandas as pd
import httplib2
from urllib.request import Request, urlopen
import re
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options

# data = pd.read_csv('ca_sku_file.csv')
# sku_list = data['SKU'].tolist()
# sku_list = [sku for sku in sku_list if str(sku) != 'nan']

product_names_list = []
cdw_parts_list = []
min_price_list = []
url3_list = []
records = []

#sku = 'SYA12K16P'
# sku = 'SYA4K8P'
sku_list = ['SYA4K8P']

price_list = []
# url_1 = f'https://www.cdw.ca/search/?key={sku}'
# myuseragent = UserAgent("all", requestsPrefix=True).Random()
# session = requests.Session()
# source = session.get(url_1, headers=myuseragent, allow_redirects=False).text
# soup = BeautifulSoup(source, 'lxml')
#
# try:
#     price_url_content = soup.find('div', class_='container').script.text.split('"')[1]
#     generic_url = 'https://www.cdw.ca'
#     price_url = generic_url + (price_url_content)
#
#     source = session.get(price_url, headers=myuseragent, allow_redirects=False).text
#     soup = BeautifulSoup(source, 'lxml')
#     price_1 = soup.find('span', class_='price-type-selected').text
#     price_list.append(price_1)
#     product_name = soup.find('h1', class_='fn').text
#     # product_names_list.append(product_name)
#     cdw_part = soup.find('span', class_='edc').text
#     # cdw_parts_list.append(cdw_part)
#
#     print(sku, price_1, product_name, cdw_part)
#     print()
#
# except Exception as e:
#     price_1 = "SKU Not found"
#     # price_list.append(price)
#     # product_name = "Not applicable"
#     # product_names_list.append(product_name)
#     # cdw_part = "Not applicable"
#     # cdw_parts_list.append(cdw_part)
#     # print(sku, "SKU Not found", "Not applicable", "Not applicable")
#     # print()
for sku in sku_list:
    price_list = []
    url3_list = []
    url_2 = f'https://www.pc-canada.com/item/{sku}'
    url_3 = f'https://www.cendirect.com/main_en/find_simple.php?rSearchKeyword={sku}'
    myuseragent = UserAgent("all", requestsPrefix=True).Random()
    session = requests.Session()

    # source = session.get(url_3, headers=myuseragent, allow_redirects=False).text
    # soup = BeautifulSoup(source, 'lxml')

    # req = Request(url_3)
    # html_page = urlopen(req)
    # soup = BeautifulSoup(html_page, "lxml")

#     links = []
#     for link in soup.findAll('a'):
#         links.append(link.get('href'))
#
#     for link in links:
#         if sku in str(link):
#             url3_list.append(link)
#
#
#     if len(url3_list) > 2:
#         print(url3_list)
#         url3_final = url3_list[1]
#     else:
#         print(url3_list)
#         url3_final = url3_list[0]
#
#     source = session.get(url3_final, headers=myuseragent, allow_redirects=True).text
#     soup = BeautifulSoup(source, 'lxml')
#     print(sku)
#     price_3 = soup.find_all('b')
#     print(price_3)
#     price_3 = str(soup.find_all('b')[7].text).strip('$')
#
#     price_list.append(price_3)
#     min_price = min(price_list)
#     min_price_list.append(min_price)
#
# print(min_price_list)


source = session.get(url_2, headers=myuseragent, allow_redirects=False).text
soup = BeautifulSoup(source, 'lxml')
print(soup.prettify())