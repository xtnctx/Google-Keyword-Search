# Automatically finds your target keyword in the google page search for each page with the search word located in your spreadsheet.
# You might get detected by reCaptcha which is a little annoying.
# This can be done by making an captcha automatic solver but has not yet been made.

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Store all your keywords you want to search here. 
# The element/s in this array is/are the words that you put in the search bar.
# For example, ['who is albert einstein', 'how to bypass recaptcha', 'best programming language for automation']
keywords = []

# replace this with your target text
text_to_find = 'I am difficult to find' 


# your desired browser where search bar is active
url = 'https://www.google.com'

# Every browser is different, so you can manually do this by hand.
# If you right click then inspect the search bar of your browser,
# you should see <input class='...' value='...' name='q'>.
# same with id of next anchor button in google page since it doesn't have the element name.
search_bar_element_name = 'q'
next_anchor_element_id = 'pnnext'


# I tried too many options to get rid of reCAPTCHA.
# After some testing this one works. But at some point I still detected by 
# reCAPTCHA when you have many keywords and you leave it running by itself.
options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# This opens your 'chromedriver.exe' but I added some delay because
# We humans does not actually search immediately when the browser is successfully loaded.
# Basically adding time delay means we are trying to imitate human activity.
driver = webdriver.Chrome(options=options, executable_path='chromedriver.exe')
driver.get(url)
time.sleep(5)


# The page number where your key word found will be stored in this array. If none, it will store zero.
values = []

# This is where searching is executed, you will see chrome popping on your screen
# It will search all the elements in your keywords array.
# I also added 1s delay for every next page.
for text_field_search in keywords:
    search = driver.find_element_by_name(search_bar_element_name)
    search.send_keys(text_field_search)
    search.send_keys(Keys.RETURN)
    
    page_number = 1 # you are in page 1 (starting)

    while text_to_find not in driver.page_source:

        if text_to_find in driver.page_source:
            print(f'{text_to_find} found on page {page_number}')
            values.append(page_number)
            break
        
        next_page = driver.find_elements_by_id(next_anchor_element_id)
        if len(next_page) != 0:
            next_page[0].click()
            time.sleep(1)
            page_number += 1
        else:
            print(f'{text_to_find} not found.')
            values.append(0)
            break
    
    driver.find_element_by_name(search_bar_element_name).clear()
driver.quit()



# Finally, prints all the result
spacing = 50
print('-'*spacing*2)
print('{0:<50} | {1:<0}'.format("KEYWORD", f"{text_to_find} IS AVAILABLE AT PAGE"))
print('-'*spacing*2)
for i in range(len(keywords)):
    result = '{0:<50} | {1:<0}'.format(keywords[i], str(values[i]))
    print(result)
    print('-'*spacing*2)



