
## Proskauer
import pandas
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import openpyxl

chrome_Webdriver_loc = 'C:/Users/csavage/Downloads/chromedriver_win32 (3) for 104/chromedriver.exe'
# Path to Chrome Beta (104)
Options.binary_location = "C:/Program Files/Google/Chrome Beta/Application/chrome.exe"

s = Service(chrome_Webdriver_loc)
driver = webdriver.Chrome(service=s)

driver.implicitly_wait(10)

import string
ABC = list(string.ascii_uppercase)

A_Z_URLS = []

for i in ABC:
    A_Z_URL = f'https://www.proskauer.com/professionals?general=no&prefix={i}&key_contact=&practice_group=&practices=&industries=&market_solutions=&offices=&languages=&titles=&educations=&schools=&degrees=&sort=&search=&search-mobile='
    A_Z_URLS.append(A_Z_URL)

URLS = []
for A_Z_URL in A_Z_URLS:
    driver.get(A_Z_URL)
    # SCROLL TO THE BOTTOM OF THE PAGE
    SCROLL_PAUSE_TIME = 5
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            driver.find_element(By.LINK_TEXT, 'LOAD MORE').click()
        except Exception:
            pass
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    elems = driver.find_elements(By.TAG_NAME, 'a')
        for elem in elems:
            href = elem.get_attribute('href')
            if href is not None:
                try:
                    print(href)
                    URLS.append(href)
                except Exception:
                    pass

URL_DF = pandas.DataFrame({"URLS":URLS})

# Get rid of the URLs we don't need:
URL_DF = (URL_DF
 .loc[URL_DF['URLS'].str.lower().str.contains('/professionals/',regex=True,na=False)] #Unique identifier
 #.loc[URL_DF['URLS'].str.lower().str.contains('.html', regex=True, na=False)]  # Unique identifier
 .query('URLS not in ["nan"]')
 .drop_duplicates()
 .dropna()
)

URL_DF['URLS'] = URL_DF[URL_DF['URLS'].str.contains('vcard') == False]
URL_DF = URL_DF.dropna()


LIST_URLS = list(URL_DF['URLS'])

Attorneys = []

#XPath_Contact = str(input("Enter XPath for Attorney's Contact (or Name): "))
#XPath_Bio = str(input("Enter XPath for Attorney's Bio: "))
PATH_FOR_EXCELS = "C:/Users/csavage/OneDrive - Alvarez and Marsal/Desktop/"

for A in LIST_URLS:
    try:
        driver.get(A)
        driver.implicitly_wait(1000)
        Name = driver.find_element('xpath', '//*[@id="main"]/section[1]/div/div[2]/div/div/div/div[1]/h2')
        Position = driver.find_element('xpath', '//*[@id="main"]/section[1]/div/div[2]/div/div/div/div[1]/h3')
        Location = driver.find_element('xpath', '//*[@id="main"]/section[1]/div/div[2]/div/div/div/div[2]/h3/a[1]')
        Attorneys.append({"Name":Name.text,"Location":Location.text,"Position":Position.text,"URL:":A})
    except Exception:
        pass
    time.sleep(.1)

LF_NAME = 'ReedSmith'
ATT_DF = pandas.DataFrame(Attorneys)
ATT_DF.to_excel(PATH_FOR_EXCELS+LF_NAME+".xlsx")
# Open the Excel file
import os
os.system(f'start "excel" "{PATH_FOR_EXCELS}{LF_NAME}.xlsx"')
