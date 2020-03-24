# -*- coding: utf-8 -*-
import scrapy


class LinkseleniumSpider(scrapy.Spider):
    name = 'linkselenium'
    allowed_domains = ['www.linkedin.ch']
    start_urls = ['http://www.linkedin.ch/']

import csv
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

writer = csv.writer(open('linkedin.csv', 'w+', encoding='utf-8-sig', newline=''))
writer.writerow(['Wohnort', 'Hochschule', 'Tätigkeitsbereich', 'Studium', 'Kenntnisse und Fähigkeiten'])

# Login-Prozess auf LinkedIn Startseite mit erstelltem Account.

driver = webdriver.Chrome('C:\webdrivers\chromedriver.exe')
driver.get('https://ch.linkedin.com/')
sleep(3)

username = driver.find_element_by_name("session_key")
username.send_keys('ostmau@hotmail.com')
sleep(1)

password = driver.find_element_by_name("session_password")
password.send_keys('data2dollar')
sleep(1)

sign_in_button = driver.find_element_by_class_name('sign-in-form__submit-btn')
sign_in_button.click()
sleep(2)

# Crawl Prozess für Hevletia als Beispielunternehmen

driver.get('https://www.linkedin.com/company/helvetia-versicherungen-schweiz/')
sleep(0.5)

personen = driver.find_element_by_xpath('//*[@data-control-name="page_member_main_nav_people_tab"]')
personen.click()
sleep(2)

element = driver.find_element_by_xpath('//*[@data-control-name="people_toggle_see_more_insights_button"]')
driver.execute_script("arguments[0].scrollIntoView(0, document.documentElement.scrollHeight-5);", element)

mehr_anzeigen = driver.find_element_by_xpath('//*[@data-control-name="people_toggle_see_more_insights_button"]')
mehr_anzeigen.click()
sleep(2)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
 
 
sel = Selector(text=driver.page_source)
for container in sel.xpath('//*[@class="insight-container"]'):
    if 'Where they studied' in container.extract():
        raw_data = container.xpath('.//*[contains(@class, "org-people-bar-graph-element__percentage-bar-info ")]//text()').extract()
 
        raw_data = [rd.strip() for rd in raw_data]
        raw_data = [rd for rd in raw_data if rd != '']
        
        # split raw data in numbers & schools
        for rd in list(chunks(raw_data, 2)):
            number = rd[0]
            school = rd[1]
 
            print('number: {}'.format(number))
            print('school: {}'.format(school))
            print('\n')

driver.quit()