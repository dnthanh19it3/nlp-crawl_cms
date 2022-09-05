import time

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json

url = 'https://daotao.vku.udn.vn/gv'
data = requests.get(url)

my_data = []

html = BeautifulSoup(data.text, 'html.parser')
result = html.select("tr", {"class": "even pointer"})

for tr in result:
    if(len(tr.select("td")) > 2):
        my_data.append({
            "subject": tr.select("td")[1].getText().strip(),
            "tuttor": tr.select("td")[2].getText().strip(),
            "room": tr.select("td")[3].getText().strip().split("|")[0],
            "time": tr.select("td")[3].getText().strip().split("|")[1]
        })

jsonString = json.dumps(my_data)
jsonFile = open("data.json", "w")
jsonFile.write(jsonString)
jsonFile.close()

print(my_data)



# print(html, result)

# articles = html.select('a.post-card')
#
# for article in articles:
#
#     title = article.select('.card-title')[0].get_text()
#     excerpt = article.select('.card-text')[0].get_text()
#     pub_date = article.select('.card-footer small')[0].get_text()
#
#     my_data.append({"title": title, "excerpt": excerpt, "pub_date": pub_date})
#
# pprint(my_data)