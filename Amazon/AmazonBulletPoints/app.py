import json
import time
import Amazon
import os
from flask import Flask
from flask import render_template, request


import requests as __requests
import re as __re


def __getCorrectlyURL(coutryName: str, keyword: str) -> str:
    correctlyURL = {
        "AMAZON_CO_UK": "https://completion.amazon.co.uk/api/2017/suggestions?limit=20&prefix=%s&suggestion-type=WIDGET&suggestion-type=KEYWORD&page-type=Gateway&alias=aps&site-variant=desktop&version=3&event=onKeyPress&wc=&lop=en_GB&last-prefix=%s&avg-ks-time=10554&fb=1&session-id=262-6625362-2272630&request-id=4FJ7XRXTY8Y1PCBYE1F5&mid=A1F83G8C2ARO7P&plain-mid=3&client-info=amazon-search-ui" % (keyword, keyword),
        "AMAZON_FR": "https://completion.amazon.fr/api/2017/suggestions?limit=11&prefix=%s&suggestion-type=WIDGET&suggestion-type=KEYWORD&page-type=Gateway&alias=aps&site-variant=desktop&version=3&event=onKeyPress&wc=&lop=fr_FR&last-prefix=%s&avg-ks-time=8016&fb=1&session-id=259-0596377-8269066&request-id=XTGS8YC5NK80TVD1GNMD&mid=A13V1IB3VIYZZH&plain-mid=5&client-info=amazon-search-ui" % (keyword, keyword),
        "AMAZON_DE": "https://completion.amazon.de/api/2017/suggestions?limit=11&prefix=%s&suggestion-type=WIDGET&suggestion-type=KEYWORD&page-type=Gateway&alias=aps&site-variant=desktop&version=3&event=onKeyPress&wc=&lop=en_GB&last-prefix=%s&avg-ks-time=2360&fb=1&session-id=262-2215706-7186424&request-id=SRJ59TEPP7V20EM9B9JH&mid=A1PA6795UKMFR9&plain-mid=4&client-info=amazon-search-ui" % (keyword, keyword),
        "AMAZON_IT": "https://completion.amazon.it/api/2017/suggestions?limit=11&prefix=%s&suggestion-type=WIDGET&suggestion-type=KEYWORD&page-type=Gateway&alias=aps&site-variant=desktop&version=3&event=onKeyPress&wc=&lop=it_IT&last-prefix=%s&avg-ks-time=648&fb=1&session-id=259-4805383-5190563&request-id=2JDWZAVK6808K7D6HMTA&mid=APJ6JRA9NG5V4&plain-mid=35691&client-info=amazon-search-ui" % (keyword, keyword),
        "AMAZON_ES": "https://completion.amazon.es/api/2017/suggestions?limit=11&prefix=%s&suggestion-type=WIDGET&suggestion-type=KEYWORD&page-type=Gateway&alias=aps&site-variant=desktop&version=3&event=onKeyPress&wc=&lop=es_ES&last-prefix=%s&avg-ks-time=1132&fb=1&session-id=262-6917168-3211857&request-id=VQ6WF6146MPKXQNSNGPJ&mid=A1RKKUPIHCS9HS&plain-mid=44551&client-info=amazon-search-ui" % (keyword, keyword)}

    return correctlyURL[coutryName]


def __getReuqestsToURL(url: str) -> object:
    try:
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"
        }
        return __requests.get(url, headers=header, timeout=3)
    except:
        print("getRequestsToURL出错了! ")
        return None


def __processResponseData(response: object):
    return response.text.\
        replace("false", "False").\
        replace("null", "None").\
        replace("true", "True")


def __getPopularity(value: str, keywordURL: str) -> str:
    response = __getReuqestsToURL(keywordURL + value.replace(" ", "+"))
    if response == None:
        return "-1"

    text = response.text.replace("\n", "")

    try:
        result = __re.findall(
            r"a-spacing-top-small.*?</span>", text, __re.MULTILINE)
        result = __re.findall(r"<span>.*</span>", result[0])

        distinct = __re.findall(r"1-[0-9]{1,3}", result[0])  # 去掉 由 -连接的数字

        result = result[0].replace("&nbsp;", " ").replace(distinct[0], "")
        strNum = ""

        for item in result:
            if "0" <= item < "9":
                strNum += item
            if item == "-":
                strNum = ""

        return strNum
    except Exception as e:
        return "-2"


def returnKeywordList(countryName: str, keyword: str):
    url = __getCorrectlyURL(countryName, keyword)
    response = __getReuqestsToURL(url)
    if response == None:
        return []
    keywordData = eval(__processResponseData(response))
    keyword = [[i["value"], 0]
               for i in keywordData["suggestions"]]
    if countryName == "AMAZON_CO_UK":
        keywordURL = "https://www.amazon.co.uk/s?k="
    elif countryName == "AMAZON_FR":
        keywordURL = "https://www.amazon.fr/s?k="
    elif countryName == "AMAZON_DE":
        keywordURL = "https://www.amazon.de/s?k="
    elif countryName == "AMAZON_IT":
        keywordURL = "https://www.amazon.it/s?k="
    else:
        keywordURL = "https://www.amazon.es/s?k="

    for key in keyword:
        value = key[0]  # 关键词
        popular = __getPopularity(value, keywordURL)
        key[1] = popular
    return keyword


def getAtoZList():
    aToZ = list()
    for i in range(65, 91):
        aToZ.append(chr(i).lower())

    return aToZ


app = Flask(__name__)


@app.route("/")
def root():
    return render_template("html/index.html")


@app.route("/English")
def English():
    return render_template("html/EnglishRemove.html")


@app.route("/Format")
def Format():
    return render_template("html/Format.html")


@app.route("/bullet")
def Bullet():
    return render_template("html/bullet.html")


@app.route("/Tools")
def Tools():
    return render_template("html/tools.html")


@app.route("/shangchuan")
def shangchuan():
    paths = os.listdir("static/bullets/")
    print(paths)
    return render_template("html/Download.html", path=paths)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        savePath = "static/bullets/"
        f = request.files['file']
        if "__" not in f.filename:
            return "file uploaded error! Could file name is incorrectly !"
        f.save(savePath + f.filename)
        gcc()
        writeLOG("UPLOAD", path="static/bullets/" + f.filename)
        return 'file uploaded successfully'
    else:
        return render_template('upload.html')


@app.route("/getkeyword/<keyword>/<countryName>", methods=["get"])
@app.route("/getkeyword")
def getKeyword(keyword="", countryName="AMAZON_CO_UK"):
    if keyword == "":
        return ["Keyword Error!"]
    return returnKeywordList(countryName, keyword)


# @app.route("/Download/<data>", methods=["get"])
# def Download(data):
#     data = json.loads(data)
#     for i in data:
#         print(data)
#
#     return ""

@app.route("/load_cache", methods=["get"])
def Load_cache():
    import os
    import re
    files = os.listdir('static/bullets')

    data = {}
    for file in files:
        name = file.replace(".txt", "")
        name = name.replace(re.findall(r"__.*", name)[0], "")

        f = open("static/bullets/" + file, "r+", encoding="utf-8")
        data[name] = {}
        data[name]["CN"] = file.split("__")[1].replace(".txt", "")
        data[name]["content"] = f.readlines()
        f.close()

    return data


def writeLOG(operate, path):
    f = open("static/DEL.LOG", "a+")
    clock = str(time.localtime().tm_year) + " " + str(time.localtime().tm_mon) + " " + \
        str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min) + \
        ":" + str(time.localtime().tm_sec)
    f.write("[" + operate + "]\t" + path + "\t" + clock)
    f.close()


def gcc():
    paths = os.listdir("static/bullets/")
    for path in paths:
        sizes = os.path.getsize("static/bullets/" + path)
        if sizes <= 4000:
            os.system("del " + ".\\static\\bullets\\" + path)
            writeLOG("DELETE", "static/bullets/" + path)


if __name__ == "__main__":
    # automatic open brower
    # os.system(
    #     '"C:\Program Files\Google\Chrome\Application\chrome.exe" http://localhost:5000')
    app.run(debug=True)
