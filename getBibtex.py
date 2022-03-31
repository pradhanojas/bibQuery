# -*- coding: utf-8 -*-
"""
Bibtex scraper
"""
import os
import sys
import pandas as pd
import csv
csv.QUOTE_NONE
import re
import time 
from random import random
from fp.fp import FreeProxy
from scholarly import scholarly, ProxyGenerator

# current_working_path = os.path.dirname(os.path.abspath(__file__))
# os.chdir(current_working_path)

data = pd.read_excel('FDD Process Categories.xlsx', sheet_name=["Detection","Diagnosis"])

# Export publication to Bibtex
names = []
collect_names = []
collect_idx = []
collect_bib = []   
for key in data:    
    names.append(data[key].stack().values.tolist())
    
titles = list(set([item for sublist in names for item in sublist]))
titles.sort()
print(len(titles))

pg = ProxyGenerator()
success = pg.ScraperAPI('c4f41f7e1a3a3e9e7a8d1a2aa0c165f6')
# proxy = FreeProxy(rand=True, timeout=1, country_id=['US']).get()
# pg.SingleProxy(http=proxy, https=proxy)
scholarly.use_proxy(pg)

# sleep_interval = 45
 
for i, name in enumerate(titles):
    print('Running '+str(i)+ ' of ' +str(len(titles)))
    query = scholarly.search_pubs(name)
    pub = next(query)
    text = scholarly.bibtex(pub)
    
    collect_bib.append(text)
    idx = re.search('{(.+?),', text).group(1)    
    collect_idx.append(idx)    
    collect_names.append(name)
    # time.sleep(sleep_interval + random()*60)
    
    output = pd.DataFrame({'Title': collect_names, 'bibtex': collect_bib, 'idx': collect_idx})
    output.to_csv('papersQuery.csv', index=False)
