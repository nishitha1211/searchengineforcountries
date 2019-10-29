#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 11:26:19 2018

@author: bharatsimhareddyrs
"""

import json
from nltk.stem import SnowballStemmer

ss = SnowballStemmer('english')
with open('invindex.json', 'r') as file:
    dictionary = json.load(file)

query = input('query:')
tokens  = query.split()
links=[]
try:
    for keyword in tokens:
        key = ss.stem(keyword)
        links.append(dictionary[key])
    result=set(links[0]).intersection(*links[1:])
    print('search results: ')
    print(result)

except:
    print('No results')