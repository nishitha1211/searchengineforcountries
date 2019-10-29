from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import queue
import validators as validator_collection
import os.path

print("Please enter the URL: ")
websitelink = input()
unvisitedpages = queue.Queue()
unvisitedpages.put(websitelink)
visitedhyperlinks = []

i=0

def getpage(url):
    global i
    parsed_uri = urlparse(url)
    baseurl = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    try:
        requests = Request(url)
        htm_page = urlopen(requests)
    except:
        print('error loading this url:',url)  
    page = BeautifulSoup(htm_page, "lxml")
    for script in page(["script", "style"]):
        script.decompose()
    text = page.get_text()
    lines = (line.strip() for line in text.splitlines())
    text = (phrase.strip() for line in lines for phrase in line.split("  "))
    path='/Users/bharatsimhareddyrs/crawled/'
    completefname = os.path.join(path,"crawled_data_"+str(i))  
    with open(str(completefname), 'w',encoding="utf-8") as output:
        output.write(url+"\n")
        output.write(str(page.html))
    i+=1
    for hyperlink in page.findAll('a'):
        url = str(hyperlink.get('href'))
        if url.startswith(websitelink) and url not in visitedhyperlinks:
            unvisitedpages.put(url)
        elif url.startswith('/'):
            url = baseurl + url
            if url not in visitedhyperlinks:
                unvisitedpages.put(url)

while not unvisitedpages.empty():
    url = unvisitedpages.get()
    if validator_collection.url(websitelink) and url not in visitedhyperlinks:
        try:
            getpage(url)
            visitedhyperlinks.append(url)     
        except Exception as e:
            print(' error visiting URL')
            print(e)
    else:
        print('invalid URL!')
        
print(visitedhyperlinks)
print("count", str(len(visitedhyperlinks)))
