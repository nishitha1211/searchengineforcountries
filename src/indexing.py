import re					#Module for using regular expressions to preprocess documents
import nltk					#Module for tokenizing and stemming 
import collections				#Module for sorting,grouping and frequency count calculation of tokens and stems
from collections import defaultdict
import time
import sys
import os
from os import listdir
from os.path import isfile, join
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import math
import json

with open('item.json') as json_file:  
    data = json.load(json_file)

lemmaindex_uncompressed = open('Index_Version1.uncompressed','w+')
lemmaindex_compressed = open('Index_Version1.compressed.bin','wb')
entire_posting1 = {}
ordered_dict_lemmas = {}
query_dict = {}
collection_size = 0
totallen = 0
cosine = 0
cosine_value = 0
totalnz = 0
docid = 0
totalnz1 = 0
cos_order_w1 = {}
cos_order_w2 = {}
query = ""
query_lemmas = []
query_list = []
lemmas = []
token_dict = {}
lemmatizer = WordNetLemmatizer()
w1_query = {}
w1_doc = {}
w1_fullqueries = []
w1_fulldoc = []
w2_fulldoc = []
w2_query = {}
w2_doc = {}
url_db = {}
w2_fullqueries = []
top_five_w1 = []
top_five_w2 = []
#headline = []
value_list1 = [] 
value_list2 = []
term_string = ""
termpointer = 0

def gamma(number):
	binaryform = str(bin(number))
	offset = binaryform[3:]
	offset_length = len(offset)
	unaryform = unary(offset_length)
	gammaform = str(unaryform) + str(offset)
	return gammaform
    
def unary(number1):
	unaryform1 = ""
	i = 0
	while i < number1:
		unaryform1 = unaryform1 + str(1)
		i += 1
	unaryform1 = unaryform1 + str(0)
	return unaryform1

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN



avg_doclen1 = 4.684039087947883

#Query Preprocessing
'''inputfile = open(mypath,"r")
queries = inputfile.readlines()
for i in range(0,len(queries)):
	if queries[i].startswith('Q'):
		j = i+1
		while j != len(queries) and queries[j] != "\n":
			query += queries[j]
			j += 1
		query_list.append(query)
		query = ""'''

#Removing Document Tags along with non alphanumerics and numbers(Preprocessing) and Tokenizing

for obj in data:
	docid +=1
	'''if docid == 536 or docid == 1250 or docid == 924:
		print(obj['url']+obj['title'])'''
	url_db[docid] = obj['url']
	collection_size += 1
	line = obj['title']
	#headline.append(line[(line.index('<TITLE>') + len('<TITLE>')):line.index('</TITLE>')])
	line = re.sub('<[^<]+>', " ", line)	
	line = re.sub('[\d]+', " ", line)
	line = re.sub('[\W]+', " ", line)
	line = nltk.word_tokenize(line.lower()) 
	processed_tokens = [word for word in line if word not in stopwords.words('english')]
	doclen = len(processed_tokens)
	totallen += doclen
	token_dict = dict(nltk.pos_tag(processed_tokens))
	#Lemmatization
	for key,value in token_dict.items():
		lemmas.append(lemmatizer.lemmatize(key,get_wordnet_pos(value)))
	lemmacount = collections.Counter(lemmas)
	maxtf = max(lemmacount.values())
	#w1 Calculation for Queries
	for word,tf in lemmacount.items():
		w1 = (0.4 + 0.6 * math.log10(tf + 0.5)/math.log10(maxtf + 1.0))
		w1_doc[word] = w1	
	#W2 Calculation for Queries
		w2 = (0.4 + 0.6 * (tf / (tf + 0.5 + 1.5 * (doclen / avg_doclen1))))
		w2_doc[word] = w2
	for word,tf in lemmacount.items():
		each_posting1 = [[docid,tf,maxtf,doclen]]
		if word in entire_posting1:
			entire_posting1[word].extend(each_posting1)
		else:
			entire_posting1[word] = each_posting1
	lemmas = []
	w1_fulldoc.append(w1_doc)
	w2_fulldoc.append(w2_doc)
	w1_doc = {}
	w2_doc = {}

#Create Index Files of lemmas
ordered_dict_lemmas= collections.OrderedDict(sorted(entire_posting1.items()))
lemmaindex_uncompressed.write("Format:LemmaTerm\tDocumentFrequency\t[DocumentId, TermFrequency, MaxTermFrequency, DocumentLength]\n")
for term, postings in ordered_dict_lemmas.items():
	lemmaindex_uncompressed.write(term+":\t"+str(len(postings))+"\t"+str(postings)+"\n")
avg_doclen = totallen/collection_size
print(avg_doclen)

#Index1Compression	
for term, postings in ordered_dict_lemmas.items():
	term_string = term_string + str(len(term)) + term
lemmaindex_compressed.write(bytearray("LemmaTerms: "+term_string+"\n\n",'utf-8'))
for term, postings in ordered_dict_lemmas.items():
	termpointer = termpointer + 1
	posting_list = []
	gapslist = []
	binary_postings = ""
	for post in postings:
		posting_list.append(post[0])
	gapslist.append(posting_list[0])
	for i in range(0,(len(posting_list)-1)):
		gapslist.append(posting_list[i+1] - posting_list[i])
	for num in gapslist:
		gamma_code = str(gamma(num))
		binary_postings = binary_postings + gamma_code

	lemmaindex_compressed.write(bytearray(binary_postings+"\n",'utf-8'))
	term_string = ""
	term_string = term_string + str(len(term)) + term
	if (termpointer % 8 == 0):
		index_pointer = len(term_string)
		lemmaindex_compressed.write(bytearray("\n"+str(index_pointer)+"\n",'utf-8'))

termpointer = 0
term_string = ""

query = sys.argv[1]

processed_query = re.sub('[\d]+', " ", query)
processed_query = re.sub('[\W]+', " ", processed_query)
query_tokens = nltk.word_tokenize(processed_query.lower())
processed_query = [word for word in query_tokens if word not in stopwords.words('english')]
query_dict = dict(nltk.pos_tag(processed_query))
for key,value in query_dict.items():
	query_lemmas.append(lemmatizer.lemmatize(key,get_wordnet_pos(value)))
query_doclen = len(query_lemmas)
query_count = collections.Counter(query_lemmas)
maxtf_query = max(query_count.values())
for qterm,tf in query_count.items():
	for term, postings in ordered_dict_lemmas.items():
		if term == qterm:
			query_df = len(postings)  
#W1 Calculation for Queries
	w1 = (0.4 + 0.6 * math.log10(tf + 0.5)/math.log10(maxtf_query + 1.0)) * (math.log10(collection_size / query_df) / math.log10(collection_size))
	w1_query[qterm] = w1	
#W2 Calculation for Queries
	w2 = (0.4 + 0.6 * (tf / (tf + 0.5 + 1.5 * (query_doclen / avg_doclen))) * math.log10(collection_size / query_df) / math.log10(collection_size))
	w2_query[qterm] = w2	
print(w1_query)

#w1_fullqueries.append(w1_query)
#w2_fullqueries.append(w2_query)
#w1_query = {} 
#w2_query = {} 
#query_lemmas = []


for key,value in w1_query.items():
	totalnz += value**2
totalnz = math.sqrt(totalnz)
for key,value in w1_query.items():
	w1_query[key] = value / totalnz
for key,value in w2_query.items():
	totalnz1 += value**2
totalnz1 = math.sqrt(totalnz1)
for key,value in w2_query.items():
	w2_query[key] = value / totalnz1
#totalnz = 0
#totalnz1 = 0

for i in range(0,collection_size):
	for key,value in w1_fulldoc[i].items():
		totalnz += value**2
	totalnz = math.sqrt(totalnz)
	for key,value in w1_fulldoc[i].items():
		w1_fulldoc[i][key] = value / totalnz
	for key,value in w2_fulldoc[i].items():
		totalnz1 += value**2
	totalnz1 = math.sqrt(totalnz1)
	for key,value in w2_fulldoc[i].items():
		w2_fulldoc[i][key] = value / totalnz1
	totalnz = 0
	totalnz1 = 0


#print("Vector Representation for Query under w1 weighting schema:")
#print("Query	"+query+":	"+str(w1_query))

#print("Vector Representation for Query under w2 weighting schema:")
#print("Query	"+query+":	"+str(w2_query))

#print("\n\n\nThe top 5 documents ranked for the query under both weighting schemes with W1 & W2:-")

for j in range(0,collection_size):
	for key,value in w1_query.items():
		for key1,value1 in w1_fulldoc[j].items():
			if key == key1:
				cosine = value * value1
		cosine_value += cosine
	name = 'Query'+ ',D' + str(j+1)
	cos_order_w1[name] = cosine_value
	cosine_value = 0
	for key,value in w2_query.items():
		for key1,value1 in w2_fulldoc[j].items():
			if key == key1:
				cosine = value * value1
		cosine_value += cosine
	name = 'Query'+ ',D' + str(j+1)
	cos_order_w2[name] = cosine_value
	cosine_value = 0
#print("Weight1:")
#print(dict(collections.Counter(cos_order_w1).most_common(5)))
top_five_w1.append(list(dict(collections.Counter(cos_order_w1).most_common(10)).keys()))
value_list1.append(list(dict(collections.Counter(cos_order_w1).most_common(10)).values()))
#print("Weight2:")
#print(dict(collections.Counter(cos_order_w2).most_common(5)))
top_five_w2.append(list(dict(collections.Counter(cos_order_w2).most_common(5)).keys()))
value_list2.append(list(dict(collections.Counter(cos_order_w2).most_common(5)).values()))
#cos_order_w1 = {}
#cos_order_w2 = {}

print("\n\n\n")	
#Calculation of rank,scoree,externalDocumentIdentifier and Headline 
for i in range(0,len(top_five_w1)):
	#print("Query" + " Characteristics[Weight1]:")
	print("RANK\t\tLinks")
	for j in range(0,10):
		top_five_w1[i][j] = int(top_five_w1[i][j].split('D')[1]) - 1
		print(str(j+1)+"\t"+"\t"+url_db[top_five_w1[i][j] + 1])
print("\n\n")

'''for i in range(0,len(top_five_w2)):
	print("Query" + " Characteristics[Weight2]:")
	print("RANK\tSCORE\tEXTERNALDOCUMENTIDENTIFIER")
	for j in range(0,5):
		top_five_w2[i][j] = int(top_five_w2[i][j].split('D')[1]) - 1
		print(str(j+1)+"\t"+str(value_list2[i][j])+"\t"+str(top_five_w2[i][j] + 1))
print("\n\n\n")'''
