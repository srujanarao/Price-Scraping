import configparser
import pymysql
from bs4 import BeautifulSoup
import requests
from getuseragent import UserAgent
import pandas as pd

data = pd.read_csv('input_US.csv')
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

    except Exception as e:
        price = "SKU Not found"
        price_list.append(price)
        product_name = "Not applicable"
        product_names_list.append(product_name)
        cdw_part = "Not applicable"
        cdw_parts_list.append(cdw_part)
        print(sku, "SKU Not found", "Not applicable", "Not applicable")
        print()

# config = configparser.RawConfigParser()
# config.read(filenames='my.properties')
#
# host = config.get('mysql', 'host')
# user = config.get('mysql', 'user')
# password = config.get('mysql', 'password')
#
# connection = pymysql.connect(host=host, user=user, password=password)
# cursor = connection.cursor()
# cursor.execute("DROP DATABASE IF EXISTS EATON")
# cursor.execute("CREATE DATABASE EATON")
# connection = pymysql.connect(host=host, user=user, password=password, database='EATON')
# cursor = connection.cursor()
# cursor.execute("DROP TABLE IF EXISTS SKU_TABLE")
# mysql_create_query = "CREATE TABLE SKU_TABLE ( SKU CHAR(100), PRICE CHAR(100), PRODUCT_NAME CHAR(200), CDW_PART CHAR(" \
#                      "200)) "
# cursor.execute(mysql_create_query)
# mysql_insert_query = "INSERT INTO SKU_TABLE (SKU, PRICE, PRODUCT_NAME, CDW_PART) VALUES (%s, %s, %s, %s) "
#
# for i in range(len(sku_list)):
#     records = (sku_list[i], price_list[i], product_names_list[i], cdw_parts_list[i])
#     cursor.execute(mysql_insert_query, records)
#     connection.commit()
#
# cursor.close()
# connection.close()
