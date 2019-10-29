#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 11:20:11 2018

@author: bharatsimhareddyrs
"""

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import queue
import validators as validator_collection
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
import json
import sys

dictionary = {}
i = 0
List= sys.argv[1]      
for k in range(0,len(List)):
    weblink = List[k]
    unvisitedlinks = queue.Queue()
    unvisitedlinks.put(weblink)
    visitedlinks = []
    stop_words = set(stopwords.words('english'))
    ss=SnowballStemmer('english')

    def InvertedIndex(token, url):
        if token not in dictionary:
            dictionary[token] = [url]
        elif token in dictionary:
            if url not in dictionary[token]:
                dictionary[token].append(url)
  
    def tokenizer(soup, url):
        for paragraph in soup.findAll('p'):
            sentence = paragraph.text
            words = word_tokenize(sentence)
            for w in words:
                token = ss.stem(w)
                if token not in stop_words:
                    InvertedIndex(token, url)

    def fetchpage(url):
        parsed_uri = urlparse(url)
        baseurl = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        try:
            req = Request(url)
            html_page = urlopen(req)
        except:
            print('Error')
            
        soup = BeautifulSoup(html_page, "lxml")
        tokenizer(soup, url)
        for link in soup.findAll('a'):
            url = str(link.get('href'))
            if url.startswith('http') and url not in visitedlinks:
                unvisitedlinks.put(url)
            elif url.startswith('/'):
                url = baseurl + url
                if url not in visitedlinks:
                    unvisitedlinks.put(url)
    num = sys.argv[2]
    while i < int(num):
        url = unvisitedlinks.get()
        if validator_collection.url(url) and url not in visitedlinks:
            try:
                fetchpage(url)
                i = i+1
                visitedlinks.append(url)
            except:
                print('Error')
        else:
            print('Invalid URL!')    
    break

with open('invindex.json', 'w') as file:
    json.dump(dictionary, file)    