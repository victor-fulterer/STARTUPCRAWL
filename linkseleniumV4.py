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

writer = csv.writer(open('linkedin.csv', 'w+', encoding='utf-8-sig', newline=''))
writer.writerow(['Anzahl', 'Typ', 'Art der Daten', 'URL'])

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

lste = list()
cleanlste = list()

filepath ='/Users/Mauro Osta/Downloads/crunchbase_bereinigt_1_100.xlsx'

df = pd.read_excel(filepath, sheet_name='Data')

for i in df['LinkedIn']:
    lste.append(i)

#Eliminieren der ursprünglich leeren Zellwerte im Excel in der generierten Liste
cleanlste = [x for x in lste if str(x) != 'nan']

# Crawl Prozess für Hevletia als Beispielunternehmen

for url in cleanlste:
    driver.get(url)
    sleep(3)

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
        if 'Wohnort' in container.extract():
            raw_data = container.xpath('.//*[contains(@class, "org-people-bar-graph-element__percentage-bar-info ")]//text()').extract()
     
            raw_data = [rd.strip() for rd in raw_data]
            raw_data = [rd for rd in raw_data if rd != '']
            
            # split raw data in numbers & residence
            for rd in list(chunks(raw_data, 2)):
                number_residence = rd[0]
                residence = rd[1]

                print('number_residence: {}'.format(number_residence))
                print('residence: {}'.format(residence))
                print('\n')
                
                writer.writerow([number_residence, residence, 'Wohnort', url])
     
                
    for container in sel.xpath('//*[@class="insight-container"]'):
        if 'Hochschule' in container.extract():
            raw_data = container.xpath('.//*[contains(@class, "org-people-bar-graph-element__percentage-bar-info ")]//text()').extract()
     
            raw_data = [rd.strip() for rd in raw_data]
            raw_data = [rd for rd in raw_data if rd != '']
            
            # split raw data in numbers & schools
            for rd in list(chunks(raw_data, 2)):
                number_school = rd[0]
                school = rd[1]

                print('number_school: {}'.format(number_school))
                print('school: {}'.format(school))
                print('\n')
                
                writer.writerow([number_school, school, 'Hochschule', url])
     
                
    next_site = driver.find_element_by_xpath('//*[@class="artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view"]')
    next_site.click()
    sleep(2)

    for container in sel.xpath('//*[@class="insight-container"]'):
        if 'Tätigkeitsbereich' in container.extract():
            raw_data = container.xpath('.//*[contains(@class, "org-people-bar-graph-element__percentage-bar-info ")]//text()').extract()
     
            raw_data = [rd.strip() for rd in raw_data]
            raw_data = [rd for rd in raw_data if rd != '']
            
            # split raw data in numbers & fields
            for rd in list(chunks(raw_data, 2)):
                number_field = rd[0]
                field = rd[1]

                print('number_field: {}'.format(number_field))
                print('field: {}'.format(field))
                print('\n')
                
                writer.writerow([number_field, field, 'Tätigkeitsbereich', url])
     
                
    for container in sel.xpath('//*[@class="insight-container"]'):
        if 'Studium' in container.extract():
            raw_data = container.xpath('.//*[contains(@class, "org-people-bar-graph-element__percentage-bar-info ")]//text()').extract()
     
            raw_data = [rd.strip() for rd in raw_data]
            raw_data = [rd for rd in raw_data if rd != '']
            
            # split raw data in numbers & fields
            for rd in list(chunks(raw_data, 2)):
                number_study = rd[0]
                study = rd[1]

                print('number_study: {}'.format(number_study))
                print('study: {}'.format(study))
                print('\n')
                
                writer.writerow([number_study, study, 'Studium', url])
     
                
    next_site = driver.find_element_by_xpath('//*[@class="artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view"]')
    next_site.click()
    sleep(2)

    for container in sel.xpath('//*[@class="insight-container"]'):
        if 'Kenntnisse und Fähigkeiten' in container.extract():
            raw_data = container.xpath('.//*[contains(@class, "org-people-bar-graph-element__percentage-bar-info ")]//text()').extract()
     
            raw_data = [rd.strip() for rd in raw_data]
            raw_data = [rd for rd in raw_data if rd != '']
            
            # split raw data in numbers & fields
            for rd in list(chunks(raw_data, 2)):
                number_skills = rd[0]
                skills = rd[1]
     
                print('number_skills: {}'.format(number_skills))
                print('skills: {}'.format(skills))
                print('\n')                        

                writer.writerow([number_skills, skills, 'Skills', url])

driver.quit()