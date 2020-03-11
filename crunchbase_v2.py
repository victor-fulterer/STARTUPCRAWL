from selenium import webdriver
import time
from pandas.io.json import json_normalize
import pandas as pd
import os
import socket
import requests


socket.setdefaulttimeout(120)

if not os.path.exists('imgs'):
    os.makedirs('imgs')
    
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Zeile 18 den Dateipfad angeben wo sich euer Google Chrome Browser befindet

driver = webdriver.Chrome('/Users/victor/chromedriver')
# Zeile 22 den Dateipfad angeben wo euer Chromedriver liegt

driver.get('https://www.crunchbase.com/login')
time.sleep(3)




from selenium.webdriver.common.action_chains import ActionChains
def click_and_hold(driver, element):
    ActionChains(driver).click_and_hold(element).perform()
    time.sleep(5)
    ActionChains(driver).release(element).perform()
    time.sleep(10)


try:
    driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))
    click_and_hold(driver, driver.find_element_by_xpath('/html/body'))
except:
    pass

email = 'ostmau@gmail.com'
password = 'data2dollar'

# Zeile 45 & 46 den Test Pro Account für Crunchbase

driver.find_element_by_name('email').send_keys(email)
driver.find_element_by_name('password').send_keys(password)


driver.find_element_by_xpath('//*[@id="mat-tab-content-0-0"]/div/login/form/div/button[2]').click()

driver.get('https://www.crunchbase.com/search/organization.companies/21dbfe09b3e5b81d31a86c169acd16de')
time.sleep(3)

# Zeile 56 den Link angeben mit den Filtereinstellungen - Beispiel "Switzerland"


try:
    driver.execute_script("arguments[0].click()",  driver.find_element_by_xpath('/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/search/page-layout/div/div/form/div[2]/results/div/div/div[3]/sheet-grid/div/div/grid-body/div/div/div/upsell/upsell-actions/div/div/button'))
    time.sleep(5)
    driver.get('https://www.crunchbase.com/search/organization.companies/21dbfe09b3e5b81d31a86c169acd16de')
    time.sleep(3)
    driver.refresh()
    time.sleep(3)
except:
    pass

datas = []
while True:
    divs = driver.find_elements_by_class_name('component--grid-row')
    for div in divs:
        data = {}
        data['Name'] = div.find_element_by_class_name('column-id-identifier').get_attribute('innerText').strip().split('\n')[1]
        data['Industries'] = div.find_element_by_class_name('column-id-categories').get_attribute('innerText').strip()
        data['Location'] = div.find_element_by_class_name('column-id-location_identifiers').get_attribute('innerText').strip()
        data['Description'] = div.find_element_by_class_name('column-id-short_description ').get_attribute('innerText').strip()
        data['Company Link'] = div.find_element_by_class_name('column-id-identifier').find_element_by_tag_name('a').get_attribute('href')
        datas.append(data)
        try:
            url = div.find_element_by_class_name('column-id-identifier').find_element_by_tag_name('img').get_attribute('src')
            myfile = requests.get(url)
            open('imgs/'+data['Name']+'.jpg', 'wb').write(myfile.content)
        except:
            pass
    try:
        if driver.find_element_by_class_name('component--results-info').find_element_by_class_name('page-button-next').get_attribute('aria-disabled') == 'true':
            break
        driver.execute_script("arguments[0].click()", driver.find_element_by_class_name('component--results-info').find_element_by_class_name('page-button-next'))
        time.sleep(7)
    except Exception as e:
        print(e)
        break

df = json_normalize(datas)


df['Linked In'] = 'N/A'
df['Total Funding Ammount'] = 'N/A'
for index, row in df.iterrows():
    try:
        driver.get(row['Company Link'])
    except:
        continue
    time.sleep(7)
    
    try:
        driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))
        click_and_hold(driver, driver.find_element_by_xpath('/html/body'))
    except:
        pass
    try:
        row['Linked In'] = driver.find_element_by_xpath('//a[@aria-label="View on LinkedIn"]').get_attribute('href')
    except:
        pass
    try:
        row['Total Funding Ammount'] = driver.find_element_by_xpath('//*[@id="section-overview"]/mat-card/div[2]/big-values-card/div/div[1]/mat-card/span[2]/field-formatter/a').get_attribute('innerText')
    except:
        pass

writer = pd.ExcelWriter('crunchbase.xlsx', engine='xlsxwriter')
df.to_excel(writer,sheet_name = 'Data', index=False)
writer.save() 
driver.quit()
        
