#!/usr/bin/env python3
# -*- coding: utf-8 -*-



"""
program description:
#k-means clustering program 
#reading urls from crawled data as id's and title and descirpiton as text on which the clusters are made
#writing cluster data into csv file as url and its cluster id
#fixed k value as 12 where we are able to generate relevant clusters
    
"""    

from __future__ import print_function
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

import numpy as np
import pandas as pd
import csv, json

fileInput = "item.json"
fileOutput = "data.csv"
inputFile = open(fileInput,'r')
outputFile = open(fileOutput, 'w') 
data = json.load(inputFile) 
for obj in data:
    if 'description' in obj:
        obj["title"]= obj["title"]+obj["description"]
        obj.pop('description',None)
        print(obj)
inputFile.close() 
output = csv.writer(outputFile) 
output.writerow(data[0].keys()) 
for row in data:
     output.writerow(row.values())
          
dataset = pd.read_csv("data.csv")
document_list = []
dataset.columns = ['id', 'doc']

document_list = dataset['doc'].tolist()
id_list = dataset['id'].tolist()
dataset['doc'].isnull()
labels = dataset['id'].tolist()
true_k = np.unique(labels).shape[0]
vectorizer = TfidfVectorizer(max_df=0.5,min_df=2, stop_words='english',use_idf=True)
X = vectorizer.fit_transform(document_list)
km = KMeans(n_clusters=12, init='k-means++', max_iter=100, n_init=1)
km.fit(X)
document_Series = pd.Series(document_list)
cluster_Series = pd.Series(km.labels_)
id_Series = pd.Series(id_list)
columns_to_export=(pd.concat([id_Series,cluster_Series], axis=1)).columns
results = (pd.concat([id_Series,cluster_Series], axis=1))
results.columns = ['id', 'cluster']
results.to_csv("Clustered_results.txt", sep=',', columns=['id', 'cluster'] ,header=False,index=False,encoding='utf-8')