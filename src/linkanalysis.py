import networkx as nx
import json

with open('links.txt') as json_file:  
	data = json.load(json_file)
# Initialize directed graph
G = nx.DiGraph()

for obj in data:
	for i in range(len(obj['totallinks'])):
		G.add_edge(obj['url'],obj['totallinks'][i])

pr = nx.pagerank(G)
with open('pr.json','w') as p_file:
	json.dump(pr,p_file)
		
h,a = nx.hits(G)
with open('hub.json','w') as h_file:
	json.dump(h,h_file)
with open('authority.json','w') as a_file:
	json.dump(a,a_file)
