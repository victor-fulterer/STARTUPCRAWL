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
options.binary_location = "/Applications/Google Chrome/Contents/MacOS/Google Chrome"

# Zeile 18 den Dateipfad angeben wo sich euer Google Chrome Browser befindet

driver = webdriver.Chrome("/Users/stephanbergmann/Downloads/chromedriver 3")
# Zeile 22 den Dateipfad angeben wo euer Chromedriver liegt

driver.get('https://www.crunchbase.com/login')
time.sleep(3)

# To run im terminal - im richtigen directory <python crunchbase.py>


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

email = 'stephan.bergmann@student.unisg.ch'
password = 'data2dollar'

# Zeile 45 & 46 den Test Pro Account für Crunchbase

driver.find_element_by_name('email').send_keys(email)
driver.find_element_by_name('password').send_keys(password)


driver.find_element_by_xpath('//*[@id="mat-tab-content-0-0"]/div/login/form/div/button[2]').click()

driver.get('https://www.crunchbase.com/search/organization.companies/d0a758d683ea1fad8ebed67055618de8')
time.sleep(3)

# Zeile 56 den Link angeben mit den Filtereinstellungen - Beispiel "Switzerland"


try:
    driver.execute_script("arguments[0].click()",  driver.find_element_by_xpath('/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/search/page-layout/div/div/form/div[2]/results/div/div/div[3]/sheet-grid/div/div/grid-body/div/div/div/upsell/upsell-actions/div/div/button'))
    time.sleep(5)
    driver.get('https://www.crunchbase.com/search/organization.companies/d0a758d683ea1fad8ebed67055618de8')
    time.sleep(3)
    driver.refresh()
    time.sleep(3)
except:
    pass


driver.execute_script("arguments[0].click()",  driver.find_element_by_xpath('/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/search/page-layout/div/div/form/div[2]/results/div/div/div[1]/div/div/div/button[1]'))
time.sleep(2)
driver.execute_script("arguments[0].click()", driver.find_element_by_xpath('//*[@id="mat-checkbox-64"]/label/span/label-with-info/div'))
time.sleep(2)
driver.execute_script("arguments[0].click()", driver.find_element_by_xpath('//*[@id="mat-dialog-0"]/column-panel/div/dialog-layout/div/mat-dialog-content/div/div/div[1]/div/div[1]/mat-nav-list/mat-list-item[6]/div/div[3]/label-with-info/div'))
time.sleep(2)
driver.execute_script("arguments[0].click()", driver.find_element_by_xpath('//*[@id="mat-checkbox-78"]/label/span/label-with-info/div'))
time.sleep(2)
driver.execute_script("arguments[0].click()", driver.find_element_by_xpath('//*[@id="mat-dialog-0"]/column-panel/div/dialog-layout/div/mat-dialog-actions/div/button'))
time.sleep(5)

datas = []
while True:
    divs = driver.find_elements_by_class_name('component--grid-row')
    for div in divs:
        data = {}
        data['Name'] = div.find_element_by_class_name('column-id-identifier').get_attribute('innerText').strip().split('\n')[1]
        data['Industries'] = div.find_element_by_class_name('column-id-categories').get_attribute('innerText').strip()
        data['Location'] = div.find_element_by_class_name('column-id-location_identifiers').get_attribute('innerText').strip()
        data['Description'] = div.find_element_by_class_name('column-id-short_description ').get_attribute('innerText').strip()
        try:
            data['Twitter'] = div.find_element_by_class_name('column-id-twitter').find_element_by_tag_name('a').get_attribute('href')
        except:
            pass
        data['Total Funding Amount'] = div.find_element_by_class_name('column-id-funding_total').get_attribute('innerText').strip()
        try:
            data['LinkedIn'] = div.find_element_by_class_name('column-id-linkedin').find_element_by_tag_name('a').get_attribute('href')
        except:
            pass
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
        time.sleep(3)
    except Exception as e:
        print(e)
        break

df = json_normalize(datas)

writer = pd.ExcelWriter('crunchbase.xlsx', engine='xlsxwriter')
df.to_excel(writer,sheet_name = 'Data', index=False)
writer.save() 
driver.quit()