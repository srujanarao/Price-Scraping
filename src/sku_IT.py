from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import IT_creds
import pandas as pd
import csv
import sys
from datetime import datetime
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Generate Results in a csv file appended with current time
current_datetime = datetime.now()
str_current_datetime = str(current_datetime)
results_file = 'Results_IT_'+str_current_datetime+'.csv'
csv_file = open(results_file, 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['SKU', 'Batch_Price'])

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
login_page = 'https://www.ingrammicro.com/IMD_WASWeb/jsp/login/corporateVendorLogin.jsp'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100)     # Does not work with headless=True
    page = browser.new_page()
    page.goto(login_page)
    page.fill('input#username-field', IT_creds.USER)
    page.fill('input#password-field', IT_creds.PASSWORD)
    page.click('input[type=submit]')

    for sku in sku_list:
        prices = []
        # Initialize vendor price. If a valid price is found later on, it will be overwritten with the correct price.
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
        # Write the results into a csv file
        csv_writer.writerow([sku, vendor_price])

csv_file.close()