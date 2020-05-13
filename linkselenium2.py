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
from pandas.io.json import json_normalize
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

# Das Excel Dokument wird geschrieben
writer = csv.writer(open('linkedin_801_888.csv', 'w+', encoding='utf-8-sig', newline=''))
writer.writerow(['Branche', 'URL'])

# Login-Prozess auf LinkedIn Startseite mit erstelltem Account. (Jens Anoroc)
driver = webdriver.Chrome('C:\webdrivers\chromedriver.exe')
driver.get('https://ch.linkedin.com/')
sleep(3)

# Eingabe des Username
username = driver.find_element_by_name("session_key")
username.send_keys('ostmau@hotmail.com')
sleep(1)

# Eingabe des Passworts
password = driver.find_element_by_name("session_password")
password.send_keys('data2dollar')
sleep(1)

# Klick auf Sign-In Button
sign_in_button = driver.find_element_by_class_name('sign-in-form__submit-btn')
sign_in_button.click()
sleep(2)

# Gecrawlte Excel-Liste von Crunchbase wird gesucht und als neue Liste mit den gewünschten URL's verwendet
# Dabei wird jeweils in 100er Schritten gecrwalt, damit es für LinkedIn nicht zu offensichtlich ist.
lste = list()
cleanlste = list()

filepath ='/Users/Mauro Osta/Downloads/crunchbase_801_888.xlsx'

df = pd.read_excel(filepath, sheet_name='Data')

for i in df['LinkedIn']:
    lste.append(i)

#Eliminieren der ursprünglich leeren Zellwerte im Excel in der generierten Liste
cleanlste = [x for x in lste if str(x) != 'nan']

# Schleife der einzelnen Unternehmen
for url in cleanlste:
    driver.get(url)
    sleep(4)

# Sicherheitsschleife, falls URL nicht funktioniert oder Unternehmen keine Personenangaben listet
    try:
        sel = Selector(text=driver.page_source)

        Branche = sel.xpath('//*[@class="org-top-card-summary-info-list__info-item"]/text()').extract_first().strip()
        url = driver.current_url
                    
        writer.writerow([Branche,url])
        sleep(2)
         
    except:
        continue

driver.quit()

