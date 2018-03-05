# Web-Crawler

An application developed to facilitate search for data scrapped from specified website (Play Store).The search engine returns the top list of apps based on the number of downloads and the reviews provided by the users.

WebCrawl.py file uses BeautifulSoup library to hit the website and fetches the necessary information such as Name, Description, Reviews and Downloads to feed them into AppJson file.

Rank.py file is used to return the top k matches for the provided query. It uses TfidfVectorizer library to generate the term document matrix and similarities are calculated using cosine similarity library. Finally the top k similarities are ranked and the relevant links are returned.

App.py builds the UI part of the application using Tkinter Library.

Note: If the network from which HTTP Requests are sent needs to bypass using proxies, uncomment the proxy line in WebCrawl.py file

The example URL used here is google play store and we hit the topcharts page, based on the given search words relevant top k apps are returned.


