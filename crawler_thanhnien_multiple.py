import time

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json


def dumpContentJson(my_data, name):
    jsonString = json.dumps(my_data)
    jsonFile = open(name + ".json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()


def getListPage(min, max):
    cmsLinks = []
    cmsRange = list(range(min, max))
    urlList = []
    count = 1
    baseUrl = "https://thanhnien.vn/cong-nghe-game/tin-tuc/?trang="
    for page_num in cmsRange:
        urlList.append(baseUrl + str(page_num))
    for url in urlList:
        data = requests.get(url)
        html = BeautifulSoup(data.text, 'html.parser')
        articles = html.select("article", {"class": "story"})
        for article in articles:
            articleLink = article.find("a", {"class": "story__title cms-link"})
            cmsLinks.append(articleLink.get_attribute_list("href")[0])
        print("Get link: " + str(count) + "/" + str(max) + "\n")
        count += 1
    return cmsLinks


def getPageContent(cmsLinks):
    output = []
    count = 1
    for url in cmsLinks:
        data = requests.get(url)
        html = BeautifulSoup(data.text, 'html.parser')
        body = html.find("div", {"id": "abody"})

        if body is None:
            continue
        body = body.find_all("p")
        title = html.find("h1", {"class": "details__headline cms-title"}).text
        content = ""
        for p in body:
            content += p.getText()
        dumpContentJson({
            "url": url,
            "title": title,
            "content": content
        }, "storage/cms_content_" + str(count))
        print("Get data: " + str(count) + "/" + str(len(cmsLinks)) + "\n")
        count += 1
    return output


cmsLinks = getListPage(1, 2)
content = getPageContent(cmsLinks)
print("Got " + str(len(content)) + "item")
dumpContentJson(content, "cms_content")
