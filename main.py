
# Automatically finds your target keyword in the google page search on each page with the search word located in your spreadsheet.
# You first need to creeate your own OAuth Client IDs that can be found on https://console.cloud.google.com
# Download the json file, put it in the same path and you are good to go.
# P.S. You might get detected by reCaptcha which is a little annoying.
# This can be done by making an captcha automatic solver but has not yet been made.

import time
from Google import Create_Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



# Prepairing access on Spreadsheet

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
spreadsheet_id = '********************************************' # https://docs.google.com/spreadsheets/d/<this section>/edit#gid=0
mySpreadSheets = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

worksheet_name = 'Sheet2!'

# Get Items
range_name = worksheet_name + 'A3:A32'
result = service.spreadsheets().values().get(
    spreadsheetId = spreadsheet_id,
    range = range_name,
    majorDimension='COLUMNS').execute()

keywords, = result.get('values', [])


cell_range_insert = 'C3' # Target/cursor

def updateSheet(values):
    value_range_body = {
        'majorDimension': 'COLUMNS',
        'values': [values]
    }

    # Update values on sheet
    service.spreadsheets().values().update(
        spreadsheetId = spreadsheet_id,
        valueInputOption = 'USER_ENTERED',
        range = worksheet_name + cell_range_insert,
        body = value_range_body
    ).execute()

# [WebScraping / Automating] Finding the target on each page of Google Search

url = 'https://www.google.com'

options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options, executable_path='chromedriver.exe')
driver.get(url)
time.sleep(5)



text_to_find = 'I am difficult to find' # replace this with your target text


# The page number where your key word found will be stored in the values. If none, it will store zero.
values = []

for text_field_search in keywords:
    search = driver.find_element_by_name('q')
    search.send_keys(text_field_search)
    search.send_keys(Keys.RETURN)
    
    page_number = 1 # you are in page 1 (starting)

    while text_to_find not in driver.page_source:

        if text_to_find in driver.page_source:
            print(f'{text_to_find} found on page {page_number}')
            values.append(page_number)
            break
        
        next_page = driver.find_elements_by_id('pnnext')
        if len(next_page) != 0:
            next_page[0].click()
            time.sleep(1)
            page_number += 1
        else:
            print(f'{text_to_find} not found.')
            values.append(0)
            break
    
    driver.find_element_by_name('q').clear()
    print(values)

updateSheet(values)
driver.quit()