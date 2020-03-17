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

writer = csv.writer(open('output.csv', 'w+', encoding='utf-8-sig', newline=''))
writer.writerow(['Hochschule', 'Position', 'Company', 'Education', 'Location', 'URL'])

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


sel = Selector(text = driver.page_source)
ueberschriften = sel.xpath('//h4/text()').extract()[1:6]
untere dinge = sel.xpath('//*[@class="org-people-bar-graph-element__category"]/text()').extract()[10:15]
zahlen = sel.xpath('//*[@class="org-people-bar-graph-element__percentage-bar-info truncate full-width mt2 mb1 t-14 t-back--light t-normal"]')

# nummern noch anpassen und das ganze dann 5x für jeden Datensatz

#hochschule = sel.xpath('//*[@class = "org-people-bar-graph-element__percentage-bar-info truncate full-width mt2 mb1 t-14 t-black--light t-normal"]/text()').extract_first().split()
#hochschule = ' '.join(hochschule)

#url = driver.current_url

#print('\n')
#print('Hochschule: ', hochschule)
#print('\n')
          
#writer.writerow([hochschule])

driver.quit()