import requests
import os
import json
from bs4 import BeautifulSoup
from collections import OrderedDict



#proxies = {'https': 'https://don:techies2k12@172.16.8.22:3128/'}

def getApp(app_link):

    file = open(r'C:\Users\User\Desktop\IR\Package\APP.json','w',encoding='utf-8')
    file.write('{"Apps":[')
    for app in app_link:
        ordict = OrderedDict()
        #handle = requests.get(app, proxies=proxies) #if proxies are required.
		handle = requests.get(app)
        soup = BeautifulSoup(handle.text, 'html.parser')
        name = str(soup.find_all('div', class_ = "id-app-title")[0].text)
        ordict["Name"] = name
        print(name)
        description = str(soup.find_all('div', jsname = "C4s9Ed")[0].text)
        ordict["Description"] = description
        reviews = soup.find_all('div', class_ = "review-body with-review-wrapper")#review-body with-review-wrapper
        for index,review in enumerate(reviews):
            ordict["Review "+str(index)] = str(review.text)
        rating = str(soup.find_all('div', class_ = "score")[0].text)
        download = str(soup.find_all('div', itemprop = "numDownloads")[0].text)
        ordict["Download"] = download.split("-")[0].replace(",","").replace(" ","")
        print(ordict["Download"])
        ordict["Rating"] = rating
        ordiink"] = app
        json.dump(ordict,file)
        file.write(',\n')

    file.write(']}')
    file.close()ct["L


def getAppLink(link,depth):
    result = []
    if depth >= 1:
        handle = requests.get(link)
        soup = BeautifulSoup(handle.text, 'html.parser')
        all_link = [a["href"] for a in soup.find_all('a', href=True)]
        app_link = ['https://play.google.com/' + a for a in list(set(all_link)) if "id" in a]
        for app in app_link:
            in_handle = requests.get(app)
            in_soup = BeautifulSoup(in_handle.text, 'html.parser')
            name = in_soup.find_all('div', class_ = "id-app-title")
            if name:
                result += [app]
            else:
                result += getAppLink(app,depth-1)
    return result



#link = "https://play.google.com/store/apps?hl=en"\
link = "https://play.google.com/store/apps/top"
#app_links = list(set(getAppLink(link,1)))
#for app_link in app_links:
#    print(app_link)
file = open(r'C:\Users\User\Desktop\IR\Package\topchart.txt','r')
app_link = file.read().split("\n")
getApp(app_link)

