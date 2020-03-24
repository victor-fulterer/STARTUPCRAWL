#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 18:40:56 2020

@author: Samuel
"""
import pandas as pd

lst = list()
cleanlst = list()

#Pfad ändern, wo das Crunchbase-File abgelegt wird
#(alternativ könnte man den CB und LinkedIn Crawl mergen und die URLs direkt übergeben)
filepath ='/Users/Samuel/Documents/2.Semester/Data2Dollar/crunchbase.xlsx' 

#Bei Traceback darauf achten, ob das Tabellenblatt im File "Sheet1" heißt, ansonsten entweder im Code oder im File umbenenen
df = pd.read_excel(filepath, sheet_name='Data')

#relevanten Spaltennamen ändern (wo jetzt Kilometerstand steht)
for i in df['LinkedIn']:
    lst.append(i)

#Eliminieren der ursprünglich leeren Zellwerte im Excel in der generierten Liste
cleanlst = [x for x in lst if str(x) != 'nan']

print(cleanlst)