# -*- encoding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup

HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"}
URL = "https://www.sohu.com/a/394227970_120699377"

response = requests.get(URL, HEADER)

if response is not None:
    responseHTML = response.text
else:
    responseHTML = ""

editor = BeautifulSoup(responseHTML, "html.parser").select("article#mp-editor")
webURLList = re.findall(r"http[s]?:.*?\.(cn|com|org)/", str(editor))

File = open("WebsiteFromSoHuWallPaper.py.txt", "a+")
for url in webURLList:
    writeContent = "{}{}".format(url, "\n")
    File.write(writeContent)
File.close()
