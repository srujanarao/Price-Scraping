from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import IT_creds
import pandas as pd
import csv

csv_file = open('Results_IT.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['SKU', 'Price'])

data = pd.read_csv('IT_vendor_portal.csv')
sku_list = data['SKU'].tolist()
sku_list = [sku for sku in sku_list if str(sku) != 'nan']
# sku_list = ['NDRB1500', 'SMC1000C', 'GVSUPS30K0B5FS']
price_list = []
records = {}
login_page = 'https://www.ingrammicro.com/IMD_WASWeb/jsp/login/corporateVendorLogin.jsp'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page()
    page.goto(login_page)
    page.fill('input#username-field', IT_creds.USER)
    page.fill('input#password-field', IT_creds.PASSWORD)
    page.click('input[type=submit]')

    for sku in sku_list:
        prices = []
        vendor_price = "SKU Not Found"
        sku_url = f'https://www.ingrammicro.com/IMD_WASWeb/jsp/search/Results_nav.jsp?keywords={sku}&scope=3'
        page.goto(sku_url)
        soup = BeautifulSoup(page.inner_html('body'), 'lxml')

        prices = soup.find_all('small')
        for price in prices:
            if '$' in price.text:
                vendor_price = str(price.text).strip()

        price_list.append(vendor_price)
        print(sku, vendor_price)
        print()
        csv_writer.writerow([sku, vendor_price])

csv_file.close()
