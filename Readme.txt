1.The project folder should contains source and data folders.Source folder contains all source files and data folder contains all data files that are the input and output for several programs in source folder

2.For implementing crawling i.e scrapy folder pp, do cd pp and then type command 'scrapy crawl gh -o item.json'[For installing scrapy,the command is pip3 install scrapy] and the outputs are item.json and links.txt 

3.Similarly,the crawleddata.py can be implemented by 'python crawleddata.py' and give urls.Similarly,tokenindex.py and tokenindexsearch.py can be run with python run command

4.The indexing.py can be run by python run command.It takes items.json as input and outputs the index files as compressed formats
and url dictionary as db.json

5.The linkanalysis.py can be run by python run command.It takes links.txt and outputs pageranks i.e pr.json and hubs and authority scores as authority.json and hub.json

6.The cluster.py can be run by python run command.It takes items.json as input and outputs Clustered_results.txt.

7.The QueryExpansion.py can be run by python run command and query as commandline argument.[install pandas and constant by usind pip command]

8.In the UI flder,Run the home.html file using any browser(Chrome preferably).  
