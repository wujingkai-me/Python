import json
import Amazon
import os
from flask import Flask
from flask import render_template

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


@app.route("/getkeyword/<keyword>/<countryName>", methods=["get"])
@app.route("/getkeyword")
def getKeyword(keyword="", countryName="AMAZON_CO_UK"):
    if keyword == "":
        return ["Keyword Error!"]
    return Amazon.returnKeywordList(countryName, keyword)


# @app.route("/Download/<data>", methods=["get"])
# def Download(data):
#     data = json.loads(data)
#     for i in data:
#         print(data)
#
#     return ""

@app.route("/load_cache", methods=["get"])
def Load_cache():
    import os, re
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


if __name__ == "__main__":
    # automatic open brower
    # os.system(
    #     '"C:\Program Files\Google\Chrome\Application\chrome.exe" http://localhost:5000')
    app.run(debug=True)
